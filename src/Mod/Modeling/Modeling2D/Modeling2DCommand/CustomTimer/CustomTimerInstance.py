# -*- coding: utf-8 -*-
import FreeCAD
from Modeling.Modeling2D.Tools.Tools2D import ObjectType


class CustomTimer(object):
    def __init__(self):
        # self.obj = None
        FreeCAD.ActiveDocument.openTransaction("CreateCustomTimer")
        self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "CustomTimer")
        FreeCAD.ActiveDocument.commitTransaction()
        self.__setProperty(self.obj)

    def __setProperty(self, obj):
        # self.obj.addProperty("App::PropertyString","objName").name = "Foil"
        # 此处type通过一个枚举类来进行赋值
        self.obj.addProperty("App::PropertyString", "Type").Type = ObjectType.Timer
        # 类型有多种，用StringList
        self.obj.addProperty("App::PropertyString", "defTimerType").defTimerType = "周期型"
        self.obj.addProperty("App::PropertyBool", "isTimeSteps").isTimeSteps = True
        self.obj.addProperty("App::PropertyBool", "isSimulationSteps").isSimulationSteps = False
        self.obj.addProperty("App::PropertyString", "startTime").startTime = "10"
        self.obj.addProperty("App::PropertyString", "endTime").endTime = "100000"
        self.obj.addProperty("App::PropertyString", "timeCycle").timeCycle = "5000"
        self.obj.addProperty("App::PropertyString", "discreteTime").discreteTime = "10 12 15 24 85 168 468"


def getObject():
    """
    创建obj并添加与DefTimer相关的属性，然后返回obj
    """
    customTimerIns = CustomTimer()
    return customTimerIns.obj
