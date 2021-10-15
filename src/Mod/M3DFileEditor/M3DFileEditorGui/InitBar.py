def Load(workbench):
    cmdlst_m3d1 = ["EditorOpen", "EditorSave","EditorSaveAs"]
    cmdlst_m3d2 = ["EditorUndo","EditorRedo","EditorCut","EditorCopy","EditorPaste","EditorFind","EditorReplace"]
    cmdlst_m3d3 = ["EditorDisplay"]
    workbench.appendToolbar("M3D File Editor - other operation", cmdlst_m3d3)
    workbench.appendToolbar("M3D File Editor - basic operation", cmdlst_m3d2)
    workbench.appendToolbar("M3D File Editor - file operation", cmdlst_m3d1)

    workbench.removeToolbar("View")


