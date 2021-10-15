#-*- coding: utf-8 -*-
import FreeCADGui
import Modeling3DCommand
import FreeCAD as App
import Units
import ObliqueLineInstance as Instance
from Modeling.Common.Tools import ObjectsTools
def createObliqueLine():
    App.ActiveDocument.openTransaction("ObliqueLine")
    obj = App.ActiveDocument.addObject("Part::FeaturePython",ObjectsTools.ObjectType.Line_Oblique)
    Instance.ObliqueLine(obj)
    Instance.ViewProviderObliqueLine(obj.ViewObject)
    obj.ViewObject.LineWidth=5.0
    ObjectsTools.setRandColor(obj)
    # group=App.ActiveDocument.getObjectsByLabel("线")
    # App.Console.PrintMessage(str(group)+"\n")
    # if len(group):
    #     App.Console.PrintMessage("0\n")
    #     group[0].addObject(obj)
    # else:
    #     App.Console.PrintMessage("1\n")
    #     group=App.ActiveDocument.addObject("App::DocumentObjectGroup","Line")
    #     group.Label="线"
    #     group.addObject(obj)
    # ObjectsTools.setFitViewOfObject(obj)
    # App.ActiveDocument.recompute()
    # FreeCADGui.SendMsgToActiveView("ViewFit")
    App.ActiveDocument.commitTransaction()
    return obj