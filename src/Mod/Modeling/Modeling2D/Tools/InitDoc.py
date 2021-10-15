# -*- coding: utf-8 -*-
import FreeCAD
import FreeCADGui

from File.FileCommand.M2dFile import M2DContainer
from Modeling.Common.Tools import ObjectsTools, CoordinateSystemTools
# from Modeling.Common.Tools.DocumentTools import DocumentObservers, TransparencyObserver, NeedsRecomputeObserver

# 该文件负责二维建模工作台打开时，整个工程的初始化工作
from Modeling.Modeling2D.Modeling2DCommand.DataExportSetting import DataExportSettingInstance
from Modeling.Modeling2D.Modeling2DCommand.ModelInfo import ModelInfoInstance
from Modeling.Modeling2D.Modeling2DCommand.NetStepSetting import NetStepSettingInstance
from Modeling.Modeling2D.Modeling2DCommand.RunProcessingOptions import RunProcessingOptionsInstance
from Modeling.Modeling2D.Modeling2DCommand.TimeDomainSetting import TimeDomainSettingInstance
# from Modeling.Modeling2D.Modeling2DCommand.FiledSetting import FiledSettingInstance
# from Modeling.Modeling2D.Modeling2DCommand.DefTimer import DefTimerInstance
from Modeling.Modeling2D.Tools import Tools2D
from Modeling.Modeling2D.Tools.Tools2D import ObjectType


def otherDocInit():
    """
    文件初始化时会调用该函数
    """
    doc = FreeCAD.ActiveDocument
    initDocument(doc)
    initParamObj(doc)
    FreeCADGui.doCommand("from Modeling.Common.Tools import DocumentTools")
    # FreeCAD.addDocumentObserver(NeedsRecomputeObserver())


def createInitGroup(groupName, groupLabel):
    """
    在树形结构中创建文件分组\n
    groupName : internal name of this object\n
    groupLabel: user name of this object
    """
    g = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroup", groupName)
    g.Label = groupLabel
    return g


def initGroup():
    """
    初始化树结构，为树结构设置一级二级目录
    """
    # 一级目录
    modelG = createInitGroup("Modeling2D", "模型")
    boundG = createInitGroup("BoundarySetting", "边界设置")
    obsG = createInitGroup("ObservationSetting", "观测设置")
    projectG = createInitGroup("ProjectSetting", "工程设置")

    # 模型二级目录
    model_list = []
    model_list.append(createInitGroup("PointG", "点"))
    model_list.append(createInitGroup("LineG", "线"))
    model_list.append(createInitGroup("AreaG", "面"))
    model_list.append(createInitGroup("AnnotationG", "注释"))
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
    obs_list.append(createInitGroup("DefaultTimer", "默认定时器"))
    obs_list.append(createInitGroup("EquivalentObs", "等值观测"))
    obs_list.append(createInitGroup("TimeObs", "时间观测"))
    obs_list.append(createInitGroup("VectorObs", "矢量观测"))
    obs_list.append(createInitGroup("ParticleObs", "粒子观测"))
    obs_list.append(createInitGroup("ControlObs", "控制观测"))
    obs_list.append(createInitGroup("AreaObs", "空间观测"))
    obs_list.append(createInitGroup("Timer", "定时器"))

    # 将二级目录添加到一级目录中
    for i in model_list:
        modelG.addObject(i)
    for i in bound_list:
        boundG.addObject(i)
    for i in obs_list:
        obsG.addObject(i)


