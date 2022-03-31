class VisualWorkbench(Workbench):
    """Workbench of Plot module."""
    def __init__(self):
        self.__class__.Icon = FreeCAD.ConfigGet("AppHomePath") + "Mod/Visualization/VisualizationResources/VisualWorkbench.svg"
        self.__class__.MenuText = "Post Processing"
        self.__class__.ToolTip = "Post Processing workbench"

    from VisualizationCommand import VisualizationFunction

    def Initialize(self):
        def QT_TRANSLATE_NOOP(ctx,txt): return txt
        # dummy function for the QT translator
        from DraftTools import translate
        import FreeCADGui,FreeCAD
        # cmdlst = ["Vis_Grid",
        #           "Vis_Labels",
        #           "Vis_Series",
        #           "Vis_Point",
        #           "Vis_Axes",
        #           "Vis_Geometric_Ratio",
        #           "Vis_Struct_grid"]
        # # benches = ["Separator", "Modeling 2D","Modeling 3D", "Simulation"]
        # # self.appendToolbar("Workbench", benches)
        # self.appendToolbar(QT_TRANSLATE_NOOP("Workbench","Graphic post-processing"), cmdlst)
        #
        # self.removeToolbar("View")
        # self.appendMenu(QT_TRANSLATE_NOOP("Workbench","Graphic post-processing"), cmdlst)
        import os
        # FreeCADGui.addLanguagePath("D:/PICGUI/buildD/Mod/Modeling/Modeling3D/modeling3DResources/translations")
        FreeCADGui.addLanguagePath(os.getcwd()+"/../Mod/Modeling/Modeling3D/modeling3DResources/translations")
        FreeCADGui.updateLocale()
        # FreeCAD.Console.PrintMessage("HERE")

Gui.addWorkbench(VisualWorkbench())
