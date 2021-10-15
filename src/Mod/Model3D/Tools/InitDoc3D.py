# -*- coding: utf-8 -*-
import FreeCAD
import FreeCADGui
from Model3D.Tools import ObjectTools, Tools3D
from Model3D.Tools.ObjectTools import ObjectType


def otherDocInit():
    """
    文件初始化时会调用该函数
    """
    doc = FreeCAD.ActiveDocument
    initDocument(doc)


def createInitGroup(groupName, groupLabel):
    """
    在树形结构中创建文件分组\n
    groupName : internal name of this object\n
    groupLabel: user name of this object
    """
    g = FreeCAD.ActiveDocument.getObject(groupName)
    if g:
        pass
    else:
        g = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroup", groupName)
        g.Label = groupLabel
    return g


def initGroup():
    """
    初始化树结构，为树结构设置一级二级目录
    """
    # 一级目录
    modelG = createInitGroup("Modeling3D", "模型")
    boundG = createInitGroup("BoundarySetting", "边界设置")
    obsG = createInitGroup("ObservationSetting", "观测设置")
    projectG = createInitGroup("ProjectSetting", "工程设置")

    # 模型二级目录
    model_list = []
    model_list.append(createInitGroup("PointG", "点"))
    model_list.append(createInitGroup("LineG", "线"))
    model_list.append(createInitGroup("AreaG", "面"))
    model_list.append(createInitGroup("Conformal", "正投影体"))
    model_list.append(createInitGroup("Annular", "环形体"))
    model_list.append(createInitGroup("Cylinder", "圆柱体"))
    model_list.append(createInitGroup("SpecialCone", "圆锥体"))
    model_list.append(createInitGroup("Spherical", "球体"))
    # model_list.append(createInitGroup("Annular_Section", "环形区域体"))
    # model_list.append(createInitGroup("Extruded", "挤出体"))
    # model_list.append(createInitGroup("Function", "函数体"))
    # model_list.append(createInitGroup("Revolution", "旋转体"))
    # model_list.append(createInitGroup("Helical", "螺旋体"))
    # model_list.append(createInitGroup("Parallelepipedal", "平行六面体"))
    # model_list.append(createInitGroup("Pyramid", "金字塔体"))
    # model_list.append(createInitGroup("Rhombus", "菱形体"))
    # model_list.append(createInitGroup("Tetrahedron", "四面体"))
    # model_list.append(createInitGroup("Toroidal_Section", "半圆环体"))
    # model_list.append(createInitGroup("Wedge", "楔形体"))
    # model_list.append(createInitGroup("Array", "阵列体"))
    # model_list.append(createInitGroup("Draft", "草图"))

    # 边界设置二级目录
    bound_list = []
    bound_list.append(createInitGroup("WaveguidePort", "波导端口"))
    bound_list.append(createInitGroup("Absorbing", "吸收边界"))
    bound_list.append(createInitGroup("Symmetry", "对称边界"))
    bound_list.append(createInitGroup("Launch", "发射处理"))
    bound_list.append(createInitGroup("NewParticleG", "新粒子"))
    bound_list.append(createInitGroup("NewMaterialG", "新材料"))
    bound_list.append(createInitGroup("Mark", "Mark"))
    bound_list.append(createInitGroup("OtherModel", "其他模型"))
    # 观测设置二级目录
    obs_list = []
    obs_list.append(createInitGroup("EquivalentObs", "等值观测"))
    obs_list.append(createInitGroup("TimeObs", "时间观测"))
    obs_list.append(createInitGroup("VectorObs", "矢量观测"))
    obs_list.append(createInitGroup("ParticleObs", "粒子观测"))
    # obs_list.append(createInitGroup("ControlObs", "控制观测"))
    obs_list.append(createInitGroup("AreaObs", "空间观测"))
    obs_list.append(createInitGroup("DefaultTimer", "默认定时器"))
    obs_list.append(createInitGroup("CustomTimer", "新建定时器"))
    # 工程设置二级目录
    project_list = []
    project_list.append(createInitGroup("Info", "模型信息输入"))
    project_list.append(createInitGroup("Simu", "工作区间设置"))
    project_list.append(createInitGroup("TimeDomain", "时域计算设置"))
    project_list.append(createInitGroup("DataProcess", "数据导出设定"))
    project_list.append(createInitGroup("RunOptions", "运行处理选项"))
    project_list.append(createInitGroup("FieldSetting", "场及函数定义"))

    # 将二级目录添加到一级目录中
    for i in model_list:
        modelG.addObject(i)
    for i in bound_list:
        boundG.addObject(i)
    for i in obs_list:
        obsG.addObject(i)
    for i in project_list:
        projectG.addObject(i)


