# -*- coding: utf-8 -*-
import FreeCAD
from Model3D.Tools import Tools3D, ObjectTools, InitDoc3D


class Foil(object):
    def __init__(self):
        # self.obj = None
        FreeCAD.ActiveDocument.openTransaction("Create_3D_Foil")
        self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "FoilObj")
        self.__setProperty(self.obj)
        InitDoc3D.addObjectToGroup_helper(self.obj, "OtherModel", "其他模型")
        FreeCAD.ActiveDocument.commitTransaction()

    def __setProperty(self, obj):
        # self.obj.addProperty("App::PropertyString","objName").name = "Foil"
        # 此处type通过一个枚举类来进行赋值
        self.obj.addProperty("App::PropertyString", "Type").Type = ObjectTools.ObjectType.FOIL
        # stringList是一个列表，类型箔片会有很多指定类型
        self.obj.addProperty("App::PropertyString", "foilType").foilType = "未指定"
        self.obj.addProperty("App::PropertyString", "foilThickness").foilThickness = "1mm"
        self.obj.addProperty("App::PropertyString", "defaultMaterial").defaultMaterial = "GOLD"
        self.obj.addProperty("App::PropertyString", "customMaterial").customMaterial = "未指定"
        self.obj.addProperty("App::PropertyBool", "isCheckCustom").isCheckCustom = True
        self.obj.addProperty("App::PropertyBool", "isCheckDefault").isCheckDefault = False
        Tools3D.addCommonStartEndCoordinate(obj)
        Tools3D.addCommonDirection(obj)
        Tools3D.isNegativeOrPositive(obj)
        if not hasattr(obj, "Boundary"):
            self.obj.addProperty("App::PropertyString", "Boundary")


def getObject():
    """
    创建obj并添加与Foil相关的属性，然后返回obj
    """
    foilIns = Foil()
    return foilIns.obj

