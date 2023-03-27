# -*- coding: utf-8 -*-
import FreeCAD
from Model3D.Tools import Tools3D, ObjectTools, InitDoc3D


class Gasout(object):
    def __init__(self):
        FreeCAD.ActiveDocument.openTransaction("CreateGasOut")
        self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "GasOut")
        self.__setProperty(self.obj)
        InitDoc3D.addObjectToGroup_helper(self.obj, "OtherModel", "其他模型")
        FreeCAD.ActiveDocument.commitTransaction()

    def __setProperty(self, obj):
        self.obj.addProperty("App::PropertyString", "Type").Type =ObjectTools.ObjectType.GASOUT
        self.obj.addProperty("App::PropertyString", "absorbVol").absorbVol = "未指定"

        self.obj.addProperty("App::PropertyString", "density").density = "1E19"
        self.obj.addProperty("App::PropertyString", "area").area = "1E-19"
        self.obj.addProperty("App::PropertyString", "threshold").threshold = "10"
        self.obj.addProperty("App::PropertyString", "grid").grid = "10"
        self.obj.addProperty("App::PropertyString", "normal").normal = "X1"
        self.obj.addProperty("App::PropertyBool", "isNegative").isNegative = False
        self.obj.addProperty("App::PropertyBool", "isPositive").isPositive = True
        if not hasattr(obj, "Boundary"):
            self.obj.addProperty("App::PropertyString", "Boundary")


def getObject():
    GasoutIns = Gasout()
    return GasoutIns.obj