# -*- coding: utf-8 -*-
import FreeCAD
from Model3D.Tools import Tools3D, ObjectTools, InitDoc3D


class Symtry(object):
    def __init__(self):
        # self.obj = None
        FreeCAD.ActiveDocument.openTransaction("CreateSymtry")
        self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "Symtry")
        self.__setProperty(self.obj)
        InitDoc3D.addObjectToGroup_helper(self.obj, "Symmetry", "对称边界")
        FreeCAD.ActiveDocument.commitTransaction()


    def __setProperty(self, obj):
        # 此处type通过一个枚举类来进行赋值
        self.obj.addProperty("App::PropertyString", "Type").Type = ObjectTools.ObjectType.SYMT
        # stringList是一个列表，正交投影面会有很多指定面
        self.obj.addProperty("App::PropertyString", "orthogonalProjectionPlane").orthogonalProjectionPlane = "未指定"
        # 对称类型有很多种，所以用StringList
        self.obj.addProperty("App::PropertyString", "symmetricalType").symmetricalType = "轴对称"
        self.obj.addProperty("App::PropertyString", "assignType").assignType = "未指定"
        self.obj.addProperty("App::PropertyString", "theNormalCycle").theNormalCycle = "0"
        self.obj.addProperty("App::PropertyDistance", "helper", ).helper = 0
        self.obj.addProperty("App::PropertyAngle", "helper1", ).helper1 = 0
        Tools3D.addCommonStartEndCoordinate(obj)
        Tools3D.addCommonDirection(obj)
        Tools3D.addPhysicsProperty(obj)
        Tools3D.isNegativeOrPositive(obj)
        if not hasattr(obj, "Boundary"):
            self.obj.addProperty("App::PropertyString", "Boundary")


def getObject():
    """
    创建obj并添加与Symtry相关的属性，然后返回obj
    """
    symtryIns = Symtry()
    return symtryIns.obj