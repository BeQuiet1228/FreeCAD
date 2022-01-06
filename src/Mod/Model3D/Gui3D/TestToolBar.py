# -*- coding: utf8 -*-

def Load(workbench):
    cmd_3D = ['CreatePoint_3D', 'CreateLineOblique_3D', 'CreateLineConformal_3D', 'CreateAreaConformal_3D',
             'CreateAreaFunction_3D', 'CreateAreaRectangle_3D', 'CreatePolygonal_3D']
    # 布尔运算和m3d   'UpdateBooleanCommand_3D', 'CreateM3D_new'

    cmdCommon_3D = ['CreateVolConformal_3D', 'CreateVolAnnular_3D', 'Create_3D_Cylinder', 'Create_3D_SpecialCone',
                   'CreateVolSpherical_3D', 'CreateVolToroidal_Section_3D', 'CreateVolParallelepipedal_3D',
                   'CreateVolAnnular_Section_3D', 'CreateVolFunction_3D']

    cmdSpecial_3D = ['CreateVolPyramid_3D', 'Create_3D_Wedge', 'CreateVolRhombus_3D', 'Create3DExtruded',
                    'Create_3D_Tetrahedron', 'CreateVolHelical_3D']

    # 草图旋转体暂时隐藏'CreateDraftRevolution_3D',
    cmd3dComplex_3D = ['CreateVolRevolution_3D', 'CreateDraftExtruded_3D',
                       'CreateObjectArray_3D', 'CreateVolArray']

    clip = ['Clip_3D']

    otherSetting_3D = ['CreateNewMaterial_3D', 'CreateFieldSetting_3D', 'TimeDomainSetting_3D', 'CreateMacroParticle_3D',
                    'CreateParticleDefine_3D', "CreateMark"]

    cmdBoundary_3D = ['CreatePort_3D', 'Create3DFreeSpace', 'Create3DSymtry','CreateSolend_3D',
                     'Create_3D_Foil', 'Create3D_Driv', 'CreateInductor_3D']

    cmdEmit_3D = ['CreateBeam_3D', 'CreateExps_3D', 'CreateGyro_3D', 'CreateFeld_3D', 'CreateTher_3D',
                        'CreateSecd_3D', 'Create3D_Popu', 'CreateIoni_3D']

    cmdObserve_3D = ['CreateObserve_3D', 'CreateCntr_3D', 'CreateAreaRan_3D', 'CreatePhasSpace_3D', 'CreateVector_3D']

    cmdTimer_3D = ['CreateDefTimer_3D', 'CreateCustomTimer_3D']

    cmdProjectSettinglst_3D = ['CreateModelingInfo', 'NetStepSetting_3D', 'CreateDataProcessingSetting',
                            'CreateRunOptions', 'Std_My_Parameter']

    view = ["Std_ViewAxo", "Separator", "Std_ViewFront", "Std_ViewTop", "Std_ViewRight",
            "Separator", "Std_ViewRear", "Std_ViewBottom", "Std_ViewLeft", "Separator", "Std_MeasureDistance"]

    workbench.appendToolbar('视图', view)
    workbench.appendToolbar('点线面', cmd_3D)
    workbench.appendToolbar('常用体', cmdCommon_3D)
    workbench.appendToolbar('特殊体', cmdSpecial_3D)
    workbench.appendToolbar('复杂体', cmd3dComplex_3D)
    workbench.appendToolbar('工具', clip)
    workbench.appendToolbar('边界设置', cmdBoundary_3D)
    workbench.appendToolbar('发射设置', cmdEmit_3D)
    workbench.appendToolbar('观测设置', cmdObserve_3D)
    workbench.appendToolbar('工程设置', cmdProjectSettinglst_3D)
    workbench.appendToolbar('定时器设置', cmdTimer_3D)
    workbench.appendToolbar('其他设置', otherSetting_3D)
