import FreeCAD
import FreeCADGui

#fubiao
import PySide
from PySide import QtCore, QtGui
import os
import Units
#end
import ConformalAreaNewDialog

import DraftTools
def QT_TRANSLATE_NOOP(ctx,txt): return txt # dummy function for the QT translator
from DraftTools import translate
# FreeCADGui.addLanguagePath("D:/PICGUI/buildD/Mod/Modeling/Modeling3D/modeling3DResources/translations")

class CreateConformalAreaCommand:
    def Activated(self):
        if FreeCAD.activeDocument()==None:
            FreeCAD.newDocument()
        import CreateConformalArea
        #lzg
        obj=CreateConformalArea.createConformalArea()
        Form = ConformalAreaNewDialog.showConformalAreaDialog(obj)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling3D/Modeling3DResources/3D_Area_Conformal.svg"
        MenuText = QT_TRANSLATE_NOOP('CreateConformalArea','Create ConformalArea')
        ToolTip = QT_TRANSLATE_NOOP('CreateConformalArea','Create a new ConformalArea instance')

        return {'Pixmap': IconPath,'MenuText': MenuText,'ToolTip': ToolTip}

    def IsActive(self):
        if not FreeCAD.ActiveDocument:
            return False
        return True

FreeCADGui.addCommand('CreateConformalArea',CreateConformalAreaCommand())