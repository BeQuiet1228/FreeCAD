# -*- coding:utf-8 -*-
# @Time: 2020/11/2 08:19
# @Author: lilei
# @File: FiledSettingInstance.py
import FreeCAD
from Modeling.Modeling2D.Tools.Tools2D import ObjectType
from Modeling.Modeling2D.Tools import Tools2D


class FiledSetting(object):
    def __init__(self):
        self.obj = FreeCAD.ActiveDocument.getObject("FiledSetting")
        if self.obj is None:
            self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "FiledSetting")
            self.__setProperty()

    def __setProperty(self):
        # 此处type通过一个枚举类来进行赋值
        self.obj.addProperty("App::PropertyString", "Type").Type = ObjectType.FieldSetting
        # stringList是一个列表，类型箔片会有很多指定类型

        self.obj.addProperty("App::PropertyBool", "isMagnetostaticFieldX").isMagnetostaticFieldX = False
        self.obj.addProperty("App::PropertyString", "magnetostaticFieldX").magnetostaticFieldX = "0.0"
        self.obj.addProperty("App::PropertyBool", "isMagnetostaticFieldY").isMagnetostaticFieldY = False
        self.obj.addProperty("App::PropertyString", "magnetostaticFieldY").magnetostaticFieldY = "0.0"

        self.obj.addProperty("App::PropertyBool", "isElectrostaticFieldX").isElectrostaticFieldX = False
        self.obj.addProperty("App::PropertyString", "electrostaticFieldX").electrostaticFieldX = "0.0"
        self.obj.addProperty("App::PropertyBool", "isElectrostaticFieldY").isElectrostaticFieldY = False
        self.obj.addProperty("App::PropertyString", "electrostaticFieldY").electrostaticFieldY = "0.0"
        self.obj.addProperty("App::PropertyString", "self_definingFunction").self_definingFunction = ""


def getObject():
    """
    创建obj并添加与Foil相关的属性，然后返回obj
    """
    filedSettingIns = FiledSetting()
    return filedSettingIns.obj

