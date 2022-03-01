# -*- coding: utf8 -*-
import sys

import FreeCADGui
import Draft
import DraftTools
import FreeCAD
import DraftGui
import FreeCAD
from Modeling.Modeling2D.Tools import Tools2D


class Line2D(DraftTools.Line):
    def finish(self,closed=False,cont=False,type="Line"):
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
                projectName = "Line.LineDlgMain.ShowDialog(line, True)"
                if type == "AreaPolygonal":
                    projectName = "Wire.WireDlgMain.ShowDialog(line)"
                self.commit(DraftGui.translate("draft","Create DWire"),
                            ['points='+pts,
                             'line = Draft.makeWire(points,closed='+str(closed)+',face='+fil+',support='+sup+')',
                             'Draft.autogroup(line)',
                             'Modeling2DCommand.CallBack.CallBackTools.processObject(line, \"'+type+'\")',
                             'Form = Modeling2DCommand.' + projectName,
                             'Form.show()'])

        DraftTools.Creator.finish(self)
        if self.ui:
            if self.ui.continueMode:
                self.Activated()
    pass

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling2D/modeling2DResources/线.svg"
        MenuText = Tools2D.QT_TRANSLATE_NOOP(
            'CreateLine',
            '线')
        ToolTip = Tools2D.QT_TRANSLATE_NOOP(
            'CreateLine',
            'Line')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}
    # def delayCommit(self,closed=False,cont=False):
    #     rot, sup, pts, fil = self.getStrings()
    #     points = pts
    #     line = Draft.makeWire(points,closed=closed,face=fil,support=sup)
    #     Draft.autogroup(line)


FreeCADGui.addCommand('CreateLine_2D', Line2D())
