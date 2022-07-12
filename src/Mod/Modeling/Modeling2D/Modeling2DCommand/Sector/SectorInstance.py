#-*- coding: utf-8 -*-
import FreeCAD, Part, FreeCADGui
from math import pi,radians
import pivy
from pivy import coin
from Modeling.Modeling2D.Modeling2DCommand.CallBack.CallBackTools import processObject
from Modeling.Modeling2D.Modeling2DCommand.Sector import SectorDlgMain
from Modeling.Modeling2D.Tools.Tools2D import ObjectType
from Modeling.Modeling2D.Tools import Tools2D


class Sector2D():
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False
    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling2D/modeling2DResources/2d扇形.svg"
        MenuText = Tools2D.QT_TRANSLATE_NOOP(
            'CreateSector',
            '四分圆面')
        ToolTip = Tools2D.QT_TRANSLATE_NOOP(
            'CreateSector',
            'Sector')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

    def Activated(self):
        self.finish()

    def finish(self):
        # 打开对话框
        Sector = FreeCAD.ActiveDocument.addObject("Part::Part2DObjectPython", "Sector")
        ObjectCreate(Sector)
        ViewProvider(Sector.ViewObject)
        processObject(Sector, Tools2D.ObjectType.Sector)
        Sector.recompute()
        Form = SectorDlgMain.ShowDialog(Sector, True)
        Form.exec_()
        pass


class ObjectCreate:
    def __init__(self, obj):
        "Add some custom properties to our box feature"
        obj.addProperty("App::PropertyLength", "Radius", "sector1/4", "Radius").Radius = 0.1
        obj.addProperty("App::PropertyDistance", "X", "sector1/4", " centre point X").X = 0
        obj.addProperty("App::PropertyDistance", "Y", "sector1/4", " centre point Y").Y = 0
        obj.addProperty("App::PropertyEnumeration", "Quadrant", "sector1/4",
                        "Quadrant").Quadrant = ["第一象限", "第二象限", "第三象限", "第四象限"]
        obj.addProperty("Part::PropertyPartShape", "Shape", "sector1/4", "Shape of the octahedron")
        obj.Proxy = self

    def execute(self, fp):
        Tools2D.sayz("execute被触发")
        circlePoint = FreeCAD.Vector(fp.X.Value, fp.Y.Value, 0)
        circle = Part.Circle(circlePoint, FreeCAD.Vector(0, 0, 1), fp.Radius)
        startAngle = 0
        endAngle = 90
        if fp.Quadrant == "第二象限":
            startAngle += 90
            endAngle += 90
        elif fp.Quadrant == "第三象限":
            startAngle += 180
            endAngle += 180
        elif fp.Quadrant == "第四象限":
            startAngle += 270
            endAngle += 270
        arc = Part.Arc(circle, radians(startAngle), radians(endAngle))
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
        fp.Shape = face
        # helper mehod to create the faces

        from Modeling.Modeling2D.Tools import ToolsForDisplay
        ToolsForDisplay.setColors(fp)

    def make_face(self, v1, v2, v3):
        wire = Part.makePolygon([v1, v2, v3, v1])
        face = Part.Face(wire)
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


FreeCADGui.addCommand('CreateSector_2D', Sector2D())