def addObjectToGroup_helper(obj, groupName, groupLabel):
    """
    将obj添加到对应分组的辅助函数，将obj真正添加到分组中\n
    如果不存在这个分组，则创建一个分组
    """
    group = FreeCAD.ActiveDocument.getObject(groupName)
    if group:
        group.addObject(obj)
    else:
        group = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroup", groupName)
        group.Label = groupLabel
        group.addObject(obj)
    #  放在模型文件夹
    if hasattr(obj, "Order"):
        modelG = createInitGroup("Modeling3D", "模型")
        modelG.addObject(group)
    # 放在边界设置文件夹
    if hasattr(obj, "Boundary"):
        modelG = createInitGroup("BoundarySetting", "边界设置")
        modelG.addObject(group)
    # 放在观测设置文件夹
    if hasattr(obj, "Observation"):
        modelG = createInitGroup("ObservationSetting", "观测设置")
        modelG.addObject(group)
    # 放在工程设置文件夹
    if hasattr(obj, "Project"):
        modelG = createInitGroup("ProjectSetting", "工程设置")
        modelG.addObject(group)


def initDocument(doc):
    """
    author:   @WZG
    function: 0、新增结果对象；
              1、为文档增加监听；
              2、将默认的json加到comment中；
              3、添加默认定时器
    note: 模仿伏彪的代码编写的
    """
    # 新建文档时，增加一个空的三维对象，之后的布尔求交都在这个对象上进行
    obj = ObjectTools.initResultIbj(doc)
    # 将ResultShape设置为Flat Lines的状态
    FreeCAD.ActiveDocument.getObject("ResultShape").ViewObject.DisplayMode = u"Flat Lines"

    # 监听
    FreeCAD.addDocumentObserver(DocumentObservers())

    # 初始化2D建模平台下的分组
    initGroup()
    addDefaultObjects()
    FreeCADGui.runCommand("CreateM3D_new")
    # 进入工作台初始对话框
    FreeCADGui.runCommand("NetStepSetting_3D")
    FreeCADGui.runCommand("TimeDomainSetting_3D")


def addDefaultObjects():
    """
    当一个新工程打开时，有些obj需要被初始化
    """
    # 网格步长设定
    from Model3D.Command3D.Physics3DCommand.NetStepSetting import NetStepSettingInstance
    NetStepSettingInstance.getObject()
    # 模型信息输入
    from Model3D.Command3D.Physics3DCommand.ModelingInfo import ModelingInfoInstance
    ModelingInfoInstance.getObject()
    # 时域计算
    from Model3D.Command3D.Physics3DCommand.TimeDomainSetting import TimeDomainSettingInstance
    TimeDomainSettingInstance.getObject()
    # 数据导出
    from Model3D.Command3D.Physics3DCommand.DataProcessingSetting import DataProcessingSettingInstance
    DataProcessingSettingInstance.getObject()
    # 运行处理
    from Model3D.Command3D.Physics3DCommand.RunOptions import RunOptionsInstance
    RunOptionsInstance.getObject()
    # 默认定时器
    from Model3D.Command3D.Physics3DCommand.DefTimer import DefTimerInstance
    DefTimerInstance.getObject()


