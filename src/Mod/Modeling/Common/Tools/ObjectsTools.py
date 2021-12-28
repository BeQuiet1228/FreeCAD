# -*- coding: utf-8 -*-
import FreeCAD, math,FreeCADGui
from FreeCAD import Base
from pivy import coin
import re 
import FreeCADGui as Gui
import CoordinateSystemTools
import CoordinateSystemTools,DocumentTools
import Part
import UnitTools

import DynamicData


class ObjectType:
    # 变量类型
    Variable="Variable"
    #没有类型
    none="none"

    Point="PointObj"
    Line_Conformal="Line_Conformal"
    Line_Oblique="Line_Oblique"
    Area_Conformal="Area_Conformal"
    Area_Rectangular="Area_Rectangular"
    Area_Polygonal="Area_Polygonal"
    Area_Function="Area_Function"
    Vol_Conformal="Vol_Conformal"
    # 圆台
    Vol_SpecialCone="Vol_SpecialCone"
    Vol_Cone="Vol_Cone"
    Vol_Cylinder="Vol_Cylinder"
    Vol_Parallelepipedal="Vol_Parallelepipedal"
    # 带孔的圆柱
    Vol_Annular="Vol_Annular"
    Vol_Pyramid="Vol_Pyramid"
    Vol_Rhombus="Vol_Rhombus"
    Vol_Spherical="Vol_Spherical"
    Vol_Wedge="Vol_Wedge"
    Vol_Tetrahedron="Vol_Tetrahedron"
    Vol_Toroidal_Section="Vol_Toroidal_Section"
    Vol_Annular_Section="Vol_Annular_Section"
    Vol_Function="Vol_Function"
    Vol_Extruded="Vol_Extruded"
    Vol_Helical="Vol_Helical"
    Vol_Array = "Vol_Array"

    Vol_Draft_Revolution="Vol_Draft_Revolution"
    Vol_Revolution="Vol_Revolution"
    # 参数阵列体
    Vol_ParamArray="Vol_ParamArray"
    Vol_Test="Vol_Test"

    #草图建模的拉伸
    Vol_Draft_Extrude="Vol_Draft_Extrude"
    Vol_Draft_Revolution="Vol_Draft_Revolution"
class Custom:
    propList=["ConductivitySIGMA","RelativeDielectricConstant"]
    class ConductivitySIGMA:
        Iostropy="Iostropy"
        Anisotropy="Anisotropy"
        NotDefine="NotDefine"
    class RelativeDielectricConstant:
        Iostropy="Iostropy"
        Anisotropy="Anisotropy"
        NotDefine="NotDefine"
#定义属性
class Attribute:
    NotDefine="NotDefine"
    Conductor="Conductor"
    Custom="Custom"
    Vacuo="Vacuo"
#定义法向
class Normal:
    X="x"
    Y="y"
    Z="z"
    R="r"
    Theta="theta"
# 定义模型拥有的自身属性
class PropertiesOfObj:
    class Conformal:
        Point1="Point1"
        Point2="Point2"
        Vol_Conformal={"Point1":"App::PropertyVectorDistance",
                    "Point2":"App::PropertyVectorDistance"}
    class Annular:
        Point_1="Point_1"
        Point_2="Point_2"
        RadiusInside="RadiusInside"
        RadiusOutside="RadiusOutside"
        Vol_Annular={"Point_1":"App::PropertyVectorDistance",\
                    "Point_2":"App::PropertyVectorDistance",\
                    "RadiusInside":"App::PropertyLength",\
                    "RadiusOutside":"App::PropertyLength"}
    class Cylinder:
        Point_1="Point_1"
        Point_2="Point_2"
        Radius="Radius"
        Vol_Cylinder={"Point_1":"App::PropertyVectorDistance",
                    "Point_2":"App::PropertyVectorDistance",
                    "Radius":"App::PropertyLength"}
########################################通用函数工具########################################
# 文档初始化时，创建分组
def initGroup():
    createInitGroup("PointG","点")
    createInitGroup("Line","线")
    createInitGroup("Area","面")
    createInitGroup("Annular","环形体")
    createInitGroup("Annular_Section","环形区域体")
    createInitGroup("Conformal","正投影体")
    createInitGroup("Cylinder","圆柱体")
    createInitGroup("Extruded","挤出体")
    createInitGroup("Function","函数体")
    createInitGroup("evolution","旋转体")
    createInitGroup("Helical","螺旋体")
    createInitGroup("Parallelepipedal","平行六面体")
    createInitGroup("Pyramid","金字塔体")
    createInitGroup("Rhombus","菱形体")
    createInitGroup("SpecialCone","圆锥体")
    createInitGroup("Spherical","球体")
    createInitGroup("Tetrahedron","四面体")
    createInitGroup("Toroidal_Section","半圆环体")
    createInitGroup("Wedge","楔形体")
    createInitGroup("Array","阵列体")
    createInitGroup("Draft","草图")

def createInitGroup(groupName,groupLabel):
    g=FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroup",groupName)
    g.Label=groupLabel
# 将obj进行分组
def addTheirGroupForObj(obj):
    if obj.Type==ObjectType.Point:
        addGroupForObj(obj,"PointG","点")
        pass
    elif obj.Type==ObjectType.Line_Conformal or obj.Type==ObjectType.Line_Oblique:
        addGroupForObj(obj,"Line","线")
    elif (obj.Type==ObjectType.Area_Conformal or obj.Type==ObjectType.Area_Polygonal 
            or obj.Type==ObjectType.Area_Rectangular) or obj.Type==ObjectType.Area_Function:
        addGroupForObj(obj,"Area","面")
    elif obj.Type==ObjectType.Vol_Annular:
        addGroupForObj(obj,"Annular","环形体")
    elif obj.Type==ObjectType.Vol_Annular_Section:
        addGroupForObj(obj,"Annular_Section","环形区域体")
    elif obj.Type==ObjectType.Vol_Conformal:
        addGroupForObj(obj,"Conformal","正投影体")
    elif obj.Type==ObjectType.Vol_Cylinder:
        addGroupForObj(obj,"Cylinder","圆柱体")
    elif obj.Type==ObjectType.Vol_Extruded:
        addGroupForObj(obj,"Extruded","挤出体")
    elif obj.Type==ObjectType.Vol_Function:
        addGroupForObj(obj,"Function","函数体")
    elif obj.Type==ObjectType.Vol_Revolution:
        addGroupForObj(obj,"Revolution","旋转体")
    elif obj.Type==ObjectType.Vol_Helical:
        addGroupForObj(obj,"Helical","螺旋体")
    elif obj.Type==ObjectType.Vol_Parallelepipedal:
        addGroupForObj(obj,"Parallelepipedal","平行六面体")
    elif obj.Type==ObjectType.Vol_Pyramid:
        addGroupForObj(obj,"Pyramid","金字塔体")
    elif obj.Type==ObjectType.Vol_Rhombus:
        addGroupForObj(obj,"Rhombus","菱形体")    
    elif obj.Type==ObjectType.Vol_SpecialCone:
        addGroupForObj(obj,"SpecialCone","圆锥体")
    elif obj.Type==ObjectType.Vol_Spherical:
        addGroupForObj(obj,"Spherical","球体")
    elif obj.Type==ObjectType.Vol_Tetrahedron:
        addGroupForObj(obj,"Tetrahedron","四面体")
    elif obj.Type==ObjectType.Vol_Toroidal_Section:
        addGroupForObj(obj,"Toroidal_Section","半圆环体")
    elif obj.Type==ObjectType.Vol_Wedge:
        addGroupForObj(obj,"Wedge","楔形体")
    elif obj.Type==ObjectType.Vol_Array or obj.Type==ObjectType.Vol_ParamArray:
        addGroupForObj(obj,"Array","阵列体")
    elif obj.Type==ObjectType.Vol_Draft_Extrude or obj.Type==ObjectType.Vol_Draft_Revolution:
        addGroupForObj(obj,"Draft","草图")

def addGroupForObj(obj,groupName,groupLabel):
    group=FreeCAD.ActiveDocument.getObjectsByLabel(groupLabel)
    if len(group):
        group[0].addObject(obj)
    else:
        group=FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroup",groupName)
        group.Label=groupLabel
        group.addObject(obj)
# 当复制对象是已经创建的group的时候，需要移除多余的group
def resetGroup(grp):
    import string
    #去掉grp中name后缀数字
    group=FreeCAD.ActiveDocument.getObject(grp.Name.rstrip(string.digits))
    if group!=grp:    
        for objItem in grp.OutList:
            grp.removeObject(objItem)
            group.addObject(objItem)
        # FreeCAD.ActiveDocument.removeObject(grp.Name)
    # FreeCAD.Console.PrintMessage(grp.Label)
    # FreeCAD.Console.PrintMessage("1grp:\n")
    # FreeCAD.Console.PrintMessage(grp.OutList)
    # FreeCAD.Console.PrintMessage("1\n")
    # # 如果不等，则表示group多余
    # if group!=grp:
    #     for objItem in grp.OutList:
    #         grp.removeObject(objItem)
    #         group.addObject(objItem)
    # FreeCAD.Console.PrintMessage(grp.Label)
    # FreeCAD.Console.PrintMessage("2grp:\n")
    # FreeCAD.Console.PrintMessage(grp.OutList)
    # FreeCAD.Console.PrintMessage("2\n")
        # FreeCAD.ActiveDocument.recompute()
        # FreeCAD.ActiveDocument.removeObject(grp.Name)
    # else:
    #     FreeCAD.Console.PrintMessage("group==")
# 重置工程（去掉工程中没有group的模型，显示resultShape）      
def resetProject():
    clipObj=FreeCAD.ActiveDocument.getObject("Generated__cross_section")
    if clipObj:
        FreeCAD.ActiveDocument.removeObject("Generated__cross_section")
    resultObj=FreeCAD.ActiveDocument.getObject("ResultShape")
    resultObj.ViewObject.Visibility=True
# 判断四个点是否共面
def isFourPointsOnTheSamePlane(points):
    '''
    points:   []长度为4的list
    return:   四个点在一个平面上：True
              否则：False
    '''
    point_1=points[0]
    point_2=points[1]
    point_3=points[2]
    point_4=points[3]
    points.append(point_1)
    try:
        wires=Part.makePolygon(points)
        shape=Part.makeFace(wires,"Part::FaceMakerBullseye")
    except Base.FreeCADError as identifier:
        return False
        pass
    return True
# 判断一个物体是否含有某个属性
def hasTheProperty(objLabel,prop):
    objs=FreeCAD.ActiveDocument.getObjectsByLabel(objLabel)
    if len(objs):
        obj=objs[0]
        props=obj.PropertiesList
        for propItem in props:
            if propItem==prop:
                return True
        return False
        pass
    else:
        FreeCAD.Console.PrintErrot(objLabel+" cann't be found.")
        return False

# 判断一个物体是否含有某个属性
def hasThePropertyByObj(obj,prop):
    if obj:
        props=obj.PropertiesList
        for propItem in props:
            if propItem==prop:
                return True
        return False
        pass
    else:
        # FreeCAD.Console.PrintErrot(objLabel+" cann't be found.")
        return False
# 为paramObj设置DX1等属性
def setDX1DX2DX3(DX1,DX2,DX3):
    paramObj=getParamObj()

    typeOfDX1=UnitTools.getTypeOfData(DX1)
    # 如果是string类型则表示，这个变量是前面定义过的变量名
    # if typeOfDX1==UnitTools.SupportUnitType.STRING:
    resultList=UnitTools.getTypeOfPossiblePropertyName(paramObj,"DX1",DX1)
    DX1=resultList[0]
    typeOfDX1=resultList[1]

    if hasattr(paramObj,"DX1"):
        paramObj.removeProperty("DX1")
    paramObj.addProperty('App::Property'+typeOfDX1,"DX1","Base","")
    paramObj.setExpression("DX1", DX1)


    typeOfDX2=UnitTools.getTypeOfData(DX2)
    # if typeOfDX2==UnitTools.SupportUnitType.STRING:
    resultList=UnitTools.getTypeOfPossiblePropertyName(paramObj,"DX2",DX2)
    DX2=resultList[0]
    typeOfDX2=resultList[1]
    
    if hasattr(paramObj,"DX2"):
        paramObj.removeProperty("DX2")
    paramObj.addProperty('App::Property'+typeOfDX2,"DX2","Base","")
    paramObj.setExpression("DX2", DX2)


    typeOfDX3=UnitTools.getTypeOfData(DX3)
    # if typeOfDX3==UnitTools.SupportUnitType.STRING:
    resultList=UnitTools.getTypeOfPossiblePropertyName(paramObj,"DX3",DX3)
    DX3=resultList[0]
    typeOfDX3=resultList[1]

    if hasattr(paramObj,"DX3"):
        paramObj.removeProperty("DX3")
    paramObj.addProperty('App::Property'+typeOfDX3,"DX3","Base","")

    paramObj.setExpression("DX3", DX3)

    paramObj.setEditorMode('DX1',1)
    paramObj.setEditorMode('DX2',1)
    paramObj.setEditorMode('DX3',1)
    FreeCAD.ActiveDocument.recompute()
# 将paramObj的所有属性设置为不可更改模式
def setImmutableOfParamObjFromUI():
    obj=getParamObj()
    properties=obj.PropertiesList
    for propItem in properties:
        #[]表示可见可改，["Hidden"]表示隐藏，["ReadOnly"]只读
        # 0,可见可改1只读，2隐藏
        if obj.getEditorMode(propItem)==[]:
            obj.setEditorMode(propItem,1)

# 得到参数定义对象
def getParamObj():
    # 获得变量对象
    objsInDoc=FreeCAD.ActiveDocument.Objects
    paramObj=None
    for objItem in objsInDoc:
        if hasattr(objItem,"DynamicData"):
            paramObj=objItem
            break
    # 若不存在，则新建
    if paramObj==None:
        paramObj=DynamicData.DynamicDataCmd.DynamicDataCreateObjectCommandClass().Activated()
    return paramObj
