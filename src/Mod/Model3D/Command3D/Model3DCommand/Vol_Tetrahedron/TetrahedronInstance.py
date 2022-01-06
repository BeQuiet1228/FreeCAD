# -*- coding: utf-8 -*-
import FreeCAD
import FreeCADGui
from Model3D.Tools import Tools3D, ObjectTools, InitDoc3D
import Part
import math
from FreeCAD import Base


class CreateTetrahedron:
    def __init__(self, obj):
        obj.Proxy = self

    def onChanged(self, fp, prop):
        pass

    def execute(self, fp):
        """
           排除四点在一个面无法形成立体模型的错误情况，再排除两点重合的错误情况，然后连续形成面再形成体建模。
        """
        Tools3D.sayz("绘图已经调用")
        point1 = Tools3D.transToRecVector(fp.Point1X.Value, fp.Point1Y.Value, fp.Point1Z.Value)
        point2 = Tools3D.transToRecVector(fp.Point2X.Value, fp.Point2Y.Value, fp.Point2Z.Value)
        point3 = Tools3D.transToRecVector(fp.Point3X.Value, fp.Point3Y.Value, fp.Point3Z.Value)
        point4 = Tools3D.transToRecVector(fp.Point4X.Value, fp.Point4Y.Value, fp.Point4Z.Value)
        try:
            if ObjectTools.isFourPointsOnTheSamePlane([point1, point2, point3, point4]):
                # 警告用户数据错误及错误原因
                Tools3D.sayz("错误")
                pass
            if point1 == point2:
                # 警告用户数据错误及错误原因
                Tools3D.sayz("错误")
                pass
            if point1 == point3:
                # 警告用户数据错误及错误原因
                Tools3D.sayz("错误")
                pass
            if point1 == point4:
                # 警告用户数据错误及错误原因
                Tools3D.sayz("错误")
                pass
            if point2 == point3:
                # 警告用户数据错误及错误原因
                Tools3D.sayz("错误")
                pass
            if point2 == point4:
                # 警告用户数据错误及错误原因
                Tools3D.sayz("错误")
                pass
            if point3 == point4:
                # 警告用户数据错误及错误原因
                Tools3D.sayz("错误")
                pass
            buttom_wire = Part.makePolygon([point1, point2, point3, point1])
            front_wire = Part.makePolygon([point1, point2, point4, point1])
            left_wire = Part.makePolygon([point1, point3, point4, point1])
            right_wire = Part.makePolygon([point2, point4, point3, point2])
            bottom_face = Part.Face(buttom_wire)
            front_face = Part.Face(front_wire)
            right_face = Part.Face(right_wire)
            left_face = Part.Face(left_wire)
            Shape1 = Part.makeShell([front_face, bottom_face, right_face, left_face])
            fp.Shape = Part.makeSolid(Shape1)
            # bottom_face = Part.makeFace(buttom_wire, "Part::FaceMakerExtrusion")
            # front_face = Part.makeFace(front_wire, "Part::FaceMakerExtrusion")
            # right_face = Part.makeFace(right_wire, "Part::FaceMakerExtrusion")
            # left_face = Part.makeFace(left_wire, "Part::FaceMakerExtrusion")
            # 每个面都划分为三角形
            # fp.Shape = Part.makeShell([front_face, bottom_face, right_face, left_face])
        except:
            Tools3D.sayz("Redraw Tetrahedron Failed!")

