#-*- coding: utf-8 -*-
import FreeCAD
from Model3D.Tools import Tools3D, ObjectTools, InitDoc3D


class RunOptions(object):
    def __init__(self):
        self.obj = FreeCAD.ActiveDocument.getObject("runOptions")
        if self.obj is None:
            self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "runOptions")
            self.__setProperty()
        InitDoc3D.addObjectToGroup_helper(self.obj, "RunOptions", "运行处理选项")

    def __setProperty(self):

        # 此处type通过一个枚举类来进行赋值
        self.obj.addProperty("App::PropertyString", "Type").Type = ObjectTools.ObjectType.RunOptions
        # stringList是一个列表，类型箔片会有很多指定类型
        self.obj.addProperty("App::PropertyBool", "isCheckBox_show_structureChart").isCheckBox_show_structureChart = True
        self.obj.addProperty("App::PropertyBool", "isCheckBox_paused_when_start").isCheckBox_paused_when_start = False
        if not hasattr(self.obj, "Project"):
            self.obj.addProperty("App::PropertyString", "Project")



def getObject():
    """
    创建obj并添加与Foil相关的属性，然后返回obj
    """
    RunOptionsIns = RunOptions()
    return RunOptionsIns.obj