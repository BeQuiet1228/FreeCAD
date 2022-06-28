#-*- coding: utf-8 -*-
import FreeCAD
from Modeling.Modeling2D.Tools import Tools2D
from Modeling.Modeling2D.Tools.Tools2D import ObjectType


class FreeSpace(object):
    def __init__(self):
        # self.obj = None
        FreeCAD.ActiveDocument.openTransaction("CreateFreeSpace")
        self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "FreeSpace")
        FreeCAD.ActiveDocument.commitTransaction()
        self.__setProperty(self.obj)
    
    def __setProperty(self, obj):
        # 此处type通过一个枚举类来进行赋值
        self.obj.addProperty("App::PropertyString", "Type").Type = ObjectType.FREE
        # stringList是一个列表，正交投影面会有很多指定面
        self.obj.addProperty("App::PropertyString", "orthogonalProjectionPlane").orthogonalProjectionPlane = "未指定"
        # 吸收分量有很多种，所以用StringList
        self.obj.addProperty("App::PropertyString", "absorb").absorb = "ALL"
        self.obj.addProperty("App::PropertyBool", "isCustomConductivity").isCustomConductivity = False
        self.obj.addProperty("App::PropertyString", "customConductivity").customConductivity = "1.0*Xn*Xn"
        Tools2D.addCommonStartEndCoordinate(obj)
        Tools2D.addCommonDirection(obj)
        Tools2D.addCommonPropertyToObject(obj)
        Tools2D.isNegativeOrPositive(obj)


def getObject():
    """
    创建obj并添加与FreeSpace相关的属性，然后返回obj
    """
    freeSpaceIns = FreeSpace()
    return freeSpaceIns.obj
