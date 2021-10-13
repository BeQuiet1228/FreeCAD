#-*- coding: utf-8 -*-
import CustomParameterGui.DlgCustomeParameter
import CustomParameterGui.searchTool
import PySide
from PySide import QtGui
import string
import json
import re
import FreeCAD,FreeCADGui
from Modeling.Common.Tools import DocumentTools,ObjectsTools,CoordinateSystemTools
import DynamicData
from Modeling.Common.Tools import UnitTools
import INHighLighter
import time

# 请认真阅读 https://wiki.freecadweb.org/Expressions（FreeCAD的Expressions的文档）！！！
# 主要流程为：doInit -> PreDoParam ->  doHandleListParams -> deleteNotDefinedParam

# 该文件负责参数定义，思路为获取变量定义的文本，预处理去除注释空格，然后对字符串进行分隔，\
# 得到单独的变量字符串，然后对变量字符串进行识别分类，利用addProperty添加到FreeCAD中，\
# 分类的原因是因为不同的类型对应不同的属性，比如mm，cm与KV，A等对应不同类型的属性，\
# 属性的具体介绍见 https://wiki.freecadweb.org/Property_editor/zh-cn 

# 注意:
# 1. self.paramObj.DynamicData.append()， 该stringList的函数调用是无效的，\
#    只能通过"="来赋值，所以定义self.listOfParamDefined来记录已经定义的变量
# 2. 由于属性的种类比较多，但是属性提供的方法不一致，对变量进行操作时，可以使用 self.paramObj.ExpressionEngine

# @LZG 于 2020-10-12 对此处代码进行重构，对主要流程的代码进行封装和梳理，对变量定义做了规范化处理,\
# 但大多辅助用的函数沿用原有代码
from Modeling.Modeling2D.Tools import Tools2D


class ParamItem:
    '''
    参数类
    '''
    def __init__(self, n, t, v):
        self._name = n
        self._type = t
        self._value = v

    def getType(self):
        return self._type

    def getName(self):
        return self._name

    def getValue(self):
        return self._value


class SearchTool(QtGui.QDialog):
    '''
    查找功能
    '''
    def __init__(self, main_ui, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = CustomParameterGui.searchTool.Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.find)
        self.main_ui = main_ui

    def find(self):
        findText = self.ui.lineEdit.text()
        temp = self.main_ui.textEdit_defintParam.find(findText,
                                                      PySide.QtGui.QTextDocument.FindBackward |
                                                      PySide.QtGui.QTextDocument.FindWholeWords)

        if self.main_ui.textEdit_defintParam.find(findText):
            palette = self.main_ui.textEdit_defintParam.palette()
            # palette.setColor(QtGui.QPalette.Highlight, palette.color(QtGui.QPalette.Active, QtGui.QPalette.Highlight))
            self.main_ui.textEdit_defintParam.setPalette(palette)
        else:
            pass


