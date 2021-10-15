# -*- coding: utf8 -*-
import FreeCADGui
import FreeCAD
import Part
from Model3D.Tools import Tools3D, ObjectTools, InitDoc3D


class LineConformal:
    def __init__(self, obj):
        obj.Proxy = self

    def onChanged(self, fp, prop):
        pass

    def execute(self, fp):
        point1 = Tools3D.transToRecVector(fp.Point1X.Value, fp.Point1Y.Value, fp.Point1Z.Value)
        point2 = Tools3D.transToRecVector(fp.Point2X.Value, fp.Point2Y.Value, fp.Point2Z.Value)
        ##当在极坐标和柱坐标下，theta值为0和360时不进行makeLine
        if FreeCAD.ActiveDocument.CoordinateSystem == "Polar":
            if (fp.Point1Y.Value == 0 and fp.Point2Y.Value == 360) or (
                    fp.Point1Y.Value == 360 and fp.Point2Y.Value == 0):
                fp.Shape = Part.makeSphere(0.0001, point1)
                return
        if FreeCAD.ActiveDocument.CoordinateSystem == "Cylindrical":
            if (fp.Point1Z.Value == 0 and fp.Point2Z.Value == 360) or (
                    fp.Point1Z.Value == 360 and fp.Point2Z.Value == 0):
                fp.Shape = Part.makeSphere(0.0001, point1)
                return
        try:
            if point1 == point2:
                fp.Shape = Part.Vertex(point1)
            else:
                fp.Shape = Part.makeLine(point1, point2)
        except:
            Tools3D.sayz("Redraw LineOblique Failed!")


class GetProperty:
    def __init__(self):
        FreeCAD.ActiveDocument.openTransaction('CreateLineConformal_3D')
        self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", ObjectTools.ObjectType.Line_Conformal)
        self.__setProperty(self.obj)
        InitDoc3D.addObjectToGroup_helper(self.obj, "LineG", "线")
        FreeCAD.ActiveDocument.commitTransaction()

    def __setProperty(self, obj):
        obj.addProperty("App::PropertyString", "Type").Type = ObjectTools.ObjectType.Line_Conformal
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
            obj.addProperty("App::PropertyAngle", "Point2Y").Point2Y = 0
            obj.addProperty("App::PropertyDistance", "Point2Z").Point2Z = 0
            obj.addProperty("App::PropertyString", "Normal", "Normal", "").Normal = "R"
        else:
            obj.addProperty("App::PropertyDistance", "Point1X").Point1X = 0
            obj.addProperty("App::PropertyDistance", "Point1Y").Point1Y = 0
            obj.addProperty("App::PropertyAngle", "Point1Z").Point1Z = 0
            obj.addProperty("App::PropertyDistance", "Point2X").Point2X = 0
            obj.addProperty("App::PropertyDistance", "Point2Y").Point2Y = 0
            obj.addProperty("App::PropertyAngle", "Point2Z").Point2Z = 0
            obj.addProperty("App::PropertyString", "Normal", "Normal", "").Normal = "Z"
        Tools3D.addCommonProperty(obj)
        Tools3D.addAttributeToObject(obj)
        Tools3D.addHelperProperty(obj, 2)
        Tools3D.getHelperValue(obj)


def getObject():
    LineConformalObj = GetProperty()
    LineConformal(LineConformalObj.obj)
    Tools3D.ViewProvider(LineConformalObj.obj.ViewObject)
    return LineConformalObj.obj
