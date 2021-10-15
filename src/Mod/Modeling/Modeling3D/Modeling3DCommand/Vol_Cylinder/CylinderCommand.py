import FreeCAD
import FreeCADGui

#fubiao
import PySide
from PySide import QtCore, QtGui
import os
import Units
import CylinderNewDialog
#end
import DraftTools
def QT_TRANSLATE_NOOP(ctx,txt): return txt # dummy function for the QT translator
from DraftTools import translate

class CreateCylinderCommand:
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        if FreeCAD.activeDocument()==None:
            FreeCAD.newDocument()
        import CreateCylinder
        obj=CreateCylinder.createCylinder()
        Form=CylinderNewDialog.showCylinderDialog(obj)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling3D/Modeling3DResources/3D_Vol_Cylinder.svg"
        MenuText = QT_TRANSLATE_NOOP(
            'CreateCylinder',
            'Create Cylinder')
        ToolTip = QT_TRANSLATE_NOOP(
            'CreateCylinder',
            'Create a new Cylinder instance')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

FreeCADGui.addCommand('CreateCylinder',CreateCylinderCommand())