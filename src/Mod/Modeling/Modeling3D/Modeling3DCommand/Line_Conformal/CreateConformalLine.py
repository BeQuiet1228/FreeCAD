#-*- coding: utf-8 -*-
import FreeCADGui
import Modeling3DCommand
import FreeCAD as App
import Units
import ConformalLineInstance as Instance
from Modeling.Common.Tools import ObjectsTools

def createConformalLine():
    App.ActiveDocument.openTransaction("ConformalLine")
    obj = App.ActiveDocument.addObject("Part::FeaturePython","Conformal_Line")
    Instance.ConformalLine(obj)
    Instance.ViewProviderConformalLine(obj.ViewObject)
    obj.ViewObject.LineWidth=5.0
    obj.setEditorMode("Type",2)
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
    # FreeCADGui.SendMsgToActiveView("ViewSelection")
    App.ActiveDocument.commitTransaction()
    return obj