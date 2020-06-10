import FreeCAD
import FreeCADGui

#fubiao
import PySide
from PySide import QtCore, QtGui
import os
import Units
#end
#Create a Sphere
class CreateSphere:
    def Activated(self):
        if FreeCAD.activeDocument() == None:
            FreeCAD.newDocument()
        import CreateSphere
        CreateSphere.createSphere()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling3D/Modeling3DResources/3DSphere.svg"
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'Sphere',
            'Create a new Sphere')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'Sphere',
            'Create a new Sphere instance on top of the hull geometry')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

FreeCADGui.addCommand('CreateSphere',CreateSphere())