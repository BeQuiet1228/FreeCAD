# -*- coding: utf-8 -*-
import FreeCAD
from Modeling.Modeling2D.Tools.Tools2D import ObjectType

class NewMaterial(object):
    def __init__(self):
        # self.obj = None
        FreeCAD.ActiveDocument.openTransaction("CreateNewMaterial")
        self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "NewMaterial")
        FreeCAD.ActiveDocument.commitTransaction()
        self.__setProperty()

    def __setProperty(self):
        # 此处type通过一个枚举类来进行赋值
        self.obj.addProperty("App::PropertyString", "Type").Type = ObjectType.NewMaterial
        self.obj.addProperty("App::PropertyString", "AtomicNumber").AtomicNumber = "1"
        self.obj.addProperty("App::PropertyString", "AtomicMassNumber").AtomicMassNumber = "1"
        self.obj.addProperty("App::PropertyString", "MaterialDensity").MaterialDensity = "1"
        self.obj.addProperty("App::PropertyBool", "isConductivity").isConductivity = False
        self.obj.addProperty("App::PropertyString", "conductivity").conductivity = "1"
        self.obj.addProperty("App::PropertyBool", "isDielectricConstant").isDielectricConstant = False
        self.obj.addProperty("App::PropertyString", "dielectricConstant").dielectricConstant = "1"


def getObject():
    """
    创建obj并添加与Foil相关的属性，然后返回obj
    """
    newMaterialIns = NewMaterial()
    return newMaterialIns.obj

