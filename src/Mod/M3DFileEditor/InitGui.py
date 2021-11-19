# -*- coding: utf-8 -*-
class M3DFileEditorWorkbench(Workbench):

    def __init__(self):
        self.__class__.Icon = FreeCAD.ConfigGet(
            "AppHomePath") + "Mod/M3DFileEditor/M3DFileEditorResources/M3DFileEditorWorkbench.svg"
        self.__class__.MenuText = "M3D File Editor"
        self.__class__.ToolTip = "M3D File Editor workbench"

    def Initialize(self):
        # load the module
        import M3DFileEditorCommand
        import M3DFileEditorGui
        from Physics.PhysicsCommand import Simulation
        from Control.controlCommand import TaskControlMain
        M3DFileEditorGui.LoadAll(self)

        # 显示文本编辑器
        from M3DFileEditor.M3DFileEditorCommand.FileTextEditor import FileEditor
        FileEditor().showThisSubWindow()

Gui.addWorkbench(M3DFileEditorWorkbench())