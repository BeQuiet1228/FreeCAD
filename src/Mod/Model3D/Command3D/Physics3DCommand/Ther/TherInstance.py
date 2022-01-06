#-*- coding: utf-8 -*-
import FreeCAD
from Model3D.Tools import Tools3D, ObjectTools, InitDoc3D


class Ther(object):
    def __init__(self):
        FreeCAD.ActiveDocument.openTransaction("CreateTher_3D")
        self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "Emit_Them")
        self.__setProperty(self.obj)
        InitDoc3D.addObjectToGroup_helper(self.obj, "Launch", "发射处理")
        FreeCAD.ActiveDocument.commitTransaction()

    def __setProperty(self, obj):
        # 此处type通过一个枚举类来进行赋值
        self.obj.addProperty("App::PropertyString", "Type").Type = ObjectTools.ObjectType.THER
        # stringList是一个列表，类型箔片会有很多指定类型
        self.obj.addProperty("App::PropertyString", "emitter").emitter = "未指定"
        self.obj.addProperty("App::PropertyString", "workingFunctionWF").workingFunctionWF = "0.0"
        self.obj.addProperty("App::PropertyString", "workingTemperatureTP").workingTemperatureTP = "0.0"
        # 发射选项
        Tools3D.addLaunchOptionsCommonProperty(obj)
        if not hasattr(obj, "Boundary"):
            self.obj.addProperty("App::PropertyString", "Boundary")


def getObject():
    """
    创建obj并添加与Foil相关的属性，然后返回obj
    """
    therIns = Ther()
    return therIns.obj