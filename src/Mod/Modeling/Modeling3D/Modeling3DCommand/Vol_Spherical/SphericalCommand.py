import FreeCAD
import FreeCADGui

#fubiao
import PySide
from PySide import QtCore, QtGui
import os
import Units
import SphericalNewDialog
#end
import DraftTools
def QT_TRANSLATE_NOOP(ctx,txt): return txt # dummy function for the QT translator
from DraftTools import translate
#Create a Spherical
class CreateSpherical:
    def Activated(self):
        if FreeCAD.activeDocument() == None:
            FreeCAD.newDocument()
        import CreateSpherical
        obj = CreateSpherical.createSpherical()
        Form = SphericalNewDialog.showSphericalDialog(obj)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling3D/Modeling3DResources/3D_Vol_Spherical.svg"
        MenuText = QT_TRANSLATE_NOOP(
            'CreateSpherical',
            'Create Spherical')
        ToolTip = QT_TRANSLATE_NOOP(
            'CreateSpherical',
            'Create a new Spherical instance')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

FreeCADGui.addCommand('CreateSpherical',CreateSpherical())