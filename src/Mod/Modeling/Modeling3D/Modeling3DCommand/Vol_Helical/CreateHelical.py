#-*- coding: utf-8 -*-
import FreeCADGui
import Modeling3DCommand
import FreeCAD as App
import Units
import HelicalInstance as Instance
from Modeling.Common.Tools import ObjectsTools
def createHelical():
    App.ActiveDocument.openTransaction("Helical")
    obj = App.ActiveDocument.addObject("Part::FeaturePython",ObjectsTools.ObjectType.Vol_Helical)
    Instance.Helical(obj)
    Instance.ViewProviderHelical(obj.ViewObject)
    ObjectsTools.setRandColor(obj)
    # group=App.ActiveDocument.getObjectsByLabel("螺旋体")
    # App.Console.PrintMessage(str(group)+"\n")
    # if len(group):
    #     App.Console.PrintMessage("0\n")
    #     group[0].addObject(obj)
    # else:
    #     App.Console.PrintMessage("1\n")
    #     group=App.ActiveDocument.addObject("App::DocumentObjectGroup","Vol_Helical")
    #     group.Label="螺旋体"
    #     group.addObject(obj)
    # ObjectsTools.setFitViewOfObject(obj)
    # App.ActiveDocument.recompute()
    # FreeCADGui.SendMsgToActiveView("ViewFit")
    App.ActiveDocument.commitTransaction()
    return obj