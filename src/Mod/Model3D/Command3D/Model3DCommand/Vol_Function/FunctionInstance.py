# -*- coding: utf8 -*-
import FreeCAD
import Part
import PartChipic
from Model3D.Tools import Tools3D, ObjectTools, InitDoc3D


class VolFunction:
    def __init__(self, obj):
        obj.Proxy = self

    def onChanged(self, fp, prop):
        pass

    def execute(self, fp):
        maxX = max(fp.Point1X.Value, fp.Point2X.Value)
        minX = min(fp.Point1X.Value, fp.Point2X.Value)
        maxY = max(fp.Point1Y.Value, fp.Point2Y.Value)
        minY = min(fp.Point1Y.Value, fp.Point2Y.Value)
        maxZ = max(fp.Point1Z.Value, fp.Point2Z.Value)
        minZ = min(fp.Point1Z.Value, fp.Point2Z.Value)

        sys = FreeCAD.ActiveDocument.CoordinateSystem

        
        px = fp.precision_x 
        py = fp.precision_y 
        pz = fp.precision_z

        expressionStr = ObjectTools.parseExpressionStr(fp.Expression.replace(" ", ""))
        Tools3D.sayz("------------------------------")
        Tools3D.sayz(expressionStr)
        Tools3D.sayz("------------------------------")
        try:
            fp.Shape = Part.makeFunctionShape(minX, maxX, minY, maxY, minZ, maxZ,
                                               sys,
                                               expressionStr,
                                               px, py, pz)
            return
        except:
            Tools3D.sayz("Redraw Function Failed!")


class Function:
    """
    工厂类
    """

    def __init__(self):
        FreeCAD.ActiveDocument.openTransaction('CreateVolFunction_3D')
        self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", ObjectTools.ObjectType.Vol_Function)
        self.__setProperty(self.obj)
        InitDoc3D.addObjectToGroup_helper(self.obj, "Function", "函数体")
        FreeCAD.ActiveDocument.commitTransaction()
        # self.__setProperty(self.obj)

    def __setProperty(self, obj):
        obj.addProperty("App::PropertyString", "Type").Type = ObjectTools.ObjectType.Vol_Function
        if FreeCAD.ActiveDocument.CoordinateSystem == "Rectangular":
            obj.addProperty("App::PropertyDistance", "Point1X").Point1X = -0.01
            obj.addProperty("App::PropertyDistance", "Point1Y").Point1Y = -0.01
            obj.addProperty("App::PropertyDistance", "Point1Z").Point1Z = -0.01
            obj.addProperty("App::PropertyDistance", "Point2X").Point2X = 0.01
            obj.addProperty("App::PropertyDistance", "Point2Y").Point2Y = 0.01
            obj.addProperty("App::PropertyDistance", "Point2Z").Point2Z = 0.01
            obj.addProperty("App::PropertyString", "Expression").Expression = "x*x+y*y+z*z-1"
        elif FreeCAD.ActiveDocument.CoordinateSystem == "Polar":
            obj.addProperty("App::PropertyDistance", "Point1X").Point1X = 0
            obj.addProperty("App::PropertyAngle", "Point1Y").Point1Y = 0
            obj.addProperty("App::PropertyDistance", "Point1Z").Point1Z = 0
            obj.addProperty("App::PropertyDistance", "Point2X").Point2X = 0
            obj.addProperty("App::PropertyAngle", "Point2Y").Point2Y = 0
            obj.addProperty("App::PropertyDistance", "Point2Z").Point2Z = 0
            obj.addProperty("App::PropertyString", "Expression").Expression = ""
        else:
            obj.addProperty("App::PropertyDistance", "Point1X").Point1X = 0
            obj.addProperty("App::PropertyDistance", "Point1Y").Point1Y = 0
            obj.addProperty("App::PropertyAngle", "Point1Z").Point1Z = 0
            obj.addProperty("App::PropertyDistance", "Point2X").Point2X = 0
            obj.addProperty("App::PropertyDistance", "Point2Y").Point2Y = 0
            obj.addProperty("App::PropertyAngle", "Point2Z").Point2Z = 0
            obj.addProperty("App::PropertyString", "Expression").Expression = ""

        obj.addProperty("App::PropertyFloat", "precision_x", "Object of a Function",
                        "Precision of the function").precision_x = 10
        obj.addProperty("App::PropertyFloat", "precision_y", "Object of a Function",
                        "Precision of the function").precision_y = 10
        obj.addProperty("App::PropertyFloat", "precision_z", "Object of a Function",
                        "Precision of the function").precision_z = 10
        Tools3D.addCommonPropertyToObject(obj)
        Tools3D.addAttributeToObject(obj)
        Tools3D.addHelperProperty(obj, 2)
        Tools3D.getHelperValue(obj)


def getObject():
    """
    返回获取的obj
    """
    function = Function()
    VolFunction(function.obj)
    Tools3D.ViewProvider(function.obj.ViewObject)
    return function.obj
