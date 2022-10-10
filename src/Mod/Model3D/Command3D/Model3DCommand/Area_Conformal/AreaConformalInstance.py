# -*- coding: utf8 -*-
import math
import FreeCADGui
import FreeCAD
import Part
from Model3D.Tools import Tools3D, ObjectTools, InitDoc3D


class AreaConformal:
    def __init__(self, obj):
        obj.Proxy = self

    def onChanged(self, fp, prop):
        pass

    def execute(self, fp):
        coordinate = FreeCAD.ActiveDocument.CoordinateSystem
        if coordinate == "Rectangular":
            point1 = FreeCAD.Vector(fp.Point1X.Value, fp.Point1Y.Value, fp.Point1Z.Value)
            point3 = FreeCAD.Vector(fp.Point2X.Value, fp.Point2Y.Value, fp.Point2Z.Value)
            if fp.Normal == "X":
                point2 = FreeCAD.Vector(fp.Point1X.Value, fp.Point2Y.Value, fp.Point1Z.Value)
                point4 = FreeCAD.Vector(fp.Point1X.Value, fp.Point1Y.Value, fp.Point2Z.Value)
            elif fp.Normal == "Y":
                point2 = FreeCAD.Vector(fp.Point2X.Value, fp.Point1Y.Value, fp.Point1Z.Value)
                point4 = FreeCAD.Vector(fp.Point1X.Value, fp.Point1Y.Value, fp.Point2Z.Value)
            elif fp.Normal == "Z":
                point2 = FreeCAD.Vector(fp.Point2X.Value, fp.Point1Y.Value, fp.Point1Z.Value)
                point4 = FreeCAD.Vector(fp.Point1X.Value, fp.Point2Y.Value, fp.Point1Z.Value)
            else:
                pass
            try:
                if point1 == point2 or point1 == point3 or point1 == point4:
                    Tools3D.sayz("point not overlapping")
                else:
                    Area = Part.makePolygon([point1, point2, point3, point4, point1])
                    fp.Shape = Part.makeFace(Area, "Part::FaceMakerExtrusion")
            except:
                Tools3D.sayz("Redraw Area Conformal Failed!")

        else:
            # 数据处理
            if coordinate == "Polar":
                if fp.Point1X.Value < 0 or fp.Point2X.Value < 0:
                    Tools3D.sayz(u"R不能为负")
                    Tools3D.sayz("Redraw Area Conformal Failed!")
                    return
                elif fp.Point1X.Value == 0 and fp.Point2X.Value == 0:
                    # R均为0，建模为一条平行于Z轴的正投影线
                    try:
                        fp.Shape = Part.makeLine(FreeCAD.Vector(0,0,fp.Point1Z.Value), FreeCAD.Vector(0,0,fp.Point2Z.Value))
                        return
                    except:
                        Tools3D.sayz("Redraw Area Conformal Failed!")
                        return
                else:
                    h_bottom = min(fp.Point1Z.Value, fp.Point2Z.Value)
                    h_top = max(fp.Point1Z.Value, fp.Point2Z.Value)
                    minRadius = min(fp.Point1X.Value, fp.Point2X.Value)
                    maxRadius = max(fp.Point1X.Value, fp.Point2X.Value)
                    angle_start = fp.Point1Y.Value % 360.0
                    angle_end = fp.Point2Y.Value % 360.0
            else:
                if fp.Point1Y.Value < 0 or fp.Point2Y.Value < 0:
                    Tools3D.sayz(u"R不能为负")
                    Tools3D.sayz("Redraw Area Conformal Failed!")
                    return
                if fp.Point1Y.Value == 0 and fp.Point2Y.Value == 0:
                    # R均为0，建模为一条平行于Z轴的正投影线
                    fp.Shape = Part.makeLine(FreeCAD.Vector(0,0,fp.Point1X.Value), FreeCAD.Vector(0,0,fp.Point2X.Value))
                    return
                else:
                    h_bottom = min(fp.Point1X.Value, fp.Point2X.Value)
                    h_top = max(fp.Point1X.Value, fp.Point2X.Value)
                    minRadius = min(fp.Point1Y.Value, fp.Point2Y.Value)
                    maxRadius = max(fp.Point1Y.Value, fp.Point2Y.Value)
                    angle_start = fp.Point1Z.Value % 360.0
                    angle_end = fp.Point2Z.Value % 360.0

            radian_start = angle_start * math.pi / 180.0
            if fp.Normal == "Theta":
                point1 = FreeCAD.Vector(maxRadius * math.cos(radian_start),
                                        maxRadius * math.sin(radian_start), h_bottom)
                point2 = FreeCAD.Vector(minRadius * math.cos(radian_start),
                                        minRadius * math.sin(radian_start), h_bottom)
                point3 = FreeCAD.Vector(minRadius * math.cos(radian_start),
                                        minRadius * math.sin(radian_start), h_top)
                point4 = FreeCAD.Vector(maxRadius * math.cos(radian_start),
                                        maxRadius * math.sin(radian_start), h_top)
                Area = Part.makePolygon([point1, point2, point3, point4, point1])
                fp.Shape = Part.makeFace(Area, "Part::FaceMakerExtrusion")
                return
            else:
                if fp.Normal == "R":
                    point_start = FreeCAD.Vector(maxRadius * math.cos(radian_start),
                                                 maxRadius * math.sin(radian_start), h_bottom)
                    point_start_top = FreeCAD.Vector(maxRadius * math.cos(radian_start),
                                                     maxRadius * math.sin(radian_start), h_top)
                    line = Part.makeLine(point_start, point_start_top)
                elif fp.Normal == "Z":
                    point_outer = FreeCAD.Vector(maxRadius * math.cos(radian_start),
                                                 maxRadius * math.sin(radian_start), h_bottom)
                    point_inner = FreeCAD.Vector(minRadius * math.cos(radian_start),
                                                 minRadius * math.sin(radian_start), h_bottom)
                    line = Part.makeLine(point_inner, point_outer)
                else:
                    Tools3D.sayz("Normal Wrong!")
                    return

                arcShape = Part.makeCircle(maxRadius, FreeCAD.Vector(0, 0, h_bottom), FreeCAD.Vector(0, 0, 1),
                                           angle_start, angle_end)
                path = Part.Wire(arcShape)
                fp.Shape = path.makePipe(line)
                return


