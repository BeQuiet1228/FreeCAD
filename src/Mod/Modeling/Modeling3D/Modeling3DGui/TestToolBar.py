# -*- coding: UTF-8 -*-
def Load(workbench):
    # fileList = ["Std_New"]
    # workbench.appendToolbar('File', fileList)
    cmdlst = ["CreatePoint",
              "CreateConformalLine",
              "CreateObliqueLine",
              "CreateConformalArea",
              "CreateFunctionAreaCommand",
              "CreateRectangular",
              "CreatePolygonal",
              # "PolygonalCommand",
              "CreateConformal",
              "CreateAnnular",
              # "CreateTorusFace",
              "CreateCylinder",
              # "CreateCone",
              "CreateSpecialCone",
            #   "CreateTorus",
            #   "CreateOrthographicBody",
              "CreateParallelepipedal",
              "CreateSpherical",
              "CreateWedge",
              "CreatePyramid",
              "CreateRhombus",
              "CreateExtruded",
              "CreateTetrahedron",
              "CreateToroidal_Section",
              "CreateAnnular_Section",
              "CreateHelical",
              "CreateRevolutionCommand",
              "Object_Array",
              "CreateFunction",
              "CreateNewVolArrayCommand",
              "CreateNewDraftModeling_ExtrudeCommand",
              "CreateNewDraftModeling_RevolutionCommand",
              # "ShowAllFunctionCommand"
              #"CreateArray",
              #"TestCommand"
              ]
    # "CreateFunction"]
    cmdlst_new = ["ShowAllFunctionCommand",
                 "EmSE",
                 "Merge",
                 "Populate",
                 "Species"]
    cmdNewSetting = ["TimeDomainComputing",
                    'NewMaterical',
                      'Species']

    # 物理建模
    cmdlst_comboundary = ["Port", "Free", "Sym"]
    cmdlst_emit = ["EmB", "EmE", "EmG","Popu", "EmH", "EmT","Secd","Ioni"]
    cmdlst_spboundary = ["Sol", "Excitation power", "Foil", "Ind"]
    cmdlst_observe = ["Cntr", "Vec", "Pha", "Ran", "Obs"]
    cmdlst_physics=[
                    "Sol", "Excitation power", "Foil", "Ind",
                    "Separator",
                    "Port", "Free", "Sym", "Mark",
                    "Separator",
                    "EmB", "EmE", "EmG","Popu", "EmH", "EmT","Secd","Ioni",
                    "Separator",
                    "Cntr", "Vec", "Pha", "Ran", "Obs"]

    cmdOptlst = [
                 "Separator",
                #"ClipCommand",
                  "Clip",
                #  "RecomputeBooleanForAllObjs",
                #  "RecomputeBooleanForPartObjs",
                 "CopyCommand",
                 "PasteCommand",
                 "CutCommand",
                 #"CutCommand"
                 ]

    cmdDynamicDate = [
                      # "DynamicDataCreateObject",
                      # "DynamicDataAddProperty",
                      # "DynamicDataRemoveProperty",
                      "CustomeParameterMainCommand"
                      ]

    cmdlst_m3d = ["Separator", "M3DView", "M3DFind","UndoPal","RedoPal"]

    # benches = ["Separator", "Simulation", "Post Processing"]
    
    viewCmd=["RotateViewLeft","RotateViewRight"]

    # cmdParam=["CustomeParameterMainCommand"]

    cmdlst_Timer = ["TimerDef", "Timer"]

    workbench.appendToolbar('File', cmdOptlst)
    # workbench.appendToolbar('Workbench', benches)
    workbench.appendToolbar("File", cmdlst_m3d)
    workbench.appendToolbar("View",viewCmd)
    # 把自定义参数设置挪动到前面
    workbench.appendToolbar('DynamicDate', cmdDynamicDate)
    workbench.appendToolbar('3D Modeling', cmdlst)
    
    # 这是测试用的ToolBar，在测试完成后要注释掉
    # workbench.appendToolbar('ShowAllFunction', cmdlst_new)
    workbench.appendToolbar('NewSettinbgs', cmdNewSetting)

    # 添加物理建模工具栏
    # workbench.appendToolbar("Common Boundary", cmdlst_comboundary)
    # workbench.appendToolbar("Emission Processing", cmdlst_emit)
    # workbench.appendToolbar("Special Boundary", cmdlst_spboundary)
    # workbench.appendToolbar("Observation", cmdlst_observe)
    workbench.appendToolbar("Physics", cmdlst_physics)
    workbench.appendToolbar("Timer", cmdlst_Timer)

    # workbench.appendToolbar('Operations', cmdOptlst)
    # workbench.appendToolbar("M3DView", cmdlst_m3d)
    # workbench.appendToolbar("CustomParam",cmdParam)

######################################ProjectSettings####################################
    # cmdProjectSettinglst=["WorkSpaceSettings",
    #                        "NewMaterical",
    #                        "FiledSetting",
    #                        "TimeDomainComputing",
    #                        "DataProcessingSetting",
    #                        "ModelingInfo"]
    # workbench.appendToolbar("Project Settings",cmdProjectSettinglst)
    # workbench.appendCommandbar('3D Modeling',cmdOptlst)
    # FreeCAD.Console.PrintMessage(workbenchNameList)
    # if "MeshWorkbench" in workbenchNameList:
    #     Gui.removeWorkbench("MeshWorkbench")



