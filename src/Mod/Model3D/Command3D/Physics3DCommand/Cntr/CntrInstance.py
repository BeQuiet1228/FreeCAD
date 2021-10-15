# -*- coding: utf-8 -*-
import FreeCAD
from Model3D.Tools import Tools3D, ObjectTools, InitDoc3D


class Cntr(object):
    def __init__(self):
        FreeCAD.ActiveDocument.openTransaction("CreateCntr_3D")
        self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", ObjectTools.ObjectType.CNTR)
        self.__setProperty(self.obj)
        InitDoc3D.addObjectToGroup_helper(self.obj, "EquivalentObs", "等值观测")
        FreeCAD.ActiveDocument.commitTransaction()

    def __setProperty(self, obj):
        # 此处type通过一个枚举类来进行赋值
        self.obj.addProperty("App::PropertyString", "Type").Type = ObjectTools.ObjectType.CNTR
        # stringList是一个列表，正交投影面会有很多指定面
        # self.obj.addProperty("App::PropertyString", "orthogonalProjectionLine").orthogonalProjectionLine = "未指定"
        self.obj.addProperty("App::PropertyString", "orthogonalProjectionPlane").orthogonalProjectionPlane = "未指定"
        # 观测场有多种，所以用StringList
        self.obj.addProperty("App::PropertyString", "observationField").observationField = "E1"
        self.obj.addProperty("App::PropertyString", "timer").timer = "默认定时器"
        self.obj.addProperty("App::PropertyBool", "isoline").isoline = False
        Tools3D.addCommonStartEndCoordinate(obj)
        Tools3D.addCommonDirection(obj)
        if not hasattr(obj, "Observation"):
            self.obj.addProperty("App::PropertyString", "Observation")

def getObject():
    """
    创建obj并添加与Cntr相关的属性，然后返回obj
    """
    cntrIns = Cntr()
    return cntrIns.obj
