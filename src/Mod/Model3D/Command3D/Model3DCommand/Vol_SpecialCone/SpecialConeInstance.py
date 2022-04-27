# -*- coding: utf-8 -*-
import FreeCAD
import Part
from Model3D.Tools import Tools3D, ObjectTools, InitDoc3D


class CreateSpecialCone:
    def __init__(self, obj):
        obj.Proxy = self

    def onChanged(self, fp, prop):
        pass

    def execute(self, fp):
        # 先排除高等于零即两点重合的错误情况，再排除上下半径均为零的错误情况，然后直接调用建模。
        point1 = Tools3D.transToRecVector(fp.Point1X.Value, fp.Point1Y.Value, fp.Point1Z.Value)
        point2 = Tools3D.transToRecVector(fp.Point2X.Value, fp.Point2Y.Value, fp.Point2Z.Value)
        vector = point2 - point1
        height = point1.distanceToPoint(point2)
        # 上下半径相等为圆柱，也可以按圆台画法绘制
        # 圆环
        try:
            if height == 0:
                # 警告用户数据错误及错误原因
                Tools3D.sayz("错误，高不能等于零")
                pass
        # 圆环，台，锥
            else:
                if fp.Radius_Bottom == 0 and fp.Radius_Top == 0:
                    # 警告用户数据错误及错误原因
                    Tools3D.sayz("错误。上下半径不能同时等于零")
                    pass
                    # fp.Shape = Part.makeCylinder(fp.Radius_Bottom.Value, height, point1, vector, 360)
                elif fp.Radius_Bottom < 0 or fp.Radius_Top < 0:
                    Tools3D.sayz("错误。上下半径不能小于零")
                elif fp.Radius_Bottom == fp.Radius_Top:
                    fp.Shape = Part.makeCylinder(fp.Radius_Bottom.Value, height, point1, vector, 360)
                else:
                    fp.Shape = Part.makeCone(fp.Radius_Bottom.Value, fp.Radius_Top.Value, height, point1, vector)
        except:
            Tools3D.sayz("Redraw SpecialCone Failed!")


class SpecialCone:
    """
    工厂类
    """
    def __init__(self):
        FreeCAD.ActiveDocument.openTransaction('Create_3D_SpecialCone')
        self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "Vol_SpecialCone")
        self.__setProperty(self.obj)
        InitDoc3D.addObjectToGroup_helper(self.obj, "SpecialCone", "圆锥体")
        FreeCAD.ActiveDocument.commitTransaction()

    def __setProperty(self, obj):
        obj.addProperty("App::PropertyString", "Type").Type = ObjectTools.ObjectType.Vol_SpecialCone
        if FreeCAD.ActiveDocument.CoordinateSystem == "Rectangular":
            obj.addProperty("App::PropertyDistance", "Point1X", "Cone", " centre point1 X").Point1X = 0
            obj.addProperty("App::PropertyDistance", "Point1Y", "Cone", " centre point1 Y").Point1Y = 0
            obj.addProperty("App::PropertyDistance", "Point1Z", "Cone", " centre point1 Z").Point1Z = 0
            obj.addProperty("App::PropertyDistance", "Point2X", "Cone", " centre point2 X").Point2X = 0
            obj.addProperty("App::PropertyDistance", "Point2Y", "Cone", " centre point2 Y").Point2Y = 0
            obj.addProperty("App::PropertyDistance", "Point2Z", "Cone", " centre point2 Z").Point2Z = 0.01
        elif FreeCAD.ActiveDocument.CoordinateSystem == "Polar":
            obj.addProperty("App::PropertyDistance", "Point1X", "Cone", " centre point1 X").Point1X = 0
            obj.addProperty("App::PropertyAngle", "Point1Y", "Cone", " centre point1 Y").Point1Y = 0
            obj.addProperty("App::PropertyDistance", "Point1Z", "Cone", " centre point1 Z").Point1Z = 0
            obj.addProperty("App::PropertyDistance", "Point2X", "Cone", " centre point2 X").Point2X = 0
            obj.addProperty("App::PropertyAngle", "Point2Y", "Cone", " centre point2 Y").Point2Y = 360
            obj.addProperty("App::PropertyDistance", "Point2Z", "Cone", " centre point2 Z").Point2Z = 0
        else:
            obj.addProperty("App::PropertyDistance", "Point1X", "Cone", " centre point1 X").Point1X = 0
            obj.addProperty("App::PropertyDistance", "Point1Y", "Cone", " centre point1 Y").Point1Y = 0
            obj.addProperty("App::PropertyAngle", "Point1Z", "Cone", " centre point1 Z").Point1Z = 0
            obj.addProperty("App::PropertyDistance", "Point2X", "Cone", " centre point2 X").Point2X = 0
            obj.addProperty("App::PropertyDistance", "Point2Y", "Cone", " centre point2 Y").Point2Y = 0
            obj.addProperty("App::PropertyAngle", "Point2Z", "Cone", " centre point2 Z").Point2Z = 360
        obj.addProperty("App::PropertyLength", "Radius_Bottom", "Cone", "Radius_Bottom").Radius_Bottom = 0.02
        obj.addProperty("App::PropertyLength", "Radius_Top", "Cone", "Radius_Top").Radius_Top = 0.01
        Tools3D.addCommonPropertyToObject(obj)
        Tools3D.addAttributeToObject(obj)
        Tools3D.addHelperProperty(obj, 2)
        Tools3D.getHelperValue(obj)
        Tools3D.addRadiusProperty(obj)
        Tools3D.getRadiusProperty(obj)


def getObject():
    specialCone = SpecialCone()
    CreateSpecialCone(specialCone.obj)
    Tools3D.ViewProvider(specialCone.obj.ViewObject)
    return specialCone.obj
