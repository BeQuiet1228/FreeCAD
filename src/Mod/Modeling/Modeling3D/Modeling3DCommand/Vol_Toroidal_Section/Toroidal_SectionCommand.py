import FreeCAD
import FreeCADGui

#fubiao
import PySide
from PySide import QtCore, QtGui
import os
import Units
import ToroidalSectionNewDialog
#end
import DraftTools
def QT_TRANSLATE_NOOP(ctx,txt): return txt # dummy function for the QT translator
from DraftTools import translate
#Create a Toroidal_Section
class CreateToroidal_Section:
    def Activated(self):
        if FreeCAD.activeDocument() == None:
            FreeCAD.newDocument()
        import CreateToroidal_Section
        obj = CreateToroidal_Section.createToroidal_Section()
        Form = ToroidalSectionNewDialog.showToroidalSectionDialog(obj)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling3D/Modeling3DResources/3D_Vol_Toroidal_Section.svg"
        MenuText = QT_TRANSLATE_NOOP(
            'CreateToroidal_Section',
            'Create Toroidal_Section')
        ToolTip = QT_TRANSLATE_NOOP(
            'CreateToroidal_Section',
            'Create a new Toroidal_Section instance')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

FreeCADGui.addCommand('CreateToroidal_Section',CreateToroidal_Section())