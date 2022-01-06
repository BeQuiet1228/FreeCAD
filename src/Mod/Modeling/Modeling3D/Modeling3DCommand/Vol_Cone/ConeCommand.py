import FreeCAD
import FreeCADGui

#fubiao
import PySide
from PySide import QtCore, QtGui
import os
import Units
#end

class CreateConeCommand:
    def Activated(self):
        if FreeCAD.activeDocument()==None:
            FreeCAD.newDocument()
        import CreateCone
        CreateCone.createCone()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling3D/Modeling3DResources/3DCone.svg"
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'Cone',
            'Create Cone')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'Cone',
            'Create a new Cone instance on top of the hull geometry')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

FreeCADGui.addCommand('CreateCone',CreateConeCommand())