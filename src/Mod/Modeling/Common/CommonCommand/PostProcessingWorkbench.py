import FreeCAD
import FreeCADGui

class PostProcessingWorkbench:
    def Activated(self):
        FreeCADGui.activateWorkbench("VisualWorkbench")

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Visualization/visualizationResources/VisualWorkbench.svg"
        MenuText = "Post Processing"
        ToolTip = "To Post Processing Part"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

FreeCADGui.addCommand('Post Processing', PostProcessingWorkbench())