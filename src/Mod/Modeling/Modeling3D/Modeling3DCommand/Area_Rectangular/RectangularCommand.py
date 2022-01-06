import FreeCAD
import FreeCADGui

#fubiao
import PySide
from PySide import QtCore, QtGui
import os
import Units
from Common.Tools import CoordinateSystemTools
import RectangularAreaNewDialog
#end
import DraftTools
def QT_TRANSLATE_NOOP(ctx,txt): return txt # dummy function for the QT translator
from DraftTools import translate

class CreateRectangularCommand:
    def Activated(self):
        if FreeCAD.activeDocument()==None:
            FreeCAD.newDocument()
        import CreateRectangular
        obj = CreateRectangular.createRectangular()
        Form = RectangularAreaNewDialog.showRectangularAreaDialog(obj)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling3D/Modeling3DResources/3D_Area_Rectangular.svg"
        MenuText = QT_TRANSLATE_NOOP(
            'CreateRectangular',
            'Create Rectangular')
        ToolTip = QT_TRANSLATE_NOOP(
            'CreateRectangular',
            'Create a new Rectangular instance')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            #Rectangular coordinate system only
            if FreeCAD.ActiveDocument.CoordinateSystem==CoordinateSystemTools.CoordinateType.Rectangular:
                return True
            else:
                return False
        else:
            return False

FreeCADGui.addCommand('CreateRectangular',CreateRectangularCommand())