import FreeCAD
import FreeCADGui
from PySide import QtGui
class M3DEditorWorkbench:
    def Activated(self):
        FreeCADGui.activateWorkbench("M3DFileEditorWorkbench")
        mainWindow = FreeCADGui.getMainWindow()
        propertyView = mainWindow.findChild(QtGui.QDockWidget, "Property view")
        propertyView.setVisible(False)
 
    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/M3DFileEditor/M3DFileEditorResources/M3DFileEditorWorkbench.svg"
        MenuText = "M3D File Editor"
        ToolTip = "To M3D File Editor Part"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

FreeCADGui.addCommand('M3D File Editor', M3DEditorWorkbench())
