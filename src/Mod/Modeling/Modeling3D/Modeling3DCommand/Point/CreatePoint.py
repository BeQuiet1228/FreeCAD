#-*- coding: utf-8 -*-
import FreeCADGui
import Modeling3DCommand
import FreeCAD as App
import Units
import PointInstance as Instance
from Modeling.Common.Tools import ObjectsTools


def createPoint():
    App.ActiveDocument.openTransaction("PointObj")
    obj = App.ActiveDocument.addObject("Part::FeaturePython", ObjectsTools.ObjectType.Point)
    Instance.PointObj(obj)
    Instance.ViewProviderPoint(obj.ViewObject)
    #FreeCADGui.ActiveDocument.getObject(obj).DisplayMode="Flat Lines"
    ObjectsTools.setRandColor(obj)
    # group=App.ActiveDocument.getObjectsByLabel("点")
    # App.Console.PrintMessage(str(group)+"\n")
    # if len(group):
    #     App.Console.PrintMessage("0\n")
    #     group[0].addObject(obj)
    # else:
    #     App.Console.PrintMessage("1\n")
    #     group=App.ActiveDocument.addObject("App::DocumentObjectGroup","Point")
    #     group.Label="点"
    #     group.addObject(obj)
    # ObjectsTools.setFitViewOfObject(obj)
    # App.ActiveDocument.recompute()
    # FreeCADGui.SendMsgToActiveView("ViewSelection")
    App.ActiveDocument.commitTransaction()
    return obj
