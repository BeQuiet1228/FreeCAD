# -*- coding: utf-8 -*-
import FreeCAD
import FreeCADGui
from Model3D.Tools import Tools3D, ObjectTools, InitDoc3D
import Part, math
from FreeCAD import Base


class CreateExtruded:
    def __init__(self, obj):
        obj.Proxy = self

    def onChanged(self, fp, prop):
        pass

    def execute(self, fp):
        """
            获取文档中的面和线，然后进行建模
            需要先建立并选取一条线和一个面才能进行有效建模，如果选取了多个则可以手动在多个线或者多个面之间相互切换。
        """
        try:
            objLine = FreeCAD.ActiveDocument.getObjectsByLabel(fp.Line)[0]
            objArea = FreeCAD.ActiveDocument.getObjectsByLabel(fp.Area)[0]
            if objLine is None or objArea is None:
                Tools3D.sayz("错误，不能为空")
                return
            path = Part.Wire(objLine.Shape)
            fp.Shape = path.makePipeShell([objArea.Shape.Wires[0]],True,True)
            # shape1=path.makePipeShell([objArea.Shape.Wires[0]],True,True)
            # shape2=objArea.Shape
        except :
            Tools3D.sayz("ExtrudedInstance failed\n")

class Extruded:
    """
    工厂类
    """
    def __init__(self):
        FreeCAD.ActiveDocument.openTransaction('Create3DExtruded')
        self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "Vol_Extruded")
        self.__setProperty(self.obj)
        InitDoc3D.addObjectToGroup_helper(self.obj, "Extruded", "挤出体")
        FreeCAD.ActiveDocument.commitTransaction()
        # self.__setProperty(self.obj)

    def __setProperty(self, obj):
        obj.addProperty("App::PropertyString", "Type").Type = "Vol_Extruded"
        obj.addProperty("App::PropertyEnumeration", "Area", "Object of a Extruded", "Area of the Extruded")
        obj.Area = ObjectTools.getAllAreas()
        obj.addProperty("App::PropertyEnumeration", "Line", "Object of a Extruded", "Line of the Extruded")
        obj.Line = ObjectTools.getAllLines()
        Tools3D.addCommonPropertyToObject(obj)
        Tools3D.addAttributeToObject(obj)


def getObject():
    extruded = Extruded()
    CreateExtruded(extruded.obj)
    Tools3D.ViewProvider(extruded.obj.ViewObject)
    return extruded.obj
