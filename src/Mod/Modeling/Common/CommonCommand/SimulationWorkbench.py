import FreeCAD
import FreeCADGui
from PySide import QtGui
class SimulationWorkbench:
    def Activated(self):
        FreeCADGui.activateWorkbench("PhysicsWorkbench")

        mainWindow = FreeCADGui.getMainWindow()
        propertyView = mainWindow.findChild(QtGui.QDockWidget, "Property view")
        propertyView.setVisible(False)
 
    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Physics/PhysicsResources/physics-workbench.svg"
        MenuText = "Simulation"
        ToolTip = "To Simulation Part"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

FreeCADGui.addCommand('Simulation', SimulationWorkbench())