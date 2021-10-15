# -*- coding: utf-8 -*-
import ObjectsTools
import FreeCAD
import math,re

global defauleUnit
defauleUnit=["m","deg","s","A","V","GHz"]
usualFloat=["e","pi"]



class SupportUnit:
    #长度
    mm="mm"
    cm="cm"
    m="m"
    #角度
    deg="deg"
    degree="degree"
    rad="rad"
    #时间
    ns="ns"
    ms="ms"
    s="s"
    min="min"
    h="h"
    # 电流
    A="a"
    kA="ka"
    MA="ma"
    #电压
    V="v"
    kV="kv"
    MV="mv"
    #频率
    Hz="hz"
    kHz="khz"
    MHz="mhz"
    GHz="ghz"
    THz="thz"

# 之前除了Length和Angle之外数值都有问题，这里的数值应该满足：
# [数值1][单位1]=[数值2][单位2]=[数值3][单位3]
# 比如 1.0mm = 0.1cm = 0.001m
class Length:
    thisList=[SupportUnit.mm,SupportUnit.cm,SupportUnit.m]
    scale=[1.0,0.1,0.001]
    mm="mm"
    cm="cm"
    m="m"
class Angle:
    thisList=[SupportUnit.deg,SupportUnit.rad,SupportUnit.degree]
    scale=[1.0,math.pi/180,1.0]
    deg="deg"
    degree="degree"
    rad="rad"
class TimeSpan:
    thisList=[SupportUnit.ns, SupportUnit.ms,SupportUnit.s,SupportUnit.min,SupportUnit.h]
    scale=[3600000000000.0,3600000.0,3600.0,60.0,1.0]
    ns="ns"
    ms="ms"
    s="s"
    min="min"
    h="h"
class ElectricCurrent:
    thisList=[SupportUnit.A,SupportUnit.kA,SupportUnit.MA]
    scale=[1000000.0,1000.0,1.0]
    A="a"
    kA="ka"
    MA="ma"   
class ElectricPotential:
    thisList=[SupportUnit.V,SupportUnit.kV,SupportUnit.MV]
    scale=[1000000.0,1000.0,1.0]
    V="v"
    kV="kv"
    MV="mv"   
class  Frequency:
    thisList=[SupportUnit.Hz,SupportUnit.kHz,SupportUnit.MHz,SupportUnit.GHz,SupportUnit.THz]
    scale=[1000000000.0,1000000.0,1000.0,1.0,0.001]
    Hz="hz"
    kHz="khz"
    MHz="mhz"
    GHz="ghz"
    THz="thz"

class SupportUnitType:
    #所有类的列表
    thisAllList=["Integer","Float","Length","Angle","String","TimeSpan","ElectricCurrent","ElectricPotential","Frequency"]
    #所有有单位的类列表
    thisWithUnitList=["Length","Angle","TimeSpan","ElectricCurrent","ElectricPotential","Frequency"]

    Integert="Integer"
    Float="Float"
    Length="Length"
    Angle="Angle"
    STRING="String"
    # 时间
    TimeSpan="TimeSpan"
    # 电流
    ElectricCurrent="ElectricCurrent"
    # 电压
    ElectricPotential="ElectricPotential"
    # 频率
    Frequency="Frequency"

#单例修饰器
def Singleton(cls):
    _instance = {}

    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]

    return _singleton

@Singleton
class DefaultUnits:
    def getDefaultLengthUnit(self):
        return defauleUnit[0]
    def getDefaultAngleUnit(self):
        return defauleUnit[1]
    def getDefaultTimeSpanUnit(self):
        return defauleUnit[2]
    def getDefaultElectricCurrentUnit(self):
        return defauleUnit[3]
    def getDefaultElectricPotentialUit(self):
        return defauleUnit[4]
    def getDefaultFrequencyUnit(self):
        return defauleUnit[5]

    def setDefaultLengthUnit(self,unit):
        if unit in Length.thisList:
            defauleUnit[0]=unit
    def setDefaultAngleUnit(self,unit):
        if unit in Angle.thisList:
            defauleUnit[1]=unit
    def setDefaultTimeSpanUnit(self,unit):   
        if unit in TimeSpan.thisList:
            defauleUnit[2]=unit
    def setDefaultElectricCurrentUnit(self):
        if unit in ElectricCurrent.thisList:
            defauleUnit[3]=unit
    def setDefaultElectricPotentialUit(self):
        if unit in ElectricPotential.thisList:
            defauleUnit[4]=unit
    def setDefaultFrequencyUnit(self):   
        if unit in Frequency.thisList:
            defauleUnit[5]=unit
