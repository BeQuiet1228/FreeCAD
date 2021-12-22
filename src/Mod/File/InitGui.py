import sys
sys.path.append(Dir)
import FileGui
import FileCommand
class FileWorkbench(Workbench):
    def __init__(self):
        self.__class__.Icon = FreeCAD.ConfigGet("AppHomePath") + "Mod/File/FileResources/file-workbench.svg"
        self.__class__.MenuText = "Files"
        self.__class__.ToolTip = "File workbench"

    import FileCommand.FileActions

    def Initialize(self):
        cmdlst = ["File_SaveAs",
                  "File_Recent",
                  "File_Close",
                  "App_Exit"]
        self.appendToolbar("Files", cmdlst)

#Gui.addWorkbench(FileWorkbench())
