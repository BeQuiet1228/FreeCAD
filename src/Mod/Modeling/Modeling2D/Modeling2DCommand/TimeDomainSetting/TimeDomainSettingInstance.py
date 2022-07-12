# -*- coding:utf-8 -*-
# @Time: 2020/11/2 08:19
# @Author: lilei
# @File: TimeDomainSettingInstance.py
import FreeCAD
from Modeling.Modeling2D.Tools.Tools2D import ObjectType
from Modeling.Modeling2D.Tools import Tools2D


class TimeDomainSetting(object):

    def __init__(self):
        self.obj = FreeCAD.ActiveDocument.getObject("timeDomain")
        if self.obj is None:
            self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "timeDomain")
            self.__setProperty()

    def __setProperty(self):
        # 此处type通过一个枚举类来进行赋值
        self.obj.addProperty("App::PropertyString", "Type").Type = ObjectType.TimeDomain
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


def getObject():
    """
    创建obj并添加与Foil相关的属性，然后返回obj
    """
    timeDomainSettingIns = TimeDomainSetting()
    return timeDomainSettingIns.obj






