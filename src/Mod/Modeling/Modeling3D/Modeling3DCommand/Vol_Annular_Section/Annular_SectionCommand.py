import FreeCAD
import FreeCADGui

#fubiao
import PySide
from PySide import QtCore, QtGui
import os
import Units
import AnnularSectionNewDialog
#end
import DraftTools
def QT_TRANSLATE_NOOP(ctx,txt): return txt # dummy function for the QT translator
from DraftTools import translate
#Create a Annular_Section
class CreateAnnular_Section:
    def Activated(self):
        if FreeCAD.activeDocument() == None:
            FreeCAD.newDocument()
        import CreateAnnular_Section
        obj = CreateAnnular_Section.createAnnular_Section()
        Form = AnnularSectionNewDialog.showAnnularSectionDialog(obj)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling3D/Modeling3DResources/3D_Vol_Annular_Section.svg"
        MenuText = QT_TRANSLATE_NOOP(
            'CreateAnnular_Section',
            'Create Annular_Section')
        ToolTip = QT_TRANSLATE_NOOP(
            'CreateAnnular_Section',
            'Create a new Annular_Section instance')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

FreeCADGui.addCommand('CreateAnnular_Section',CreateAnnular_Section())