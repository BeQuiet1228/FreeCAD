#-*- coding: utf-8 -*-
import FreeCAD
from Modeling.Modeling2D.Tools.Tools2D import ObjectType
from Modeling.Modeling2D.Tools import Tools2D


class Exps(object):
    def __init__(self):
        FreeCAD.ActiveDocument.openTransaction("CreateExps")
        self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "Emit_Explo")
        FreeCAD.ActiveDocument.commitTransaction()
        self.__setProperty(self.obj)

    def __setProperty(self, obj):

        # 此处type通过一个枚举类来进行赋值
        self.obj.addProperty("App::PropertyString", "Type").Type = ObjectType.EXPS
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
        Tools2D.addLaunchOptionsCommonProperty(obj)


def getObject():
    """
    创建obj并添加与Foil相关的属性，然后返回obj
    """
    expsIns = Exps()
    return expsIns.obj
