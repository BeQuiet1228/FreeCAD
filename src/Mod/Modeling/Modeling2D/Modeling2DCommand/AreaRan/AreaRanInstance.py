# -*- coding: utf-8 -*-
import FreeCAD
from Modeling.Modeling2D.Tools import Tools2D
from Modeling.Modeling2D.Tools.Tools2D import ObjectType


class AreaRan(object):
    def __init__(self):
        # self.obj = None
        FreeCAD.ActiveDocument.openTransaction("CreateAreaRan")
        self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "AreaRan")
        FreeCAD.ActiveDocument.commitTransaction()
        self.__setProperty(self.obj)

    def __setProperty(self, obj):
        # 此处type通过一个枚举类来进行赋值
        self.obj.addProperty("App::PropertyString", "Type").Type = ObjectType.AreaRan
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
        self.obj.addProperty("App::PropertyString", "timer").timer = "默认定时器"
        Tools2D.addCommonStartEndCoordinate(obj)
        Tools2D.addCommonDirection(obj)


def getObject():
    """
    创建obj并添加与AreaRan相关的属性，然后返回obj
    """
    areaRanIns = AreaRan()
    return areaRanIns.obj


def completionProperties(obj):
    obj.addProperty("App::PropertyBool", "isParticle").isParticle = False
    obj.addProperty("App::PropertyString", "chooseParticle").chooseParticle = "CURRENT"
    obj.addProperty("App::PropertyString", "particleType").particleType = "ELECTRON"
    obj.addProperty("App::PropertyString", "particleAxis").particleAxis = "X1"
