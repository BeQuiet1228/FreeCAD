#-*- coding: utf-8 -*-
import FreeCAD
from Modeling.Modeling2D.Tools.Tools2D import ObjectType
from Modeling.Modeling2D.Tools import Tools2D


class Ioni(object):
    def __init__(self):
        FreeCAD.ActiveDocument.openTransaction("CreateGasgas")
        self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "Gasgas")
        FreeCAD.ActiveDocument.commitTransaction()
        self.__setProperty()

    def __setProperty(self):
        # 此处type通过一个枚举类来进行赋值
        self.obj.addProperty("App::PropertyString", "Type").Type = ObjectType.IONI
        # stringList是一个列表，类型箔片会有很多指定类型

        self.obj.addProperty("App::PropertyString", "ionizationOfGas").ionizationOfGas = "ARGON"
        self.obj.addProperty("App::PropertyString", "gasPressure").gasPressure = "1333.22"
        self.obj.addProperty("App::PropertyString", "gasTemperature").gasTemperature = "300"


def getObject():
    """
    创建obj并添加与Foil相关的属性，然后返回obj
    """
    ioniIns = Ioni()
    return ioniIns.obj
