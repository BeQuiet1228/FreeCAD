#-*- coding: utf-8 -*-
import FreeCAD
from Modeling.Modeling2D.Tools.Tools2D import ObjectType
from Modeling.Modeling2D.Tools import Tools2D


class Feld(object):
    def __init__(self):
        FreeCAD.ActiveDocument.openTransaction("CreateFeld")
        self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "Emit_Field")
        FreeCAD.ActiveDocument.commitTransaction()
        self.__setProperty(self.obj)

    def __setProperty(self, obj):

        # 此处type通过一个枚举类来进行赋值
        self.obj.addProperty("App::PropertyString", "Type").Type = ObjectType.FELD
        # stringList是一个列表，类型箔片会有很多指定类型
        self.obj.addProperty("App::PropertyString", "emitter").emitter = "未指定"

        self.obj.addProperty("App::PropertyString", "constantA").constantA = "1.5414e-006"
        self.obj.addProperty("App::PropertyString", "constantB").constantB = "6830800000"
        self.obj.addProperty("App::PropertyString", "workingFunctionPHI").workingFunctionPHI = "0"
        # 发射选项
        Tools2D.addLaunchOptionsCommonProperty(obj)


def getObject():
    """
    创建obj并添加与Foil相关的属性，然后返回obj
    """
    feldIns = Feld()
    return feldIns.obj
