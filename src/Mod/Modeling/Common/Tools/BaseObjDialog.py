#-*- coding: utf-8 -*-

###############################  工具类函数相关的函数 ##########################################           
#重新获取obj时做单位的转换
def ValueUnitslength(num1,units):
    if units == 'mm':
        num1=num1*1000
    elif units == 'cm':
        num1=num1*100
    elif units == 'm':
        num1=num1
    # FreeCAD.Console.PrintMessage(str(num1)+'\n')
    return num1
def ValueUnitsangle(num1,units):
    if units == 'deg':
        num1=num1
    elif units == 'rad':
        num1=num1*180/pi
    return num1 
# 单独为环形体设计的函数
def ValueUnitsangleForTS(num1,units):
    if num1 == 359.9:
        num1 = 360.0
    if units == 'deg':
        num1=num1
    elif units == 'rad':
        num1=num1*180/pi
    return num1 

def getNumberfromUnicode(string):
    # string="A1.45，b5，6.45，8.82"
    result=re.findall(r"\d+\.?\d*",string)
    return result
def isNumber(n):
    result=True
    try:
        num=float(n)
        result = num == num
    except :
        result=False
    return result
def getGlobalVar():
    import Modeling
    GlobalVariablelist=Modeling.Common.Tools.ModelingCommandForM3dFile.getGlobalVariable()
    list1=[]
    for x in GlobalVariablelist:
        list1.append(x[0])
    list1.append('DX1')
    list1.append('DX2')
    list1.append('DX3')
    return list1