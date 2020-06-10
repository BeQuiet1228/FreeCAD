import FreeCAD
import FreeCADGui

IconCommonPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Visualization/visualizationResources/"

class Save:
    def Activated(self):
        FreeCAD.Console.PrintMessage("visualization_Save\n")

    def GetResources(self):
        IconPath = IconCommonPath + "/Save.svg"
        MenuText = "Plot_Save"
        ToolTip = "Save the plot as an image file"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


class Axes:
    def Activated(self):
        FreeCAD.Console.PrintMessage("visualization_Axes\n")

    def GetResources(self):
        IconPath = IconCommonPath + "/Axes.svg"
        MenuText = "Plot axes"
        ToolTip = "Configure the axes parameters"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


class Series:
    def Activated(self):
        FreeCAD.Console.PrintMessage("visualization_Series\n")

    def GetResources(self):
        IconPath = IconCommonPath + "/Series.svg"
        MenuText = "Plot_series"
        ToolTip = "Configure series drawing style and label"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


class Grid:
    def Activated(self):
        FreeCAD.Console.PrintMessage("visualization_Grid\n")

    def GetResources(self):
        IconPath = IconCommonPath + "/Grid.svg"
        MenuText = "Plot_Grid"
        ToolTip = "Plot_Grid"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


class Legend:
    def Activated(self):
        FreeCAD.Console.PrintMessage("visualization_Legend\n")

    def GetResources(self):
        IconPath = IconCommonPath + "/Legend.svg"
        MenuText = "Plot_Legend"
        ToolTip = "Show/Hide legend on selected plot"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


class Labels:
    def Activated(self):
        FreeCAD.Console.PrintMessage("visualization_Labels\n")

    def GetResources(self):
        IconPath = IconCommonPath + "/Labels.svg"
        MenuText = "Plot_Labels"
        ToolTip = "Set title and axes labels"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


class Positions:
    def Activated(self):
        FreeCAD.Console.PrintMessage("visualization_Position\n")

    def GetResources(self):
        IconPath = IconCommonPath + "/Positions.svg"
        MenuText = "Plot_Positions"
        ToolTip = "Set labels and legend positions and sizes"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

class Visualization_Plot:
    def Activated(self):
        FreeCAD.Console.PrintMessage("Visualization_Plot\n")
        import visualizationCommand.VisualizationPlot as VisualizationPlot
        VisualizationPlot.plot()
    def GetResources(self):
        IconPath = IconCommonPath + "/Positions.svg"
        MenuText = "Visualization_Plot"
        ToolTip = "Visualization_Plot"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

class Modeling2DWorkbench:
    def Activated(self):
        FreeCADGui.activateWorkbench("Modeling2DWorkbench")

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling2D/modeling2DResources/2DModelingWorkbench.svg"
        MenuText = "2D Modeling"
        ToolTip = "To 2D Modeling Part"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

class Modeling3DWorkbench:
    def Activated(self):
        FreeCADGui.activateWorkbench("Modeling3DWorkbench")

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling3D/modeling3DResources/3DModelingWorkbench.svg"
        MenuText = "3D Modeling"
        ToolTip = "To 3D Modeling Part"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

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

FreeCADGui.addCommand('Plot_SaveFig', Save())
FreeCADGui.addCommand('Plot_Axes', Axes())
FreeCADGui.addCommand('Plot_Series', Series())
FreeCADGui.addCommand('Plot_Grid', Grid())
FreeCADGui.addCommand('Plot_Legend', Legend())
FreeCADGui.addCommand('Plot_Labels', Labels())
FreeCADGui.addCommand('Plot_Positions', Positions())
FreeCADGui.addCommand('Visualization_Plot', Visualization_Plot())
FreeCADGui.addCommand('Modeling 2D', Modeling2DWorkbench())
FreeCADGui.addCommand('Modeling 3D', Modeling3DWorkbench())
FreeCADGui.addCommand('Simulation', SimulationWorkbench())
