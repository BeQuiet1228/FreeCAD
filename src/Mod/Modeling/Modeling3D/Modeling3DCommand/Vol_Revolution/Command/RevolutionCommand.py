import FreeCAD
import FreeCADGui

#fubiao
import PySide
from PySide import QtCore, QtGui
import os
import Units
#end
import DraftTools
def QT_TRANSLATE_NOOP(ctx,txt): return txt # dummy function for the QT translator
from DraftTools import translate
# import ConformalAreaNewDialog
class CreateRevolutionCommand:
    def Activated(self):
        if FreeCAD.activeDocument()==None:
            FreeCAD.newDocument()
        import RevolutionDlgMain
        dlg=RevolutionDlgMain.VolRevolotion()
        dlg.show()
        dlg.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling3D/Modeling3DResources/3DRevolution.svg"
        MenuText = QT_TRANSLATE_NOOP(
            'CreateRevolutionCommand',
            'Create Revolution')
        ToolTip = QT_TRANSLATE_NOOP(
            'CreateRevolutionCommand',
            'Create a new Revolution instance')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

    def IsActive(self):
        if not FreeCAD.ActiveDocument:
            return False
        return True

FreeCADGui.addCommand('CreateRevolutionCommand',CreateRevolutionCommand())