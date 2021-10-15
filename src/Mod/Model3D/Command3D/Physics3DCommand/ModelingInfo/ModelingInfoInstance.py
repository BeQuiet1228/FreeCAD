#-*- coding: utf-8 -*-
import FreeCAD
from Model3D.Tools import Tools3D, ObjectTools, InitDoc3D

class ModelingInfo(object):
    def __init__(self):
        # FreeCAD.ActiveDocument.openTransaction("CreateModelingInfo")
        # self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "ModelingInfo")
        # FreeCAD.ActiveDocument.commitTransaction()
        # self.__setProperty()
        self.obj = FreeCAD.ActiveDocument.getObject("HEADER")
        if self.obj is None:
            self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "HEADER")
            self.__setProperty()
        InitDoc3D.addObjectToGroup_helper(self.obj, "Info", "模型信息输入")

    def __setProperty(self):

        # 此处type通过一个枚举类来进行赋值
        self.obj.addProperty("App::PropertyString", "Type").Type = ObjectTools.ObjectType.Info
        # stringList是一个列表，类型箔片会有很多指定类型
        self.obj.addProperty("App::PropertyString", "modeling").modeling = "NONE"
        self.obj.addProperty("App::PropertyString", "author").author = "NONE"
        self.obj.addProperty("App::PropertyString", "company").company = "NONE"
        self.obj.addProperty("App::PropertyString", "remarks").remarks = "NONE"
        if not hasattr(self.obj, "Project"):
            self.obj.addProperty("App::PropertyString", "Project")


def getObject():
    """
    创建obj并添加与Foil相关的属性，然后返回obj
    """
    ModelingInfoIns = ModelingInfo()
    return ModelingInfoIns.obj