# -*- coding: UTF-8 -*-
import CustomParameter
def Load(workbench):
    # fileList = ["Std_New"]
    # workbench.appendToolbar('File', fileList)
    cmd2d = ["CreatePoint",
              "CreateConformalLine",
              "CreateObliqueLine",
              "CreateConformalArea",
              "CreateFunctionAreaCommand",
              "CreateRectangular",
              "CreatePolygonal"]
    cmd3dCommon = ["CreateConformal",
                    "CreateAnnular",
                    "CreateCylinder",
                    "CreateSpecialCone",
                    "CreateSpherical",
                    "CreateToroidal_Section",
                    "CreateAnnular_Section",
                    "CreateFunction",
                    "CreateParallelepipedal"
                  ]
    cmd3dSpecil = ["CreatePyramid",
                    "CreateWedge",
                    "CreateRhombus",
                    "CreateExtruded",
                    "CreateTetrahedron",
                    "CreateHelical",
                  ]
    cmd3dComplex =[ "CreateRevolutionCommand",
                    "Object_Array",
                    "CreateNewVolArrayCommand",
                    "CreateNewDraftModeling_ExtrudeCommand",
                    "CreateNewDraftModeling_RevolutionCommand"
                  ]
    view = ["Std_ViewAxo","Separator", "Std_ViewFront", "Std_ViewTop", "Std_ViewRight", 
    "Separator", "Std_ViewRear","Std_ViewBottom","Std_ViewLeft","Separator","Std_MeasureDistance"]
    workbench.appendToolbar('视图', view)
    workbench.appendToolbar('点线面', cmd2d)
    workbench.appendToolbar('常用体', cmd3dCommon)
    workbench.appendToolbar('特殊体', cmd3dSpecil)
    workbench.appendToolbar('复杂体', cmd3dComplex)
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
                 "Populate",
                 "Species"]
    cmdNewSetting = ["TimeDomainComputing",
                    'NewMaterical',
                      'Species']

    # 物理建模
    cmdlst_comboundary = ["Port", "Free", "Sym"]
    cmdlst_emit = ["EmB", "EmE", "EmG","Popu", "EmH", "EmT","Secd","Ioni"]
    cmdlst_spboundary = ["Sol", "Excitation power", "Foil", "Ind"]
    cmdlst_observe = ["Cntr", "Vec", "Ran", "Pha", "Obs"]
    workbench.appendToolbar('边界设置', cmdlst_comboundary)
    workbench.appendToolbar('边界设置', cmdlst_spboundary)
    workbench.appendToolbar('发射设置', cmdlst_emit)
    workbench.appendToolbar('观测设置', cmdlst_observe)

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
    setting = ["NewMaterical","FiledSetting","TimeDomainComputingMenu","Merge","Species","Mark"]
    projectSetting = ["ModelingInfo","WorkSpaceSettings" ,"DataProcessingSetting" , "RunOptions" ]
    workbench.appendToolbar('定时器设置', cmdlst_Timer)

    workbench.appendToolbar('工程设置',projectSetting)
    workbench.appendToolbar('工程设置',cmdDynamicDate)
    workbench.appendToolbar('其他设置',setting)
    clip = ["Clip"]
    workbench.appendToolbar('工具',clip)

    vcmdlst = ["Vis_Grid",
                  "Vis_Labels",
                  "Vis_Series",
                  "Vis_Point",
                  "Vis_Axes",
                  "Vis_Geometric_Ratio",
                  "Vis_Struct_grid"]
    workbench.appendToolbar('后处理',vcmdlst)
    

    # workbench.appendToolbar('File', cmdOptlst)
    # # workbench.appendToolbar('Workbench', benches)
    # workbench.appendToolbar("File", cmdlst_m3d)
    # workbench.appendToolbar("View",viewCmd)
    # # 把自定义参数设置挪动到前面
    # workbench.appendToolbar('DynamicDate', cmdDynamicDate)
    # workbench.appendToolbar('3D Modeling', cmdlst)
    
    # # 这是测试用的ToolBar，在测试完成后要注释掉
    # # workbench.appendToolbar('ShowAllFunction', cmdlst_new)
    # workbench.appendToolbar('NewSettinbgs', cmdNewSetting)

    # # 添加物理建模工具栏
    # # workbench.appendToolbar("Common Boundary", cmdlst_comboundary)
    # # workbench.appendToolbar("Emission Processing", cmdlst_emit)
    # # workbench.appendToolbar("Special Boundary", cmdlst_spboundary)
    # # workbench.appendToolbar("Observation", cmdlst_observe)
    # workbench.appendToolbar("Physics", cmdlst_physics)
    # workbench.appendToolbar("Timer", cmdlst_Timer)

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

    # 测试用的代码
    # cmdTest = ["CreateFoil","CreateDriv","CreatePort","CreateInductor","CreateFreeSpace","CreateSymtry","CreateMark","CreateCntr",
    #            "CreateVector","CreatePhasSpace","CreateAreaRan","CreateObserve"]
    # workbench.appendToolbar("File", cmdTest)
