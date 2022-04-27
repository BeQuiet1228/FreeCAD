# -*- coding: utf-8 -*-
import FreeCAD
from Model3D.Tools import ObjectTools, InitDoc3D


class DefTimer(object):
    def __init__(self):
        self.obj = FreeCAD.ActiveDocument.getObject("DefTimer")
        if self.obj is None:
            self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "DefTimer")
            self.__setProperty()
        InitDoc3D.addObjectToGroup_helper(self.obj, "DefaultTimer", "默认定时器")

    def __setProperty(self):
        # self.obj.addProperty("App::PropertyString","objName").name = "Foil"
        # 此处type通过一个枚举类来进行赋值
        self.obj.addProperty("App::PropertyString", "Type").Type = ObjectTools.ObjectType.DefaultTimer
        # 类型有多种，用StringList
        self.obj.addProperty("App::PropertyString", "defTimerType").defTimerType = "周期型"
        self.obj.addProperty("App::PropertyBool", "isTimeSteps").isTimeSteps = True
        self.obj.addProperty("App::PropertyBool", "isSimulationSteps").isSimulationSteps = False
        self.obj.addProperty("App::PropertyString", "startTime").startTime = "10"
        self.obj.addProperty("App::PropertyString", "endTime").endTime = "100000"
        self.obj.addProperty("App::PropertyString", "timeCycle").timeCycle = "5000"
        self.obj.addProperty("App::PropertyString", "discreteTime").discreteTime = "10 12 15 24 85 168 468"
        if not hasattr(self.obj, "Observation"):
            self.obj.addProperty("App::PropertyString", "Observation")


def getObject():
    """
    创建obj并添加与DefTimer相关的属性，然后返回obj
    """
    defTimerIns = DefTimer()
    return defTimerIns.obj
