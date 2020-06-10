import FreeCAD
import FreeCADGui

#fubiao
import PySide
from PySide import QtCore, QtGui
import os
import Units
#end
class Save:
    def Activated(self):
        from PySide import QtGui, QtCore
        FreeCAD.Console.PrintMessage("3DModeling_Saving now!\n")
        reply = QtGui.QMessageBox.information(None,"","3DModeling_Saving now!")
    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling3D/Modeling3DResources/save.svg"
        MenuText = "2DModeling_Save"

        ToolTip = "Save the 2DModeling as an obj file"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

#fubiao




FreeCADGui.addCommand('3DModeling_Save', Save())
#fubiao