# 通过label得到模型
def getObjByLabel(label):
    objs=FreeCAD.ActiveDocument.getObjectsByLabel(label)
    if len(objs)==0:
        raise RuntimeError('does not has this obj')
    obj=objs[0]
    return obj
    

# 判断一个物体是否包含某个属性列表
def hasTheProperties(objLabel,propList):
    objs=FreeCAD.ActiveDocument.getObjectsByLabel(objLabel)
    if len(objs):
        obj=objs[0]
        props=obj.PropertiesList
        return set(propList).issubset(set(props))
#根据obj判断一个物体是否包含某个属性列表
def hasThePropertiesByObj(obj,propList):
    props=obj.PropertiesList
    return set(propList).issubset(set(props))


def getLabelWithoutOrder(obj):
    label=obj.Label
    label=re.sub(r"^\[\d+\]_","",label)
    return label




        # 用于获取模型文本文件网格的函数
def getMarkCommands(objectLabel):
    """
    获取当前物体的非均匀网格的值，
    return [isX1,isX2,isX3,X1Size,X2Size,X3Size]
    """
    objs=FreeCAD.ActiveDocument.getObjectsByLabel(objectLabel)
    isX1=False 
    isX2=False
    isX3=False
    X1Size=""
    X2Size=""
    X3Size=""
    results=[]
    if len(objs):
        obj=objs[0]
        curCoordinateSys=obj.Document.CoordinateSystem
        if curCoordinateSys==CoordinateSystemTools.CoordinateType.Rectangular:
            isX1=obj.X
            isX2=obj.Y
            isX3=obj.Z
            X1Size=str(obj.X_Value.Value)+"mm"
            X2Size=str(obj.Y_Value.Value)+"mm"
            X3Size=str(obj.Z_Value.Value)+"mm"
        elif curCoordinateSys==CoordinateSystemTools.CoordinateType.Polar or CoordinateSystemTools.CoordinateType.Cylindrical:
            isX1=obj.R
            isX2=obj.Theta
            isX3=obj.Z
            X1Size=str(obj.R_Value.Value)+"mm"
            X2Size=str(obj.Theta_Value.Value)+"deg"
            X3Size=str(obj.Z_Value.Value)+"mm"
        # if curCoordinateSys==CoordinateSystemTools.CoordinateType.Cylindrical:
        #     isX1=obj.Z
        #     isX2=obj.R
        #     isX3=obj.Theta
        #     X1Size=str(obj.Z_Value.Value)+"mm"
        #     X2Size=str(obj.R_Value.Value)+"mm"
        #     X3Size=str(obj.Theta_Value.Value)+"deg"
        
    else:
        FreeCAD.Console.PrintError(objectLabel+" cann't be found.\n")
    # FreeCAD.Console.PrintMessage("isX1:"+str(isX1)+"isX2:"+str(isX2)+"isX3:"+str(isX3)+"X1:"+X1Size+"X2:"+X2Size+"X3:"+X3Size)
    results=[isX1,isX2,isX3,X1Size,X2Size,X3Size]
    return results
def findObjByLabelWithoutOrderAndInvisible(labelWithoutOrder):
    doc=FreeCAD.ActiveDocument
    objs=getListOfOrderedObjects(doc.Name)
    for objItem in objs:
        if getRealNameBySplitObjectLabel(objItem)==labelWithoutOrder:
            Gui.ActiveDocument.getObject(objItem.Name).Visibility=False
            return True
    return False

def findObjByLabelWithoutOrderAndVisible(labelWithoutOrder):
    try:
        doc=FreeCAD.ActiveDocument
        objs=getListOfOrderedObjects(doc.Name)
        for objItem in objs:
            if getRealNameBySplitObjectLabel(objItem)==labelWithoutOrder:
                Gui.ActiveDocument.getObject(objItem.Name).Visibility=True
                return True
        return False
    except:
        FreeCAD.Console.PrintError("findObjByLabelWithoutOrderAndVisible Wrong!\n")


def setRandColor(obj):
    '''
    为模型生成随机颜色
    '''
    if FreeCADGui.ActiveDocument.getObject(obj.Name).ShapeColor==(0.800000011920929, 0.800000011920929, 0.800000011920929, 0.0):
        import random as rd
        FreeCADGui.ActiveDocument.getObject(obj.Name).ShapeColor=(rd.random(),rd.random(),rd.random())
        pass
    else:
        FreeCAD.Console.PrintError(FreeCADGui.ActiveDocument.getObject(obj.Name).ShapeColor)
# 设置初始默认值
def setInitTransparency(obj):
    FreeCADGui.ActiveDocument.getObject(obj.Name).Transparency=95

# 新建模型后，该模型最大视图
def setObjToFitTheView (obj):
    '''
    obj:    被放到适合位置的物体
    return: none
    '''
    # TypeId:对象在C++中的TypeId,本程序所有的模型均为“Part::PartFeature”
    if obj.TypeId == "Part::FeaturePython":
        #清除所有的选择
        Gui.Selection.clearSelection()
        # 增加当前选择
        Gui.Selection.addSelection(obj)
        # 将当前选择的物体放在镜头前合适位置
        Gui.SendMsgToActiveView("ViewSelection")

def setFitViewOfObject(obj):
    setObjToFitTheView(obj)
    FreeCADGui.ActiveDocument.getObject(obj.Name).Transparency=0

# 判断是数还是字符串
def isNumber(n):
    result=True
    try:
        num=float(n)
        result = num == num
    except ValueError:
        result=False
    return result
# 根据索引返回坐标值下标
def returnSubscriptInCoor(i,curCoordinateSys):
    if curCoordinateSys==CoordinateSystemTools.CoordinateType.Rectangular or curCoordinateSys==CoordinateSystemTools.CoordinateType.Polar:
        if i==0:
            return ".x"
        elif i==1:
            return ".y"
        elif i==2:
            return ".z"
        else:
            FreeCAD.Console.PrintError("Error 20190817\n")
    else:
        if i==0:
            return ".z"
        elif i==1:
            return ".x"
        elif i==2:
            return ".y"
        else:
            FreeCAD.Console.PrintError("Error 20190817\n")
def handleVauleStr(valueStr):
    '''
       处理m3d中值得字符串
       将 valueStr="ee"        ->"dd.ee"
                   "ee + 11mm" ->"dd.ee+11mm"
                   "11mm"      ->直接赋值
    '''
    obj=getParamObj()
    paramName=obj.Name+"."
    # 先去掉所有的空格
    valueStr=valueStr.replace(" ","")
    resultStr=""
    # flagCurState 表示当前的状态，遇到“+”、“-”、“*”、“/”后改变状态
    flagCurState=False
    # 临时str,存放类似上面“ee”的字符串
    tempStr=""
    # FreeCAD.Console.PrintMessage("valueStr "+str(valueStr)+"\n")
    for letterItem in valueStr:
        if letterItem=="+" or letterItem=="-" or letterItem=="*" or letterItem=="/":
            if tempStr=="":
                pass
            # 如果是数字  直接赋值
            elif isNumber(tempStr):
                resultStr=resultStr+tempStr
            else:
                # 如果第一位是数字，则表示它是类似“11mm”或者“30deg”这种的字符串，也直接相加
                # if isNumber(tempStr[0]):
                FreeCAD.Console.PrintMessage("tempStr\n")
                if UnitTools.isValueWithUnit(tempStr):
                    resultStr=resultStr+tempStr
                    # FreeCAD.Console.PrintMessage("tempStr 1"+str(resultStr)+"\n")

                # 否则在字符串上加dd
                else:
                    resultStr=resultStr+paramName+tempStr
                    # FreeCAD.Console.PrintMessage("tempStr 2"+str(resultStr)+"\n")

            resultStr=resultStr+letterItem
            tempStr=""
        else:
            tempStr=tempStr+letterItem
    # 最后还得处理下tempStr
    # 如果是数字  直接赋值
    if isNumber(tempStr):
        resultStr=resultStr+tempStr
    else:
        # 如果第一位是数字，则表示它是类似“11mm”或者“30deg”这种的字符串，也直接相加
        if isNumber(tempStr[0]):
            resultStr=resultStr+tempStr
        # 否则在字符串上加dd
        else:
            resultStr=resultStr+paramName+tempStr
    # FreeCAD.Console.PrintMessage("resultStr: "+str(resultStr)+"\n")
    return resultStr
def handleExpressionStr(expressionStr):
    '''
       处理字符串表达式
       例如 expressionStr="dd.ll + dd001.ee" 将其转化为 "ll+ee"
                           dd.ll+11 mm                ll+11mm

    '''
    # flagCurState 表示当前的状态，遇到“.”或者“+”、“-”、“*”、“/”后改变状态
    flagCurState=False
    # 先去掉空格
    expressionStr=expressionStr.replace(" ","")
    resultStr=""
    # 临时字符串：因为不知道加减乘除后面的是否是dd001还是有用的 11mm 所以先暂存起来
    tempStr=""
    for letterItem in expressionStr:
        if letterItem ==".":
            if isNumber(tempStr):
                tempStr=tempStr+letterItem
                pass
            else:
                flagCurState=True
                tempStr=""
        elif letterItem=="+" or letterItem=="-" or letterItem=="*" or letterItem=="/":
            flagCurState=False
            if not tempStr=="":
                resultStr=resultStr+tempStr
                tempStr=""
            resultStr=resultStr+letterItem
        else:
            if flagCurState:
                resultStr=resultStr+letterItem
            else:
                tempStr=tempStr+letterItem
    if not tempStr=="":
        resultStr=resultStr+tempStr
    return resultStr
    pass
# 将表达式或者具体值转化为属性值  
def turnExpressionToProperty(obj,propertyName,propertyValue):
    '''
        @obj:           需要转换的对象
        @propertyName:  属性名称
        @propertyValue: 属性在m3d中的值，可能是具体的值 也有可能是变量
    '''
    # 表示是一个列表，point
    # if hasattr(propertyValue,"__len__"):
    if isinstance(propertyValue,list):
        # 长度为3时才正常
        if len(propertyValue)==3:
            # 一次处理每一个值
            for index in range(len(propertyValue)):
                #如果是具体的值,且不带单位
                if isNumber(propertyValue[index]):
                    # setattr(obj,propertyName+returnSubscriptInCoor(index),propertyValue[index])
                    if obj.Document.CoordinateSystem==CoordinateSystemTools.CoordinateType.Rectangular or obj.Document.CoordinateSystem==CoordinateSystemTools.CoordinateType.Polar:                     
                        if index==0:
                            getattr(obj,propertyName).x=float(propertyValue[index])
                        elif index==1:
                            getattr(obj,propertyName).y=float(propertyValue[index])
                        else:
                            getattr(obj,propertyName).z=float(propertyValue[index])
                        pass
                    else:
                        if index==0:
                            getattr(obj,propertyName).z=float(propertyValue[index])
                        elif index==1:
                            getattr(obj,propertyName).x=float(propertyValue[index])
                        else:
                            getattr(obj,propertyName).y=float(propertyValue[index])
                        pass 
                #带单位或者变量
                else:
                    # 去掉末尾单位，并去掉两端空格
                    propertyValueWithoutUnit1=propertyValue[index].replace("m","").replace("deg","").strip(" ")
                    propertyValueWithoutUnit2=propertyValue[index].replace("mm","").strip(" ")
                    propertyValueWithoutUnit3=propertyValue[index].replace("cm","").strip(" ")
                    
                    if UnitTools.getTypeOfData(propertyValue[index]) != UnitTools.SupportUnitType.STRING:
                        valueWithDefaultUnit=UnitTools.getDataOfDefauleUnit(propertyValue[index],UnitTools.defauleUnit)
                        value=UnitTools.getValueAndUnitOfData(valueWithDefaultUnit)[0]
                        if obj.Document.CoordinateSystem==CoordinateSystemTools.CoordinateType.Rectangular or obj.Document.CoordinateSystem==CoordinateSystemTools.CoordinateType.Polar:
                            if index==0:
                                getattr(obj,propertyName).x=float(value)
                            elif index==1:
                                getattr(obj,propertyName).y=float(value)
                            else:
                                getattr(obj,propertyName).z=float(value)
                        else:
                            if index==0:
                                getattr(obj,propertyName).z=float(value)
                            elif index==1:
                                getattr(obj,propertyName).x=float(value)
                            else:
                                getattr(obj,propertyName).y=float(value)
                    #变量  或者变量加上具体值，即表达式
                    else:
                        # obj.setExpression(propertyName,u"dd."+str(propertyValueWithoutUnit))
                        obj.setExpression(propertyName+returnSubscriptInCoor(index,obj.Document.CoordinateSystem),handleVauleStr(propertyValue[index]))
                    pass
        else:
            FreeCAD.Console.PrintError("Error Log 20190817! "+str(len(propertyValue)))
    # 不是point属性
    else:
        #如果是具体的值,且不带单位
        if isNumber(propertyValue):
            setattr(obj,propertyName,int(propertyValue))
            pass
        #带单位或者变量
        else:
            # 去掉末尾单位，并去掉两端空格
            propertyValueWithoutUnit1=propertyValue.replace("m","").replace("deg","").strip(" ")
            propertyValueWithoutUnit2=propertyValue.replace("mm","").strip(" ")
            propertyValueWithoutUnit3=propertyValue.replace("cm","").strip(" ")
            #带单位
            if isNumber(propertyValue[:-1].replace(" ","")) and propertyValue.endswith("m") :
                setattr(obj,propertyName,float(propertyValueWithoutUnit1))
            elif isNumber(propertyValue[:-2].replace(" ","")) and propertyValue.endswith("mm") :
                setattr(obj,propertyName,float(propertyValueWithoutUnit1)*0.001)
            elif isNumber(propertyValue[:-2].replace(" ","")) and propertyValue.endswith("cm") :
                setattr(obj,propertyName,float(propertyValueWithoutUnit1*0.01))
            elif isNumber(propertyValue[:-3].replace(" ","")) and propertyValue.endswith("deg") :
                setattr(obj,propertyName,float(propertyValueWithoutUnit1))
            #变量  或者变量加上具体值，即表达式
            else:
                # obj.setExpression(propertyName,u"dd."+str(propertyValueWithoutUnit))
                obj.setExpression(propertyName,handleVauleStr(propertyValue))
            pass
