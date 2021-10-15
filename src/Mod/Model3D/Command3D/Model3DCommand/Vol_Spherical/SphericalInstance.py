# -*- coding: utf8 -*-
import FreeCAD
import Part
from Model3D.Command3D.Model3DCommand.Object_Array import ArrayDraftPack
from Model3D.Tools import Tools3D, ObjectTools, InitDoc3D


class VolSpherical:
    def __init__(self, obj):
        obj.Proxy = self

    def onChanged(self, fp, prop):
        pass

    def execute(self, fp):
        point = Tools3D.transToRecVector(fp.Point1X.Value, fp.Point1Y.Value, fp.Point1Z.Value)
        if fp.Radius.Value <= 0:
            Tools3D.sayz("半径有误，请重新输入")
            return
        else:
            try:
                fp.Shape = Part.makeSphere(fp.Radius, point)
                return
            except:
                Tools3D.sayz("Redraw Spherical Failed!")
                
class Spherical:
    """
    工厂类
    """
    def __init__(self):
        FreeCAD.ActiveDocument.openTransaction('CreateVolSpherical_3D')
        self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", ObjectTools.ObjectType.Vol_Spherical)
        self.__setProperty(self.obj)
        InitDoc3D.addObjectToGroup_helper(self.obj, "Spherical", "球体")
        FreeCAD.ActiveDocument.commitTransaction()

    def __setProperty(self, obj):
        obj.addProperty("App::PropertyString", "Type").Type = ObjectTools.ObjectType.Vol_Spherical
        if FreeCAD.ActiveDocument.CoordinateSystem == "Rectangular":
            obj.addProperty("App::PropertyDistance", "Point1X").Point1X = 0
            obj.addProperty("App::PropertyDistance", "Point1Y").Point1Y = 0
            obj.addProperty("App::PropertyDistance", "Point1Z").Point1Z = 0

        elif FreeCAD.ActiveDocument.CoordinateSystem == "Polar":
            obj.addProperty("App::PropertyDistance", "Point1X").Point1X = 0
            obj.addProperty("App::PropertyAngle", "Point1Y").Point1Y = 0
            obj.addProperty("App::PropertyDistance", "Point1Z").Point1Z = 0
        else:
            obj.addProperty("App::PropertyDistance", "Point1X").Point1X = 0
            obj.addProperty("App::PropertyDistance", "Point1Y").Point1Y = 0
            obj.addProperty("App::PropertyAngle", "Point1Z").Point1Z = 0
        obj.addProperty("App::PropertyDistance", "Radius").Radius = 0.01
        Tools3D.addCommonPropertyToObject(obj)
        Tools3D.addAttributeToObject(obj)
        Tools3D.addHelperProperty(obj, 1)
        Tools3D.getHelperValue(obj)
        Tools3D.addRadiusProperty(obj)
        Tools3D.getRadiusProperty(obj)


def getObject():
    """
    返回获取的obj
    """
    spherical = Spherical()
    VolSpherical(spherical.obj)
    Tools3D.ViewProvider(spherical.obj.ViewObject)
    return spherical.obj
