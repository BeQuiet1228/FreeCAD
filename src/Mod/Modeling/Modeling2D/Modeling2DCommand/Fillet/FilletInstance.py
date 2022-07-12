# -*- coding: utf-8 -*-
import traceback

import FreeCAD, Part, FreeCADGui
from math import pi, radians
import pivy
from pivy import coin
from Modeling.Modeling2D.Modeling2DCommand.CallBack.CallBackTools import processObject
from Modeling.Modeling2D.Modeling2DCommand.Fillet import FilletDlgMain
from Modeling.Modeling2D.Tools.Tools2D import ObjectType
from Modeling.Modeling2D.Tools import Tools2D


class Fillet2D():
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False
    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling2D/modeling2DResources/倒角形.svg"
        MenuText = Tools2D.QT_TRANSLATE_NOOP(
            'CreateFillet',
            '倒角圆面')
        ToolTip = Tools2D.QT_TRANSLATE_NOOP(
            'CreateFillet',
            'Fillet')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

    def Activated(self):
        self.finish()

    def finish(self):
        # 打开对话框
        FreeCAD.ActiveDocument.openTransaction("Fillet creation")
        Fillet = FreeCAD.ActiveDocument.addObject("Part::Part2DObjectPython", "FilletObj")
        ObjectCreate(Fillet)
        ViewProvider(Fillet.ViewObject)
        processObject(Fillet, Tools2D.ObjectType.Fillet)
        Form = FilletDlgMain.ShowDialog(Fillet, True)
        Form.exec_()
        FreeCAD.ActiveDocument.commitTransaction()
        pass


