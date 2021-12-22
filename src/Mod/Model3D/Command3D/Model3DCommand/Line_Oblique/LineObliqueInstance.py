# -*- coding: utf8 -*-
import FreeCADGui
import FreeCAD
import Part
from Model3D.Tools import Tools3D, ObjectTools, InitDoc3D


class LineOblique:
    def __init__(self, obj):
        obj.Proxy = self

    def onChanged(self, fp, prop):
        pass

    def execute(self, fp):
        if FreeCAD.ActiveDocument.CoordinateSystem == 'Rectangular':
            point1 = Tools3D.transToRecVector(fp.Point1X.Value, fp.Point1Y.Value, fp.Point1Z.Value)
            point2 = Tools3D.transToRecVector(fp.Point2X.Value, fp.Point2Y.Value, fp.Point2Z.Value)
            try:
                if point1 == point2:
                    fp.Shape = Part.Vertex(point1)
                else:
                    fp.Shape = Part.makeLine(point1, point2)
            except:
                Tools3D.sayz("Redraw LineOblique Failed!")


class GetProperty:
    def __init__(self):
        FreeCAD.ActiveDocument.openTransaction('CreateLineOblique_3D')
        self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", ObjectTools.ObjectType.Line_Oblique)
        self.__setProperty(self.obj)
        InitDoc3D.addObjectToGroup_helper(self.obj, "LineG", "线")
        FreeCAD.ActiveDocument.commitTransaction()

    def __setProperty(self, obj):
        obj.addProperty("App::PropertyString", "Type").Type = ObjectTools.ObjectType.Line_Oblique
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
            obj.addProperty("App::PropertyAngle", "Point2Y").Point2Y = 360
            obj.addProperty("App::PropertyDistance", "Point2Z").Point2Z = 0
        else:
            obj.addProperty("App::PropertyDistance", "Point1X").Point1X = 0
            obj.addProperty("App::PropertyDistance", "Point1Y").Point1Y = 0
            obj.addProperty("App::PropertyAngle", "Point1Z").Point1Z = 0
            obj.addProperty("App::PropertyDistance", "Point2X").Point2X = 0
            obj.addProperty("App::PropertyDistance", "Point2Y").Point2Y = 0
            obj.addProperty("App::PropertyAngle", "Point2Z").Point2Z = 360
        Tools3D.addCommonProperty(obj)
        Tools3D.addAttributeToObject(obj)
        Tools3D.addHelperProperty(obj, 2)
        Tools3D.getHelperValue(obj)

def getObject():
    LineObliqueObj = GetProperty()
    LineOblique(LineObliqueObj.obj)
    Tools3D.ViewProvider(LineObliqueObj.obj.ViewObject)
    return LineObliqueObj.obj

