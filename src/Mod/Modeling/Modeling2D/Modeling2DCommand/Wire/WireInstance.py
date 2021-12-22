# -*- coding: utf8 -*-
import sys

import FreeCADGui


import Draft
import DraftTools
import FreeCAD
import DraftGui
from DraftGui import QtCore
from Modeling.Modeling2D.Modeling2DCommand.Line.LineInstance import Line2D
from Modeling.Modeling2D.Tools import Tools2D, ToolsForDisplay
from Modeling.Modeling2D.Tools.Tools2D import sayz

class Wire2D(Line2D):
    def __init__(self):
        Line2D.__init__(self, wiremode=True)

    def Activated(self):

        # allow to convert several Draft Lines to a Wire
        if len(FreeCADGui.Selection.getSelection()) > 1:
            edges = []
            for o in FreeCADGui.Selection.getSelection():
                if Draft.getType(o) != "Wire":
                    edges = []
                    break
                edges.extend(o.Shape.Edges)
            if edges:
                try:
                    import Part
                    w = Part.Wire(edges)
                except:
                    sayz(DraftGui.translate("draft", "Unable to create a Wire from selected objects\n"), mode="error")
                else:
                    pts = ",".join([str(v.Point) for v in w.Vertexes])
                    pts = pts.replace("Vector", "FreeCAD.Vector")
                    rems = ["FreeCAD.ActiveDocument.removeObject(\"" + o.Name + "\")" for o in
                            FreeCADGui.Selection.getSelection()]
                    FreeCADGui.addModule("Draft")
                    Draft.todo.delayCommit([(DraftGui.translate("draft", "Convert to Wire"),
                                       ['wire = Draft.makeWire([' + pts + '])'] + rems + ['Draft.autogroup(wire)'])])
                    return

        Line2D.Activated(self, name=DraftGui.translate("draft", "DWire"))

    # def GetResources(self):
    #     return {'Pixmap'  : 'Draft_Wire',
    #             'Accel' : "W, I",
    #             'MenuText': QtCore.QT_TRANSLATE_NOOP("Draft_Wire", "DWire"),
    #             'ToolTip': QtCore.QT_TRANSLATE_NOOP("Draft_Wire", "Creates a multiple-point DraftWire (DWire). CTRL to snap, SHIFT to constrain")}

    def action(self,arg):
        "scene event handler"
        if arg["Type"] == "SoKeyboardEvent":
            # key detection
            if arg["Key"] == "ESCAPE":
                self.finish()
        elif arg["Type"] == "SoLocation2Event":
            # mouse movement detection
            self.point,ctrlPoint,info = DraftTools.getPoint(self,arg)
            DraftTools.redraw3DView()
        elif arg["Type"] == "SoMouseButtonEvent":
            # mouse button detection
            if (arg["State"] == "DOWN") and (arg["Button"] == "BUTTON1"):
                if arg["Position"] == self.pos:
                    Tools2D.sayz("检测到多边形首尾两点重合，结束草图建模")
                    Tools2D.sayz(str(arg["Position"]))
                    Tools2D.sayz(str(self.pos))
                    self.finish(False,cont=True)
                else:
                    if (not self.node) and (not self.support):
                        DraftTools.getSupport(arg)
                        self.point,ctrlPoint,info = DraftTools.getPoint(self,arg)
                    if self.point:
                        self.ui.redraw()
                        self.pos = arg["Position"]
                        self.node.append(self.point)
                        self.drawSegment(self.point)
                        if (not self.isWire and len(self.node) == 2):
                            self.finish(False,cont=True)
                        if (len(self.node) > 2):
                            # 此处保留原有if语句，如果出现问题则替换为原有if
                            # if ((self.point-self.node[0]).Length < Draft.tolerance()):
                            if ((self.point - self.node[0]).Length < 0.0001):
                                self.undolast()
                                self.finish(True,cont=True)
                                DraftTools.msg(DraftTools.translate("draft", "DWire has been closed\n"))

    def finish(self, closed=False, cont=False):
        "terminates the operation and closes the poly if asked"
        if self.obj:
            # remove temporary object, if any
            try:
                old = self.obj.Name
            except ReferenceError:
                # object already deleted, for some reason
                pass
            else:
                DraftGui.todo.delay(self.doc.removeObject, old)
        self.obj = None
        if self.oldWP:
            FreeCAD.DraftWorkingPlane = self.oldWP
            if hasattr(FreeCADGui, "Snapper"):
                FreeCADGui.Snapper.setGrid()
                FreeCADGui.Snapper.restack()
        self.oldWP = None
        if (len(self.node) > 1):
            if (len(self.node) == 2) and Draft.getParam("UsePartPrimitives", False):
                # use Part primitive
                p1 = self.node[0]
                p2 = self.node[-1]
                self.commit(DraftGui.translate("draft", "Create Line"),
                            ['line = FreeCAD.ActiveDocument.addObject("Part::Line","Line")',
                             'line.X1 = ' + str(p1.x),
                             'line.Y1 = ' + str(p1.y),
                             'line.Z1 = ' + str(p1.z),
                             'line.X2 = ' + str(p2.x),
                             'line.Y2 = ' + str(p2.y),
                             'line.Z2 = ' + str(p2.z),
                             'Draft.autogroup(line)'])
            else:
                # building command string
                rot, sup, pts, fil = self.getStrings()
                FreeCADGui.addModule("Draft")
                FreeCADGui.addModule("Modeling")
                FreeCADGui.doCommand("from Modeling.Modeling2D import Modeling2DCommand")
                projectName = "Wire.WireDlgMain.ShowDialog(line, True)"
                self.commit(DraftGui.translate("draft", "Create DWire"),
                            ['points=' + pts,
                             'line = Draft.makeWire(points,closed=' + str(
                                 True) + ',face=' + fil + ',support=' + sup + ')',
                             'Draft.autogroup(line)',
                             'Modeling2DCommand.CallBack.CallBackTools.processObject(line, \"AreaPolygonal\")',
                             'Form = Modeling2DCommand.' + projectName,
                             'Form.show()'])

        DraftTools.Creator.finish(self)
        if self.ui:
            if self.ui.continueMode:
                self.Activated()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling2D/modeling2DResources/2d多边形面.svg"
        MenuText = Tools2D.QT_TRANSLATE_NOOP(
            'CreatePoint',
            '多边形面')
        ToolTip = Tools2D.QT_TRANSLATE_NOOP(
            'CreatePoint',
            '多边形面')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreatePolygonal_2D', Wire2D())


