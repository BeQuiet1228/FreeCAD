# -*- coding: utf-8 -*-
import FreeCAD
import PySide
from PySide import QtGui
import FreeCADGui
import re


# 定义obj类型
from Modeling.Modeling2D.Tools import ExpressionTools


class ObjectType:
    # 变量类型
    Variable = "Variable"
    # 没有类型
    none = "none"
    # 2D模型
    Point = "Point"
    Line = "Line"
    LineConformal = "LineConformal"
    AreaPolygonal = "AreaPolygonal"
    AreaConformal = "AreaConformal"
    AreaCircular = "AreaCircular"
    AreaFunction = "AreaFunction"
    Rectangle = "Rectangle"
    RegularPolygon = "RegularPolygon"
    Sector = "Sector"
    Fillet = "Fillet"
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
    # 观测设置
    CNTR = "Cntr"
    Vector = "Vector"
    PhasSpace = "PhasSpace"
    AreaRan = "AreaRan"
    Observe = "Observe"
    # 定时器
    DefaultTimer = "DefaultTimer"
    Timer = "Timer"
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
    MarcoParticle = "MarcoParticle"
    # 注释
    Annotation = "Annotation"
    # 网格
    DiyGrid = "DiyGrid"


# 定义属性
class Attribute:
    NotDefine = "NotDefine"
    Conductor = "Conductor"
    Custom = "Custom"
    Vacuo = "Vacuo"
    # @wangzhenguo 修改Vacuo为Void
    Void = "Void"


# @lilei
# 定义工程设置和物理设置的枚举


# class SettingType(Enum):
#     beam = 0
#     exps = 1
#     gyro = 2
#     popu = 3
#     feld = 4
#     ther = 5
#     secd = 6
#     ioni = 7
#     sole = 8
#     driv = 9
#
#     foil = 10
#     inductor = 11
#     port = 12
#     free = 13
#     symt = 14
#     mark = 15
#     cntr = 16
#     vector = 17
#     phasSpace = 18
#     areaRan = 19
#     observe = 20
#     info = 21
#     simu = 22
#     newMaterial = 23
#     fieldSetting = 24
#     timeDomain = 25
#     dataProcess = 26
#     runOptions = 27
#     newParticle = 28


def sayz(msg):
    FreeCAD.Console.PrintError(msg)
    FreeCAD.Console.PrintError("\n")


# 判断一个物体是否含有某个属性
def hasThePropertyByObj(obj, prop):
    """
    判断一个物体是否含有某个属性
    """
    if obj:
        props = obj.PropertiesList
        for propItem in props:
            if propItem == prop:
                return True
        return False
    else:
        return False


# def createInitGroup(groupName, groupLabel):
#     """
#     在树形结构中创建文件分组\n
#     groupName : internal name of this object\n
#     groupLabel: user name of this object
#     """
#     g = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroup", groupName)
#     g.Label = groupLabel
#     return g


# def initGroup():
#     """
#     初始化树结构，为树结构添加分组
#     """
#     # 一级目录
#     createInitGroup("Modeling2D11", "模型")
#     createInitGroup("Physics11", "物理设置")
#     createInitGroup("ProjectSetting11", "工程设置")
#     # 二级目录
#     createInitGroup("PointG", "点")
#     createInitGroup("Line", "线")
#     createInitGroup("Area", "面")
#     # addObject(a)
#
#
# def addObjectToGroup(obj):
#     """
#     将obj添加到对应的分组，主要执行分类操作
#     """
#     if obj.Type == ObjectType.Point:
#         addObjectToGroup_helper(obj, 'PointG', '点')
#
#
# def addObjectToGroup_helper(obj, groupName, groupLabel):
#     """
#     将obj添加到对应分组的辅助函数，将obj真正添加到分组中
#     """
#     group = FreeCAD.ActiveDocument.getObject(groupName)
#     if group:
#         group[0].addObject(obj)
#     else:
#         group = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroup", groupName)
#         group.Label = groupLabel
#         group.addObject(obj)
#
#
# def initDocument(doc):
#     """
#     author:   @LZG
#     @ doc :   document
#     @ return: void
#     function: 0、新增结果对象；
#               1、为文档增加监听；
#               2、将默认的json加到comment中；
#               3、添加默认定时器
#     note: 模仿伏彪的代码编写的
#     """
#     # 新增结果object
#     obj = ObjectsTools.initResultIbj(doc)
#
#     # 监听
#     # obs=DocumentObservers()
#     FreeCAD.addDocumentObserver(DocumentObservers())
#     FreeCAD.addDocumentObserver(TransparencyObserver())
#
#     # 测试
#     # FreeCAD.addDocumentObserver(NeedsRecomputeObserver())
#     # 新增加json文件到comment中去
#     ProjectSettingsTools.initPrjectSettings()
#
#     # 添加默认定时器
#     # init TimerDef
#     from Modeling.Common.CommonCommand.NewDocument import ObjectDict
#     from Physics.PhysicsCommand.DefaultTimerDlgMain import DefaultTimerMain
#
#     ObjectDict["TimerDef1"] = DefaultTimerMain("new", "TimerDef1")
#     ObjectDict["TimerDef1"].initToDoc()
#     # end
#     # 初始化2D建模平台下的分组
#     initGroup()
#
#
# def otherDocInit():
#     doc = FreeCAD.ActiveDocument
#     initDocument(doc)
#     initParamObj(doc)
#     FreeCADGui.doCommand("from Modeling.Common.Tools import DocumentTools")
#     # FreeCAD.addDocumentObserver(AfterReBuildByM3dObserver())
#     FreeCAD.addDocumentObserver(NeedsRecomputeObserver())


# # 初始化参量对象，这个不能直接加载initDocument中，因为解析时，也会执行上面的函数，报错
# def initParamObj(doc):
#     if doc.CoordinateSystem == CoordinateSystemTools.CoordinateType.Rectangular:
#         ObjectsTools.setDX1DX2DX3("1mm","1mm","1mm")
#     elif doc.CoordinateSystem == CoordinateSystemTools.CoordinateType.Polar:
#         ObjectsTools.setDX1DX2DX3("1mm","30deg","1mm")
#     elif doc.CoordinateSystem == CoordinateSystemTools.CoordinateType.Cylindrical:
#         ObjectsTools.setDX1DX2DX3("1mm","1mm","30deg")


