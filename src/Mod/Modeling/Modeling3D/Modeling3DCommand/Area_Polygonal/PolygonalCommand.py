import FreeCAD
import FreeCADGui

#fubiao
import PySide
from PySide import QtCore, QtGui
import os
import Units
#end
import PolygonalNewDialog

import DraftTools
def QT_TRANSLATE_NOOP(ctx,txt): return txt # dummy function for the QT translator
from DraftTools import translate

class CreatePolygonalCommand:
    def Activated(self):
        if FreeCAD.activeDocument()==None:
            FreeCAD.newDocument()
        import CreatePolygonal
        # lzg
        obj = CreatePolygonal.createPolygonal()
        Form = PolygonalNewDialog.showPolygonalDialog(obj)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling3D/Modeling3DResources/3D_Area_Polygonal.svg"
        MenuText = QT_TRANSLATE_NOOP(
            'CreatePolygonal',
            'Create Polygonal')
        ToolTip = QT_TRANSLATE_NOOP(
            'CreatePolygonal',
            'Create a new Polygonal instance')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

FreeCADGui.addCommand('CreatePolygonal',CreatePolygonalCommand())