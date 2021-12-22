# -*- coding: utf-8 -*-
import FreeCAD
from Model3D.Tools import Tools3D, ObjectTools


class ParticleDefine(object):
    def __init__(self):
        # self.obj = None
        FreeCAD.ActiveDocument.openTransaction("CreateIONS")
        self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "IONS")
        self.__setProperty()
        FreeCAD.ActiveDocument.commitTransaction()

    def __setProperty(self):
        # 此处type通过一个枚举类来进行赋值
        self.obj.addProperty("App::PropertyString", "Type").Type = ObjectTools.ObjectType.NewParticle
        self.obj.addProperty("App::PropertyString", "powerUnit").powerUnit = "+1"
        self.obj.addProperty("App::PropertyString", "mass").mass = "28"
        self.obj.addProperty("App::PropertyString", "protonMassUnit").protonMassUnit = "PROTON"
        if not hasattr(self.obj, "Boundary"):
            self.obj.addProperty("App::PropertyString", "Boundary")


def getObject():
    """
    创建obj并添加与Foil相关的属性，然后返回obj
    """
    particleDefineIns = ParticleDefine()
    return particleDefineIns.obj
