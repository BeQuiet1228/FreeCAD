#-*- coding: utf-8 -*-
import FreeCAD
from Modeling.Modeling2D.Tools import Tools2D
from Modeling.Modeling2D.Tools.Tools2D import ObjectType


class Port(object):
    def __init__(self):
        # self.obj = None
        FreeCAD.ActiveDocument.openTransaction("CreatePort")
        self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "LinePort")
        FreeCAD.ActiveDocument.commitTransaction()
        self.__setProperty(self.obj)
    
    def __setProperty(self, obj):
        # 此处type通过一个枚举类来进行赋值
        self.obj.addProperty("App::PropertyString", "Type").Type = ObjectType.PORT
        # stringList是一个列表，正投影面会有很多指定面
        self.obj.addProperty("App::PropertyString", "orthogonalProjectionPlane").orthogonalProjectionPlane = "未指定"
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
        # 增加表达式引擎，用于m2d判断起点和终点
        self.obj.addProperty("App::PropertyDistance", "helper").helper = 0
        Tools2D.addCommonStartEndCoordinate(obj)
        Tools2D.addCommonDirection(obj)
        Tools2D.addCommonPropertyToObject(obj)
        Tools2D.isNegativeOrPositive(obj)


def getObject():
    """
    创建obj并添加与Port相关的属性，然后返回obj
    """
    portIns = Port()
    return portIns.obj
