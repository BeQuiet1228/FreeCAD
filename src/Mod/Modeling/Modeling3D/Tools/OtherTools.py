# -*- coding: UTF-8 -*-
import FreeCAD
from Modeling.Common.Tools import ObjectsTools,UnitTools
import re
def parseExpressionStr(expressionStr):
    '''
    将表达式中带有参数的值转化为具体的值
    '''
    paramObj=ObjectsTools.getParamObj()
    propertyList=paramObj.PropertiesList

    propertyList=[i for i in propertyList if i not in ['DynamicData', 'ExpressionEngine', 'Label', 'Proxy', 'Type']]
    resultExpressionStr=expressionStr
    for propertyItem in propertyList:
        resultExpressionStr=re.sub("\\b"+propertyItem+"\\b",
                                    UnitTools.getDataOfDefauleUnit(str(getattr(paramObj,propertyItem))),
                                    resultExpressionStr,
                                    flags=re.IGNORECASE)
    sayzError(resultExpressionStr)
    return resultExpressionStr

def parseFunctionObjStr(expressionStr):
    '''
    将函数表达式中的某些运算符转换一下
    1、**->^
    2、X->x,Y->y,Z->z
    '''
    resultExpressionStr=expressionStr.replace(" ","").replace("\n","").replace("\r","")
    resultExpressionStr=resultExpressionStr.replace("**","^")
    resultExpressionStr=re.sub(r"\bX\b","x",resultExpressionStr,re.IGNORECASE)
    resultExpressionStr=re.sub(r"\bY\b","y",resultExpressionStr,re.IGNORECASE)
    resultExpressionStr=re.sub(r"\bZ\b","z",resultExpressionStr,re.IGNORECASE)

    # resultExpressionStr=re.sub(r"\b\*\*\b","^",resultExpressionStr)

    return resultExpressionStr

def sayzError(msg):
    FreeCAD.Console.PrintError(msg)
    FreeCAD.Console.PrintError("\n")
