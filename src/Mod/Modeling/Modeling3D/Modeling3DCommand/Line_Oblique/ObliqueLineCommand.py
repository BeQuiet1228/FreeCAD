import FreeCAD
import FreeCADGui

#fubiao
import PySide
from PySide import QtCore, QtGui
import os
import Units
#end
import ObliqueLineNewDialog

import DraftTools
def QT_TRANSLATE_NOOP(ctx,txt): return txt # dummy function for the QT translator
from DraftTools import translate

class CreateObliqueLineCommand:
    def Activated(self):
        if FreeCAD.activeDocument()==None:
            FreeCAD.newDocument()
        import CreateObliqueLine
        obj = CreateObliqueLine.createObliqueLine()
        Form = ObliqueLineNewDialog.showObliqueLineDialog(obj)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling3D/Modeling3DResources/3D_LineOblique.svg"
        MenuText = QT_TRANSLATE_NOOP(
            'CreateObliqueLine',
            'Create ObliqueLine')
        ToolTip = QT_TRANSLATE_NOOP(
            'CreateObliqueLine',
            'Create a new ObliqueLine instance')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

FreeCADGui.addCommand('CreateObliqueLine',CreateObliqueLineCommand())