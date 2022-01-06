#-*- coding: utf-8 -*-
import FreeCAD
from Modeling.Modeling2D.Tools import Tools2D
from Modeling.Modeling2D.Tools.Tools2D import ObjectType


class Foil(object):
    def __init__(self):
        # self.obj = None
        self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "Foil")
        self.__setProperty(self.obj)
    
    def __setProperty(self, obj):
        # self.obj.addProperty("App::PropertyString","objName").name = "Foil"
        # 此处type通过一个枚举类来进行赋值
        self.obj.addProperty("App::PropertyString", "Type").Type = ObjectType.FOIL
        # stringList是一个列表，类型箔片会有很多指定类型
        self.obj.addProperty("App::PropertyString", "foilType").foilType = "未指定"
        self.obj.addProperty("App::PropertyString", "foilThickness").foilThickness = "1mm"         
        self.obj.addProperty("App::PropertyString", "defaultMaterial").defaultMaterial = "GOLD"
        self.obj.addProperty("App::PropertyString", "customMaterial").customMaterial = "未指定"
        self.obj.addProperty("App::PropertyBool", "isCheckCustom").isCheckCustom = True
        self.obj.addProperty("App::PropertyBool", "isCheckDefault").isCheckDefault = False
        Tools2D.addCommonStartEndCoordinate(obj)


def getObject():
    """
    创建obj并添加与Foil相关的属性，然后返回obj
    """
    foilIns = Foil()
    return foilIns.obj
