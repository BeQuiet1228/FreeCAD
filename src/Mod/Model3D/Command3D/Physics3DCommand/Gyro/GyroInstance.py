#-*- coding: utf-8 -*-
import FreeCAD
from Model3D.Tools import Tools3D, ObjectTools, InitDoc3D


class Gyro(object):
    def __init__(self):
        FreeCAD.ActiveDocument.openTransaction("CreateGyro_3D")
        self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "Emit_Gyro")
        self.__setProperty(self.obj)
        InitDoc3D.addObjectToGroup_helper(self.obj, "Launch", "发射处理")
        FreeCAD.ActiveDocument.commitTransaction()

    def __setProperty(self, obj):
        # 此处type通过一个枚举类来进行赋值
        self.obj.addProperty("App::PropertyString", "Type").Type = ObjectTools.ObjectType.GYRO
        # stringList是一个列表，类型箔片会有很多指定类型
        self.obj.addProperty("App::PropertyString", "emitter").emitter = "未指定"

        self.obj.addProperty("App::PropertyString", "beamCurrent").beamCurrent = "0.0"
        self.obj.addProperty("App::PropertyString", "guidingMagneticField").guidingMagneticField = "0"
        self.obj.addProperty("App::PropertyString", "guideRadius").guideRadius = "0"
        self.obj.addProperty("App::PropertyString", "longitudinalMomentum").longitudinalMomentum = "0"
        self.obj.addProperty("App::PropertyString", "theHorizontalMomentum").theHorizontalMomentum = "0"
        self.obj.addProperty("App::PropertyBool", "isCheckX").isCheckX = True
        self.obj.addProperty("App::PropertyBool", "isCheckY").isCheckY = False
        self.obj.addProperty("App::PropertyBool", "isCheckZ").isCheckZ = False

        self.obj.addProperty("App::PropertyString", "launchCenterCoordinatesX").launchCenterCoordinatesX = "0"
        self.obj.addProperty("App::PropertyString", "launchCenterCoordinatesY").launchCenterCoordinatesY = "0"
        self.obj.addProperty("App::PropertyString", "launchCenterCoordinatesZ").launchCenterCoordinatesZ = "0"

        self.obj.addProperty("App::PropertyBool", "isVelocityDistribution").isVelocityDistribution = False
        self.obj.addProperty("App::PropertyString", "velocityDistribution").velocityDistribution = "0"

        # 发射选项
        Tools3D.addLaunchOptionsCommonProperty(obj)
        if not hasattr(obj, "Boundary"):
            self.obj.addProperty("App::PropertyString", "Boundary")


def getObject():
    """
    创建obj并添加与Foil相关的属性，然后返回obj
    """
    gyroIns = Gyro()
    return gyroIns.obj