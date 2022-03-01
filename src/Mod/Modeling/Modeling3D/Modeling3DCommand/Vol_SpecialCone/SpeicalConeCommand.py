import FreeCAD
import FreeCADGui

#fubiao
import PySide
from PySide import QtCore, QtGui
import os
import Units
import SpecicalConeNewDialog
#end
import DraftTools
def QT_TRANSLATE_NOOP(ctx,txt): return txt # dummy function for the QT translator
from DraftTools import translate
#Create a SpecialCone
class CreateSpecialCone:
    def Activated(self):
        if FreeCAD.activeDocument() == None:
            FreeCAD.newDocument()
        import CreateSpecialCone
        obj = CreateSpecialCone.createSpecialCone()
        Form = SpecicalConeNewDialog.showSpecialConeDialog(obj)
        Form.show()
        Form.exec_() 

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling3D/Modeling3DResources/3D_Vol_SpecialCone.svg"
        MenuText = QT_TRANSLATE_NOOP(
            'CreateSpecialCone',
            'Create SpecialCone')
        ToolTip = QT_TRANSLATE_NOOP(
            'CreateSpecialCone',
            'Create a new SpecialCone instance')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False
FreeCADGui.addCommand('CreateSpecialCone',CreateSpecialCone())