def addObjectToGroup(obj):
    """
    根据obj的类型添加到对应的分组中
    """
    # 模型相关的分组
    if not hasattr(obj, "Type"):
        return

    if obj.Type == ObjectType.Point:
        addObjectToGroup_helper(obj, 'PointG', '点')
    elif obj.Type == ObjectType.Line_Conformal or obj.Type == ObjectType.Line_Oblique:
        addObjectToGroup_helper(obj, "LineG", "线")
    elif obj.Type == ObjectType.Area_Conformal \
            or obj.Type == ObjectType.Area_Rectangular \
            or obj.Type == ObjectType.Area_Polygonal\
            or obj.Type == ObjectType.Area_Function:
        addObjectToGroup_helper(obj, "AreaG", "面")
    elif obj.Type == ObjectType.Vol_Annular:
        addObjectToGroup_helper(obj, "Annular", "环形体")
    elif obj.Type == ObjectType.Vol_Annular_Section:
        addObjectToGroup_helper(obj, "Annular_Section", "环形区域体")
    elif obj.Type == ObjectType.Vol_Conformal:
        addObjectToGroup_helper(obj, "Conformal", "正投影体")
    elif obj.Type == ObjectType.Vol_Cylinder:
        addObjectToGroup_helper(obj, "Cylinder", "圆柱体")
    elif obj.Type == ObjectType.Vol_Extruded:
        addObjectToGroup_helper(obj, "Extruded", "挤出体")
    elif obj.Type == ObjectType.Vol_Function:
        addObjectToGroup_helper(obj, "Function", "函数体")
    elif obj.Type == ObjectType.Vol_Revolution:
        addObjectToGroup_helper(obj, "Revolution", "旋转体")
    elif obj.Type == ObjectType.Vol_Helical:
        addObjectToGroup_helper(obj, "Helical", "螺旋体")
    elif obj.Type == ObjectType.Vol_Parallelepipedal:
        addObjectToGroup_helper(obj, "Parallelepipedal", "平行六面体")
    elif obj.Type == ObjectType.Vol_Pyramid:
        addObjectToGroup_helper(obj, "Pyramid", "金字塔体")
    elif obj.Type == ObjectType.Vol_Rhombus:
        addObjectToGroup_helper(obj, "Rhombus", "菱形体")
    elif obj.Type == ObjectType.Vol_SpecialCone:
        addObjectToGroup_helper(obj, "SpecialCone", "圆锥体")
    elif obj.Type == ObjectType.Vol_Spherical:
        addObjectToGroup_helper(obj, "Spherical", "球体")
    elif obj.Type == ObjectType.Vol_Tetrahedron:
        addObjectToGroup_helper(obj, "Tetrahedron", "四面体")
    elif obj.Type == ObjectType.Vol_Toroidal_Section:
        addObjectToGroup_helper(obj, "Toroidal_Section", "半圆环体")
    elif obj.Type == ObjectType.Vol_Wedge:
        addObjectToGroup_helper(obj, "Wedge", "楔形体")
    elif obj.Type == ObjectType.Vol_Array or obj.Type == ObjectType.Vol_ParamArray:
        addObjectToGroup_helper(obj, "Array", "阵列体")
    elif obj.Type == ObjectType.Vol_Draft_Extrude or obj.Type == ObjectType.Vol_Draft_Revolution:
        addObjectToGroup_helper(obj, "Draft", "草图")

    # 边界设置相关的分组
    elif obj.Type == ObjectType.FOIL or obj.Type == ObjectType.SOLE \
            or obj.Type == ObjectType.IND or obj.Type == ObjectType.DRIV:
        addObjectToGroup_helper(obj, "OtherModel", "其他模型")
    elif obj.Type == ObjectType.NewMaterial:
        addObjectToGroup_helper(obj, "NewMaterialG", "新材料")
    elif obj.Type == ObjectType.PORT:
        addObjectToGroup_helper(obj, "WaveguidePort", "波导端口")
    elif obj.Type == ObjectType.FREE:
        addObjectToGroup_helper(obj, "Absorbing", "吸收边界")
    elif obj.Type == ObjectType.SYMT:
        addObjectToGroup_helper(obj, "Symmetry", "对称边界")

    # 发射处理相关分组
    elif obj.Type == ObjectType.BEAM or obj.Type == ObjectType.EXPS \
            or obj.Type == ObjectType.GYRO or obj.Type == ObjectType.POPU \
            or obj.Type == ObjectType.FELD or obj.Type == ObjectType.THER \
            or obj.Type == ObjectType.SECD or obj.Type == ObjectType.IONI:
        addObjectToGroup_helper(obj, "Launch", "发射处理")
    elif obj.Type == ObjectType.NewParticle:
        addObjectToGroup_helper(obj, "NewParticleG", "新粒子")
    elif obj.Type == ObjectType.MARK:
        addObjectToGroup_helper(obj, "Mark", "Mark")

    # 观测设置相关分组
    elif obj.Type == ObjectType.CNTR:
        addObjectToGroup_helper(obj, "EquivalentObs", "等值观测")
    elif obj.Type == ObjectType.Observe:
        addObjectToGroup_helper(obj, "TimeObs", "时间观测")
    elif obj.Type == ObjectType.Vector:
        addObjectToGroup_helper(obj, "VectorObs", "矢量观测")
    elif obj.Type == ObjectType.PhasSpace:
        addObjectToGroup_helper(obj, "ParticleObs", "粒子观测")
    elif obj.Type == ObjectType.AreaRan:
        addObjectToGroup_helper(obj, "AreaObs", "空间观测")
    elif obj.Type == ObjectType.DefaultTimer:
        addObjectToGroup_helper(obj, "DefaultTimer", "默认定时器")
    elif obj.Type == ObjectType.CustomTimer:
        addObjectToGroup_helper(obj, "CustomTimer", "新建定时器")

    # 工程设置分组
    elif obj.Type == ObjectType.Info:
        addObjectToGroup_helper(obj, "Info", "模型信息输入")
    elif obj.Type == ObjectType.Simu:
        addObjectToGroup_helper(obj, "Simu", "工作区间设置")
    elif obj.Type == ObjectType.TimeDomain:
        addObjectToGroup_helper(obj, "TimeDomain", "时域计算设置")
    elif obj.Type == ObjectType.DataProcess:
        addObjectToGroup_helper(obj, "DataProcess", "数据导出设定")
    elif obj.Type == ObjectType.RunOptions:
        addObjectToGroup_helper(obj, "RunOptions", "运行处理选项")
    elif obj.Type == ObjectType.FieldSetting:
        addObjectToGroup_helper(obj, "FieldSetting", "场及函数定义")


