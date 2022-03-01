#-*- coding: utf-8 -*-
import FreeCADGui
import Modeling3DCommand
import FreeCAD as App
import Units
import RhombusInstance as Instance
from Modeling.Common.Tools import ObjectsTools
def createRhombus():
    App.ActiveDocument.openTransaction("Rhombus")
    obj = App.ActiveDocument.addObject("Part::FeaturePython",ObjectsTools.ObjectType.Vol_Rhombus)
    Rhombus = Instance.Rhombus(obj)
    Instance.ViewProviderRhombus(obj.ViewObject)
    ObjectsTools.setRandColor(obj)
    # group=App.ActiveDocument.getObjectsByLabel("菱形体")
    # if len(group):
    #     group[0].addObject(obj)
    # else:
    #     group=App.ActiveDocument.addObject("App::DocumentObjectGroup","Vol_Parallelepipedal")
    #     group.Label="菱形体"
    #     group.addObject(obj)
    # ObjectsTools.setFitViewOfObject(obj)
    # App.ActiveDocument.recompute()
    # FreeCADGui.SendMsgToActiveView("ViewFit")
    App.ActiveDocument.commitTransaction()
    return obj