# -*- coding: utf-8 -*-
import FreeCAD
from Model3D.Tools import Tools3D, ObjectTools, InitDoc3D


class Vector(object):
    def __init__(self):
        FreeCAD.ActiveDocument.openTransaction("CreateVector_3D")
        self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", ObjectTools.ObjectType.Vector)
        self.__setProperty(self.obj)
        InitDoc3D.addObjectToGroup_helper(self.obj, "VectorObs", "矢量观测")
        FreeCAD.ActiveDocument.commitTransaction()

    def __setProperty(self, obj):
        # 此处type通过一个枚举类来进行赋值
        self.obj.addProperty("App::PropertyString", "Type").Type = ObjectTools.ObjectType.Vector
        # stringList是一个列表，正交投影面会有很多指定面
        # self.obj.addProperty("App::PropertyString", "orthogonalProjectionLine").orthogonalProjectionLine = "未指定"
        self.obj.addProperty("App::PropertyString", "orthogonalProjectionPlane").orthogonalProjectionPlane = "未指定"
        # 有多种观测场，所以用StringList
        self.obj.addProperty("App::PropertyString", "observationField1").observationField1 = "E1"
        self.obj.addProperty("App::PropertyString", "observationField2").observationField2 = "E1"
        self.obj.addProperty("App::PropertyString", "timer").timer = "默认定时器"
        self.obj.addProperty("App::PropertyBool", "isVectorNumber").isVectorNumber = False
        self.obj.addProperty("App::PropertyString", "vectorNumber1").vectorNumber1 = "20"
        self.obj.addProperty("App::PropertyString", "vectorNumber2").vectorNumber2 = "20"
        Tools3D.addCommonStartEndCoordinate(obj)
        Tools3D.addCommonDirection(obj)
        if not hasattr(obj, "Observation"):
            self.obj.addProperty("App::PropertyString", "Observation")


def getObject():
    """
    创建obj并添加与Vector相关的属性，然后返回obj
    """
    vectorIns = Vector()
    return vectorIns.obj
