#-*- coding: utf-8 -*-
import FreeCAD
from Model3D.Tools import ObjectTools, InitDoc3D


class Popu(object):
    def __init__(self):
        FreeCAD.ActiveDocument.openTransaction("Create3D_Populate")
        self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "Populate")
        self.__setProperty()
        InitDoc3D.addObjectToGroup_helper(self.obj, "Launch", "发射处理")
        FreeCAD.ActiveDocument.commitTransaction()

    def __setProperty(self):

        # 此处type通过一个枚举类来进行赋值
        self.obj.addProperty("App::PropertyString", "Type").Type = ObjectTools.ObjectType.POPU
        # stringList是一个列表，类型箔片会有很多指定类型
        self.obj.addProperty("App::PropertyString", "typesOfParticles").typesOfParticles = "ELECTRON"
        self.obj.addProperty("App::PropertyString", "orthogonalProjectionArea").orthogonalProjectionArea = "未指定"

        self.obj.addProperty("App::PropertyString", "gridMacroParticleNumberX").gridMacroParticleNumberX = "1"
        self.obj.addProperty("App::PropertyString", "gridMacroParticleNumberY").gridMacroParticleNumberY = "1"
        self.obj.addProperty("App::PropertyString", "gridMacroParticleNumberZ").gridMacroParticleNumberZ = "1"

        self.obj.addProperty("App::PropertyString", "averagelectronVelocityX").averagelectronVelocityX = "0"
        self.obj.addProperty("App::PropertyString", "averagelectronVelocityY").averagelectronVelocityY = "0"
        self.obj.addProperty("App::PropertyString", "averagelectronVelocityZ").averagelectronVelocityZ = "0"
        self.obj.addProperty("App::PropertyString", "electricDensity").electricDensity = "1.6e-10"
        self.obj.addProperty("App::PropertyString", "temperature").temperature = "300"
        if not hasattr(self.obj, "Boundary"):
            self.obj.addProperty("App::PropertyString", "Boundary")


def getObject():
    """
    创建obj并添加与Foil相关的属性，然后返回obj
    """
    popuIns = Popu()
    return popuIns.obj