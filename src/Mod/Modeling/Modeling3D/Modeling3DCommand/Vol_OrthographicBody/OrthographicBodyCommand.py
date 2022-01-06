import FreeCAD
import FreeCADGui

#fubiao
import PySide
from PySide import QtCore, QtGui
import os
import Units
#end
import DraftTools
def QT_TRANSLATE_NOOP(ctx,txt): return txt # dummy function for the QT translator
from DraftTools import translate

class CreateOrthographicBodyCommand:
    def Activated(self):
        if FreeCAD.activeDocument()==None:
            FreeCAD.newDocument()
        import CreateOrthographicBody
        CreateOrthographicBody.createOrthographicBody()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling3D/Modeling3DResources/3DOrthographicBody.svg"
        MenuText = QT_TRANSLATE_NOOP(
            'CreateOrthographicBody',
            'Create OrthographicBody')
        ToolTip = QT_TRANSLATE_NOOP(
            'CreateOrthographicBody',
            'Create a new OrthographicBody instance')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

FreeCADGui.addCommand('CreateOrthographicBody',CreateOrthographicBodyCommand())