#-*- coding: utf-8 -*-
import FreeCADGui
import Modeling3DCommand
import FreeCAD as App
import Units
import CylinderInstance as Instance
from Modeling.Common.Tools import ObjectsTools

def createCylinder():
    App.ActiveDocument.openTransaction("Cylinder")
    obj = App.ActiveDocument.addObject("Part::FeaturePython",ObjectsTools.ObjectType.Vol_Cylinder)
    Cylinder = Instance.Cylinder(obj)
    Instance.ViewProviderCylinder(obj.ViewObject)
    ObjectsTools.setRandColor(obj)
    # group=App.ActiveDocument.getObjectsByLabel("圆柱体")
    # if len(group):
    #     group[0].addObject(obj)
    # else:
    #     group=App.ActiveDocument.addObject("App::DocumentObjectGroup","Vol_Cylinder")
    #     group.Label="圆柱体"
    #     group.addObject(obj)
    
    #ObjectsTools.setFitViewOfObject(obj)
    # App.ActiveDocument.recompute()
    # FreeCADGui.SendMsgToActiveView("ViewFit")
    App.ActiveDocument.commitTransaction()
    return obj