# 将属性转换为带有表达式的值
def turnPropertyToExpression(obj,propertyName):
    '''
        @obj:          需要转换的对象
        @propertyName: 需要转换的对象的属性
        @return：      转换以后的属性值
    '''
    coordinateSystem=FreeCAD.ActiveDocument.CoordinateSystem
    result=""
    propertyValue=None
    try:
        # 这里得到对象该属性的值
        propertyValue=obj.getPropertyByName(propertyName)
    except AttributeError :
        return None
        pass
    #获得该模型的所有表达式[("property","value"),()]
    propertiesList=obj.ExpressionEngine
    # 判断该对象的属性是否具有Value参数
    if hasattr(propertyValue,"Value"):
        valueList=str(propertyValue).split(" ")
        if len(valueList)==2:
            result=str(propertyValue.Value)+str(propertyValue).split(" ")[1]
        else:
            result=propertyValue.Value
    # 列表,point
    elif hasattr(propertyValue,"__len__"):
    # elif isinstance(propertyValue,list): *1000的意思是将m->mm
        if coordinateSystem==CoordinateSystemTools.CoordinateType.Rectangular:
            result=[propertyValue[0],propertyValue[1],propertyValue[2]]
        else:
            result=[propertyValue[0],propertyValue[1],propertyValue[2]]
    else:
        result=propertyValue
    if len(propertiesList)==0:
        return result
    # 如果传入的属性是列表,这里默认为point属性
    elif  hasattr(propertyValue,"__len__"):
    # elif  isinstance(propertyValue,list):
        for index in range(len(propertiesList)):
            if propertiesList[index][0]==str(propertyName+".x"):
                # result[0]=propertiesList[index][1].split(".")[1]
                result[0]=handleExpressionStr(propertiesList[index][1])
            elif propertiesList[index][0]==str(propertyName+".y"):
                # result[1]=propertiesList[index][1].split(".")[1]
                result[1]=handleExpressionStr(propertiesList[index][1])
            elif propertiesList[index][0]==str(propertyName+".z"):
                # result[2]=propertiesList[index][1].split(".")[1]
                result[2]=handleExpressionStr(propertiesList[index][1])
        return result
    #非列表属性
    else:
        for index in range(len(propertiesList)):
            if propertiesList[index][0]==propertyName:
                # result=propertiesList[index][1].split(".")[1]
                result=handleExpressionStr(propertiesList[index][1])
                return result
                break
    return result
        
# 定义一个类：obj,level
class ObjectWithTransparencyLevel:
    def __init__(self,objItem,lev):
        self.obj=objItem
        self.level=lev
    def show(self):
        # FreeCAD.Console.PrintMessage("obj: "+str(self.obj.Label)+" level: "+str(self.level)+"\n")
        pass
    # def create(self,obj,level)
def showObjectWithTransparencyLevel(flag,orderLevelOfBoundBox):
    for ObjectWithTransparencyLevelItem in orderLevelOfBoundBox:
        FreeCAD.Console.PrintMessage(str(ObjectWithTransparencyLevelItem.obj.Label)+" "+str(ObjectWithTransparencyLevelItem.level)+"\n")
# 获取场景中所有的导体数量,及他们的包围盒有小到大的排序：理想导体与自定义导体
def lGetNumAndOrderBoundBoxOfConductor():
    '''
        return: [numofConducotr,numoflevels,obj1,obj2...]
    '''
    objsList=FreeCAD.ActiveDocument.Objects
    numofConducotr=0
    numoflevels=0
    orderLevelOfBoundBox=[]
    for objItem in objsList:
        if hasThePropertyByObj(objItem,"Attribute"):
            if objItem.Attribute==Attribute.Conductor or objItem.Attribute== Attribute.Custom:
                numofConducotr=numofConducotr+1
                # 若为空，直接将其加入，numoflevels++
                if len(orderLevelOfBoundBox)==0:
                    numoflevels=numoflevels+1
                    orderLevelOfBoundBox.append(ObjectWithTransparencyLevel(objItem,numoflevels))
                    # showObjectWithTransparencyLevel(1,orderLevelOfBoundBox)
                else:
                    for objectWithTransparencyLevelItem in orderLevelOfBoundBox:
                        # objItem在objectWithTransparencyLevelItem.obj的内部：
                        #   若objectWithTransparencyLevelItem.obj不是第一个，则将objItem放在它的前一层,level=前一层level
                        #   .......................................是......，将objItem插入最前方，numoflevels++
                        #objItem在objectWithTransparencyLevelItem.obj的外部或者相交：
                        #   下一个objectWithTransparencyLevelItem
                        #
                        if checkBoundBox(objItem,objectWithTransparencyLevelItem.obj)<0:
                            if orderLevelOfBoundBox.index(objectWithTransparencyLevelItem)==0:
                                numoflevels=numoflevels+1
                                orderLevelOfBoundBox.insert(0,ObjectWithTransparencyLevel(objItem,numoflevels))
                                # showObjectWithTransparencyLevel(2,orderLevelOfBoundBox)
                            else:
                                for ind in range(orderLevelOfBoundBox.index(objectWithTransparencyLevelItem),0,-1):
                                    if not orderLevelOfBoundBox[ind].level == objectWithTransparencyLevelItem.level:
                                        orderLevelOfBoundBox.insert(ind+1,ObjectWithTransparencyLevel(objItem,orderLevelOfBoundBox[ind].level))
                                        # showObjectWithTransparencyLevel(3,orderLevelOfBoundBox)
                                        break
                            break
                        elif checkBoundBox(objItem,objectWithTransparencyLevelItem.obj)==0:
                            orderLevelOfBoundBox.insert(orderLevelOfBoundBox.index(objectWithTransparencyLevelItem)+1,ObjectWithTransparencyLevel(objItem,objectWithTransparencyLevelItem.level))
                            # showObjectWithTransparencyLevel(4,orderLevelOfBoundBox)
                            break
                        # objItem在objectWithTransparencyLevelItem 外部  并且循环到了最后一个模型，在其后面追加
                        elif checkBoundBox(objItem,objectWithTransparencyLevelItem.obj)>0 and objectWithTransparencyLevelItem==orderLevelOfBoundBox[len(orderLevelOfBoundBox)-1]:
                            numoflevels=numoflevels+1
                            orderLevelOfBoundBox.append(ObjectWithTransparencyLevel(objItem,numoflevels))
                            # showObjectWithTransparencyLevel(5,orderLevelOfBoundBox)
                            break
                            pass
                        # objItem在objectWithTransparencyLevelItem 外部  但是不是最后一个
                        elif checkBoundBox(objItem,objectWithTransparencyLevelItem.obj)>0 and not objectWithTransparencyLevelItem==orderLevelOfBoundBox[len(orderLevelOfBoundBox)-1]:
                            pass
                        else:
                            pass
        
    orderLevelOfBoundBox.insert(0,numofConducotr)
    orderLevelOfBoundBox.insert(1,numoflevels)
    # # FreeCAD.Console.PrintMessage(orderLevelOfBoundBox)
    # for i in range(len(orderLevelOfBoundBox)):
    #     if i<=1:
    #         FreeCAD.Console.PrintMessage(str(orderLevelOfBoundBox[i])+"\n")
    #     else:
    #         orderLevelOfBoundBox[i].show()
    # FreeCAD.Console.PrintMessage("End:\n")
    return orderLevelOfBoundBox

def checkBoundBox(theFirstObj,theSecondObj):
    # FreeCAD.Console.PrintMessage("Name:"+str(theFirstObj.Name)+" "+str(theFirstObj.Shape.BoundBox)+"\n")
    import exceptions
    try:
        if theSecondObj.Shape.BoundBox.isInside(theFirstObj.Shape.BoundBox):
            theFirstBoundBox=theFirstObj.Shape.BoundBox
            theSecondBoundBox=theSecondObj.Shape.BoundBox
            if theFirstBoundBox.XMin==theSecondBoundBox.XMin and theFirstBoundBox.YMin==theSecondBoundBox.YMin and theFirstBoundBox.ZMin==theSecondBoundBox.ZMin and theFirstBoundBox.XMax==theSecondBoundBox.XMax and theFirstBoundBox.YMax==theSecondBoundBox.YMax and theFirstBoundBox.ZMax==theSecondBoundBox.ZMax:
                # 两者的包围盒相同
                return 0
            # theFirstObj 在 theSecondObj 的 外部
            return -1
        else: 
            # theFirstObj 在 theSecondObj 的内部
            return 1
    except exceptions.FloatingPointError as e:
        FreeCAD.Console.PrintError(e)

#------------------------------------------结束-------------------------------------------#




########################################建模用的工具函数########################################

# 已知两个极坐标点，求两个点形成的薄管形
def getPipeObj(polarPoint1,polarPoint2):
    tempP1=CoordinateSystemTools.otherToRecOne("Polar",polarPoint1)
    tempP2=CoordinateSystemTools.otherToRecOne("Polar",FreeCAD.Vector(polarPoint1.x,polarPoint1.y,polarPoint2.z))
    
    starAngle=polarPoint1.y
    endAngle=polarPoint2.y
    dir=FreeCAD.Vector(0,0,2)
    #这样设置可以生成面片
    if starAngle==endAngle:
        endAngle=starAngle+0.01
    line=Part.makeLine(tempP1,tempP2)
    if tempP1==tempP2:
        resultShape=Part.makeCircle(polarPoint1.x,FreeCAD.Vector(0,0,tempP1.z),dir,starAngle,endAngle)
    else:

        linePath=Part.makeCircle((polarPoint1.x+polarPoint2.x)/2,FreeCAD.Vector(0,0,tempP1.z),dir,starAngle,endAngle)
        path=Part.Wire(linePath)
        resultShape=path.makePipe(line)
    return resultShape
#极坐标系下两个点得到扇形
def getArcObj(polarPoint1,polarPoint2):
    tempP1=CoordinateSystemTools.otherToRecOne("Polar",polarPoint1)
    tempP2=CoordinateSystemTools.otherToRecOne("Polar",FreeCAD.Vector(polarPoint2.x,polarPoint1.y,polarPoint2.z))

    startAngle=polarPoint1.y
    endAngle=polarPoint2.y
    dir=FreeCAD.Vector(0,0,2)
    #这样设置可以生成面片
    if startAngle==endAngle:
        endAngle=startAngle+0.01
    if tempP1==tempP2:
        # 排除polarPoint.x为0
        if not polarPoint2 == 0.0:
            resultShape=Part.makeCircle(math.fabs((polarPoint2.x)),FreeCAD.Vector(0,0,tempP1.z),dir,startAngle,endAngle)
        else:
            resultShape=Part.makeSphere(0.0001,tempP1)
    else:
        if math.fabs(startAngle-endAngle)==360:
            wires=[]
            if not polarPoint1.x ==0.0:
                arcLine1=Part.makeCircle(math.fabs(polarPoint1.x),FreeCAD.Vector(0,0,tempP1.z),dir,polarPoint1.y,polarPoint2.y)
                wires.append(arcLine1)
            if not polarPoint2.x==0.0:
                arcLine2=Part.makeCircle(math.fabs(polarPoint2.x),FreeCAD.Vector(0,0,tempP2.z),dir,polarPoint1.y,polarPoint2.y)
                wires.append(arcLine2)
            shapeCircle = Part.makeFace(wires, "Part::FaceMakerBullseye")
            resultShape=shapeCircle
        else:
            line=Part.makeLine(tempP1,tempP2)
            linePath=Part.makeCircle(math.fabs((polarPoint1.x+polarPoint2.x)/2),FreeCAD.Vector(0,0,tempP1.z),dir,startAngle,endAngle)
            path=Part.Wire(linePath)
            resultShape=path.makePipe(line)


    return resultShape
#在体模型刷新形状后需要做的事：先加上体的形状检查，后面还需要的话可以再加
def doSomethingAfterRecomputerVolShape(obj):
    checkVolShape(obj)

# 测试一个shape是不是一个体，如果不是的话，提示
def checkVolShape(obj):
    if hasattr(obj,"Type"):
        if obj.Type.startswith("Vol"):
            if (len(obj.Shape.Faces)<=1) and not obj.Type==ObjectType.Vol_Spherical:
                # FreeCAD.Console.PrintMessage(str(obj.Label)+"is not vol\n")
                # 去掉它的shape属性
                obj.Shape=obj.Shape.removeShape(obj.Shape.Faces)
                # obj.ViewObject.Visibility=False
            # boundBox=obj.Shape.BoundBox
            # xmin=boundBox.XMin
            # xmax=boundBox.XMax
            # ymin=boundBox.YMin
            # ymmax=boundBox.YMax
            # zmin=boundBox.ZMin
            # Zmax=boundBox.ZMax
            # precision=1e-4
            # if  math.fabs(xmax-xmin)<=precision or math.fabs(ymax-ymin)<=precision or math.fabs(zmax-zmin)<=precision:
            #     DocumentTools.errorMessage(str(obj.Label)+u"的形状不是一个体！\n")
# 如果两个点重合则形成一个点
def makePoint(position):
    obj=Part.makeSphere(0.0001,position)
    return obj

# 直角坐标系下任意两个点得到矩形
def getConformalArea(curCoordinateSystem,startPoint,EndPoint,normal):
    pass

