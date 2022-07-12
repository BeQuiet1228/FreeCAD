# -*- coding: utf-8 -*-
import FreeCAD,FreeCADGui
from Modeling.Modeling2D.Tools.Tools2D import ObjectType


class DiyGrid(object):
    def __init__(self):
        self.obj = FreeCAD.ActiveDocument.getObject("DiyGrid")
        if self.obj is None:
            self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "DiyGrid")
            self.__setProperty()

    def __setProperty(self):

        # 此处type通过一个枚举类来进行赋值
        self.obj.addProperty("App::PropertyString", "Type").Type = ObjectType.DiyGrid
        # stringList是一个列表，类型箔片会有很多指定类型
        self.obj.addProperty("App::PropertyFloat", "p1_x").p1_x = 0.0
        self.obj.addProperty("App::PropertyFloat", "p1_y").p1_y = 0.0

        self.obj.addProperty("App::PropertyInteger", "gridNum").gridNum = 100
        self.obj.addProperty("App::PropertyInteger", "gridSizeX").gridSizeX = 10
        self.obj.addProperty("App::PropertyInteger", "gridSizeY").gridSizeY = 10
        self.obj.addProperty("App::PropertyBool", "isShow").isShow = True




def getObject():
    """
    创建obj并添加与Foil相关的属性，然后返回obj
    """
    gridIns = DiyGrid()
    return gridIns.obj