def addObjectToGroup(obj):
    """
    根据obj的类型添加到对应的分组中
    """
    # Tools2D.sayz(obj.Type)
    # 模型相关的分组
    if not hasattr(obj, "Type"):
        return

    if obj.Type == ObjectType.Point:
        addObjectToGroup_helper(obj, 'PointG', '点')
    elif obj.Type == ObjectType.Line or obj.Type == ObjectType.LineConformal:
        addObjectToGroup_helper(obj, "LineG", "线")
    elif obj.Type == ObjectType.AreaConformal \
            or obj.Type == ObjectType.AreaPolygonal \
            or obj.Type == ObjectType.AreaCircular:
        addObjectToGroup_helper(obj, "AreaG", "面")
    elif obj.Type == ObjectType.Rectangle:
        addObjectToGroup_helper(obj, "AreaG", "面")
    elif obj.Type == ObjectType.RegularPolygon:
        addObjectToGroup_helper(obj, "AreaG", "面")
    elif obj.Type == ObjectType.Sector:
        addObjectToGroup_helper(obj, "AreaG", "面")
    elif obj.Type == ObjectType.Fillet:
        addObjectToGroup_helper(obj, "AreaG", "面")
    elif obj.Type == ObjectType.AreaFunction:
        addObjectToGroup_helper(obj, "AreaG", "面")
    # elif obj.Type == ObjectType.Annotation:
    #     addObjectToGroup_helper(obj, "AnnotationG", "注释")
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
    elif obj.Type == ObjectType.DefaultTimer:
        addObjectToGroup_helper(obj, "DefaultTimer", "默认定时器")
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
    elif obj.Type == ObjectType.Timer:
        addObjectToGroup_helper(obj, "Timer", "定时器")
    # 工程设置
    elif obj.Type == ObjectType.Info:
        addObjectToGroup_helper(obj, "ProjectSetting", "工程设置")
    elif obj.Type == ObjectType.Simu:
        addObjectToGroup_helper(obj, "ProjectSetting", "工程设置")
    elif obj.Type == ObjectType.TimeDomain:
        addObjectToGroup_helper(obj, "ProjectSetting", "工程设置")
    elif obj.Type == ObjectType.DataProcess:
        addObjectToGroup_helper(obj, "ProjectSetting", "工程设置")
    elif obj.Type == ObjectType.RunOptions:
        addObjectToGroup_helper(obj, "ProjectSetting", "工程设置")
    elif obj.Type == ObjectType.FieldSetting:
        addObjectToGroup_helper(obj, "ProjectSetting", "工程设置")
    # 网格设置
    elif obj.Type == ObjectType.DiyGrid:
        addObjectToGroup_helper(obj, "ProjectSetting", "工程设置")


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


def initDocument(doc):
    """
    author:   @LZG
    function: 0、新增结果对象；
              1、为文档增加监听；
              2、将默认的json加到comment中；
              3、添加默认定时器
    note: 模仿伏彪的代码编写的
    """
    # 新建文档时，增加一个空的三维对象，之后的布尔求交都在这个对象上进行
    obj = ObjectsTools.initResultIbj(doc)
    # 将ResultShape设置为Flat Lines的状态
    FreeCAD.ActiveDocument.getObject("ResultShape").ViewObject.DisplayMode = u"Flat Lines"

    # 监听
    FreeCAD.addDocumentObserver(DocumentObservers())
    # FreeCAD.addDocumentObserver(TransparencyObserver())

    # 测试
    # FreeCAD.addDocumentObserver(NeedsRecomputeObserver())

    # 添加默认定时器
    # init TimerDef


    # ObjectDict["TimerDef1"] = DefaultTimerMain("new", "TimerDef1")
    # ObjectDict["TimerDef1"].initToDoc()
    # end
    # 初始化2D建模平台下的分组
    initGroup()
    addDefaultObjects()
    FreeCADGui.runCommand("CreateM2D")
    # 以下为测试用例
    FreeCADGui.runCommand("CreateNetStepSetting")
    FreeCADGui.runCommand("CreateTimeDomainSetting")
    FreeCADGui.runCommand("SetGrid")


