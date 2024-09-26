# -*- coding: utf-8 -*-
import FreeCAD
from Model3D.Tools import ObjectTools, InitDoc3D


class PhasSpace(object):
    def __init__(self):
        # self.obj = None
        FreeCAD.ActiveDocument.openTransaction("CreatePhasSpace_3D")
        self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", ObjectTools.ObjectType.PhasSpace)
        self.__setProperty()
        InitDoc3D.addObjectToGroup_helper(self.obj, "ParticleObs", "粒子观测")
        FreeCAD.ActiveDocument.commitTransaction()

    def __setProperty(self):
        # 此处type通过一个枚举类来进行赋值
        self.obj.addProperty("App::PropertyString", "Type").Type = ObjectTools.ObjectType.PhasSpace
        # 观测粒子有多种，所以用StringList
        self.obj.addProperty("App::PropertyString", "observationParticle").observationParticle = "全部"
        # 有多种定时器，所以用StringList
        self.obj.addProperty("App::PropertyString", "timer").timer = "默认定时器"
        # 横轴显示，纵轴显示有多种选项
        self.obj.addProperty("App::PropertyString", "horizontalAxisShow").horizontalAxisShow = "X1"
        self.obj.addProperty("App::PropertyString", "verticalAxisShow").verticalAxisShow = "X1"
        self.obj.addProperty("App::PropertyBool", "isShowThickness").isShowThickness = False
        self.obj.addProperty("App::PropertyString", "showThick").showThick = "X1"
        self.obj.addProperty("App::PropertyString", "thickValue1").thickValue1 = "0"
        self.obj.addProperty("App::PropertyString", "thickValue2").thickValue2 = "0"
        self.obj.addProperty("App::PropertyBool", "isSuffix").isSuffix = False
        self.obj.addProperty("App::PropertyString", "suffix").suffix = "phase1"
        self.obj.addProperty("App::PropertyBool", "isCROSS").isCROSS = False
        self.obj.addProperty("App::PropertyString", "CROSS").CROSS = "0"
        if not hasattr(self.obj, "Observation"):
            self.obj.addProperty("App::PropertyString", "Observation")


def getObject():
    """
    创建obj并添加与PhasSpace相关的属性，然后返回obj
    """
    phasSpaceIns = PhasSpace()
    return phasSpaceIns.obj
