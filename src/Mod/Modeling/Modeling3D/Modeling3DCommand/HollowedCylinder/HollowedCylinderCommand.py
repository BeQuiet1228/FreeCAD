import FreeCAD
import FreeCADGui

#fubiao
import PySide
from PySide import QtCore, QtGui
import os
import Units
#end
#Create a HollowedCylinder
class CreateHollowedCylinderCommand:
    def Activated(self):
        if FreeCAD.activeDocument() == None:
            FreeCAD.newDocument()
        import CreateHollowedCylinder
        CreateHollowedCylinder.createHollowedCylinder() 

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling3D/Modeling3DResources/3DHollowedCylinder.svg"
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'HollowedCylinder',
            'Create a new HollowedCylinder')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'HollowedCylinder',
            'Create a new HollowedCylinder instance on top of the hull geometry')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

FreeCADGui.addCommand('CreateHollowedCylinder',CreateHollowedCylinderCommand())