class GetProperty:
    def __init__(self):
        FreeCAD.ActiveDocument.openTransaction('CreateAreaConformal_3D')
        self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", ObjectTools.ObjectType.Area_Conformal)
        self.__setProperty(self.obj)
        InitDoc3D.addObjectToGroup_helper(self.obj, "AreaG", "面")
        FreeCAD.ActiveDocument.commitTransaction()

    def __setProperty(self, obj):
        obj.addProperty("App::PropertyString", "Type").Type = ObjectTools.ObjectType.Area_Conformal
        if FreeCAD.ActiveDocument.CoordinateSystem == "Rectangular":
            obj.addProperty("App::PropertyDistance", "Point1X").Point1X = 0
            obj.addProperty("App::PropertyDistance", "Point1Y").Point1Y = 0
            obj.addProperty("App::PropertyDistance", "Point1Z").Point1Z = 0
            obj.addProperty("App::PropertyDistance", "Point2X").Point2X = 0.01
            obj.addProperty("App::PropertyDistance", "Point2Y").Point2Y = 0.01
            obj.addProperty("App::PropertyDistance", "Point2Z").Point2Z = 0.01
            obj.addProperty("App::PropertyString", "Normal", "Normal", "").Normal = "X"
        elif FreeCAD.ActiveDocument.CoordinateSystem == "Polar":
            obj.addProperty("App::PropertyDistance", "Point1X").Point1X = 0
            obj.addProperty("App::PropertyAngle", "Point1Y").Point1Y = 0
            obj.addProperty("App::PropertyDistance", "Point1Z").Point1Z = 0
            obj.addProperty("App::PropertyDistance", "Point2X").Point2X = 0
            obj.addProperty("App::PropertyAngle", "Point2Y").Point2Y = 360
            obj.addProperty("App::PropertyDistance", "Point2Z").Point2Z = 0
            obj.addProperty("App::PropertyString", "Normal", "Normal", "").Normal = "Z"
        else:
            obj.addProperty("App::PropertyDistance", "Point1X").Point1X = 0
            obj.addProperty("App::PropertyDistance", "Point1Y").Point1Y = 0
            obj.addProperty("App::PropertyAngle", "Point1Z").Point1Z = 0
            obj.addProperty("App::PropertyDistance", "Point2X").Point2X = 0
            obj.addProperty("App::PropertyDistance", "Point2Y").Point2Y = 0
            obj.addProperty("App::PropertyAngle", "Point2Z").Point2Z = 360
            obj.addProperty("App::PropertyString", "Normal", "Normal", "").Normal = "Z"

        Tools3D.addCommonProperty(obj)
        Tools3D.addAttributeToObject(obj)
        Tools3D.addHelperProperty(obj, 2)
        Tools3D.getHelperValue(obj)


def getObject():
    AreaConformalObj = GetProperty()
    AreaConformal(AreaConformalObj.obj)
    Tools3D.ViewProvider(AreaConformalObj.obj.ViewObject)
    return AreaConformalObj.obj
