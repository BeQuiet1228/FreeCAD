import FreeCAD
import FreeCADGui

#fubiao
import PySide
from PySide import QtCore, QtGui
import os
import Units
#end

class CreateCylinderCommand:
    def Activated(self):
        if FreeCAD.activeDocument()==None:
            FreeCAD.newDocument()
        import CreateCylinder
        CreateCylinder.createCylinder()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling3D/Modeling3DResources/3DCylinder.svg"
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'Cylinder',
            'Create a new Cylinder')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'Cylinder',
            'Create a new Cylinder instance on top of the hull geometry')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

FreeCADGui.addCommand('CreateCylinder',CreateCylinderCommand())