class ObjectCreate:
    def __init__(self, obj):
        "Add some custom properties to our box feature"
        obj.addProperty("App::PropertyLength", "Radius", "Fillet2D", "Radius").Radius = 0.05
        obj.addProperty("App::PropertyDistance", "Point1X", "Fillet2D", " centre point1 X").Point1X = 0
        obj.addProperty("App::PropertyDistance", "Point1Y", "Fillet2D", " centre point1 Y").Point1Y = 0
        obj.addProperty("App::PropertyDistance", "Point2X", "Fillet2D", " centre point2 X").Point2X = 0.1
        obj.addProperty("App::PropertyDistance", "Point2Y", "Fillet2D", " centre point2 Y").Point2Y = 0.1
        obj.addProperty("App::PropertyAngle", "StartAngle", "Fillet2D", " StartAngle").StartAngle = 0
        obj.addProperty("App::PropertyAngle", "EndAngle", "Fillet2D", " EndAngle").EndAngle = 90
        obj.addProperty("Part::PropertyPartShape", "Shape", "Fillet2D", "Shape of the octahedron")
        obj.Proxy = self

    def execute(self, fp):
        # 检测点是否正确
        if fp.Point1X.Value == fp.Point2X.Value:
            return
        if fp.Point1Y.Value == fp.Point2Y.Value:
            return
        # 检测角度是否正确

        # 点
        point1 = FreeCAD.Vector(fp.Point1X.Value, fp.Point1Y.Value, 0)
        point2 = FreeCAD.Vector(fp.Point2X.Value, fp.Point1Y.Value, 0)
        point3 = FreeCAD.Vector(fp.Point2X.Value, fp.Point2Y.Value, 0)
        point4 = FreeCAD.Vector(fp.Point1X.Value, fp.Point2Y.Value, 0)
        # 画矩形
        shape = self.make_rec_face(point1, point2, point3, point4)
        arc = False
        # 画圆弧

        if fp.Radius.Value - 0.00001 <= abs(fp.Point2X.Value - fp.Point1X.Value) \
                and fp.Radius.Value - 0.00001 <= abs(fp.Point2Y.Value - fp.Point1Y.Value):
            if 0 < (fp.EndAngle.Value - fp.StartAngle.Value) <= 90:
                if fp.Point2X.Value > fp.Point1X.Value:
                    if fp.Point2Y.Value > fp.Point1Y.Value:
                        if 90 >= fp.StartAngle.Value >= 0 and 90 >= fp.EndAngle.Value >= 0:
                            arc = self.make_arc_face(point1, fp.Radius, fp.StartAngle.Value, fp.EndAngle.Value)
                    elif fp.Point2Y.Value < fp.Point1Y.Value:
                        if 360 >= fp.StartAngle.Value >= 270 and 360 >= fp.EndAngle.Value >= 270:
                            arc = self.make_arc_face(point1, fp.Radius, fp.StartAngle.Value, fp.EndAngle.Value)
                elif fp.Point2X.Value < fp.Point1X.Value:
                    if fp.Point2Y.Value > fp.Point1Y.Value:
                        if 180 >= fp.StartAngle.Value >= 90 and 180 >= fp.EndAngle.Value >= 90:
                            arc = self.make_arc_face(point1, fp.Radius, fp.StartAngle.Value, fp.EndAngle.Value)
                    elif fp.Point2Y.Value < fp.Point1Y.Value:
                        if 270 >= fp.StartAngle.Value >= 180 and 270 >= fp.EndAngle.Value >= 180:
                            arc = self.make_arc_face(point1, fp.Radius, fp.StartAngle.Value, fp.EndAngle.Value)
            else:
                FreeCAD.Console.PrintError("Fillet坐标点画角度错误\n")
                return
        else:
            FreeCAD.Console.PrintError("Fillet坐标点画圆弧半径错误\n")
            return
        # 画扇形
        if arc:
            sec = self.make_sec_face(arc, point1)
            shape = shape.cut(sec)
        # 画圆弧后矩形

        if arc:
            arc_edge = arc.toShape()
            x1 = arc_edge.Vertexes[0].X
            y1 = arc_edge.Vertexes[0].Y
            x2 = arc_edge.Vertexes[1].X
            y2 = arc_edge.Vertexes[1].Y
            if (fp.Point2X.Value > fp.Point1X.Value and fp.Point2Y.Value > fp.Point1Y.Value) or \
                    (fp.Point2X.Value < fp.Point1X.Value and fp.Point2Y.Value < fp.Point1Y.Value):
                # 矩形1
                if x1 != point2.x and y1 != point2.y:
                    p1 = FreeCAD.Vector(point1.x, point1.y, 0)
                    p2 = FreeCAD.Vector(point1.x, y1, 0)
                    p3 = FreeCAD.Vector(point2.x, y1, 0)
                    p4 = FreeCAD.Vector(point2.x, point2.y, 0)
                    rec1 = self.make_rec_face(p1, p2, p3, p4)
                    shape = shape.cut(rec1)
                # 矩形2
                if x2 != point4.x and y2 != point4.y:
                    p1 = FreeCAD.Vector(point1.x, point1.y, 0)
                    p2 = FreeCAD.Vector(x2, point1.y, 0)
                    p3 = FreeCAD.Vector(x2, point4.y, 0)
                    p4 = FreeCAD.Vector(point4.x, point4.y, 0)
                    rec2 = self.make_rec_face(p1, p2, p3, p4)
                    shape = shape.cut(rec2)
            if (fp.Point2X.Value < fp.Point1X.Value and fp.Point2Y.Value > fp.Point1Y.Value) or \
                    (fp.Point2X.Value > fp.Point1X.Value and fp.Point2Y.Value < fp.Point1Y.Value):
                if x1 != point4.x and y1 != point4.y:
                    p1 = FreeCAD.Vector(point1.x, point1.y, 0)
                    p2 = FreeCAD.Vector(x1, point1.y, 0)
                    p3 = FreeCAD.Vector(x1, point4.y, 0)
                    p4 = FreeCAD.Vector(point4.x, point4.y, 0)
                    rec1 = self.make_rec_face(p1, p2, p3, p4)
                    shape = shape.cut(rec1)
                # 矩形2
                if x2 != point2.x and y2 != point2.y:
                    p1 = FreeCAD.Vector(point1.x, point1.y, 0)
                    p2 = FreeCAD.Vector(point1.x, y2, 0)
                    p3 = FreeCAD.Vector(point2.x, y2, 0)
                    p4 = FreeCAD.Vector(point2.x, point2.y, 0)
                    rec2 = self.make_rec_face(p1, p2, p3, p4)
                    shape = shape.cut(rec2)

        fp.Shape = shape

        from Modeling.Modeling2D.Tools import ToolsForDisplay
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

    def make_arc_face(self, circlePoint, radius, startAngle, endAngle):
        circle = Part.Circle(circlePoint, FreeCAD.Vector(0, 0, 1), radius.Value)
        arc = Part.Arc(circle, radians(startAngle), radians(endAngle))
        return arc

    def make_sec_face(self, arc, circlePoint):
        arc_edge = arc.toShape()
        p1 = FreeCAD.Vector(arc_edge.Vertexes[0].X, arc_edge.Vertexes[0].Y, 0)
        p2 = FreeCAD.Vector(arc_edge.Vertexes[1].X, arc_edge.Vertexes[1].Y, 0)
        l1 = Part.LineSegment(circlePoint, p1)
        l2 = Part.LineSegment(circlePoint, p2)

        S1 = Part.Shape([arc, l1, l2])
        # 得到拓扑形状的边
        W = Part.Wire(S1.Edges)
        # 创建面
        face = Part.Face(W)
        return face