# 输入单位str->标准单位大小写
def turnLowerUnitToNormalTunit(unitLower):
    if unitLower in Length.thisList:
        return unitLower
    elif unitLower in Angle.thisList:
        if unitLower==Angle.degree:
            return Angle.deg
        return unitLower
    elif unitLower in TimeSpan.thisList:
        return unitLower
    elif unitLower in ElectricCurrent.thisList:
        if unitLower==ElectricCurrent.A:
            return "A"
        elif unitLower==ElectricCurrent.kA:
            return "kA"
        elif unitLower==ElectricCurrent.MA:
            return "MA"
    elif unitLower in ElectricPotential.thisList:
        if unitLower==ElectricPotential.V:
            return "V"
        elif unitLower==ElectricPotential.kV:
            return "kV"
        elif unitLower==ElectricPotential.MV:
            return "MV"
    elif unitLower in Frequency.thisList:
        if unitLower==Frequency.Hz:
            return "Hz"
        elif unitLower==Frequency.kHz:
            return "kHz"
        elif unitLower==Frequency.MHz:
            return "MHz"
        elif unitLower==Frequency.GHz:
            return "GHz"
        elif unitLower==Frequency.THz:
            return "THz"
    else:
        return ""
# 输入带数值+单位->标准大小写的单位
def turnLowerUnitWithValueToNormalTunit(data):
    data=data.lower().replace(" ","")
    if not isValueWithUnit(data):
        return
    else:
        turnLowerUnitToNormalTunit(getValueAndUnitOfData(data)[1])
#获得数据的类型
def getTypeOfData(data):
    dataWithoutSpace=data.replace(" ","")
    #没有单位
    if ObjectsTools.isNumber(dataWithoutSpace):
        if "." in dataWithoutSpace:
            return SupportUnitType.Float
        else:
            return SupportUnitType.Integert
    else:
        dataWithoutSpaceAndLower=dataWithoutSpace.lower()
        #长度
        if isThisUnit(data,SupportUnit.mm) or isThisUnit(data,SupportUnit.cm) or isThisUnit(data,SupportUnit.m):
            return SupportUnitType.Length
        #角度
        elif  isThisUnit(data,SupportUnit.deg) or isThisUnit(data,SupportUnit.rad) or isThisUnit(data,SupportUnit.degree):
            return SupportUnitType.Angle
        #时间
        elif isThisUnit(data,SupportUnit.ms) or isThisUnit(data,SupportUnit.s) or isThisUnit(data,SupportUnit.min) or isThisUnit(data,SupportUnit.h):
            return SupportUnitType.TimeSpan
        #电流
        elif isThisUnit(data,SupportUnit.A)  or isThisUnit(data,SupportUnit.kA) or isThisUnit(data,SupportUnit.MA) :
            return SupportUnitType.ElectricCurrent
        #电压
        elif isThisUnit(data,SupportUnit.V) or isThisUnit(data,SupportUnit.kV) or isThisUnit(data,SupportUnit.MV):
            return SupportUnitType.ElectricPotential     
        #频率
        elif isThisUnit(data,SupportUnit.Hz) or isThisUnit(data,SupportUnit.kHz) or isThisUnit(data,SupportUnit.MHz) or isThisUnit(data,SupportUnit.GHz) or isThisUnit(data,SupportUnit.THz):
            return SupportUnitType.Frequency       
        else:
            # 常用的 e,pi等
            if dataWithoutSpaceAndLower in usualFloat:
                return SupportUnitType.Float
            # else:
            #     # 是参数的形式
            #     paramObj=ObjectsTools.getParamObj()
            #     propertiesList=paramObj.PropertiesList
            #     for propertyItem in propertiesList:
            #         if propertyItem.lower()==data.lower():
            #             #判断这个对象的该属性是否有unit属性，float,int,string没有unit属性
            #             if hasattr(getattr(paramObj,propertyItem),"Unit"):
            #                 return (str(getattr(paramObj,propertyItem).Unit.Type))
            #             else:
            #                 if isinstance(getattr(paramObj,propertyItem),int):
            #                     return (SupportUnitType.Integert)
            #                 elif isinstance(getattr(paramObj,propertyItem),float):
            #                     return (SupportUnitType.Float)
            #                 elif isinstance(getattr(paramObj,propertyItem),basestring):
            #                     return (SupportUnitType.STRING)
            return SupportUnitType.STRING
# 判断一个数值+单位是不是某个单位
def isThisUnit(data,unit):
    dataWithOutSpaceAndLower=data.lower().replace(" ","")
    if dataWithOutSpaceAndLower.endswith(unit) and ObjectsTools.isNumber( dataWithOutSpaceAndLower[0:-len(unit)]):
        return True
    else:
        return False
# 判断一个str是不是数值+单位的形式
def isValueWithUnit(data):
    typeOfData=getTypeOfData(data)
    FreeCAD.Console.PrintMessage("typeOfData: "+str(typeOfData)+"\n")
    if typeOfData in SupportUnitType.thisWithUnitList:
        return True
    else:
        return False
