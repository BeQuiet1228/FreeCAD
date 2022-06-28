# -*- coding: utf-8 -*-
import FreeCAD
import Part
from Model3D.Tools import Tools3D, ObjectTools, InitDoc3D


class CreateCylinder:
    def __init__(self, obj):
        obj.Proxy = self

    def onChanged(self, fp, prop):
        pass

    def execute(self, fp):
        # 先排除圆半径小于等于零的错误情况，再判断两基点是否重合，如果重合，就建一个圆形面：如果不重合，就正常建圆柱。
        point1 = Tools3D.transToRecVector(fp.Point1X.Value, fp.Point1Y.Value, fp.Point1Z.Value)
        point2 = Tools3D.transToRecVector(fp.Point2X.Value, fp.Point2Y.Value, fp.Point2Z.Value)
        normal = point2.sub(point1)
        height = normal.Length
        try:
            if fp.Radius.Value <= 0:
                # 警告用户数据错误及错误原因
                Tools3D.sayz("错误，半径不能小于等于零")
                pass
            else:
                if point1 != point2:
                    fp.Shape = Part.makeCylinder(fp.Radius.Value, height, point1, normal, 360)
                else:
                 # 如果point1和point2坐标相等，图形为圆，法向默认为Z轴
                    circle = Part.makeCircle(fp.Radius.Value, point1, FreeCAD.Vector(0,0,1))
                    fp.Shape = Part.makeFace([Part.Wire([circle])], "Part::FaceMakerBullseye")
        except:
            Tools3D.sayz("Redraw Cylinder Failed!")


class Cylinder:
    def __init__(self):
        FreeCAD.ActiveDocument.openTransaction('Create_3D_Cylinder')
        self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "Vol_Cylinder")
        self.__setProperty(self.obj)
        InitDoc3D.addObjectToGroup_helper(self.obj, "Cylinder", "圆柱体")
        FreeCAD.ActiveDocument.commitTransaction()

    def __setProperty(self, obj):
        obj.addProperty("App::PropertyString", "Type").Type = ObjectTools.ObjectType.Vol_Cylinder
        if FreeCAD.ActiveDocument.CoordinateSystem == "Rectangular":
            obj.addProperty("App::PropertyDistance", "Point1X", "Cylinder", " centre point1 X").Point1X = 0
            obj.addProperty("App::PropertyDistance", "Point1Y", "Cylinder", " centre point1 Y").Point1Y = 0
            obj.addProperty("App::PropertyDistance", "Point1Z", "Cylinder", " centre point1 Z").Point1Z = 0
            obj.addProperty("App::PropertyDistance", "Point2X", "Cylinder", " centre point2 X").Point2X = 0
            obj.addProperty("App::PropertyDistance", "Point2Y", "Cylinder", " centre point2 Y").Point2Y = 0
            obj.addProperty("App::PropertyDistance", "Point2Z", "Cylinder", " centre point2 Z").Point2Z = 0.001
        elif FreeCAD.ActiveDocument.CoordinateSystem == "Polar":
            obj.addProperty("App::PropertyDistance", "Point1X", "Cylinder", " centre point1 X").Point1X = 0
            obj.addProperty("App::PropertyAngle", "Point1Y", "Cylinder", " centre point1 Y").Point1Y = 0
            obj.addProperty("App::PropertyDistance", "Point1Z", "Cylinder", " centre point1 Z").Point1Z = 0
            obj.addProperty("App::PropertyDistance", "Point2X", "Cylinder", " centre point2 X").Point2X = 0
            obj.addProperty("App::PropertyAngle", "Point2Y", "Cylinder", " centre point2 Y").Point2Y = 360
            obj.addProperty("App::PropertyDistance", "Point2Z", "Cylinder", " centre point2 Z").Point2Z = 0
        else:
            obj.addProperty("App::PropertyDistance", "Point1X", "Cylinder", " centre point1 X").Point1X = 0
            obj.addProperty("App::PropertyDistance", "Point1Y", "Cylinder", " centre point1 Y").Point1Y = 0
            obj.addProperty("App::PropertyAngle", "Point1Z", "Cylinder", " centre point1 Z").Point1Z = 0
            obj.addProperty("App::PropertyDistance", "Point2X", "Cylinder", " centre point2 X").Point2X = 0
            obj.addProperty("App::PropertyDistance", "Point2Y", "Cylinder", " centre point2 Y").Point2Y = 0
            obj.addProperty("App::PropertyAngle", "Point2Z", "Cylinder", " centre point2 Z").Point2Z = 360

        obj.addProperty("App::PropertyLength", "Radius", "Cylinder", "Radius").Radius = 0.02
        Tools3D.addCommonPropertyToObject(obj)
        Tools3D.addAttributeToObject(obj)
        Tools3D.addHelperProperty(obj, 2)
        Tools3D.getHelperValue(obj)
        Tools3D.addRadiusProperty(obj)
        Tools3D.getRadiusProperty(obj)


def getObject():
    cylinder = Cylinder()
    CreateCylinder(cylinder.obj)
    Tools3D.ViewProvider(cylinder.obj.ViewObject)
    return cylinder.obj