class ViewProvider:
    def __init__(self, obj):
        "Set this object to the proxy object of the actual view provider"
        obj.addProperty("App::PropertyColor", "Color", "Octahedron", "Color of the octahedron").Color = (1.0, 0.0, 0.0)
        obj.Proxy = self

    def attach(self, obj):
        "Setup the scene sub-graph of the view provider, this method is mandatory"
        self.shaded = coin.SoGroup()
        self.wireframe = coin.SoGroup()
        self.scale = coin.SoScale()
        self.color = coin.SoBaseColor()

        self.data = coin.SoCoordinate3()
        self.face = coin.SoIndexedLineSet()

        self.shaded.addChild(self.scale)
        self.shaded.addChild(self.color)
        self.shaded.addChild(self.data)
        self.shaded.addChild(self.face)
        obj.addDisplayMode(self.shaded, "Shaded")
        style = coin.SoDrawStyle()
        style.style = coin.SoDrawStyle.LINES
        self.wireframe.addChild(style)
        self.wireframe.addChild(self.scale)
        self.wireframe.addChild(self.color)
        self.wireframe.addChild(self.data)
        self.wireframe.addChild(self.face)
        obj.addDisplayMode(self.wireframe, "Wireframe")
        self.onChanged(obj, "Color")

    def updateData(self, fp, prop):
        "If a property of the handled feature has changed we have the chance to handle this here"
        # fp is the handled feature, prop is the name of the property that has changed
        if prop == "Shape":
            s = fp.getPropertyByName("Shape")
            self.data.point.setNum(6)
            cnt = 0
            for i in s.Vertexes:
                self.data.point.set1Value(cnt, i.X, i.Y, i.Z)
                cnt = cnt + 1

            self.face.coordIndex.set1Value(0, 0)
            self.face.coordIndex.set1Value(1, 1)
            self.face.coordIndex.set1Value(2, 2)
            self.face.coordIndex.set1Value(3, -1)

            self.face.coordIndex.set1Value(4, 1)
            self.face.coordIndex.set1Value(5, 3)
            self.face.coordIndex.set1Value(6, 2)
            self.face.coordIndex.set1Value(7, -1)

            self.face.coordIndex.set1Value(8, 3)
            self.face.coordIndex.set1Value(9, 4)
            self.face.coordIndex.set1Value(10, 2)
            self.face.coordIndex.set1Value(11, -1)

            self.face.coordIndex.set1Value(12, 4)
            self.face.coordIndex.set1Value(13, 0)
            self.face.coordIndex.set1Value(14, 2)
            self.face.coordIndex.set1Value(15, -1)

            self.face.coordIndex.set1Value(16, 1)
            self.face.coordIndex.set1Value(17, 0)
            self.face.coordIndex.set1Value(18, 5)
            self.face.coordIndex.set1Value(19, -1)

            self.face.coordIndex.set1Value(20, 3)
            self.face.coordIndex.set1Value(21, 1)
            self.face.coordIndex.set1Value(22, 5)
            self.face.coordIndex.set1Value(23, -1)

            self.face.coordIndex.set1Value(24, 4)
            self.face.coordIndex.set1Value(25, 3)
            self.face.coordIndex.set1Value(26, 5)
            self.face.coordIndex.set1Value(27, -1)

            self.face.coordIndex.set1Value(28, 0)
            self.face.coordIndex.set1Value(29, 4)
            self.face.coordIndex.set1Value(30, 5)
            self.face.coordIndex.set1Value(31, -1)

    def getDisplayModes(self, obj):
        "Return a list of display modes."
        modes = []
        modes.append("Shaded")
        modes.append("Wireframe")
        return modes

    def getDefaultDisplayMode(self):
        "Return the name of the default display mode. It must be defined in getDisplayModes."
        return "Shaded"

    def setDisplayMode(self, mode):
        return mode

    def onChanged(self, vp, prop):
        "Here we can do something when a single property got changed"
        # FreeCAD.Console.PrintMessage("Change property: " + str(prop) + "\n")
        # if prop == "Color":
        #     c = vp.getPropertyByName("Color")
        #     self.color.rgb.setValue(c[0], c[1], c[2])
        pass

    def getIcon(self):
        return(":/icons/Draft_Draft.svg")

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None


FreeCADGui.addCommand('Fillet2D_2D', Fillet2D())


def getObject():
    try:
        Fillet = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "FilletObj")
        ObjectCreate(Fillet)
        Fillet.ViewObject.Proxy = 0
        processObject(Fillet, Tools2D.ObjectType.Fillet)
    except:
        Tools2D.sayz(traceback.format_exc())

    return Fillet
