# -*- coding: utf8 -*-
import FreeCAD
import Part
from Model3D.Tools import Tools3D, ObjectTools, InitDoc3D


class VolPyramid:
    def __init__(self, obj):
        obj.Proxy = self

    def onChanged(self, fp, prop):
        pass

    def execute(self, fp):
        """
        金字塔体
        绘制方式：由4个点组成底面，另一个点为顶点。除了底面，剩余的面皆为三角面。
        1.五个点不能相同
        2.绘制底面的4个点在一个平面上
        """
        point1 = Tools3D.transToRecVector(fp.Point1X.Value, fp.Point1Y.Value, fp.Point1Z.Value)
        point2 = Tools3D.transToRecVector(fp.Point2X.Value, fp.Point2Y.Value, fp.Point2Z.Value)
        point3 = Tools3D.transToRecVector(fp.Point3X.Value, fp.Point3Y.Value, fp.Point3Z.Value)
        point4 = Tools3D.transToRecVector(fp.Point4X.Value, fp.Point4Y.Value, fp.Point4Z.Value)
        point5 = Tools3D.transToRecVector(fp.Point5X.Value, fp.Point5Y.Value, fp.Point5Z.Value)

        # 判断是否有相等的点
        points_list = [point1, point2, point3, point4, point5]
        if ObjectTools.isPointEqual(points_list):
            Tools3D.sayz("不能有相同的点，请重新输入")
            return

        # 判断4个点是否共面
        points = [point1, point2, point3, point4]
        if not ObjectTools.isFourPointsOnTheSamePlane(points):
            Tools3D.sayz("point1, point2, point3, point4 不在同一个平面")
            return

        if point5 in points:
            Tools3D.sayz("point5不能在底面上")
            return

        try:
            buttom_wire_left_bottom = Part.makePolygon([point1, point2, point3, point1])
            buttom_wire_right_bottom = Part.makePolygon([point1, point3, point4, point1])
            front_wire = Part.makePolygon([point1, point2, point5, point1])
            back_wire = Part.makePolygon([point3, point4, point5, point3])
            left_wire = Part.makePolygon([point1, point4, point5, point1])
            right_wire = Part.makePolygon([point2, point3, point5, point2])
            bottom_face_left_bottom = Part.makeFace(buttom_wire_left_bottom, "Part::FaceMakerExtrusion")
            bottom_face_right_bottom = Part.makeFace(buttom_wire_right_bottom, "Part::FaceMakerExtrusion")
            front_face = Part.makeFace(front_wire, "Part::FaceMakerExtrusion")
            back_face = Part.makeFace(back_wire, "Part::FaceMakerExtrusion")
            right_face = Part.makeFace(right_wire, "Part::FaceMakerExtrusion")
            left_face = Part.makeFace(left_wire, "Part::FaceMakerExtrusion")
            # 底面为四边形，其他面都划分为三角形
            fp.Shape = Part.makeShell([bottom_face_left_bottom,
                                       bottom_face_right_bottom,
                                       front_face,
                                       right_face,
                                       left_face,
                                       back_face])
            fp.Shape = Part.makeSolid(fp.Shape)
        except:
            Tools3D.sayz("Redraw Pyramid Failed!")


class GetProperty:
    def __init__(self):
        FreeCAD.ActiveDocument.openTransaction('CreateVolPyramid_3D')
        self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", ObjectTools.ObjectType.Vol_Pyramid)
        self.__setProperty(self.obj)
        InitDoc3D.addObjectToGroup_helper(self.obj, "Pyramid", "金字塔体")
        FreeCAD.ActiveDocument.commitTransaction()
        # self.__setProperty(self.obj)

    def __setProperty(self, obj):
        obj.addProperty("App::PropertyString", "Type").Type = ObjectTools.ObjectType.Vol_Pyramid
        if FreeCAD.ActiveDocument.CoordinateSystem == "Rectangular":
            obj.addProperty("App::PropertyDistance", "Point1X").Point1X = 0.01
            obj.addProperty("App::PropertyDistance", "Point1Y").Point1Y = -0.01
            obj.addProperty("App::PropertyDistance", "Point1Z").Point1Z = 0
            obj.addProperty("App::PropertyDistance", "Point2X").Point2X = 0.01
            obj.addProperty("App::PropertyDistance", "Point2Y").Point2Y = 0.01
            obj.addProperty("App::PropertyDistance", "Point2Z").Point2Z = 0
            obj.addProperty("App::PropertyDistance", "Point3X").Point3X = -0.01
            obj.addProperty("App::PropertyDistance", "Point3Y").Point3Y = 0.01
            obj.addProperty("App::PropertyDistance", "Point3Z").Point3Z = 0
            obj.addProperty("App::PropertyDistance", "Point4X").Point4X = -0.01
            obj.addProperty("App::PropertyDistance", "Point4Y").Point4Y = -0.01
            obj.addProperty("App::PropertyDistance", "Point4Z").Point4Z = 0
            obj.addProperty("App::PropertyDistance", "Point5X").Point5X = 0
            obj.addProperty("App::PropertyDistance", "Point5Y").Point5Y = 0
            obj.addProperty("App::PropertyDistance", "Point5Z").Point5Z = 0.01
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
        Tools3D.addCommonPropertyToObject(obj)
        Tools3D.addAttributeToObject(obj)
        Tools3D.addHelperProperty(obj, 5)
        Tools3D.getHelperValue(obj)


def getObject():
    """
    返回获取的obj
    """
    volPyramidObj = GetProperty()
    VolPyramid(volPyramidObj.obj)
    Tools3D.ViewProvider(volPyramidObj.obj.ViewObject)
    return volPyramidObj.obj

