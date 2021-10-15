# -*- coding: utf-8 -*-
import FreeCAD
from Model3D.Tools import Tools3D, ObjectTools, InitDoc3D


class Port(object):
    def __init__(self):
        FreeCAD.ActiveDocument.openTransaction("CreatePort_3D")
        self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "AreaPort")
        self.__setProperty(self.obj)
        InitDoc3D.addObjectToGroup_helper(self.obj, "WaveguidePort", "波导端口")
        FreeCAD.ActiveDocument.commitTransaction()

    def __setProperty(self, obj):
        # 此处type通过一个枚举类来进行赋值
        self.obj.addProperty("App::PropertyString", "Type").Type = ObjectTools.ObjectType.PORT
        # stringList是一个列表，正投影面会有很多指定面
        self.obj.addProperty("App::PropertyString", "orthogonalProjectionPlane").orthogonalProjectionPlane = u"未指定"
        self.obj.addProperty("App::PropertyBool", "isCheckVPORT").isCheckVPORT = False
        self.obj.addProperty("App::PropertyString", "VPORT").VPORT = "1"
        self.obj.addProperty("App::PropertyBool", "isCheckSCALE").isCheckSCALE = False
        self.obj.addProperty("App::PropertyString", "SCALE").SCALE = "1"
        self.obj.addProperty("App::PropertyBool", "isCheckFT").isCheckFT = False
        self.obj.addProperty("App::PropertyString", "FT").FT = "0.0"
        self.obj.addProperty("App::PropertyBool", "isCheckGE1").isCheckGE1 = False
        self.obj.addProperty("App::PropertyString", "GE1").GE1 = "0.0"
        self.obj.addProperty("App::PropertyBool", "isCheckGE2").isCheckGE2 = False
        self.obj.addProperty("App::PropertyString", "GE2").GE2 = "0.0"
        self.obj.addProperty("App::PropertyBool", "isCheckGE3").isCheckGE2 = False
        self.obj.addProperty("App::PropertyString", "GE3").GE3 = "0.0"
        self.obj.addProperty("App::PropertyBool", "isCheckNormalization").isCheckNormalization = False
        self.obj.addProperty("App::PropertyString", "normalization").normalization = "AreaPort.LINE"
        self.obj.addProperty("App::PropertyBool", "isCircuit").isCircuit = False
        self.obj.addProperty("App::PropertyString", "circuit").circuit = "0.002E-9"
        self.obj.addProperty("App::PropertyString", "observeName").observeName = "InputVoltage"
        self.obj.addProperty("App::PropertyBool", "isCheckLapras").isCheckLapras = False
        self.obj.addProperty("App::PropertyInteger", "laprasNumbers").laprasNumbers = 2
        self.obj.addProperty("App::PropertyString", "lapras1").lapras1 = "未指定"
        self.obj.addProperty("App::PropertyInteger", "lapras1Value").lapras1Value = 1
        self.obj.addProperty("App::PropertyString", "lapras2").lapras2 = "未指定"
        self.obj.addProperty("App::PropertyInteger", "lapras2Value").lapras2Value = 0
        self.obj.addProperty("App::PropertyString", "lapras3").lapras3 = "未指定"
        self.obj.addProperty("App::PropertyInteger", "lapras3Value").lapras3Value = 0
        self.obj.addProperty("App::PropertyString", "lapras4").lapras4 = "未指定"
        self.obj.addProperty("App::PropertyInteger", "lapras4Value").lapras4Value = 0
        self.obj.addProperty("App::PropertyString", "lapras5").lapras5 = "未指定"
        self.obj.addProperty("App::PropertyInteger", "lapras5Value").lapras5Value = 0
        # 增加表达式引擎，用于m3d判断起点和终点
        self.obj.addProperty("App::PropertyDistance", "helper").helper = 0
        self.obj.addProperty("App::PropertyAngle", "helper0").helper0 = 0
        if FreeCAD.ActiveDocument.CoordinateSystem == "Rectangular":
            self.obj.addProperty("App::PropertyDistance", "helper1").helper1 = 0
            self.obj.addProperty("App::PropertyDistance", "helper2").helper2 = 0
            self.obj.addProperty("App::PropertyDistance", "helper3").helper3 = 0
        elif FreeCAD.ActiveDocument.CoordinateSystem == "Polar":
            self.obj.addProperty("App::PropertyDistance", "helper1").helper1 = 0
            self.obj.addProperty("App::PropertyAngle", "helper2").helper2 = 0
            self.obj.addProperty("App::PropertyDistance", "helper3").helper3 = 0
        else:
            self.obj.addProperty("App::PropertyDistance", "helper1").helper1 = 0
            self.obj.addProperty("App::PropertyDistance", "helper2").helper2 = 0
            self.obj.addProperty("App::PropertyAngle", "helper3").helper3 = 0

        # self.obj.addProperty("App::PropertyDistance", "helper").helper = 0
        # self.obj.addProperty("App::PropertyDistance", "helper1").helper1 = 0
        # self.obj.addProperty("App::PropertyDistance", "helper2").helper2 = 0
        # self.obj.addProperty("App::PropertyDistance", "helper3").helper3 = 0
        Tools3D.addCommonStartEndCoordinate(obj)
        Tools3D.addCommonDirection(obj)
        Tools3D.addPhysicsProperty(obj)
        Tools3D.isNegativeOrPositive(obj)
        if not hasattr(obj, "Boundary"):
            self.obj.addProperty("App::PropertyString", "Boundary")


def getObject():
    """
    创建obj并添加与Port相关的属性，然后返回obj
    """
    portIns = Port()
    return portIns.obj