class Tetrahedron:
    """
    工厂类
    """
    def __init__(self):
        FreeCAD.ActiveDocument.openTransaction('Create_3D_Tetrahedron')
        self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "Vol_Tetrahedron")
        self.__setProperty(self.obj)
        InitDoc3D.addObjectToGroup_helper(self.obj, "Tetrahedron", "四面体")
        FreeCAD.ActiveDocument.commitTransaction()
        # self.__setProperty(self.obj)

    def __setProperty(self, obj):
        obj.addProperty("App::PropertyString", "Type").Type = "Vol_Tetrahedron"
        if FreeCAD.ActiveDocument.CoordinateSystem == "Rectangular":
            obj.addProperty("App::PropertyDistance", "Point1X", "Cone", " centre point1 X").Point1X = 0
            obj.addProperty("App::PropertyDistance", "Point1Y", "Cone", " centre point1 Y").Point1Y = 0
            obj.addProperty("App::PropertyDistance", "Point1Z", "Cone", " centre point1 Z").Point1Z = 0
            obj.addProperty("App::PropertyDistance", "Point2X", "Cone", " centre point2 X").Point2X = 0.05
            obj.addProperty("App::PropertyDistance", "Point2Y", "Cone", " centre point2 Y").Point2Y = 0
            obj.addProperty("App::PropertyDistance", "Point2Z", "Cone", " centre point2 Z").Point2Z = 0
            obj.addProperty("App::PropertyDistance", "Point3X", "Cone", " centre point3 X").Point3X = 0.05
            obj.addProperty("App::PropertyDistance", "Point3Y", "Cone", " centre point3 Y").Point3Y = 0.05
            obj.addProperty("App::PropertyDistance", "Point3Z", "Cone", " centre point3 Z").Point3Z = 0
            obj.addProperty("App::PropertyDistance", "Point4X", "Cone", " centre point4 X").Point4X = 0
            obj.addProperty("App::PropertyDistance", "Point4Y", "Cone", " centre point4 Y").Point4Y = 0
            obj.addProperty("App::PropertyDistance", "Point4Z", "Cone", " centre point4 Z").Point4Z = 0.05
        elif FreeCAD.ActiveDocument.CoordinateSystem == "Polar":
            obj.addProperty("App::PropertyDistance", "Point1X", "Cone", " centre point1 X").Point1X = 0
            obj.addProperty("App::PropertyAngle", "Point1Y", "Cone", " centre point1 Y").Point1Y = 0
            obj.addProperty("App::PropertyDistance", "Point1Z", "Cone", " centre point1 Z").Point1Z = 0
            obj.addProperty("App::PropertyDistance", "Point2X", "Cone", " centre point2 X").Point2X = 0
            obj.addProperty("App::PropertyAngle", "Point2Y", "Cone", " centre point2 Y").Point2Y = 0
            obj.addProperty("App::PropertyDistance", "Point2Z", "Cone", " centre point2 Z").Point2Z = 0
            obj.addProperty("App::PropertyDistance", "Point3X", "Cone", " centre point3 X").Point3X = 0
            obj.addProperty("App::PropertyAngle", "Point3Y", "Cone", " centre point3 Y").Point3Y = 0
            obj.addProperty("App::PropertyDistance", "Point3Z", "Cone", " centre point3 Z").Point3Z = 0
            obj.addProperty("App::PropertyDistance", "Point4X", "Cone", " centre point4 X").Point4X = 0
            obj.addProperty("App::PropertyAngle", "Point4Y", "Cone", " centre point4 Y").Point4Y = 0
            obj.addProperty("App::PropertyDistance", "Point4Z", "Cone", " centre point4 Z").Point4Z = 0
        else:
            obj.addProperty("App::PropertyDistance", "Point1X", "Cone", " centre point1 X").Point1X = 0
            obj.addProperty("App::PropertyDistance", "Point1Y", "Cone", " centre point1 Y").Point1Y = 0
            obj.addProperty("App::PropertyAngle", "Point1Z", "Cone", " centre point1 Z").Point1Z = 0
            obj.addProperty("App::PropertyDistance", "Point2X", "Cone", " centre point2 X").Point2X = 0
            obj.addProperty("App::PropertyDistance", "Point2Y", "Cone", " centre point2 Y").Point2Y = 0
            obj.addProperty("App::PropertyAngle", "Point2Z", "Cone", " centre point2 Z").Point2Z = 0
            obj.addProperty("App::PropertyDistance", "Point3X", "Cone", " centre point3 X").Point3X = 0
            obj.addProperty("App::PropertyDistance", "Point3Y", "Cone", " centre point3 Y").Point3Y = 0
            obj.addProperty("App::PropertyAngle", "Point3Z", "Cone", " centre point3 Z").Point3Z = 0
            obj.addProperty("App::PropertyDistance", "Point4X", "Cone", " centre point4 X").Point4X = 0
            obj.addProperty("App::PropertyDistance", "Point4Y", "Cone", " centre point4 Y").Point4Y = 0
            obj.addProperty("App::PropertyAngle", "Point4Z", "Cone", " centre point4 Z").Point4Z = 0
        Tools3D.addCommonPropertyToObject(obj)
        Tools3D.addAttributeToObject(obj)
        Tools3D.addHelperProperty(obj, 4)
        Tools3D.getHelperValue(obj)


def getObject():
    tetrahedron = Tetrahedron()
    CreateTetrahedron(tetrahedron.obj)
    Tools3D.ViewProvider(tetrahedron.obj.ViewObject)
    return tetrahedron.obj


