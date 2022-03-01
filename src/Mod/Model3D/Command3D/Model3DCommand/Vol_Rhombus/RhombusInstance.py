# -*- coding: utf8 -*-
import FreeCADGui
import FreeCAD
import Part
from Model3D.Tools import Tools3D, ObjectTools, InitDoc3D


class VolRhombus:
    def __init__(self, obj):
        obj.Proxy = self

    def onChanged(self, fp, prop):
        pass

    def execute(self, fp):
        """
        菱形体
        绘制方式：每个面皆有4个点组成，并且4个点逆时针排列
        1.所有的点不能重合
        2.4个点在一个平面上才可以组成平面
        """
        try:
            point1 = Tools3D.transToRecVector(fp.Point1X.Value, fp.Point1Y.Value, fp.Point1Z.Value)
            point2 = Tools3D.transToRecVector(fp.Point2X.Value, fp.Point2Y.Value, fp.Point2Z.Value)
            point3 = Tools3D.transToRecVector(fp.Point3X.Value, fp.Point3Y.Value, fp.Point3Z.Value)
            point4 = Tools3D.transToRecVector(fp.Point4X.Value, fp.Point4Y.Value, fp.Point4Z.Value)
            point5 = Tools3D.transToRecVector(fp.Point5X.Value, fp.Point5Y.Value, fp.Point5Z.Value)
            point6 = Tools3D.transToRecVector(fp.Point6X.Value, fp.Point6Y.Value, fp.Point6Z.Value)
            point7 = Tools3D.transToRecVector(fp.Point7X.Value, fp.Point7Y.Value, fp.Point7Z.Value)
            point8 = Tools3D.transToRecVector(fp.Point8X.Value, fp.Point8Y.Value, fp.Point8Z.Value)

            point_list = [point1, point2, point3, point4, point5, point6, point7, point8]
            # 判断是否有相同的坐标点
            if ObjectTools.isPointEqual(point_list):
                Tools3D.sayz("不能有相同的点，请重新输入")
                return

            front_point1_list = [point1, point2, point3, point4]
            if not ObjectTools.isFourPointsOnTheSamePlane(front_point1_list):
                Tools3D.sayz("point1, point2, point3, point4 不在同一个平面")
                return

            back_point_list = [point5, point6, point7, point8]
            if not ObjectTools.isFourPointsOnTheSamePlane(back_point_list):
                Tools3D.sayz("point5, point6, point7, point8 不在同一个平面")
                return

            left_point_list = [point1, point5, point8, point4]
            if not ObjectTools.isFourPointsOnTheSamePlane(left_point_list):
                Tools3D.sayz("point1, point5, point8, point4 不在同一个平面")
                return

            right_point_list = [point2, point6, point7, point3]
            if not ObjectTools.isFourPointsOnTheSamePlane(right_point_list):
                Tools3D.sayz("point2, point6, point7, point3 不在同一个平面")
                return

            top_point_list = [point4, point3, point7, point8]
            if not ObjectTools.isFourPointsOnTheSamePlane(top_point_list):
                Tools3D.sayz("point4, point3, point7, point8 不在同一个平面")
                return

            bottom_point_list = [point1, point2, point6, point5]
            if not ObjectTools.isFourPointsOnTheSamePlane(bottom_point_list):
                Tools3D.sayz("point1, point2, point6, point5 不在同一个平面")
                return

            front_wire_left_bottom = Part.makePolygon([point1, point2, point4, point1])
            front_wire_right_top = Part.makePolygon([point2, point3, point4, point2])

            back_wire_left_bottom = Part.makePolygon([point5, point7, point8, point5])
            back_wire_right_top = Part.makePolygon([point5, point6, point7, point5])

            buttom_wire_left_bottom = Part.makePolygon([point1, point2, point5, point1])
            buttom_wire_right_top = Part.makePolygon([point2, point5, point6, point2])

            top_wire_left_top = Part.makePolygon([point4, point7, point8, point4])
            top_wire_right_bottom = Part.makePolygon([point4, point7, point3, point4])

            left_wire_left_top = Part.makePolygon([point8, point4, point5, point8])
            left_wire_right_bottom = Part.makePolygon([point1, point4, point5, point1])

            right_wire_right_top = Part.makePolygon([point7, point3, point6, point7])
            right_wire_left_bottom = Part.makePolygon([point2, point3, point6, point2])

            front_face_left_bottom = Part.makeFace(front_wire_left_bottom, "Part::FaceMakerExtrusion")
            front_face_right_top = Part.makeFace(front_wire_right_top, "Part::FaceMakerExtrusion")

            back_face_left_bottom = Part.makeFace(back_wire_left_bottom, "Part::FaceMakerExtrusion")
            back_face_right_top = Part.makeFace(back_wire_right_top, "Part::FaceMakerExtrusion")

            bottom_face_left_bottom = Part.makeFace(buttom_wire_left_bottom, "Part::FaceMakerExtrusion")
            buttom_face_right_top = Part.makeFace(buttom_wire_right_top, "Part::FaceMakerExtrusion")

            top_face_left_top = Part.makeFace(top_wire_left_top, "Part::FaceMakerExtrusion")
            top_face_right_bottom = Part.makeFace(top_wire_right_bottom, "Part::FaceMakerExtrusion")

            left_face_left_top = Part.makeFace(left_wire_left_top, "Part::FaceMakerExtrusion")
            left_face_right_bottom = Part.makeFace(left_wire_right_bottom, "Part::FaceMakerExtrusion")

            right_face_left_top = Part.makeFace(right_wire_right_top, "Part::FaceMakerExtrusion")
            right_face_right_bottom = Part.makeFace(right_wire_left_bottom, "Part::FaceMakerExtrusion")

            '''Every three points make up a face'''
            fp.Shape = Part.makeShell([back_face_right_top,
                                       back_face_left_bottom,
                                       bottom_face_left_bottom,
                                       buttom_face_right_top,
                                       right_face_left_top,
                                       top_face_left_top,
                                       top_face_right_bottom,
                                       right_face_right_bottom,
                                       left_face_left_top,
                                       left_face_right_bottom,
                                       front_face_left_bottom,
                                       front_face_right_top])
            fp.Shape = Part.makeSolid(fp.Shape)

        except:
            Tools3D.sayz("Redraw Rhombus Failed!")


