import FreeCAD
import FreeCADGui

#fubiao
import PySide
from PySide import QtCore, QtGui
import os
import Units
#end
#Create a Wedge
class CreateWedgeCommand:
    def Activated(self):
        if FreeCAD.activeDocument() == None:
            FreeCAD.newDocument()
        import CreateWedge
        CreateWedge.createWedge()  

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling3D/Modeling3DResources/3DWedge.svg"
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'Wedge',
            'Create a new Wedge')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'Wedge',
            'Create a new Wedge instance on top of the hull geometry')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

FreeCADGui.addCommand('CreateWedge',CreateWedgeCommand())
#end