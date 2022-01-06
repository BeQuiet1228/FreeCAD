#-*- coding: utf-8 -*-
import FreeCAD
import Part
from Common.Tools import CoordinateSystemTools
from Common.Tools import ObjectsTools
from Common.Tools import PlacementTools

class Circular(_DraftObject):
    "The Circle object"

    def __init__(self, obj):
        _DraftObject.__init__(self,obj,"Circle")
        obj.addProperty("App::PropertyAngle","CenterPoint","Draft",QT_TRANSLATE_NOOP("App::Property","Start angle of the arc"))
        obj.addProperty("App::PropertyAngle","StartPoint","Draft",QT_TRANSLATE_NOOP("App::Property","End angle of the arc (for a full circle, give it same value as First Angle)"))
        obj.addProperty("App::PropertyLength","EndPoint","Draft",QT_TRANSLATE_NOOP("App::Property","Radius of the circle"))
        obj.addProperty("App::PropertyBool","MakeFace","Draft",QT_TRANSLATE_NOOP("App::Property","Create a face"))
        obj.MakeFace = getParam("fillmode",True)

    def execute(self, obj):
        import Part
        plm = obj.Placement
        shape = Part.makeCircle(obj.Radius.Value,Vector(0,0,0),Vector(0,0,1),obj.FirstAngle.Value,obj.LastAngle.Value)
        if obj.FirstAngle.Value == obj.LastAngle.Value:
            shape = Part.Wire(shape)
            if hasattr(obj,"MakeFace"):
                if obj.MakeFace:
                    shape = Part.Face(shape)
            else:
                shape = Part.Face(shape)
        obj.Shape = shape
        obj.Placement = plm
        obj.positionBySupport()