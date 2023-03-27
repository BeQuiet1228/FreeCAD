# -*- coding: utf-8 -*-
import FreeCAD
import FreeCADGui
import Part
import re
###########################################################
###  此文件不允许导入其他包，否则会导致程序崩溃，难以维护      ####
###########################################################


class ObjectType:
    # 变量类型
    Variable = "Variable"
    #没有类型
    none = "none"
    # 点
    Point = "PointObj"
    # 线
    Line_Conformal = "Line_Conformal"
    Line_Oblique = "Line_Oblique"
    # 面
    Area_Conformal = "Area_Conformal"
    Area_Rectangular = "Area_Rectangular"
    Area_Polygonal = "Area_Polygonal"
    Area_Function = "Area_Function"
    # 体
    Vol_Conformal = "Vol_Conformal"
    # 圆台
    Vol_SpecialCone = "Vol_SpecialCone"
    Vol_Cone = "Vol_Cone"
    Vol_Cylinder = "Vol_Cylinder"
    Vol_Parallelepipedal = "Vol_Parallelepipedal"
    # 带孔的圆柱
    Vol_Annular = "Vol_Annular"
    Vol_Pyramid = "Vol_Pyramid"
    Vol_Rhombus = "Vol_Rhombus"
    Vol_Spherical = "Vol_Spherical"
    Vol_Wedge = "Vol_Wedge"
    Vol_Tetrahedron = "Vol_Tetrahedron"
    Vol_Toroidal_Section = "Vol_Toroidal_Section"
    Vol_Annular_Section = "Vol_Annular_Section"
    Vol_Function = "Vol_Function"
    Vol_Extruded = "Vol_Extruded"
    Vol_Helical = "Vol_Helical"

    Vol_Draft_Revolution = "Vol_Draft_Revolution"
    Vol_Revolution = "Vol_Revolution"
    # 阵列体
    Vol_Array = "Vol_Array"
    # 参数阵列体
    Vol_ParamArray = "Vol_ParamArray"
    Vol_Test = "Vol_Test"

    #草图建模的拉伸
    Vol_Draft_Extrude = "Vol_Draft_Extrude"

    # 边界设置
    SOLE = "SOLE"
    DRIV = "Driv"
    FOIL = "Foil"
    IND = "Inductor"
    PORT = "Port"
    FREE = "FreeSpace"
    SYMT = "Symtry"
    MARK = "Mark"
    # 发射处理
    BEAM = "Beam"
    EXPS = "Exps"
    GYRO = "Gyro"
    POPU = "Popu"
    FELD = "Feld"
    THER = "Ther"
    SECD = "Secd"
    IONI = "Ioni"
    GASOUT = "GasOut"
    # 观测设置
    CNTR = "Cntr"
    Vector = "Vector"
    PhasSpace = "PhasSpace"
    AreaRan = "AreaRan"
    Observe = "Obs"
    # 定时器
    DefaultTimer = "DefaultTimer"
    CustomTimer = "CustomTimer"
    # 工程设置
    Info = "Info"
    Simu = "Simu"
    NewMaterial = "NewMaterial"
    FieldSetting = "FieldSetting"
    TimeDomain = "TimeDomain"
    DataProcess = "DataProcess"
    RunOptions = "RunOptions"
    NewParticle = "ParticleDefine"
    # 宏粒子合并
    MacroParticle = "MacroParticle"
    CollectionOutput = "CollectionOutput"


# 定义属性
class Attribute:
    NotDefine = "NotDefine"
    Conductor = "Conductor"
    Custom = "Custom"
    Vacuo = "Vacuo"
    Void = "Void"


def getAllObjs():
    """
    获取文档中所有的obj
    :return:
    """
    # 模型类型，随着项目的不断拓展，模型的类型可能会不断增加，新增类型如果需要参与布尔运算则添加到该列表
    target_list = ['Part::FeaturePython', 'Part::CustomFeaturePython']
    temp_list = []
    for i in target_list:
        temp_list = temp_list + FreeCAD.ActiveDocument.findObjects(i)
    all_list = []
    for i in temp_list:
        all_list.append(i)
    return all_list


def getAllObjects():
    """
    获取当前文档中的所有模型列表
    """
    # 模型类型，随着项目的不断拓展，模型的类型可能会不断增加，新增类型如果需要参与布尔运算则添加到该列表
    target_list = ['Part::FeaturePython', 'Part::CustomFeaturePython']
    temp_list = []
    for i in target_list:
        temp_list = temp_list + FreeCAD.ActiveDocument.findObjects(i)
    model_list = []
    # 含有Order属性即被认作Model
    for i in temp_list:
        if hasattr(i, "Order") and hasattr(i, "Type"):
            model_list.append(i)
    return model_list


