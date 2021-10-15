# -*- coding: utf-8 -*-
import FreeCAD
from Model3D.Tools import Tools3D, ObjectTools, InitDoc3D


class Driv(object):
    def __init__(self):
        FreeCAD.ActiveDocument.openTransaction("CreateDriv")
        self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "CurrentSrc")
        self.__setProperty(self.obj)
        InitDoc3D.addObjectToGroup_helper(self.obj, "OtherModel", "其他模型")
        FreeCAD.ActiveDocument.commitTransaction()

    def __setProperty(self, obj):
        self.obj.addProperty("App::PropertyString", "Type").Type =ObjectTools.ObjectType.DRIV
        self.obj.addProperty("App::PropertyString", "sourceType").sourceType = "点电流源"
        # self.obj.addProperty("App::PropertyString", "assignSource").assignSource = "未指定"
        self.obj.addProperty("App::PropertyString", "orthogonalProjectionPlane").orthogonalProjectionPlane = "未指定"
        self.obj.addProperty("App::PropertyString", "electricCurrentDensity").electricCurrentDensity = "J1"
        self.obj.addProperty("App::PropertyString", "function").function = "0.0"
        Tools3D.addCommonStartEndCoordinate(obj)
        Tools3D.addCommonDirection(obj)
        if not hasattr(obj, "Boundary"):
            self.obj.addProperty("App::PropertyString", "Boundary")


def getObject():
    DrivIns = Driv()
    return DrivIns.obj