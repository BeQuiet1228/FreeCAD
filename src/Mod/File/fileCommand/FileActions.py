import FreeCAD
import FreeCADGui

class SaveAs:
    def Activated(self):
        from PySide import QtGui, QtCore
        FreeCAD.Console.PrintMessage("Save file as...\n")
        reply = QtGui.QMessageBox.information(None, "", "save-as button")
    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/File/FileResources/file-save-as.svg"
        MenuText = "File save as"
        ToolTip = "File save as..."
        Accel = "Ctrl+F4"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'Accel': Accel,
                'ToolTip': ToolTip}

class Close:
    def Activated(self):
        from PySide import QtGui, QtCore
        FreeCAD.Console.PrintMessage("Close file\n")
        reply = QtGui.QMessageBox.information(None, "", "close button")
    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/File/FileResources/file-close.svg"
        MenuText = "Close file"
        ToolTip = "Close file"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

class Exit:
    def Activated(self):
        from PySide import QtGui, QtCore
        FreeCAD.Console.PrintMessage("Exit app\n")
        reply = QtGui.QMessageBox.information(None,"","exit button")
    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/File/FileResources/application-exit.svg"
        MenuText = "Exit app"
        ToolTip = "Exit app"
        Accel = "Alt+F4"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'Accel': Accel,
                'ToolTip': ToolTip}

class RecentFile:
    def Activated(self):
        from PySide import QtGui, QtCore
        FreeCAD.Console.PrintMessage("open recent file\n")
        reply = QtGui.QMessageBox.information(None,"","recent file button")
    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/File/FileResources/file-recent.svg"
        MenuText = "Open recent file"
        ToolTip = "Open recent file"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

FreeCADGui.addCommand('File_SaveAs', SaveAs())
FreeCADGui.addCommand('File_Close', Close())
FreeCADGui.addCommand('App_Exit', Exit())
FreeCADGui.addCommand('File_Recent', RecentFile())