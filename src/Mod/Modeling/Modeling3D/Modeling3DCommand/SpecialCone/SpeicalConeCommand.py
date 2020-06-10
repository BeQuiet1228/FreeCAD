import FreeCAD
import FreeCADGui

#fubiao
import PySide
from PySide import QtCore, QtGui
import os
import Units
#end
#Create a SpecialCone
class CreateSpecialCone:
    def Activated(self):
        if FreeCAD.activeDocument() == None:
            FreeCAD.newDocument()
        import CreateSpecialCone
        CreateSpecialCone.createSpecialCone()  

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling3D/Modeling3DResources/3DSpecialCone.svg"
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'SpecialCone',
            'Create a new SpecialCone')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'SpecialCone',
            'Create a new SpecialCone instance on top of the hull geometry')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

FreeCADGui.addCommand('CreateSpecialCone',CreateSpecialCone())