class GetProperty:
    def __init__(self):
        FreeCAD.ActiveDocument.openTransaction('CreateVolRhombus_3D')
        self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", ObjectTools.ObjectType.Vol_Rhombus)
        self.__setProperty(self.obj)
        InitDoc3D.addObjectToGroup_helper(self.obj, "Rhombus", "菱形体")
        FreeCAD.ActiveDocument.commitTransaction()
        # self.__setProperty(self.obj)

    def __setProperty(self, obj):
        obj.addProperty("App::PropertyString", "Type").Type = ObjectTools.ObjectType.Vol_Rhombus
        if FreeCAD.ActiveDocument.CoordinateSystem == "Rectangular":
            obj.addProperty("App::PropertyDistance", "Point1X").Point1X = 0
            obj.addProperty("App::PropertyDistance", "Point1Y").Point1Y = 0
            obj.addProperty("App::PropertyDistance", "Point1Z").Point1Z = 0
            obj.addProperty("App::PropertyDistance", "Point2X").Point2X = 0.02
            obj.addProperty("App::PropertyDistance", "Point2Y").Point2Y = 0
            obj.addProperty("App::PropertyDistance", "Point2Z").Point2Z = 0
            obj.addProperty("App::PropertyDistance", "Point3X").Point3X = 0.03
            obj.addProperty("App::PropertyDistance", "Point3Y").Point3Y = 0
            obj.addProperty("App::PropertyDistance", "Point3Z").Point3Z = 0.01
            obj.addProperty("App::PropertyDistance", "Point4X").Point4X = 0.01
            obj.addProperty("App::PropertyDistance", "Point4Y").Point4Y = 0
            obj.addProperty("App::PropertyDistance", "Point4Z").Point4Z = 0.01
            obj.addProperty("App::PropertyDistance", "Point5X").Point5X = 0
            obj.addProperty("App::PropertyDistance", "Point5Y").Point5Y = -0.01
            obj.addProperty("App::PropertyDistance", "Point5Z").Point5Z = 0
            obj.addProperty("App::PropertyDistance", "Point6X").Point6X = 0.02
            obj.addProperty("App::PropertyDistance", "Point6Y").Point6Y = -0.01
            obj.addProperty("App::PropertyDistance", "Point6Z").Point6Z = 0
            obj.addProperty("App::PropertyDistance", "Point7X").Point7X = 0.03
            obj.addProperty("App::PropertyDistance", "Point7Y").Point7Y = -0.01
            obj.addProperty("App::PropertyDistance", "Point7Z").Point7Z = 0.01
            obj.addProperty("App::PropertyDistance", "Point8X").Point8X = 0.01
            obj.addProperty("App::PropertyDistance", "Point8Y").Point8Y = -0.01
            obj.addProperty("App::PropertyDistance", "Point8Z").Point8Z = 0.01
        elif FreeCAD.ActiveDocument.CoordinateSystem == "Polar":
            obj.addProperty("App::PropertyDistance", "Point1X").Point1X = 0
            obj.addProperty("App::PropertyAngle", "Point1Y").Point1Y = 0
            obj.addProperty("App::PropertyDistance", "Point1Z").Point1Z = 0
            obj.addProperty("App::PropertyDistance", "Point2X").Point2X = 0
            obj.addProperty("App::PropertyAngle", "Point2Y").Point2Y = 0
            obj.addProperty("App::PropertyDistance", "Point2Z").Point2Z = 0
            obj.addProperty("App::PropertyDistance", "Point3X").Point3X = 0
            obj.addProperty("App::PropertyAngle", "Point3Y").Point3Y = 0
            obj.addProperty("App::PropertyDistance", "Point3Z").Point3Z = 0
            obj.addProperty("App::PropertyDistance", "Point4X").Point4X = 0
            obj.addProperty("App::PropertyAngle", "Point4Y").Point4Y = 0
            obj.addProperty("App::PropertyDistance", "Point4Z").Point4Z = 0
            obj.addProperty("App::PropertyDistance", "Point5X").Point5X = 0
            obj.addProperty("App::PropertyAngle", "Point5Y").Point5Y = 0
            obj.addProperty("App::PropertyDistance", "Point5Z").Point5Z = 0
            obj.addProperty("App::PropertyDistance", "Point6X").Point6X = 0
            obj.addProperty("App::PropertyAngle", "Point6Y").Point6Y = 0
            obj.addProperty("App::PropertyDistance", "Point6Z").Point6Z = 0
            obj.addProperty("App::PropertyDistance", "Point7X").Point7X = 0
            obj.addProperty("App::PropertyAngle", "Point7Y").Point7Y = 0
            obj.addProperty("App::PropertyDistance", "Point7Z").Point7Z = 0
            obj.addProperty("App::PropertyDistance", "Point8X").Point8X = 0
            obj.addProperty("App::PropertyAngle", "Point8Y").Point8Y = 0
            obj.addProperty("App::PropertyDistance", "Point8Z").Point8Z = 0
        else:
            obj.addProperty("App::PropertyDistance", "Point1X").Point1X = 0
            obj.addProperty("App::PropertyDistance", "Point1Y").Point1Y = 0
            obj.addProperty("App::PropertyAngle", "Point1Z").Point1Z = 0
            obj.addProperty("App::PropertyDistance", "Point2X").Point2X = 0
            obj.addProperty("App::PropertyDistance", "Point2Y").Point2Y = 0
            obj.addProperty("App::PropertyAngle", "Point2Z").Point2Z = 0
            obj.addProperty("App::PropertyDistance", "Point3X").Point3X = 0
            obj.addProperty("App::PropertyDistance", "Point3Y").Point3Y = 0
            obj.addProperty("App::PropertyAngle", "Point3Z").Point3Z = 0
            obj.addProperty("App::PropertyDistance", "Point4X").Point4X = 0
            obj.addProperty("App::PropertyDistance", "Point4Y").Point4Y = 0
            obj.addProperty("App::PropertyAngle", "Point4Z").Point4Z = 0
            obj.addProperty("App::PropertyDistance", "Point5X").Point5X = 0
            obj.addProperty("App::PropertyDistance", "Point5Y").Point5Y = 0
            obj.addProperty("App::PropertyAngle", "Point5Z").Point5Z = 0
            obj.addProperty("App::PropertyDistance", "Point6X").Point6X = 0
            obj.addProperty("App::PropertyDistance", "Point6Y").Point6Y = 0
            obj.addProperty("App::PropertyAngle", "Point6Z").Point6Z = 0
            obj.addProperty("App::PropertyDistance", "Point7X").Point7X = 0
            obj.addProperty("App::PropertyDistance", "Point7Y").Point7Y = 0
            obj.addProperty("App::PropertyAngle", "Point7Z").Point7Z = 0
            obj.addProperty("App::PropertyDistance", "Point8X").Point8X = 0
            obj.addProperty("App::PropertyDistance", "Point8Y").Point8Y = 0
            obj.addProperty("App::PropertyAngle", "Point8Z").Point8Z = 0

        Tools3D.addCommonPropertyToObject(obj)
        Tools3D.addAttributeToObject(obj)
        Tools3D.addHelperProperty(obj, 8)
        Tools3D.getHelperValue(obj)


def getObject():
    volRhombusObj = GetProperty()
    VolRhombus(volRhombusObj.obj)
    Tools3D.ViewProvider(volRhombusObj.obj.ViewObject)
    return volRhombusObj.obj
