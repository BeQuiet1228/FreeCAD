import FreeCAD
import FreeCADGui

#fubiao
import PySide
from PySide import QtCore, QtGui
import os
import Units
import PyramidNewDialog
#end
import DraftTools
def QT_TRANSLATE_NOOP(ctx,txt): return txt # dummy function for the QT translator
from DraftTools import translate

class CreatePyramidCommand:
    def Activated(self):
        if FreeCAD.activeDocument()==None:
            FreeCAD.newDocument()
        import CreatePyramid
        obj = CreatePyramid.createPyramid()
        From = PyramidNewDialog.showPyramidDialog(obj)
        From.show()
        From.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling3D/Modeling3DResources/3D_Vol_Pyramid.svg"
        MenuText = QT_TRANSLATE_NOOP(
            'CreatePyramid',
            'Create Pyramid')
        ToolTip = QT_TRANSLATE_NOOP(
            'CreatePyramid',
            'Create a new Pyramid instance')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

FreeCADGui.addCommand('CreatePyramid',CreatePyramidCommand())