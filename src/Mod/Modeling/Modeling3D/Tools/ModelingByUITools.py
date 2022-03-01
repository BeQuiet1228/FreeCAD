# -*- coding: UTF-8 -*-
from Modeling.Common.Tools import CoordinateSystemTools,ObjectsTools,UnitTools
import FreeCAD
import re
# 根据字符串（常量或者参数）赋值
def setValue(obj,paramName,paramValue):
    '''
    @brief 根据obj的paramName和paramValue，为obj设置表达式
    @ 比如setVale(obj,"Length","rrr")->设置obj的Length属性为Param.rrr
    '''
    paramObj=ObjectsTools.getParamObj()
    result=UnitTools.getTypeOfPossiblePropertyName(paramObj,"",paramValue,isParamObjSelf=False)
    FreeCAD.Console.PrintMessage("value: "+str(result)+"\n")
    if result[0]!=""and result[1]!=UnitTools.SupportUnitType.STRING:
        obj.setExpression(paramName,result[0])

def setDX1DX2DX3Value(obj,ui):
    '''
    @ brief 为obj设置非均匀网格的值
    '''
    currentCoordinate=obj.Document.CoordinateSystem
    #设置非均匀网格属性
    if currentCoordinate==CoordinateSystemTools.CoordinateType.Rectangular:
        obj.X=ui.checkBox_UniformX.isChecked()
        obj.Y=ui.checkBox_UniformY.isChecked()
        obj.Z=ui.checkBox_UniformZ.isChecked()

        uniforX=str(ui.lineEdit_UniformX.text()).replace(" ","")
        uniforY=str(ui.lineEdit_UniformY.text()).replace(" ","")
        uniforZ=str(ui.lineEdit_UniformZ.text()).replace(" ","")

        
        setValue(obj,"X_Value",uniforX)
        setValue(obj,"Y_Value",uniforY)
        setValue(obj,"Z_Value",uniforZ)

    elif currentCoordinate==CoordinateSystemTools.CoordinateType.Polar:
        obj.R=ui.checkBox_UniformX.isChecked()
        obj.Theta=ui.checkBox_UniformY.isChecked()
        obj.Z=ui.checkBox_UniformZ.isChecked()

        uniforX=str(ui.lineEdit_UniformX.text()).replace(" ","")
        uniforY=str(ui.lineEdit_UniformY.text()).replace(" ","")
        uniforZ=str(ui.lineEdit_UniformZ.text()).replace(" ","")
        
        setValue(obj,"R_Value",uniforX)
        setValue(obj,"Theta_Value",uniforY)
        setValue(obj,"Z_Value",uniforZ)
    else:
        obj.Z=ui.checkBox_UniformX.isChecked()
        obj.R=ui.checkBox_UniformY.isChecked()
        obj.Theta=ui.checkBox_UniformZ.isChecked()

        uniforZ=str(ui.lineEdit_UniformX.text()).replace(" ","")
        uniforR=str(ui.lineEdit_UniformY.text()).replace(" ","")
        uniforTheta=str(ui.lineEdit_UniformZ.text()).replace(" ","")

        setValue(obj,"Z_Value",uniforZ)
        setValue(obj,"R_Value",uniforR)
        setValue(obj,"Theta_Value",uniforTheta)

    
def setPointValue(obj,pointName,x1Str,
                                x2Str,
                                x3Str):
    '''
    @ param obj: 模型对象
    @ param pointName:点的名称
    @ param x1Str,x2Str,x3Str:UI面板上点从左往右的顺序
    '''
    curCoordinate=obj.Document.CoordinateSystem
    if curCoordinate==CoordinateSystemTools.CoordinateType.Rectangular or curCoordinate==CoordinateSystemTools.CoordinateType.Polar:
        setValue(obj,pointName+".x",x1Str)
        setValue(obj,pointName+".y",x2Str)
        setValue(obj,pointName+".z",x3Str)
    else:
        # z R Theta
        setValue(obj,pointName+".x",x2Str)
        setValue(obj,pointName+".y",x3Str)
        setValue(obj,pointName+".z",x1Str)

def setValueNew(obj,paramName,expressStr):
    '''
    与上面setValue不同之处在于，换了种方式
    '''
    resultExp=expressStr
    objParam=ObjectsTools.getParamObj()
    propertyList=objParam.PropertiesList
    for propertyItem in propertyList:
        # resultExp=re.sub("\\b"+propertyItem+"\\b",objParam.Name+"."+propertyItem,flags=re.IGNORECASE)
        resultExp=re.sub("\\b"+propertyItem+"\\b",objParam.Name+"."+propertyItem,resultExp,flags=re.IGNORECASE)
    sayz(resultExp)
    obj.setExpression(paramName,resultExp)

def setAttributeValue(obj,curIndex):
    '''
    设置obj的属性，curIndex表示面板中表示模型属性的索引，0：NotDefine;1:Conductor;2:Costum;3:Vocau
    '''
    if curIndex==0:
        obj.Attribute=ObjectsTools.Attribute.NotDefine
    elif curIndex==1:
        obj.Attribute=ObjectsTools.Attribute.Conductor
    elif curIndex==2:
        obj.Attribute=ObjectsTools.Attribute.Custom
    elif curIndex==3:
        obj.Attribute=ObjectsTools.Attribute.Vacuo
    else:
        sayzError("setAttributeValue Error")
def sayz(msg):
    FreeCAD.Console.PrintMessage("\n")   
    FreeCAD.Console.PrintMessage(msg)
    FreeCAD.Console.PrintMessage("\n")    

def sayzError(msg):
    FreeCAD.Console.PrintMessage("\n")   
    FreeCAD.Console.PrintError(msg)
    FreeCAD.Console.PrintMessage("\n")  