# def getAllObjectsByTypes(docName, findTypes):
#     """
#     docName: 当前文件名
#     findTypes: 需要寻找的类型列表
#     return list of objs
#     """
#     resultObjs = []
#     objs = getAllObjectsOfThisDoc(docName)
#     for objItem in objs:
#         if hasThePropertyByObj(objItem, "Type"):
#             if objItem.Type in findTypes:
#                 resultObjs.append(objItem)
#     return resultObjs
#
#
# # 获取当前文档中的所有模型列表
# def getAllObjectsOfThisDoc(docName):
#     """
#     docName: String 文档的Name
#     return: List[]
#     """
#     curDocument = FreeCAD.getDocument(docName)
#     featurePythonList = curDocument.findObjects('Part::FeaturePython')
#     customFeaturePythonList = curDocument.findObjects('Part::CustomFeaturePython')
#     objectList = featurePythonList + customFeaturePythonList
#     tempList = []
#     # 剔除没有Type属性的物体
#     for objItem in objectList:
#         if hasThePropertyByObj(objItem, "Type") and hasThePropertyByObj(objItem, "Order"):
#             tempList.append(objItem)
#     return tempList


# 为模型对象添加通用的属性
def addCommonPropertyToObject(obj):
    # Mark
    obj.addProperty("App::PropertyBool", "isMarkX", "NonUniformGrid", "").isMarkX = True
    obj.addProperty("App::PropertyBool", "isMarkY", "NonUniformGrid", "").isMarkY = True
    obj.addProperty("App::PropertyBool", "isCheckMinX", "NonUniformGrid", "").isCheckMinX = False
    obj.addProperty("App::PropertyBool", "isCheckMidX", "NonUniformGrid", "").isCheckMidX = False
    obj.addProperty("App::PropertyBool", "isCheckMaxX", "NonUniformGrid", "").isCheckMaxX = False
    obj.addProperty("App::PropertyBool", "isCheckMinY", "NonUniformGrid", "").isCheckMinY = False
    obj.addProperty("App::PropertyBool", "isCheckMidY", "NonUniformGrid", "").isCheckMidY = False
    obj.addProperty("App::PropertyBool", "isCheckMaxY", "NonUniformGrid", "").isCheckMaxY = False
    obj.addProperty("App::PropertyString", "MarkX", "NonUniformGrid", "").MarkX = "DX1"
    obj.addProperty("App::PropertyString", "MarkY", "NonUniformGrid", "").MarkY = "DX2"
    # Order
    obj.addProperty("App::PropertyInteger", "Order", "NonUniformGrid", "").Order = 9999


# 为模型添加Attribute属性
def addAttributeToObject(obj):
    # 属性
    obj.addProperty("App::PropertyString", "Attribute", "Attribute", "Conformal of Object")
    obj.Attribute = Attribute.NotDefine
    obj.addProperty("App::PropertyString", "C_SIGMA", "Attribute", "").C_SIGMA = "Isotropy"
    obj.addProperty("App::PropertyString", "RDC", "Attribute", "").RDC = "Isotropy"
    obj.addProperty("App::PropertyString", "SIGMA1", "Attribute", "").SIGMA1 = "0.05"
    obj.addProperty("App::PropertyString", "SIGMA2", "Attribute", "").SIGMA2 = "1.0"
    obj.addProperty("App::PropertyString", "SIGMA3", "Attribute", "").SIGMA3 = "1.0"
    obj.addProperty("App::PropertyString", "EPS1", "Attribute", "").EPS1 = "1.0"
    obj.addProperty("App::PropertyString", "EPS2", "Attribute", "").EPS2 = "0.0"
    obj.addProperty("App::PropertyString", "EPS3", "Attribute", "").EPS3 = "0.0"


# 补全属性，如果老工程没有的话
def completionProperties(obj):
    obj.addProperty("App::PropertyString", "C_SIGMA", "Attribute", "").C_SIGMA = "Isotropy"
    obj.addProperty("App::PropertyString", "RDC", "Attribute", "").RDC = "Isotropy"
    obj.addProperty("App::PropertyString", "SIGMA1", "Attribute", "").SIGMA1 = "0.05"
    obj.addProperty("App::PropertyString", "SIGMA2", "Attribute", "").SIGMA2 = "1.0"
    obj.addProperty("App::PropertyString", "SIGMA3", "Attribute", "").SIGMA3 = "1.0"
    obj.addProperty("App::PropertyString", "EPS1", "Attribute", "").EPS1 = "1.0"
    obj.addProperty("App::PropertyString", "EPS2", "Attribute", "").EPS2 = "0.0"
    obj.addProperty("App::PropertyString", "EPS3", "Attribute", "").EPS3 = "0.0"


# 为obj添加user_xxx属性，该属性直接存储用户的输入信息
def addUserProperty(obj, num):
    """
    为obj添加user_xxx属性，该属性直接存储用户的输入信息
    :param obj: FreeCAD对象
    :param num: 添加属性的数量
    :return: None
    """
    if num > 0:
        # 从1开始命名
        for i in range(num):
            obj.addProperty("App::PropertyString", "user_point" + str(i+1) + "_x")
            obj.addProperty("App::PropertyString", "user_point" + str(i+1) + "_y")


# @lilei
# QT转换器的虚拟函数
def QT_TRANSLATE_NOOP(ctx, txt):
    return txt


# 发射选项
def addLaunchOptionsCommonProperty(obj):
    obj.addProperty("App::PropertyBool", "isParticleType").isParticleType = False
    obj.addProperty("App::PropertyString", "particleType").particleType = "电子"
    obj.addProperty("App::PropertyBool", "isGenerationRate").isGenerationRate = False
    obj.addProperty("App::PropertyInteger", "generationRate").generationRate = 1

    obj.addProperty("App::PropertyBool", "isFiringInterval").isFiringInterval = False
    obj.addProperty("App::PropertyBool", "isRandomDistribution").isRandomDistribution = True
    obj.addProperty("App::PropertyBool", "isStrictTiming").isStrictTiming = False
    obj.addProperty("App::PropertyInteger", "firingInterval").firingInterval = 0

    obj.addProperty("App::PropertyBool", "isSurfaceDistribution").isSurfaceDistribution = False
    obj.addProperty("App::PropertyBool", "isRandom1").isRandom1 = True
    obj.addProperty("App::PropertyBool", "isBalance1").isBalance1 = False
    obj.addProperty("App::PropertyBool", "isImmobilization1").isImmobilization1 = False

    obj.addProperty("App::PropertyBool", "isOuterSurfaceDistribution").isOuterSurfaceDistribution = False
    obj.addProperty("App::PropertyBool", "isRandom2").isRandom2 = True
    obj.addProperty("App::PropertyBool", "isImmobilization2").isImmobilization2 = False
    obj.addProperty("App::PropertyString", "excursion").excursion = "0.001"

    obj.addProperty("App::PropertyString", "launchArea1").launchArea1 = "不指定"
    obj.addProperty("App::PropertyString", "launchArea2").launchArea2 = "不指定"
    obj.addProperty("App::PropertyString", "launchOrthogonalProjectionRegin1").launchOrthogonalProjectionRegin1 = "不指定"
    obj.addProperty("App::PropertyString", "launchOrthogonalProjectionRegin2").launchOrthogonalProjectionRegin2 = "不指定"


