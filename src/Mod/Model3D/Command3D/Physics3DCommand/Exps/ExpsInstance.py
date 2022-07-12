#-*- coding: utf-8 -*-
import FreeCAD
from Model3D.Tools import Tools3D, ObjectTools, InitDoc3D


class Exps(object):
    def __init__(self):
        FreeCAD.ActiveDocument.openTransaction("CreateExps_3D")
        self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "Emit_Explo")
        self.__setProperty(self.obj)
        InitDoc3D.addObjectToGroup_helper(self.obj, "Launch", "发射处理")
        FreeCAD.ActiveDocument.commitTransaction()

    def __setProperty(self, obj):
        # 此处type通过一个枚举类来进行赋值
        self.obj.addProperty("App::PropertyString", "Type").Type = ObjectTools.ObjectType.EXPS
        # stringList是一个列表，类型箔片会有很多指定类型
        self.obj.addProperty("App::PropertyString", "emitter").emitter = "未指定"
        self.obj.addProperty("App::PropertyBool", "isLimitFieldValue").isLimitFieldValue = False
        self.obj.addProperty("App::PropertyString", "limitFieldValue").limitFieldValue = "2.3E7"
        self.obj.addProperty("App::PropertyBool", "isMoreThanSpacemoreThanSpace").isMoreThanSpacemoreThanSpace = False
        self.obj.addProperty("App::PropertyString", "moreThanSpace").moreThanSpace = "0.0"
        self.obj.addProperty("App::PropertyBool", "isTheMinimumCharge").isTheMinimumCharge = False
        self.obj.addProperty("App::PropertyString", "theMinimumCharge").theMinimumCharge = "0.0"
        self.obj.addProperty("App::PropertyBool", "isPlasmaProductionRate").isPlasmaProductionRate = False
        self.obj.addProperty("App::PropertyString", "plasmaProductionRate").plasmaProductionRate = "THETA(T-5,E-9)"
        # 发射选项
        Tools3D.addLaunchOptionsCommonProperty(obj)
        if not hasattr(obj, "Boundary"):
            self.obj.addProperty("App::PropertyString", "Boundary")


def getObject():
    """
    创建obj并添加与Foil相关的属性，然后返回obj
    """
    expsIns = Exps()
    return expsIns.obj