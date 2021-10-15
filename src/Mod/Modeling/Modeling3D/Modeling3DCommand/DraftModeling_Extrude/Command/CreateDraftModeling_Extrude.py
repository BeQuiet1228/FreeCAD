#-*- coding: utf-8 -*-
import FreeCADGui
import Modeling3DCommand
import FreeCAD as App
import Units
import DraftModeling_ExtrudeInstance as Instance
from Modeling.Common.Tools import ObjectsTools
from Modeling3D.Tools import RebuildForUITools,ModelingByUITools
def createDraftModeling_Extrude(obj=None,area=None,length=None):
    App.ActiveDocument.openTransaction("DraftModeling_Extrude")
    if not obj:
        obj = App.ActiveDocument.addObject("Part::FeaturePython",ObjectsTools.ObjectType.Vol_Draft_Extrude)

    Instance.DraftModeling_Extrude(obj)

    #初始化
    if area:
        obj.Area=area
    if length:
        ModelingByUITools.setValue(obj,"Length",str(length))

    Instance.ViewProviderDraftModeling_Extrude(obj.ViewObject)
    ObjectsTools.setRandColor(obj)

    ObjectsTools.setFitViewOfObject(obj)
    App.ActiveDocument.recompute()
    # FreeCADGui.SendMsgToActiveView("ViewFit")
    App.ActiveDocument.commitTransaction()
    return obj