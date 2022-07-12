#-*- coding: utf-8 -*-
import FreeCAD
from Modeling.Modeling2D.Tools import Tools2D
from Modeling.Modeling2D.Tools.Tools2D import ObjectType


class Driv(object):
    def __init__(self):
        FreeCAD.ActiveDocument.openTransaction("CreateDriv")
        self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "CurrentSrc")
        FreeCAD.ActiveDocument.commitTransaction()
        self.__setProperty(self.obj)
    
    def __setProperty(self, obj):
        self.obj.addProperty("App::PropertyString", "Type").Type = ObjectType.DRIV
        self.obj.addProperty("App::PropertyString", "sourceType").sourceType = "点电流源"
        self.obj.addProperty("App::PropertyString", "assignSource").assignSource = "未指定"
        self.obj.addProperty("App::PropertyString", "electricCurrentDensity").electricCurrentDensity = "J1"
        self.obj.addProperty("App::PropertyString", "function").function = "0.0"
        Tools2D.addCommonStartEndCoordinate(obj)
        Tools2D.addCommonDirection(obj)


def getObject():
    DrivIns = Driv()
    return DrivIns.obj
