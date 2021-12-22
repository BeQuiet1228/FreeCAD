# -*- coding: utf-8 -*-
import FreeCAD

from Modeling.Modeling2D.Tools import Tools2D
from Modeling.Modeling2D.Tools.Tools2D import ObjectType

class Cntr(object):
    def __init__(self):
        # self.obj = None
        FreeCAD.ActiveDocument.openTransaction("CreateCntr")
        self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "Cntr")
        FreeCAD.ActiveDocument.commitTransaction()
        self.__setProperty(self.obj)

    def __setProperty(self, obj):
        # 此处type通过一个枚举类来进行赋值
        self.obj.addProperty("App::PropertyString", "Type").Type = ObjectType.CNTR
        # stringList是一个列表，正交投影面会有很多指定面
        self.obj.addProperty("App::PropertyString", "orthogonalProjectionLine").orthogonalProjectionLine = "未指定"
        # 观测场有多种，所以用StringList
        self.obj.addProperty("App::PropertyString", "observationField").observationField = "E1"
        self.obj.addProperty("App::PropertyString", "timer").timer = "默认定时器"
        self.obj.addProperty("App::PropertyBool", "isoline").isoline = False
        Tools2D.addCommonStartEndCoordinate(obj)
        Tools2D.addCommonDirection(obj)


def getObject():
    """
    创建obj并添加与Cntr相关的属性，然后返回obj
    """
    CntrIns = Cntr()
    return CntrIns.obj