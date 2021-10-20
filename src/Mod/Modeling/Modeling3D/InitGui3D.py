sys.path.append(Dir + '/Modeling3D/')
sys.path.append(Dir)
import FreeCADGui
class Modeling3DWorkbench(Workbench):
    "3D Modeling workbench object"
    def __init__(self):
        self.__class__.Icon = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling3D/modeling3DResources/3DModelingWorkbench.svg"
        self.__class__.MenuText = "3D Modeling"
        self.__class__.ToolTip = "3D Modeling workbench"

    import Modeling3DGui

    def Initialize(self):
        # load the module
        import Modeling3DCommand
        import Modeling3DGui

        Modeling3DGui.LoadAll(self)

# FreeCADGui.addWorkbench(Modeling3DWorkbench())
