#-*- coding: utf-8 -*-
import CustomParameterGui.DlgCustomeParameter
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

# 参数类
class ParamItem:
    def __init__(self,n,t,v):
        self._name=n
        self._type=t
        self._value=v
    def getType(self):
        return self._type
    def getName(self):
        return self._name
    def getValue(self):
        return self._value

class CustomeParameterMain(QtGui.QDialog):
    def __init__(self,flagIsFromM3d=False,parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = CustomParameterGui.DlgCustomeParameter.Ui_Dialog_CustomParameterDlg()
        self.ui.setupUi(self)

        self.paramObj=ObjectsTools.getParamObj()
        self.flagColorChange=True
        self.curColor=QtGui.QColor(0,0,0)
        #先记录一下初始参数值
        self.lastInfo=FreeCAD.ActiveDocument.Company

        self.ui.textEdit_defintParam.setText(FreeCAD.ActiveDocument.Company)
        # FreeCAD.Console.PrintMessage(str(self.ui.textEdit_defintParam.toPlainText()))
        if self.ui.textEdit_defintParam.toPlainText()=="":
            self.ui.textEdit_defintParam.setText(self.getParametersFromParamObj())
        
        # self.ui.textEdit_ValidInfo.setPlainText(self.getParametersFromParamObj())
        self.ui.pushButton_ok.clicked.connect(self.onOkBtn)
        # self.ui.pushButton_valid.clicked.connect(self.onValidBtn)
        self.ui.pushButton_cancel.clicked.connect(self.onCancelBtn)
        self.ui.pushButton_help.clicked.connect(self.onHelpBtn)


        self.listOfParamNameAndValueDefined=['DynamicData', 'ExpressionEngine', 'Label', 'Proxy', 'Type',"DX1","DX2","DX3"]
        
        
        if flagIsFromM3d:
            self.lastInfo=""
        # 给textEdit设置Highlighter
        highlighter = INHighLighter.Highlighter(self.ui.textEdit_defintParam.document())

        #记录一次验证时，错误的变量列表
        self.errorParams=[]

    def onCancelBtn(self):
        self.close()

    def onOkBtn(self):
        # 判断变量输入是否有更新？
        Paraminfo=self.ui.textEdit_defintParam.toPlainText()
        # infoLast=FreeCAD.ActiveDocument.Company
        # 如果变量没有变化
        if Paraminfo==self.lastInfo:
            self.close()
            return
        else:
            # doInit一些初始化动作
            self.doInit()
            #预处理
            paramsStr=self.PreDoParam(Paraminfo)
            #按照“；”拆分变量
            # self.listParams=re.split(r";|；",paramsStr)
            self.listParams=self.getParamAndValues(paramsStr)
            FreeCAD.Console.PrintMessage("self.listParams: "+str(self.listParams)+"\n")
            #获得最近一次的变量str
            lastParamStr=self.PreDoParam(self.lastInfo)
            #最近一次变量列表
            # listLastParams=re.split(r";|；",lastParamStr)
            listLastParams=self.getParamAndValues(lastParamStr)
            FreeCAD.Console.PrintMessage("listLastParams: "+str(listLastParams)+"\n")

            # 得到未曾变化的值
            self.listParamsSame=[x for x in self.listParams if x in listLastParams]

            sayz("self.listParamsSame: "+str(self.listParamsSame)+"\n")

            # 两个list不同元素的集合
            self.listParamsDiff=[y for y in (self.listParams+listLastParams) if y not in self.listParamsSame]

            sayz("self.listParamsDiff: "+str(self.listParamsDiff)+"\n")

            # 新增加的元素集合
            self.listParamAdd=[z for z in self.listParamsDiff if z in self.listParams]

            sayz("self.listParamAdd: "+str(self.listParamAdd)+"\n")

            FreeCAD.Console.PrintMessage("add params: "+str(self.listParamAdd)+"\n")

            # #这里处理一下两个list不同的元素，如果有变量名相同，需要去掉上一个，例如之前已有x1=5,现有定义了x1=6,需要去掉前面的x1=5;
            # self.doHandleListDiff()
            # #这里处理一下新加的元素集合，如新加的变量名相同，只取最后一个，
            # self.doHandleListAdd()
            #处理所有的listParams
            self.doHandleListParams()

            # 删除未定义，但是已存在于obj的属性
            self.deleteNotDefinedParam(self.paramObj)

            FreeCAD.Console.PrintError("FreeCAD.ActiveDocument.PropertiesChanged: "+str(FreeCAD.ActiveDocument.PropertiesChanged)+"\n")

            FreeCAD.ActiveDocument.recompute()
            
            # #刷新布尔
            DocumentTools.updateBoolean()
            FreeCAD.Console.PrintMessage(str(self.ui.textEdit_ValidInfo.toPlainText()))

            if self.ui.textEdit_ValidInfo.toPlainText()=="":
                # 设置属性名列表
                self.paramObj.DynamicData=[ i for i in self.listOfParamNameAndValueDefined if i not in  ['DynamicData', 'ExpressionEngine', 'Label', 'Proxy', 'Type',"DX1","DX2","DX3"]]
                FreeCAD.ActiveDocument.Company=self.ui.textEdit_defintParam.toPlainText()
                self.close()
            # 定义出错
            else:
                # FreeCAD.Console.PrintMessage("定义出错！\n")
                # FreeCAD.Console.PrintMessage(self.paramNamesAlreadyAdd)
                # 设置属性名列表
                self.paramObj.DynamicData=[ i for i in self.listOfParamNameAndValueDefined if i not in  ['DynamicData', 'ExpressionEngine', 'Label', 'Proxy', 'Type',"DX1","DX2","DX3"]]
                # FreeCAD.ActiveDocument.Company=FreeCAD.ActiveDocument.Company+self.paramNamesAlreadyAdd
                FreeCAD.Console.PrintMessage(" start removeErrorParam\n")
                FreeCAD.ActiveDocument.Company=self.removeErrorParam()
                FreeCAD.Console.PrintMessage(" end removeErrorParam\n")

            # 去重
            # 一个变量名重复定义时，只取最后一个
            FreeCAD.ActiveDocument.Company=self.deleteRepeat()

            FreeCAD.ActiveDocument.recompute()

    
    def doInit(self):
        #验证的错误信息
        self.errorText=""
        self.errorParams=[]
        #重置验证消息
        self.ui.textEdit_ValidInfo.setPlainText("")
        # 存放已经定义变量的名称、类型、值
        self.listOfParamObj=[]
        if hasattr(self.paramObj,"DX1"):     
            self.listOfParamObj.append(ParamItem("DX1",UnitTools.SupportUnitType.Length,str(getattr(self.paramObj,"DX1").Value)))
        if hasattr(self.paramObj,"DX2"):
            if self.paramObj.Document.CoordinateSystem==CoordinateSystemTools.CoordinateType.Rectangular or self.paramObj.Document.CoordinateSystem==CoordinateSystemTools.CoordinateType.Cylindrical:
                self.listOfParamObj.append(ParamItem("DX2",UnitTools.SupportUnitType.Length,str(getattr(self.paramObj,"DX2").Value)))
            else:
                self.listOfParamObj.append(ParamItem("DX2",UnitTools.SupportUnitType.Angle,str(getattr(self.paramObj,"DX2"))))
        if hasattr(self.paramObj,"DX3"):
            if self.paramObj.Document.CoordinateSystem==CoordinateSystemTools.CoordinateType.Rectangular or self.paramObj.Document.CoordinateSystem==CoordinateSystemTools.CoordinateType.Polar:
                self.listOfParamObj.append(ParamItem("DX3",UnitTools.SupportUnitType.Length,str(getattr(self.paramObj,"DX3").Value)))
            else:
                self.listOfParamObj.append(ParamItem("DX3",UnitTools.SupportUnitType.Angle,str(getattr(self.paramObj,"DX3"))))
    def PreDoParam(self,Paraminfo):
        # 预处理
        # 1.先去掉注释
        Paraminfo=re.sub(r"[!|！][^\n]*","",Paraminfo)
        # 2.掉空格与换行符
        infoWithOutSpaceOrEnter=Paraminfo.replace(" ","").replace("\n","").replace("\r","").replace("\t","")
        
        #处理**这样的操作符


        #处理小数点2.->2.0
        infoWithOutSpaceOrEnter=re.sub(r"(?<=\d)\.(?!\d)",".0",infoWithOutSpaceOrEnter)
        # 3.将一些单位转化为标准单位,例如：kilo volt->kv
        #   长度
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
        #处理listParams
        # 初始化变的变量Str

        FreeCAD.ActiveDocument.PropertiesChanged=""
        # 进度条
    
        progress_bar=FreeCAD.Base.ProgressIndicator()

        progress_bar.start("Start Validing Param...",len(self.listParams))
        # 本次函数已添加的Str内容
        self.thisHandleAddSuccess="\n"
        #循环每一次
        for paramItem in self.listParams:
            try:
                if paramItem=="":
                    continue
                #属于相同的内容
                elif paramItem in self.listParamsSame:
                    #定义的是函数
                    if paramItem.lower().startswith("function"):
                        [paramName,paramValue]=self.getParamNameAndValueByFunctionStr(paramItem)
                        # self.listOfParamNameAndValueDefined.append(paramName)
                    #非函数
                    else:
                        paramItemNameAndValue=paramItem.split("=")
                        paramName=paramItemNameAndValue[0]
                        paramValue=paramItemNameAndValue[1]
                        # IN 整数
                        if paramName[0].lower in ["i","j","k","l","m","n"]:
                            self.listOfParamObj.append(ParamItem(UnitTools.SupportUnitType.Integert,self.getValueOfQuantity(self.paramObj,paramName)))
                        else:
                            [normalValue,typeOfThisParam]=self.getNormalParamValueAndTypeOfIt(paramName,paramValue,self.listOfParamObj)

                            self.listOfParamObj.append(ParamItem(paramName,typeOfThisParam,self.getValueOfQuantity(self.paramObj,paramName)))
                            # 所有已经添加的变量名称
                            # self.listOfParamNameAndValueDefined.append(paramName)
                # 新增加的变量
                elif paramItem in self.listParamAdd:
                    #函数
                    if paramItem.lower().startswith("function"):
                        [paramName,paramValue]=self.getParamNameAndValueByFunctionStr(paramItem)
                        #添加这个属性
                        self.addParam(paramName,paramValue,UnitTools.SupportUnitType.STRING)
                        
                        # self.listOfParamNameAndValueDefined.append(paramName)
                    else:
                        paramItemNameAndValue=paramItem.split("=")
                        paramName=paramItemNameAndValue[0]
                        paramValue=paramItemNameAndValue[1]

                        # 整形
                        if paramItem.lower()[0] in ["i","j","k","l","m","n"]:
                            [normalValue,typeOfThisParam]=self.getNormalParamValueAndTypeOfIt(paramName,paramValue,self.listOfParamObj)
                            self.addParam(paramName,normalValue,typeOfThisParam)
                            self.listOfParamObj.append(ParamItem(paramName,typeOfThisParam,self.getValueOfQuantity(self.paramObj,paramName)))
                        #非整形
                        else:
                            [normalValue,typeOfThisParam]=self.getNormalParamValueAndTypeOfIt(paramName,paramValue,self.listOfParamObj)
                            # FreeCAD.Console.PrintError("normalValue: "+str(normalValue)+" typeOfThisParam"+str(typeOfThisParam)+"\n")
                            # 当type是string时，将所有的单位(暂不解析的)去掉，判断是否还是string
                            if typeOfThisParam==UnitTools.SupportUnitType.STRING:
                                #去掉单位
                                valueWithoutUnit=self.removeAllUnits(paramValue)
                                #去掉已定义变量名
                                valueWithoutUnit=self.removeAllParamsList(valueWithoutUnit)
                                [normalValueWithoutUnit,typeWithoutUnit]=self.getNormalParamValueAndTypeOfIt(paramName,valueWithoutUnit,self.listOfParamObj)
                                if typeWithoutUnit==UnitTools.SupportUnitType.STRING:
                                    #定义有错
                                    self.errorHandle(self.listParams.index(paramItem)+1,paramName)
                                    continue
                            #继续执行
                            self.addParam(paramName,normalValue,typeOfThisParam)

                            self.listOfParamObj.append(ParamItem(paramName,typeOfThisParam,self.getValueOfQuantity(self.paramObj,paramName)))

                    self.thisHandleAddSuccess=self.thisHandleAddSuccess+paramItem+";\n"
                
                # 添加已经定义的属性名(需要判断是否以及存在)
                if paramName not in self.listOfParamNameAndValueDefined:
                    self.listOfParamNameAndValueDefined.append(paramName)
                progress_bar.next()   
            except:
                self.errorHandle(self.listParams.index(paramItem)+1,paramName)
        progress_bar.stop()

    def errorHandle(self,index,paramName):
        '''
        定义失败的处理
        '''
        tip=u"第"+str(index)+u"个，变量"+str(paramName)+u"定义出错！\n"
        self.errorParams.append(paramName)
        self.errorText=self.errorText+tip
        self.ui.textEdit_ValidInfo.setPlainText(self.errorText)

        FreeCAD.Console.PrintError(u"第"+str(index)+u"个定义有误!\n")

    def getParamNameAndValueByFunctionStr(self,functionStr):
        functionStr=functionStr.replace(" ","")
        indexOfLeftParenthesis=paramItemLowerWithoutSpace.index("(")
        if indexOfLeftParenthesis>8:
            # 获得变量名
            paramName=paramItem[8:indexOfLeftParenthesis]
            # 为了在FUNCTION前加一个空格
            paramItemWithLeftSpace=paramItem.lstrip()
            paramValue=paramItemWithLeftSpace[:8].upper()+" "+paramItemWithLeftSpace[8:]

            return [paramName,paramValue]
        else:
            sayzError("getParamNameAndValueByFunctionStr "+str(functionStr)+"error")
            return ["",""]


    def getValueOfQuantity(self,obj,param):
        '''
        @ brief 获得对象的属性值对应的值 String
        '''
        value=getattr(obj,param)
        if hasattr(value,"Value"):
            return str(getattr(value,"Value"))
        else:
            return str(value)

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
        operators=["+","-","*","/","^","(",")",":"]
        #科学计数法的e
        otherOperators=["e"]
        resultValue=""
        listOfResultType=[]

        word=""
        for i in range(len(paramValue)):
            #运算符
            if paramValue[i] in operators:
                # 处理上一个word
                if word!="":
                    if word.lower() in mathSymbol:
                        resultValue=resultValue+word.lower()
                        listOfResultType.append(UnitTools.SupportUnitType.Float)
                    else:
                        [resultValue,listOfResultType]=self.handleLastWord(paramName,resultValue,listOfResultType,word)
                    word=""
                resultValue=resultValue+paramValue[i]
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
                word=word+paramValue[i]
        if word!="":
            if word.lower() in mathSymbol:
                resultValue=resultValue+word.lower()
                listOfResultType.append(UnitTools.SupportUnitType.Float)
            else:
                [resultValue,listOfResultType]=self.handleLastWord(paramName,resultValue,listOfResultType,word)
            word=""
    
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


        return [resultValue,resultType]

    def handleLastWord(self,paramName,paramValue,listOfResultType,word):
        # 此处的word可能是数字、字母或字母加数字
        resultValue=paramValue
        resultType=listOfResultType
        # 先处理一下小数点
        indexOfPoint=word.find(".")
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

    def addParam(self,paramName,paramValue,typeOfParam):
        # sayz("addparam name:"+str(paramName)+" value:"+str(paramValue)+" type:"+str(typeOfParam)+"\n")
        #在这里处理**运算符
        paramValue=self.changeToPow(paramValue)
        #将新增的属性加入列表
        self.paramObj.DynamicData.append(paramName)

        # 该属性已经在属性对象中呈现
        if paramName in self.listOfParamNameAndValueDefined or paramName in self.paramObj.PropertiesList:
            # 可能以后的属性类型与现在即将定义的属性类型不一致，remove后新建
            if hasattr(getattr(self.paramObj,paramName),"Unit"):
                if str(getattr(self.paramObj,paramName).Unit.Type)!=typeOfParam:
                    self.paramObj.removeProperty(paramName)
                    self.paramObj.addProperty('App::Property'+typeOfParam,paramName,"Custom","")
            else:
                if (isinstance(getattr(self.paramObj,paramName),int) and typeOfParam!=UnitTools.SupportUnitType.Integert) \
                    or (isinstance(getattr(self.paramObj,paramName),float) and typeOfParam!=UnitTools.SupportUnitType.Float) \
                        or (isinstance(getattr(self.paramObj,paramName),basestring) and typeOfParam!=UnitTools.SupportUnitType.STRING):
                    self.paramObj.removeProperty(paramName)
                    self.paramObj.addProperty('App::Property'+typeOfParam,paramName,"Custom","")  

            if typeOfParam== UnitTools.SupportUnitType.STRING:
                # 也可能是String类型的不在表达式解析器中
                setattr(self.paramObj,paramName,paramValue)
            else:
                # 可能是在表达式解析器中
                for expressionParam in self.paramObj.ExpressionEngine:
                    if paramName==expressionParam[0]:
                        #值没有发生变化
                        if paramValue==expressionParam[1]:
                            FreeCAD.Console.PrintMessage("not changed ParamName "+"paramValue: "+str(paramValue)+" "+"expressionParam[1]: "+str(expressionParam[1])+"\n")
                            #设置属性不可改
                            self.paramObj.setEditorMode(paramName,1)
                            #直接返回
                            return
                            break
                        # 值改变了
                        else:
                            FreeCAD.Console.PrintMessage("changed ParamName "+"paramValue: "+str(paramValue)+" "+"expressionParam[1]: "+str(expressionParam[1])+"\n")
                            self.paramObj.setExpression(paramName, paramValue)
                            FreeCAD.ActiveDocument.PropertiesChanged=FreeCAD.ActiveDocument.PropertiesChanged+";"+paramName
                            self.paramObj.setEditorMode(paramName,1)
                            return

        # 该属性不在属性对象中，新增属性
        # 设置属性
        self.paramObj.addProperty('App::Property'+typeOfParam,paramName,"Custom","")

        # String类型直接赋值
        if typeOfParam==UnitTools.SupportUnitType.STRING:
            setattr(self.paramObj,paramName,paramValue)
        # 其他类型，设置表达式
        # elif not isFinished:
        else:
            # 去掉“deg”
            # paramValue=paramValue.replace("deg","")
            self.paramObj.setExpression(paramName, paramValue)
        self.listOfParamNameAndValueDefined.append(paramName)
        self.paramObj.setEditorMode(paramName,1)
        #加入已更改属性列表
        FreeCAD.ActiveDocument.PropertiesChanged=FreeCAD.ActiveDocument.PropertiesChanged+";"+paramName

            # self.paramObj.setEditorMode(paramName,1)
        # except:
            # FreeCAD.Console.PrintError("Error in addParam\n")
    #通过输入的的定义字符串得到最后的param=value类型
    def getParamAndValues(self,paramStr):
        paramsAndVaules=re.split(r";|；",paramStr)
        resultList=[]
        #处理连等于号
        for item in paramsAndVaules:
            paramsAndVaule=item.split("=")
            if len(paramsAndVaule)<=2:
                resultList.append(item)
            else:
                # 有连等于号
                for index in range(len(paramsAndVaule)-1):
                    tempStr=paramsAndVaule[index]+"="+paramsAndVaule[len(paramsAndVaule)-1]
                    resultList.append(tempStr)
        # FreeCAD.Console.PrintError(paramStr+str(paramsAndVaules==resultList))
        return resultList

    def deleteNotDefinedParam(self,paramObj):
        listOfParamsInObj=paramObj.PropertiesList
        paramNotDefined=[ i for i in listOfParamsInObj if i not in self.listOfParamNameAndValueDefined ]
        for paramItem in paramNotDefined:
            try:
                setattr(paramObj,paramItem,0)
            except:
                FreeCAD.Console.PrintError("setattr "+str(paramItem)+" error!\n")
            paramObj.removeProperty(str(paramItem))
            # 去掉FreeCAD.Activatedocument.company 对应内容
            FreeCAD.ActiveDocument.Company=re.sub(r"\b"+paramItem+"[^;]*[;]","",str(FreeCAD.ActiveDocument.Company))
            sayz("remove: "+str(paramItem))

    def deleteRepeat(self):
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
    #删除company中一些验证错误的变量字符串
    def removeErrorParam(self):
        FreeCAD.Console.PrintError("START REMOVE\n")
        resultParams=self.ui.textEdit_defintParam.toPlainText()
        for paramItem in self.errorParams:
            # sayz("paramItem:"+str(paramItem))
            # sayz([i.start() for i in re.finditer('\\b'+paramItem+'\\b', resultParams)])
            #将paramItem转为转义字符
            # item=""
            # for letter in paramItem:
            #     item=item+"\\"+letter
            # s='\\b'+paramItem+'\\b'
            # sayz(s)
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
                    # FreeCAD.Console.PrintError("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT:"+str(preIdx)+" "+str(behIdx2)+"\n")
                    resultParams=resultParams[:preIdx]+resultParams[behIdx2:]
                else:
                    # FreeCAD.Console.PrintError("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF:"+str(preIdx)+" "+str(behIdx1)+"\n")
                    resultParams=resultParams[:preIdx]+resultParams[behIdx1:]
        return resultParams
    # 去掉字符串中的**运算符改为pow(a;b)
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

    def removeAllParamsList(self,paramValue):
        '''
        去掉已定义的参数名
        '''
        resultValue=paramValue.replace(" ","")
        for paramName in self.listOfParamNameAndValueDefined:
            resultValue=re.sub("\\b"+paramName+"\\b","",resultValue,flags=re.IGNORECASE)
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

    def onHelpBtn(self):
        DocumentTools.errorMessage(u"支持类型：Angle、Length、Float、Int、String!\n \
Angle类型值后面加上deg标识,例如：angle1=30deg；\n \
Length类型值后面加上mm、cm、m(不区分大小写),例如：length1=11mm；\n \
Float类型值一定带上小数点,例如 f1=1.0；\n \
Int类型值是个具体的数值，例如 i1=1；\n \
其他剩下的则为string类型,例如 str1=\"My string\"。\n \
每一项以英文分号结束！")
        pass

class CustomeParameterMainCommand:
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False
    def Activated(self):
        dlg=CustomeParameterMain()
        dlg.ui.textEdit_defintParam.setText(FreeCAD.ActiveDocument.Company)
        dlg.exec_()
        # dlg.show()
        
               
    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/CustomParameter/CustomParameterResources/Parameter.svg"
        MenuText = "CustomParameters"
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
        



