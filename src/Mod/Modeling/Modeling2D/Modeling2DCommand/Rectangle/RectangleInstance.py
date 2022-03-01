# -*- coding: utf8 -*-
import FreeCADGui
import Draft
import DraftVecUtils
import DraftTools
import DraftGui
import FreeCAD
import Part
from Modeling.Modeling2D.Tools import Tools2D, ToolsForDisplay
from Modeling.Modeling2D.Modeling2DCommand.CallBack.CallBackTools import processObject
from Modeling.Modeling2D.Modeling2DCommand.Rectangle import RectangleDlgMain


class Rectangle2D(DraftTools.Rectangle):
    def createObject(self):
        "creates the final object in the current doc"
        FreeCAD.ActiveDocument.openTransaction("Rectangle creation")
        p1 = self.node[0]
        p3 = self.node[-1]

        obj = FreeCAD.ActiveDocument.addObject("Part::Part2DObjectPython", "Rectangle")
        ObjectCreate(obj)


        obj.Point1X = p1.x
        obj.Point1Y = p1.y
        obj.Point2X = p3.x
        obj.Point2Y = p3.y
        processObject(obj, Tools2D.ObjectType.Rectangle)
        Draft._ViewProviderRectangle(obj.ViewObject)

        Form = RectangleDlgMain.ShowDialog(obj, True)
        Form.exec_()
        self.finish(cont=True)
        FreeCAD.ActiveDocument.commitTransaction()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling2D/modeling2DResources/2d矩形面.svg"
        MenuText = Tools2D.QT_TRANSLATE_NOOP(
            'CreateRectangle',
            '矩形面')
        ToolTip = Tools2D.QT_TRANSLATE_NOOP(
            'CreateRectangle',
            'Rectangle')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreateRectangle_2D', Rectangle2D())


class ObjectCreate:
    def __init__(self, obj):
        "Add some custom properties to our box feature"
        obj.addProperty("App::PropertyDistance", "Point1X", "Fillet2D", " centre point1 X").Point1X = 0
        obj.addProperty("App::PropertyDistance", "Point1Y", "Fillet2D", " centre point1 Y").Point1Y = 0
        obj.addProperty("App::PropertyDistance", "Point2X", "Fillet2D", " centre point2 X").Point2X = 10
        obj.addProperty("App::PropertyDistance", "Point2Y", "Fillet2D", " centre point2 Y").Point2Y = 10
        obj.addProperty("Part::PropertyPartShape", "Shape", "Fillet2D", "Shape of the octahedron")
        obj.Proxy = self

    def execute(self, fp):
        point1 = FreeCAD.Vector(fp.Point1X.Value, fp.Point1Y.Value, 0)
        point2 = FreeCAD.Vector(fp.Point2X.Value, fp.Point1Y.Value, 0)
        point3 = FreeCAD.Vector(fp.Point2X.Value, fp.Point2Y.Value, 0)
        point4 = FreeCAD.Vector(fp.Point1X.Value, fp.Point2Y.Value, 0)
        fp.Shape = self.make_rec_face(point1, point2, point3, point4)
        ToolsForDisplay.setColors(fp)

    def make_rec_face(self, v1, v2, v3, v4):
        l1 = Part.LineSegment(v1, v2)
        l2 = Part.LineSegment(v2, v3)
        l3 = Part.LineSegment(v3, v4)
        l4 = Part.LineSegment(v4, v1)
        S1 = Part.Shape([l1, l2, l3, l4])
        # 得到拓扑形状的边
        W = Part.Wire(S1.Edges)
        # 创建面
        face = Part.Face(W)
        return face