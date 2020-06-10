import FreeCAD
import FreeCADGui
#fubiao
import PySide
from PySide import QtCore, QtGui
import os
import Units
#end
#Create a Torus
class CreateTorusCommand:
    def Activated(self):
        if FreeCAD.activeDocument() == None:
            FreeCAD.newDocument()
        import CreateTorus
        CreateTorus.createTorus()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling3D/Modeling3DResources/3DTorus.svg"
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'Torus',
            'Create a new Torus')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'Torus',
            'Create a new Torus instance on top of the hull geometry')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

FreeCADGui.addCommand('CreateTorus',CreateTorusCommand())
#end