def addCommonStartEndCoordinate(obj):
    obj.addProperty("App::PropertyString", "point1_X", ).point1_X = "0mm"
    obj.addProperty("App::PropertyString", "point1_Y", ).point1_Y = "0mm"
    obj.addProperty("App::PropertyString", "point1_name", ).point1_name = "NULL"
    obj.addProperty("App::PropertyString", "point2_X", ).point2_X = "0mm"
    obj.addProperty("App::PropertyString", "point2_Y", ).point2_Y = "0mm"
    obj.addProperty("App::PropertyString", "point2_name", ).point2_name = "NULL"


def addCommonDirection(obj):
    obj.addProperty("App::PropertyBool", "isCheckNormal1", ).isCheckNormal1 = True
    obj.addProperty("App::PropertyBool", "isCheckNormal2", ).isCheckNormal2 = False


def isNegativeOrPositive(obj):
    obj.addProperty("App::PropertyBool", "isNegative").isNegative = False
    obj.addProperty("App::PropertyBool", "isPositive").isPositive = True


def getAllValidModelObj():
    """
    获取当前文档所有有效的可以参与布尔运算的模型的列表
    返回的列表是根据Order排序的
    return type -> list
    """
    # 模型类型，随着项目的不断拓展，模型的类型可能会不断增加，新增类型如果需要参与布尔运算则添加到该列表
    target_list = ["Part::Part2DObject", "Part::FeaturePython"]
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
    # 时间：2020.11.24
    # 修改原因：添加一个循环使得该函数的返回值总是以一个conductor或者custom属性的体开头
    valid_num = 0
    for i in eligible_list:
        if i.Attribute == Attribute.Void:
            valid_num += 1
        else:
            break
    # end by lzg
    return eligible_list[valid_num:]


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
        sayz("error:传入的order:  " + str(newOrder) + "不在合理范围内")
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
            sayz("error:传入的order错误")
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
            sayz("error:传入的order错误")


def getOrderedObjects():
    model_list = getAllModelObjects()
    model_list.sort(key=getOrderOfObj)
    return model_list


def getAllModelObjects():
    """
    获取当前所有的体
    """
    # 模型类型，随着项目的不断拓展，模型的类型可能会不断增加，新增类型如果需要参与布尔运算则添加到该列表
    target_list = ["Part::Part2DObject", "Part::FeaturePython"]
    temp_list = []
    for i in target_list:
        temp_list = temp_list + FreeCAD.ActiveDocument.findObjects(i)
    model_list = []
    # 含有Order属性即被认作Model
    for i in temp_list:
        if hasattr(i, "Order"):
            model_list.append(i)
    return model_list


def getAllObjects():
    """
    获取当前工程所有的obj，包括体和物理设置
    """
    target_list = ["Part::Part2DObject", "Part::FeaturePython"]
    obj_list = []
    for i in target_list:
        obj_list = obj_list + FreeCAD.ActiveDocument.findObjects(i)
    return obj_list


def setLabelToObj(obj, label):
    """
    将Label设置到obj中去，该函数主要解决Label的重复问题
    """
    label = label.replace(" ", "")
    if obj.Label == label:
        return
    obj_list = FreeCAD.ActiveDocument.getObjectsByLabel(label)
    if len(obj_list) == 0:
        obj.Label = label
    elif len(obj_list) == 1:
        if len(label) < 4:
            obj.Label = label + "001"
        else:
            # 获取最后三个字母并判断是否为数字，如果是数字就+1
            end_str = label[-3:]
            if end_str.isdigit():
                end_str = str(int(end_str) + 1)
                if len(end_str) == 1:
                    end_str = "00" + end_str
                elif len(end_str) == 2:
                    end_str = "0" + end_str
                obj.Label = label[:-3] + end_str
            else:
                obj.Label = label + "001"
            pass
    else:
        sayz("严重错误！Label出现重复！")


def getAllPhyAndProObjects():
    """
    获取当前所有物理设置工程设置的obj
    """
    # 模型类型，随着项目的不断拓展，模型的类型可能会不断增加，新增类型如果需要参与布尔运算则添加到该列表
    target_list = ["Part::FeaturePython"]
    pp_list = []  # physics and project list
    for i in target_list:
        pp_list = pp_list + FreeCAD.ActiveDocument.findObjects(i)
    res_list = []
    # 挑选出所有有Type类型的obj
    for i in pp_list:
        if hasattr(i, "Type"):
            res_list.append(i)
    return res_list


