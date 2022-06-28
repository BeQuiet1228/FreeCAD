# -*- coding:utf-8 -*-
# @Time: 2020/11/2 08:35
# @Author: lilei
# @File: RunProcessingOptionsInstance.py

import FreeCAD
from Modeling.Modeling2D.Tools.Tools2D import ObjectType
from Modeling.Modeling2D.Tools import Tools2D


class RunProcessingOptions(object):
    def __init__(self):
        self.obj = FreeCAD.ActiveDocument.getObject("runOptions")
        if self.obj is None:
            self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "runOptions")
            self.__setProperty()

    def __setProperty(self):
        # 此处type通过一个枚举类来进行赋值
        self.obj.addProperty("App::PropertyString", "Type").Type = ObjectType.RunOptions
        # stringList是一个列表，类型箔片会有很多指定类型

        self.obj.addProperty("App::PropertyBool", "isDisplayStructureDrawing").isDisplayStructureDrawing = True
        self.obj.addProperty("App::PropertyBool", "isHaltedState").isHaltedState = False


def getObject():
    """
    创建obj并添加与Foil相关的属性，然后返回obj
    """
    runProcessingOptionsIns = RunProcessingOptions()
    return runProcessingOptionsIns.obj
