#-*- coding: utf-8 -*-
import FreeCAD
from Modeling.Modeling2D.Tools.Tools2D import ObjectType
from Modeling.Modeling2D.Tools import Tools2D


class Gyro(object):
    def __init__(self):
        FreeCAD.ActiveDocument.openTransaction("CreateGyro")
        self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "Emit_Gyro")
        FreeCAD.ActiveDocument.commitTransaction()
        self.__setProperty(self.obj)

    def __setProperty(self, obj):

        # 此处type通过一个枚举类来进行赋值
        self.obj.addProperty("App::PropertyString", "Type").Type = ObjectType.GYRO
        # stringList是一个列表，类型箔片会有很多指定类型
        self.obj.addProperty("App::PropertyString", "emitter").emitter = "未指定"

        self.obj.addProperty("App::PropertyString", "beamCurrent").beamCurrent = "0.0"
        self.obj.addProperty("App::PropertyString", "guidingMagneticField").guidingMagneticField = "0"
        self.obj.addProperty("App::PropertyString", "guideRadius").guideRadius = "0"
        self.obj.addProperty("App::PropertyString", "longitudinalMomentum").longitudinalMomentum = "0"
        self.obj.addProperty("App::PropertyString", "theHorizontalMomentum").theHorizontalMomentum = "0"
        self.obj.addProperty("App::PropertyBool", "isCheckX").isCheckX = True
        self.obj.addProperty("App::PropertyBool", "isCheckY").isCheckY = False

        self.obj.addProperty("App::PropertyString", "launchCenterCoordinatesX").launchCenterCoordinatesX = "0"
        self.obj.addProperty("App::PropertyString", "launchCenterCoordinatesY").launchCenterCoordinatesY = "0"

        # 发射选项
        Tools2D.addLaunchOptionsCommonProperty(obj)


def getObject():
    """
    创建obj并添加与Foil相关的属性，然后返回obj
    """
    gyroIns = Gyro()
    return gyroIns.obj