def addDefaultObjects():
    """
    当一个新工程打开时，有些obj需要被初始化
    """
    # 网格步长设定
    NetStepSettingInstance.getObject()
    # 模型信息
    ModelInfoInstance.getObject()
    # 时域计算
    TimeDomainSettingInstance.getObject()
    # 场及函数定义
    # FiledSettingInstance.getObject()
    # 数据导出
    DataExportSettingInstance.getObject()
    # 运行处理
    RunProcessingOptionsInstance.getObject()
    # 由于导包的顺序问题，在该包运行的时候，DefTimer还未被导入
    from Modeling.Modeling2D.Modeling2DCommand.DefTimer import DefTimerInstance
    # 默认定时器
    DefTimerInstance.getObject()
    # 新建工程时显示网格
    from Modeling.Modeling2D import Modeling2DCommand
    Modeling2DCommand.Grid.GridCommand.showGrid()


# 初始化参量对象，这个不能直接加载initDocument中，因为解析时，也会执行上面的函数，报错
def initParamObj(doc):
    if doc.CoordinateSystem == CoordinateSystemTools.CoordinateType.Rectangular:
        ObjectsTools.setDX1DX2DX3("1mm", "1mm", "1mm")
    elif doc.CoordinateSystem == CoordinateSystemTools.CoordinateType.Polar:
        ObjectsTools.setDX1DX2DX3("1mm", "30deg", "1mm")
    elif doc.CoordinateSystem == CoordinateSystemTools.CoordinateType.Cylindrical:
        ObjectsTools.setDX1DX2DX3("1mm", "1mm", "30deg")


# 事件监听器
# 为2D建模工作台创建一个事件监听器
##########################定义一个监测类，当对象删除或者创建时执行相应的动作#########
class DocumentObservers(object):
    def __init__(self):
        pass

    def slotDeletedObject(self, obj):
        Tools2D.sayz("\n" + str(obj.Label) + "被删除")
        # 经测试，撤销恢复和手动删除都会触发这个函数
        # 为所有的物体重新编号
        # if Tools2D.hasThePropertyByObj(obj, "Order"):
        #     for index in range(obj.Order + 1, ObjectsTools.getNumOfObjects(FreeCAD.ActiveDocument.Name)):
        #         objs = ObjectsTools.getListOfOrderedObjects(FreeCAD.ActiveDocument.Name)
        #         objs[index].Order = objs[index].Order - 1

    def slotChangedObject(self, obj, prop):
        # Tools2D.sayz(str(obj.Label) + "的属性发生改变")
        # Tools2D.sayz(str(prop) + "\tvalue:\t" + str(getattr(obj, prop)) + "\t发生改变")
        # Type发生改变，只能是新增，不会一直变
        if prop == "Type":
            if obj.getParentGroup() is None:
                addObjectToGroup(obj)
                pass
        # 更新m2d信息
        # M2DContainer.setM2DToInterface()

        import json
        FreeCAD.ActiveDocument.License = json.dumps('True')
        # 暂时不对order进行处理
        # 为了解决复制对象时，Order跟随复制
        # if ObjectsTools.hasThePropertyByObj(obj, "Order") and prop == "Type":
        #     if ObjectsTools.hasThePropertyByObj(obj, "Order"):
        #         numOfObjects = len(ObjectsTools.getAllObjectszofThisDoc(FreeCAD.ActiveDocument.Name))
        #         if obj.Order < numOfObjects:
        #             # 更新Order
        #             obj.Order = numOfObjects
        #             pass

    # 文档关闭，关闭物理设置与任务控制面板
    def slotDeletedDocument(self, doc):
        # 移除所有的监听
        FreeCAD.removeAllDocumentObserver()
        import os
        if os.path.exists(FreeCAD.clientUserDir()):
            pass
        try:
            import Visualization.VisualizationCommand.VisualizationTree
            import Visualization.VisualizationCommand.VisualizationFigTree
            # 清除保存的plot对象
            Visualization.VisualizationCommand.VisualizationTree.cloePlotTree()
            Visualization.VisualizationCommand.VisualizationFigTree.showfigTree()
        except:
            FreeCAD.Console.PrintError("Wrong in DocumentTool.slotDeletedDocument\n")

    # # 新建Object
    # def slotCreatedObject(self, obj):
    #     pass
