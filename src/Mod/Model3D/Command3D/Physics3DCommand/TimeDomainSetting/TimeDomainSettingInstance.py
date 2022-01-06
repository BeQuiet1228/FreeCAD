# -*- coding: utf-8 -*-
import FreeCAD
from Model3D.Tools import ObjectTools, InitDoc3D


class TimeDomainSetting(object):

    def __init__(self):
        self.obj = FreeCAD.ActiveDocument.getObject("TimeDomainSetting")
        if self.obj is None:
            self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "TimeDomainSetting")
            self.__setProperty()
        InitDoc3D.addObjectToGroup_helper(self.obj, "TimeDomain", "时域计算设置")

    def __setProperty(self):
        # 此处type通过一个枚举类来进行赋值
        self.obj.addProperty("App::PropertyString", "Type").Type = ObjectTools.ObjectType.TimeDomain
        self.obj.addProperty("App::PropertyString", "computationTime").computationTime = "20"
        self.obj.addProperty("App::PropertyString", "fieldAlgorithm").fieldAlgorithm = "时偏FDTD"
        self.obj.addProperty("App::PropertyBool", "isSettingPattern").isSettingPattern = False
        self.obj.addProperty("App::PropertyBool", "isEM").isEM = True
        self.obj.addProperty("App::PropertyBool", "isTE").isTE = False
        self.obj.addProperty("App::PropertyBool", "isTM").isTM = False
        self.obj.addProperty("App::PropertyBool", "isSetStep").isSetStep = False
        self.obj.addProperty("App::PropertyString", "setStep").setStep = "0.01"
        self.obj.addProperty("App::PropertyBool", "isSetAlgorithm").isSetAlgorithm = False
        self.obj.addProperty("App::PropertyBool", "isParticleCalculatesTimeStepInterval").isParticleCalculatesTimeStepInterval = False
        self.obj.addProperty("App::PropertyString", "particleCalculatesTimeStepInterval").particleCalculatesTimeStepInterval = "1"
        self.obj.addProperty("App::PropertyBool", "isNonrelativistic").isNonrelativistic = True
        self.obj.addProperty("App::PropertyBool", "isRelativistic").isRelativistic = False
        if not hasattr(self.obj, "Project"):
            self.obj.addProperty("App::PropertyString", "Project")

        # 宏粒子合并对应属性
        # self.obj.addProperty("App::PropertyBool", "isMacroParticle").isMacroParticle = False
        # self.obj.addProperty("App::PropertyString", "particleType").particleType = "ALL"
        # self.obj.addProperty("App::PropertyString", "every").every = "1"
        # self.obj.addProperty("App::PropertyString", "max").max = "50000"


def getObject():
    timeDomainSettingIns = TimeDomainSetting()
    return timeDomainSettingIns.obj






