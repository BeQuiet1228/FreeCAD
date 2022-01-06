#-*- coding: utf-8 -*-
import FreeCADGui
import Modeling3DCommand
import FreeCAD as App
import Units
import AreaFunctionInstance as Instance
from Modeling.Common.Tools import ObjectsTools

def createFunctionArea():
                    #    name=ObjectsTools.ObjectType.Area_Function,
                    #    type=ObjectsTools.ObjectType.Area_Function,
                    #    order=100,
                    #    attribute=ObjectsTools.Attribute.NotDefine,
                    #    valueDx1="DX1",
                    #    ValueDx2="DX2",
                    #    ValueDx3="DX3",
                    #    isDx1=True,
                    #    isDx2=True,
                    #    isDX3=True,
                    #    Point_1X=None,
                    #    Point_1Y=None,
                    #    Point_1Z=None,
                    #    Point_2X=None,
                    #    Point_2Y=None,
                    #    Point_3Z=None,
                    #    Expression=None,
                    #    Precision=16
                       
    App.ActiveDocument.openTransaction("FunctionArea")
    obj = App.ActiveDocument.addObject("Part::FeaturePython",ObjectsTools.ObjectType.Area_Function)

    Instance.AreaFunction(obj)

    Instance.ViewProviderFunction(obj.ViewObject)

    ObjectsTools.setRandColor(obj)

    ObjectsTools.setFitViewOfObject(obj)

    App.ActiveDocument.commitTransaction()
    return obj