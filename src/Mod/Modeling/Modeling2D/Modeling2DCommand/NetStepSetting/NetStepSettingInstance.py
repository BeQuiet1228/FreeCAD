# -*- coding:utf-8 -*-
# @Time: 2020/11/1 12:13
# @Author: lilei
# @File: NetStepSettingInstance.py
import FreeCAD
from Modeling.Modeling2D.Tools.Tools2D import ObjectType
from Modeling.Modeling2D.Tools import Tools2D


class NetStepSetting(object):
    def __init__(self):
        self.obj = FreeCAD.ActiveDocument.getObject("SIMUVOLUME")
        if self.obj is None:
            self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "SIMUVOLUME")
            self.__setProperty()

    def __setProperty(self):
        # 此处type通过一个枚举类来进行赋值
        self.obj.addProperty("App::PropertyString", "Type").Type = ObjectType.Simu
        # stringList是一个列表，类型箔片会有很多指定类型

        self.obj.addProperty("App::PropertyString", "point1_X").point1_X = "0mm"
        self.obj.addProperty("App::PropertyString", "point2_X").point2_X = "0mm"
        self.obj.addProperty("App::PropertyString", "stepSizeX").stepSizeX = "1mm"
        self.obj.addProperty("App::PropertyString", "point1_Y").point1_Y = "0mm"
        self.obj.addProperty("App::PropertyString", "point2_Y").point2_Y = "0mm"
        self.obj.addProperty("App::PropertyString", "stepSizeY").stepSizeY = "1mm"
        self.obj.addProperty("App::PropertyBool", "isStartUsing").isStartUsing = False


def getObject():
    """
    创建obj并添加与Foil相关的属性，然后返回obj
    """
    netStepSettingIns = NetStepSetting()
    return netStepSettingIns.obj