#thisUnit转换为otherUnit
def thisUnitToOtherUnit(unitType,thisUnit,otherUnit):

    # lengthScale=[1,0.1,0.001]
    # degreeScale=[1,math.pi/180]
    # timeSpanScale=[0.001,1,60,3600]
    # electricCurrentScale=[1,1000,1000000]
    # electricPotentialScale=[1,1000,1000000]
    # frequencyScale=[0.000000001,0.000001,0.001,1,1000]
    thisUnit=thisUnit.lower()
    otherUnit=otherUnit.lower()

    if unitType==SupportUnitType.Length:
        thisIndex=Length.thisList.index(thisUnit)
        otherIndex=Length.thisList.index(otherUnit)
        return Length.scale[otherIndex]/Length.scale[thisIndex]
    elif unitType==SupportUnitType.Angle:
        thisIndex=Angle.thisList.index(thisUnit)
        otherIndex=Angle.thisList.index(otherUnit)
        return Angle.scale[otherIndex]/Angle.scale[thisIndex]
    elif unitType==SupportUnitType.TimeSpan:
        thisIndex=TimeSpan.thisList.index(thisUnit)
        otherIndex=TimeSpan.thisList.index(otherUnit)
        return TimeSpan.scale[otherIndex]/TimeSpan.scale[thisIndex]

    elif unitType==SupportUnitType.ElectricCurrent:
        thisIndex=ElectricCurrent.thisList.index(thisUnit)
        otherIndex=ElectricCurrent.thisList.index(otherUnit)
        return ElectricCurrent.scale[otherIndex]/ElectricCurrent.scale[thisIndex]

    elif unitType==SupportUnitType.ElectricPotential:
        thisIndex=ElectricPotential.thisList.index(thisUnit)
        otherIndex=ElectricPotential.thisList.index(otherUnit)
        return ElectricPotential.scale[otherIndex]/ElectricPotential.scale[thisIndex]

    elif unitType==SupportUnitType.Frequency:
        thisIndex=Frequency.thisList.index(thisUnit)
        otherIndex=Frequency.thisList.index(otherUnit)
        return Frequency.scale[otherIndex]/Frequency.scale[thisIndex]
# 返回数据的数值和单位：
def getValueAndUnitOfData(data):
    dataType=getTypeOfData(data)
    if dataType==SupportUnitType.STRING:
        return [data,""]
    elif dataType==SupportUnitType.Float or dataType==SupportUnitType.Integert:
        return  [data,""]
    elif dataType==SupportUnitType.Length:
        if isThisUnit(data,Length.mm):
            return [data[0:-2], Length.mm]
        elif isThisUnit(data,Length.cm):
            return [data[0:-2], Length.cm]
        elif isThisUnit(data,Length.m):
            return [data[0:-1],Length.m]
    elif dataType==SupportUnitType.Angle:
        if isThisUnit(data,Angle.deg):
            return [data[0:-3],Angle.deg]
        elif isThisUnit(data,Angle.degree):
            return [data[0:-6],Angle.degree]
        elif isThisUnit(data,Angle.rad):
            return [data[0:-3],Angle.rad]
    elif dataType==SupportUnitType.TimeSpan:
        if isThisUnit(data,TimeSpan.ms):
            return [data[0:-2], TimeSpan.ms]
        elif isThisUnit(data,TimeSpan.s):
            return [data[0:-1], TimeSpan.s]
        elif isThisUnit(data,TimeSpan.min):
            return [data[0:-3], TimeSpan.min]
        elif isThisUnit(data,TimeSpan.h):
            return [data[0:-1],TimeSpan.h]
    elif dataType==SupportUnitType.ElectricCurrent:
        if isThisUnit(data,ElectricCurrent.A):
            return [data[0:-1],ElectricCurrent.A]
        elif isThisUnit(data,ElectricCurrent.kA):
            return [data[0:-2], ElectricCurrent.kA]
        elif isThisUnit(data,ElectricCurrent.MA):
            return [data[0:-2], ElectricCurrent.MA]
    elif dataType==SupportUnitType.ElectricPotential:
        if isThisUnit(data,ElectricPotential.V):
            return [data[0:-1],ElectricPotential.V]
        elif isThisUnit(data,ElectricPotential.kV):
            return [data[0:-2], ElectricPotential.kV]
        elif isThisUnit(data,ElectricPotential.MV):
            return [data[0:-2], ElectricPotential.MV]
    elif dataType==SupportUnitType.Frequency:
        if isThisUnit(data,Frequency.Hz):
            return [data[0:-2], Frequency.Hz]
        if isThisUnit(data,Frequency.kHz):
            return [data[0:-3], Frequency.kHz]
        if isThisUnit(data,Frequency.MHz):
            return [data[0:-3],Frequency.MHz]
        if isThisUnit(data,Frequency.GHz):
            return [data[0:-3],Frequency.GHz]
        if isThisUnit(data,Frequency.THz):
            return [data[0:-3],Frequency.THz]
# 返回参数模型中某一属性的数值和单位
def getValueAndUnitOfDataFromParamObj(data):
    '''
    @ param:data表示参数对象的属性运算
    @ return:返回这个属性的数值和单位，如果没有单位返回“”
    '''
    resultValue=""
    resultUnit=""
    paramObj=ObjectsTools.getParamObj()
    #获得值
    resultValue=getValueByStr(data)
    #获得类型
    resultType=getTypeOfPossiblePropertyName(paramObj,"",data)[1]
    if resultType==SupportUnitType.Length:
        resultUnit=defauleUnit[0]
    elif resultType==SupportUnitType.Angle:
        resultUnit=defauleUnit[1]
    elif resultType==SupportUnitType.TimeSpan:
        resultUnit=defauleUnit[2]  
    elif resultType==SupportUnitType.ElectricCurrent:
        resultUnit=defauleUnit[3]  
    elif resultType==SupportUnitType.ElectricPotential:
        resultUnit=defauleUnit[4]
    elif resultType==SupportUnitType.Frequency:
        resultUnit=defauleUnit[5]


    # FreeCAD.Console.PrintError("resultValue:"+str(resultValue)+"resultType:"+str(resultUnit)+"\n")
    return [resultValue,resultUnit]
    
