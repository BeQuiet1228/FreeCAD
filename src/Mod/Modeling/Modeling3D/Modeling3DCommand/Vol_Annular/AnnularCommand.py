# encoding:utf-8
import FreeCAD
import FreeCADGui

#fubiao
import PySide
from PySide import QtCore, QtGui
import os
import Units
import AnnularNewDialog
#end
import DraftTools
def QT_TRANSLATE_NOOP(ctx,txt): return txt # dummy function for the QT translator
from DraftTools import translate
#Create a Annular
class CreateAnnularCommand:
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        if FreeCAD.activeDocument() == None:
            #FreeCAD.newDocument()
            from Common import CommonCommand
            CommonCommand.NewDocument()
        import CreateAnnular
        obj = CreateAnnular.createAnnular() 
        Form = AnnularNewDialog.showAnnularDialog(obj)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling3D/Modeling3DResources/3D_Vol_Annular.svg"
        MenuText = QT_TRANSLATE_NOOP(
            'CreateAnnular',
            'Create Annular')
        ToolTip = QT_TRANSLATE_NOOP(
            'CreateAnnular',
            'Create a new Annular instance')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreateAnnular',CreateAnnularCommand())