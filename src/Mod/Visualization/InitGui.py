class VisualWorkbench(Workbench):
    """Workbench of Plot module."""
    def __init__(self):
        self.__class__.Icon = FreeCAD.ConfigGet("AppHomePath") + "Mod/Visualization/visualizationResources/VisualWorkbench.svg"
        self.__class__.MenuText = "Post Processing"
        self.__class__.ToolTip = "Post Processing workbench"

    from visualizationGui import VisualizationGui

    def Initialize(self):
        cmdlst = ["Plot_SaveFig",
                  "Plot_Axes",
                  "Plot_Series",
                  "Plot_Grid",
                  "Plot_Legend",
                  "Plot_Labels",
                  "Plot_Positions",
                  "Visualization_Plot"]
        benches = ["Modeling 2D","Modeling 3D", "Simulation"]
        self.appendToolbar("File", benches)
        self.appendToolbar("Post Processing", cmdlst)
        self.appendMenu("Post Processing", cmdlst)

Gui.addWorkbench(VisualWorkbench())
