#-*- coding: utf-8 -*-
import FreeCADGui
import Modeling3DCommand
import FreeCAD as App
import Units
import ConformalAreaInstance as Instance
from Modeling.Common.Tools import ObjectsTools

def createConformalArea():
    App.ActiveDocument.openTransaction("ConformalArea")

    obj = App.ActiveDocument.addObject("Part::FeaturePython",ObjectsTools.ObjectType.Area_Conformal)
    Instance.ConformalArea(obj)
    Instance.ViewProviderConformalArea(obj.ViewObject)
    ObjectsTools.setRandColor(obj)
    # ObjectsTools.setInitTransparency(obj)
    # group=App.ActiveDocument.getObjectsByLabel("面")
    # App.Console.PrintMessage(str(group)+"\n")
    # if len(group):
    #     App.Console.PrintMessage("0\n")
    #     group[0].addObject(obj)
    # else:
    #     App.Console.PrintMessage("1\n")
    #     group=App.ActiveDocument.addObject("App::DocumentObjectGroup","Area")
    #     group.Label="面"
    #     group.addObject(obj)
    # ObjectsTools.setFitViewOfObject(obj)
    # App.ActiveDocument.recompute()
    # FreeCADGui.SendMsgToActiveView("ViewFit")
    App.ActiveDocument.commitTransaction()
    return obj