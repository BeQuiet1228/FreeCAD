# -*- coding: utf-8 -*-
import FreeCAD
from Model3D.Tools import Tools3D, ObjectTools, InitDoc3D

class MacroParticle(object):
    def __init__(self):
        # self.obj = None
        FreeCAD.ActiveDocument.openTransaction("CreateMacroParticle")
        self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "MacroParticle")
        self.__setProperty(self.obj)
        InitDoc3D.addObjectToGroup_helper(self.obj, "NewParticleG", "新粒子")
        FreeCAD.ActiveDocument.commitTransaction()

    def __setProperty(self, obj):
        # 此处type通过一个枚举类来进行赋值
        self.obj.addProperty("App::PropertyString", "Type").Type = ObjectTools.ObjectType.MacroParticle
        self.obj.addProperty("App::PropertyString", "particleType").particleType = "ALL"
        self.obj.addProperty("App::PropertyString", "every").every = "999"
        self.obj.addProperty("App::PropertyString", "max").max = "100000"
        if not hasattr(obj, "Boundary"):
            self.obj.addProperty("App::PropertyString", "Boundary")


def getObject():
    """
    创建obj并添加与MacroParticle相关的属性，然后返回obj
    """
    MacroParticleIns = MacroParticle()
    return MacroParticleIns.obj
