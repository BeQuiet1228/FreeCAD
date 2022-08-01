# -*- coding: utf-8 -*-
import FreeCAD
from Model3D.Tools import Tools3D, ObjectTools, InitDoc3D

class CollectionOutput(object):
    def __init__(self):
        self.obj = FreeCAD.ActiveDocument.getObject("collectionOutput")
        if self.obj is None:
            self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "collectionOutput")
            self.__setProperty()
        InitDoc3D.addObjectToGroup_helper(self.obj, "CollectionOutput", "收集粒子数据导出")
        FreeCAD.ActiveDocument.commitTransaction()

    def __setProperty(self):
        # 此处type通过一个枚举类来进行赋值
        self.obj.addProperty("App::PropertyString", "Type").Type = ObjectTools.ObjectType.CollectionOutput
        self.obj.addProperty("App::PropertyString", "collectionType").collectionType = "未指定"
        self.obj.addProperty("App::PropertyString", "path").path = " "
        # self.obj.addProperty("App::PropertyString", "max").max = "100000"
        if not hasattr(self.obj, "Project"):
            self.obj.addProperty("App::PropertyString", "Project")


def getObject():
    """
    创建obj并添加与MacroParticle相关的属性，然后返回obj
    """
    CollectionOutputIns = CollectionOutput()
    return CollectionOutputIns.obj
