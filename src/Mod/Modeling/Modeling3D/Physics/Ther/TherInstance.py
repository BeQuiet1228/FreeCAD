#-*- coding: utf-8 -*-
import FreeCAD
from Modeling.Modeling2D.Tools.Tools2D import ObjectType
from Modeling.Modeling2D.Tools import Tools2D


class Ther(object):
    def __init__(self):
        self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "ther")
        self.__setProperty(self.obj)

    def __setProperty(self, obj):

        # 此处type通过一个枚举类来进行赋值
        self.obj.addProperty("App::PropertyString", "Type").Type = ObjectType.THER
        # stringList是一个列表，类型箔片会有很多指定类型
        self.obj.addProperty("App::PropertyString", "emitter").emitter = "未指定"

        self.obj.addProperty("App::PropertyString", "workingFunctionWF").workingFunctionWF = "0.0"
        self.obj.addProperty("App::PropertyString", "workingTemperatureTP").workingTemperatureTP = "0.0"

        # 发射选项
        Tools2D.addLaunchOptionsCommonProperty(obj)


def getObject():
    """
    创建obj并添加与Foil相关的属性，然后返回obj
    """
    therIns = Ther()
    return therIns.obj