# 创建一个弧形
def makeCircle(radius, placement=None, face=None, startangle=None, endangle=None, support=None):
    '''makeCircle(radius,[placement,face,startangle,endangle])
    or makeCircle(edge,[face]):
    Creates a circle object with given radius. If placement is given, it is
    used. If face is False, the circle is shown as a
    wireframe, otherwise as a face. If startangle AND endangle are given
    (in degrees), they are used and the object appears as an arc. If an edge
    is passed, its Curve must be a Part.Circle'''
    import Part, DraftGeomUtils
    if placement: typecheck([(placement,FreeCAD.Placement)], "makeCircle")
    if startangle != endangle:
        n = "Arc"
    else:
        n = "Circle"
    obj = FreeCAD.ActiveDocument.addObject("Part::Part2DObjectPython",n)
    _Circle(obj)
    if face != None:
        obj.MakeFace = face
    if isinstance(radius,Part.Edge):
        edge = radius
        if DraftGeomUtils.geomType(edge) == "Circle":
            obj.Radius = edge.Curve.Radius
            placement = FreeCAD.Placement(edge.Placement)
            delta = edge.Curve.Center.sub(placement.Base)
            placement.move(delta)
            if len(edge.Vertexes) > 1:
                ref = placement.multVec(FreeCAD.Vector(1,0,0))
                v1 = (edge.Vertexes[0].Point).sub(edge.Curve.Center)
                v2 = (edge.Vertexes[-1].Point).sub(edge.Curve.Center)
                a1 = -math.degrees(DraftVecUtils.angle(v1,ref))
                a2 = -math.degrees(DraftVecUtils.angle(v2,ref))
                obj.FirstAngle = a1
                obj.LastAngle = a2
    else:
        obj.Radius = radius
        if (startangle != None) and (endangle != None):
            if startangle == -0: startangle = 0
            obj.FirstAngle = startangle
            obj.LastAngle = endangle
    obj.Support = support
    if placement: obj.Placement = placement
    if gui:
        _ViewProviderDraft(obj.ViewObject)
        formatObject(obj)
        select(obj)
    FreeCAD.ActiveDocument.recompute()
    return obj

# 通过两个点（取值范围）得到直角坐标系下取值范围
def getRMinMaxPoints(pointMin,pointMax,coordinate):
    '''
    @ 思路是得到这样的一个conformal的Shape，通过这个Shape得到包围盒

    '''
    resultShape=None

    if coordinate=='Rectangular':
        length = abs(pointMin.x - pointMax.x)
        width = abs(pointMin.y - pointMax.y)
        height = abs(pointMin.z - pointMax.z)
        dir=FreeCAD.Vector(0,0,1)
        try:
            resultShape  = Part.makeBox(length, width, height, pointMin, dir)
        except:
            DocumentTools.printErrorMessage("Redraw Conformal Failed!")
            return
            pass
        # resultShape  = Part.makeBox(length, width, height, pointMin, dir)
        pass
    elif coordinate=='Polar' or coordinate=='Cylindrical':
        tempP1=CoordinateSystemTools.otherToRecOne(coordinate,pointMin)
        tempP2=CoordinateSystemTools.otherToRecOne(coordinate,FreeCAD.Vector(pointMax.x,pointMin.y,pointMin.z))
        tempP3=CoordinateSystemTools.otherToRecOne(coordinate,FreeCAD.Vector(pointMax.x,pointMin.y,pointMax.z))
        tempP4=CoordinateSystemTools.otherToRecOne(coordinate,FreeCAD.Vector(pointMin.x,pointMin.y,pointMax.z))
        
        #只有一个点的情况
        if tempP1==tempP2 and tempP2==tempP4:
            resultShape=makePoint(tempP1)
        #防止两个点重合出现错误的情况
        elif tempP1==tempP2:
            if tempP3==tempP4:
                resultShape=Part.makeLine(tempP1,tempP3)
            else:
                resultShape=getPipeObj(pointMin,pointMax)
        elif tempP1==tempP4:
            # tempP4=tempP4.add(FreeCAD.Vector(0,0,0.01))
            resultShape=getArcObj(pointMin,pointMax)
        else:
            # line1=Part.makeLine(tempP1,tempP2)
            line2=Part.makeLine(tempP1,tempP4)
            shapeCir=getArcObj(FreeCAD.Vector(pointMin.x,pointMin.y,pointMax.z),pointMax)
            path=Part.Wire(line2)
            resultShape=path.makePipe(shapeCir)
            pass
    boundBox=resultShape.BoundBox
    return [[boundBox.XMin,boundBox.YMin,boundBox.ZMin],[boundBox.XMax,boundBox.YMax,boundBox.ZMax]]

#通过两个点得到一个conformal的shape(借鉴comformal体)
def getShapeOfComformal(curCoordinateSys, pointmin,pointmax):
    resultShape=None
    Point1=pointmin
    Point2=pointmax
    if curCoordinateSys=='Rectangular':
        length = abs(Point1.x - Point2.x)
        width = abs(Point1.y - Point2.y)
        height = abs(Point1.z - Point2.z)
        dir=FreeCAD.Vector(0,0,1)
        try:
            resultShape  = Part.makeBox(length, width, height, Point1, dir)
        except:
            DocumentTools.printErrorMessage("Redraw Conformal Failed!")
            return
            pass
        # Shape  = Part.makeBox(length, width, height, Point1, dir)
        pass
    elif curCoordinateSys=='Polar' or curCoordinateSys=='Cylindrical':
        tempP1=CoordinateSystemTools.otherToRecOne(curCoordinateSys,Point1)
        tempP2=CoordinateSystemTools.otherToRecOne(curCoordinateSys,FreeCAD.Vector(Point2.x,Point1.y,Point1.z))
        tempP3=CoordinateSystemTools.otherToRecOne(curCoordinateSys,FreeCAD.Vector(Point2.x,Point1.y,Point2.z))
        tempP4=CoordinateSystemTools.otherToRecOne(curCoordinateSys,FreeCAD.Vector(Point1.x,Point1.y,Point2.z))
        
        #只有一个点的情况
        if tempP1==tempP2 and tempP2==tempP4:
            # Shape=Part.Vertex(FreeCAD.Vector(tempP1.x,tempP1.y,tempP1.z))
            # Shape=Part.makeBox(0.001,0.001,0.001,tempP1)
            # return
            resultShape=makePoint(tempP1)
        #防止两个点重合出现错误的情况
        elif tempP1==tempP2:
            # tempP2=tempP2.add(FreeCAD.Vector(0.001*math.cos(tempP2.y),0.001*math.sin(tempP2.y),0))
            if tempP3==tempP4:
                resultShape=Part.makeLine(tempP1,tempP3)
            else:
                resultShape=getPipeObj(Point1,Point2)
        elif tempP1==tempP4:
            # tempP4=tempP4.add(FreeCAD.Vector(0,0,0.01))
            resultShape=getArcObj(Point1,Point2)
        else:
            # line1=Part.makeLine(tempP1,tempP2)
            line2=Part.makeLine(tempP1,tempP4)
            shapeCir=getArcObj(FreeCAD.Vector(Point1.x,Point1.y,Point2.z),Point2)
            path=Part.Wire(line2)
            resultShape=path.makePipe(shapeCir)
            pass
    if resultShape!=None:
        return Part.makeSolid(resultShape)
    else:
        DocumentTools.printErrorMessage("getShapeOfComformal error!")
#------------------------------------------结束-----------------------------------------------#
########################################模型属性控制模块########################################
# 为物体增加非均匀网格属性
def addNonUniformGridAttribute(curCoordinateSys,obj):
    if curCoordinateSys==CoordinateSystemTools.CoordinateType.Rectangular:
        obj.addProperty("App::PropertyBool","X","NonUniformGrid","").X=True
        obj.addProperty("App::PropertyLength","X_Value","NonUniformGrid","").X_Value=0
        
        obj.addProperty("App::PropertyBool","Y","NonUniformGrid","").Y=True
        obj.addProperty("App::PropertyLength","Y_Value","NonUniformGrid","").Y_Value=0
            
        obj.setEditorMode('X_Value',0)
        obj.setEditorMode('Y_Value',0)

    elif curCoordinateSys==CoordinateSystemTools.CoordinateType.Polar or curCoordinateSys==CoordinateSystemTools.CoordinateType.Cylindrical:
        obj.addProperty("App::PropertyBool","R","NonUniformGrid","").R=True
        obj.addProperty("App::PropertyLength","R_Value","NonUniformGrid","").R_Value=0
        
        obj.addProperty("App::PropertyBool","Theta","NonUniformGrid","").Theta=True
        obj.addProperty("App::PropertyAngle","Theta_Value","NonUniformGrid","").Theta_Value=0
            
        obj.setEditorMode('R_Value',0)
        obj.setEditorMode('Theta_Value',0)

    obj.addProperty("App::PropertyBool","Z","NonUniformGrid","").Z=True
    obj.addProperty("App::PropertyLength","Z_Value","NonUniformGrid","").Z_Value=0        
    obj.setEditorMode('Z_Value',0)

    # 为mark补充新的属性 @lzg
    switch = False #开关，方便用于测试时切换默认状态，实际运行时候应该以False状态运行
    obj.addProperty("App::PropertyBool","min_1","NonUniformGrid","").min_1 = switch
    obj.addProperty("App::PropertyBool","mid_1","NonUniformGrid","").mid_1 = switch
    obj.addProperty("App::PropertyBool","max_1","NonUniformGrid","").max_1 = switch
    obj.addProperty("App::PropertyBool","min_2","NonUniformGrid","").min_2 = switch
    obj.addProperty("App::PropertyBool","mid_2","NonUniformGrid","").mid_2 = switch
    obj.addProperty("App::PropertyBool","max_2","NonUniformGrid","").max_2 = switch
    obj.addProperty("App::PropertyBool","min_3","NonUniformGrid","").min_3 = switch
    obj.addProperty("App::PropertyBool","mid_3","NonUniformGrid","").mid_3 = switch
    obj.addProperty("App::PropertyBool","max_3","NonUniformGrid","").max_3 = switch
    # 设置mark属性的默认状态 @lzg
    obj.setEditorMode('min_1',0)
    obj.setEditorMode('mid_1',0)
    obj.setEditorMode('max_1',0)
    obj.setEditorMode('min_2',0)
    obj.setEditorMode('mid_2',0)
    obj.setEditorMode('max_2',0)
    obj.setEditorMode('min_3',0)
    obj.setEditorMode('mid_3',0)
    obj.setEditorMode('max_3',0)


      # 将ParamObj的DX1,DX2,DX3加到这里
    paramObj=getParamObj()
    paramObjName=paramObj.Name
    if paramObj:
        if curCoordinateSys==CoordinateSystemTools.CoordinateType.Rectangular:
            if hasattr(paramObj,"DX1"):
                obj.setExpression("X_Value",paramObjName+".DX1")
            if hasattr(paramObj,"DX2"):
                obj.setExpression("Y_Value",paramObjName+".DX2")
            if hasattr(paramObj,"DX3"):
                obj.setExpression("Z_Value",paramObjName+".DX3")
        elif curCoordinateSys==CoordinateSystemTools.CoordinateType.Polar:
            if hasattr(paramObj,"DX1"):
                obj.setExpression("R_Value",paramObjName+".DX1")
            if hasattr(paramObj,"DX2"):
                obj.setExpression("Theta_Value",paramObjName+".DX2")
            if hasattr(paramObj,"DX3"):
                obj.setExpression("Z_Value",paramObjName+".DX3")     
        elif curCoordinateSys==CoordinateSystemTools.CoordinateType.Cylindrical:
            if hasattr(paramObj,"DX1"):
                obj.setExpression("Z_Value",paramObjName+".DX1")
            if hasattr(paramObj,"DX2"):
                obj.setExpression("R_Value",paramObjName+".DX2")
            if hasattr(paramObj,"DX3"):
                obj.setExpression("Theta_Value",paramObjName+".DX3") 

# 控制物体的属性代码更新
def fucUpdateProps(self):
    if self.flagShape:
        self.flagShape=False
        self.flagPlacement=False
        #将物体置为原点
        fp.Placement=FreeCAD.Placement(FreeCAD.Vector(0.0,0.0,0.0),FreeCAD.Rotation(0.0,0.0,0.0,1.0))
        self.vectorList=[fp.StartPoint,fp.EndPoint]
        self.flagShape=True
        self.flagPlacement=True
        self.flagExcute=True

# 为“体”增加统一的属性
def addPropertyForVol(obj,typeName,curCoordinateSystem):
    # obj.addProperty("App::PropertyBool", "ConductivitySIGMA", "Attribute", "Conformal of Object").ConductivitySIGMA=True
    obj.addProperty("App::PropertyFloat", "ConductivitySIGMAValue", "Attribute", "Conformal of Object").ConductivitySIGMAValue=0.05
    # 因为新的custom需求，对此处进行修改   前面虽然保留C_SIGMAValue但是不再使用这个变量！！@lizhanguang
    obj.addProperty("App::PropertyEnumeration", "ConductivitySIGMA", "Attribute", "Conformal of Object").ConductivitySIGMA=["Isotropy","Anisotropy","NotDefine"]
    obj.addProperty("App::PropertyFloat", "CS_SetEPS", "Attribute", "Conformal of Object").CS_SetEPS=0.05
    obj.addProperty("App::PropertyFloat", "CS_SetEPS2", "Attribute", "Conformal of Object").CS_SetEPS2=1
    obj.addProperty("App::PropertyFloat", "CS_SetEPS3", "Attribute", "Conformal of Object").CS_SetEPS3=1

    obj.addProperty("App::PropertyEnumeration", "RelativeDielectricConstant", "Attribute", "Conformal of Object").RelativeDielectricConstant=["Isotropy","Anisotropy","NotDefine"]
    obj.addProperty("App::PropertyFloat", "SetEPS", "Attribute", "Conformal of Object").SetEPS=0.05
    obj.addProperty("App::PropertyFloat", "SetEPS2", "Attribute", "Conformal of Object").SetEPS=1
    obj.addProperty("App::PropertyFloat", "SetEPS3", "Attribute", "Conformal of Object").SetEPS=1


    obj.addProperty("App::PropertyEnumeration", "Attribute", "Attribute", "Conformal of Object")
    obj.Attribute=[Attribute.NotDefine,Attribute.Conductor,Attribute.Custom,Attribute.Vacuo]
    obj.addProperty("App::PropertyString", "Type", "", "Type of Object").Type = typeName
    addNonUniformGridAttribute(curCoordinateSystem,obj)
    obj.setEditorMode('Type',2)
    obj.setEditorMode('ConductivitySIGMA',2)
    obj.setEditorMode('ConductivitySIGMAValue',2)
    obj.setEditorMode('RelativeDielectricConstant',2)
    obj.setEditorMode('SetEPS',2)
    obj.setEditorMode('SetEPS2',2)
    obj.setEditorMode('SetEPS3',2)
    # @lizhenguang
    obj.setEditorMode('CS_SetEPS',2)
    obj.setEditorMode('CS_SetEPS2',2)
    obj.setEditorMode('CS_SetEPS3',2)


