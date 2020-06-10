import FreeCAD
import FreeCADGui

#fubiao
import PySide
from PySide import QtCore, QtGui
import os
import Units
#end

class CreatePyramidCommand:
    def Activated(self):
        if FreeCAD.activeDocument()==None:
            FreeCAD.newDocument()
        import CreatePyramid
        CreatePyramid.createPyramid()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling3D/Modeling3DResources/3DPyramid.svg"
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'Pyramid',
            'Create a new Pyramid')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'Pyramid',
            'Create a new Pyramid instance on top of the hull geometry')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

FreeCADGui.addCommand('CreatePyramid',CreatePyramidCommand())