# 转换迭代时间
def turnIterTime(data,paramDef=""):
    '''
    @ param : data表示迭代时间，可以是数值，也可能是参量
    @ paramDef: 主要是在m3d编辑器的工作台会用到，他表示runtime=35nanosecond;类似的
    @ return: 单位为ns的时间的数值
    '''
    resultVal=""
    val=""
    unitThisType=TimeSpan.s
    dataType=""
    if FreeCAD.ActiveDocument:
        val=re.sub(r"(?<=\d)\.(?!\d)",".0",data)
        #是数值m3d中这个数值的单位是ns，直接返回
        try:
            val=eval(val)
            return float(val)
        except:
            FreeCAD.Console.PrintError("not float\n")
        # if not val.isalpha():
        #     FreeCAD.Console.PrintError(" val.isalpha:"+str( val))
        #     return float(val)
        val=getValueByStr(data)
        paramObj=ObjectsTools.getParamObj()
        dataType=getTypeOfPossiblePropertyName(paramObj,"",data)[1]
    else:
        try:
            #没有document说明打开的是m3d编辑器
            paramDef=\
                paramDef.lower().replace(" ","").replace(";","").replace("nanosecond","ns").replace("nanoseconds","ns").replace("sec","s").replace("second","s")
            
            paramDef=paramDef.split("=")[1]
            #将5.ns变为5.0ns
            paramDef=re.sub(r"(?<=\d)\.(?!\d)",".0",paramDef)
            # 直接是数值
            try:
                num=float(eval(paramDef))
                if(isinstance(num,float)):
                    resultVal=float(num)*thisUnitToOtherUnit(SupportUnitType.TimeSpan,TimeSpan.s,TimeSpan.ns)
                    return resultVal
            except:
                FreeCAD.Console.PrintError("not a num\n")
            vals=re.findall(r"\d+[\.\d+]?",paramDef,re.I)
            if len(vals)>0:
                val=vals[0]
            
            unitThisType=paramDef.replace(str(val),"")
            FreeCAD.Console.PrintError("val:"+str(val)+" unit:"+str(unitThisType)+"\n")
            if unitThisType=="":
                dataType=SupportUnitType.Float
            else:
                dataType=SupportUnitType.TimeSpan
                pass
        except:
            FreeCAD.Console.PrintError("handle M3d Editor iter Time error\n")

        pass
    if dataType==SupportUnitType.STRING:
        FreeCAD.Console.PrintError("wrong iter data\n")
    elif dataType==SupportUnitType.Integert or dataType==SupportUnitType.Float:
        # FreeCAD.Console.PrintError("string to float 1:"+str(val)+"\n")
        #这里默认单位是s,转换为纳秒
        resultVal=float(val)*thisUnitToOtherUnit(SupportUnitType.TimeSpan,TimeSpan.s,TimeSpan.ns)
    else:
        # FreeCAD.Console.PrintError("string to float 2:"+str(val)+"\n")
        resultVal=float(val)*thisUnitToOtherUnit(SupportUnitType.TimeSpan,unitThisType,TimeSpan.ns)
    return resultVal


# 返回默认单位的数值
def getDataOfDefauleUnit(data,theDefaultUnits=[SupportUnit.m,SupportUnit.deg,SupportUnit.s,SupportUnit.A,SupportUnit.V,SupportUnit.GHz]):
    dataType=getTypeOfData(data)
    if dataType==SupportUnitType.STRING:
        return data
    elif dataType==SupportUnitType.Float or dataType==SupportUnitType.Integert:
        return data
    elif dataType==SupportUnitType.Length:
        value=getValueAndUnitOfData(data)[0]
        unit=getValueAndUnitOfData(data)[1]
        return str(float(value)*thisUnitToOtherUnit(SupportUnitType.Length,unit,theDefaultUnits[0]))
    elif dataType==SupportUnitType.Angle:
        value=getValueAndUnitOfData(data)[0]
        unit=getValueAndUnitOfData(data)[1]
        return str(float(value)*thisUnitToOtherUnit(SupportUnitType.Angle,unit,theDefaultUnits[1]))
    elif dataType==SupportUnitType.TimeSpan:
        value=getValueAndUnitOfData(data)[0]
        unit=getValueAndUnitOfData(data)[1]
        return str(float(value)*thisUnitToOtherUnit(SupportUnitType.TimeSpan,unit,theDefaultUnits[2]))
    elif dataType==SupportUnitType.ElectricCurrent:
        value=getValueAndUnitOfData(data)[0]
        unit=getValueAndUnitOfData(data)[1]
        return str(float(value)*thisUnitToOtherUnit(SupportUnitType.ElectricCurrent,unit,theDefaultUnits[3]))
    elif dataType==SupportUnitType.ElectricPotential:
        value=getValueAndUnitOfData(data)[0]
        unit=getValueAndUnitOfData(data)[1]
        return str(float(value)*thisUnitToOtherUnit(SupportUnitType.ElectricPotential,unit,theDefaultUnits[4]))
    elif dataType==SupportUnitType.Frequency:
        value=getValueAndUnitOfData(data)[0]
        unit=getValueAndUnitOfData(data)[1]
        return str(float(value)*thisUnitToOtherUnit(SupportUnitType.Frequency,unit,theDefaultUnits[5]))

