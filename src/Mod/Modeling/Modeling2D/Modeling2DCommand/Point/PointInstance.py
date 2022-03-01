# -*- coding: utf8 -*-
import sys
import FreeCAD
from Modeling.Modeling2D.Tools import Tools2D
import FreeCADGui
import Draft
import DraftTools
import DraftGui
from pivy import coin
class Point2D(DraftTools.Point):
    def click(self,event_cb=None):
        if event_cb:
            event = event_cb.getEvent()
            if event.getState() != coin.SoMouseButtonEvent.DOWN:
                return
        if self.point:
            self.stack.append(self.point)
            if len(self.stack) == 1:
                self.view.removeEventCallbackPivy(coin.SoMouseButtonEvent.getClassTypeId(),self.callbackClick)
                self.view.removeEventCallbackPivy(coin.SoLocation2Event.getClassTypeId(),self.callbackMove)
                commitlist = []
                if Draft.getParam("UsePartPrimitives",False):
                    # using
                    commitlist.append((DraftGui.translate("draft","Create Point"),
                                        ['point = FreeCAD.ActiveDocument.addObject("Part::Vertex","Point")',
                                         'point.X = '+str(self.stack[0][0]),
                                         'point.Y = '+str(self.stack[0][1]),
                                         'point.Z = '+str(self.stack[0][2]),
                                         'Draft.autogroup(point)']))
                else:
                    # building command string
                    FreeCADGui.addModule("Draft")
                    FreeCADGui.addModule("Modeling")
                    FreeCADGui.doCommand("from Modeling.Modeling2D import Modeling2DCommand")
                    commitlist.append((DraftGui.translate("draft","Create Point"),
                                        ['point = Draft.makePoint('+str(self.stack[0][0])+','+str(self.stack[0][1])+','+str(self.stack[0][2])+',color=None,name = "PointObj"'+')',
                                         'Draft.autogroup(point)',
                                         'Modeling2DCommand.CallBack.CallBackTools.processObject(point, \'Point\')',
                                         'Form = Modeling2DCommand.Point.PointDlgMain.ShowDialog(point, True)',
                                         'Form.show()'
                                         ]))
                DraftGui.todo.delayCommit(commitlist)
                FreeCADGui.Snapper.off()
            self.finish()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling2D/modeling2DResources/点.svg"
        MenuText = Tools2D.QT_TRANSLATE_NOOP(
            'CreatePoint',
            '点')
        ToolTip = Tools2D.QT_TRANSLATE_NOOP(
            'CreatePoint',
            'Point')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreatePoint_2D', Point2D())
