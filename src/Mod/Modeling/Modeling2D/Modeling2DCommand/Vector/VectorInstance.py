# -*- coding: utf-8 -*-
import FreeCAD
from Modeling.Modeling2D.Tools import Tools2D
from Modeling.Modeling2D.Tools.Tools2D import ObjectType


class Vector(object):
    def __init__(self):
        # self.obj = None
        FreeCAD.ActiveDocument.openTransaction("CreateVector")
        self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "Vector")
        FreeCAD.ActiveDocument.commitTransaction()
        self.__setProperty(self.obj)

    def __setProperty(self, obj):
        # 此处type通过一个枚举类来进行赋值
        self.obj.addProperty("App::PropertyString", "Type").Type = ObjectType.Vector
        # stringList是一个列表，正交投影面会有很多指定面
        self.obj.addProperty("App::PropertyString", "orthogonalProjectionLine").orthogonalProjectionLine = "未指定"
        # 有多种观测场，所以用StringList
        self.obj.addProperty("App::PropertyString", "observationField1").observationField1 = "E1"
        self.obj.addProperty("App::PropertyString", "observationField2").observationField2 = "E1"
        self.obj.addProperty("App::PropertyString", "timer").timer = "默认定时器"
        self.obj.addProperty("App::PropertyBool","isVectorNumber").isVectorNumber = False
        self.obj.addProperty("App::PropertyString", "vectorNumber1").vectorNumber1 = "20"
        self.obj.addProperty("App::PropertyString", "vectorNumber2").vectorNumber2 = "20"
        Tools2D.addCommonStartEndCoordinate(obj)
        Tools2D.addCommonDirection(obj)


def getObject():
    """
    创建obj并添加与Symtry相关的属性，然后返回obj
    """
    VectorIns = Vector()
    return VectorIns.obj
