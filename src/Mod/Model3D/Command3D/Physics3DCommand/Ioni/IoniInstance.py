# -*- coding: utf-8 -*-
import FreeCAD
from Model3D.Tools import ObjectTools, InitDoc3D, Tools3D


class Ioni(object):
    def __init__(self):
        FreeCAD.ActiveDocument.openTransaction("CreateIoni_3D")
        self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", ObjectTools.ObjectType.IONI)
        self.__setProperty(self.obj)
        InitDoc3D.addObjectToGroup_helper(self.obj, "Launch", "发射处理")
        FreeCAD.ActiveDocument.commitTransaction()

    def __setProperty(self, obj):
        # 此处type通过一个枚举类来进行赋值
        self.obj.addProperty("App::PropertyString", "Type").Type = ObjectTools.ObjectType.IONI
        # stringList是一个列表，类型箔片会有很多指定类型
        self.obj.addProperty("App::PropertyString", "ionizationOfGas").ionizationOfGas = "ARGON"
        self.obj.addProperty("App::PropertyString", "ioniType").ioniType = "未指定"
        self.obj.addProperty("App::PropertyString", "gasPressure").gasPressure = "1333.22"
        self.obj.addProperty("App::PropertyString", "gasTemperature").gasTemperature = "300"
        self.obj.addProperty("App::PropertyString", "GPreTimeFunction").GPreTimeFunction = "GPreTime"
        Tools3D.addCommonStartEndCoordinate(obj)
        if not hasattr(obj, "Boundary"):
            self.obj.addProperty("App::PropertyString", "Boundary")


def getObject():
    """
    创建obj并添加与Foil相关的属性，然后返回obj
    """
    ioniIns = Ioni()
    return ioniIns.obj
