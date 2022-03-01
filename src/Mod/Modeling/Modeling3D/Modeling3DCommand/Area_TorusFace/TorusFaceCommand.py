import FreeCAD
import FreeCADGui

#fubiao
import PySide
from PySide import QtCore, QtGui
import os
import Units
#end
#Create a TorusFace
class CreateTorusFaceCommand:
    def Activated(self):
        if FreeCAD.activeDocument() == None:
            FreeCAD.newDocument()
        import CreateTorusFace
        CreateTorusFace.createTorusFace()  

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling3D/Modeling3DResources/3DTorusFace.svg"
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'TorusFace',
            'Create TorusFace')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'TorusFace',
            'Create a new TorusFace instance on top of the hull geometry')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

FreeCADGui.addCommand('CreateTorusFace',CreateTorusFaceCommand())
#end