# 控制非均匀网格属性面板的显示与隐藏
def fucNonUniformGrid(curCoordinateSystem,fp,prop):
    return
    if prop=="X" or prop=="Y" or prop=="Z" or prop=="R" or prop=="Theta" or prop=="X_Value" or prop=="Y_Value" or prop =="Z_Value" or prop=="R_Value" or prop=="Theta_Value":
        if curCoordinateSystem==CoordinateSystemTools.CoordinateType.Rectangular:
            if hasThePropertiesByObj(fp,["X","X_Value"]):
                if fp.X:
                    fp.setEditorMode('X_Value',0)
                else:
                    fp.setEditorMode('X_Value',2)
            if hasThePropertiesByObj(fp,["Y","Y_Value"]):
                if fp.Y:
                    fp.setEditorMode('Y_Value',0)
                else:
                    fp.setEditorMode('Y_Value',2)
            if hasThePropertiesByObj(fp,["Z","Z_Value"]):        
                if fp.Z:
                    fp.setEditorMode('Z_Value',0)
                else:
                    fp.setEditorMode('Z_Value',2)
                # fuc(fp,isX,isY,isZ,X,Y,Z)
                pass
        elif curCoordinateSystem==CoordinateSystemTools.CoordinateType.Polar or CoordinateSystemTools.CoordinateType.Cylindrical:
            if hasThePropertiesByObj(fp,["R","R_Value"]):
                if fp.R:
                    fp.setEditorMode('R_Value',0)
                else:
                    fp.setEditorMode('R_Value',2)
            if hasThePropertiesByObj(fp,["Theta","Theta_Value"]):
                if fp.Theta:
                    fp.setEditorMode('Theta_Value',0)
                else:
                    fp.setEditorMode('Theta_Value',2)
            if hasThePropertiesByObj(fp,["Z","Z_Value"]):     
                if fp.Z:
                    fp.setEditorMode('Z_Value',0)
                else:
                    fp.setEditorMode('Z_Value',2)
                # fuc(fp,isX,isY,isZ,X,Y,Z)
                pass
        else:
            pass

#打开自定义属性时
def customAttribute(fp):
    # if hasThePropertyByObj(fp,"ConductivitySIGMA"):
    #     fp.setEditorMode('ConductivitySIGMA',0)
    #     if hasThePropertyByObj(fp,"ConductivitySIGMAValue"):
    #         if fp.ConductivitySIGMA:
    #             fp.setEditorMode('ConductivitySIGMAValue',0)
    #         else:
    #             fp.setEditorMode('ConductivitySIGMAValue',1)

    if hasThePropertyByObj(fp,"ConductivitySIGMA"):
        fp.setEditorMode('ConductivitySIGMA',0)
        if fp.ConductivitySIGMA=="Isotropy":
            if hasThePropertyByObj(fp,'CS_SetEPS'):
                fp.setEditorMode('CS_SetEPS',0)
            if hasThePropertyByObj(fp,'CS_SetEPS2'):
                fp.setEditorMode('CS_SetEPS2',1)
            if hasThePropertyByObj(fp,'CS_SetEPS3'):
                fp.setEditorMode('CS_SetEPS3',1)
        elif fp.ConductivitySIGMA=="Anisotropy":
            if hasThePropertyByObj(fp,'CS_SetEPS'):
                fp.setEditorMode('CS_SetEPS',0)
            if hasThePropertyByObj(fp,'CS_SetEPS2'):
                fp.setEditorMode('CS_SetEPS2',0)
            if hasThePropertyByObj(fp,'CS_SetEPS3'):
                fp.setEditorMode('CS_SetEPS3',0)
        else:
            if hasThePropertyByObj(fp,'CS_SetEPS'):
                fp.setEditorMode('CS_SetEPS',1)
            if hasThePropertyByObj(fp,'CS_SetEPS2'):
                fp.setEditorMode('CS_SetEPS2',1)
            if hasThePropertyByObj(fp,'CS_SetEPS3'):
                fp.setEditorMode('CS_SetEPS3',1)

    if hasThePropertyByObj(fp,'SetEPS'):
        fp.setEditorMode('SetEPS',0)

    if hasThePropertyByObj(fp,'RelativeDielectricConstant'):
        fp.setEditorMode('RelativeDielectricConstant',0)
        if fp.RelativeDielectricConstant=="Isotropy":
            if hasThePropertyByObj(fp,'SetEPS2'):
                fp.setEditorMode('SetEPS2',1)
            if hasThePropertyByObj(fp,'SetEPS3'):
                fp.setEditorMode('SetEPS3',1)
        elif fp.RelativeDielectricConstant=="Anisotropy":
            if hasThePropertyByObj(fp,'SetEPS2'):
                fp.setEditorMode('SetEPS2',0)
            if hasThePropertyByObj(fp,'SetEPS3'):
                fp.setEditorMode('SetEPS3',0)
        elif fp.RelativeDielectricConstant=="NotDefine":
            if hasThePropertyByObj(fp,'SetEPS'):
                fp.setEditorMode('SetEPS',1)
            if hasThePropertyByObj(fp,'SetEPS2'):
                fp.setEditorMode('SetEPS2',1)
            if hasThePropertyByObj(fp,'SetEPS3'):
                fp.setEditorMode('SetEPS3',1)

#打开非自定义属性时
def notCustomAttribute(fp):
    # if hasThePropertyByObj(fp,"ConductivitySIGMA"):
    #     fp.setEditorMode('ConductivitySIGMA',2)
    #     if hasThePropertyByObj(fp,"ConductivitySIGMAValue"):
    #         if fp.ConductivitySIGMA:
    #             fp.setEditorMode('ConductivitySIGMAValue',2)
    #         else:
    #             fp.setEditorMode('ConductivitySIGMAValue',2)

    if hasThePropertyByObj(fp,"ConductivitySIGMA"):
        fp.setEditorMode('ConductivitySIGMA',2)
        if fp.ConductivitySIGMA=="Isotropy":
            if hasThePropertyByObj(fp,'CS_SetEPS'):
                fp.setEditorMode('CS_SetEPS',2)
            if hasThePropertyByObj(fp,'CS_SetEPS2'):
                fp.setEditorMode('CS_SetEPS2',2)
            if hasThePropertyByObj(fp,'CS_SetEPS3'):
                fp.setEditorMode('CS_SetEPS3',2)
        elif fp.ConductivitySIGMA=="Anisotropy":
            if hasThePropertyByObj(fp,'CS_SetEPS'):
                fp.setEditorMode('CS_SetEPS',2)
            if hasThePropertyByObj(fp,'CS_SetEPS2'):
                fp.setEditorMode('CS_SetEPS2',2)
            if hasThePropertyByObj(fp,'CS_SetEPS3'):
                fp.setEditorMode('CS_SetEPS3',2)
        else:
            if hasThePropertyByObj(fp,'CS_SetEPS'):
                fp.setEditorMode('CS_SetEPS',2)
            if hasThePropertyByObj(fp,'CS_SetEPS2'):
                fp.setEditorMode('CS_SetEPS2',2)
            if hasThePropertyByObj(fp,'CS_SetEPS3'):
                fp.setEditorMode('CS_SetEPS3',2)

    if hasThePropertyByObj(fp,'SetEPS'):
        fp.setEditorMode('SetEPS',2)

    if hasThePropertyByObj(fp,'RelativeDielectricConstant'):
        fp.setEditorMode('RelativeDielectricConstant',2)
        if fp.RelativeDielectricConstant=="Isotropy":
            if hasThePropertyByObj(fp,'SetEPS2'):
                fp.setEditorMode('SetEPS2',2)
            if hasThePropertyByObj(fp,'SetEPS3'):
                fp.setEditorMode('SetEPS3',2)
        elif fp.RelativeDielectricConstant=="Anisotropy":
            if hasThePropertyByObj(fp,'SetEPS2'):
                fp.setEditorMode('SetEPS2',2)
            if hasThePropertyByObj(fp,'SetEPS3'):
                fp.setEditorMode('SetEPS3',2)
        elif fp.RelativeDielectricConstant=="NotDefine":
            if hasThePropertyByObj(fp,'SetEPS'):
                fp.setEditorMode('SetEPS',2)
            if hasThePropertyByObj(fp,'SetEPS2'):
                fp.setEditorMode('SetEPS2',2)
            if hasThePropertyByObj(fp,'SetEPS3'):
                fp.setEditorMode('SetEPS3',2)
# 当物体的属性发生改变时：未定义、理想导体、自定义、真空
def fucAttributeChange(fp,prop):
    # if prop=="Attribute" or prop=="ConductivitySIGMA" or prop=="ConductivitySIGMAValue" or prop=="RelativeDielectricConstant" or prop=="SetEPS" or prop=="SetEPS2" or prop=="SetEPS3":
    if prop=="Attribute" or prop=="ConductivitySIGMA" or prop=="CS_SetEPS" or prop=="CS_SetEPS2" or prop=="CS_SetEPS3" or prop=="RelativeDielectricConstant" or prop=="SetEPS" or prop=="SetEPS2" or prop=="SetEPS3":
        if hasThePropertyByObj(fp,"Attribute"):
            if fp.Attribute==Attribute.NotDefine:
                # FreeCADGui.ActiveDocument.getObject(fp.Name).Transparency=90
                notCustomAttribute(fp)        
                # fp.Transparency=90
                pass
            elif fp.Attribute==Attribute.Conductor:
                # FreeCADGui.ActiveDocument.getObject(fp.Name).Transparency=0
                notCustomAttribute(fp)
                # OperationCommands.getConductorCommands(fp.Name)
                # fp.Transparency=0
                pass
            elif fp.Attribute==Attribute.Vacuo:
                # FreeCADGui.ActiveDocument.getObject(fp.Name).Transparency=95
                notCustomAttribute(fp)
                # OperationCommands.getVoidCommands(fp.Name)
                # fp.Transparency=90
                pass
            elif fp.Attribute==Attribute.Custom:
                customAttribute(fp)

                pass

# 获得一个obj列表中，某一个索引下最近前后导体的索引
def getIndexOfUpAndButtomConductors(listOfObj,index):
    upIndex=-1
    buttomIndex=len(listOfObj)
    for i in range(len(listOfObj)):
        if hasattr(listOfObj[i],"Type"):
            if listOfObj[i].Type==Attribute.Custom or listOfObj[i].Type==Attribute.Conductor:
                if i<index:
                    upIndex=i
                elif i>index:
                    buttomIndex=i
                    break
    return upIndex,buttomIndex
def fucPointsChange():
    pass
def getAttributeValue(fp):
    isConductor=False
    isVoid=True
    # results=[isConductor,isVoid]
    if fp.Attribute==Attribute.NotDefine:
        pass
    elif fp.Attribute==Attribute.Conductor:
        isConductor=True
        isVoid=False
        pass
    elif fp.Attribute==Attribute.Vacuo:
        isVoid=True
        isConductor=False
        pass
    elif fp.Attribute==Attribute.Custom:
        pass
    results=[isConductor,isVoid]
    return results

def getParamValueOfObj(obj,PropStr,UnitType):
    '''
    @ brief 获得obj对应属性的值，如果是参数优先获得参数
            例如 objItem,"Point1.x"->
    '''
    expressionList=obj.ExpressionEngine
    for item in expressionList:
        if item[0]==PropStr:
            paramObj=getParamObj()
            valueStr=item[1].replace(paramObj.Name+".","")
            return valueStr
    # 表达式编辑器里没有找到
    props=PropStr.split(".")
    # try:
    if len(props)==1:
        value= getattr(obj,props[0])
        valueWithUnit=UnitTools.turnNormalUnitToShowUnit(UnitType,value)
        return valueWithUnit
    elif len(props)>=2:
        value= getattr(getattr(obj,props[0]),props[1])
        valueWithUnit=UnitTools.turnNormalUnitToShowUnit(UnitType,value)
        return valueWithUnit
    # except:
    #     FreeCAD.Console.PrintError(str(obj.Name)+" doesn't have property "+str(PropStr)+"\n")
    
#------------------------------------------结束-------------------------------------------#

##############################不知道什么东西可能没有用，暂时留着##############################
# 返回带单位的点坐标
def getUnitPoint(obj,point):
    curCoordinateSys=obj.Document.CoordinateSystem
    resultPoint=[]
    x1="0mm"
    x2="0mm"
    x3="0mm"

    if curCoordinateSys==CoordinateSystemTools.CoordinateType.Rectangular:
        x1=str(point.x)+"mm"
        x2=str(point.y)+"mm"
        x3=str(point.z)+"mm"
    elif  curCoordinateSys==CoordinateSystemTools.CoordinateType.Polar or CoordinateSystemTools.CoordinateType.Cylindrical:
        x1=str(point.x)+"mm"
        x2=str(point.y)+"deg"
        x3=str(point.z)+"mm"
    else:
        pass
    resultPoint=[x1,x2,x3]
    return resultPoint
#------------------------------------------结束-------------------------------------------#

#######################################Vol_Extruded相关函数################################
def getAllObjectsByType(docName,myType):
    '''
    docName: 当前的文档名
    type:    类型：ObjectType
    return:  list
    '''
    resultObjs=[]
    objs=getAllObjectszofThisDoc(docName)
    for objItem in objs:
        if hasThePropertyByObj(objItem,"Type"):
            if objItem.Type==myType:
                resultObjs.append(objItem)
    return resultObjs
