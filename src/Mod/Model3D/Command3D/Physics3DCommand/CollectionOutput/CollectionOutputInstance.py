# -*- coding: utf-8 -*-
import FreeCAD
from Model3D.Tools import Tools3D, ObjectTools, InitDoc3D

class CollectionOutput(object):
    def __init__(self):
        # self.obj = None
        FreeCAD.ActiveDocument.openTransaction("CreateCollectionOutput")
        self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "CollectionOutput")
        self.__setProperty(self.obj)
        InitDoc3D.addObjectToGroup_helper(self.obj, "CollectionOutput", "收集体导出")
        FreeCAD.ActiveDocument.commitTransaction()

    def __setProperty(self, obj):
        # 此处type通过一个枚举类来进行赋值
        self.obj.addProperty("App::PropertyString", "Type").Type = ObjectTools.ObjectType.CollectionOutput
        self.obj.addProperty("App::PropertyString", "collectionType").collectionType = "未指定"
        self.obj.addProperty("App::PropertyString", "path").path = " "
        # self.obj.addProperty("App::PropertyString", "max").max = "100000"
        # if not hasattr(obj, "Boundary"):
        #     self.obj.addProperty("App::PropertyString", "Boundary")


def getObject():
    """
    创建obj并添加与MacroParticle相关的属性，然后返回obj
    """
    CollectionOutputIns = CollectionOutput()
    return CollectionOutputIns.obj
