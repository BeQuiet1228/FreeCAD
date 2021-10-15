import FreeCAD
import FreeCADGui
from PySide import QtGui
class PostProcessingWorkbench:
    def Activated(self):
        FreeCADGui.activateWorkbench("VisualWorkbench")

        mainWindow = FreeCADGui.getMainWindow()
        propertyView = mainWindow.findChild(QtGui.QDockWidget, "Property view")
        propertyView.setVisible(False)

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Visualization/visualizationResources/VisualWorkbench.svg"
        MenuText = "Post Processing"
        ToolTip = "To Post Processing Part"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

FreeCADGui.addCommand('Post Processing', PostProcessingWorkbench())