def getAllVolumeObj():
    """
    只获取体的obj
    """
    all_volumes = []
    all_obj = getAllObjects()
    for i in all_obj:
        if hasattr(i, "Type"):
            if i.Type != ObjectType.Point and i.Type != ObjectType.Line_Conformal and i.Type != ObjectType.Line_Oblique and \
                    i.Type != ObjectType.Area_Conformal and i.Type != ObjectType.Area_Rectangular and \
                    i.Type != ObjectType.Area_Polygonal and i.Type != ObjectType.Area_Function:
                all_volumes.append(i)
    return all_volumes


def getAllLines():
    """
    获取当前文档中所有的线
    """
    allLines = []
    objs = getAllObjects()
    for i in objs:
        if hasattr(i, "Type"):
            if i.Type == ObjectType.Line_Conformal or i.Type == ObjectType.Line_Oblique:
                allLines.append(str(i.Label))
    return allLines


def getAllAreas():
    """
    获取当前文档中所有的面
    """
    allAreas = []
    objs = getAllObjects()
    for i in objs:
        if hasattr(i, "Type"):
            if i.Type == ObjectType.Area_Conformal or i.Type == ObjectType.Area_Rectangular or \
                    i.Type == ObjectType.Area_Polygonal or i.Type == ObjectType.Area_Function:
                allAreas.append(str(i.Label))
    return allAreas


def getAllVolumes():
    """
    获取当前文档中所有的体
    """
    allVolumes = []
    objs = getAllObjects()
    allLines = getAllLines()
    allAreas = getAllAreas()
    for i in objs:
        if i not in allLines and i not in allAreas:
            allVolumes.append(str(i.Label))
    return allVolumes


def getObjByLabel(label):
    """
    通过Label获取当前的obj
    """
    objs = FreeCAD.ActiveDocument.getObjectsByLabel(label)
    if len(objs) == 0:
        FreeCAD.Console.PrintMessage("does not get this obj by Label\n")
        return
    obj = objs[0]
    return obj


def getLabelsByType(obj_type):
    """
    根据输入的type，获取所有该类型的名字
    """
    allObjsList = getAllObjs()
    resList = []
    for i in allObjsList:
        if hasattr(i, "Type") and i.Type == obj_type:
            resList.append(str(i.Label))
    return resList


def getBaseTypeByType(obj_type):
    """
    根据输入的type，获取所有该类型的baseType
    """
    allObjsList = getAllObjs()
    resList = {}
    for i in allObjsList:
        if hasattr(i, "BaseObjType") and i.Type == obj_type:
            baseObj = getObjByLabel(i.BaseType)
            resList[str(baseObj.Label)] = i
            # resList.append(str(baseObj.Label) : str(i.Label))
    return resList


def getConductorVols():
    """
    获得属性值为Conductor的正投影体
    """
    allObjsList = getAllObjects()
    resList = []
    for i in allObjsList:
        if hasattr(i, "Attribute"):
            if i.Attribute == Attribute.Conductor:
                resList.append(str(i.Label))
    return resList


def getAllValidModelObj():
    """
    获取当前文档所有有效的可以参与布尔运算的模型的列表
    返回的列表是根据Order排序的
    return type -> list
    """
    # 模型类型，随着项目的不断拓展，模型的类型可能会不断增加，新增类型如果需要参与布尔运算则添加到该列表
    target_list = ["Part::FeaturePython"]
    model_list = []
    for i in target_list:
        model_list = model_list + FreeCAD.ActiveDocument.findObjects(i)
    # 挑选含有Type，Attribute, Order属性的obj，并根据obj的Order进行排序
    eligible_list = []  # 合格的obj列表
    for i in model_list:
        if hasattr(i, "Type") and hasattr(i, "Order") and hasattr(i, "Attribute"):
            if i.Attribute != Attribute.NotDefine:
                eligible_list.append(i)
    # 对obj进行排序
    eligible_list.sort(key=getOrderOfObj)
    # begin
    # 修改原因：添加一个循环使得该函数的返回值总是以一个conductor或者custom属性的体开头
    valid_num = 0
    for i in eligible_list:
        if i.Attribute == Attribute.Void:
            valid_num += 1
        else:
            break
    return eligible_list[valid_num:]


def getBoolList():
    """
    把布尔运算属性分开，conductor和custom放在一起，void放在一起。交替进行
    return type->[[]]
    """
    bool_list = []
    valid_list = getAllValidModelObj()
    left = 0
    right = 0
    while right < len(valid_list):
        # 把conduct和Custom的属性放在列表中
        while right < len(valid_list) and \
                (valid_list[right].Attribute == Attribute.Conductor or valid_list[right].Attribute == Attribute.Custom):
            right += 1
        judgeList1 = valid_list[left:right]
        if len(judgeList1) != 0:
            bool_list.append(judgeList1)
        left = right
        # 把void放在列表中，和conduct，custom交替进行
        while right < len(valid_list) and valid_list[right].Attribute == Attribute.Void:
            right += 1
        judgeList2 = valid_list[left:right]
        if len(judgeList2) != 0:
            bool_list.append(judgeList2)
        left = right
    return bool_list


