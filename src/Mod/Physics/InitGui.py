class PhysicsWorkbench(Workbench):
    def __init__(self):
        self.__class__.Icon = FreeCAD.ConfigGet("AppHomePath") + "Mod/Physics/PhysicsResources/physics-workbench.svg"
        self.__class__.MenuText = "Simulation"
        self.__class__.ToolTip = "Simulation workbench"

    import PhysicsCommand.Simulation

    def Initialize(self):
        def QT_TRANSLATE_NOOP(scope, text):
            return text
        cmdlst_comboundary = ["Port","Free","Sym"]
        cmdlst_emit = ["EmB","EmE","EmG","EmH","EmT"]
        cmdlst_spboundary = ["Sol","Excitation power","Foil","Ind"]
        cmdlst_observe = ["CnTr","Vec","Pha","Ran","Obs"]
        cmdlst_control = ["TimerDef","Timer","Run","AllRun"]
        benches = ["Modeling 2D","Modeling 3D","Post Processing"]

        self.appendToolbar('File', benches)
        self.appendToolbar(QT_TRANSLATE_NOOP("Workbench","Common Boundary"), cmdlst_comboundary)
        self.appendToolbar(QT_TRANSLATE_NOOP("Workbench","Emission Processing"), cmdlst_emit)
        self.appendToolbar(QT_TRANSLATE_NOOP("Workbench","Special Boundary"), cmdlst_spboundary)
        self.appendToolbar(QT_TRANSLATE_NOOP("Workbench","Observation"), cmdlst_observe)
        self.appendToolbar(QT_TRANSLATE_NOOP("Workbench","Task Control"), cmdlst_control)
        self.appendMenu(QT_TRANSLATE_NOOP("Simulation", "&Simulation"), cmdlst_control)
        self.appendMenu([QT_TRANSLATE_NOOP("Simulation", "&Simulation"), QT_TRANSLATE_NOOP("Simulation", "Common Boundary")],cmdlst_comboundary)
        self.appendMenu([QT_TRANSLATE_NOOP("Simulation", "&Simulation"), QT_TRANSLATE_NOOP("Simulation", "Emission Processing")],cmdlst_emit)
        self.appendMenu([QT_TRANSLATE_NOOP("Simulation", "&Simulation"), QT_TRANSLATE_NOOP("Simulation", "Special Boundary")],cmdlst_spboundary)
        self.appendMenu([QT_TRANSLATE_NOOP("Simulation", "&Simulation"), QT_TRANSLATE_NOOP("Simulation", "Observation")],cmdlst_observe)

Gui.addWorkbench(PhysicsWorkbench())