#-*- coding: utf-8 -*-
import FreeCADGui
import Modeling3DCommand
import FreeCAD as App
import Units
import RectangularInstance as Instance
from Modeling.Common.Tools import ObjectsTools

def createRectangular():
    App.ActiveDocument.openTransaction("Rectangular")
    obj = App.ActiveDocument.addObject("Part::FeaturePython",ObjectsTools.ObjectType.Area_Rectangular)
    Instance.Rectangular(obj)
    Instance.ViewProviderRectangular(obj.ViewObject)
    ObjectsTools.setRandColor(obj)
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