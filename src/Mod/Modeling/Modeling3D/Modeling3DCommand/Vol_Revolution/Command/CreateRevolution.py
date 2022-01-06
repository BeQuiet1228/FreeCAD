#-*- coding: utf-8 -*-
import FreeCADGui
import Modeling3DCommand
import FreeCAD as App
import Units
import RevolutionInstance as Instance
from Modeling.Common.Tools import ObjectsTools

def createRevolution():       
    App.ActiveDocument.openTransaction("Revolution")
    obj = App.ActiveDocument.addObject("Part::FeaturePython",ObjectsTools.ObjectType.Vol_Revolution)        

    Instance.VolRevolution(obj)
    Instance.ViewProviderFunction(obj.ViewObject)    

    ObjectsTools.setRandColor(obj)
    ObjectsTools.setFitViewOfObject(obj)     

    App.ActiveDocument.commitTransaction()
    return obj


def sayz(msg):
    App.Console.PrintMessage("\n")   
    App.Console.PrintMessage(msg)
    App.Console.PrintMessage("\n")   