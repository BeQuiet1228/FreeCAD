#-*- coding: utf-8 -*-
import FreeCADGui
import Modeling3DCommand
import FreeCAD as App
import Units
import ParallelepipedalInstance as Instance
from Modeling.Common.Tools import ObjectsTools
def createParallelepipedal():
    App.ActiveDocument.openTransaction("Parallelepipedal")
    obj = App.ActiveDocument.addObject("Part::FeaturePython",ObjectsTools.ObjectType.Vol_Parallelepipedal)
    Parallelepipedal = Instance.Parallelepipedal(obj)
    Instance.ViewProviderParallelepipedal(obj.ViewObject)
    ObjectsTools.setRandColor(obj)
    # group=App.ActiveDocument.getObjectsByLabel("平行六面体")
    # if len(group):
    #     group[0].addObject(obj)
    # else:
    #     group=App.ActiveDocument.addObject("App::DocumentObjectGroup","Vol_Parallelepipedal")
    #     group.Label="平行六面体"
    #     group.addObject(obj)
    # ObjectsTools.setFitViewOfObject(obj)
    # App.ActiveDocument.recompute()
    # FreeCADGui.SendMsgToActiveView("ViewFit")
    App.ActiveDocument.commitTransaction()
    return obj