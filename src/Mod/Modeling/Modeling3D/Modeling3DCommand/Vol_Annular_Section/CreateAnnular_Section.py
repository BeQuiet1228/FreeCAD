#-*- coding: utf-8 -*-
import FreeCADGui
import Modeling3DCommand
import FreeCAD as App
import Units
import Annular_SectionInstance as Instance
from Modeling.Common.Tools import ObjectsTools


def createAnnular_Section():
    App.ActiveDocument.openTransaction("Annular_Section")
    obj = App.ActiveDocument.addObject("Part::FeaturePython", ObjectsTools.ObjectType.Vol_Annular_Section)
    Annular_Section = Instance.Annular_Section(obj)
    Instance.ViewProviderAnnular_Section(obj.ViewObject)
    ObjectsTools.setRandColor(obj)
    # group=App.ActiveDocument.getObjectsByLabel("环形区域体")
    # if len(group):
    #     group[0].addObject(obj)
    # else:
    #     group=App.ActiveDocument.addObject("App::DocumentObjectGroup","Vol_Annular_Section")
    #     group.Label="环形区域体"
    #     group.addObject(obj)
    # ObjectsTools.setFitViewOfObject(obj)
    # App.ActiveDocument.recompute()
    # FreeCADGui.SendMsgToActiveView("ViewFit")
    App.ActiveDocument.commitTransaction()
    return obj