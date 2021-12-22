# -*- coding: utf-8 -*-
import FreeCAD

from Modeling.Modeling2D.Tools import Tools2D


class MacroParticle(object):
    def __init__(self):
        # self.obj = None
        FreeCAD.ActiveDocument.openTransaction("CreateMacroParticle")
        self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "MacroParticle")
        FreeCAD.ActiveDocument.commitTransaction()
        self.__setProperty()

    def __setProperty(self):
        # 此处type通过一个枚举类来进行赋值
        self.obj.addProperty("App::PropertyString", "Type").Type = Tools2D.ObjectType.MarcoParticle
        self.obj.addProperty("App::PropertyBool", "isMacroParticle").isMacroParticle = False
        self.obj.addProperty("App::PropertyString", "typeOfParticles").typeOfParticles = "ALL"
        self.obj.addProperty("App::PropertyString", "particleNumber").particleNumber = "1"
        self.obj.addProperty("App::PropertyString", "macroParticleNumber").macroParticleNumber = "5000"


def getObject():
    """
    创建obj并添加与MacroParticle相关的属性，然后返回obj
    """
    macroParticleIns = MacroParticle()
    return macroParticleIns.obj

