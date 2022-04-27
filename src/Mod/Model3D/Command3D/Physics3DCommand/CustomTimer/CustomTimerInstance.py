# -*- coding: utf-8 -*-
import FreeCAD
from Model3D.Tools import ObjectTools, InitDoc3D


class CustomTimer(object):
    def __init__(self):
        # self.obj = None
        FreeCAD.ActiveDocument.openTransaction("CreateCustomTimer_3D")
        self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "Timer")
        self.__setProperty(self.obj)
        InitDoc3D.addObjectToGroup_helper(self.obj, "CustomTimer", "新建定时器")
        FreeCAD.ActiveDocument.commitTransaction()

    def __setProperty(self, obj):
        # 此处type通过一个枚举类来进行赋值
        self.obj.addProperty("App::PropertyString", "Type").Type = ObjectTools.ObjectType.CustomTimer
        self.obj.addProperty("App::PropertyString", "CustomTimerType").CustomTimerType = "周期型"
        self.obj.addProperty("App::PropertyBool", "isTimerStep").isTimerStep = True
        self.obj.addProperty("App::PropertyBool", "isTimerSimulate").isTimerSimulate = False
        self.obj.addProperty("App::PropertyString", "startTime").startTime = "10"
        self.obj.addProperty("App::PropertyString", "endTime").endTime = "1000000"
        self.obj.addProperty("App::PropertyString", "period").period = "5000"
        self.obj.addProperty("App::PropertyString", "DiscreteTime").DiscreteTime = "10 12 15 24 85 168 468"
        if not hasattr(obj, "Observation"):
            self.obj.addProperty("App::PropertyString", "Observation")


def getObject():
    """
    创建obj并添加与CustomTimer相关的属性，然后返回obj
    """
    CustomTimerIns = CustomTimer()
    return CustomTimerIns.obj