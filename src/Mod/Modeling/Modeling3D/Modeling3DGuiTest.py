import FreeCAD
import FreeCADGui

class Save:
    def Activated(self):
        FreeCAD.Console.PrintMessage("3DModeling_Saving now!\n")

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling3D/modeling3DResources/save.svg"
        MenuText = "3DModeling_Save"
        ToolTip = "Save the 3DModeling as an obj file"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

FreeCADGui.addCommand('3DModeling_Save', Save())