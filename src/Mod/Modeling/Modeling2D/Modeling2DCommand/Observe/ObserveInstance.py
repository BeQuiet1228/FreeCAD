# -*- coding:utf-8 -*-
import FreeCAD
from Modeling.Modeling2D.Tools import Tools2D
from Modeling.Modeling2D.Tools.Tools2D import ObjectType


class Observe(object):
    def __init__(self):
        # self.obj = None
        FreeCAD.ActiveDocument.openTransaction("CreateObserve")
        self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "Observe")
        FreeCAD.ActiveDocument.commitTransaction()
        self.__setProperty(self.obj)

    def __setProperty(self, obj):
        # 此处type通过一个枚举类来进行赋值
        self.obj.addProperty("App::PropertyString", "Type").Type = ObjectType.Observe
        # 观测类型有多种，用StringList
        self.obj.addProperty("App::PropertyString", "ObservationType").ObservationType = "时间观测点"
        # 根据观测类型选择对应的点，线，面
        self.obj.addProperty("App::PropertyString", "optionType").optionType = "未指定"
        self.obj.addProperty("App::PropertyString", "alias").alias = ""
        self.obj.addProperty("App::PropertyBool", "isField").isField = True
        self.obj.addProperty("App::PropertyBool", "isFieldIntegral").isFieldIntegral = False
        self.obj.addProperty("App::PropertyBool", "isFieldPower").isFieldPower = False
        self.obj.addProperty("App::PropertyBool", "isFieldEnergy").isFieldEnergy = False
        self.obj.addProperty("App::PropertyBool", "isParticleStatistics").isParticleStatistics = False
        self.obj.addProperty("App::PropertyBool", "isCollectedParticles").isCollectedParticles = False
        self.obj.addProperty("App::PropertyBool", "isEmittedParticle").isEmittedParticle = False
        self.obj.addProperty("App::PropertyBool", "isAnnihilatingParticle").isAnnihilatingParticle = False
        # 分类子项有多种，所以用StringList
        self.obj.addProperty("App::PropertyString", "field").field = "E1"
        self.obj.addProperty("App::PropertyString", "fieldIntegral").fieldIntegral ="E.DL"
        self.obj.addProperty("App::PropertyString", "fieldPower").fieldPower = "S.DA"
        self.obj.addProperty("App::PropertyString", "fieldEnergy").fieldEnergy = "EM"
        # 根据所选的粒子类型对应的粒子
        self.obj.addProperty("App::PropertyString", "particles1").particles1 = "phase1"
        self.obj.addProperty("App::PropertyString", "particles2").particles2 = "EMIT_EPS"
        self.obj.addProperty("App::PropertyString", "particles3").particles3 = "CHARGE"
        self.obj.addProperty("App::PropertyString", "particles4").particles4 = "ELECTRON"
        self.obj.addProperty("App::PropertyBool", "isFFT").isFFT = False
        self.obj.addProperty("App::PropertyBool", "isRealAnalysis").isRealAnalysis = True
        self.obj.addProperty("App::PropertyBool", "isComplexAnalysis").isComplexAnalysis = False
        self.obj.addProperty("App::PropertyBool", "isFrequencyRange").isFrequencyRange = False
        self.obj.addProperty("App::PropertyString", "frequencyRange1").frequencyRange1 = "0"
        self.obj.addProperty("App::PropertyString", "frequencyRange2").frequencyRange2 = "0"
        self.obj.addProperty("App::PropertyBool", "isTimeRange").isTimeRange = False
        self.obj.addProperty("App::PropertyString", "timeRange1").timeRange1 = "0"
        self.obj.addProperty("App::PropertyString", "timeRange2").timeRange2 = "10"
        self.obj.addProperty("App::PropertyBool", "isObservationInterval").isObservationInterval = False
        self.obj.addProperty("App::PropertyString", "observationInterval").observationInterval = ""
        self.obj.addProperty("App::PropertyBool", "isDataDisplay").isDataDisplay = False
        self.obj.addProperty("App::PropertyBool", "isTimeAverage").isTimeAverage = True
        self.obj.addProperty("App::PropertyBool", "isRcAnalyze").isRcAnalyze = False
        self.obj.addProperty("App::PropertyString", "filteringTimeParameter").filteringTimeParameter = "0.05"
        Tools2D.addCommonStartEndCoordinate(obj)
        Tools2D.addCommonDirection(obj)


def getObject():
    """
    创建obj并添加与Observe相关的属性，然后返回obj
    """
    observeIns = Observe()
    return observeIns.obj
