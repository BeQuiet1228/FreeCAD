import FreeCAD
import FreeCADGui

class Save:
    def Activated(self):
        from PySide import QtGui, QtCore
        FreeCAD.Console.PrintMessage("2DModeling_Saving now!\n")
        reply = QtGui.QMessageBox.information(None,"","2DModeling_Saving now!")
    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling2D/Modeling2DResources/save.svg"
        MenuText = "2DModeling_Save"
        ToolTip = "Save the 2DModeling as an obj file"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

FreeCADGui.addCommand('2DModeling_Save', Save())