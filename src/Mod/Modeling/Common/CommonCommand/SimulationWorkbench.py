import FreeCAD
import FreeCADGui

class SimulationWorkbench:
    def Activated(self):
        FreeCADGui.activateWorkbench("PhysicsWorkbench")

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Physics/PhysicsResources/physics-workbench.svg"
        MenuText = "Simulation"
        ToolTip = "To Simulation Part"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

FreeCADGui.addCommand('Simulation', SimulationWorkbench())