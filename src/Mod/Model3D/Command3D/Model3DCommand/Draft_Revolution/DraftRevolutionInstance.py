# -*- coding: utf-8 -*-
import FreeCAD
import FreeCADGui
from Model3D.Tools import Tools3D, ObjectTools, InitDoc3D
import Part


class CreateDraftRevolution:
    def __init__(self, obj):
        obj.Proxy = self

    def onChanged(self, fp, prop):
        pass

    def execute(self, fp):
        if fp.Area is None:
            Tools3D.sayz(U"草图旋转体必须先定义一个面")
            return
        try:
            point_base = Tools3D.transToRecVector(fp.Point1X.Value, fp.Point1Y.Value, fp.Point1Z.Value)
            point_top = Tools3D.transToRecVector(fp.Point2X.Value, fp.Point2Y.Value, fp.Point2Z.Value)
            tempArea = ObjectTools.getObjByLabel(fp.Area)
            fp.Shape = Part.makePicRevolution(tempArea.Name, 360, point_base, point_top)
        except:
            Tools3D.sayz("redraw fail")


class DraftRevolution:
    def __init__(self):
        FreeCAD.ActiveDocument.openTransaction('CreateDraftRevolution_3D')
        self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "Draft_Revolution")
        self.__setProperty(self.obj)
        InitDoc3D.addObjectToGroup_helper(self.obj, "Draft", "草图")
        FreeCAD.ActiveDocument.commitTransaction()
        # self.__setProperty(self.obj)

    def __setProperty(self, obj):
        obj.addProperty("App::PropertyString", "Type").Type = ObjectTools.ObjectType.Vol_Draft_Revolution
        obj.addProperty("App::PropertyEnumeration", "Area", "Object of a Revolution", "Area of the Revolution")
        obj.Area = ObjectTools.getAllAreas()
        if FreeCAD.ActiveDocument.CoordinateSystem == "Rectangular":
            obj.addProperty("App::PropertyDistance", "Point1X").Point1X = 0
            obj.addProperty("App::PropertyDistance", "Point1Y").Point1Y = 0
            obj.addProperty("App::PropertyDistance", "Point1Z").Point1Z = 0
            obj.addProperty("App::PropertyDistance", "Point2X").Point2X = 0
            obj.addProperty("App::PropertyDistance", "Point2Y").Point2Y = 0
            obj.addProperty("App::PropertyDistance", "Point2Z").Point2Z = 0.01
        elif FreeCAD.ActiveDocument.CoordinateSystem == "Polar":
            obj.addProperty("App::PropertyDistance", "Point1X").Point1X = 0
            obj.addProperty("App::PropertyAngle", "Point1Y").Point1Y = 0
            obj.addProperty("App::PropertyDistance", "Point1Z").Point1Z = 0
            obj.addProperty("App::PropertyDistance", "Point2X").Point2X = 0
            obj.addProperty("App::PropertyAngle", "Point2Y").Point2Y = 0
            obj.addProperty("App::PropertyDistance", "Point2Z").Point2Z = 0
        else:
            obj.addProperty("App::PropertyDistance", "Point1X").Point1X = 0
            obj.addProperty("App::PropertyDistance", "Point1Y").Point1Y = 0
            obj.addProperty("App::PropertyAngle", "Point1Z").Point1Z = 0
            obj.addProperty("App::PropertyDistance", "Point2X").Point2X = 0
            obj.addProperty("App::PropertyDistance", "Point2Y").Point2Y = 0
            obj.addProperty("App::PropertyAngle", "Point2Z").Point2Z = 0
        Tools3D.addCommonPropertyToObject(obj)
        Tools3D.addAttributeToObject(obj)
        Tools3D.addHelperProperty(obj, 2)
        Tools3D.getHelperValue(obj)


def getObject():
    draft_revolution = DraftRevolution()
    CreateDraftRevolution(draft_revolution.obj)
    Tools3D.ViewProvider(draft_revolution.obj.ViewObject)
    return draft_revolution.obj
