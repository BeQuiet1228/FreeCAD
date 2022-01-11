# -*- coding: utf-8 -*-
import traceback

from DraftTools import Creator, translate, msg, sys, getPoint, redraw3DView
from PySide import QtCore
import FreeCADGui
from FreeCAD import Vector
import FreeCAD
from Modeling.Modeling2D.Tools import Tools2D


import DraftVecUtils


class Text(Creator):
    """This class creates an annotation feature."""

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling2D/modeling2DResources/文字.svg"
        MenuText = Tools2D.QT_TRANSLATE_NOOP(
            'CreateText',
            '注释')
        ToolTip = Tools2D.QT_TRANSLATE_NOOP(
            'CreateText',
            'Text')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

    def Activated(self):
        name = translate("draft", "Text")
        Creator.Activated(self, name)
        if self.ui:
            self.dialog = None
            self.text = ''
            self.ui.sourceCmd = self
            self.ui.pointUi(name)
            self.call = self.view.addEventCallback("SoEvent", self.action)
            self.active = True
            self.ui.xValue.setFocus()
            self.ui.xValue.selectAll()
            msg(translate("draft", "Pick location point:\n"))
            FreeCADGui.draftToolBar.show()
            # FreeCAD.Console.PrintError("\nactive执行完毕\n")

    def finish(self, closed=False, cont=False):
        """terminates the operation"""
        Creator.finish(self)
        if self.ui:
            del self.dialog
            if self.ui.continueMode:
                self.Activated()

    def createObject(self):
        """creates an object in the current doc"""
        # tx = '['
        # for l in self.text:
        #     if len(tx) > 1:
        #         tx += ','
        #     if sys.version_info.major < 3:
        #         l = unicode(l)
        #     tx += '"'+str(l.encode("utf8"))+'"' #Python3 no more unicode
        # tx += ']'
        tx = '[\'\']'
        FreeCADGui.addModule("Draft")
        FreeCADGui.doCommand("from Modeling.Modeling2D import Modeling2DCommand")
        self.commit(translate("draft", "Create Text"),
                    ['text = Draft.makeText('+tx+',point='+DraftVecUtils.toString(self.node[0])+')',
                     'text.ViewObject.setEditorMode("DisplayMode",2)',
                     'Draft.autogroup(text)',
                     'Form = Modeling2DCommand.Text.TextDlgMain.ShowDialog(text, True)',
                     'Form.show()',
                     ])

        self.finish(cont=True)

    def action(self, arg):
        """scene event handler"""
        if arg["Type"] == "SoKeyboardEvent":
            if arg["Key"] == "ESCAPE":
                self.finish()
        elif arg["Type"] == "SoLocation2Event":   # mouse movement detection
            if self.active:
                self.point, ctrlPoint, info = getPoint(self, arg)
            redraw3DView()
        elif arg["Type"] == "SoMouseButtonEvent":
            if (arg["State"] == "DOWN") and (arg["Button"] == "BUTTON1"):
                if self.point:
                    self.active = False
                    FreeCADGui.Snapper.off()
                    self.node.append(self.point)
                    # self.ui.textUi()
                    self.ui.hideXYZ()
                    # self.ui.textValue.setFocus()
                    self.ui.offUi()
                    self.createObject()
                    FreeCAD.Console.PrintError("\n设置焦点\n")

    def numericInput(self, numx, numy, numz):
        """this function gets called by the toolbar when valid
        x, y, and z have been entered there"""
        self.point = Vector(numx, numy, numz)
        self.node.append(self.point)
        self.ui.textUi()
        self.ui.textValue.setFocus()


FreeCADGui.addCommand('CreateText', Text())
