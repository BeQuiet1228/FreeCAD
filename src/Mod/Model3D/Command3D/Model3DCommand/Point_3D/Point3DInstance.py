# -*- coding: utf8 -*-
import FreeCADGui
import FreeCAD
import Part
from Model3D.Tools import Tools3D, ObjectTools, InitDoc3D


class Point3D:
    def __init__(self, obj):
        obj.Proxy = self

    def onChanged(self, fp, prop):
        pass

    def execute(self, fp):
        try:
            point = Tools3D.transToRecVector(fp.Point1X.Value, fp.Point1Y.Value, fp.Point1Z.Value)
            fp.Shape = Part.makeSphere(0.0001, point)
        except:
            Tools3D.sayz("Redraw Point Failed!")


class GetProperty:
    def __init__(self):
        FreeCAD.ActiveDocument.openTransaction('CreatePoint_3D')
        self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", ObjectTools.ObjectType.Point)
        self.__setProperty(self.obj)
        InitDoc3D.addObjectToGroup_helper(self.obj, 'PointG', '点')
        FreeCAD.ActiveDocument.commitTransaction()

    def __setProperty(self, obj):
        obj.addProperty("App::PropertyString", "Type").Type = ObjectTools.ObjectType.Point

        if FreeCAD.ActiveDocument.CoordinateSystem == "Rectangular":
            obj.addProperty("App::PropertyDistance", "Point1X").Point1X = 0
            obj.addProperty("App::PropertyDistance", "Point1Y").Point1Y = 0
            obj.addProperty("App::PropertyDistance", "Point1Z").Point1Z = 0
        elif FreeCAD.ActiveDocument.CoordinateSystem == "Polar":
            obj.addProperty("App::PropertyDistance", "Point1X").Point1X = 0
            obj.addProperty("App::PropertyAngle", "Point1Y").Point1Y = 0
            obj.addProperty("App::PropertyDistance", "Point1Z").Point1Z = 0
        else:
            obj.addProperty("App::PropertyDistance", "Point1X").Point1X = 0
            obj.addProperty("App::PropertyDistance", "Point1Y").Point1Y = 0
            obj.addProperty("App::PropertyAngle", "Point1Z").Point1Z = 0
        Tools3D.addCommonProperty(obj)
        Tools3D.addAttributeToObject(obj)
        Tools3D.addHelperProperty(obj, 1)
        Tools3D.getHelperValue(obj)


def getObject():
    PointObj = GetProperty()
    Point3D(PointObj.obj)
    Tools3D.ViewProvider(PointObj.obj.ViewObject)
    return PointObj.obj