def getAllPhyAndProObjects():
    """
    获取当前所有物理设置工程设置的obj，没有order和Atrribute的认定为物理设置
    """
    # 模型类型，随着项目的不断拓展，模型的类型可能会不断增加，新增类型如果需要参与布尔运算则添加到该列表
    target_list = ["Part::FeaturePython"]
    pp_list = []  # physics and project list
    for i in target_list:
        pp_list = pp_list + FreeCAD.ActiveDocument.findObjects(i)
    res_list = []
    # 挑选出所有有Type类型的obj
    for i in pp_list:
        if hasattr(i, "Type") and not hasattr(i, "Order") and not hasattr(i, "Atrribute"):
            res_list.append(i)
    return res_list


def isFourPointsOnTheSamePlane(points):
    """
    判断几个点是否共面
    """
    point_1 = points[0]
    points.append(point_1)
    try:
        wires = Part.makePolygon(points)
        shape = Part.makeFace(wires, "Part::FaceMakerBullseye")
    except:
        return False
    return True


def isPointEqual(points):
    """
    判断是否有相同的点
    """
    for i in range(0, len(points)-1):
        for j in range(i+1, len(points)):
            if points[i] == points[j]:
                return True
    return False


def getOrderedObjects():
    """
    根据order对obj排序
    """
    model_list = getAllObjects()
    model_list.sort(key=getOrderOfObj)
    return model_list


def getOrderOfObj(obj):
    return obj.Order


def updateWhenOrderChanged(obj, lastOrder, newOrder):
    """
    当Order发生变化时自动调整所有obj的Order
    """
    ordered_list = getOrderedObjects()  # 已经排序的obj的list
    objNumbers = len(ordered_list)  # 当前所有obj的数量

    if objNumbers == 1:
        obj.Order = 0
        return
    # 首先判断newOrder, lastOrder均在合理范围内
    if 0 <= newOrder < objNumbers:
        pass
    else:
        FreeCAD.Console.PrintError("error:传入的order:  " + str(newOrder) + "不在合理范围内\n")
        obj.Order = objNumbers - 1
        return
    # obj新建的时候默认order为9999
    if lastOrder == 9999 or lastOrder >= objNumbers:
        if newOrder == objNumbers - 1:
            obj.Order = newOrder
        elif newOrder < objNumbers - 1:
            # range的范围是左闭右开的 [newOrder， objNumbers)
            for i in range(newOrder, objNumbers):
                ordered_list[i].Order = ordered_list[i].Order + 1
            obj.Order = newOrder
        else:
            FreeCAD.Console.PrintError.sayz("error:传入的order错误\n")
    else:
        if newOrder < lastOrder:
            for i in range(newOrder, lastOrder):
                ordered_list[i].Order = ordered_list[i].Order + 1
            obj.Order = newOrder
        elif newOrder > lastOrder:
            for i in range(lastOrder + 1, newOrder + 1):
                ordered_list[i].Order = ordered_list[i].Order - 1
            obj.Order = newOrder
        else:
            FreeCAD.Console.PrintError("error:传入的order错误\n")


def initResultIbj(doc):
    """
    初始化布尔运算对象
    doc: 新建模型所在文档
    return：obj
    """
    obj = doc.getObject("ResultShape")
    if not obj:
        obj = doc.addObject("Part::FeaturePython", "ResultShape")
    # 把布尔运算的结果抛光
    obj.ViewObject.ShapeMaterial.SpecularColor = (0.45, 0.45, 0.45)
    obj.addProperty("Part::PropertyShapeHistory","History","","")
    obj.ViewObject.Proxy = 0
    FreeCADGui.getDocument(doc.Name).getObject(obj.Name).DisplayMode = u"Shaded"
    doc.recompute()

    obj.setEditorMode('Placement', 2)
    doc.recompute()
    return obj


def parseExpressionStr(expressionStr):
    '''
    将表达式中带有参数的值转化为具体的值
    '''
    paramObj = FreeCAD.ActiveDocument.Param
    propertyList = paramObj.PropertiesList
    propertyList = [i for i in propertyList if i not in ['DynamicData', 'ExpressionEngine', 'Label', 'Proxy', 'Type']]
    resultExpressionStr = expressionStr
    resultExpressionStr = re.sub("\\b\\*\\*\\b","^",resultExpressionStr,flags=re.IGNORECASE)
    for propertyItem in propertyList:
        resultExpressionStr = re.sub("\\b" + propertyItem + "\\b",str(getattr(paramObj, propertyItem)),resultExpressionStr,flags=re.IGNORECASE)
    FreeCAD.Console.PrintError(resultExpressionStr)
    return resultExpressionStr




