# #-*- coding: utf-8 -*-
# import CustomParameterGui.DlgCustomeParameter
# import CustomParameterGui.searchTool
# from PySide import QtGui
# import string
# import json
# import re
# import FreeCAD,FreeCADGui
# from Modeling.Common.Tools import DocumentTools,ObjectsTools,CoordinateSystemTools
# import DynamicData
# from Modeling.Common.Tools import UnitTools
# import INHighLighter
# import time
# # 请认真阅读 https://wiki.freecadweb.org/Expressions（FreeCAD的Expressions的文档）！！！
# from Modeling.Modeling2D.Tools import Tools2D
#
#
# class ParamItem:
#     """
#     参数类
#     """
#     def __init__(self, name, expression, genre, value, description):
#         self._name = name
#         self._expression = expression
#         self._type = genre      # 避免与关键字冲突
#         self._value = value
#         self._description = description
#
#     def getType(self):
#         return self._type
#
#     def getName(self):
#         return self._name
#
#     def getValue(self):
#         return self._value
#
#     def getDescription(self):
#         return self._description
#
#     def process(self):
#         mathSymbol = ["e", "pi",
#                       "acos", "asin", "atan", "atan2", "cos", "cosh", "sin", "sinh", "tan", "tanh",
#                       "exp", "log", "log10", "pow", "sqrt",
#                       "abs", "ceil", "floor", "mod", "round", "trunc",
#                       "average", "count", "max", "min", "stddev", "sum"]
#         # 在此处添加逗号，但是不确定这样的添加会不会导致其他问题
#         operators = ["+", "-", "*", "/", "^", "(", ")", ":", ","]
#         # 科学计数法的e
#         otherOperators = ["e"]
#         res_value = ""
#         res_type = ""
#         type_list = []
#
#         word = ""
#         for i in range(len(self._value)):
#             if self._value[i] in operators:
#                 if word != "":
#                     if word.lower() in mathSymbol:
#                         res_value = res_value + word.lower()
#                     else:
#                         pass
#                     word = ""
#                 res_value = res_value + self._value[i]
#             elif self._value[i].lower() in otherOperators and i != 0 and self._value[i - 1].isdigit():
#                 pass
#             else:
#                 word = word + self._value[i]
#
#         if word != "":
#             word = ""
#
#
#     def getNormalParamValueAndTypeOfIt(self, paramName, paramValue, isInt=False):
#         '''
#         @ brief 将表达式的值变为标准的值例如，s1=rrr->s1=Param.rrr
#         @ paramName:变量名
#         @ paramValue:变量的值
#         @ isint:是否类型是否为整数
#         '''
#         mathSymbol = ["e", "pi",
#                       "acos", "asin", "atan", "atan2", "cos", "cosh", "sin", "sinh", "tan", "tanh",
#                       "exp", "log", "log10", "pow", "sqrt",
#                       "abs", "ceil", "floor", "mod", "round", "trunc",
#                       "average", "count", "max", "min", "stddev", "sum"]
#         # 在此处添加逗号，但是不确定这样的添加会不会导致其他问题
#         operators = ["+", "-", "*", "/", "^", "(", ")", ":", ","]
#         # 科学计数法的e
#         otherOperators = ["e"]
#         resultValue = ""
#         listOfResultType = []
#
#         word = ""
#         for i in range(len(paramValue)):
#
#             # 运算符
#             if paramValue[i] in operators:
#                 # 处理上一个word
#                 if word != "":
#                     # sayzError("观察:  " + str(word) + "\n")
#                     if word.lower() in mathSymbol:
#                         resultValue = resultValue + word.lower()
#                         listOfResultType.append(UnitTools.SupportUnitType.Float)
#                     else:
#                         [resultValue, listOfResultType] = self.handleLastWord(paramName, resultValue, listOfResultType,
#                                                                               word)
#                     word = ""
#                 resultValue = resultValue + paramValue[i]
#             # 9E-9类似这种E前后没有运算符,且e前面是数字
#             elif paramValue[i].lower() in otherOperators and i != 0 and paramValue[i - 1].isdigit():
#                 # 处理上一个word
#                 if word != "":
#                     if word.lower() in mathSymbol:
#                         resultValue = resultValue + word.lower()
#                         listOfResultType.append(UnitTools.SupportUnitType.Float)
#                     else:
#                         [resultValue, listOfResultType] = self.handleLastWord(paramName, resultValue, listOfResultType,
#                                                                               word)
#                     word = ""
#                 resultValue = resultValue + paramValue[i]
#                 listOfResultType.append(UnitTools.SupportUnitType.Float)
#             else:
#                 word = word + paramValue[i]
#
#         if word != "":
#             if word.lower() in mathSymbol:
#                 resultValue = resultValue + word.lower()
#                 listOfResultType.append(UnitTools.SupportUnitType.Float)
#             else:
#                 [resultValue, listOfResultType] = self.handleLastWord(paramName, resultValue, listOfResultType, word)
#             word = ""
#
#         # sayzError("list: " + str(listOfResultType))
#         resultType = ""
#         # 获得最终的Type:
#         # Length 和 Angle 不能同时出现，否则出错
#         # if not [False for c in [UnitTools.SupportUnitType.Length,UnitTools.SupportUnitType.Angle] if c not in listOfResultType ]:
#         #      FreeCAD.Console.PrintError(u"Length 和 Angle 不能同时出现")
#
#         if UnitTools.SupportUnitType.STRING in listOfResultType:
#             resultType = UnitTools.SupportUnitType.STRING
#         elif UnitTools.SupportUnitType.Frequency in listOfResultType:
#             resultType = UnitTools.SupportUnitType.Frequency
#         elif UnitTools.SupportUnitType.TimeSpan in listOfResultType:
#             resultType = UnitTools.SupportUnitType.TimeSpan
#         elif UnitTools.SupportUnitType.ElectricCurrent in listOfResultType:
#             resultType = UnitTools.SupportUnitType.ElectricCurrent
#         elif UnitTools.SupportUnitType.ElectricPotential in listOfResultType:
#             resultType = UnitTools.SupportUnitType.ElectricPotential
#         elif UnitTools.SupportUnitType.Length in listOfResultType:
#             resultType = UnitTools.SupportUnitType.Length
#         elif UnitTools.SupportUnitType.Angle in listOfResultType:
#             resultType = UnitTools.SupportUnitType.Angle
#         elif UnitTools.SupportUnitType.Float in listOfResultType:
#             resultType = UnitTools.SupportUnitType.Float
#         elif UnitTools.SupportUnitType.Integert in listOfResultType:
#             resultType = UnitTools.SupportUnitType.Integert
#
#         return [resultValue, resultType]
#
#     def handleLastWord(self,paramName,paramValue,listOfResultType,word):
#         # 此处的word可能是数字、字母或字母加数字
#         resultValue = paramValue
#         resultType = listOfResultType
#         # 先处理一下小数点
#         indexOfPoint = word.find(".")
#         if indexOfPoint !=-1:
#             if word.find(".")==0:
#                 word=word.replace(".","0.")
#             if word.find(".")==len(word)-1:
#                 word=word.replace(".",".0")
#             if not word.find(".")==0 and not  word.find(".")==len(word)-1:
#                 if not word[indexOfPoint-1].isdigit():
#                     word=word.replace(".","0.")
#                 if not word[indexOfPoint+1].isdigit():
#                     word=word.replace(".",".0")
#
#         # 纯数字
#         if ObjectsTools.isNumber(word):
#             if "." in word:
#                 resultType.append(UnitTools.SupportUnitType.Float)
#             else:
#                 resultType.append(UnitTools.SupportUnitType.Integert)
#             resultValue=resultValue+word
#         # 数值带单位、可能是变量名、String字符串
#         else:
#             # 已经定义的变量
#             # 这个用于判断是否找到了类型
#             wordLower=word.lower()
#             flagFindType=False
#             for alreadDefineParamItem in self.listOfParamObj:
#                 alreadDefineParamItemLower=alreadDefineParamItem.getName().lower()
#                 # 确实是以前定义过的变量
#                 if wordLower == alreadDefineParamItemLower:
#                     resultType.append(alreadDefineParamItem.getType())
#
#                     if paramName.lower()==alreadDefineParamItemLower:
#                         resultValue=resultValue+alreadDefineParamItem.getValue()
#                     else:
#                         resultValue=resultValue+alreadDefineParamItem.getName()
#                     flagFindType=True
#                     break
#             # 没有找到Type, 非定义变量名，数值带单位或者String字符串
#             if not flagFindType:
#
#                 valueAndUnit=UnitTools.getValueAndUnitOfData(word)
#                 num=valueAndUnit[0]
#                 unitStr=valueAndUnit[1]
#                 resultValue=resultValue+num+UnitTools.turnLowerUnitToNormalTunit(unitStr)
#
#                 resultType.append(UnitTools.getTypeOfData(word))
#         result=[resultValue,resultType]
#         return result
#
#
# class SearchTool(QtGui.QDialog):
#     '''
#     查找功能
#     '''
#     def __init__(self, main_ui, parent=None):
#         QtGui.QDialog.__init__(self, parent)
#         self.ui = CustomParameterGui.searchTool.Ui_Dialog()
#         self.ui.setupUi(self)
#         self.ui.pushButton.clicked.connect(self.find)
#         self.main_ui = main_ui
#
#     def find(self):
#         findText = self.ui.lineEdit.text()
#         sayzError("进入到查找函数\n")
#         temp = self.main_ui.textEdit_defintParam.find(findText, PySide.QtGui.QTextDocument.FindBackward)
#         sayzError("测试find函数，结果： " + str(temp) + "\n")
#         if self.main_ui.textEdit_defintParam.find(findText):
#             sayzError("找到查找内容\n")
#             palette = self.main_ui.textEdit_defintParam.palette()
#             # palette.setColor(QtGui.QPalette.Highlight, palette.color(QtGui.QPalette.Active, QtGui.QPalette.Highlight))
#             self.main_ui.textEdit_defintParam.setPalette(palette)
#             sayzError("shezhi\n")
#         else:
#             pass
#
#
# class CustomParameterMain(QtGui.QDialog):
#     def __init__(self, flagIsFromM3d=False, parent=None):
#         QtGui.QDialog.__init__(self, parent)
#         self.ui = CustomParameterGui.DlgCustomeParameter.Ui_Dialog_CustomParameterDlg()
#         self.ui.setupUi(self)
#         self.setModal(False)
#
#         self.paramObj = ObjectsTools.getParamObj()
#
#         if self.ui.textEdit_defintParam.toPlainText() == "":
#             self.ui.textEdit_defintParam.setPlainText(self.getParametersFromParamObj())
#
#         self.connectSignalAndSlot()
#
#         # 已经定义的变量列表，这个是原有代码定义的，并不清楚有什么用
#         self.listOfParamNameAndValueDefined = ['DynamicData', 'ExpressionEngine', 'Label', 'Proxy', 'Type', "DX1",
#                                                "DX2", "DX3"]
#
#         # 记录之前被定义的变量，不要去修改这个list，该list仅用于记录使用
#         self.lastListParamDefined = self.paramObj.DynamicData
#         # 成功定义的变量
#         self.listOfParamDefined = self.paramObj.DynamicData
#         # 记录之前变量的名字以及对应的值，结果存放于self.dict_last
#         self.recordLastParams()
#
#         # 给textEdit设置Highlighter
#         INHighLighter.Highlighter(self.ui.textEdit_defintParam.document())
#
#         # 记录一次验证时，错误的变量列表
#         self.errorParams = []
#
#     def connectSignalAndSlot(self):
#         """
#         链接信号与槽
#         """
#         self.ui.pushButton_ok.clicked.connect(self.onOkBtn)
#         self.ui.pushButton_cancel.clicked.connect(self.onCancelBtn)
#         self.ui.pushButton_help.clicked.connect(self.onHelpBtn)
#         self.ui.pushButton_redo.clicked.connect(self.__slotOfRedo)
#         self.ui.pushButton_undo.clicked.connect(self.__slotOfUndo)
#         self.ui.pushButton_find.clicked.connect(self.__find)
#
#     def slotCancel(self):
#         self.close()
#
#     def slotOK(self):
#         pass
#
#     def __getTextFromParam(self):
#         """
#         从当前工程中获取变量信息，并且设置到Dialog中
#         :return: 初始的变量文本
#         """
#         info = FreeCAD.ActiveDocument.Company
#         # 新建的工程的info是空的，需要进行初始化操作
#         if len(info) == 0:
#             pass
#         else:
#             self.ui.textEdit_defintParam.setPlainText(info)
#         return info
#
#     def __processingTextToStandardFormat(self, text):
#         """
#         将text处理为标准格式的字符串
#         :param text: 原始字符串
#         :return: 标准格式的字符串
#         """
#         pass
#
#     @staticmethod
#     def __processingStepOne(text):
#         """
#         处理步骤一：去掉注释、空格、换行符，对小数点做处理，将一些单位转换为标准单位
#         :param text:原始文本
#         :return: 第一次处理后的文本
#         """
#         # 1.去掉注释
#         text = re.sub(r"[!|！][^\n]*", "", text)
#         # 2.去掉换行符以及多余空格
#         text = text.replace(" ", "").replace("\n", "").replace("\r", "").replace("\t", "")
#         # 3.处理小数点2.->2.0
#         text = re.sub(r"(?<=\d)\.(?!\d)", ".0", text)
#         # 4.将一些单位转化为标准单位,例如：kilo volt->kv
#         # 长度
#         text = re.sub(r"(?<=[\d])pico\b", "*1.0e-12m", text, flags=re.IGNORECASE)
#         text = re.sub(r"(?<=[\d])nano\b", "*1.0e-9m", text, flags=re.IGNORECASE)
#         text = re.sub(r"(?<=[\d])micro\b", "*1.0e-6m", text, flags=re.IGNORECASE)
#         text = re.sub(r"(?<=[\d])mils\b", "*2.54e-5m", text, flags=re.IGNORECASE)
#         text = re.sub(r"(?<=[\d])mil\b", "*2.54e-5m", text, flags=re.IGNORECASE)
#         text = re.sub(r"(?<=[\d])inches\b", "*2.54e-2m", text, flags=re.IGNORECASE)
#         text = re.sub(r"(?<=[\d])feet\b", "*2.54e-2m", text, flags=re.IGNORECASE)
#         text = re.sub(r"(?<=[\d])foot\b", "*2.54e-2m", text, flags=re.IGNORECASE)
#         text = re.sub(r"(?<=[\d])kilometer\b", "*1.0e+3m", text, flags=re.IGNORECASE)
#         text = re.sub(r"(?<=[\d])kilometers\b", "*1.0e+3m", text, flags=re.IGNORECASE)
#         # 时间
#         text = re.sub(r"(?<=[\d])sec\b", "s", text, flags=re.IGNORECASE)
#         text = re.sub(r"(?<=[\d])second\b", "s", text, flags=re.IGNORECASE)
#         text = re.sub(r"(?<=[\d])NANOSECONDS\b", "*10.0e-7ms", text, flags=re.IGNORECASE)
#         text = re.sub(r"(?<=[\d])NANOSECOND\b", "*10.0e-7ms", text, flags=re.IGNORECASE)
#         text = re.sub(r"(?<=[\d])ns\b", "*10.0e-7ms", text, flags=re.IGNORECASE)
#         # 电流
#         text = re.sub(r"(?<=[\d])amp\b", "a", text, flags=re.IGNORECASE)
#         # 电压
#         text = re.sub(r"(?<=[\d])volt\b", "v", text, flags=re.IGNORECASE)
#         text = re.sub(r"(?<=[\d])kilovolts\b", "*1.0e+3v", text, flags=re.IGNORECASE)
#         text = re.sub(r"(?<=[\d])kilovolt\b", "*1.0e+3v", text, flags=re.IGNORECASE)
#         # 角度
#         text = re.sub(r"(?<=[\d])radian\b", "rad", text, flags=re.IGNORECASE)
#         text = re.sub(r"(?<=[\d])degree\b", "deg", text, flags=re.IGNORECASE)
#         text = re.sub(r"(?<=[\d])degrees\b", "deg", text, flags=re.IGNORECASE)
#         # 频率
#         text = re.sub(r"(?<=[\d])kilohertz\b", "*1.0e+3hz", text, flags=re.IGNORECASE)
#
#         return text
#
#     @staticmethod
#     def __processingStepTwo(text):
#         """
#         处理步骤二：将标准化的文本分隔，并生成ParamItem对象
#         :param text: 标准化的文本
#         :return: ParamItem的List
#         """
#         param_list = re.split(r";|；", text)
#         process_list = []   # 挑选后的文本的list
#         error_list = []     # 错误的文本的list
#         result_list = []    # 返回值
#         # 挑选出只有一个"="的字符串
#         for i in param_list:
#             if 0 < i.count('=') < 2:
#                 process_list.append(i)
#             else:
#                 error_list.append(i)
#         # 处理字符串，转换为ParamItem对象
#         for i in process_list:
#             # 经过之前的处理此处可以确保temp是长度为2的list
#             temp = i.split("=")
#             if len(temp[0]) != 0 and len(temp[1]) != 0:
#                 result_list.append(ParamItem(name=temp[0], expression=temp[1]))
#             else:
#                 error_list.append(i)
#         return result_list
#
#
#
#
#
#     def doHandleListParams(self):
#         '''
#         将变量文本转化为变量，并存放在变量列表中
#         '''
#         # 初始化改变的变量，这是一个C++的对象
#         FreeCAD.ActiveDocument.PropertiesChanged = ""
#         # 进度条
#         progress_bar=FreeCAD.Base.ProgressIndicator()
#         progress_bar.start("Start Validing Param...", len(self.curListParams))
#
#         # 已添加的Str内容
#         self.thisHandleAddSuccess="\n"
#
#         for paramItem in self.curListParams:
#             # sayzError("参数-当前处理的变量：" + str(paramItem))
#             try:
#                 if paramItem=="":
#                     continue
#                 # 利用setExpression的机制来进行赋值以及报错处理
#                 paramItemNameAndValue = paramItem.split("=")
#                 paramName = paramItemNameAndValue[0]
#                 paramValue = paramItemNameAndValue[1]
#                 # 整形，以i-n开头的变量的意义为整形变量，如果时其他类型，计算程序会强转为整形
#                 if paramItem.lower()[0] in ["i","j","k","l","m","n"]:
#                     [normalValue,typeOfThisParam]=self.getNormalParamValueAndTypeOfIt(paramName,paramValue,self.listOfParamObj)
#                     self.addParam(paramName,normalValue,typeOfThisParam)
#                     # 这行代码的作用是什么？或者说这个list的作用是什么
#                     self.listOfParamObj.append(ParamItem(paramName,typeOfThisParam,self.getValueOfQuantity(self.paramObj,paramName)))
#                 else:
#                     [normalValue,typeOfThisParam]=self.getNormalParamValueAndTypeOfIt(paramName,paramValue,self.listOfParamObj)
#                     if typeOfThisParam == UnitTools.SupportUnitType.STRING:
#                         # 去掉单位和已经定义的变量，然后重新进行一次判断
#                         # 这里为什么要这样操作？？？
#                         valueWithoutUnit = self.removeAllUnits(paramValue)
#                         valueWithoutUnit = self.removeAllParamsList(valueWithoutUnit)
#                         [normalValueWithoutUnit,typeWithoutUnit] = self.getNormalParamValueAndTypeOfIt(paramName,valueWithoutUnit,self.listOfParamObj)
#                         if typeWithoutUnit == UnitTools.SupportUnitType.STRING:
#                             self.errorHandle(self.curListParams.index(paramItem)+1,paramName)
#                             continue
#                     self.addParam(paramName,normalValue,typeOfThisParam)
#                     self.listOfParamObj.append(ParamItem(paramName,typeOfThisParam,self.getValueOfQuantity(self.paramObj,paramName)))
#                 self.thisHandleAddSuccess=self.thisHandleAddSuccess+paramItem+";\n"
#                 # 添加已经定义的属性名(需要判断是否以及存在)
#                 if paramName not in self.listOfParamNameAndValueDefined:
#                     self.listOfParamNameAndValueDefined.append(paramName)
#                 progress_bar.next()
#             except:
#                 # sayzError("参数-进入到异常处理部分")
#                 self.errorHandle(self.curListParams.index(paramItem)+1,paramName)
#         progress_bar.stop()
#
#
#
#
#
# class CustomeParameterMainCommand:
#     def IsActive(self):
#         if FreeCADGui.ActiveDocument:
#             return True
#         else:
#             return False
#     def Activated(self):
#         dlg=CustomeParameterMain()
#         #? 是否重复设置了变量数组到控件
#         dlg.ui.textEdit_defintParam.setText(FreeCAD.ActiveDocument.Company)
#         dlg.exec_()
#         # dlg.show()
#
#
#     def GetResources(self):
#         IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/CustomParameter/CustomParameterResources/Parameter.svg"
#         MenuText = "CustomParameters"
#         ToolTip = "CustomParameters"
#         return {'Pixmap': IconPath,
#                 'MenuText': MenuText,
#                 'ToolTip': ToolTip}
#
# FreeCADGui.addCommand('CustomeParameterMainCommand', CustomeParameterMainCommand())
#
# def sayzError(msg):
#     FreeCAD.Console.PrintError(msg)
#     FreeCAD.Console.PrintError("\n")
# def sayz(msg):
#     FreeCAD.Console.PrintMessage(str(msg)+"\n")
