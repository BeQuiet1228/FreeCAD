#-*- coding: utf-8 -*-
import FreeCAD
from Model3D.Tools import Tools3D, ObjectTools, InitDoc3D


class Beam(object):
    def __init__(self):
        FreeCAD.ActiveDocument.openTransaction("CreateBeam_3D")
        self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "Emit_Beam")
        self.__setProperty(self.obj)
        InitDoc3D.addObjectToGroup_helper(self.obj, "Launch", "发射处理")
        FreeCAD.ActiveDocument.commitTransaction()

    def __setProperty(self, obj):
        # 此处type通过一个枚举类来进行赋值
        self.obj.addProperty("App::PropertyString", "Type").Type = ObjectTools.ObjectType.BEAM
        # stringList是一个列表，类型箔片会有很多指定类型
        self.obj.addProperty("App::PropertyString", "emitter").emitter = "未指定"
        self.obj.addProperty("App::PropertyString", "beamCurrentDensity").beamCurrentDensity = "0.0"
        self.obj.addProperty("App::PropertyString", "beamVoltageDensity").beamVoltageDensity = "0.0"
        Tools3D.addLaunchOptionsCommonProperty(obj)
        if not hasattr(obj, "Boundary"):
            self.obj.addProperty("App::PropertyString", "Boundary")


def getObject():
    """
    创建obj并添加与Foil相关的属性，然后返回obj
    """
    beamIns = Beam()
    return beamIns.obj