def calculator(formulaStr,UnitsType):
    '''
    @ brief: 根据公式string求值：“1mm+5”
    @ param: formulaStr:表达式字符串
    @ param: UnitsType:结果

    @ return: 值+单位
    '''
    value=getValueByStr(formulaStr)
    unitStr=""
    if UnitsType==SupportUnitType.Length:
        unitStr="m"
    elif UnitsType==SupportUnitType.Angle:
        unitStr="deg"
    elif UnitsType==SupportUnitType.TimeSpan:
        unitStr="s"
    elif UnitsType==SupportUnitType.ElectricCurrent:
        unitStr="A"
    elif UnitsType==SupportUnitType.ElectricPotential:
        unitStr="V"
    elif UnitsType==SupportUnitType.Frequency:
        unitStr="Hz"
    
    resultStr=str(value)+unitStr
    return resultStr
    pass
def getResultUnitsType(formulaStr):
    '''
    @ brief :输入一个字符串的表达式，返回最终的类型
    '''
    pass
def turnNormalUnitToShowUnit(unitType,normalValue):
    '''
    将标准单位转化为显示单位
    exp: showUnitList=[0,0,1,0,0,0]: 0.001->1mm
    '''
    # FreeCAD.Console.PrintMessage("unitType: "+str(unitType)+" normalValue: "+str(normalValue)+"\n")
    #这个是默认显示单位列表：[长度，角度，时间，电流，电压，频率]
    showUnitIndexList=FreeCAD.Units.getDefaultUnits()
    # FreeCAD.Console.PrintMessage("0\n")
    showUnitList=[
        Length.thisList[showUnitIndexList[0]],
        Angle.thisList[showUnitIndexList[1]],
        TimeSpan.thisList[showUnitIndexList[2]],
        ElectricCurrent.thisList[showUnitIndexList[3]],
        ElectricPotential.thisList[showUnitIndexList[4]],
        Frequency.thisList[showUnitIndexList[5]]
        ]
    # FreeCAD.Console.PrintMessage("1\n")
    FreeCAD.Console.PrintMessage(showUnitList)
    # FreeCAD.Console.PrintMessage("2\n")

    if unitType==SupportUnitType.Length:
        return getDataOfDefauleUnit(str(normalValue)+"m",showUnitList)+str(Length.thisList[showUnitIndexList[0]])
    elif unitType==SupportUnitType.Angle:
        return getDataOfDefauleUnit(str(normalValue)+"deg",showUnitList)+str( Angle.thisList[showUnitIndexList[1]])
    elif unitType==SupportUnitType.TimeSpan:
        return getDataOfDefauleUnit(str(normalValue)+"s",showUnitList)+str(TimeSpan.thisList[showUnitIndexList[2]])
    elif unitType==SupportUnitType.ElectricCurrent:
        return getDataOfDefauleUnit(str(normalValue)+"A",showUnitList)+str(ElectricCurrent.thisList[showUnitIndexList[3]])
    elif unitType==SupportUnitType.ElectricPotential:
        return getDataOfDefauleUnit(str(normalValue)+"V",showUnitList)+str(ElectricPotential.thisList[showUnitIndexList[4]])
    elif unitType==SupportUnitType.Frequency:
        return getDataOfDefauleUnit(str(normalValue)+"GHz",showUnitList)+str(Frequency.thisList[showUnitIndexList[5]])
    else:
        return str(normalValue)
# 下方两个函数借鉴了DlgCustomParameterMain.py中的函数

