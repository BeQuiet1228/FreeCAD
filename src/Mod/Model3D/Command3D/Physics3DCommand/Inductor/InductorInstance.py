# -*- coding: utf-8 -*-
import FreeCAD
from Model3D.Tools import Tools3D, ObjectTools, InitDoc3D


class Inductor(object):
    def __init__(self):
        FreeCAD.ActiveDocument.openTransaction("CreateInductor_3D")
        self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "Inductor")
        self.__setProperty(self.obj)
        InitDoc3D.addObjectToGroup_helper(self.obj, "OtherModel", "其他模型")
        FreeCAD.ActiveDocument.commitTransaction()
    
    def __setProperty(self, obj):
        # 此处type通过一个枚举类来进行赋值
        self.obj.addProperty("App::PropertyString", "Type").Type = ObjectTools.ObjectType.IND
        # stringList是一个列表，类型::电感会有很多指定类型
        self.obj.addProperty("App::PropertyString", "inductorType").inductorType = "未指定"
        self.obj.addProperty("App::PropertyString", "coilDiameter").coilDiameter = "1.0mm"         
        self.obj.addProperty("App::PropertyBool", "isCheckSelfInductor").isCheckSelfInductor = False
        self.obj.addProperty("App::PropertyString", "selfInductorCoefficient").selfInductorCoefficient = "0"
        Tools3D.addCommonStartEndCoordinate(obj)
        Tools3D.addCommonDirection(obj)
        if not hasattr(obj, "Boundary"):
            self.obj.addProperty("App::PropertyString", "Boundary")

def getObject():
    """
    创建obj并添加与Foil相关的属性，然后返回obj
    """
    inductorIns = Inductor()
    return inductorIns.obj

