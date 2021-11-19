


class PhysicsWorkbench(Workbench):
    def __init__(self):
        self.__class__.Icon = FreeCAD.ConfigGet("AppHomePath") + "Mod/Physics/PhysicsResources/physics-workbench.svg"
        self.__class__.MenuText = "Simulation"
        self.__class__.ToolTip = "Simulation workbench"

    import PhysicsCommand
    import ProjectSetting.Commands.ProjectSettingCommand
    import Control.controlCommand.TaskControlMain

    import FreeCADGui
    import FreeCAD,os
    
    def Initialize(self):
        def QT_TRANSLATE_NOOP(ctx,txt): return txt # dummy function for the QT translator
        from DraftTools import translate
        from PySide import QtCore
        
        
        # FreeCADGui.addLanguagePath("D:/PICGUI/buildD/Mod/Physics/PhysicsResources/translations")
        # FreeCADGui.updateLocale()

        # def getLanguagePath():
        #     import os
        #     return os.path.join(os.path.dirname("__file__"),"PhysicsResources/translations")

        # 移至3D建模工作台
        # cmdlst_control = ["TimerDef", "Timer"]
        cmdlst_m3d = ["Separator", "M3DView", "M3DFind"]
        cmdlst_pal = [ "UndoPal", "RedoPal"]
        # cmdlst_controlPanel = ["Run", "MutiThreadSetting", "Continue", "TimerSwitch", "ReceiveResult", "RefreshState", "CheckResult","LogFile"]
        cmdlst_controlPanel = ["Run", "MutiThreadSetting", "Continue", "TimerSwitch", "RefreshState","LogFile", "Batch"]
        # benches = ["Separator", "Modeling 2D","Modeling 3D","Post Processing"]
        #工程设置
        cmdProjectSettinglst=["ModelingInfo",
                              "WorkSpaceSettings",
                              "NewMaterical",
                              "FiledSetting",
                              "TimeDomainComputing",
                              "DataProcessingSetting",
                              "RunOptions"]

        cmdlst_taskMonitor = ["ReceiveResult", "CheckResult"]

        # self.appendToolbar('Workbench', benches)
        # self.appendToolbar(QT_TRANSLATE_NOOP("Workbench","Common Boundary"), cmdlst_comboundary)
        # self.appendToolbar(QT_TRANSLATE_NOOP("Workbench","Emission Processing"), cmdlst_emit)
        # self.appendToolbar(QT_TRANSLATE_NOOP("Workbench","Special Boundary"), cmdlst_spboundary)
        # self.appendToolbar(QT_TRANSLATE_NOOP("Workbench","Observation"), cmdlst_observe)
        # self.appendToolbar(QT_TRANSLATE_NOOP("Workbench", "Task Control"), cmdlst_control)
        self.appendToolbar(QT_TRANSLATE_NOOP("Workbench", "File"), cmdlst_m3d)
        self.appendToolbar(QT_TRANSLATE_NOOP("Workbench", "File"), cmdlst_pal)
        # add by chenjian
        self.appendToolbar(QT_TRANSLATE_NOOP("Workbench", "ControlPanel"), cmdlst_controlPanel)
        # end

        self.appendToolbar("Task Monitor", cmdlst_taskMonitor)

        # 删除模型翻转工作台
        self.removeToolbar("View")
        # self.appendMenu(QT_TRANSLATE_NOOP("Simulation", "&Simulation"), cmdlst_control)

        # add by chenjian
        # self.appendMenu(QT_TRANSLATE_NOOP("Workbench", "Simulation"), cmdlst_m3d)
        # from PySide import QtCore
        

        self.appendMenu(QT_TRANSLATE_NOOP("Workbench","Simulations"), cmdlst_m3d+cmdlst_controlPanel)
        # end

        # self.appendMenu([QT_TRANSLATE_NOOP("Simulation", "&Simulation"), QT_TRANSLATE_NOOP("Simulation", "Common Boundary")],cmdlst_comboundary)
        # self.appendMenu([QT_TRANSLATE_NOOP("Simulation", "&Simulation"), QT_TRANSLATE_NOOP("Simulation", "Emission Processing")],cmdlst_emit)
        # self.appendMenu([QT_TRANSLATE_NOOP("Simulation", "&Simulation"), QT_TRANSLATE_NOOP("Simulation", "Special Boundary")],cmdlst_spboundary)
        # self.appendMenu([QT_TRANSLATE_NOOP("Simulation", "&Simulation"), QT_TRANSLATE_NOOP("Simulation", "Observation")],cmdlst_observe)
        self.appendMenu(QT_TRANSLATE_NOOP("Workbench", "Project Settings"),cmdProjectSettinglst)
        # FreeCAD.Console.PrintMessage("getLanguagePath():"+str(getLanguagePath())+"\n")
        
        
        # FreeCADGui.addLanguagePath("D:/PICGUI/buildD/Mod/Physics/PhysicsResources/translations")
        # FreeCADGui.updateLocale()
        import os
        # FreeCAD.Console.PrintMessage(os.getcwd()+"/../Mod/Modeling/Modeling3D/modeling3DResources/translations")
        FreeCADGui.addLanguagePath(os.getcwd()+"/../Mod/Modeling/Modeling3D/modeling3DResources/translations")
        FreeCADGui.updateLocale()
        # self.appendMenu("File",["Port"])
        # from PhysicsCommand.TreeStructMain import FigTreeShow               
        # FigTreeShow()



Gui.addWorkbench(PhysicsWorkbench())