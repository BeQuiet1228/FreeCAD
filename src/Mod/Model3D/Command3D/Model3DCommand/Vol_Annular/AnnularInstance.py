# -*- coding: utf8 -*-
import FreeCAD
import Part
from Model3D.Tools import Tools3D, ObjectTools, InitDoc3D


class VolAnnular:
    def __init__(self, obj):
        obj.Proxy = self

    def onChanged(self, fp, prop):
        pass

    def execute(self, fp):
        """
        环形体
        绘制方式：画出两个圆组成环形面，由point1到point2方向延长环形面
        1.考虑point1和point2两个点不能重合
        2.内外半径不能小于等于0,并且内半径小于外半径
        """
        point1 = Tools3D.transToRecVector(fp.Point1X.Value, fp.Point1Y.Value, fp.Point1Z.Value)
        point2 = Tools3D.transToRecVector(fp.Point2X.Value, fp.Point2Y.Value, fp.Point2Z.Value)
        dir = point2 - point1
        if not dir.Length:
            Tools3D.sayz(u"point1和point2重合，请重新输入!")
            return

        if fp.Radius1.Value < 0 or fp.Radius2.Value <= 0 or fp.Radius1.Value >= fp.Radius2.Value:
            Tools3D.sayz("半径有误，请重新输入")
            return
        if fp.Radius1.Value == 0:
            # 内半径为0的情况，建模为圆柱
            fp.Shape = Part.makeCylinder(fp.Radius2.Value, dir.Length, point1, dir, 360)
            return

        e1 = Part.makeCircle(fp.Radius1, point1, dir)
        e2 = Part.makeCircle(fp.Radius2, point1, dir)
        wires = [e1, e2]
        try:
            line = Part.makeLine(point1, point2)
            path = Part.Wire(line)
            shapeCircle = Part.makeFace(wires, "Part::FaceMakerBullseye")
            fp.Shape = path.makePipe(shapeCircle)
            return
        except:
            Tools3D.sayz("Redraw Annular Failed!")


class GetProperty:
    def __init__(self):
        FreeCAD.ActiveDocument.openTransaction('CreateVolAnnular_3D')
        self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", ObjectTools.ObjectType.Vol_Annular)
        self.__setProperty(self.obj)
        InitDoc3D.addObjectToGroup_helper(self.obj, "Annular", "环形体")
        FreeCAD.ActiveDocument.commitTransaction()

    def __setProperty(self, obj):
        obj.addProperty("App::PropertyString", "Type").Type = ObjectTools.ObjectType.Vol_Annular
        if FreeCAD.ActiveDocument.CoordinateSystem == "Rectangular":
            obj.addProperty("App::PropertyDistance", "Point1X").Point1X = 0
            obj.addProperty("App::PropertyDistance", "Point1Y").Point1Y = 0
            obj.addProperty("App::PropertyDistance", "Point1Z").Point1Z = 0
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

        obj.addProperty("App::PropertyDistance", "Radius1").Radius1 = 0.005
        obj.addProperty("App::PropertyDistance", "Radius2").Radius2 = 0.01
        Tools3D.addCommonPropertyToObject(obj)
        Tools3D.addAttributeToObject(obj)
        Tools3D.addHelperProperty(obj, 2)
        Tools3D.getHelperValue(obj)
        Tools3D.addRadiusProperty(obj)
        Tools3D.getRadiusProperty(obj)


def getObject():
    """
    返回获取的obj
    """
    volAnnularObj = GetProperty()
    VolAnnular(volAnnularObj.obj)
    Tools3D.ViewProvider(volAnnularObj.obj.ViewObject)
    return volAnnularObj.obj