def getAllObjectsByTypes(docName,findTypes):
    '''
    docName: 当前文件名
    findTypes: 需要寻找的类型列表
    return list of objs
    '''
    resultObjs=[]
    objs=getAllObjectszofThisDoc(docName)
    for objItem in objs:
        if hasThePropertyByObj(objItem,"Type"):
            if objItem.Type in findTypes:
                resultObjs.append(objItem)
    return resultObjs

# 返回文档中所有的线
def getLinesByDoc(doc):
    '''
    doc:    文档对象
    return：list
    '''
    resultLines=[]
    objs=getAllObjectszofThisDoc(doc.Name)
    for objItem in objs:
        if hasThePropertyByObj(objItem,"Type"):
            if objItem.Type[0]=="L":
                resultLines.append(str(objItem.Label))
    return resultLines

    # 返回文档中所有的面
def getAreasByDoc(doc):
    '''
    doc:    文档对象
    return：list
    '''
    resultLines=[]
    objs=getAllObjectszofThisDoc(doc.Name)
    for objItem in objs:
        if hasThePropertyByObj(objItem,"Type"):
            if objItem.Type[0:3]=="Are":
                resultLines.append(str(objItem.Label))
    return resultLines
#------------------------------------------结束-------------------------------------------#
######################################螺旋体使用的一些函数###################################
#某个向量映射到XOY面与x轴正方向之间的夹角 0-pi
def getAngleWithXByVector(vec):
    vecXDir=FreeCAD.Vector(1,0,0)
    #先将vec映射到XOY面上
    vecXOY=FreeCAD.Vector(vec.x,vec.y,0)
    if vecXOY.Length==0.0:
        return 0.0
    else:
        angle=math.acos((vecXDir.dot(vecXOY))/(vecXDir.Length*vecXOY.Length))*180/math.pi
        if vecXOY.y<0:
            angle=360-angle
        return angle

#某个向量与z轴正方向之间的夹角 0-pi
def getAngleWithZByVector(vec2):
    vecZDir=FreeCAD.Vector(0,0,1)
    angle=math.acos(vec2.dot(vecZDir)/vec2.Length*vecZDir.Length)*180/math.pi
    if vec2.y<0:
        angle=360-angle
    return angle

#将某个向量旋转到Z轴方向上后的四元数
def getQuatAfterRotation(vec):
    dirVec=FreeCAD.Vector(0,0,1)
    #判断vec是否已在Z轴上
    if vec.x==0 and vec.y==0:
        return FreeCAD.Rotation(0,0,0,1)
    else:
        #先通过叉乘求得旋转轴
        axis=vec.cross(dirVec)
        axis.normalize()
        #求出旋转角度
        angle=getAngleWithZByVector(vec)
        #得出四元数
        rot=FreeCAD.Rotation(axis,angle)
        return rot
#------------------------------------------结束-------------------------------------------#

###############################根据步骤顺序进行Boolean运算###################################
# def getDocNameOfThisObject(obj):
#     docName=obj.Document.Name
#     return docName
class BooleanInstance:
    curIndex=-1
    @staticmethod
    def getLastRecomputeBooleanIndex():
        return curIndex
    @staticmethod
    def setLastRecomputeBooleanIndex(index):
        curIndex=index


#初始化结果对象
def initResultIbj(doc):
    '''
    doc:    新建模型所在文档
    return：obj
    '''
    obj=doc.getObject("ResultShape")
    if not obj:
        obj=doc.addObject("Part::FeaturePython", "ResultShape")
    obj.addProperty("Part::PropertyShapeHistory","History","","")
    obj.ViewObject.Proxy=0
    # obj.Shape=Part.makeSphere(0.00001)
    Gui.getDocument(doc.Name).getObject(obj.Name).DisplayMode=u"Shaded"
    # Gui.getDocument(doc.Name).getObject(obj.Name).Transparency=100
    # Gui.getDocument(doc.Name).getObject(obj.Name).Selectable = False
    # Gui.ActiveDocument.getObject(obj.Name).Visibility = False
    doc.recompute()

    obj.setEditorMode('Placement',2) 

    # obj1=doc.getObject("t1")
    # if not obj1:
    #     obj1=doc.addObject("Part::FeaturePython", "t1")
    # obj1.addProperty("Part::PropertyShapeHistory","History","","")
    # obj1.ViewObject.Proxy=0
    # obj1.Shape=obj.Shape

    # obj2=doc.getObject("t2")
    # if not obj2:
    #     obj2=doc.addObject("Part::FeaturePython", "t2")
    # obj2.addProperty("Part::PropertyShapeHistory","History","","")
    # obj2.ViewObject.Proxy=0
    # obj2.Shape=obj.Shape
    # # 
    # obj3=doc.getObject("t")
    # if not obj3:
    #     obj3=doc.addObject("Part::FeaturePython", "t")
    # obj3.addProperty("Part::PropertyShapeHistory","History","","")
    # obj3.ViewObject.Proxy=0
    # # obj3.Shape=obj.Shape

    # obj4=doc.getObject("tt")
    # if not obj4:
    #     obj4=doc.addObject("Part::FeaturePython", "tt")
    # obj4.addProperty("Part::PropertyShapeHistory","History","","")
    # obj4.ViewObject.Proxy=0

    # t3=doc.getObject("t3")
    # if not t3:
    #     t3=doc.addObject("Part::FeaturePython", "t3")
    # t3.addProperty("Part::PropertyShapeHistory","History","","")
    # t3.ViewObject.Proxy=0

    # t4=doc.getObject("t4")
    # if not t4:
    #     t4=doc.addObject("Part::FeaturePython", "t4")
    # t4.addProperty("Part::PropertyShapeHistory","History","","")
    # t4.ViewObject.Proxy=0

    doc.recompute()
    # FreeCADGui.ActiveDocument.getObject("ResultShape").Transparency = 95
    return obj   

#为文档新建一个空对象，最为最终结果
def createResultObj(doc):
    '''
    doc:    新建模型所在文档
    return：null
    '''
    obj=doc.addObject("Part::FeaturePython", "ResultShape")
    obj.ViewObject.Proxy=0
    obj.Shape=Part.makeSphere(0.01)
    Gui.getDocument(doc.Name).getObject(obj.Name).DisplayMode=u"Shaded"
    doc.recompute()
    obj.setEditorMode('Placement',2)


#获取当前文档中的所有模型列表
def getAllObjectszofThisDoc(docName):
    '''
    docName: String 文档的Name
    return: List[]
    '''
    curDocument=FreeCAD.getDocument(docName)
    featurePythonList=curDocument.findObjects('Part::FeaturePython')
    customFeaturePythonList=curDocument.findObjects('Part::CustomFeaturePython')
    objectList=featurePythonList+customFeaturePythonList
    tempList=[]
    # 剔除没有Type属性的物体
    for objItem in objectList:
        if hasThePropertyByObj(objItem,"Type") and hasThePropertyByObj(objItem,"Order"):
            tempList.append(objItem)
    # objectList=tempList
    return tempList

def getAllObjectszofThisDocWithoutOrder(docName):
    '''
    作用返回去掉order的模型Label列表
    docName:    文档名称
    return :    list[],按order排序的去掉Order显示的Label
    '''
    objs=getListOfOrderedObjects(docName)
    tempList=[]
    for objItem in objs:
        labelWithoutOrder=DocumentTools.removeOrderFromLabel(objItem.Label)
        tempList.append(labelWithoutOrder)
    return tempList

#按顺序获取当前模型的列表
def getListOfOrderedObjects(docName):
    '''
    docName: String 文档的Name
    return: List[]
    '''
    curListOfObjects=getAllObjectszofThisDoc(docName)
    #冒泡排序
    count=len(curListOfObjects)
    for i in range(0,count):
        for j in range(i+1,count):
            if hasThePropertyByObj(curListOfObjects[i],"Order"):
                if  curListOfObjects[i].Order>curListOfObjects[j].Order:
                    curListOfObjects[i],curListOfObjects[j]=curListOfObjects[j],curListOfObjects[i]
    return curListOfObjects
    pass
#获取当前文档中的自建的模型个数（顺序）
def getNumOfObjects(docName):
    '''
    docname:当前的文档名称
    return :int
    '''
    curListOfObjects=getAllObjectszofThisDoc(docName)
    # print curListOfObjects
    return len(curListOfObjects)
    pass
#将object的Label名进行拆分，将顺序和后缀分开
def getRealNameBySplitObjectLabel(obj):
    '''
    obj:    进行拆分的对象
    return：去掉顺序的对象名
    '''
    labelWithoutOrder=obj.Label
    if re.match(r"\[[0-9]\d*\]\_",str(labelWithoutOrder)):
        labelWithoutOrder=str(re.split(r"\[[0-9]\d*\]\_",str(labelWithoutOrder))[1])
    return labelWithoutOrder
    # strList=obj.Label.split("_")
    # realName=""
    # if len(strList)==0:
    #     realName=obj.Label
    #     # #异常
    #     # FreeCAD.Console.PrintError("ObjectTools中 ,strList为空\n")
    # elif len(strList)==1:
    #     realName="_"+obj.Label
    # else:
    #     for i in range(1,len(strList)):
    #         realName="_"+realName+strList[i]
    # return realName
# 判断模型名称去掉顺序后的字符串是否相等，若相等则加后缀
def checkLabelNameRepeat(labelWithoutOrder):
    '''
    labelWithoutOrder:    输入的欲检查的名称
    return：              返回检查之后的名称
    note: 2019/10/30对这里进行了更新（复制粘贴操作后label命名），后面如果有问题可回退版本
    '''
    objsLabelNameWithoutOrder=getAllObjectszofThisDocWithoutOrder(FreeCAD.ActiveDocument.Name)
    if  (objsLabelNameWithoutOrder.count(labelWithoutOrder)==1 and not None in objsLabelNameWithoutOrder) or  objsLabelNameWithoutOrder.count(labelWithoutOrder)==0:
        return labelWithoutOrder
    # suffixNum=0
    labelWithoutSuffixNum=""
    # suffix=re.findall(r"\B\d+",labelWithoutOrder)
    if len(labelWithoutOrder)<3:
        labelWithoutSuffixNum=labelWithoutOrder
        FreeCAD.Console.PrintMessage("labelWithoutSuffixNum 1:"+str(labelWithoutSuffixNum)+'\n')
    else:
        if labelWithoutOrder[len(labelWithoutOrder)-3:len(labelWithoutOrder)].isdigit():
            labelWithoutSuffixNum=labelWithoutOrder[:-3]
            FreeCAD.Console.PrintMessage("labelWithoutSuffixNum 2:"+str(labelWithoutSuffixNum)+'\n')
        else:
            labelWithoutSuffixNum=labelWithoutOrder
            FreeCAD.Console.PrintMessage("labelWithoutSuffixNum 3:"+str(labelWithoutSuffixNum)+'\n')

    objsLabelWithOrderAndSuffixnum=[]
    for objLabelItem in objsLabelNameWithoutOrder:
        if objLabelItem==None:
            objsLabelWithOrderAndSuffixnum.append(objLabelItem)
            continue
        # FreeCAD.Console.PrintMessage("objLabelItem: "+str(objLabelItem)+"\n")
        if len(labelWithoutOrder)<=3:
            objsLabelWithOrderAndSuffixnum.append(objLabelItem)
        else:
            suffix=objLabelItem[len(labelWithoutOrder)-3:len(labelWithoutOrder)]
            if suffix.isdigit():
                objsLabelWithOrderAndSuffixnum.append(labelWithoutOrder[:-3])
            else:
                objsLabelWithOrderAndSuffixnum.append(objLabelItem)

    suffixNum=objsLabelWithOrderAndSuffixnum.count(labelWithoutSuffixNum)+objsLabelWithOrderAndSuffixnum.count(None)
    # o.Label="Volume",用次赋值命令时objsLabelWithOrderAndSuffixnum中会有None，暂时考虑不会出现两个None的情况
    if suffixNum>1:
        result=labelWithoutSuffixNum+str(suffixNum-1).zfill(3)
        return result
    else:
        return labelWithoutSuffixNum 

    # if None in objsLabelNameWithoutOrder:
    #     FreeCAD.Console.PrintMessage("checkLabelNameRepeat 1\n")
    #     while objsLabelNameWithoutOrder.count(labelWithoutOrder)==1:
    #         labelWithoutOrder=labelWithoutSuffixNum+str(suffixNum).zfill(3)
    #         suffixNum=suffixNum+1
    # else:
    #     FreeCAD.Console.PrintMessage("checkLabelNameRepeat 2\n")
    #     while objsLabelNameWithoutOrder.count(labelWithoutOrder)>1:
    #         FreeCAD.Console.PrintMessage("suffixNum: "+str(suffixNum)+"\n")
    #         FreeCAD.Console.PrintMessage("labelWithoutSuffixNum: "+str(labelWithoutSuffixNum)+"\n")
    #         labelWithoutOrder=labelWithoutSuffixNum+str(suffixNum).zfill(3)
    #         suffixNum=suffixNum+1
    # FreeCAD.Console.PrintMessage("labelWithoutOrder: "+str(labelWithoutOrder)+"\n")
    # return labelWithoutOrder

#设置物体初始化时候的顺序
def setInitOrderForObject(obj):
    '''
    obj:    物体对象
    return :None
    '''
    docName=obj.Document.Name
    curNumOfObjects=getNumOfObjects(docName)
    obj.Order=curNumOfObjects-1
    pass
