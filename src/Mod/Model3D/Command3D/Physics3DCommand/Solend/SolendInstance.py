#-*- coding: utf-8 -*-
import FreeCAD
from Model3D.Tools import ObjectTools, InitDoc3D


class Solend(object):
    def __init__(self):
        FreeCAD.ActiveDocument.openTransaction("CreateSolend_3D")
        self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "Solend")
        self.__setProperty()
        InitDoc3D.addObjectToGroup_helper(self.obj, "OtherModel", "其他模型")
        FreeCAD.ActiveDocument.commitTransaction()


    def __setProperty(self):

        # 此处type通过一个枚举类来进行赋值
        self.obj.addProperty("App::PropertyString", "Type").Type = ObjectTools.ObjectType.SOLE
        # stringList是一个列表，类型箔片会有很多指定类型
        self.obj.addProperty("App::PropertyString", "uniformParam").uniformParam = "None"
        self.obj.addProperty("App::PropertyString", "coreZ").coreZ = "0"
        self.obj.addProperty("App::PropertyString", "coreR").coreR = "0"
        self.obj.addProperty("App::PropertyString", "coilHalf").coilHalf = "0"
        self.obj.addProperty("App::PropertyString", "innerRadius").innerRadius = "0"
        self.obj.addProperty("App::PropertyString", "outerRadius").outerRadius = "0"
        self.obj.addProperty("App::PropertyString", "turnRatio").turnRatio = "0"
        self.obj.addProperty("App::PropertyBool", "isMarkX", "NonUniformGrid", "").isMarkX = True
        self.obj.addProperty("App::PropertyBool", "isMarkY", "NonUniformGrid", "").isMarkY = True
        self.obj.addProperty("App::PropertyBool", "isMarkZ", "NonUniformGrid", "").isMarkZ = True
        self.obj.addProperty("App::PropertyString", "MarkX", "NonUniformGrid", "").MarkX = "DX1"
        self.obj.addProperty("App::PropertyString", "MarkY", "NonUniformGrid", "").MarkY = "DX2"
        self.obj.addProperty("App::PropertyString", "MarkZ", "NonUniformGrid", "").MarkZ = "DX3"
        self.obj.addProperty("App::PropertyString", "factorZ").factorZ = "0"
        self.obj.addProperty("App::PropertyString", "factorR").factorR = "0"
        self.obj.addProperty("App::PropertyString", "dutyCycle").dutyCycle = "0"
        self.obj.addProperty("App::PropertyString", "radiusInner").radiusInner = "0"
        self.obj.addProperty("App::PropertyString", "radiusOuter").radiusOuter = "0"
        self.obj.addProperty("App::PropertyString", "permeability").permeability = "0"
        self.obj.addProperty("App::PropertyString", "coilCurrent").coilCurrent = "0"
        self.obj.addProperty("App::PropertyString", "angleTheta").angleTheta = "0"
        self.obj.addProperty("App::PropertyString", "anglePhi").anglePhi = "0"
        if not hasattr(self.obj, "Boundary"):
            self.obj.addProperty("App::PropertyString", "Boundary")


def getObject():
    """
    创建obj并添加与Foil相关的属性，然后返回obj
    """
    solendIns = Solend()
    return solendIns.obj