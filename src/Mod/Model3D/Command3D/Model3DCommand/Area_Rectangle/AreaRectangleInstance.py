# -*- coding: utf8 -*-
import FreeCADGui
import FreeCAD
import Part
from Model3D.Tools import Tools3D, ObjectTools, InitDoc3D


class AreaRectangle:
    def __init__(self, obj):
        obj.Proxy = self

    def onChanged(self, fp, prop):
        pass

    def execute(self, fp):
        point1 = FreeCAD.Vector(fp.Point1X.Value, fp.Point1Y.Value, fp.Point1Z.Value)
        point3 = FreeCAD.Vector(fp.Point2X.Value, fp.Point2Y.Value, fp.Point2Z.Value)
        if fp.Normal == "X":
            point2 = FreeCAD.Vector(fp.Point1X.Value, fp.Point2Y.Value, fp.Point1Z.Value)
            point4 = FreeCAD.Vector(fp.Point1X.Value, fp.Point1Y.Value, fp.Point2Z.Value)
        elif fp.Normal == "Y":
            point2 = FreeCAD.Vector(fp.Point2X.Value, fp.Point1Y.Value, fp.Point1Z.Value)
            point4 = FreeCAD.Vector(fp.Point1X.Value, fp.Point1Y.Value, fp.Point2Z.Value)
        else:
            point2 = FreeCAD.Vector(fp.Point2X.Value, fp.Point1Y.Value, fp.Point1Z.Value)
            point4 = FreeCAD.Vector(fp.Point1X.Value, fp.Point2Y.Value, fp.Point1Z.Value)

        try:
            if point1 == point2 or point1 == point3 or point1 == point4:
                Tools3D.sayz("point not overlapping")
            else:
                Area = Part.makePolygon([point1, point2, point3, point4, point1])
                fp.Shape = Part.makeFace(Area, "Part::FaceMakerBullseye")
        except:
            Tools3D.sayz("Redraw LineOblique Failed!")


class GetProperty:
    def __init__(self):
        FreeCAD.ActiveDocument.openTransaction('CreateAreaRectangle_3D')
        self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", ObjectTools.ObjectType.Area_Rectangular)
        self.__setProperty(self.obj)
        InitDoc3D.addObjectToGroup_helper(self.obj, "AreaG", "面")
        FreeCAD.ActiveDocument.commitTransaction()

    def __setProperty(self, obj):
        obj.addProperty("App::PropertyString", "Type").Type = ObjectTools.ObjectType.Area_Rectangular
        obj.addProperty("App::PropertyDistance", "Point1X").Point1X = 0
        obj.addProperty("App::PropertyDistance", "Point1Y").Point1Y = 0
        obj.addProperty("App::PropertyDistance", "Point1Z").Point1Z = 0
        obj.addProperty("App::PropertyDistance", "Point2X").Point2X = 0.01
        obj.addProperty("App::PropertyDistance", "Point2Y").Point2Y = 0.01
        obj.addProperty("App::PropertyDistance", "Point2Z").Point2Z = 0.01
        obj.addProperty("App::PropertyString", "Normal", "Normal", "").Normal = "X"
        Tools3D.addCommonProperty(obj)
        Tools3D.addAttributeToObject(obj)
        Tools3D.addHelperProperty(obj, 2)
        Tools3D.getHelperValue(obj)


def getObject():
    """
           返回获取的obj
        """
    AreaRectanglObj = GetProperty()
    AreaRectangle(AreaRectanglObj.obj)
    Tools3D.ViewProvider(AreaRectanglObj.obj.ViewObject)
    return AreaRectanglObj.obj
