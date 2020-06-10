import FreeCAD
import FreeCADGui

#fubiao
import PySide
from PySide import QtCore, QtGui
import os
import Units
#end

class CreateOrthographicBodyCommand:
    def Activated(self):
        if FreeCAD.activeDocument()==None:
            FreeCAD.newDocument()
        import CreateOrthographicBody
        CreateOrthographicBody.createOrthographicBody()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling3D/Modeling3DResources/3DOrthographicBody.svg"
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'OrthographicBody',
            'Create a new OrthographicBody')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'OrthographicBody',
            'Create a new OrthographicBody instance on top of the hull geometry')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

FreeCADGui.addCommand('CreateOrthographicBody',CreateOrthographicBodyCommand())