def updateWhenOrderChanged(obj,lastOrder,newOrder):
    docName=obj.Document.Name
    orderedObjects=getListOfOrderedObjects(docName)
    curNumOfObjects=getNumOfObjects(docName)
    #因为从0开始计数，所以此处获取最后一个的顺序为数量－1
    lastNumOfObject=curNumOfObjects-1

    # FreeCAD.Console.PrintMessage
    # obj.Label="[0]_Test"
    #没有变化
    if lastOrder==newOrder:
        return
    #处理为负值
    elif newOrder<0:
        obj.Order=lastOrder
        return
        pass
    elif newOrder>lastNumOfObject:
        #交换当前这个和最后一个的顺序
        obj.Order=lastNumOfObject
        obj.Label="["+str(lastNumOfObject)+"]_"+getRealNameBySplitObjectLabel(obj)
        for objItem in orderedObjects:
            if objItem.Order==lastNumOfObject and not objItem==obj:
                objItem.Order=lastOrder
                objItem.Label="["+str(lastOrder)+"]_"+getRealNameBySplitObjectLabel(objItem)
        return
    else:
        # spilestr=getRealNameBySplitObjectLabel(obj)
        obj.Label="["+str(newOrder)+"]_"+getRealNameBySplitObjectLabel(obj)
        #找到与之交换的另外一个物体
        for objItem in orderedObjects:
            if objItem.Order==newOrder and not objItem==obj:
                objItem.Order=lastOrder
                objItem.Label="["+str(lastOrder)+"]_"+getRealNameBySplitObjectLabel(objItem)
                return
        pass
    pass
def updateWhenLableChanged(obj,lastLabel,newLabel):
    '''
    obj:      发生改变的物体
    lastLable:更新前的物体Label
    newLable: 更新后的物体Label
    '''
    if hasThePropertyByObj(obj,"Order"):
        if len(newLabel)>=4:
            # 正则表达式匹配是否存在[...]_
            if re.match(r"\[[0-9]\d*\]\_",str(newLabel)):
                #改变obj的order,split[0]=""
                # obj.Label="Test"
                # obj.Label="[0]_test"
                # FreeCAD.Console.PrintError(getRealNameBySplitObjectLabel(obj))
                
                obj.Order=int(re.split(r"\[|\]",str(newLabel))[1])
                labelWithoutOrder=getRealNameBySplitObjectLabel(obj)
                # FreeCAD.Console.PrintError("labelWithoutOrder: "+str(labelWithoutOrder)+"\n")
                obj.Label="["+str(obj.Order)+"]_"+checkLabelNameRepeat(labelWithoutOrder)
                # FreeCAD.Console.PrintError("obj.Label: "+str(obj.Label)+"\n")
                # obj.Label="["+str(obj.Order)+"]_"+labelWithoutOrder
                return 
                pass
        # obj.Label="[0]_test"
        obj.Label="["+str(obj.Order)+"]"+"_"+checkLabelNameRepeat(newLabel)
        # obj.Label="["+str(obj.Order)+"]"+"_"+newLabel
        pass
#布尔加
def booleanAdd(baseObj,toolObj,flagNeedRedraw=1):
    doc=FreeCAD.ActiveDocument
    # 如果flagNeedRedraw==2说明上次使用的是reComputeBooleanBySubVacuo函数，需要将模型刷新一下
    if flagNeedRedraw==2:
        if hasattr(baseObj,"flagRedraw"):
            setattr(baseObj,"flagRedraw",not getattr(baseObj,"flagRedraw"))
            # baseObj.recompute()
        if hasattr(toolObj,"flagRedraw"):
            setattr(toolObj,"flagRedraw",not getattr(toolObj,"flagRedraw"))
            # toolObj.recompute()
        doc.recompute()
    #分别复制两个对象，因为不能直接拿场景中的对象直接布尔
    # tempBaseObj=doc.copyObject(baseObj,True)
    tempBaseObj=doc.addObject("Part::FeaturePython", "tempBaseObj")
    tempBaseObj.ViewObject.Proxy=0
    tempBaseObj.Shape=baseObj.Shape
    Gui.ActiveDocument.getObject(tempBaseObj.Name).Transparency=Gui.ActiveDocument.getObject(baseObj.Name).Transparency
    tempBaseObj.ViewObject.DiffuseColor=baseObj.ViewObject.DiffuseColor
    doc.recompute()
    
    fusion=doc.addObject("Part::MultiFuse","Fusion")
    fusion.Shapes=[tempBaseObj,toolObj,]
    doc.recompute()
    baseObj.Shape=fusion.Shape
    baseObj.ViewObject.DiffuseColor=fusion.ViewObject.DiffuseColor
    doc.recompute()
    doc.removeObject(fusion.Name)
    doc.removeObject(tempBaseObj.Name)
    doc.recompute()
    return baseObj


def booleanSub(baseObj,toolObj,flagNeedRedraw=1):
    doc=FreeCAD.ActiveDocument
    # 如果flagNeedRedraw==2说明上次使用的是reComputeBooleanBySubVacuo函数，需要将模型刷新一下
    if flagNeedRedraw==2:
        if hasattr(baseObj,"flagRedraw"):
            setattr(baseObj,"flagRedraw",not getattr(baseObj,"flagRedraw"))
            # baseObj.recompute()
        if hasattr(toolObj,"flagRedraw"):
            setattr(toolObj,"flagRedraw",not getattr(toolObj,"flagRedraw"))
            # toolObj.recompute()
        FreeCAD.Console.PrintMessage("booleanSub: "+str(flagNeedRedraw)+"\n")
        doc.recompute()
    #分别复制两个对象，因为不能直接拿场景中的对象直接布尔
    # tempBaseObj=doc.copyObject(baseObj,True)
    tempBaseObj=doc.addObject("Part::FeaturePython", "tempBaseObj")
    tempBaseObj.ViewObject.Proxy=0
    tempBaseObj.Shape=baseObj.Shape
    Gui.ActiveDocument.getObject(tempBaseObj.Name).Transparency=Gui.ActiveDocument.getObject(baseObj.Name).Transparency
    tempBaseObj.ViewObject.DiffuseColor=baseObj.ViewObject.DiffuseColor
    doc.recompute()

    cut=doc.addObject("Part::Cut","Cut")
    cut.Base=tempBaseObj
    cut.Tool=toolObj
    cut.ViewObject.DiffuseColor=tempBaseObj.ViewObject.DiffuseColor
    doc.recompute()
    # cut.Tool=tempToolObj
    baseObj.Shape=cut.Shape
    baseObj.ViewObject.DiffuseColor=cut.ViewObject.DiffuseColor
    doc.recompute()
    # doc.removeObject(cut.Name)
    # doc.removeObject(tempBaseObj.Name)
    doc.recompute()
# 将所有真空体做布尔和，然后将结果赋值给ResultShape
def addAllVacuo(vacuoList,resultObj):
    doc=FreeCAD.ActiveDocument
    if len(vacuoList)==1:
        resultObj.Shape=vacuoList[0].Shape
        resultObj.ViewObject.DiffuseColor=vacuoList[0].ViewObject.DiffuseColor
        doc.recompute()
        FreeCAD.Console.PrintMessage("addAllVacuo: "+str(vacuoList[0].Name))
        # doc.removeObject(vacuoList[0].Name)
        Gui.ActiveDocument.getObject(vacuoList[0].Name).Visibility = False
        doc.recompute()
        pass
    elif len(vacuoList)==0:
        return
    else:
        fusion=doc.addObject("Part::MultiFuse","Fusion")
        fusion.Shapes = vacuoList
        doc.recompute()
        resultObj.Shape=fusion.Shape
        resultObj.ViewObject.DiffuseColor=fusion.ViewObject.DiffuseColor
        doc.recompute()
        # doc.removeObject(fusion.Name)
        doc.recompute()
    Gui.ActiveDocument.getObject(resultObj.Name).Visibility = False
    return resultObj

#做真空布尔运算操作
def reComputeBooleanForAllObjs(flagLastDoWhichCommand=1):
    import datetime
    startTime=datetime.datetime.now()
    doc=FreeCAD.ActiveDocument
    docNmae=FreeCAD.ActiveDocument.Name
    orderedList=getListOfOrderedObjects(docNmae)
    if len(orderedList)==0:
        return
    # 定义第一个非空导体
    firstNotVacuoObj=orderedList[len(orderedList)-1]
    #定义是否找到第一个非空导体
    isFindTheFirstVacuoObj=False
    #找到场景中中的结果Shape
    # resultShape=FreeCAD.ActiveDocument.getObject("ResultShape")
    # if not resultShape:
    #     createResultObj(doc)
    resultShape=initResultIbj(doc)
    # resultShape.Shape=Part.makeSphere(0.01)
    # 进度条
    progress_bar=FreeCAD.Base.ProgressIndicator()
    progress_bar.start("Do boolean command...",len(orderedList))
    for i in range(0,len(orderedList)):
        if hasThePropertyByObj(orderedList[i],"Attribute"):
            if orderedList[i].Attribute==Attribute.Conductor or orderedList[i].Attribute==Attribute.Custom :
                booleanAdd(resultShape,orderedList[i],flagNeedRedraw=flagLastDoWhichCommand)
                pass
            elif orderedList[i].Attribute==Attribute.Vacuo:
                booleanSub(resultShape,orderedList[i],flagNeedRedraw=flagLastDoWhichCommand)
                pass
            elif orderedList[i].Attribute==Attribute.NotDefine:
                Gui.getDocument(docNmae).getObject(orderedList[i].Name).Visibility=True
                # Gui.getDocument(docNmae).getObject(orderedList[i].Name).Transparency=95
        else:
            Gui.getDocument(docNmae).getObject(orderedList[i].Name).Transparency=95
        # 进度加一
        progress_bar.next()
    progress_bar.stop()
    Gui.ActiveDocument.getObject(resultShape.Name).Visibility=True
    BooleanInstance.setLastRecomputeBooleanIndex(len(orderedList)-1)
    endTime=datetime.datetime.now()
    FreeCAD.Console.PrintMessage("recompute 2 time :"+str((endTime-startTime).seconds)+"\n")

def reComputeBooleanForPartObjs():
    doc=FreeCAD.ActiveDocument
    docNmae=FreeCAD.ActiveDocument.Name
    orderedList=getListOfOrderedObjects(docNmae)
    if len(orderedList)==0:
        return
    # 定义第一个非空导体
    firstNotVacuoObj=orderedList[len(orderedList)-1]
    #定义是否找到第一个非空导体
    isFindTheFirstVacuoObj=False
    #找到场景中中的结果Shape
    # resultShape=FreeCAD.ActiveDocument.getObject("ResultShape")
    # if not resultShape:
    resultShape=initResultIbj(doc)
    #判断BooleanInstance是否在范围内
    if BooleanInstance.getLastRecomputeBooleanIndex()>=0 and BooleanInstance.getLastRecomputeBooleanIndex()<=(len(orderedList)-1):
        for i in range(BooleanInstance.getLastRecomputeBooleanIndex(),len(orderedList)):
            if hasThePropertyByObj(orderedList[i],"Attribute"):
                if orderedList[i].Attribute==Attribute.Conductor or orderedList[i].Attribute==Attribute.Custom :
                    booleanAdd(resultShape,orderedList[i])
                    pass
                elif orderedList[i].Attribute==Attribute.Vacuo:
                    booleanSub(resultShape,orderedList[i])
                    pass
                elif orderedList[i].Attribute==Attribute.NotDefine:
                    Gui.getDocument(docNmae).getObject(orderedList[i].Name).Visibility=True
                    # Gui.getDocument(docNmae).getObject(orderedList[i].Name).Transparency=95
    else:
        reComputeBooleanForAllObjs()
    # FreeCADGui.ActiveDocument.getObject(resultShape.Name).Transparency = 95
    BooleanInstance.setLastRecomputeBooleanIndex(len(orderedList)-1)

def reComputeBooleanBySubVacuo(flagLastDoWhichCommand=1):
    FreeCAD.Console.PrintError("Run\n")
    # if flagNeedsRecompute:
    #     FreeCAD.Console.PrintError("Yes\n")
    # else:
    #     FreeCAD.Console.PrintError("No\n")

        
    import datetime
    startTime=datetime.datetime.now()
    doc=FreeCAD.ActiveDocument
    docNmae=FreeCAD.ActiveDocument.Name
    orderedList=getListOfOrderedObjects(docNmae)
    listConductorOrCustom=[]
    listVacuo=[]

    resultShape=initResultIbj(doc)
    # resultShape.Shape=Part.makeSphere(0.01)
    # 进度条
    progress_bar=FreeCAD.Base.ProgressIndicator()
    progress_bar.start("Do boolean command...",len(orderedList))
    for i in range(0,len(orderedList)):
        if hasThePropertyByObj(orderedList[i],"Attribute"):
            # 若上一次执行的是reComputeBooleanBySubVacuo函数，则现在需要将它们刷新一下
            if flagLastDoWhichCommand==2:
                setattr(orderedList[i],"flagRedraw",not getattr(orderedList[i],"flagRedraw"))
                FreeCAD.Console.PrintMessage("flagLastDoWhichCommand: "+str(flagLastDoWhichCommand)+"\n")
                doc.recompute()
            if orderedList[i].Attribute==Attribute.Conductor or orderedList[i].Attribute==Attribute.Custom :
                Gui.ActiveDocument.getObject(orderedList[i].Name).Visibility=True
                listConductorOrCustom.append(orderedList[i])
                pass
            elif orderedList[i].Attribute==Attribute.Vacuo:
                listVacuo.append(orderedList[i])
                pass               
                # doc.recompute()
                # if flagLastDoWhichCommand==2:
                #     setattr(orderedList[i],"flagRedraw",not getattr(orderedList[i],"flagRedraw"))
                #     FreeCAD.Console.PrintMessage("flagLastDoWhichCommand: "+str(flagLastDoWhichCommand)+"\n")
                #     doc.recompute()
            elif orderedList[i].Attribute==Attribute.NotDefine:
                Gui.getDocument(docNmae).getObject(orderedList[i].Name).Visibility=True
                # Gui.getDocument(docNmae).getObject(orderedList[i].Name).Transparency=95
        else:
            Gui.getDocument(docNmae).getObject(orderedList[i].Name).Transparency=95
        # 进度加一
        progress_bar.next()
    progress_bar.stop()
    # FreeCAD.Console.PrintMessage(listConductorOrCustom[0].Name)
    # FreeCAD.Console.PrintMessage("name\n")
    # FreeCAD.Console.PrintMessage(listVacuo[0].Name)

    # 将所有的真空布尔加
    addAllVacuo(listVacuo,resultShape)
    # 遍历所有的实体，实体=实体-真空集合
    for objItem in listConductorOrCustom:
        booleanSub(objItem,resultShape,flagLastDoWhichCommand)
    endTime=datetime.datetime.now()
    FreeCAD.Console.PrintMessage("recompute 2 time :"+str((endTime-startTime).seconds)+"\n")

