#-*- coding: utf-8 -*-
import FreeCAD
from Modeling.Modeling2D.Tools.Tools2D import ObjectType
from Modeling.Modeling2D.Tools import Tools2D


class Secd(object):
    def __init__(self):
        FreeCAD.ActiveDocument.openTransaction("CreateEmSE")
        self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "EmSE")
        FreeCAD.ActiveDocument.commitTransaction()
        self.__setProperty(self.obj)

    def __setProperty(self, obj):

        # 此处type通过一个枚举类来进行赋值
        self.obj.addProperty("App::PropertyString", "Type").Type = ObjectType.SECD
        # stringList是一个列表，类型箔片会有很多指定类型
        self.obj.addProperty("App::PropertyString", "emitter").emitter = "未指定"

        self.obj.addProperty("App::PropertyString", "maximumEmissionFactor").maximumEmissionFactor = "2"
        self.obj.addProperty("App::PropertyString", "maximumEmissionFactorEnergy").maximumEmissionFactorEnergy = "400"

        self.obj.addProperty("App::PropertyBool", "isWeightCoefficient").isWeightCoefficient = False
        self.obj.addProperty("App::PropertyString", "weightCoefficient").weightCoefficient = "1"

        self.obj.addProperty("App::PropertyBool", "isEnergyDistribution").isEnergyDistribution = False
        self.obj.addProperty("App::PropertyString", "energyDistribution").energyDistribution = ""
        self.obj.addProperty("App::PropertyString", "minimumEnergy").minimumEnergy = ""
        self.obj.addProperty("App::PropertyString", "maximumEnergy").maximumEnergy = ""
        self.obj.addProperty("App::PropertyBool", "isAngularDistribution").isAngularDistribution = False
        self.obj.addProperty("App::PropertyString", "angularDistribution").angularDistribution = ""
        # 发射选项
        Tools2D.addLaunchOptionsCommonProperty(obj)


def getObject():
    """
    创建obj并添加与Foil相关的属性，然后返回obj
    """
    secdIns = Secd()
    return secdIns.obj