def getAllPropertiesAndProcessesObj():
    """
    获取所有与 Properties And Processes 相关的obj
    return type -> dict
    """
    res_dict = {ObjectType.SOLE: [],
                ObjectType.DRIV: [],
                ObjectType.FOIL: [],
                ObjectType.IND:  [],
                ObjectType.PORT: [],
                ObjectType.FREE: [],
                ObjectType.SYMT: [],
                ObjectType.BEAM: [],
                ObjectType.EXPS: [],
                ObjectType.GYRO: [],
                ObjectType.POPU: [],
                ObjectType.FELD: [],
                ObjectType.THER: [],
                ObjectType.SECD: [],
                ObjectType.IONI: [],
                ObjectType.MarcoParticle: [],
                }

    pp_list = getAllPhyAndProObjects()  # physics and project list , 请不要混淆
    # 挑选与Properties And Processes相关的obj
    for i in pp_list:
        if i.Type == ObjectType.SOLE:
            res_dict[ObjectType.SOLE].append(i)
        elif i.Type == ObjectType.DRIV:
            res_dict[ObjectType.DRIV].append(i)
        elif i.Type == ObjectType.FOIL:
            res_dict[ObjectType.FOIL].append(i)
        elif i.Type == ObjectType.IND:
            res_dict[ObjectType.IND].append(i)
        elif i.Type == ObjectType.PORT:
            res_dict[ObjectType.PORT].append(i)
        elif i.Type == ObjectType.FREE:
            res_dict[ObjectType.FREE].append(i)
        elif i.Type == ObjectType.SYMT:
            res_dict[ObjectType.SYMT].append(i)
        # 发射处理
        elif i.Type == ObjectType.BEAM:
            res_dict[ObjectType.BEAM].append(i)
        elif i.Type == ObjectType.EXPS:
            res_dict[ObjectType.EXPS].append(i)
        elif i.Type == ObjectType.GYRO:
            res_dict[ObjectType.GYRO].append(i)
        elif i.Type == ObjectType.POPU:
            res_dict[ObjectType.POPU].append(i)
        elif i.Type == ObjectType.FELD:
            res_dict[ObjectType.FELD].append(i)
        elif i.Type == ObjectType.THER:
            res_dict[ObjectType.THER].append(i)
        elif i.Type == ObjectType.SECD:
            res_dict[ObjectType.SECD].append(i)
        elif i.Type == ObjectType.IONI:
            res_dict[ObjectType.IONI].append(i)
        # 宏粒子合并
        elif i.Type == ObjectType.MarcoParticle:
            res_dict[ObjectType.MarcoParticle].append(i)

    return res_dict

# 获取给定类型的对象
def getSpecificTypePhyAndProObjects(objType):
    pp_list = getAllPhyAndProObjects()
    res_list = []
    for i in pp_list:
        if i.Type == objType:
            res_list.append(i)
    return res_list

def recomputeAreaPolygon(obj):
    """
    重新计算多边形的形状，由于多边形的helper的数量并不确定
    可以将该功能写在execute里面
    """
    points = []
    for index in range(len(obj.Points)):
        temp_x = getattr(obj, "helper_" + str(index)).x
        temp_y = getattr(obj, "helper_" + str(index)).y
        Vector = FreeCAD.Vector(temp_x, temp_y, 0)
        points.append(Vector)
    obj.Points = points


def updateText(self, m2d_str):
    # 该关键词的list本来存放在File文件中，但因为该文件导包出现异常，暂时将该list存放在此处
    # 定义涉及到的关键字
    keywordInCommand = ["FUNCTION",
                        "START", "STOP",
                        "SYSTEM", "POINT", "LINE", "AREA", "VOLUME",
                        "DURATION", "TIMER", "MARK", "AUTOGRID",
                        "SYMMETRY", "PORT", "FREESPACE",
                        "CONDUCTANCE", "DIELECTRIC", "CONDUCTOR", "VOID", "MATERIAL", "FOIL", "INDUCTOR", "DRIVER",
                        "EMISSION", "EMIT",
                        "MAXWELL", "MODE", "TIME_STEP",
                        "CONTINUITY",
                        "PRESET",
                        "GRAPHICS", "DUMP", "HEADER",
                        "OBSERVE",
                        "DISPLAY", "CONTOUR", "VECTOR", "PHASESPACE", "RANGE",
                        "KINEMATICS"]
    # 获得面板
    thisSubWindow = self.getThisSubWindow()

    if thisSubWindow is None:
        self.showThisSubWindow()
        thisSubWindow = self.getThisSubWindow()

    fileView = thisSubWindow.widget()
    # 清除原来的文字
    fileView.ui.textEdit.clear()
    # 做初始化设置
    textEdit = fileView.ui.textEdit
    textEdit.setFontWeight(63)          # 设置字体粗细
    textEdit.setFontFamily(u"Arial")    # 设置字体

    # 设置颜色变量
    green = PySide.QtGui.QColor(0, 128, 0, 255)
    black = PySide.QtGui.QColor(0, 0, 0, 255)
    blue = PySide.QtGui.QColor(0, 0, 150, 255)
    gray = PySide.QtGui.QColor(200, 200, 200, 255)
    white = PySide.QtGui.QColor(255, 255, 255, 255)

    # 将要显示的字符串按行分割并赋值给lineStrs
    lineStrs = m2d_str.split("\n")

    # 循环遍历每一行字符，并根据需求加上具体的效果
    for lineStr in lineStrs:
        textEdit.append("")
        # 如果某一行的首字符为!，则这一行为注释行，颜色为绿色
        if lineStr != "" and lineStr[0] == "!":
            textEdit.setTextColor(green)
            textEdit.insertPlainText(lineStr)
        else:
            # 如果该行的第一个单词为关键字，则显示为蓝色
            words = lineStr.split(" ")
            if keywordInCommand.__contains__(words[0]):
                textEdit.setTextColor(blue)
                textEdit.insertPlainText(words[0])
                textEdit.setTextColor(black)
                textEdit.insertPlainText(lineStr[len(words[0]): len(lineStr)])
            else:
                textEdit.setTextColor(black)
                textEdit.insertPlainText(lineStr)


def getAllModelObjDict():
    """
    获取所有的点线面的obj
    """
    res_dict = {
        ObjectType.Point: [],
        ObjectType.Line: [],
        ObjectType.LineConformal: [],
        ObjectType.AreaPolygonal: [],
        ObjectType.AreaConformal: [],
        ObjectType.AreaCircular: [],
        ObjectType.Rectangle: [],
        ObjectType.Sector: [],
        ObjectType.Fillet: []
    }
    obj_List = getAllModelObjects()
    for i in obj_List:
        if i.Type == ObjectType.Point:
            res_dict[ObjectType.Point].append(i)

        elif i.Type == ObjectType.Line:
            res_dict[ObjectType.Line].append(i)

        elif i.Type == ObjectType.LineConformal:
            res_dict[ObjectType.LineConformal].append(i)

        elif i.Type == ObjectType.AreaPolygonal:
            res_dict[ObjectType.AreaPolygonal].append(i)

        elif i.Type == ObjectType.AreaConformal:
            res_dict[ObjectType.AreaConformal].append(i)

        elif i.Type == ObjectType.AreaCircular:
            res_dict[ObjectType.AreaCircular].append(i)

        elif i.Type == ObjectType.Rectangle:
            res_dict[ObjectType.Rectangle].append(i)

        elif i.Type == ObjectType.Sector:
            res_dict[ObjectType.Sector].append(i)

        elif i.Type == ObjectType.Fillet:
            res_dict[ObjectType.Fillet].append(i)

    return res_dict


