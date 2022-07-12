#-*- coding: utf-8 -*-
import FreeCAD
from Modeling.Modeling2D.Tools import Tools2D
from Modeling.Modeling2D.Tools.Tools2D import ObjectType


class Inductor(object):
    def __init__(self):
        # self.obj = None
        FreeCAD.ActiveDocument.openTransaction("CreateInductor")
        self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "Inductor")
        FreeCAD.ActiveDocument.commitTransaction()
        self.__setProperty(self.obj)
    
    def __setProperty(self, obj):
        # 此处type通过一个枚举类来进行赋值
        self.obj.addProperty("App::PropertyString", "Type").Type = ObjectType.IND
        # stringList是一个列表，类型::电感会有很多指定类型
        self.obj.addProperty("App::PropertyString", "inductorType").inductorType = "未指定"
        self.obj.addProperty("App::PropertyString", "coilDiameter").coilDiameter = "1.0mm"         
        self.obj.addProperty("App::PropertyBool", "isCheckSelfInductor").isCheckSelfInductor = False
        self.obj.addProperty("App::PropertyString", "selfInductorCoefficient").selfInductorCoefficient = "0"
        Tools2D.addCommonStartEndCoordinate(obj)
        Tools2D.addCommonDirection(obj)

def getObject():
    """
    创建obj并添加与Foil相关的属性，然后返回obj
    """
    inductorIns = Inductor()
    return inductorIns.obj

