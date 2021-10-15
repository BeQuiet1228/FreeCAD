import FreeCAD
import FreeCADGui

#fubiao
import PySide
from PySide import QtCore, QtGui
import os
import Units
#end
import ConformalLineNewDialog

import DraftTools
def QT_TRANSLATE_NOOP(ctx,txt): return txt # dummy function for the QT translator
from DraftTools import translate
class CreateConformalLineCommand:
    def Activated(self):
        if FreeCAD.activeDocument()==None:
            FreeCAD.newDocument()
        import CreateConformalLine
        obj = CreateConformalLine.createConformalLine()
        Form = ConformalLineNewDialog.showConformalLineDialog(obj)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling3D/Modeling3DResources/3D_Line_Conformal.svg"
        MenuText = QT_TRANSLATE_NOOP(
            'CreateConformalLine',
            'Create ConformalLine')
        ToolTip = QT_TRANSLATE_NOOP(
            'CreateConformalLine',
            'Create a new ConformalLine instance')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

FreeCADGui.addCommand('CreateConformalLine',CreateConformalLineCommand())