def getAllPlotsDict():
    """
    获取观测设置相关的字典,放进ALL PLOTS
    """
    res_dict = {
        ObjectType.DefaultTimer:[],
        ObjectType.Timer: [],
        ObjectType.CNTR: [],
        ObjectType.Vector: [],
        ObjectType.PhasSpace: [],
        ObjectType.AreaRan: [],
        ObjectType.Observe: []
    }

    ap_list = getAllPhyAndProObjects()
    for i in ap_list:

        if i.Type == ObjectType.DefaultTimer:
            res_dict[ObjectType.DefaultTimer].append(i)

        if i.Type == ObjectType.Timer:
            res_dict[ObjectType.Timer].append(i)

        if i.Type == ObjectType.CNTR:
            res_dict[ObjectType.CNTR].append(i)

        elif i.Type == ObjectType.Vector:
            res_dict[ObjectType.Vector].append(i)

        elif i.Type == ObjectType.PhasSpace:
            res_dict[ObjectType.PhasSpace].append(i)

        elif i.Type == ObjectType.AreaRan:
            res_dict[ObjectType.AreaRan].append(i)

        elif i.Type == ObjectType.Observe:
            res_dict[ObjectType.Observe].append(i)

    return res_dict


def getHeaderDict():
    """
    获取模型输入信息
    """
    res_dict = {ObjectType.Info: []}
    h_list = getAllPhyAndProObjects()
    for i in h_list:
        if i.Type == ObjectType.Info:
            res_dict[ObjectType.Info].append(i)

    return res_dict

def getGridDict():
    """
    获取网格信息
    """
    res_dict = {ObjectType.Simu: []}
    grid_list = getAllPhyAndProObjects()
    for i in grid_list:
        if i.Type == ObjectType.Simu:
            res_dict[ObjectType.Simu].append(i)

    return res_dict


def getCommonPresets():
    """
    获取 CommonPresets 有关的m2d
    """
    res_dict = {ObjectType.NewParticle: [],
                ObjectType.NewMaterial: [],
                ObjectType.FieldSetting: []
                }
    cp_list = getAllPhyAndProObjects()
    for i in cp_list:
        if i.Type == ObjectType.NewParticle:
            res_dict[ObjectType.NewParticle].append(i)

        if i.Type == ObjectType.NewMaterial:
            res_dict[ObjectType.NewMaterial].append(i)

        if i.Type == ObjectType.FieldSetting:
            res_dict[ObjectType.FieldSetting].append(i)
    return res_dict

def getSimulationSetting():
    """
    获取 Simulation Setting 有关的字典
    """
    res_dict = {ObjectType.TimeDomain: []}
    ss_list = getAllPhyAndProObjects()
    for i in ss_list:
        if i.Type == ObjectType.TimeDomain:
            res_dict[ObjectType.TimeDomain].append(i)
    return res_dict

def getDumpOptions():
    """
    获取 Dump Options 有关的字典
    """
    res_dict = {ObjectType.DataProcess: []}
    do_list = getAllPhyAndProObjects()
    for i in do_list:
        if i.Type == ObjectType.DataProcess:
            res_dict[ObjectType.DataProcess].append(i)
    return res_dict

def getRunOptions():
    """
    获取Run Options有关的的字典
    """
    res_dict = {ObjectType.RunOptions: []}
    ro_list = getAllPhyAndProObjects()
    for i in ro_list:
        if i.Type == ObjectType.RunOptions:
            res_dict[ObjectType.RunOptions].append(i)
    return res_dict

