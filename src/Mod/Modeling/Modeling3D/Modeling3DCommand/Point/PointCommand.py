# encoding:utf-8
import FreeCAD
import FreeCADGui

#fubiao
import PySide
from PySide import QtCore, QtGui
import os
import Units
#end
import PointNewDialog

import DraftTools
def QT_TRANSLATE_NOOP(ctx,txt): return txt # dummy function for the QT translator
from DraftTools import translate
#Create a Point
class CreatePointCommand:
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
        import CreatePoint
        obj = CreatePoint.createPoint() 
        Form = PointNewDialog.showPointDialog(obj)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling3D/Modeling3DResources/3D_Point.svg"
        MenuText = QT_TRANSLATE_NOOP(
            'CreatePoint',
            'Create Point')
        ToolTip = QT_TRANSLATE_NOOP(
            'CreatePoint',
            'Create a new Point instance')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreatePoint',CreatePointCommand())