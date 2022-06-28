# -*- coding:utf-8 -*-
# @Time: 2020/11/1 10:23
# @Author: lilei
# @File: ModelInfoInstance.py
import FreeCAD
from Modeling.Modeling2D.Tools.Tools2D import ObjectType
from Modeling.Modeling2D.Tools import Tools2D


class ModelInfo(object):

    def __init__(self):
        self.obj = FreeCAD.ActiveDocument.getObject("HEADER")
        if self.obj is None:
            self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "HEADER")
            self.__setProperty()

    def __setProperty(self):
        # 此处type通过一个枚举类来进行赋值
        self.obj.addProperty("App::PropertyString", "Type").Type = ObjectType.Info
        # stringList是一个列表，类型箔片会有很多指定类型

        self.obj.addProperty("App::PropertyString", "model").model = "NONE"
        self.obj.addProperty("App::PropertyString", "author").author = "NONE"
        self.obj.addProperty("App::PropertyString", "organization").organization = "NONE"
        self.obj.addProperty("App::PropertyString", "remark").remark = "NONE"


def getObject():
    """
    创建obj并添加与Foil相关的属性，然后返回obj
    """
    modelInfoIns = ModelInfo()
    return modelInfoIns.obj

