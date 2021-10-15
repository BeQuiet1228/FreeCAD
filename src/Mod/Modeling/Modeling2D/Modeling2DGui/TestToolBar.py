# -*- coding: utf8 -*-
from File.FileCommand.M2dFile import M2DContainer

def Load(workbench):

    paramList = ["CustomeParameterMainCommand","CreateMacroParticle", "CreateNewMaterial", "CreateParticleDefine"]

    cmdList = ["Draft_Line", "Draft_Wire", "Draft_Circle", "Draft_Arc", "Draft_Ellipse",
               "Draft_Polygon", "Draft_Rectangle", "Draft_Text",
               "Draft_Dimension", "Draft_BSpline", "Draft_Point",
               "Draft_ShapeString", "Draft_Facebinder", "Draft_BezCurve", "Draft_Label"]

    model2DList = ["CreatePoint_2D", "CreateLine_2D", "CreateLineConformal_2D", "CreatePolygonal_2D",
                   "CreateAreaConformal_2D", "CreateRectangle_2D", "CreateCircular2D",
                   "CreateSector_2D", "Fillet2D_2D", "CreateFunction2D", "CreateText"]

    cmd2DCommon = ["CreatePoint_2D", "CreateLineConformal_2D", "CreateLine_2D"]

    cmd2DComplex = ["CreateAreaConformal_2D", "CreateRectangle_2D", "CreatePolygonal_2D", "CreateCircular2D",
                    "CreateSector_2D", "Fillet2D_2D", "CreateFunction2D"]

    modelBoolList = ["UpdateBooleanCommand", "AdjustView", "SetGrid", "RepairModel", "CreateText", "CreateDimension2D"]

    cmdPhysicSet = ["CreateFoil", "CreateDriv", "CreatePort", "CreateInductor", "CreateFreeSpace", "CreateSymtry","CreateMark",
                         "CreateBeam", "CreateExps", "CreateGyro", "CreatePopu", "CreateFeld", "CreateTher","CreateSecd",
                         "CreateIoni", "CreateCntr", "CreateVector", "CreatePhasSpace", "CreateAreaRan", "CreateObserve"]

    # cmdProjectSet = ["CreateMacroParticle", "CreateNewMaterial", "CreateParticleDefine"]
    otherSetting = ["CreateNewMaterial", "CreateFiledSetting", "CreateTimeDomainSetting", "CreateMacroParticle",
                    "CreateParticleDefine", "CreateMark"]

    cmd2DBoundary = ["CreatePort", "CreateFreeSpace", "CreateSymtry",
                     "CreateFoil", "CreateDriv", "CreateInductor"]

    cmd2DEmit = ["CreateBeam", "CreateExps", "CreateGyro", "CreatePopu",
                 "CreateFeld", "CreateTher", "CreateSecd", "CreateIoni"]

    cmd2DObserve = ["CreateCntr", "CreateVector",
                    "CreateAreaRan",  "CreatePhasSpace","CreateObserve"]

    cmd2DTimer = ["CreateDefTimer", "CreateCustomTimer"]

    # 约束工具
    # cmdSnapList = ['Draft_Snap_Lock', 'Draft_Snap_Midpoint', 'Draft_Snap_Perpendicular',
    #                  'Draft_Snap_Grid', 'Draft_Snap_Intersection', 'Draft_Snap_Parallel',
    #                  'Draft_Snap_Endpoint', 'Draft_Snap_Angle', 'Draft_Snap_Center',
    #                  'Draft_Snap_Extension', 'Draft_Snap_Near', 'Draft_Snap_Ortho', 'Draft_Snap_Special',
    #                  'Draft_Snap_Dimensions', 'Draft_Snap_WorkingPlane']

    cmdSnapList = ['Draft_Snap_Lock']
    # workbench.appendToolbar('Modeling2DOriginal', cmdList)
    # workbench.appendToolbar('Modeling2D', model2DList)
    # workbench.appendToolbar('Modeling2DPhy', cmdPhysicSet)
    # workbench.appendToolbar('Modeling2DPro', cmdProjectSet)
    # workbench.appendToolbar('工具', modelBoolList)
    cmdProjectSettinglst = ["CreateModelInfo", "CreateNetStepSetting", "CreateDataExportSetting",
                        "CreateRunProcessingOptions","CustomeParameterMainCommand" ]

    workbench.appendToolbar('常用体', cmd2DCommon)
    workbench.appendToolbar('复杂体', cmd2DComplex)
    workbench.appendToolbar('工具', modelBoolList)

    workbench.appendToolbar('边界设置', cmd2DBoundary)
    workbench.appendToolbar('发射设置', cmd2DEmit)
    workbench.appendToolbar('观测设置', cmd2DObserve)
    workbench.appendToolbar('工程设置',cmdProjectSettinglst)
    workbench.appendToolbar('定时器设置', cmd2DTimer)
    workbench.appendToolbar('其他设置', otherSetting)
    # workbench.appendToolbar('工程设置',paramList)
    workbench.appendToolbar('约束工具', cmdSnapList)

    vcmdlst = ["Vis_Grid",
                  "Vis_Labels",
                  "Vis_Series",
                  "Vis_Point",
                  "Vis_Axes",
                  "Vis_Geometric_Ratio",
                  "Vis_Struct_grid"]
    workbench.appendToolbar('后处理',vcmdlst)
