# -*- coding: utf-8 -*-
import FreeCAD
import FreeCADGui
from Model3D.Tools import Tools3D, ObjectTools, InitDoc3D
import Part


class CreateDraftExtruded:
    def __init__(self, obj):
        obj.Proxy = self

    def onChanged(self, fp, prop):
        pass

    def execute(self, fp):
        try:
            # objArea = FreeCAD.ActiveDocument.getObjectsByLabel(fp.Area)[0]
            tempArea = ObjectTools.getObjByLabel(fp.Area)
            fp.Shape = Part.makeExtrude(tempArea.Name, -fp.Length.Value)
        except:
            Tools3D.sayz("redraw fail")


class DraftExtruded:
    def __init__(self):
        FreeCAD.ActiveDocument.openTransaction('CreateDraftExtruded_3D')
        self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "Draft_Extruded")
        self.__setProperty(self.obj)
        InitDoc3D.addObjectToGroup_helper(self.obj, "Draft", "草图")
        FreeCAD.ActiveDocument.commitTransaction()
        # self.__setProperty(self.obj)

    def __setProperty(self, obj):
        obj.addProperty("App::PropertyString", "Type").Type = ObjectTools.ObjectType.Vol_Draft_Extrude
        obj.addProperty("App::PropertyEnumeration", "Area", "Object of a Extruded", "Area of the Extruded")
        obj.Area = ObjectTools.getAllAreas()
        obj.addProperty("App::PropertyDistance", "Length").Length = 0.002
        # 此处根据坐标系的不同，helper的属性也不同。App::PropertyDistance，App::PropertyAngle
        obj.addProperty("App::PropertyDistance", "helper").helper = 0
        Tools3D.addCommonPropertyToObject(obj)
        Tools3D.addAttributeToObject(obj)


def getObject():
    draft_extruded = DraftExtruded()
    CreateDraftExtruded(draft_extruded.obj)
    Tools3D.ViewProvider(draft_extruded.obj.ViewObject)
    return draft_extruded.obj
