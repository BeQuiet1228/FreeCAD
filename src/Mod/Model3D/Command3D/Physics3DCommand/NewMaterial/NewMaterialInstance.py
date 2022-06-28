# -*- coding: utf-8 -*-
import FreeCAD
from Model3D.Tools import ObjectTools, InitDoc3D


class NewMaterial(object):
    def __init__(self):
        # self.obj = None
        FreeCAD.ActiveDocument.openTransaction("CreateNewMaterial_3D")
        self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "NewMaterial")
        self.__setProperty(self.obj)
        InitDoc3D.addObjectToGroup_helper(self.obj, "NewMaterialG", "新材料")
        FreeCAD.ActiveDocument.commitTransaction()

    def __setProperty(self, obj):
        # 此处type通过一个枚举类来进行赋值
        self.obj.addProperty("App::PropertyString", "Type").Type = ObjectTools.ObjectType.NewMaterial
        self.obj.addProperty("App::PropertyBool", "isconductivity").isconductivity = False
        self.obj.addProperty("App::PropertyBool", "isdielectricConstant").isdielectricConstant = False
        self.obj.addProperty("App::PropertyString", "atomicNumber").atomicNumber = "1"
        self.obj.addProperty("App::PropertyString", "atomicMassNumber").atomicMassNumber = "1"
        self.obj.addProperty("App::PropertyString", "atomicDesity").atomicDesity = "1"
        self.obj.addProperty("App::PropertyString", "dielectricConstant").dielectricConstant = "1"
        self.obj.addProperty("App::PropertyString", "conductivity").conductivity = "1"
        if not hasattr(obj, "Boundary"):
            self.obj.addProperty("App::PropertyString", "Boundary")


def getObject():
    """
    创建obj并添加与NewMaterial相关的属性，然后返回obj
    """
    NewMaterialIns = NewMaterial()
    return NewMaterialIns.obj