# 发射处理的公共属性，ui和数据的交互
class EmissionUiData(QtGui.QDialog):
    def __init__(self, obj, ui, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.obj = obj
        self.ui = ui
        self.initEmissionDialog()
        # self.loadData()

    def initEmissionDialog(self):
        try:
            # 代码补全
            self.defaultValue = ["OSYS$PLANE"]
            # 这段代码暂时注释
            # CompleterTools.setLineEditsCompleter(CompleterTools.getAllLineEdits(self.ui))
            self.ui.checkBox_particleType.clicked.connect(self.checkBox_particleType_clicked)
            self.ui.checkBox_generationRate.clicked.connect(self.checkBox_generationRate_clicked)
            self.ui.checkBox_transmittingInterval.clicked.connect(self.checkBox_transmittingInterval_clicked)
            self.ui.checkBox_surface.clicked.connect(self.checkBox_surface_clicked)
            self.ui.checkBox_outSurface.clicked.connect(self.checkBox_outSurface_clicked)

            # self.ui.ComboBox_Shadow.currentIndexChanged.connect(lambda: self.ComboBox_changed("ComboBox_Shadow"))
            # self.ui.ComboBox_included.currentIndexChanged.connect(lambda: self.ComboBox_changed("ComboBox_included"))
            # self.ui.ComboBox_includedd.currentIndexChanged.connect(lambda: self.ComboBox_changed("ComboBox_includedd"))
            # self.ui.ComboBox_notIncludedd.currentIndexChanged.connect(lambda: self.ComboBox_changed("ComboBox_notIncludedd"))
            # self.ui.ComboBox_notInclued.currentIndexChanged.connect(lambda: self.ComboBox_changed("ComboBox_notInclued"))

            # 刷新下拉框
            self.refreshCombox()

            self.userNameBefore = self.ui.LineEdit_Name.text()
            self.flagUpdateItemName = False

            # 适配分辨率
            from Physics.PhysicsCommand import AdaptiveDPIUtil
            new_x, new_y = AdaptiveDPIUtil.get_new_dpi(self.width(), self.height())
            self.resize(500, new_y)

        except:
            import traceback
            sayz("error:" + traceback.format_exc())

    def refreshCombox(self):
        '''
        每次加载窗口时都要重新加载下拉列表，以实现动态加载
        一般来说就是ComboBox_Shadow_list需要动态刷新
        '''
        ComboBox_Shadow_list = []
        ComboBox_area_list = []
        for i in range(self.ui.ComboBox_Shadow.count()):
            ComboBox_Shadow_list.append(self.ui.ComboBox_Shadow.itemText(i))
        for i in range(self.ui.ComboBox_notInclued.count()):
            ComboBox_area_list.append(self.ui.ComboBox_notInclued.itemText(i))
        EmmiterList = getLabelsByType(ObjectType.AreaConformal)
        VolumeListAll = getAllAreaLabel()
        for i in EmmiterList:
            if i not in ComboBox_Shadow_list:
                self.ui.ComboBox_Shadow.addItem(i)
        for i in VolumeListAll:
            if i not in ComboBox_area_list:
                self.ui.ComboBox_notInclued.addItem(i)
                self.ui.ComboBox_notIncludedd.addItem(i)
                self.ui.ComboBox_included.addItem(i)
                self.ui.ComboBox_includedd.addItem(i)

    def checkBox_particleType_clicked(self):
        self.ui.ComboBox_particleType.setEnabled(self.ui.checkBox_particleType.isChecked())

    def checkBox_generationRate_clicked(self):
        self.ui.spinBox_generationRate.setEnabled(self.ui.checkBox_generationRate.isChecked())

    def checkBox_transmittingInterval_clicked(self):
        self.ui.radioButton_random.setEnabled(self.ui.checkBox_transmittingInterval.isChecked())
        self.ui.radioButton_strictTiming.setEnabled(self.ui.checkBox_transmittingInterval.isChecked())
        self.ui.spinBox_timesStep.setEnabled(self.ui.checkBox_transmittingInterval.isChecked())

    def checkBox_surface_clicked(self):
        self.ui.radioButton_randomm.setEnabled(self.ui.checkBox_surface.isChecked())
        self.ui.radioButton_uniform.setEnabled(self.ui.checkBox_surface.isChecked())
        self.ui.radioButton_fixed.setEnabled(self.ui.checkBox_surface.isChecked())

    def checkBox_outSurface_clicked(self):
        self.ui.radioButton_randommm.setEnabled(self.ui.checkBox_outSurface.isChecked())
        self.ui.radioButton_alongOutsideFixed.setEnabled(self.ui.checkBox_outSurface.isChecked())
        self.ui.LineEdit_Dn.setEnabled(self.ui.checkBox_outSurface.isChecked())

    # def ComboBox_changed(self, which):
    #     if which == "ComboBox_Shadow":
    #         ObjectsTools.findObjByLabelWithoutOrderAndVisible(self.ui.ComboBox_Shadow.currentText())
    #     elif which == "ComboBox_included":
    #         ObjectsTools.findObjByLabelWithoutOrderAndVisible(self.ui.ComboBox_included.currentText())
    #         pass
    #     elif which == "ComboBox_includedd":
    #         ObjectsTools.findObjByLabelWithoutOrderAndVisible(self.ui.ComboBox_includedd.currentText())
    #         pass
    #     elif which == "ComboBox_notIncludedd":
    #         ObjectsTools.findObjByLabelWithoutOrderAndVisible(self.ui.ComboBox_notIncludedd.currentText())
    #         pass
    #     elif which == "ComboBox_notInclued":
    #         ObjectsTools.findObjByLabelWithoutOrderAndVisible(self.ui.ComboBox_notInclued.currentText())
    #         pass

    def loadDataFromObj(self):
        self.ui.LineEdit_Name.setText(self.obj.Name)
        self.ui.ComboBox_Shadow.setCurrentIndex(self.ui.ComboBox_Shadow.findText(str(self.obj.emitter)))
        self.ui.checkBox_particleType.setChecked(self.obj.isParticleType)
        self.ui.checkBox_generationRate.setChecked(self.obj.isGenerationRate)
        self.ui.spinBox_generationRate.setValue(self.obj.generationRate)
        self.ui.checkBox_transmittingInterval.setChecked(self.obj.isFiringInterval)
        self.ui.radioButton_random.setChecked(self.obj.isRandomDistribution)
        self.ui.radioButton_strictTiming.setChecked(self.obj.isStrictTiming)
        self.ui.spinBox_timesStep.setValue(self.obj.firingInterval)
        self.ui.checkBox_surface.setChecked(self.obj.isSurfaceDistribution)
        self.ui.radioButton_randomm.setChecked(self.obj.isRandom1)
        self.ui.radioButton_uniform.setChecked(self.obj.isBalance1)
        self.ui.radioButton_fixed.setChecked(self.obj.isImmobilization1)
        self.ui.checkBox_outSurface.setChecked(self.obj.isOuterSurfaceDistribution)
        self.ui.radioButton_randommm.setChecked(self.obj.isRandom2)
        self.ui.radioButton_alongOutsideFixed.setChecked(self.obj.isImmobilization2)
        self.ui.LineEdit_Dn.setText(self.obj.excursion)
        self.ui.ComboBox_notInclued.setCurrentIndex(self.ui.ComboBox_notInclued.findText(str(self.obj.launchArea1)))
        self.ui.ComboBox_notIncludedd.setCurrentIndex(self.ui.ComboBox_notIncludedd.findText(str(self.obj.launchArea2)))
        self.ui.ComboBox_included.setCurrentIndex(
            self.ui.ComboBox_included.findText(str(self.obj.launchOrthogonalProjectionRegin1)))
        self.ui.ComboBox_includedd.setCurrentIndex(
            self.ui.ComboBox_includedd.findText(str(self.obj.launchOrthogonalProjectionRegin2)))

    def getDataFromUi(self):
        self.obj.emitter = self.ui.ComboBox_Shadow.currentText()
        self.obj.isParticleType = self.ui.checkBox_particleType.isChecked()
        self.obj.particleType = self.ui.ComboBox_particleType.currentText()
        self.obj.isGenerationRate = self.ui.checkBox_generationRate.isChecked()
        self.obj.generationRate = self.ui.spinBox_generationRate.value()
        self.obj.isFiringInterval = self.ui.checkBox_transmittingInterval.isChecked()
        self.obj.isRandomDistribution = self.ui.radioButton_random.isChecked()
        self.obj.isStrictTiming = self.ui.radioButton_strictTiming.isChecked()
        self.obj.firingInterval = self.ui.spinBox_timesStep.value()
        self.obj.isSurfaceDistribution = self.ui.checkBox_surface.isChecked()
        self.obj.isRandom1 = self.ui.radioButton_randomm.isChecked()
        self.obj.isBalance1 = self.ui.radioButton_uniform.isChecked()
        self.obj.isImmobilization1 = self.ui.radioButton_fixed.isChecked()
        self.obj.isOuterSurfaceDistribution = self.ui.checkBox_outSurface.isChecked()
        self.obj.isRandom2 = self.ui.radioButton_randommm.isChecked()
        self.obj.isImmobilization2 = self.ui.radioButton_alongOutsideFixed.isChecked()
        self.obj.excursion = self.ui.LineEdit_Dn.text()
        self.obj.launchArea1 = self.ui.ComboBox_notInclued.currentText()
        self.obj.launchArea2 = self.ui.ComboBox_notIncludedd.currentText()
        self.obj.launchOrthogonalProjectionRegin1 = self.ui.ComboBox_included.currentText()
        self.obj.launchOrthogonalProjectionRegin2 = self.ui.ComboBox_includedd.currentText()


def getAllConformalLineLabel():
    """
    获取所有的conformal line
    """
    allObjsList = getAllObjects()
    resList = []
    for i in allObjsList:
        if hasattr(i, "Type") and i.Type == ObjectType.LineConformal:
            resList.append(i.Label)
    return resList


def getLabelsByType(obj_type):
    """
    根据输入的type，获取所有该类型的名字
    """
    allObjsList = getAllObjects()
    resList = []
    for i in allObjsList:
        if hasattr(i, "Type") and i.Type == obj_type:
            resList.append(i.Label)
    return resList


def getAllMaterial():
    allObjsList = getAllObjects()
    resList = []
    for i in allObjsList:
        if hasattr(i, "Type") and i.Type == ObjectType.NewMaterial:
            resList.append(i.Label)
    return resList


def getCoordinate():
    """
    获取坐标系相关信息
    """
    # from Modeling.Common.Tools import InputTools
    # length = InputTools.currentLengthUnits()
    # angle = InputTools.currentAngleUnits()
    coodinate = FreeCAD.ActiveDocument.CoordinateSystem
    if coodinate == u'Rectangular':
        unitList = ["X", "Y", "Z", "m", "m", "m"]
        # unitList = ["X", "Y", "Z", length, length, length]
    # elif coodinate == u'Polar':
        # unitList = ["R", u"θ", "Z", "m", "deg", "m"]
        # unitList = ["R", u"θ", "Z", length, angle, length]
    elif coodinate == u'Cylindrical':
        unitList = ["Z", "R", u"θ", "m", "m", "deg"]
        # unitList = ["Z", "R", u"θ", length, length, angle]
    return unitList
    # return ["X", "Y", "Z", "mm", "mm", "mm"]


def getValueOfAreaObjByLabel(objName):
    """
    objName:    物体的Label
    return     :list[]
    """
    obj = FreeCAD.ActiveDocument.getObjectsByLabel(objName)
    valueDict = {"point1.x": "",
                 "point1.y": "",
                 "point2.x": "",
                 "point2.y": "",
                 "normal": ""}
    if len(obj) == 0:
        sayz("没有obj被命名为" + objName)
    elif len(obj) == 1:
        # 注意obj在此处从list变为FreeCAD的Object对象
        obj = obj[0]
        # 获取点坐标及法相信息
        # conformal Line
        if hasattr(obj, "Type") and obj.Type == ObjectType.LineConformal:
            point1_x_value = str(obj.user_point1_x).replace(' ', '')
            point1_y_value = str(obj.user_point1_y).replace(' ', '')
            point2_x_value = str(obj.user_point2_x).replace(' ', '')
            point2_y_value = str(obj.user_point2_y).replace(' ', '')
            # expression_list = obj.ExpressionEngine
            # for i in expression_list:
            #     if i[0] == "x1_helper":
            #         point1_x_value = i[1].replace('Param.', '').replace(' ', '')
            #     elif i[0] == "y1_helper":
            #         point1_y_value = i[1].replace('Param.', '').replace(' ', '')
            #     elif i[0] == "x2_helper":
            #         point2_x_value = i[1].replace('Param.', '').replace(' ', '')
            #     elif i[0] == "y2_helper":
            #         point2_y_value = i[1].replace('Param.', '').replace(' ', '')
            valueDict["point1.x"] = point1_x_value
            valueDict["point1.y"] = point1_y_value
            valueDict["point2.x"] = point2_x_value
            valueDict["point2.y"] = point2_y_value
            if hasattr(obj, "normal"):
                valueDict["normal"] = obj.normal
        # conformal Area
        elif hasattr(obj, "Type") and obj.Type == ObjectType.AreaConformal:
            point1_x_value = str(obj.user_point1_x).replace(' ', '')
            point1_y_value = str(obj.user_point1_y).replace(' ', '')
            point2_x_value = str(obj.user_point2_x).replace(' ', '')
            point2_y_value = str(obj.user_point2_y).replace(' ', '')
            # expression_list = obj.ExpressionEngine
            # for i in expression_list:
            #     if i[0] == "Point1X":
            #         point1_x_value = i[1].replace('Param.', '').replace(' ', '')
            #     elif i[0] == "Point1Y":
            #         point1_y_value = i[1].replace('Param.', '').replace(' ', '')
            #     elif i[0] == "Point2X":
            #         point2_x_value = i[1].replace('Param.', '').replace(' ', '')
            #     elif i[0] == "Point2Y":
            #         point2_y_value = i[1].replace('Param.', '').replace(' ', '')
            valueDict["point1.x"] = point1_x_value
            valueDict["point1.y"] = point1_y_value
            valueDict["point2.x"] = point2_x_value
            valueDict["point2.y"] = point2_y_value
        # point
        elif hasattr(obj, "Type") and obj.Type == ObjectType.Point:
            point1_x_value = str(obj.user_point1_x).replace(' ', '')
            point1_y_value = str(obj.user_point1_y).replace(' ', '')
            # expression_list = obj.ExpressionEngine
            # for i in expression_list:
            #     if i[0] == "X":
            #         point1_x_value = i[1].replace('Param.', '').replace(' ', '')
            #     elif i[0] == "Y":
            #         point1_y_value = i[1].replace('Param.', '').replace(' ', '')
            valueDict["point1.x"] = point1_x_value
            valueDict["point1.y"] = point1_y_value
    else:
        sayz("出现了重名的Label，请检查Label赋值相关代码")

    return valueDict


def getAllAreaLabel():
    """
    获取所有的面
    """
    # AreaPolygonal = "AreaPolygonal"
    # AreaConformal = "AreaConformal"
    # AreaCircular = "AreaCircular"
    # Rectangle = "Rectangle"
    # RegularPolygon = "RegularPolygon"
    # Sector = "Sector"
    # Fillet = "Fillet"
    allObjsList = getAllObjects()
    resList = []
    AreaList = [ObjectType.AreaPolygonal, ObjectType.AreaConformal, ObjectType.Rectangle,ObjectType.AreaCircular,
                ObjectType.Sector, ObjectType.Fillet]
    for i in allObjsList:
        if hasattr(i, "Type"):
            if i.Type in AreaList:
                resList.append(i.Label)
    return resList


def getAllConformalAreaLabel():
    """
    获取所有的Conformal面
    """
    allObjsList = getAllObjects()
    resList = []
    for i in allObjsList:
        if hasattr(i, "Type") and i.Type == ObjectType.AreaConformal:
            resList.append(i.Label)
    return resList


def getCoordinateValueOfAreaObjByLabel(objName):
    """
    objName:    物体的Label
    return     :list[]
    """
    obj = FreeCAD.ActiveDocument.getObjectsByLabel(objName)
    valueDict = {"point1.x": "",
                 "point1.y": "",
                 "point2.x": "",
                 "point2.y": ""}
    if len(obj) == 1:
        # 注意obj在此处从list变为FreeCAD的Object对象
        obj = obj[0]
        # 获取点坐标及法相信息
        if hasattr(obj, "Type") and obj.Type == ObjectType.AreaConformal:
            point1_x_value = str(obj.user_point1_x).replace(' ', '')
            point1_y_value = str(obj.user_point1_y).replace(' ', '')
            point2_x_value = str(obj.user_point2_x).replace(' ', '')
            point2_y_value = str(obj.user_point2_y).replace(' ', '')
            # expression_list = obj.ExpressionEngine
            # for i in expression_list:
            #     if i[0] == "x1_helper":
            #         point1_x_value = i[1].replace('Param.', '').replace(' ', '')
            #     elif i[0] == "y1_helper":
            #         point1_y_value = i[1].replace('Param.', '').replace(' ', '')
            #     elif i[0] == "x2_helper":
            #         point2_x_value = i[1].replace('Param.', '').replace(' ', '')
            #     elif i[0] == "y2_helper":
            #         point2_y_value = i[1].replace('Param.', '').replace(' ', '')
            valueDict["point1.x"] = point1_x_value
            valueDict["point1.y"] = point1_y_value
            valueDict["point2.x"] = point2_x_value
            valueDict["point2.y"] = point2_y_value
            # if hasattr(obj, "normal"):
            #     valueDict["normal"] = obj.normal
    else:
        sayz("出现了重名的Label，请检查Label赋值相关代码")

    return valueDict


def defaultSettingForPoint(obj):
    """
    为点设置user_xxx的默认值
    :param obj:
    :return:
    """
    length = ExpressionTools.currentLengthUnits()
    obj.user_point1_x = str(obj.X.getValueAs(length)) + length
    obj.user_point1_y = str(obj.Y.getValueAs(length)) + length


def defaultSettingForCircle(obj):
    """
    为圆设置user_xxx的默认值
    :param obj:
    :return:
    """
    length = ExpressionTools.currentLengthUnits()
    obj.user_point1_x = str(obj.x_helper.getValueAs(length)) + length
    obj.user_point1_y = str(obj.y_helper.getValueAs(length)) + length


def defaultSettingForLine(obj):
    """
    为线设置user_xxx的默认值
    :param obj:
    :return:
    """
    length = ExpressionTools.currentLengthUnits()
    obj.user_point1_x = str(obj.x1_helper.getValueAs(length)) + length
    obj.user_point1_y = str(obj.y1_helper.getValueAs(length)) + length

    obj.user_point2_x = str(obj.x2_helper.getValueAs(length)) + length
    obj.user_point2_y = str(obj.y2_helper.getValueAs(length)) + length


def defaultSettingForArea(obj):
    """
    为线设置user_xxx的默认值
    :param obj:
    :return:
    """
    length = ExpressionTools.currentLengthUnits()
    obj.user_point1_x = str(obj.Point1X.getValueAs(length)) + length
    obj.user_point1_y = str(obj.Point1Y.getValueAs(length)) + length

    obj.user_point2_x = str(obj.Point2X.getValueAs(length)) + length
    obj.user_point2_y = str(obj.Point2Y.getValueAs(length)) + length

    
def defaultSettingForPolygonal(obj):
    """
    为多边形设置user_xxx的默认值
    :param obj:
    :return:
    """
    for i in range(len(obj.Points)):
        pos = getattr(obj, "helper_" + str(i))
        setattr(obj, "user_point" + str(i + 1) + "_x", str(pos[0]) + "m")
        setattr(obj, "user_point" + str(i + 1) + "_y", str(pos[1]) + "m")


def getPartValidModelObj():
    """
    获取当前文档所有有效的可以参与布尔运算的模型的列表
    返回的列表是根据Order排序的
    return type -> list
    """
    # 模型类型，随着项目的不断拓展，模型的类型可能会不断增加，新增类型如果需要参与布尔运算则添加到该列表
    target_list = ["Part::Part2DObject", "Part::FeaturePython"]
    model_list = []
    for i in target_list:
        model_list = model_list + FreeCAD.ActiveDocument.findObjects(i)
    # 挑选含有Type，Attribute, Order属性的obj，并根据obj的Order进行排序
    eligible_list = []  # 合格的obj列表
    for i in model_list:
        if hasattr(i, "IsAutoFillet") and i.IsAutoFillet == True:
            if hasattr(i, "Type") and hasattr(i, "Order") and hasattr(i, "Attribute"):
                if i.Attribute != Attribute.NotDefine:
                    eligible_list.append(i)
    # 对obj进行排序
    eligible_list.sort(key=getOrderOfObj)
    return eligible_list
    # begin
    # 时间：2020.11.24
    # 修改原因：添加一个循环使得该函数的返回值总是以一个conductor或者custom属性的体开头
    valid_num = 0
    for i in eligible_list:
        if i.Attribute == Attribute.Void:
            valid_num += 1
        else:
            break
    # end by lzg
    return eligible_list[valid_num:]