def handleLastWord(paramObj,paramName,isInt,value,listOfType,word,listOfParamsOfObj,isSelf):
    # 此处的word可能是数字、字母或字母加数字
    resultValue=value
    resultType=listOfType
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
    # FreeCAD.Console.PrintError("lastWord: "+str(word.lower())+" "+str(word.lower() in usualFloat)+"\n")
    # 纯数字
    if ObjectsTools.isNumber(word):
        if "." in word:
            resultType.append(SupportUnitType.Float)
        else:
            resultType.append(SupportUnitType.Integert) 
        resultValue=resultValue+word
    # 数值带单位、可能是变量名、String字符串、还可能是数学常量pi、e
    else:
        # 已经定义的变量
        # 这个用于判断是否找到了类型
        wordLower=word.lower()
        flagFindType=False
        for alreadDefineParamItem in listOfParamsOfObj:
            alreadDefineParamItemLower=alreadDefineParamItem.lower()
            # 确实是以前定义过的变量
            if wordLower == alreadDefineParamItemLower:
                if isInt:
                    resultValue=resultValue+alreadDefineParamItem
                else:                   
                    #判断这个对象的该属性是否有unit属性，float,int,string没有unit属性
                    if hasattr(getattr(paramObj,alreadDefineParamItem),"Unit"):
                        resultType.append(str(getattr(paramObj,alreadDefineParamItem).Unit.Type))
                    else:
                        if isinstance(getattr(paramObj,alreadDefineParamItem),int):
                            resultType.append(SupportUnitType.Integert)
                        elif isinstance(getattr(paramObj,alreadDefineParamItem),float):
                            resultType.append(SupportUnitType.Float)
                        elif isinstance(getattr(paramObj,alreadDefineParamItem),basestring):
                            resultType.append(SupportUnitType.STRING)
                        else:
                            pass    
                    # 当前自身的值              
                    if paramName.lower()==wordLower:
                        resultValue=resultValue+str(getattr(paramObj,alreadDefineParamItem))
                    else:
                        if isSelf:
                            resultValue=resultValue+alreadDefineParamItem
                        else:
                            resultValue=resultValue+paramObj.Name+"."+alreadDefineParamItem                            
                    
                flagFindType=True
                break
        # 没有找到Type, 非定义变量名，数值带单位或者String字符串
        if not flagFindType:
            if isInt:
                numStr=""
                numStr=getDataOfDefauleUnit(value)
                resultValue=resultValue+numStr
            else:
                valueAndUnit=getValueAndUnitOfData(word)
                num=valueAndUnit[0]
                unitStr=valueAndUnit[1]
                resultValue=resultValue+num+turnLowerUnitToNormalTunit(unitStr)
            resultType.append(getTypeOfData(word))

            # if ObjectsTools.isNumber(wordLower.replace("e","")):
            #     resultType.append(SupportUnitType.Float)
            #     resultValue=resultValue+wordLower
            # elif ObjectsTools.isNumber(wordLower.replace("deg","")):
            #     if isInt:
            #         resultValue=resultValue+wordLower.replace("deg","")
            #     else:
            #         resultValue=resultValue+wordLower
            #     resultType.append(SupportUnitType.Angle) 
            # elif ObjectsTools.isNumber(wordLower.replace("degree","")):
            #     if isInt:
            #         resultValue=resultValue+wordLower.replace("degree","")
            #     else:
            #         resultValue=resultValue+wordLower
            #     # # 如果是度数直接去掉“deg”
            #     # resultValue=resultValue+wordLower.replace("deg","")
            #     # 添加进resultType
            #     resultType.append(SupportUnitType.Angle) 
            # # elif ObjectsTools.isNumber(wordLower.replace("cm",""))   or ObjectsTools.isNumber(wordLower.replace("mm","")) or ObjectsTools.isNumber(wordLower.replace("m","")): 
            # elif getTypeOfData(wordLower)==SupportUnitType.Length:
            #     if isInt:
            #         numStr=""
            #         if wordLower.endswith("mm"):
            #             numStr= str(float(wordLower.replace("mm",""))*0.001)
            #         elif wordLower.endswith("cm"):
            #             numStr= str(float(wordLower.replace("cm",""))*0.01)
            #         elif wordLower.endswith("dm"):
            #             numStr= str(float(wordLower.replace("dm",""))*0.1)
            #         elif wordLower.endswith("m"):
            #             numStr= str(float(wordLower.replace("m",""))*1)
            #         # 抛出异常
            #         else:
            #             1/0
            #         resultValue=resultValue+numStr
            #     else:
            #         # 这里表示单位,加上小写单位
            #         resultValue=resultValue+wordLower
            #         FreeCAD.Console.PrintMessage("resultValue222: "+str(resultValue)+"wordLower: "+str(wordLower)+"\n")
            #     resultType.append(SupportUnitType.Length)
                
            # elif wordLower=="pi":
            #     resultValue=resultValue+wordLower
            # # 电流
            # elif  getTypeOfData(wordLower)==SupportUnitType.ElectricCurrent:
            #     # 是整型
            #     if isInt:
            #         numStr=""
            #         if wordLower.endswith("a"):
            #             numStr=str(float(wordLower.replace("a",""))*1.0)
            #         elif wordLower.endswith("ka"):
            #             numStr=str(float(wordLower.replace("ka",""))*1000.0)
            #         elif wordLower.endswith("ma"):
            #             numStr=str(float(wordLower.replace("ma",""))*1000000.0)
            #         # 抛出异常
            #         else:
            #             1/0
            #         pass
            #         resultValue=resultValue+numStr
            #     # 非整型
            #     else:
            #         tempWord=""
            #         if turnLowerUnitWithValueToNormalTunit(wordLower)=="A":
            #             tempWord=wordLower[0:len(wordLower)-1]+"A"
            #         elif turnLowerUnitWithValueToNormalTunit(wordLower)=="kA":
            #             tempWord=wordLower[0:len(wordLower)-2]+"kA"
            #         elif turnLowerUnitWithValueToNormalTunit(wordLower)=="MA":
            #             tempWord=wordLower[0:len(wordLower)-2]+"MA"
            #         pass
            #         resultValue=resultValue+tempWord                        
            #     pass
            #     resultType.append(SupportUnitType.ElectricCurrent)
            # # 电压
            # elif getTypeOfData(wordLower)==SupportUnitType.ElectricPotential:
            #     # 整型
            #     if isInt:
            #         numStr=""
            #         if wordLower.endswith("v"):
            #             numStr=str(float(wordLower.replace("v",""))*1.0)
            #         elif wordLower.endswith("kv"):
            #             numStr=str(float(wordLower.replace("ka",""))*1000.0)
            #         elif wordLower.endswith("mv"):
            #             numStr=str(float(wordLower.replace("mv",""))*1000000.0)
            #         # 抛出异常
            #         else:
            #             1/0
            #         pass
            #         resultValue=resultValue+numStr 
            #     # 非整型
            #     else:
            #         tempWord=""
            #         if turnLowerUnitWithValueToNormalTunit(wordLower)=="V":
            #             tempWord=wordLower[0:len(wordLower)-1]+"V"
            #         elif turnLowerUnitWithValueToNormalTunit(wordLower)=="kV":
            #             tempWord=wordLower[0:len(wordLower)-2]+"kV"

            #         elif turnLowerUnitWithValueToNormalTunit(wordLower)=="MV":
            #             tempWord=wordLower[0:len(wordLower)-2]+"MV"

            #         pass
            #         resultValue=resultValue+tempWord 
            #         resultType.append(SupportUnitType.ElectricPotential)  
            #     pass
            # #时间
            # elif getTypeOfData(wordLower)==SupportUnitType.TimeSpan:
            #     # 整型
            #     if isInt:
            #         numStr=""
            #         if wordLower.endswith("ms"):
            #             numStr=str(float(wordLower.replace("ms",""))*1000.0)
            #         elif wordLower.endswith("s"):
            #             numStr=str(float(wordLower.replace("s",""))*1.0)
            #         elif wordLower.endswith("min"):
            #             numStr=str(float(wordLower.replace("min",""))*60.0)
            #         elif wordLower.endswith("h"):
            #             numStr=str(float(wordLower.replace("h",""))*3600.0)
            #         else:
            #             1/0
            #         resultValue=resultValue+numStr
            #     # 非整型
            #     else:
            #         resultValue=resultValue+wordLower
            #         # tempWord=""
            #         # if self.isTimeSpan(wordLower)=="ms":
            #         #     tempWord=str(float(wordLower[0:len(wordLower)-2]*0.001))+"s"
            #         #     resultValue=resultValue+tempWord
            #         # else:
            #         #     resultValue=resultValue+wordLower
            #         # pass  
            #     resultType.append(SupportUnitType.TimeSpan) 
            # elif getTypeOfData(wordLower)==SupportUnitType.Frequency:
            #     if isInt:
            #         numStr=""
            #         if wordLower.endswith("hz"):
            #             numStr=str(float(wordLower.replace("hz",""))*1.0)
            #         elif wordLower.endswith("khz"):
            #             numStr=str(float(wordLower.replace("khz",""))*1000.0)
            #         elif wordLower.endswith("mhz"):
            #             numStr=str(float(wordLower.replace("mhz",""))*1000000.0)
            #         elif wordLower.endswith("ghz"):
            #             numStr=str(float(wordLower.replace("ghz",""))*1000000000.0)
            #         elif wordLower.endswith("thz"):
            #             numStr=str(float(wordLower.replace("thz",""))*1000000000000.0)
            #         else:
            #             1/0
            #         resultValue=resultValue+numStr
            #     else:
            #         tempWord=""
            #         if turnLowerUnitWithValueToNormalTunit(wordLower)=="Hz":
            #             tempWord=wordLower[0:len(wordLower)-2]+"Hz"
            #         else:
            #             tempWord=wordLower[0:len(wordLower)-3]+turnLowerUnitWithValueToNormalTunit(wordLower)
            #         resultValue=resultValue+tempWord 
            #     resultType.append(SupportUnitType.Frequency) 
            #     pass                     
            # # string 类型
            # else:
            #     if isInt:
            #         1/0
            #     else:
            #         resultValue=resultValue+word
            #         resultType.append(SupportUnitType.STRING)
    result=[resultValue,resultType]
    return result

