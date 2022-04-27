# -*- coding: utf-8 -*-
import FreeCAD
from Model3D.Tools import ObjectTools, InitDoc3D


class FieldSetting(object):
    def __init__(self):
        # self.obj = None
        self.obj = FreeCAD.ActiveDocument.getObject("FiledSetting")
        if self.obj is None:
            self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "FiledSetting")
            self.__setProperty(self.obj)
        InitDoc3D.addObjectToGroup_helper(self.obj, "FieldSetting", "场及函数定义")

    def __setProperty(self, obj):
        # 此处type通过一个枚举类来进行赋值
        self.obj.addProperty("App::PropertyString", "Type").Type = ObjectTools.ObjectType.FieldSetting
        self.obj.addProperty("App::PropertyBool", "isMagnetostaticFieldX").isMagnetostaticFieldX = False
        self.obj.addProperty("App::PropertyString", "magnetostaticFieldX").magnetostaticFieldX = "0.0"
        self.obj.addProperty("App::PropertyBool", "isMagnetostaticFieldY").isMagnetostaticFieldY = False
        self.obj.addProperty("App::PropertyString", "magnetostaticFieldY").magnetostaticFieldY = "0.0"
        self.obj.addProperty("App::PropertyBool", "isMagnetostaticFieldZ").isMagnetostaticFieldZ = False
        self.obj.addProperty("App::PropertyString", "magnetostaticFieldZ").magnetostaticFieldZ = "0.0"

        self.obj.addProperty("App::PropertyBool", "isElectrostaticFieldX").isElectrostaticFieldX = False
        self.obj.addProperty("App::PropertyString", "electrostaticFieldX").electrostaticFieldX = "0.0"
        self.obj.addProperty("App::PropertyBool", "isElectrostaticFieldY").isElectrostaticFieldY = False
        self.obj.addProperty("App::PropertyString", "electrostaticFieldY").electrostaticFieldY = "0.0"
        self.obj.addProperty("App::PropertyBool", "isElectrostaticFieldZ").isElectrostaticFieldZ = False
        self.obj.addProperty("App::PropertyString", "electrostaticFieldZ").electrostaticFieldZ = "0.0"
        self.obj.addProperty("App::PropertyString", "self_definingFunction").self_definingFunction = ""
        if not hasattr(obj, "Project"):
            self.obj.addProperty("App::PropertyString", "Project")


def getObject():
    """
    创建obj并添加与FieldSetting相关的属性，然后返回obj
    """
    FieldSettingIns = FieldSetting()
    return FieldSettingIns.obj