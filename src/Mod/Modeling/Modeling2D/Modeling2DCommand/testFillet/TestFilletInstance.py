# -*- coding: utf8 -*-
import make_fiilet
import FreeCAD as App
import FreeCAD
import Part
import math
from Model3D.Tools import Tools3D, ObjectTools, InitDoc3D
from Modeling.Modeling2D.Tools import Tools2D, ToolsUI

class AreaFillet:
    def __init__(self, obj):
        GetProperty(obj)
        obj.Proxy = self

    def onChanged(self, fp, prop):
        pass

    def execute(self, fp):
        """
        函数面
        """
        p1 = App.Vector(fp.Point1X, fp.Point1Y, 0)
        p2 = App.Vector(fp.Point2X, fp.Point2Y, 0)
        p3 = App.Vector(fp.Point3X, fp.Point3Y, 0)

        line1 = Part.LineSegment(p1, p2)
        line2 = Part.LineSegment(p2, p3)
        line3 = Part.LineSegment(p3, p1)
        line1 = line1.toShape()
        line2 = line2.toShape()
        line3 = line3.toShape()
        arc_list = make_fiilet.fillet([line1, line2], fp.Radius, False)
        arc_point1 = arc_list[0]
        arc_point2 = arc_list[1]
        arc_point3 = arc_list[2]
        arc_center = arc_list[3]
        Tools3D.sayz("arc_point1=" + str(arc_point1))
        Tools3D.sayz("arc_point2=" + str(arc_point2))
        Tools3D.sayz("arc_point3=" + str(arc_point3))
        Tools3D.sayz("arc_center1=" + str(arc_center))
        right_vec = arc_point1.sub(arc_center)
        left_vec = arc_point3.sub(arc_center)
        Tools3D.sayz("right_vec=" + str(right_vec))
        Tools3D.sayz("left_vec=" + str(left_vec))
        Tools3D.sayz("arc_center2=" + str(arc_center))
        start_angle = math.atan2(right_vec.y, right_vec.x)
        end_angle = math.atan2(left_vec.y, left_vec.x)
        if end_angle < 0:
            end_angle += 2 * math.pi

        # 测试倒角是否能正确生成
        from Modeling.Modeling2D.Modeling2DCommand.Fillet import FilletInstance
        fillet = FilletInstance.getObject()
        fillet.user_radius = str(fp.Radius)
        fillet.user_point1_x = str(arc_center.x)
        fillet.user_point1_y = str(arc_center.y)
        fillet.user_point2_x = str(p2.x)
        fillet.user_point2_y = str(p2.y)
        fillet.user_startAngle = str(start_angle*180/math.pi)
        fillet.user_endAngle = str(end_angle*180/math.pi)

        fillet.Attribute = "Void"
        ToolsUI.setPlaceToObj(fillet, "Point1X", fillet.user_point1_x)
        ToolsUI.setPlaceToObj(fillet, "Point1Y", fillet.user_point1_y)
        ToolsUI.setPlaceToObj(fillet, "Point2X", fillet.user_point2_x)
        ToolsUI.setPlaceToObj(fillet, "Point2Y", fillet.user_point2_y)
        ToolsUI.setPlaceToObj(fillet, "Radius", fillet.user_radius)
        ToolsUI.setAngleToObj(fillet, "StartAngle", fillet.user_startAngle)
        ToolsUI.setAngleToObj(fillet, "EndAngle", fillet.user_endAngle)

        Tools3D.sayz("fillet.Radius =" + str(fillet.Radius))
        Tools3D.sayz("fillet.Point1X=" + str(fillet.Point1X))
        Tools3D.sayz("fillet.Point1Y=" + str(fillet.Point1Y))
        Tools3D.sayz("fillet.Point2X=" + str(fillet.Point2X))
        Tools3D.sayz("fillet.Point2Y=" + str(fillet.Point2Y))
        Tools3D.sayz("fillet.StartAngle=" + str(fillet.StartAngle))
        Tools3D.sayz("fillet.EndAngle=" + str(fillet.EndAngle))
        fillet.recompute()

        arc = Part.Edge(Part.Arc(arc_point1, arc_point2, arc_point3))
        Tools3D.sayz("p3=" + str(p2))
        line_left = Part.Edge(Part.LineSegment(arc_point1, p2))
        line_right = Part.Edge(Part.LineSegment(arc_point3, p2))
        w = Part.Wire([line_left, arc, line_right])
        fp.Shape = Part.Face(w)


class GetProperty:
    def __init__(self, obj):
        obj.addProperty("App::PropertyString", "Type").Type = ObjectTools.ObjectType.Area_Function

        obj.addProperty("App::PropertyDistance", "Point1X").Point1X = 0
        obj.addProperty("App::PropertyDistance", "Point1Y").Point1Y = 0
        obj.addProperty("App::PropertyDistance", "Point2X").Point2X = 0.1
        obj.addProperty("App::PropertyDistance", "Point2Y").Point2Y = 0.1
        obj.addProperty("App::PropertyDistance", "Point3X").Point3X = 0.2
        obj.addProperty("App::PropertyDistance", "Point3Y").Point3Y = 0
        obj.addProperty("App::PropertyDistance", "Radius").Radius = 0.05

        Tools3D.addCommonProperty(obj)
        Tools3D.addAttributeToObject(obj)
        Tools3D.addHelperProperty(obj, 2)
        # Tools3D.getHelperValue(obj)


def getObject():
    FreeCAD.ActiveDocument.openTransaction('CreateAreaFunction_3D')
    obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", ObjectTools.ObjectType.Area_Function)
    InitDoc3D.addObjectToGroup_helper(obj, "AreaG", "面")
    AreaFillet(obj)
    Tools3D.ViewProvider(obj.ViewObject)
    FreeCAD.ActiveDocument.commitTransaction()
    return obj


