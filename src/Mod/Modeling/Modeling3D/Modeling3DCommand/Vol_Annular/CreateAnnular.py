#-*- coding: utf-8 -*-
import FreeCADGui
import Modeling3DCommand
import FreeCAD as App
import Units
import AnnularInstance as Instance
from Modeling.Common.Tools import ObjectsTools


def createAnnular():
    """Create a new Annular instance

    Position arguments:
    solids -- List of solid shapes
    ship -- Ship owner

    Returned value:
    The new Annular object
    """
    App.ActiveDocument.openTransaction("Annular")
    obj = App.ActiveDocument.addObject("Part::FeaturePython", ObjectsTools.ObjectType.Vol_Annular)
    Annular = Instance.Annular(obj)
    Instance.ViewProviderAnnular(obj.ViewObject)
    ObjectsTools.setRandColor(obj)
    # group=App.ActiveDocument.getObjectsByLabel("环形体")
    # if len(group):
    #     group[0].addObject(obj)
    # else:
    #     group=App.ActiveDocument.addObject("App::DocumentObjectGroup","Vol_Annular")
    #     group.Label="环形体"
    #     group.addObject(obj)
    # ObjectsTools.setFitViewOfObject(obj)
    # App.ActiveDocument.recompute()
    # FreeCADGui.SendMsgToActiveView("ViewFit")
    App.ActiveDocument.commitTransaction()
    return obj