class CustomeParameterMain(QtGui.QDialog):
    def __init__(self, flagIsFromM3d=False, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = CustomParameterGui.DlgCustomeParameter.Ui_Dialog_CustomParameterDlg()
        self.ui.setupUi(self)
        self.setModal(False)

        self.paramObj = ObjectsTools.getParamObj()
        self.flagColorChange = True
        self.curColor = QtGui.QColor(0, 0, 0)
        # 记录初始参数值并设置到UI界面上
        self.lastInfo = FreeCAD.ActiveDocument.Company
        self.ui.textEdit_defintParam.setPlainText(FreeCAD.ActiveDocument.Company)
        if self.ui.textEdit_defintParam.toPlainText() == "":
            self.ui.textEdit_defintParam.setPlainText(self.getParametersFromParamObj())
        # 连接信号与槽
        self.ui.pushButton_ok.clicked.connect(self.onOkBtn)
        self.ui.pushButton_cancel.clicked.connect(self.onCancelBtn)
        self.ui.pushButton_help.clicked.connect(self.onHelpBtn)
        self.ui.pushButton_redo.clicked.connect(self.__slotOfRedo)
        self.ui.pushButton_undo.clicked.connect(self.__slotOfUndo)
        self.ui.pushButton_find.clicked.connect(self.__find)
   
        # 已经定义的变量列表，这个是原有代码定义的，并不清楚有什么用
        self.listOfParamNameAndValueDefined = ['DynamicData', 'ExpressionEngine', 'Label', 'Proxy', 'Type',"DX1","DX2","DX3"]
        # 记录之前被定义的变量，不要去修改这个list，该list仅用于记录使用
        self.lastListParamDefined = self.paramObj.DynamicData
        # 成功定义的变量
        self.listOfParamDefined = self.paramObj.DynamicData
        # 记录之前变量的名字以及对应的值，结果存放于self.dict_last
        self.recordLastParams()

        if flagIsFromM3d:
            self.lastInfo = ""
        # 给textEdit设置Highlighter
        highlighter = INHighLighter.Highlighter(self.ui.textEdit_defintParam.document())

        # 记录一次验证时，错误的变量列表
        self.errorParams = []

    def onCancelBtn(self):
        self.close()

    def onOkBtn(self):
        # 判断变量输入是否有更新？
        Paraminfo = self.ui.textEdit_defintParam.toPlainText()
        # 如果变量没有变化
        if Paraminfo == self.lastInfo:
            self.close()
            return
        else:
            # 初始化
            self.doInit()
            # 对变量字符串进行预处理，然后生成字符列表
            paramsStr = self.PreDoParam(Paraminfo)
            self.curListParams = self.getParamAndValues(paramsStr)
            lastParamStr = self.PreDoParam(self.lastInfo)
            self.lastListParams = self.getParamAndValues(lastParamStr)
            sayzError("参数-成功获取参数列表")

            errors = self.checkForSyntaxErrors(self.curListParams)
            if len(errors) != 0:
                self.ui.textEdit_ValidInfo.setPlainText(errors)
                return

            self.doHandleListParams()
            sayzError("参数-处理参数列表成功")
            # 删除未定义，但是已存在于obj的属性
            self.deleteNotDefinedParam()
            sayzError("参数-删除参数成功")

            self.getNamesOfAllChangedParams()
            sayzError("发生改变的属性列表"+str(FreeCAD.ActiveDocument.PropertiesChanged))

            if self.ui.textEdit_ValidInfo.toPlainText() == "":
                FreeCAD.ActiveDocument.Company = self.ui.textEdit_defintParam.toPlainText()
                self.paramObj.DynamicData = self.listOfParamDefined
                self.close()
            # 定义出错
            else:
                FreeCAD.ActiveDocument.Company = self.removeErrorParam()

            # 更新体并进行布尔运算
            FreeCAD.ActiveDocument.recompute()
            DocumentTools.updateBoolean()
            # 一个变量名重复定义时，只取最后一个
            FreeCAD.ActiveDocument.Company = self.deleteRepeat()
            FreeCAD.ActiveDocument.recompute()
            if FreeCAD.ActiveDocument.Comment == "2D":
                model_list = Tools2D.getAllModelObjects()
                for i in model_list:
                    if i.Type == Tools2D.ObjectType.AreaPolygonal:
                        Tools2D.recomputeAreaPolygon(i)
                    i.recompute()
                FreeCADGui.runCommand("CreateM2D")


    def getSomething(self):
        '''
        这里保留原有代码获取未改变、改变、新增、删除变量列表的方式
        '''
        # 两个list相同的元素集合，也就是未曾变化的值
        self.listParamsSame = [x for x in self.curListParams if x in self.lastListParams]
        sayz("self.listParamsSame: "+str(self.listParamsSame)+"\n")

        # 两个list不同元素的集合
        self.listParamsDiff = [y for y in (self.curListParams + self.lastListParams) if y not in self.listParamsSame]
        sayz("self.listParamsDiff: "+str(self.listParamsDiff)+"\n")

        # 新增加的元素集合
        self.listParamAdd = [z for z in self.curListParamsDiff if z in self.curListParams]
        sayz("self.listParamAdd: " + str(self.listParamAdd)+"\n")

    def doInit(self):
        '''
        初始化，将错误信息归零，向变量列表中添加DX1，DX2，DX3，变量列表定义为 self.listOfParamObj
        '''
        # 验证的错误信息
        self.errorText = ""
        self.errorParams = []
        # 重置验证消息
        self.ui.textEdit_ValidInfo.setPlainText("")
        # 存放已经定义变量的名称、类型、值
        self.listOfParamObj = []
        if hasattr(self.paramObj, "DX1"):      
            self.listOfParamObj.append(ParamItem("DX1",UnitTools.SupportUnitType.Length,str(getattr(self.paramObj,"DX1").Value)))
        if hasattr(self.paramObj, "DX2"):
            if self.paramObj.Document.CoordinateSystem==CoordinateSystemTools.CoordinateType.Rectangular or self.paramObj.Document.CoordinateSystem==CoordinateSystemTools.CoordinateType.Cylindrical:
                self.listOfParamObj.append(ParamItem("DX2",UnitTools.SupportUnitType.Length,str(getattr(self.paramObj,"DX2").Value)))
            else:
                self.listOfParamObj.append(ParamItem("DX2",UnitTools.SupportUnitType.Angle,str(getattr(self.paramObj,"DX2"))))
        if hasattr(self.paramObj, "DX3"):
            if self.paramObj.Document.CoordinateSystem==CoordinateSystemTools.CoordinateType.Rectangular or self.paramObj.Document.CoordinateSystem==CoordinateSystemTools.CoordinateType.Polar:
                self.listOfParamObj.append(ParamItem("DX3",UnitTools.SupportUnitType.Length,str(getattr(self.paramObj,"DX3").Value)))
            else:
                self.listOfParamObj.append(ParamItem("DX3",UnitTools.SupportUnitType.Angle,str(getattr(self.paramObj,"DX3"))))

    def PreDoParam(self, Paraminfo):
        '''
        对变量文本进行预处理，首先去掉所有的注释与空格，然后将单位替换为标准单位
        '''
        # 预处理
        # 1.去掉注释
        Paraminfo = re.sub(r"[!|！][^\n]*","",Paraminfo)
        # 2.去掉换行符以及多余空格
        infoWithOutSpaceOrEnter = Paraminfo.replace(" ","").replace("\n","").replace("\r","").replace("\t","")
        
        # 处理**这样的操作符

        # 处理小数点2.->2.0
        infoWithOutSpaceOrEnter=re.sub(r"(?<=\d)\.(?!\d)",".0",infoWithOutSpaceOrEnter)
        # 3.将一些单位转化为标准单位,例如：kilo volt->kv
        # 长度
        infoWithOutSpaceOrEnter=re.sub(r"(?<=[\d])pico\b","*1.0e-12m",infoWithOutSpaceOrEnter,flags=re.IGNORECASE)
        infoWithOutSpaceOrEnter=re.sub(r"(?<=[\d])nano\b","*1.0e-9m",infoWithOutSpaceOrEnter,flags=re.IGNORECASE)
        infoWithOutSpaceOrEnter=re.sub(r"(?<=[\d])micro\b","*1.0e-6m",infoWithOutSpaceOrEnter,flags=re.IGNORECASE)

        infoWithOutSpaceOrEnter=re.sub(r"(?<=[\d])mils\b","*2.54e-5m",infoWithOutSpaceOrEnter,flags=re.IGNORECASE)
        infoWithOutSpaceOrEnter=re.sub(r"(?<=[\d])mil\b","*2.54e-5m",infoWithOutSpaceOrEnter,flags=re.IGNORECASE)
        infoWithOutSpaceOrEnter=re.sub(r"(?<=[\d])inches\b","*2.54e-2m",infoWithOutSpaceOrEnter,flags=re.IGNORECASE)
        infoWithOutSpaceOrEnter=re.sub(r"(?<=[\d])feet\b","*2.54e-2m",infoWithOutSpaceOrEnter,flags=re.IGNORECASE)
        infoWithOutSpaceOrEnter=re.sub(r"(?<=[\d])foot\b","*2.54e-2m",infoWithOutSpaceOrEnter,flags=re.IGNORECASE)

        infoWithOutSpaceOrEnter=re.sub(r"(?<=[\d])kilometer\b","*1.0e+3m",infoWithOutSpaceOrEnter,flags=re.IGNORECASE)
        infoWithOutSpaceOrEnter=re.sub(r"(?<=[\d])kilometers\b","*1.0e+3m",infoWithOutSpaceOrEnter,flags=re.IGNORECASE)

        # 时间
        infoWithOutSpaceOrEnter=re.sub(r"(?<=[\d])sec\b","s",infoWithOutSpaceOrEnter,flags=re.IGNORECASE)
        infoWithOutSpaceOrEnter=re.sub(r"(?<=[\d])second\b","s",infoWithOutSpaceOrEnter,flags=re.IGNORECASE)

        infoWithOutSpaceOrEnter=re.sub(r"(?<=[\d])NANOSECONDS\b","*10.0e-7ms",infoWithOutSpaceOrEnter,flags=re.IGNORECASE)
        infoWithOutSpaceOrEnter=re.sub(r"(?<=[\d])NANOSECOND\b","*10.0e-7ms",infoWithOutSpaceOrEnter,flags=re.IGNORECASE)
        infoWithOutSpaceOrEnter=re.sub(r"(?<=[\d])ns\b","*10.0e-7ms",infoWithOutSpaceOrEnter,flags=re.IGNORECASE)
        # 电流
        infoWithOutSpaceOrEnter=re.sub(r"(?<=[\d])amp\b","a",infoWithOutSpaceOrEnter,flags=re.IGNORECASE)
        # 电压
        infoWithOutSpaceOrEnter=re.sub(r"(?<=[\d])volt\b","v",infoWithOutSpaceOrEnter,flags=re.IGNORECASE)
        infoWithOutSpaceOrEnter=re.sub(r"(?<=[\d])kilovolts\b","*1.0e+3v",infoWithOutSpaceOrEnter,flags=re.IGNORECASE)
        infoWithOutSpaceOrEnter=re.sub(r"(?<=[\d])kilovolt\b","*1.0e+3v",infoWithOutSpaceOrEnter,flags=re.IGNORECASE)
        # 角度
        infoWithOutSpaceOrEnter=re.sub(r"(?<=[\d])radian\b","rad",infoWithOutSpaceOrEnter,flags=re.IGNORECASE)
        infoWithOutSpaceOrEnter=re.sub(r"(?<=[\d])degree\b","deg",infoWithOutSpaceOrEnter,flags=re.IGNORECASE)
        infoWithOutSpaceOrEnter=re.sub(r"(?<=[\d])degrees\b","deg",infoWithOutSpaceOrEnter,flags=re.IGNORECASE)
        #频率
        infoWithOutSpaceOrEnter=re.sub(r"(?<=[\d])kilohertz\b","*1.0e+3hz",infoWithOutSpaceOrEnter,flags=re.IGNORECASE)

        return infoWithOutSpaceOrEnter

    def doHandleListParams(self):
        '''
        将变量文本转化为变量，并存放在变量列表中
        '''
        # 初始化改变的变量，这是一个C++的对象
        FreeCAD.ActiveDocument.PropertiesChanged = ""
        # 进度条
        progress_bar=FreeCAD.Base.ProgressIndicator()
        progress_bar.start("Start Validing Param...", len(self.curListParams))

        # 已添加的Str内容
        self.thisHandleAddSuccess="\n"

        for paramItem in self.curListParams:
            # sayzError("参数-当前处理的变量：" + str(paramItem))
            try:
                if paramItem=="":
                    continue
                # 利用setExpression的机制来进行赋值以及报错处理
                paramItemNameAndValue = paramItem.split("=")
                paramName = paramItemNameAndValue[0]
                paramValue = paramItemNameAndValue[1]
                # 整形，以i-n开头的变量的意义为整形变量，如果时其他类型，计算程序会强转为整形
                if paramItem.lower()[0] in ["i","j","k","l","m","n"]:
                    [normalValue,typeOfThisParam]=self.getNormalParamValueAndTypeOfIt(paramName,paramValue,self.listOfParamObj)
                    self.addParam(paramName,normalValue,typeOfThisParam)
                    # 这行代码的作用是什么？或者说这个list的作用是什么
                    self.listOfParamObj.append(ParamItem(paramName,typeOfThisParam,self.getValueOfQuantity(self.paramObj,paramName)))
                else:
                    [normalValue,typeOfThisParam]=self.getNormalParamValueAndTypeOfIt(paramName,paramValue,self.listOfParamObj)
                    if typeOfThisParam == UnitTools.SupportUnitType.STRING:
                        # 去掉单位和已经定义的变量，然后重新进行一次判断
                        # 这里为什么要这样操作？？？
                        valueWithoutUnit = self.removeAllUnits(paramValue)
                        valueWithoutUnit = self.removeAllParamsList(valueWithoutUnit)
                        [normalValueWithoutUnit,typeWithoutUnit] = self.getNormalParamValueAndTypeOfIt(paramName,valueWithoutUnit,self.listOfParamObj)
                        if typeWithoutUnit == UnitTools.SupportUnitType.STRING:
                            self.errorHandle(self.curListParams.index(paramItem)+1,paramName)
                            continue
                    self.addParam(paramName,normalValue,typeOfThisParam)
                    self.listOfParamObj.append(ParamItem(paramName,typeOfThisParam,self.getValueOfQuantity(self.paramObj,paramName)))
                self.thisHandleAddSuccess=self.thisHandleAddSuccess+paramItem+";\n"
                # 添加已经定义的属性名(需要判断是否以及存在)
                if paramName not in self.listOfParamNameAndValueDefined:
                    self.listOfParamNameAndValueDefined.append(paramName)
                progress_bar.next()   
            except:
                # sayzError("参数-进入到异常处理部分")
                self.errorHandle(self.curListParams.index(paramItem)+1,paramName)
        progress_bar.stop()

    def getNormalParamValueAndTypeOfIt(self,paramName,paramValue,isInt=False):
        '''
        @ brief 将表达式的值变为标准的值例如，s1=rrr->s1=Param.rrr
        @ paramName:变量名
        @ paramValue:变量的值
        @ isint:是否类型是否为整数
        '''
        mathSymbol=["e","pi",
                    "acos","asin","atan","atan2","cos","cosh","sin","sinh","tan","tanh",\
                    "exp","log","log10","pow","sqrt",\
                    "abs","ceil","floor","mod","round","trunc",\
                    "average","count","max","min","stddev","sum"]
        # 在此处添加逗号，但是不确定这样的添加会不会导致其他问题
        operators=["+","-","*","/","^","(",")",":", ","]
        # 科学计数法的e
        otherOperators=["e"]
        resultValue=""
        listOfResultType=[]

        word=""
        for i in range(len(paramValue)):
            
            #运算符
            if paramValue[i] in operators:
                # 处理上一个word
                if word!="":
                    # sayzError("观察:  " + str(word) + "\n")
                    if word.lower() in mathSymbol:
                        resultValue = resultValue + word.lower()
                        listOfResultType.append(UnitTools.SupportUnitType.Float)
                    else:
                        [resultValue,listOfResultType] = self.handleLastWord(paramName,resultValue,listOfResultType,word)
                    word=""
                resultValue = resultValue + paramValue[i]
            # 9E-9类似这种E前后没有运算符,且e前面是数字
            elif  paramValue[i].lower() in otherOperators and i!=0 and paramValue[i-1].isdigit():
                # 处理上一个word
                if word!="":
                    if word.lower() in mathSymbol:
                        resultValue=resultValue+word.lower()
                        listOfResultType.append(UnitTools.SupportUnitType.Float)
                    else:
                        [resultValue,listOfResultType]=self.handleLastWord(paramName,resultValue,listOfResultType,word)
                    word=""
                resultValue=resultValue+paramValue[i]
                listOfResultType.append(UnitTools.SupportUnitType.Float)
            else:
                word = word + paramValue[i]

        if word!="":
            if word.lower() in mathSymbol:
                resultValue=resultValue+word.lower()
                listOfResultType.append(UnitTools.SupportUnitType.Float)
            else:
                [resultValue,listOfResultType]=self.handleLastWord(paramName,resultValue,listOfResultType,word)
            word=""

        # sayzError("list: " + str(listOfResultType))
        resultType=""
        # 获得最终的Type:
        # Length 和 Angle 不能同时出现，否则出错
        # if not [False for c in [UnitTools.SupportUnitType.Length,UnitTools.SupportUnitType.Angle] if c not in listOfResultType ]:
        #      FreeCAD.Console.PrintError(u"Length 和 Angle 不能同时出现")
        if UnitTools.SupportUnitType.STRING in listOfResultType:
            resultType=UnitTools.SupportUnitType.STRING
        elif UnitTools.SupportUnitType.Frequency in listOfResultType:
            resultType=UnitTools.SupportUnitType.Frequency
        elif UnitTools.SupportUnitType.TimeSpan in listOfResultType:
            resultType=UnitTools.SupportUnitType.TimeSpan
        elif UnitTools.SupportUnitType.ElectricCurrent in listOfResultType:
            resultType=UnitTools.SupportUnitType.ElectricCurrent
        elif UnitTools.SupportUnitType.ElectricPotential in listOfResultType:
            resultType=UnitTools.SupportUnitType.ElectricPotential
        elif UnitTools.SupportUnitType.Length in listOfResultType:
            resultType=UnitTools.SupportUnitType.Length
        elif UnitTools.SupportUnitType.Angle in listOfResultType:
            resultType=UnitTools.SupportUnitType.Angle
        elif UnitTools.SupportUnitType.Float in listOfResultType:
            resultType=UnitTools.SupportUnitType.Float
        elif UnitTools.SupportUnitType.Integert in listOfResultType:
            resultType=UnitTools.SupportUnitType.Integert

        # sayzError("resultValue:  " + str(resultValue) + "  resultType:  " + resultType + "  list: " + str(listOfResultType))
        return [resultValue,resultType]

    def addParam(self,paramName,paramValue,typeOfParam):
        '''
        将变量添加到FreeCAD中，并且记录变量是否发生变化\n
        注意此函数会抛出异常，即借用FreeCAD的setExpression的机制来检查变量表达式是否符合要求
        '''
        #在这里处理**运算符
        paramValue = self.changeToPow(paramValue)
        # sayzError("参数-处理**结束")

        if paramName in self.listOfParamDefined:
            # 变量的类型发生变化
            if  (hasattr(getattr(self.paramObj,paramName),"Unit") and str(getattr(self.paramObj,paramName).Unit.Type) != typeOfParam) \
               or (isinstance(getattr(self.paramObj,paramName),int) and typeOfParam!=UnitTools.SupportUnitType.Integert) \
               or (isinstance(getattr(self.paramObj,paramName),float) and typeOfParam!=UnitTools.SupportUnitType.Float) \
               or (isinstance(getattr(self.paramObj,paramName),basestring) and typeOfParam!=UnitTools.SupportUnitType.STRING):
                self.deleteParamFromFreeCAD(paramName)
                self.addParamToFreeCAD(paramName, paramValue, typeOfParam)
            # 变量的类型未发生变化
            else:
                self.modifyParamToFreeCAD(paramName, paramValue, typeOfParam)
        else:
            self.addParamToFreeCAD(paramName, paramValue, typeOfParam)

    def addParamToFreeCAD(self,paramName,paramValue,typeOfParam):
        if paramName not in self.listOfParamDefined \
           or paramName not in self.listOfParamNameAndValueDefined:
            # sayzError("参数-尝试添加一个变量:  " + str(paramName))
            self.paramObj.addProperty('App::Property' + typeOfParam, paramName, "Custom", "")
            # 此处的转换是因为FreeCAD表达式的参数分隔习惯，具体信息看本文件开头的连接
            paramValue = re.sub(r",", ", ", paramValue)
            if typeOfParam == UnitTools.SupportUnitType.STRING:
                setattr(self.paramObj, paramName, paramValue)
            else:
                self.paramObj.setExpression(paramName, paramValue)
            self.listOfParamNameAndValueDefined.append(paramName)
            self.paramObj.setEditorMode(paramName, 0)
            #将新增的属性加入列表
            self.listOfParamDefined.append(paramName)
            # FreeCAD.ActiveDocument.PropertiesChanged = FreeCAD.ActiveDocument.PropertiesChanged + ";" + paramName
            # sayzError("参数-变量列表： " + str(self.listOfParamDefined))
            # sayzError("参数-成功添加一个变量:  " + str(paramName))

    def modifyParamToFreeCAD(self,paramName,paramValue,typeOfParam):
        # sayzError("参数-修改变量")
        if paramName in self.listOfParamDefined \
            or paramName in self.listOfParamNameAndValueDefined:
            if typeOfParam == UnitTools.SupportUnitType.STRING:
                # 也可能是String类型的不在表达式解析器中，为什么？？？
                setattr(self.paramObj,paramName,paramValue)
            else:
                for expressionParam in self.paramObj.ExpressionEngine:
                    if paramName == expressionParam[0] and paramValue != expressionParam[1]:
                        paramValue = re.sub(r",", ", ", paramValue)
                        self.paramObj.setExpression(paramName, paramValue)
                        # FreeCAD.ActiveDocument.PropertiesChanged = FreeCAD.ActiveDocument.PropertiesChanged+";"+paramName
            self.paramObj.setEditorMode(paramName, 0)

    def deleteParamFromFreeCAD(self, paramName):
        # 注意保证DynamicData的一致性，即保证成功定义的变量都在DynamicData里面，\
        # 未成功定义的或者被删除的都不在DynamicData
        self.paramObj.removeProperty(paramName)
        if paramName in self.listOfParamDefined:
            self.listOfParamDefined.remove(paramName)

    def deleteNotDefinedParam(self):
        '''
        删除被删除的变量
        '''
        # 查找被删除的变量
        paramDeleted = self.getNamesOfAllDeletedParams()
        # 删除
        for paramName in paramDeleted:
            try:
                setattr(self.paramObj, paramName, 0)
            except:
                sayzError("setattr "+str(paramName)+" error!\n")
            self.deleteParamFromFreeCAD(paramName)
            
    def getParamName(self, paramItem):
        paramItemNameAndValue = paramItem.split("=")
        paramName = paramItemNameAndValue[0]
        return paramName

    def onHelpBtn(self):
        DocumentTools.errorMessage(u"支持类型：Angle、Length、Float、Int、String!\n \
                                    Angle类型值后面加上deg标识,例如：angle1=30deg；\n \
                                    Length类型值后面加上mm、cm、m(不区分大小写),例如：length1=11mm；\n \
                                    Float类型值一定带上小数点,例如 f1=1.0；\n \
                                    Int类型值是个具体的数值，例如 i1=1；\n \
                                    其他剩下的则为string类型,例如 str1=\"My string\"。\n \
                                    每一项以英文分号结束！")
        
    def removeErrorParam(self):
        '''
        去除错误的变量定义字符串
        '''
        resultParams=self.ui.textEdit_defintParam.toPlainText()
        for paramItem in self.errorParams:
            while(len([i.start() for i in re.finditer("\\b"+str(paramItem)+"\\b", resultParams)])!=0):
                indexList=[i.start() for i in re.finditer("\\b"+str(paramItem)+"\\b", resultParams)]
                # for idx in indexList:
                idx=indexList[0]
                curI=idx-1
                #前面有多余等号
                preFlag=False
                #前面开始截取的位置索引
                preIdx=0
                #后面有多余等号
                behFlag=False
                #后面终止截取的位置,预选时有两个可能的位置等号那里或;那里
                behIdx1=len(resultParams)
                behIdx2=len(resultParams)
                #判断前面有没有等号
                while curI>=0:
                    if resultParams[curI]==";":
                        preFlag=False
                        preIdx=curI+1
                        break
                    elif resultParams[curI]=="=":
                        preFlag=True
                        preIdx=curI+1
                        break
                    preIdx=curI
                    curI=curI-1
                sayz("preIdx: "+str(preIdx))
                curI=idx+1
                #计数为2的时候，才算多余的等号
                countEqual=0
                while curI<len(resultParams):
                    if resultParams[curI]=="=":
                        countEqual=countEqual+1
                        if countEqual==2:
                            behFlag=True
                            break
                        elif countEqual==1:
                            behIdx1=curI+1
                    elif resultParams[curI]==";":
                        behFlag=False
                        behIdx2=curI+1
                        break
                    curI=curI+1
                    behIdx2=curI
                sayz("behIdx: "+str(behIdx1)+" "+str(behIdx2))
                sayz("flag: "+str(preFlag)+" "+str(behFlag))
                #只有当preFlag和behFlag都是False的时候，截取preIdx和behIdx2之间的，其它时候，就截取preIdx和behIdx1之间的
                if not preFlag and not behFlag:
                    resultParams=resultParams[:preIdx]+resultParams[behIdx2:]
                else:
                    resultParams=resultParams[:preIdx]+resultParams[behIdx1:]
        return resultParams

    def deleteRepeat(self):
        '''
        去除重复定义的变量
        '''
        resultParamStr=FreeCAD.ActiveDocument.Company
        paramsStr=FreeCAD.ActiveDocument.Company

        # 1.先去掉注释
        params=re.sub(r"[!|！][^\n]*","",paramsStr)
        # 2.掉空格与换行符
        params=params.replace(" ","").replace("\n","").replace("\r","").replace("\t","")

        # 按照分号拆分
        listOfAllParams=re.split(r";|；",params)
        # 用字典来存放值
        dParamNameAndValue={}

        for paramItem in listOfAllParams:
            paramNameAndValue=paramItem.split("=")
            if len(paramNameAndValue)==2:
                paramName=paramNameAndValue[0]
                paramValue=paramNameAndValue[1]
                # 查看这个paramName是否已经定义过
                if dParamNameAndValue.has_key(paramName):
                    resultParamStr=re.sub("\\b"+paramName+"[^;]*"+dParamNameAndValue[paramName]+"[^;]*","",resultParamStr)
                    dParamNameAndValue[paramName]=paramValue
                else:
                    dParamNameAndValue[paramName]=paramValue
        
        return resultParamStr
    
    def __slotOfUndo(self):
        self.ui.textEdit_defintParam.undo()

    def __slotOfRedo(self):
        self.ui.textEdit_defintParam.redo()

    def __find(self):
        sayzError("开始查找功能\n")
        dialogOfFind = SearchTool(self.ui, self)
        dialogOfFind.show()
        dialogOfFind.exec_()
        sayzError("查找功能结束\n")

    def errorHandle(self,index,paramName):
        '''
        定义失败的处理
        '''
        tip=u"第"+str(index)+u"个，变量"+str(paramName)+u"定义出错！\n"
        self.errorParams.append(paramName)
        self.errorText=self.errorText+tip
        self.ui.textEdit_ValidInfo.setPlainText(self.errorText)
        sayzError(u"第"+str(index)+u"个定义有误!\n")

    def getValueOfQuantity(self,obj,param):
        '''
        @ brief 获得对象的属性值对应的值 String
        '''
        value=getattr(obj,param)
        if hasattr(value,"Value"):
            return str(getattr(value,"Value"))
        else:
            return str(value)

    def handleLastWord(self,paramName,paramValue,listOfResultType,word):
        # sayzError("name:  " + paramName + "  value:  " + paramValue + "  type:  " + str(listOfResultType) +\
        #      "  word:  " + word)
        # 此处的word可能是数字、字母或字母加数字
        resultValue = paramValue
        resultType = listOfResultType
        # 先处理一下小数点
        indexOfPoint = word.find(".")
        if indexOfPoint !=-1:
            if word.find(".")==0:
                word=word.replace(".","0.")
            if word.find(".")==len(word)-1:
                word=word.replace(".",".0")
            if not word.find(".")==0 and not  word.find(".")==len(word)-1:
                if not word[indexOfPoint-1].isdigit():
                    word=word.replace(".","0.")
                if not word[indexOfPoint+1].isdigit():
                    word=word.replace(".",".0")

        # 纯数字
        if ObjectsTools.isNumber(word):
            if "." in word:
                resultType.append(UnitTools.SupportUnitType.Float)
            else:
                resultType.append(UnitTools.SupportUnitType.Integert) 
            resultValue=resultValue+word
        # 数值带单位、可能是变量名、String字符串
        else:
            # 已经定义的变量
            # 这个用于判断是否找到了类型
            wordLower=word.lower()
            flagFindType=False
            for alreadDefineParamItem in self.listOfParamObj:
                alreadDefineParamItemLower=alreadDefineParamItem.getName().lower()
                # 确实是以前定义过的变量
                if wordLower == alreadDefineParamItemLower:
                    resultType.append(alreadDefineParamItem.getType())

                    if paramName.lower()==alreadDefineParamItemLower:
                        resultValue=resultValue+alreadDefineParamItem.getValue()
                    else:
                        resultValue=resultValue+alreadDefineParamItem.getName()
                    flagFindType=True
                    break
            # 没有找到Type, 非定义变量名，数值带单位或者String字符串
            if not flagFindType:

                valueAndUnit=UnitTools.getValueAndUnitOfData(word)
                num=valueAndUnit[0]
                unitStr=valueAndUnit[1]
                resultValue=resultValue+num+UnitTools.turnLowerUnitToNormalTunit(unitStr)

                resultType.append(UnitTools.getTypeOfData(word))
        result=[resultValue,resultType]
        return result

    def getParamAndValues(self,paramStr):
        '''
        通过对输入的字符串进行处理，得到的param=value类型的list并返回
        '''
        paramsAndVaules=re.split(r";|；",paramStr)
        resultList=[]

        for item in paramsAndVaules:
            paramsAndVaule=item.split("=")
            # FreeCAD.Console.PrintError(str(paramsAndVaule))
            if len(paramsAndVaule)<=2:
                resultList.append(item)
            # else:
            #     # 有连等于号
            #     for index in range(len(paramsAndVaule)-1):
            #         tempStr=paramsAndVaule[index]+"="+paramsAndVaule[len(paramsAndVaule)-1]
            #         resultList.append(tempStr)
        return resultList

    def changeToPow(self,s):
        '''
        将s,如s=(a+b)**5 转换为pow((a+b);5)
        '''
        operators=["+","-","*","/","^","(",")",":"]

        resultS=s
        # **的索引
        doubleStarsIndex=resultS.find("**")
        while doubleStarsIndex!=-1:
            #先找到**前面的表达式
            previousEps=""
            if resultS[doubleStarsIndex-1]!=")":
                i=doubleStarsIndex-1
                while i>=0 and (resultS[i] not in operators) :
                    previousEps=resultS[i]+previousEps
                    i=i-1
                    if i<0:
                        break
                pass
            #有括号
            else:
                previousEps=")"
                i=doubleStarsIndex-2
                # 用于括号配对
                bracket=1
                while (resultS[i] not in operators) or bracket!=0:
                    if resultS[i]==")":
                        bracket=bracket+1
                    if resultS[i]=="(":
                        bracket=bracket-1
                    previousEps=resultS[i]+previousEps
                    i=i-1
                    if i<0:
                        break
                pass
            behindEps=""
            if resultS[doubleStarsIndex+1]!="(":
                #"**"所以+2
                i=doubleStarsIndex+2
                while (resultS[i] not in operators) and i<len(resultS):
                    behindEps =behindEps+resultS[i]
                    i=i+1
                    if i>=len(resultS):
                        break
            else:
                behindEps="("
                i=doubleStarsIndex+3
                bracket=1
                while(resultS[i] not in operators) or bracket!=0:
                    if resultS[i]=="(":
                        bracket=bracket+1
                    if resultS[i]==")":
                        bracket=bracket-1
                    behindEps=behindEps+resultS[i]
                    i=i+1
                    if i>=len(resultS):
                        break
                pass
            resultS=resultS[0:doubleStarsIndex-len(previousEps)]+"pow("+previousEps+";"+behindEps+")"+resultS[doubleStarsIndex+len(behindEps)+2:len(resultS)]
            doubleStarsIndex=resultS.find("**")
        return resultS

    def removeAllUnits(self,paramValue):
        '''
        去掉参数值中所有的单位符号
        '''
        resultValue=paramValue.replace(" ","")
        #所有的单位
        listOfAllUnit=["mils","mil","inches","feet","foot","km","m","meter","sec","second","hz","a","amp","volt","tesla",\
                        "joule","watt","rad","radian","cm","mm","deg","degree","atto","pico","nano","micro","gauss","milli",\
                            "gauss","milli","kilo","kv","khz","mega","mhz","giga","tera","thz","eta","exa","c","ev","kev",\
                                "mev","gev","kilometer","kilometers","kilovolt","kilovolts","kilohertz","s","v","t","j","w"]
        # 去掉所有的单位
        for unitStr in listOfAllUnit:
            resultValue=re.sub("(?<=[\\d])"+unitStr+"\\b","",resultValue,flags=re.IGNORECASE)
        return resultValue

    def getParametersFromParamObj(self):
        text=""

        objsInDoc=FreeCAD.ActiveDocument.Objects
        # 获得参数对象
        self.paramObj=None
        for objItem in objsInDoc:
            if hasattr(objItem,"DynamicData"):
                self.paramObj=objItem
                break
        if self.paramObj==None:
            return text
        else:
            # 属性列表
            paramObjPropertiesList=self.paramObj.PropertiesList
            # 固有属性
            propertiesUnuselessList=['DynamicData', 'ExpressionEngine', 'Label', 'Proxy', 'Type',"DX1","DX2","DX3"]
            # 表达式器里的属性[("propertyName","Value"),(...,...),]
            expressionEngineers=self.paramObj.ExpressionEngine
            # 两个list的差集
            propertiesWithoutUnuselessList = [item for item in paramObjPropertiesList if item not in propertiesUnuselessList]
            # 表达式器重也要去掉没用的属性
            expressionEngineers=[val for val in expressionEngineers if val in propertiesWithoutUnuselessList]
            # 找到在表达式器里的属性列表
            propertiesInExpressionEngineer=[]
            for i in range(len(expressionEngineers)):
                propertiesInExpressionEngineer.append(expressionEngineers[i][0])

            # 找到一般属性，即没有在表达式器里的属性
            properties=[item for item in propertiesWithoutUnuselessList if item not in propertiesInExpressionEngineer]

            # 已写入属性名
            propertyAlreadyWritedList=[]
            # 先得到一般属性的键值对
            for propertyItem in properties:
                text= text+propertyItem + "="+str(getattr(self.paramObj,propertyItem))+";\n"
                propertyAlreadyWritedList.append(propertyItem)
            
            counts=len(expressionEngineers)
            tempCounts=0
            while counts>0 and tempCounts!=counts:
                # 这里为了防止无休止的循环
                tempCounts=counts
                # 在处理在表达式器里的属性
                for expressionEngineerItem in expressionEngineers:
                    value=expressionEngineerItem[1].replace(" ","")
                    # if value=="pi" or value=="e" or ObjectsTools.isNumber(value) or self.isValueWithUnit(value):
                    if value=="pi" or value=="e" or ObjectsTools.isNumber(value) or UnitTools.isValueWithUnit(value):
                        text= text+expressionEngineerItem[0] + "="+expressionEngineerItem[1]+";\n"
                        propertyAlreadyWritedList.append(expressionEngineerItem[0])
                        expressionEngineers.remove(expressionEngineerItem)
                        tempCounts=tempCounts-1
                    #前面已经定义过的
                    elif value in propertyAlreadyWritedList:
                        text=text+expressionEngineerItem[0] + "="+expressionEngineerItem[1]+";\n"
                        propertyAlreadyWritedList.append(expressionEngineerItem[0])
                        expressionEngineers.remove(expressionEngineerItem)
                        tempCounts=tempCounts-1
                    # 多项式或者单项式
                    else:
                        # m每一项
                        # propertyItemsList=value.split("+").split("-").split("*").split("/")
                        propertyItemsList=re.split(r"\+|\-|\*|/",value)
                        flagIsCanDefine=True
                        for propertyItem in propertyItemsList:
                            # if propertyItem=="pi" or propertyItem=="e" or ObjectsTools.isNumber(propertyItem) or (propertyItem in propertyAlreadyWritedList) or self.isValueWithUnit(propertyItem):
                            if propertyItem=="pi" or propertyItem=="e" or ObjectsTools.isNumber(propertyItem) or (propertyItem in propertyAlreadyWritedList) or UnitTools.isValueWithUnit(propertyItem):
                                flagIsCanDefine=True
                                continue
                            else:
                                flagIsCanDefine=False
                                break
                        if flagIsCanDefine:
                            text=text+expressionEngineerItem[0] + "="+expressionEngineerItem[1]+";\n"
                            propertyAlreadyWritedList.append(expressionEngineerItem[0])
                            expressionEngineers.remove(expressionEngineerItem)
                            tempCounts=tempCounts-1
        FreeCAD.Console.PrintMessage("text: "+str(text)+"\n")
        return text

    def removeAllParamsList(self,paramValue):
        '''
        去掉已定义的参数名
        '''
        resultValue = paramValue.replace(" ","")
        for paramName in self.listOfParamNameAndValueDefined:
            resultValue=re.sub("\\b"+paramName+"\\b","",resultValue,flags=re.IGNORECASE)
        return resultValue

    def getNamesOfAllDeletedParams(self):
        '''
        获取被删除的变量名，返回被删除的变量名的list\n
        这里仅做简单化处理，并不考虑效率问题\n
        '''
        temp_curList = []
        temp_lastList = []
        deleted_list = []
        # 获取变量名
        for i in self.curListParams:
            temp_str = re.sub(r"=.*", "", i)
            if len(temp_str) != 0:
                temp_curList.append(temp_str)
        for i in self.lastListParams:
            temp_str = re.sub(r"=.*", "", i)
            if len(temp_str) != 0:
                temp_lastList.append(temp_str)
        # 获取被删除的变量名
        for i in temp_lastList:
            if i not in temp_curList:
                deleted_list.append(i)
        sayzError("参数-被删除的变量： " + str(deleted_list))
        return deleted_list
    
    def getNamesOfAllChangedParams(self):
        '''
        获取值改变的变量列表
        '''
        changed_list = []
        self.dict_cur = {}
        for i in self.listOfParamDefined:
            self.dict_cur[i] = getattr(self.paramObj, i)

        for i in self.dict_cur:
            if i in self.dict_last:
                if self.dict_cur[i] != self.dict_last[i]:
                    changed_list.append(i)
            else:
                changed_list.append(i)
        # 将改变的变量名存放到C++对象中，这个对象会在布尔运算的时候被使用
        for i in changed_list:
            FreeCAD.ActiveDocument.PropertiesChanged = FreeCAD.ActiveDocument.PropertiesChanged+";"+i
        sayzError("参数-改变的变量名： " + str(changed_list))

    def recordLastParams(self):
        '''
        获取当前所有变量以及对应的值，用于后面对比哪些变量发生变化
        '''
        self.dict_last = {}
        for i in self.lastListParamDefined:
            if hasattr(self.paramObj, i):
                self.dict_last[i] = getattr(self.paramObj, i)
            else:
                # 这里强行占用一个字符串
                self.dict_last[i] = "__deleted!@#"

    def checkForSyntaxErrors(self, param_list):
        """
        检查语法错误，过滤处符合语法条件的变量定义
        比如表达式'xx==yy'   1.xx不能重复   2.xx和yy不可为空 3.‘=’ 在一个表达式只能出现一次
        :param param_list:变量列表
        :return: 出现错误的变量
        """
        sayzError("检查语法错误")
        errors = []
        param_existed = []      # 已经存在的变量，用于检测变量是否重复定义
        for i in range(len(param_list)):
            if len(param_list[i]) == 0:
                continue

            # ‘=’的数量必须为一
            if param_list[i].count('=') != 1:
                errors.append(self.generateErrorMessage(i, param_list[i], "表达式有且仅能有一个‘=’"))
                continue
            [pName, pValue] = param_list[i].split('=')      # pName:变量名  pValue: 变量值

            # 变量名和变量值都不允许为空
            if len(pName) == 0 or len(pValue) == 0:
                errors.append(self.generateErrorMessage(i, param_list[i], "变量名或变量值为空"))
                continue

            # 检查变量是否重复定义
            if pName in param_existed:
                errors.append(self.generateErrorMessage(i, param_list[i], "变量重复定义"))
                continue
            param_existed.append(pName)

        res = ""
        for i in errors:
            res += i + '\n'
        sayzError(str(param_existed))
        return res

    @staticmethod
    def generateErrorMessage(num, message, reason):
        """
        根据参数生成错误信息
        :param reason: 错误原因
        :param num: 参数的序号（第几个）
        :param message: 参数的定义
        :return: str
        """
        res = "第" + str(num) + "个参数定义出错：'" + str(message) + "'  错误原因： " + str(reason)
        return res


class CustomeParameterMainCommand:
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        dlg = CustomeParameterMain()
        # ? 是否重复设置了变量数组到控件
        dlg.ui.textEdit_defintParam.setPlainText(FreeCAD.ActiveDocument.Company)
        dlg.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling2D/modeling2DResources/参数设置.svg"
        MenuText = "自定义参数"
        ToolTip = "CustomParameters"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CustomeParameterMainCommand', CustomeParameterMainCommand())


def sayzError(msg):
    FreeCAD.Console.PrintError(msg)
    FreeCAD.Console.PrintError("\n")


def sayz(msg):
    FreeCAD.Console.PrintMessage(str(msg)+"\n")
