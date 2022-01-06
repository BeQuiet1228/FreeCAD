#-*- coding: utf-8 -*-
import FreeCADGui
import Modeling3DCommand
import FreeCAD as App
import Units
import ConformalInstance as Instance
from Modeling.Common.Tools import ObjectsTools
def createConformal():
    App.ActiveDocument.openTransaction("Conformal")
    obj = App.ActiveDocument.addObject("Part::FeaturePython",ObjectsTools.ObjectType.Vol_Conformal)
    objInstance=Instance.Conformal(obj)
    Instance.ViewProviderConformal(obj.ViewObject)
    ObjectsTools.setRandColor(obj)
    # group=App.ActiveDocument.getObjectsByLabel("正投影体")
    # App.Console.PrintMessage(str(group)+"\n")
    # if len(group):
    #     App.Console.PrintMessage("0\n")
    #     group[0].addObject(obj)
    # else:
    #     App.Console.PrintMessage("1\n")
    #     group=App.ActiveDocument.addObject("App::DocumentObjectGroup","Vol_Conformal")
    #     group.Label="正投影体"
    #     group.addObject(obj)
    # ObjectsTools.setFitViewOfObject(obj)
    # App.ActiveDocument.recompute()
    # 设置物体新建就被选中
    # FreeCADGui.Selection.addSelection(obj)
    # FreeCADGui.SendMsgToActiveView("ViewSelection")
    App.ActiveDocument.commitTransaction()
    return obj