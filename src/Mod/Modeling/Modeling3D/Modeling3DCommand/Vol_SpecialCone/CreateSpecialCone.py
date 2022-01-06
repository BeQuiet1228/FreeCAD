#-*- coding: utf-8 -*-
import FreeCADGui
import Modeling3DCommand
import FreeCAD as App
import Units
import SpecialConeInstance as Instance
from Modeling.Common.Tools import ObjectsTools


def createSpecialCone():
    App.ActiveDocument.openTransaction("SpecialCone")
    obj = App.ActiveDocument.addObject("Part::FeaturePython", ObjectsTools.ObjectType.Vol_SpecialCone)
    Instance.SpecialCone(obj)
    Instance.ViewProviderSpecialCone(obj.ViewObject)
    ObjectsTools.setRandColor(obj)
    # group=App.ActiveDocument.getObjectsByLabel("圆锥")
    # App.Console.PrintMessage(str(group)+"\n")
    # if len(group):
    #     App.Console.PrintMessage("0\n")
    #     group[0].addObject(obj)
    # else:
    #     App.Console.PrintMessage("1\n")
    #     group=App.ActiveDocument.addObject("App::DocumentObjectGroup","Vol_SpecialCone")
    #     group.Label="圆锥"
    #     group.addObject(obj)
    # ObjectsTools.setFitViewOfObject(obj)
    # App.ActiveDocument.recompute()
    # FreeCADGui.SendMsgToActiveView("ViewFit")
    App.ActiveDocument.commitTransaction()
    return obj