def recumputeBooleanPartObjs(orderedList,startIndex,endIndex,flagLastDoWhichCommand=2):
    if startIndex>=endIndex:
        return
    else:
        doc=FreeCAD.ActiveDocument
        docNmae=FreeCAD.ActiveDocument.Name
        # orderedList=getListOfOrderedObjects(docNmae)
        listConductorOrCustom=[]
        listVacuo=[]

        resultShape=initResultIbj(doc)
        # resultShape.Shape=Part.makeSphere(0.01)
        # 进度条
        progress_bar=FreeCAD.Base.ProgressIndicator()
        progress_bar.start("Do boolean command...",len(orderedList))
        for i in range(startIndex,endIndex):
            if hasThePropertyByObj(orderedList[i],"Attribute"):
                # 若上一次执行的是reComputeBooleanBySubVacuo函数，则现在需要将它们刷新一下
                if flagLastDoWhichCommand==2:
                    setattr(orderedList[i],"flagRedraw",not getattr(orderedList[i],"flagRedraw"))
                    FreeCAD.Console.PrintMessage("flagLastDoWhichCommand: "+str(flagLastDoWhichCommand)+"\n")
                    doc.recompute()
                if orderedList[i].Attribute==Attribute.Conductor or orderedList[i].Attribute==Attribute.Custom :
                    if listVacuo!=[]:
                        # 将所有的真空布尔加
                        addAllVacuo(listVacuo,resultShape)
                        booleanSub(orderedList[i],resultShape,flagLastDoWhichCommand)
                        listVacuo=[]
                    Gui.ActiveDocument.getObject(orderedList[i].Name).Visibility=True
                    listConductorOrCustom.append(orderedList[i])
                    pass
                elif orderedList[i].Attribute==Attribute.Vacuo:
                    listVacuo.append(orderedList[i])
                    pass               
                    # doc.recompute()
                    # if flagLastDoWhichCommand==2:
                    #     setattr(orderedList[i],"flagRedraw",not getattr(orderedList[i],"flagRedraw"))
                    #     FreeCAD.Console.PrintMessage("flagLastDoWhichCommand: "+str(flagLastDoWhichCommand)+"\n")
                    #     doc.recompute()
                elif orderedList[i].Attribute==Attribute.NotDefine:
                    Gui.getDocument(docNmae).getObject(orderedList[i].Name).Visibility=True
                    # Gui.getDocument(docNmae).getObject(orderedList[i].Name).Transparency=95
            else:
                Gui.getDocument(docNmae).getObject(orderedList[i].Name).Transparency=95
            # 进度加一
            progress_bar.next()
        progress_bar.stop()
        # FreeCAD.Console.PrintMessage(listConductorOrCustom[0].Name)
        # FreeCAD.Console.PrintMessage("name\n")
        # FreeCAD.Console.PrintMessage(listVacuo[0].Name)
        for objItem in listVacuo:
            Gui.ActiveDocument.getObject(orderedList[i].Name).Visibility=False
        # # 将所有的真空布尔加
        # addAllVacuo(listVacuo,resultShape)
        # # 遍历所有的实体，实体=实体-真空集合
        # for objItem in listConductorOrCustom:
        #     booleanSub(objItem,resultShape,flagLastDoWhichCommand)
        endTime=datetime.datetime.now()
        FreeCAD.Console.PrintMessage("recompute 2 time :"+str((endTime-startTime).seconds)+"\n")

def autoRecompute():
    doc=FreeCAD.ActiveDocument
    docNmae=FreeCAD.ActiveDocument.Name
    orderedList=getListOfOrderedObjects(docNmae)
    listConductorOrCustom=[]
    listVacuo=[]
    lastConductorObj=None
    listOfObjAfterBoolean=[]
    for i in range(0,len(orderedList)):
        if hasThePropertyByObj(orderedList[i],"Attribute"):
            if orderedList[i].Attribute==Attribute.Conductor or orderedList[i].Attribute==Attribute.Custom :
                if listVacuo!=[]:
                    allVacuo=doc.addObject("Part::MultiFuse","AllVacuo")
                    allVacuo.Shapes=listVacuo
                    doc.recompute()
                    conductorObj=doc.addObject("Part::Cut","Conductor")
                    conductorObj.Base=lastConductorObj
                    conductorObj.Tool=allVacuo
                    
                    doc.recompute()
                    listVacuo=[]
                    listOfObjAfterBoolean.append(conductorObj)
                else:
                    if lastConductorObj!=None:
                        listOfObjAfterBoolean.append(lastConductorObj)
                    lastConductorObj=orderedList[i]    
            elif orderedList[i].Attribute==Attribute.Vacuo:
                listVacuo.append(orderedList[i])
            else:
                pass
    if listVacuo!=[]:
        if lastConductorObj!=None:
            allVacuo=doc.addObject("Part::MultiFuse","AllVacuo")
            allVacuo.Shapes=listVacuo
            doc.recompute()
            conductorObj=doc.addObject("Part::Cut","Conductor")
            conductorObj.Base=lastConductorObj
            conductorObj.Tool=allVacuo
            
            doc.recompute()
            listVacuo=[]
            listOfObjAfterBoolean.append(conductorObj)
            pass
        else:
            for objItem in listVacuo:
               Gui.ActiveDocument.getObject(orderedList[i].Name).Visibility=False 
            pass
    else:
        if lastConductorObj!=None:
            listOfObjAfterBoolean.append(lastConductorObj)
    resultShape=doc.addObject("Part::MultiFuse","ResultShape")
    resultShape.Shapes=listOfObjAfterBoolean
    doc.recompute()

#------------------------------------------结束-------------------------------------------#

# 得到场景中模型包围盒的最大最小值
# def getRangeOfAllObjs():
#
#     objsList = FreeCAD.ActiveDocument.Objects
#     xList = []
#     yList = []
#     zList = []
#
#     minPoint =[]
#     maxPoint =[]
#
#     for objItem in objsList:
#
#         # 得到所有属性
#         props = objItem.PropertiesList
#         for propItem in props:
#             prop = getattr(objItem, propItem)
#             # 判断是不是point
#             if type(prop) == Base.Vector:
#                 xList.append(prop.x)
#                 yList.append(prop.y)
#                 zList.append(prop.z)
#     # 得到xyz的范围
#     if xList!=[] and yList!=[] and zList!= []:
#         if FreeCAD.ActiveDocument.CoordinateSystem == CoordinateSystemTools.CoordinateType.Rectangular:
#             minPoint = [str(min(xList))+"m", str(min(yList))+"m",str(min(zList))+"m"]
#             maxPoint = [str(max(xList))+"m", str(max(yList))+"m",str(max(zList))+"m"]
#         elif FreeCAD.ActiveDocument.CoordinateSystem == CoordinateSystemTools.CoordinateType.Polar:
#             minPoint = [str(min(xList)) + "m", str(min(yList)) + "deg", str(min(zList)) + "m"]
#             maxPoint = [str(max(xList)) + "m", str(max(yList)) + "deg", str(max(zList)) + "m"]
#         else:
#             minPoint = [str(min(zList)) + "m", str(min(xList)) + "m", str(min(yList)) + "deg"]
#             maxPoint = [str(max(zList)) + "m", str(max(xList)) + "m", str(max(yList)) + "deg"]
#
#     return minPoint,maxPoint

# def getRangeOfAllObjs():
#
#     objsList = FreeCAD.ActiveDocument.Objects
#     xList = []
#     yList = []
#     zList = []
#
#     minPoint =[]
#     maxPoint =[]
#     # import PartGui
#     # PartGui.getPointsOfObj()
#     for objItem in objsList:
#
#         if 'Shape' in objItem.PropertiesList and objItem.Label != "ResultShape":
#
#             xList.append(objItem.Shape.BoundBox.XMin)
#             xList.append(objItem.Shape.BoundBox.XMax)
#             yList.append(objItem.Shape.BoundBox.YMin)
#             yList.append(objItem.Shape.BoundBox.YMax)
#             zList.append(objItem.Shape.BoundBox.ZMin)
#             zList.append(objItem.Shape.BoundBox.ZMax)
#
#
#
#     if xList!=[] and yList!=[] and zList!=[]:
#         if FreeCAD.ActiveDocument.CoordinateSystem == CoordinateSystemTools.CoordinateType.Rectangular:
#             minPoint = [str(min(xList))+"m", str(min(yList))+"m",str(min(zList))+"m"]
#             maxPoint = [str(max(xList))+"m", str(max(yList))+"m",str(max(zList))+"m"]
#         elif FreeCAD.ActiveDocument.CoordinateSystem == CoordinateSystemTools.CoordinateType.Polar:
#             RMin = math.sqrt(min(xList)*min(xList)+min(yList)*min(yList))
#             RMax = math.sqrt(max(xList)*max(xList)+max(yList)*max(yList))
#
#
#             if min(xList)* max(xList)<= 0 and min(yList)* max(yList)<= 0 :
#                 minPoint = ["0m", "0deg", str(min(zList)) + "m"]
#                 maxPoint = [str(max(RMin,RMax)) + "m", "360deg", str(max(zList)) + "m"]
#             else:
#                 minPoint = [str(min(RMin, RMax)) + "m", "0deg", str(max(zList)) + "m"]
#                 maxPoint = [str(max(RMin, RMax)) + "m", "360deg", str(max(zList)) + "m"]
#         else:
#             RMin = math.sqrt(min(xList) * min(xList) + min(yList) * min(yList))
#             RMax = math.sqrt(max(xList) * max(xList) + max(yList) * max(yList))
#             if min(xList)* max(xList)<= 0 and min(yList)* max(yList)<= 0 :
#                 minPoint = [str(min(zList)) + "m","0m", "0deg"]
#                 maxPoint = [str(max(zList)) + "m",str(max(RMin,RMax)) + "m", "360deg"]
#             else:
#                 minPoint = [str(min(zList)) + "m", str(min(RMin, RMax)) + "m", "0deg"]
#                 maxPoint = [str(max(zList)) + "m", str(max(RMin, RMax)) + "m", "360deg"]
#
#     return minPoint,maxPoint

def getRangeOfAllObjs():

    objsList = FreeCAD.ActiveDocument.Objects
    xList = []
    yList = []
    zList = []

    minPoint =[]
    maxPoint =[]
    import time
    t = time.time()
    if FreeCAD.ActiveDocument.CoordinateSystem == CoordinateSystemTools.CoordinateType.Rectangular:
        for objItem in objsList:
            if 'Shape' in objItem.PropertiesList and objItem.Label != "ResultShape" and 'Order' in objItem.PropertiesList:
                xList.append(objItem.Shape.BoundBox.XMin)
                xList.append(objItem.Shape.BoundBox.XMax)
                yList.append(objItem.Shape.BoundBox.YMin)
                yList.append(objItem.Shape.BoundBox.YMax)
                zList.append(objItem.Shape.BoundBox.ZMin)
                zList.append(objItem.Shape.BoundBox.ZMax)
        if xList != [] and yList != [] and zList != []:
            minPoint = [str(min(xList))+"m", str(min(yList))+"m",str(min(zList))+"m"]
            maxPoint = [str(max(xList))+"m", str(max(yList))+"m",str(max(zList))+"m"]
    else:

        import PartGui
        RZThetaRange = PartGui.getPointsOfObj()
        if RZThetaRange != None:
            # 获取r，z，theta的范围
            RMin= round(RZThetaRange[0],4)
            RMax = round(RZThetaRange[1],4)
            ZMin = round(RZThetaRange[2], 4)
            ZMax = round(RZThetaRange[3], 4)
            ThetaMin = round(RZThetaRange[4], 0)
            ThetaMax = round(RZThetaRange[5], 0)
            # 表示中间角
            ThetaMedium = round(RZThetaRange[6], 0)
            # 根据中间角判定最大最小值
            if ThetaMedium>ThetaMax or ThetaMedium<ThetaMin:
                ThetaMax = ThetaMin
                ThetaMin = ThetaMax-360
            # 修正误差，r必须大于0
            if RMin<0:
                RMin=0
            # 修正误差，存在过圆心的圆柱等时，将最小r设为0
            for objItem in objsList:
                if 'Type' in objItem.PropertiesList:

                    if objItem.Type in [ObjectType.Vol_Spherical,ObjectType.Vol_Cylinder,ObjectType.Vol_Cone] \
                            and (objItem.Shape.BoundBox.XMin * objItem.Shape.BoundBox.XMax)<0 \
                            and (objItem.Shape.BoundBox.YMin * objItem.Shape.BoundBox.YMax)<0:

                        RMin = 0
                        break

            if FreeCAD.ActiveDocument.CoordinateSystem == CoordinateSystemTools.CoordinateType.Polar:
                minPoint = [str(RMin) + "m", str(ThetaMin) +"deg", str(ZMin) + "m"]
                maxPoint = [str(RMax) + "m", str(ThetaMax) +"deg", str(ZMax) + "m"]

            else:

                minPoint = [str(ZMin) + "m", str(RMin) + "m", str(ThetaMin)+"deg"]
                maxPoint = [str(ZMax) + "m", str(RMax) + "m", str(ThetaMax) +"deg"]

    FreeCAD.Console.PrintError("求工作区域的时间")
    FreeCAD.Console.PrintError(time.time()-t)
    FreeCAD.Console.PrintError("\n")
    return minPoint,maxPoint
