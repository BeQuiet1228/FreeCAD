import FreeCAD
import FreeCADGui

#fubiao
import PySide
from PySide import QtCore, QtGui
import os
import Units
import WedgeNewDialog
#end
import DraftTools
def QT_TRANSLATE_NOOP(ctx,txt): return txt # dummy function for the QT translator
from DraftTools import translate
#Create a Wedge
class CreateWedgeCommand:
    def Activated(self):
        if FreeCAD.activeDocument() == None:
            FreeCAD.newDocument()
        import CreateWedge
        obj = CreateWedge.createWedge() 
        Form = WedgeNewDialog.showWedgeDialog(obj)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling3D/Modeling3DResources/3D_Vol_Wedge.svg"
        MenuText = QT_TRANSLATE_NOOP(
            'CreateWedge',
            'Create Wedge')
        ToolTip = QT_TRANSLATE_NOOP(
            'CreateWedge',
            'Create a new Wedge instance')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

FreeCADGui.addCommand('CreateWedge',CreateWedgeCommand())
#end