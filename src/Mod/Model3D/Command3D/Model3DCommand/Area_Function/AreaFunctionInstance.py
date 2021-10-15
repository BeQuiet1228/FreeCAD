# -*- coding: utf8 -*-
import FreeCADGui
import FreeCAD
import Part
from Model3D.Tools import Tools3D, ObjectTools, InitDoc3D
import PartChipic


class AreaFunction:
    def __init__(self, obj):
        GetProperty(obj)
        obj.Proxy = self

    def onChanged(self, fp, prop):
        pass

    def execute(self, fp):
        """
        函数面
        """
        sys = FreeCAD.ActiveDocument.CoordinateSystem
        # 获取工作区间
        x1 = fp.Point1X
        x2 = fp.Point2X
        y1 = fp.Point1Y
        y2 = fp.Point2Y
        z1 = fp.Point1Z
        z2 = fp.Point2Z
        x1 = FreeCAD.Units.Quantity(x1).Value
        x2 = FreeCAD.Units.Quantity(x2).Value
        y1 = FreeCAD.Units.Quantity(y1).Value
        y2 = FreeCAD.Units.Quantity(y2).Value
        z1 = FreeCAD.Units.Quantity(z1).Value
        z2 = FreeCAD.Units.Quantity(z2).Value
        Tools3D.sayz(str(z1)+"Z1的值\n")
        Tools3D.sayz(str(z2) + "Z2的值\n")
        if x1 == x2 or y1 == y2 or z1 == z2:
            Tools3D.sayz("坐标范围不能相同")
        try:
            fp.Shape = PartChipic.makeFuncMesh(10,  # type
                                               fp.Expression,  # func
                                               x1, x2,  # xMax, xMin
                                               y1, y2,  # yMax, yMin
                                               z1, z2,  # zMax, zMin
                                               sys,  # 坐标系
                                               str(fp.Precision),  # 精度
                                               fp.Attribute)  # 属性
        except:
            Tools3D.sayz("redraw AreaFunction fail")


class GetProperty:
    def __init__(self, obj):
        obj.addProperty("App::PropertyString", "Type").Type = ObjectTools.ObjectType.Area_Function
        if FreeCAD.ActiveDocument.CoordinateSystem == "Rectangular":
            obj.addProperty("App::PropertyDistance", "Point1X").Point1X = -0.01
            obj.addProperty("App::PropertyDistance", "Point1Y").Point1Y = -0.01
            obj.addProperty("App::PropertyDistance", "Point1Z").Point1Z = -0.01
            obj.addProperty("App::PropertyDistance", "Point2X").Point2X = 0.01
            obj.addProperty("App::PropertyDistance", "Point2Y").Point2Y = 0.01
            obj.addProperty("App::PropertyDistance", "Point2Z").Point2Z = 0.01
        elif FreeCAD.ActiveDocument.CoordinateSystem == "Polar":
            obj.addProperty("App::PropertyDistance", "Point1X").Point1X = 0
            obj.addProperty("App::PropertyAngle", "Point1Y").Point1Y = 0
            obj.addProperty("App::PropertyDistance", "Point1Z").Point1Z = 0
            obj.addProperty("App::PropertyDistance", "Point2X").Point2X = 0
            obj.addProperty("App::PropertyAngle", "Point2Y").Point2Y = 0
            obj.addProperty("App::PropertyDistance", "Point2Z").Point2Z = 0
        else:
            obj.addProperty("App::PropertyDistance", "Point1X").Point1X = 0
            obj.addProperty("App::PropertyDistance", "Point1Y").Point1Y = 0
            obj.addProperty("App::PropertyAngle", "Point1Z").Point1Z = 0
            obj.addProperty("App::PropertyDistance", "Point2X").Point2X = 0
            obj.addProperty("App::PropertyDistance", "Point2Y").Point2Y = 0
            obj.addProperty("App::PropertyAngle", "Point2Z").Point2Z = 0
        obj.addProperty("App::PropertyString", "Expression").Expression = "x+y+z-1"
        obj.addProperty("App::PropertyInteger", "Precision").Precision = 16
        Tools3D.addCommonProperty(obj)
        Tools3D.addAttributeToObject(obj)
        Tools3D.addHelperProperty(obj, 2)
        Tools3D.getHelperValue(obj)


def getObject():
    FreeCAD.ActiveDocument.openTransaction('CreateAreaFunction_3D')
    obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", ObjectTools.ObjectType.Area_Function)
    InitDoc3D.addObjectToGroup_helper(obj, "AreaG", "面")
    AreaFunction(obj)
    Tools3D.ViewProvider(obj.ViewObject)
    FreeCAD.ActiveDocument.commitTransaction()
    return obj

