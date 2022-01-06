#-*- coding: utf-8 -*-
import FreeCADGui
import Modeling3DCommand
import FreeCAD as App
import Units
import Toroidal_SectionInstance as Instance
from Modeling.Common.Tools import ObjectsTools


def createToroidal_Section():
    App.ActiveDocument.openTransaction("Torodial_Section")
    obj = App.ActiveDocument.addObject("Part::FeaturePython", ObjectsTools.ObjectType.Vol_Toroidal_Section)
    Toroidal_Section = Instance.Toroidal_Section(obj)
    Instance.ViewProviderToroidal_Section(obj.ViewObject)
    ObjectsTools.setRandColor(obj)
    # group=App.ActiveDocument.getObjectsByLabel("半环形体")
    # if len(group):
    #     group[0].addObject(obj)
    # else:
    #     group=App.ActiveDocument.addObject("App::DocumentObjectGroup","Vol_Toroidal_Section")
    #     group.Label="半环形体"
    #     group.addObject(obj)
    # ObjectsTools.setFitViewOfObject(obj)
    # App.ActiveDocument.recompute()
    # FreeCADGui.SendMsgToActiveView("ViewFit")
    App.ActiveDocument.commitTransaction()
    return obj