# 得到可能是属性名的类型
def getTypeOfPossiblePropertyName(paramObj,paramName,paramValue,isParamObjSelf=True):
    '''
    @ return list[value,type]
    @ param paramObj 属性对象
    @ param paramValue: 带有加减乘除的数据
    @ Brief 例如 paramObj对象有属性X1=5mm,X2=4deg,现在有属性DX=x1+x2,这个函数用于返回x1+x2的类型,不同类型做运算，有一个优先级

    @isParamObjSelf:是后面写参数阵列体的时候新加的，主要用作判断添加属性的模型是不是参数模型，默认是参数模型
    '''
    if not paramObj:
        paramObj=ObjectsTools.getParamObj()
    mathSymbol=["e","pi",
                "acos","asin","atan","atan2","cos","cosh","sin","sinh","tan","tanh",\
                "exp","log","log10","pow","sqrt",\
                "abs","ceil","floor","mod","round","trunc",\
                "average","count","max","min","stddev","sum"]
    operators=["+","-","*","/","^","(",")",":"]

    listOfParamsOfObj=paramObj.PropertiesList
    isInt=False
    word=""
    resultValue=""
    listOfResultType=[]
    for i in range(len(paramValue)):
        # if paramValue[i]=="+" or paramValue[i]=="-" or paramValue[i]=="*" or paramValue[i]=="/":
        if paramValue[i] in operators:
            # 处理上一个word
            if word!="":
                if word.lower() in mathSymbol:
                    resultValue=resultValue+word.lower()

                    listOfResultType.append(SupportUnitType.Float)
                else:
                    [resultValue,listOfResultType]=handleLastWord(paramObj,paramName,isInt,resultValue,listOfResultType,word,listOfParamsOfObj,isSelf=isParamObjSelf)
                word=""
            resultValue=resultValue+paramValue[i]
        else:
            word=word+paramValue[i]
    if word!="":
        # 处理上一个word
        if word!="":
            if word.lower() in mathSymbol:
                resultValue=resultValue+word.lower()
                listOfResultType.append(SupportUnitType.Float)
            else:
                [resultValue,listOfResultType]=handleLastWord(paramObj,paramName,isInt,resultValue,listOfResultType,word,listOfParamsOfObj,isSelf=isParamObjSelf)
            word=""
        # [resultValue,listOfResultType]=handleLastWord(paramObj,paramName,isInt,resultValue,listOfResultType,word,listOfParamsOfObj,isSelf=isParamObjSelf)

    resultType=""
    # 获得最终的Type:
    # Length 和 Angle 不能同时出现，否则出错

    # if not [False for c in [SupportUnitType.LENGTH,SupportUnitType.ANGLE] if c not in listOfResultType ]:
    #      FreeCAD.Console.PrintError(u"Length 和 Angle 不能同时出现")
    if SupportUnitType.STRING in listOfResultType:
        resultType=SupportUnitType.STRING
    elif SupportUnitType.Frequency in listOfResultType:
        resultType=SupportUnitType.Frequency
    elif SupportUnitType.TimeSpan in listOfResultType:
        resultType=SupportUnitType.TimeSpan
    elif SupportUnitType.ElectricCurrent in listOfResultType:
        resultType=SupportUnitType.ElectricCurrent
    elif SupportUnitType.ElectricPotential in listOfResultType:
        resultType=SupportUnitType.ElectricPotential
    elif SupportUnitType.Length in listOfResultType:
        resultType=SupportUnitType.Length
    elif SupportUnitType.Angle in listOfResultType:
        resultType=SupportUnitType.Angle
    elif SupportUnitType.Float in listOfResultType:
        resultType=SupportUnitType.Float
    elif SupportUnitType.Integert in listOfResultType:
        resultType=SupportUnitType.Integert

    return [resultValue,resultType]

