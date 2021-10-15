#sys.path.append(Dir + '/Modeling2D/')
#class Modeling2DWorkbench(Workbench):
#    "2D Modeling workbench object"
#    def __init__(self):
#        # FreeCAD.getResourceDir() = E:/FreeCAD/FreeCAD-Build/data/
#        # FreeCAD.ConfigGet("UserAppData") = C:\Users\chenjian\AppData\Roaming\FreeCAD\
#        # FreeCAD.ConfigGet("AppHomePath") = E:/FreeCAD/FreeCAD-Build/
#        self.__class__.Icon = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling2D/modeling2DResources/2DModelingWorkbench.svg"
#        self.__class__.MenuText = "2D Modeling"
#        self.__class__.ToolTip = "2D Modeling workbench"
#
#    
#
#    def Initialize(self):
#        # load the module
#        import Modeling2DCommand
#        import Modeling2DGui
#
#
#        Modeling2DGui.LoadAll(self)
#
#Gui.addWorkbench(Modeling2DWorkbench())
