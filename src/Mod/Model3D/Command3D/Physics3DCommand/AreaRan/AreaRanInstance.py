# -*- coding: utf-8 -*-
import FreeCAD
from Model3D.Tools import Tools3D, ObjectTools, InitDoc3D


class AreaRan(object):
    def __init__(self):
        FreeCAD.ActiveDocument.openTransaction("CreateAreaRan_3D")
        self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", ObjectTools.ObjectType.AreaRan)
        self.__setProperty(self.obj)
        InitDoc3D.addObjectToGroup_helper(self.obj, "AreaObs", "空间观测")
        FreeCAD.ActiveDocument.commitTransaction()

    def __setProperty(self, obj):
        # 此处type通过一个枚举类来进行赋值
        self.obj.addProperty("App::PropertyString", "Type").Type = ObjectTools.ObjectType.AreaRan
        self.obj.addProperty("App::PropertyString", "orthogonalProjectionLine").orthogonalProjectionLine = "未指定"
        self.obj.addProperty("App::PropertyBool", "isField").isField = True
        self.obj.addProperty("App::PropertyBool", "isFieldIntegral").isFieldIntegral = False
        self.obj.addProperty("App::PropertyBool", "isFieldPower").isFieldPower = False
        self.obj.addProperty("App::PropertyBool", "isFieldEnergy").isFieldEnergy = False
        # 分类子项有多种
        self.obj.addProperty("App::PropertyString", "field").field = "E1"
        self.obj.addProperty("App::PropertyString", "fieldIntegral").fieldIntegral = "E.DL"
        self.obj.addProperty("App::PropertyString", "fieldPower").fieldPower = "S.DA"
        self.obj.addProperty("App::PropertyString", "fieldEnergy").fieldEnergy = "EM"
        self.obj.addProperty("App::PropertyBool", "isFFT").isFFT = False
        self.obj.addProperty("App::PropertyBool", "isRealAnalysis").isRealAnalysis = True
        self.obj.addProperty("App::PropertyBool", "isComplexAnalysis").isComplexAnalysis = False
        obj.addProperty("App::PropertyBool", "isParticle").isParticle = False
        obj.addProperty("App::PropertyString", "chooseParticle").chooseParticle = "CURRENT"
        obj.addProperty("App::PropertyString", "particleType").particleType = "ELECTRON"
        obj.addProperty("App::PropertyString", "particleAxis").particleAxis = "X1"
        self.obj.addProperty("App::PropertyString", "timer").timer = "默认定时器"
        Tools3D.addCommonStartEndCoordinate(obj)
        Tools3D.addCommonDirection(obj)
        if not hasattr(obj, "Observation"):
            self.obj.addProperty("App::PropertyString", "Observation")


def getObject():
    """
    创建obj并添加与AreaRan相关的属性，然后返回obj
    """
    areaRanIns = AreaRan()
    return areaRanIns.obj
