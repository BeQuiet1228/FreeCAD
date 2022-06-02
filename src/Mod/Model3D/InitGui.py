# -*- coding: utf-8 -*-
import FreeCAD
import FreeCADGui


class Modeling3DWorkbench(Workbench):
    def __init__(self):
        self.__class__.Icon = FreeCAD.getResourceDir() + "Mod/Draft/Resources/icons/DraftWorkbench.svg"
        self.__class__.MenuText = "Draft123123123"
        self.__class__.ToolTip = "The Draft module is used for basic 2D CAD Drafting"

    def Initialize(self):
        """This function is executed when FreeCAD starts"""
        # import MyModuleA, MyModuleB  # import here all the needed files that create your FreeCAD commands
        import Modeling.Modeling2D.Modeling2DCommand
        import Model3D.Command3D.Model3DCommand
        import Gui3D
        Gui3D.LoadAll(self)

FreeCADGui.addWorkbench(Modeling3DWorkbench())
