import FreeCAD
import FreeCADGui

#fubiao
import PySide
from PySide import QtCore, QtGui
import os
import Units
import ParallelepipedalNewDialog
#end
import DraftTools
def QT_TRANSLATE_NOOP(ctx,txt): return txt # dummy function for the QT translator
from DraftTools import translate

class CreateParallelepipedalCommand:
    def Activated(self):
        if FreeCAD.activeDocument()==None:
            FreeCAD.newDocument()
        import CreateParallelepipedal
        obj = CreateParallelepipedal.createParallelepipedal()
        Form = ParallelepipedalNewDialog.showParallelepipedalDialog(obj)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling3D/Modeling3DResources/3D_Vol_Parallelepipedal.svg"
        MenuText = QT_TRANSLATE_NOOP(
            'CreateParallelepipedal',
            'Create Parallelepipedal')
        ToolTip = QT_TRANSLATE_NOOP(
            'CreateParallelepipedal',
            'Create a new Parallelepipedal instance')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

FreeCADGui.addCommand('CreateParallelepipedal',CreateParallelepipedalCommand())