# 事件监听器
# 为3D建模工作台创建一个事件监听器
##########################定义一个监测类，当对象删除或者创建时执行相应的动作#########
class DocumentObservers(object):
    def __init__(self):
        pass

    def slotDeletedObject(self, obj):
        Tools3D.sayz("\n" + str(obj.Label) + "被删除")
        if hasattr(obj, "Type") and obj.Type == ObjectTools.ObjectType.Vol_Array and \
                obj.isSetEnabled and hasattr(obj, "BaseType"):
            FreeCAD.ActiveDocument.removeObject(obj.BaseType)
        # 把obj删除同时把他的分组删除
        # obj_list = ["Vol_Toroidal_Section", "Vol_Parallelepipedal", "Vol_Annular_Section", "Vol_Function",
        #             "Vol_Pyramid", "Vol_Wedge", "Vol_Rhombus", "Vol_Extruded", "Vol_Tetrahedron", "Vol_Helical",
        #             "Vol_Revolution", "Vol_Draft_Revolution", "Vol_Draft_Revolution", "Vol_Array", "Vol_ParamArray"]
        # if len(obj.InList) and hasattr(obj.InList[0], "Group") and len(obj.InList[0].Group) == 1 and obj.Type in obj_list:
        #     FreeCAD.ActiveDocument.removeObject(obj.InList[0].Name)

    def slotChangedObject(self, obj, prop):
        if prop == "Type":
            if obj.getParentGroup() is None:
                addObjectToGroup(obj)
                pass

        import json
        FreeCAD.ActiveDocument.License = json.dumps('True')

    # 文档关闭，关闭物理设置与任务控制面板
    def slotDeletedDocument(self, doc):
        # 移除所有的监听
        FreeCAD.removeAllDocumentObserver()
        import os
        if os.path.exists(FreeCAD.clientUserDir()):
            pass
        # try:
        #     import Visualization.VisualizationCommand.VisualizationTree
        #     import Visualization.VisualizationCommand.VisualizationFigTree
        #     # 清除保存的plot对象
        #     Visualization.VisualizationCommand.VisualizationTree.cloePlotTree()
        #     Visualization.VisualizationCommand.VisualizationFigTree.showfigTree()
        # except:
        #     FreeCAD.Console.PrintError("Wrong in DocumentTool.slotDeletedDocument\n")