# 'Modeling2DCommand.Wire.WireInstance.MyWire(line)',
class MyWire(Draft._Wire):
    def __init__(self, obj):
        Draft._Wire.__init__(self, obj)

    def execute(self, obj):
        import DraftVecUtils
        import Part, DraftGeomUtils
        plm = obj.Placement
        if obj.Base and (not obj.Tool):
            if obj.Base.isDerivedFrom("Sketcher::SketchObject"):
                shape = obj.Base.Shape.copy()
                if obj.Base.Shape.isClosed():
                    if hasattr(obj, "MakeFace"):
                        if obj.MakeFace:
                            shape = Part.Face(shape)
                    else:
                        shape = Part.Face(shape)
                obj.Shape = shape
        elif obj.Base and obj.Tool:
            if obj.Base.isDerivedFrom("Part::Feature") and obj.Tool.isDerivedFrom("Part::Feature"):
                if (not obj.Base.Shape.isNull()) and (not obj.Tool.Shape.isNull()):
                    sh1 = obj.Base.Shape.copy()
                    sh2 = obj.Tool.Shape.copy()
                    shape = sh1.fuse(sh2)
                    if DraftGeomUtils.isCoplanar(shape.Faces):
                        shape = DraftGeomUtils.concatenate(shape)
                        obj.Shape = shape
                        p = []
                        for v in shape.Vertexes: p.append(v.Point)
                        if obj.Points != p: obj.Points = p
        elif obj.Points:
            if obj.Points[0] == obj.Points[-1]:
                if not obj.Closed: obj.Closed = True
                obj.Points.pop()
            if obj.Closed and (len(obj.Points) > 2):
                pts = obj.Points
                if hasattr(obj, "Subdivisions"):
                    if obj.Subdivisions > 0:
                        npts = []
                        for i in range(len(pts)):
                            p1 = pts[i]
                            npts.append(pts[i])
                            if i == len(pts) - 1:
                                p2 = pts[0]
                            else:
                                p2 = pts[i + 1]
                            v = p2.sub(p1)
                            v = DraftVecUtils.scaleTo(v, v.Length / (obj.Subdivisions + 1))
                            for j in range(obj.Subdivisions):
                                npts.append(p1.add(FreeCAD.Vector(v).multiply(j + 1)))
                        pts = npts
                shape = Part.makePolygon(pts + [pts[0]])
                if "ChamferSize" in obj.PropertiesList:
                    if obj.ChamferSize.Value != 0:
                        w = DraftGeomUtils.filletWire(shape, obj.ChamferSize.Value, chamfer=True)
                        if w:
                            shape = w
                if "FilletRadius" in obj.PropertiesList:
                    if obj.FilletRadius.Value != 0:
                        w = DraftGeomUtils.filletWire(shape, obj.FilletRadius.Value)
                        if w:
                            shape = w
                try:
                    if hasattr(obj, "MakeFace"):
                        if obj.MakeFace:
                            shape = Part.Face(shape)
                    else:
                        shape = Part.Face(shape)
                except Part.OCCError:
                    pass
            else:
                edges = []
                pts = obj.Points[1:]
                lp = obj.Points[0]
                for p in pts:
                    if not DraftVecUtils.equals(lp, p):
                        if hasattr(obj, "Subdivisions"):
                            if obj.Subdivisions > 0:
                                npts = []
                                v = p.sub(lp)
                                v = DraftVecUtils.scaleTo(v, v.Length / (obj.Subdivisions + 1))
                                edges.append(Part.LineSegment(lp, lp.add(v)).toShape())
                                lv = lp.add(v)
                                for j in range(obj.Subdivisions):
                                    edges.append(Part.LineSegment(lv, lv.add(v)).toShape())
                                    lv = lv.add(v)
                            else:
                                edges.append(Part.LineSegment(lp, p).toShape())
                        else:
                            edges.append(Part.LineSegment(lp, p).toShape())
                        lp = p
                try:
                    shape = Part.Wire(edges)
                except Part.OCCError:
                    print("Error wiring edges")
                    shape = None
                if "ChamferSize" in obj.PropertiesList:
                    if obj.ChamferSize.Value != 0:
                        w = DraftGeomUtils.filletWire(shape, obj.ChamferSize.Value, chamfer=True)
                        if w:
                            shape = w
                if "FilletRadius" in obj.PropertiesList:
                    if obj.FilletRadius.Value != 0:
                        w = DraftGeomUtils.filletWire(shape, obj.FilletRadius.Value)
                        if w:
                            shape = w
            if shape:
                obj.Shape = shape
                if hasattr(obj, "Length"):
                    obj.Length = shape.Length
        obj.Placement = plm
        obj.positionBySupport()
        self.onChanged(obj, "Placement")
        ToolsForDisplay.setColors(obj)