import re
def getValueByStr(data):
    '''
    @brief 输入一个str的值，可能是多项式，可能 运用了变量，可能是数字等，返回数值
    '''
    data=data.replace(" ","").lower()
    resultStr=""
    datas=re.split(r'(\+|\-|\*|\/|\(|\))', data)
    lastOperator=""
    for dataItem in datas:
        # 如果是运算符
        if dataItem in ["+","-","*","/","(",")"]:
            lastOperator=dataItem
        # 非运算符
        else:
            resultStr=resultStr+lastOperator
            # 先处理一下小数点
            indexOfPoint=dataItem.find(".")
            if indexOfPoint !=-1:
                if dataItem.find(".")==0:
                    dataItem=dataItem.replace(".","0.")
                if dataItem.find(".")==len(dataItem)-1:
                    dataItem=dataItem.replace(".",".0")
                if not dataItem.find(".")==0 and not  dataItem.find(".")==len(dataItem)-1:
                    if not dataItem[indexOfPoint-1].isdigit():
                        dataItem=dataItem.replace(".","0.")
                    if not dataItem[indexOfPoint+1].isdigit():
                        dataItem=dataItem.replace(".",".0")
            # FreeCAD.Console.PrintMessage("dataItem: "+str(dataItem)+"\n")
            # 纯数字
            if ObjectsTools.isNumber(dataItem):
                resultStr=resultStr+dataItem
            elif getTypeOfData(dataItem)== SupportUnitType.Float or getTypeOfData(dataItem)== SupportUnitType.Integert:
                if dataItem=="pi":
                    resultStr=resultStr+str(math.pi)
                elif dataItem=="e":
                    resultStr=resultStr+str(math.e)
                else:
                    continue
            elif getTypeOfData(dataItem)!= SupportUnitType.STRING:
                resultStr=resultStr+str(getDataOfDefauleUnit(dataItem))
            elif getTypeOfData(dataItem)== SupportUnitType.STRING:
                paramObj=ObjectsTools.getParamObj()
                paramObjPros=paramObj.PropertiesList
                for pro in paramObjPros:
                    if pro.lower()==dataItem:
                        resultStr=resultStr+str(getDataOfDefauleUnit(str(getattr(paramObj,pro))))
                        break
    # FreeCAD.Console.PrintMessage("resultStr: "+str(resultStr)+"\n")
    try:
        return eval(resultStr)
    except:
        FreeCAD.Console.PrintError("compute value error\n")
        return 0