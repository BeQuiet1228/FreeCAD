# -*- coding: utf-8 -*-
import FreeCAD
from Modeling.Modeling2D.Tools import Tools2D
from Modeling.Modeling2D.Tools.Tools2D import ObjectType


class Symtry(object):
    def __init__(self):
        # self.obj = None
        FreeCAD.ActiveDocument.openTransaction("CreateSymtry")
        self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "Symtry")
        FreeCAD.ActiveDocument.commitTransaction()
        self.__setProperty(self.obj)
    
    def __setProperty(self, obj):
        # 此处type通过一个枚举类来进行赋值
        self.obj.addProperty("App::PropertyString", "Type").Type = ObjectType.SYMT
        # stringList是一个列表，正交投影面会有很多指定面
        self.obj.addProperty("App::PropertyString", "orthogonalProjectionPlane").orthogonalProjectionPlane = "未指定"
        # 对称类型有很多种，所以用StringList
        self.obj.addProperty("App::PropertyString", "symmetricalType").symmetricalType = "轴对称"
        self.obj.addProperty("App::PropertyString", "assignType").assignType = "未指定"
        self.obj.addProperty("App::PropertyString", "theNormalCycle").theNormalCycle = "0"
        self.obj.addProperty("App::PropertyDistance", "helper",).helper = 0
        Tools2D.addCommonStartEndCoordinate(obj)
        Tools2D.addCommonDirection(obj)
        Tools2D.addCommonPropertyToObject(obj)
        Tools2D.isNegativeOrPositive(obj)


def getObject():
    """
    创建obj并添加与Symtry相关的属性，然后返回obj
    """
    symtryIns = Symtry()
    return symtryIns.obj
