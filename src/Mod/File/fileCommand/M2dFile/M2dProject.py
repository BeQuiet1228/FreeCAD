# -*- coding:utf-8 -*-
# @Time: 2020/11/10 14:35
# @Author: lilei
# @File: M2dProject.py

import M2dObject
import FreeCAD
import re

from Modeling.Modeling2D.Tools import Tools2D

blankSpace = " "
semicolon = ";"
newLine = "\n"
tab = "\t"
comma = ","

# 定时器暂存字典
Timer_dict = {u'默认定时器': 'DefTimer',
              u'仅开始时刻': 'TSYS$FIRST',
              u'仅结束时刻': 'TSYS$LAST',
              u'TSYS$EIGEN': 'TSYS$EIGEN',
              u'TSYS$EIGENMODE': 'TSYS$EIGENMODE',
              u'TSYS$ENERGY': 'TSYS$ENERGY'}


def ModelInfo(obj):
    """
        模型信息输入
        返回：temp_m2d_h
    """
    temp_m2d_h = ""
    temp_m2d_h += "HEADER" + blankSpace + "ORGANIZATION" + blankSpace + '"' + obj.organization + '"' + semicolon + newLine + \
                  "HEADER" + blankSpace + "AUTHOR" + blankSpace + '"' + obj.author + '"' + semicolon + newLine + \
                  "HEADER" + blankSpace + "DEVICE" + blankSpace + '"' + obj.model + '"' + semicolon + newLine + \
                  "HEADER" + blankSpace + "REMARKS" + blankSpace + '"' + obj.remark + '"' + semicolon + newLine
    return temp_m2d_h


def NetStep(obj):
    """
        网络步长
        返回值：temp_m2d_gg
                temp_m2d_p
    """
    temp_m2d_gg = ""
    temp_m2d_p = ""

    temp_m2d_p += "DX1" + blankSpace + "=" + blankSpace + obj.stepSizeX + semicolon + newLine + newLine
    temp_m2d_p += "DX2" + blankSpace + "=" + blankSpace + obj.stepSizeY + semicolon + newLine
    
    if obj.isStartUsing:
        temp_m2d_gg += "AREA " + blankSpace + obj.Label + blankSpace + "CONFORMAL"
        temp_m2d_gg += M2dObject.PointCoordinates().point1(obj)
        temp_m2d_gg += M2dObject.PointCoordinates().point2(obj) + semicolon + newLine
        temp_m2d_gg += "MARK" + blankSpace + obj.Label + blankSpace + "X1" + blankSpace + "SIZE" + blankSpace + \
                       "DX1" + semicolon + newLine
        temp_m2d_gg += "MARK" + blankSpace + obj.Label + blankSpace + "X2" + blankSpace + "SIZE" + blankSpace + \
                       "DX2" + semicolon + newLine + newLine

    # else:
    #     temp_m2d_p += "DX1" + blankSpace + "=" + blankSpace + obj.stepSizeX + semicolon + newLine + newLine
    #     temp_m2d_p += "DX2" + blankSpace + "=" + blankSpace + obj.stepSizeY + semicolon + newLine + newLine

    return temp_m2d_p, temp_m2d_gg


def NewMaterial(obj):
    """
        新型材料
        中间变量：temp_m2d
        返回值：temp_m2d_cp
    """
    temp_m2d_cp = ""
    temp_m2d = ""

    temp_m2d += "MATERIAL" + blankSpace + obj.Label + blankSpace + "ATOMIC_NUMBER" + blankSpace + obj.AtomicNumber + \
                blankSpace + "ATOMIC_MASS" + blankSpace + obj.AtomicMassNumber + blankSpace + "MASS_DENSITY" + \
                blankSpace + obj.MaterialDensity
    temp_m2d_cp += temp_m2d + semicolon + newLine

    if obj.isConductivity and (not obj.isDielectricConstant):
        temp_m2d_cp += temp_m2d + blankSpace + "CONDUCTIVITY" + blankSpace + obj.conductivity + semicolon + newLine
    if obj.isDielectricConstant and (not obj.isConductivity):
        temp_m2d_cp += temp_m2d + blankSpace + "PERMITTIVITY" + blankSpace + obj.dielectricConstant + \
                       semicolon + newLine
    if obj.isConductivity and obj.isDielectricConstant:
        temp_m2d_cp += temp_m2d + blankSpace + "CONDUCTIVITY" + blankSpace + obj.conductivity + blankSpace + \
                       "PERMITTIVITY" + blankSpace + obj.dielectricConstant + semicolon + newLine
    return temp_m2d_cp


def Filed(obj):
    """
        场及函数定义
        返回值：temp_m2d_cp
    """
    temp_m2d_cp = ""
    temp_m2d_cp += obj.self_definingFunction
    # 修改与坐标系相关的函数参数
    FB1ST = ""
    FB2ST = ""
    FE1ST = ""
    FE2ST = ""
    functionParameters = ""
    coodinate = FreeCAD.ActiveDocument.CoordinateSystem
    if coodinate == u'Rectangular' or coodinate == 'Rectangular':
        FB1ST = "FBXST"
        FB2ST = "FBYST"
        FE1ST = "FEXST"
        FE2ST = "FEYST"
        functionParameters = "(X,Y)"
    elif coodinate == u'Polar' or coodinate == 'Polar':
        pass
    elif coodinate == u'Cylindrical' or coodinate == 'Cylindrical':
        FB1ST = "FBZST"
        FB2ST = "FBRST"
        FE1ST = "FEZST"
        FE2ST = "FERST"
        functionParameters = "(Z,R)"
    else:
        Tools2D.sayz("请选择正确的坐标系")

    if obj.isMagnetostaticFieldX:
        # 作此判断的目的是在整体生成m2d时，不会多一行
        if len(temp_m2d_cp) != 0:
            temp_m2d_cp += newLine
        temp_m2d_cp += "FUNCTION" + blankSpace + FB1ST + functionParameters + blankSpace + "=" + blankSpace + \
                       obj.magnetostaticFieldX + semicolon + newLine
        temp_m2d_cp += "PRESET" + blankSpace + "B1ST" + blankSpace + "FUNCTION" + blankSpace + \
                       FB1ST + semicolon
    if obj.isMagnetostaticFieldY:
        if len(temp_m2d_cp) != 0:
            temp_m2d_cp += newLine
        temp_m2d_cp += "FUNCTION" + blankSpace + FB2ST + functionParameters + blankSpace + "=" + blankSpace + \
                       obj.magnetostaticFieldY + semicolon + newLine
        temp_m2d_cp += "PRESET" + blankSpace + "B2ST" + blankSpace + "FUNCTION" + blankSpace + \
                       FB2ST + semicolon
    if obj.isElectrostaticFieldX:
        if len(temp_m2d_cp) != 0:
            temp_m2d_cp += newLine
        temp_m2d_cp += "FUNCTION" + blankSpace + FE1ST + functionParameters + blankSpace + "=" + blankSpace + \
                       obj.electrostaticFieldX + semicolon + newLine
        temp_m2d_cp += "PRESET" + blankSpace + "E1ST" + blankSpace + "FUNCTION" + blankSpace + \
                       FE1ST + semicolon
    if obj.isElectrostaticFieldY:
        if len(temp_m2d_cp) != 0:
            temp_m2d_cp += newLine
        temp_m2d_cp += "FUNCTION" + blankSpace + FE2ST + functionParameters + blankSpace + "=" + blankSpace + \
                       obj.electrostaticFieldY + semicolon + newLine
        temp_m2d_cp += "PRESET" + blankSpace + "E2ST" + blankSpace + "FUNCTION" + blankSpace + \
                       FE2ST + semicolon + newLine
    return temp_m2d_cp


def TimeDomain(obj):
    """
        时间域计算设定
        返回值：temp_m2d_ss
    """
    temp_m2d_ss = ""

    # 场算法字典
    fieldAlgorithm_dict = {u'中心差分FDTD': 'CENTERED',
                           u'时偏FDTD': 'BIASED',
                           u'高Q值FDTD': 'HIGH_Q'}

    # 模块临时变量
    SettingPattern_temp = ""
    SetStep_temp = ""
    SetAlgorithm_temp = ""
    TimeStepInterval_temp = ""

    # 是否选中计算时间步长
    if obj.isParticleCalculatesTimeStepInterval:
        if obj.isNonrelativistic:
            TimeStepInterval_temp = "KINEMATICS" + blankSpace + obj.particleCalculatesTimeStepInterval + blankSpace + \
                                    "NONRELATIVISTIC"
        else:
            TimeStepInterval_temp += "KINEMATICS" + blankSpace + obj.particleCalculatesTimeStepInterval + blankSpace + \
                                     "RELATIVISTIC"
        temp_m2d_ss += '{}'.format(TimeStepInterval_temp) + semicolon + newLine

    temp_m2d_ss += "MAXWELL" + blankSpace + fieldAlgorithm_dict.get(obj.fieldAlgorithm) + semicolon + newLine
    # temp_m2d_ss += "DURATION" + blankSpace + obj.computationTime + "NANOSECOND" + semicolon + newLine

    # 是否开启设置模式
    if obj.isSettingPattern:
        if obj.isEM:
            SettingPattern_temp = "MODE" + blankSpace + "BOTH"
        if obj.isTE:
            SettingPattern_temp = "MODE" + blankSpace + "TE"
        if obj.isTM:
            SettingPattern_temp = "MODE" + blankSpace + "TM"
        temp_m2d_ss += '{}'.format(SettingPattern_temp) + semicolon + newLine
    # 是否设置步长
    if obj.isSetStep:
        # 设置步长如果是变量，不加NANOSECOND
        if str(obj.setStep).replace('.', '').isdigit():
            SetStep_temp = "TIME_STEP" + blankSpace + obj.setStep + "NANOSECOND"
        else:
            SetStep_temp = "TIME_STEP" + blankSpace + obj.setStep
        temp_m2d_ss += '{}'.format(SetStep_temp) + semicolon + newLine
    # 是否设置电荷连续性
    if obj.isSetAlgorithm:
        SetAlgorithm_temp = "CONTINUITY" + blankSpace + "CONSERVED"
        temp_m2d_ss += '{}'.format(SetAlgorithm_temp) + semicolon + newLine
    # # 是否选中计算时间步长
    # if obj.isParticleCalculatesTimeStepInterval:
    #     if obj.isNonrelativistic:
    #         TimeStepInterval_temp = "KINEMATICS" + blankSpace + obj.particleCalculatesTimeStepInterval + blankSpace + \
    #                                 "NONRELATIVISTIC"
    #     else:
    #         TimeStepInterval_temp += "KINEMATICS" + blankSpace + obj.particleCalculatesTimeStepInterval + blankSpace + \
    #                                  "RELATIVISTIC"
    #     temp_m2d_ss += '{}'.format(TimeStepInterval_temp) + semicolon + newLine
    # 计算时间如果是变量，不加NANOSECOND
    if str(obj.computationTime).replace('.', '').isdigit():
        temp_m2d_ss += "DURATION" + blankSpace + obj.computationTime + "NANOSECOND" + semicolon + newLine
    else:
        temp_m2d_ss += "DURATION" + blankSpace + obj.computationTime + semicolon + newLine

    return temp_m2d_ss


def DataExport(obj):
    """
        数据导出设置
        返回值：temp_m2d_do
    """
    temp_m2d_do = ""
    temp_m2d_do += "DUMP NAME Unnamed_TIME;" + newLine
    if obj.isTextFormat:
        temp_m2d_do += "DUMP" + blankSpace + "FORMAT" + blankSpace + "ASCII" + semicolon + newLine
    elif obj.isBinaryFormat:
        temp_m2d_do += "DUMP" + blankSpace + "FORMAT" + blankSpace + "BINARY" + semicolon + newLine

    if obj.isTimeObservation:
        temp_m2d_do += "DUMP" + blankSpace + "TYPE" + blankSpace + "OBSERVE" + semicolon + newLine
    if obj.isSpaceObservation:
        temp_m2d_do += "DUMP" + blankSpace + "TYPE" + blankSpace + "RANGE" + semicolon + newLine
    if obj.isAllelicChartData:
        temp_m2d_do += "DUMP" + blankSpace + "TYPE" + blankSpace + "CONTOUR" + semicolon + newLine
    if obj.isVectorGraphData:
        temp_m2d_do += "DUMP" + blankSpace + "TYPE" + blankSpace + "VECTOR" + semicolon + newLine
    if obj.isPhaseSpatialData:
        temp_m2d_do += "DUMP" + blankSpace + "TYPE" + blankSpace + "PHASESPACE" + semicolon + newLine
    if obj.isSetFilePrefix:
        temp_m2d_do += "DUMP" + blankSpace + "PREFIX" + blankSpace + '"' + obj.setFilePrefix + '"' + semicolon + newLine
    if obj.isFileSuffixes:
        temp_m2d_do += "DUMP" + blankSpace + "SUFFIX" + blankSpace + '"' + obj.fileSuffixes + '"' + semicolon + newLine

    return temp_m2d_do


def RunProcessing(obj):
    """
        运行处理选项
        返回值：temp_m2d_ro
    """
    temp_m2d_ro = ""
    if obj.isHaltedState:
        temp_m2d_ro += "GRAPHICS" + blankSpace + "PAUSE" + semicolon + newLine
    if obj.isDisplayStructureDrawing:
        temp_m2d_ro += "DISPLAY" + semicolon + newLine
    return temp_m2d_ro


def NewParticle(obj):
    """
        新型粒子
        返回值：temp_m2d_cp
    """
    temp_m2d_cp = ""
    if obj.protonMassUnit == "PROTON":
        temp_m2d_cp += "SPECIES" + blankSpace + obj.Label + blankSpace + "CHARGE" + blankSpace + obj.powerUnit + \
                       blankSpace + "MASS" + blankSpace + obj.mass + blankSpace + "PROTON" + semicolon + newLine
    if obj.protonMassUnit == "ELECTRON":
        temp_m2d_cp += "SPECIES" + blankSpace + obj.Label + blankSpace + "CHARGE" + blankSpace + obj.powerUnit + \
                       blankSpace + "MASS" + blankSpace + obj.mass + blankSpace + "ELECTRON" + semicolon + newLine
    if obj.protonMassUnit == "AMU":
        temp_m2d_cp += "SPECIES" + blankSpace + obj.Label + blankSpace + "CHARGE" + blankSpace + obj.powerUnit + \
                       blankSpace + "MASS" + blankSpace + obj.mass + blankSpace + "AMU" + semicolon + newLine
    return temp_m2d_cp


def MacParticle(obj):
    """
        宏粒子合并
        返回值：temp_m2d_ss
    """
    temp_m2d_ss = ""
    if obj.isMacroParticle:
        # if obj.typeOfParticles == "ALL":
        #     temp_m2d_ss += "MERGE" + blankSpace + "SPECIES" + blankSpace + "ALL" + blankSpace + "MAXN_PERCELL" + \
        #                    blankSpace + obj.particleNumber + blankSpace + "MAXN_WHOLE" + blankSpace + \
        #                    obj.macroParticleNumber + semicolon + newLine
        # if obj.typeOfParticles == "IONS":
        #     temp_m2d_ss += "MERGE" + blankSpace + "SPECIES" + blankSpace + "IONS" + blankSpace + "MAXN_PERCELL" + \
        #                    blankSpace + obj.particleNumber + blankSpace + "MAXN_WHOLE" + blankSpace + \
        #                    obj.macroParticleNumber + semicolon + newLine
        # if obj.typeOfParticles == "PROTON":
        #     temp_m2d_ss += "MERGE" + blankSpace + "SPECIES" + blankSpace + "PROTON" + blankSpace + "MAXN_PERCELL" + \
        #                    blankSpace + obj.particleNumber + blankSpace + "MAXN_WHOLE" + blankSpace + \
        #                    obj.macroParticleNumber + semicolon + newLine
        # if obj.typeOfParticles == "ELECTRON":
        #     temp_m2d_ss += "MERGE" + blankSpace + "SPECIES" + blankSpace + "ELECTRON" + blankSpace + "MAXN_PERCELL" + \
        #                    blankSpace + obj.particleNumber + blankSpace + "MAXN_WHOLE" + blankSpace + \
        #                    obj.macroParticleNumber + semicolon + newLine
        temp_m2d_ss += "MERGE" + blankSpace + "SPECIES" + blankSpace + obj.typeOfParticles + blankSpace + "MAXN_PERCELL" + \
                       blankSpace + obj.particleNumber + blankSpace + "MAXN_WHOLE" + blankSpace + \
                       obj.macroParticleNumber + semicolon + newLine
    else:
        pass
    return temp_m2d_ss


def Timer(obj):
    """
        定时器
        返回值：temp_m2d_ap 
    """
    temp_m2d_ap = ""

    if obj.defTimerType == "周期型":
        if obj.isTimeSteps:
            temp_m2d_ap += "TIMER" + blankSpace + obj.Label + blankSpace + "PERIODIC" + blankSpace + "INTEGER" + \
                           blankSpace + obj.startTime + blankSpace + obj.endTime + blankSpace + obj.timeCycle + \
                           semicolon + newLine
        if obj.isSimulationSteps:
            temp_m2d_ap += "TIMER" + blankSpace + obj.Label + blankSpace + "PERIODIC" + blankSpace + "REAL" + \
                           blankSpace + obj.startTime + blankSpace + obj.endTime + blankSpace + obj.timeCycle + \
                           semicolon + newLine

    if obj.defTimerType == "离散型":
        if obj.isTimeSteps:
            temp_m2d_ap += "TIMER" + blankSpace + obj.Label + blankSpace + "DISCRETE" + blankSpace + "INTEGER" + \
                           blankSpace + obj.discreteTime + semicolon + newLine
        if obj.isSimulationSteps:
            temp_m2d_ap += "TIMER" + blankSpace + obj.Label + blankSpace + "DISCRETE" + blankSpace + "REAL" + \
                           blankSpace + obj.discreteTime + semicolon + newLine
    return temp_m2d_ap


def Cntr(obj):
    """
        Cntr
        返回值：
                temp_m2d
                temp_m2d_ap
    """
    temp_m2d = ""
    # temp_m2d += "AREA" + blankSpace + obj.Label + blankSpace + "CONFORMAL"
    # temp_m2d += M2dObject.PointCoordinates().point1(obj)
    # temp_m2d += M2dObject.PointCoordinates().point2(obj) + semicolon + newLine

    temp_m2d_ap = ""
    # 模块临时变量
    ProjectionLine_temp = ""
    Oline_temp = ""
    # 定时器
    Timer_name = ""
    # # 定时器暂存字典
    # Timer_dict = {u'默认定时器': 'DefTimer',
    #               u'仅开始时刻': 'TSYS$FIRST',
    #               u'仅结束时刻': 'TSYS$LAST'}
    # 因为定时器下拉框是动态的，不能定义为字典，这里改正
    if obj.timer == "默认定时器":
        Timer_name = "DefTimer"
    elif obj.timer == "仅开始时刻":
        Timer_name = "TSYS$FIRST"
    elif obj.timer == "仅结束时刻":
        Timer_name = "TSYS$LAST"
    else:
        Timer_name = obj.timer

    # 判断正交投影面是否指定
    if obj.orthogonalProjectionLine == "未指定":
        temp_m2d += "AREA" + blankSpace + obj.Label + blankSpace + "CONFORMAL"
        temp_m2d += M2dObject.PointCoordinates().point1(obj)
        temp_m2d += M2dObject.PointCoordinates().point2(obj) + semicolon + newLine
        ProjectionLine_temp = "CONTOUR" + blankSpace + "FIELD" + blankSpace + obj.observationField + \
                              blankSpace + obj.Label
    else:
        ProjectionLine_temp = "CONTOUR" + blankSpace + "FIELD" + blankSpace + obj.observationField + blankSpace + \
                              obj.orthogonalProjectionLine
    # 是否选中等值线填充
    if obj.isoline:
        Oline_temp = blankSpace + "SHADE"

    temp_m2d_ap += '%s %s%s' % (ProjectionLine_temp, Timer_name, Oline_temp) + semicolon + newLine
    return temp_m2d, temp_m2d_ap


def Vector(obj):
    """
        vector
        返回值：temp_m2d
                temp_m2d_ap

    """
    temp_m2d = ""
    # temp_m2d += "AREA" + blankSpace + obj.Label + blankSpace + "CONFORMAL"
    # temp_m2d += M2dObject.PointCoordinates().point1(obj)
    # temp_m2d += M2dObject.PointCoordinates().point2(obj) + semicolon + newLine

    temp_m2d_ap = ""
    # 模块临时变量
    ProjectionLine_temp = ""
    VectorNumber_temp = ""
    Timer_name = ""
    # # 定时器
    # Timer_dict = {u'默认定时器': 'DefTimer',
    #               u'仅开始时刻': 'TSYS$FIRST',
    #               u'仅结束时刻': 'TSYS$LAST'}
    # 因为定时器下拉框是动态的，不能定义为字典，这里改正
    if obj.timer == "默认定时器":
        Timer_name = "DefTimer"
    elif obj.timer == "仅开始时刻":
        Timer_name = "TSYS$FIRST"
    elif obj.timer == "仅结束时刻":
        Timer_name = "TSYS$LAST"
    else:
        Timer_name = obj.timer

    # 是否指定正交投影面
    if obj.orthogonalProjectionLine == "未指定":
        temp_m2d += "AREA" + blankSpace + obj.Label + blankSpace + "CONFORMAL"
        temp_m2d += M2dObject.PointCoordinates().point1(obj)
        temp_m2d += M2dObject.PointCoordinates().point2(obj) + semicolon + newLine
        ProjectionLine_temp = "VECTOR" + blankSpace + "FIELD" + blankSpace + obj.observationField1 + comma + \
                              obj.observationField2 + blankSpace + obj.Label
    else:
        ProjectionLine_temp = "VECTOR" + blankSpace + "FIELD" + blankSpace + obj.observationField1 + comma + \
                              obj.observationField2 + blankSpace + obj.orthogonalProjectionLine
    # 是否指定矢量个数
    if obj.isVectorNumber:
        VectorNumber_temp = blankSpace + "NUMBER" + blankSpace + obj.vectorNumber1 + blankSpace + obj.vectorNumber2

    temp_m2d_ap += '%s %s%s' % (ProjectionLine_temp, Timer_name, VectorNumber_temp) + semicolon + newLine
    return temp_m2d, temp_m2d_ap


def PhasSpace(obj):
    """
        PhasSpace
        返回值：temp_m2d_ap
    """
    temp_m2d_ap = ""
    temp_m2d_use = ""
    temp_m2d_use += "PHASESPACE" + blankSpace + "AXES" + blankSpace + obj.horizontalAxisShow + comma + \
                    obj.verticalAxisShow + blankSpace

    # 模块临时变量
    Particle_temp = ""
    Thickness_temp = ""
    Suffix_temp = ""
    Timer_name = ""
    # 因为定时器下拉框是动态的，不能定义为字典，这里改正
    if obj.timer == "默认定时器":
        Timer_name = "DefTimer"
    elif obj.timer == "仅开始时刻":
        Timer_name = "TSYS$FIRST"
    elif obj.timer == "仅结束时刻":
        Timer_name = "TSYS$LAST"
    else:
        Timer_name = obj.timer

        # 观测粒子
    # Particle_dict = {u'电子': 'SPECIES ELECTRON',
    #                  u'质子': 'SPECIES PROTON'}
    if obj.observationParticle == u'全部':
        Particle_temp = ""
    elif obj.observationParticle == u'电子':
        Particle_temp = blankSpace + "SPECIES ELECTRON"
    elif obj.observationParticle == u'质子':
        Particle_temp = blankSpace + "SPECIES PROTON"
    else:
        Particle_temp = blankSpace + "SPECIES " + obj.observationParticle

    # if obj.observationParticle in Particle_dict.keys():
    #     Particle_temp = blankSpace + Particle_dict.get(obj.observationParticle)

    # 是否显示厚度
    if obj.isShowThickness:
        Thickness_temp = blankSpace + "WINDOW" + obj.showThick + blankSpace + obj.thickValue1 + \
                         blankSpace + obj.thickValue2

    # 是否选中后缀
    if obj.isSuffix:
        Suffix_temp = blankSpace + "SUFFIX" + blankSpace + obj.suffix

    temp_m2d_ap += temp_m2d_use + '%s%s%s%s' % (Timer_name, Particle_temp, Thickness_temp, Suffix_temp) +\
                   semicolon + newLine

    return temp_m2d_ap


def AreaRan(obj):
    """
        AreaRan:空间观测
        返回值：temp_m2d
                temp_m2d_ap
    """
    temp_m2d = ""
    # temp_m2d += "LINE" + blankSpace + obj.Label + blankSpace + "CONFORMAL"
    # temp_m2d += M2dObject.PointCoordinates().point1(obj)
    # temp_m2d += M2dObject.PointCoordinates().point2(obj) + semicolon + newLine

    # 模块临时变量
    temp_m2d_ap = ""
    Field_temp = ""
    FieldIntegral_temp = ""
    FieldPower_temp = ""
    FieldEnergy_temp = ""
    FFT_temp = ""
    Timer_name = ""
    # 因为定时器下拉框是动态的，不能定义为字典，这里改正
    if obj.timer == "默认定时器":
        Timer_name = "DefTimer"
    elif obj.timer == "仅开始时刻":
        Timer_name = "TSYS$FIRST"
    elif obj.timer == "仅结束时刻":
        Timer_name = "TSYS$LAST"
    else:
        Timer_name = obj.timer

    # 场、场积分、场功率、场能量
    if obj.orthogonalProjectionLine == "未指定":
        temp_m2d += "LINE" + blankSpace + obj.Label + blankSpace + "CONFORMAL"
        temp_m2d += M2dObject.PointCoordinates().point1(obj)
        temp_m2d += M2dObject.PointCoordinates().point2(obj) + semicolon + newLine
        if obj.isField:
            Field_temp = "RANGE" + blankSpace + "FIELD" + blankSpace + obj.field + blankSpace + obj.Label
        if obj.isFieldIntegral:
            FieldIntegral_temp = "RANGE" + blankSpace + "FIELD_INTEGRAL" + blankSpace + obj.fieldIntegral + blankSpace + obj.Label
        if obj.isFieldPower:
            FieldPower_temp = "RANGE" + blankSpace + "FIELD_POWER" + blankSpace + obj.fieldPower + blankSpace + obj.Label
        if obj.isFieldEnergy:
            FieldEnergy_temp = "RANGE" + blankSpace + "FIELD_ENERGY" + blankSpace + obj.fieldEnergy + \
                               blankSpace + obj.Label

    else:
        if obj.isField:
            Field_temp = "RANGE" + blankSpace + "FIELD" + blankSpace + obj.field + blankSpace + obj.orthogonalProjectionLine
        if obj.isFieldIntegral:
            FieldIntegral_temp = "RANGE" + blankSpace + "FIELD_INTEGRAL" + blankSpace + obj.fieldIntegral + blankSpace + \
                                 obj.orthogonalProjectionLine
        if obj.isFieldPower:
            FieldPower_temp = "RANGE" + blankSpace + "FIELD_POWER" + blankSpace + obj.fieldPower + blankSpace + \
                              obj.orthogonalProjectionLine
        if obj.isFieldEnergy:
            FieldEnergy_temp = "RANGE" + blankSpace + "FIELD_ENERGY" + blankSpace + obj.fieldEnergy + blankSpace + \
                               obj.orthogonalProjectionLine

    # 是否选中傅里叶变换
    if obj.isFFT:
        if obj.isRealAnalysis:
            FFT_temp = blankSpace + "FFT" + blankSpace + "MAGNITUDE"
        if obj.isComplexAnalysis:
            FFT_temp = blankSpace + "FFT" + blankSpace + "COMPLEX"

    if not hasattr(obj, "isParticle"):
        from Modeling.Modeling2D.Modeling2DCommand.AreaRan import AreaRanInstance
        AreaRanInstance.completionProperties(obj)

    if not obj.isParticle:
        temp_m2d_ap += '%s%s%s%s %s%s' % (Field_temp, FieldIntegral_temp, FieldPower_temp, FieldEnergy_temp,
                                          Timer_name, FFT_temp) + semicolon + newLine
    else:
        temp_m2d = ""
        temp_m2d_ap += "RANGE" + blankSpace + "PARTICLE" + blankSpace + obj.chooseParticle + blankSpace + \
                       obj.particleType + blankSpace + obj.particleAxis + blankSpace + Timer_name + semicolon + newLine

    return temp_m2d, temp_m2d_ap


def Observe(obj):
    """
        Observe :时间观测
        返回值：temp_m2d
                temp_m2d_ap
    """
    temp_m2d = ""
    # if obj.ObservationType == "时间观测点":
    #     temp_m2d += "POINT" + blankSpace + obj.Label + blankSpace + obj.point1_X+\
    #                 blankSpace+obj.point1_Y+semicolon+newLine
    #     # temp_m2d += M2dObject.PointCoordinates().point1(obj)
    #     # temp_m2d += M2dObject.PointCoordinates().point2(obj) + semicolon + newLine
    # elif obj.ObservationType == "时间观测线":
    #     temp_m2d += "LINE" + blankSpace + obj.Label + blankSpace + "CONFORMAL"
    #     temp_m2d += M2dObject.PointCoordinates().point1(obj)
    #     temp_m2d += M2dObject.PointCoordinates().point2(obj) + semicolon + newLine
    # elif obj.ObservationType == "时间观测面":
    #     temp_m2d += "AREA" + blankSpace + obj.Label + blankSpace + "CONFORMAL"
    #     temp_m2d += M2dObject.PointCoordinates().point1(obj)
    #     temp_m2d += M2dObject.PointCoordinates().point2(obj) + semicolon + newLine

    temp_m2d_ap = ""
    # 模块临时变量
    Field_temp = ""
    ParticleStatistics_temp = ""
    CollectedParticles_temp = ""
    EmittedParticle_temp = ""
    AnnihilatingParticle_temp = ""
    FFT_temp = ""
    TimeRange_temp = ""
    ObservationInterval_temp = ""
    DataDisplay_temp = ""
    Alias_temp = ""
    FieldIntegral_temp = ""
    FieldPower_temp = ""
    FieldEnergy_temp = ""

    # 别名
    if obj.alias:
        Alias_temp = blankSpace + "suffix" + blankSpace + obj.alias

    # 分类项
    if obj.optionType == "未指定":
        if obj.ObservationType == "时间观测点":
            temp_m2d += "POINT" + blankSpace + obj.Label + blankSpace + obj.point1_X + \
                        blankSpace + obj.point1_Y + semicolon + newLine
            if obj.isField:
                Field_temp = "OBSERVE" + blankSpace + "FIELD" + blankSpace + obj.field + blankSpace + obj.Label
            if obj.isParticleStatistics:
                if obj.particles2 == "EMIT_EPS":
                    ParticleStatistics_temp = "OBSERVE" + blankSpace + "PARTICLE_STATISTICS" + blankSpace \
                                              + obj.particles2 + blankSpace + obj.particles1 + blankSpace + obj.Label
                else:
                    ParticleStatistics_temp = "OBSERVE" + blankSpace + "PARTICLE_STATISTICS" + \
                                              blankSpace + obj.particles2 + blankSpace + obj.particles4 + \
                                              blankSpace + obj.Label
            if obj.isCollectedParticles:
                CollectedParticles_temp = "OBSERVE" + blankSpace + "COLLECTED" + blankSpace + \
                                          obj.particles3 + blankSpace + obj.particles4 + blankSpace + obj.Label
            if obj.isEmittedParticle:
                EmittedParticle_temp = "OBSERVE" + blankSpace + "EMITTED" + blankSpace + obj.particles3 + \
                                       blankSpace + obj.particles4 + blankSpace + obj.Label
            if obj.isAnnihilatingParticle:
                AnnihilatingParticle_temp = "OBSERVE" + blankSpace + "DESTROYED" + blankSpace + \
                                            obj.particles3 + blankSpace + obj.particles4 + blankSpace + obj.Label

        elif obj.ObservationType == "时间观测线":
            temp_m2d += "LINE" + blankSpace + obj.Label + blankSpace + "CONFORMAL"
            temp_m2d += M2dObject.PointCoordinates().point1(obj)
            temp_m2d += M2dObject.PointCoordinates().point2(obj) + semicolon + newLine
            if obj.isField:
                Field_temp = "OBSERVE" + blankSpace + "FIELD" + blankSpace + obj.field + \
                             blankSpace + obj.Label
            if obj.isFieldIntegral:
                FieldIntegral_temp = "OBSERVE" + blankSpace + "FIELD_INTEGRAL" + blankSpace + \
                                     obj.fieldIntegral + blankSpace + obj.Label
            if obj.isFieldPower:
                FieldPower_temp = "OBSERVE" + blankSpace + "FIELD_POWER" + blankSpace + obj.fieldPower + \
                                    blankSpace + obj.Label

            if obj.isParticleStatistics:
                if obj.particles2 == "EMIT_EPS":
                    ParticleStatistics_temp = "OBSERVE" + blankSpace + "PARTICLE_STATISTICS" + blankSpace \
                                              + obj.particles2 + blankSpace + obj.particles1 + blankSpace + obj.Label
                else:
                    ParticleStatistics_temp = "OBSERVE" + blankSpace + "PARTICLE_STATISTICS" + blankSpace \
                                              + obj.particles2 + blankSpace + obj.particles4 + blankSpace + obj.Label
            if obj.isCollectedParticles:
                CollectedParticles_temp = "OBSERVE" + blankSpace + "COLLECTED" + blankSpace + \
                                          obj.particles3 + blankSpace + obj.particles4 + blankSpace + obj.Label
            if obj.isEmittedParticle:
                EmittedParticle_temp = "OBSERVE" + blankSpace + "EMITTED" + blankSpace + obj.particles3 + \
                                       blankSpace + obj.particles4 + blankSpace + obj.Label
            if obj.isAnnihilatingParticle:
                AnnihilatingParticle_temp = "OBSERVE" + blankSpace + "DESTROYED" + blankSpace + \
                                            obj.particles3 + blankSpace + obj.particles4 + blankSpace + obj.Label

        elif obj.ObservationType == "时间观测面":
            temp_m2d += "AREA" + blankSpace + obj.Label + blankSpace + "CONFORMAL"
            temp_m2d += M2dObject.PointCoordinates().point1(obj)
            temp_m2d += M2dObject.PointCoordinates().point2(obj) + semicolon + newLine
            if obj.isField:
                Field_temp = "OBSERVE" + blankSpace + "FIELD" + blankSpace + obj.field + \
                             blankSpace + obj.Label

            # if obj.isFieldIntegral:
            #     FieldIntegral_temp = "OBSERVE" + blankSpace + "FIELD_INTEGRAL" + blankSpace + \
            #                          obj.fieldIntegral + blankSpace + obj.Label
            elif obj.isFieldPower:
                FieldPower_temp = "OBSERVE" + blankSpace + "FIELD_POWER" + blankSpace + obj.fieldPower + \
                                  blankSpace + obj.Label

            elif obj.isFieldEnergy:
                FieldEnergy_temp = "OBSERVE" + blankSpace + "FIELD_ENERGY" + blankSpace + obj.fieldEnergy + \
                                  blankSpace + obj.Label

            if obj.isParticleStatistics:
                if obj.particles2 == "EMIT_EPS":
                    ParticleStatistics_temp = "OBSERVE" + blankSpace + "PARTICLE_STATISTICS" + blankSpace \
                                              + obj.particles2 + blankSpace + obj.particles1 + blankSpace + obj.Label
                else:
                    ParticleStatistics_temp = "OBSERVE" + blankSpace + "PARTICLE_STATISTICS" + blankSpace \
                                              + obj.particles2 + blankSpace + obj.particles4 + blankSpace + obj.Label
            if obj.isCollectedParticles:
                CollectedParticles_temp = "OBSERVE" + blankSpace + "COLLECTED" + blankSpace + \
                                          obj.particles3 + blankSpace + obj.particles4 + blankSpace + obj.Label
            if obj.isEmittedParticle:
                EmittedParticle_temp = "OBSERVE" + blankSpace + "EMITTED" + blankSpace + obj.particles3 + \
                                       blankSpace + obj.particles4 + blankSpace + obj.Label
            if obj.isAnnihilatingParticle:
                AnnihilatingParticle_temp = "OBSERVE" + blankSpace + "DESTROYED" + blankSpace + \
                                            obj.particles3 + blankSpace + obj.particles4 + blankSpace + obj.Label

    else:
        if obj.ObservationType == "时间观测点":
            if obj.isField:
                Field_temp = "OBSERVE" + blankSpace + "FIELD" + blankSpace + obj.field + \
                             blankSpace + obj.optionType
            # if obj.isParticleStatistics:
            #     if obj.particles2 == "EMIT_EPS":
            #         ParticleStatistics_temp = "OBSERVE" + blankSpace + "PARTICLE_STATISTICS" + blankSpace \
            #                                   + obj.particles2 + blankSpace + obj.particles1 + blankSpace + obj.optionType
            #     else:
            #         ParticleStatistics_temp = "OBSERVE" + blankSpace + "PARTICLE_STATISTICS" + blankSpace +\
            #                                   obj.particles2 + blankSpace + obj.particles4 + blankSpace + obj.optionType
            # if obj.isCollectedParticles:
            #     CollectedParticles_temp = "OBSERVE" + blankSpace + "COLLECTED" + blankSpace + \
            #                               obj.particles3 + blankSpace + obj.particles4 + blankSpace + obj.optionType
            # if obj.isEmittedParticle:
            #     EmittedParticle_temp = "OBSERVE" + blankSpace + "EMITTED" + blankSpace + obj.particles3 + \
            #                            blankSpace + obj.particles4 + blankSpace + obj.optionType
            # if obj.isAnnihilatingParticle:
            #     AnnihilatingParticle_temp = "OBSERVE" + blankSpace + "DESTROYED" + blankSpace + \
            #                                 obj.particles3 + blankSpace + obj.particles4 + blankSpace + obj.optionType
        elif obj.ObservationType == "时间观测线":
            if obj.isField:
                Field_temp = "OBSERVE" + blankSpace + "FIELD" + blankSpace + obj.field + \
                             blankSpace + obj.optionType
            if obj.isFieldIntegral:
                FieldIntegral_temp = "OBSERVE" + blankSpace + "FIELD_INTEGRAL" + blankSpace + \
                                     obj.fieldIntegral + blankSpace + obj.optionType
            if obj.isFieldPower:
                FieldPower_temp = "OBSERVE" + blankSpace + "FIELD_POWER" + blankSpace + obj.fieldPower + \
                                  blankSpace + obj.optionType
            if obj.isParticleStatistics:
                if obj.particles2 == "EMIT_EPS":
                    ParticleStatistics_temp = "OBSERVE" + blankSpace + "PARTICLE_STATISTICS" + blankSpace \
                                              + obj.particles2 + blankSpace + obj.particles1 + blankSpace + obj.optionType
                else:
                    ParticleStatistics_temp = blankSpace + "OBSERVE" + blankSpace + "PARTICLE_STATISTICS" + blankSpace +\
                                              obj.particles2 + blankSpace + obj.particles4 + blankSpace + obj.optionType
            if obj.isCollectedParticles:
                CollectedParticles_temp = "OBSERVE" + blankSpace + "COLLECTED" + blankSpace + \
                                          obj.particles3 + blankSpace + obj.particles4 + blankSpace + obj.optionType
            if obj.isEmittedParticle:
                EmittedParticle_temp = "OBSERVE" + blankSpace + "EMITTED" + blankSpace + obj.particles3 + \
                                       blankSpace + obj.particles4 + blankSpace + obj.optionType
            if obj.isAnnihilatingParticle:
                AnnihilatingParticle_temp = "OBSERVE" + blankSpace + "DESTROYED" + blankSpace + \
                                            obj.particles3 + blankSpace + obj.particles4 + blankSpace + obj.optionType

        else:
            if obj.isField:
                Field_temp = "OBSERVE" + blankSpace + "FIELD" + blankSpace + obj.field + blankSpace + \
                             obj.optionType
            # if obj.isFieldIntegral:
            #     FieldIntegral_temp = "OBSERVE" + blankSpace + "FIELD_INTEGRAL" + blankSpace + \
            #                          obj.fieldIntegral + blankSpace + obj.Label
            if obj.isFieldPower:
                FieldPower_temp = "OBSERVE" + blankSpace + "FIELD_POWER" + blankSpace + obj.fieldPower + \
                                  blankSpace + obj.optionType
            if obj.isFieldEnergy:
                FieldEnergy_temp = "OBSERVE" + blankSpace + "FIELD_INTEGRAL" + blankSpace + \
                                     obj.fieldEnergy + blankSpace + obj.optionType

            if obj.isParticleStatistics:
                if obj.particles2 == "EMIT_EPS":
                    ParticleStatistics_temp = "OBSERVE" + blankSpace + "PARTICLE_STATISTICS" + blankSpace \
                                              + obj.particles2 + blankSpace + obj.particles1 + blankSpace + obj.optionType
                else:
                    ParticleStatistics_temp = "OBSERVE" + blankSpace + "PARTICLE_STATISTICS" + blankSpace \
                                              + obj.particles2 + blankSpace + obj.particles4 + blankSpace + obj.optionType
            if obj.isCollectedParticles:
                CollectedParticles_temp = "OBSERVE" + blankSpace + "COLLECTED" + blankSpace + \
                                          obj.particles3 + blankSpace + obj.particles4 + blankSpace + obj.optionType
            if obj.isEmittedParticle:
                EmittedParticle_temp = "OBSERVE" + blankSpace + "EMITTED" + blankSpace + obj.particles3 + \
                                       blankSpace + obj.particles4 + blankSpace + obj.optionType
            if obj.isAnnihilatingParticle:
                AnnihilatingParticle_temp = "OBSERVE" + blankSpace + "DESTROYED" + blankSpace + \
                                            obj.particles3 + blankSpace + obj.particles4 + blankSpace + obj.optionType
    temp_m2d_ap += '%s%s%s%s%s%s%s%s%s' % (Field_temp, FieldIntegral_temp, FieldPower_temp, FieldEnergy_temp,
                                           ParticleStatistics_temp, CollectedParticles_temp, EmittedParticle_temp,
                                           AnnihilatingParticle_temp, Alias_temp) + semicolon + newLine

    # 是否选中数据显示平滑处理
    if obj.isDataDisplay:
        if obj.isTimeAverage:
            DataDisplay_temp = blankSpace + "FILTER STEP" + blankSpace + obj.filteringTimeParameter + "NANOSECOND"
        if obj.isRcAnalyze:
            DataDisplay_temp = blankSpace + "FILTER LO_PASS" + blankSpace + obj.filteringTimeParameter + "NANOSECOND"

        temp_m2d_ap += '%s%s%s%s%s%s%s%s%s%s' % (Field_temp, FieldIntegral_temp, FieldPower_temp, FieldEnergy_temp,
                                                 ParticleStatistics_temp, CollectedParticles_temp, EmittedParticle_temp,
                                                 AnnihilatingParticle_temp,Alias_temp, DataDisplay_temp) + semicolon + newLine

    # 是否进行傅里叶变换
    if obj.isFFT:
        if obj.isRealAnalysis:
            FFT_temp = blankSpace + "FFT" + blankSpace + "MAGNITUDE"
            if obj.isFrequencyRange:
                FFT_temp = blankSpace + "FFT" + blankSpace + "MAGNITUDE" + blankSpace + "WINDOW FREQUENCY" + blankSpace + \
                           obj.frequencyRange1 + "GHZ" + blankSpace + obj.frequencyRange2 + "GHZ"
        if obj.isComplexAnalysis:
            FFT_temp = blankSpace + "FFT" + blankSpace + "COMPLEX"
            if obj.isFrequencyRange:
                FFT_temp = blankSpace + "FFT" + blankSpace + "COMPLEX" + blankSpace + "WINDOW FREQUENCY" + blankSpace + \
                           obj.frequencyRange1 + "GHZ" + blankSpace + obj.frequencyRange2 + "GHZ"
        temp_m2d_ap += '%s%s%s%s%s%s%s%s%s%s' % (Field_temp, FieldIntegral_temp, FieldPower_temp, FieldEnergy_temp,
                                                 ParticleStatistics_temp, CollectedParticles_temp, EmittedParticle_temp,
                                                 AnnihilatingParticle_temp, Alias_temp, FFT_temp) + semicolon + newLine

    # 是否选中时间范围
    if obj.isTimeRange:
        TimeRange_temp = blankSpace + "WINDOW TIME" + blankSpace + obj.timeRange1 + "NANOSECOND" + blankSpace + \
                         obj.timeRange2 + "NANOSECOND"

        temp_m2d_ap += '%s%s%s%s%s%s%s%s%s%s' % (Field_temp, FieldIntegral_temp, FieldPower_temp,FieldEnergy_temp,
                                                 ParticleStatistics_temp, CollectedParticles_temp, EmittedParticle_temp,
                                                 AnnihilatingParticle_temp, Alias_temp, TimeRange_temp) + semicolon + newLine
    # 是否选中观察间隔
    if obj.isObservationInterval:
        ObservationInterval_temp = blankSpace + "interval" + blankSpace + obj.observationInterval
        temp_m2d_ap += '%s%s%s%s%s%s%s%s%s%s' % (Field_temp, FieldIntegral_temp, FieldPower_temp,FieldEnergy_temp,
                                                 ParticleStatistics_temp, CollectedParticles_temp, EmittedParticle_temp,
                                                 AnnihilatingParticle_temp, Alias_temp, ObservationInterval_temp) + semicolon + newLine

    # # 是否选中数据显示平滑处理
    # if obj.isDataDisplay:
    #     if obj.isTimeAverage:
    #         DataDisplay_temp = blankSpace + "FILTER STEP" + blankSpace + obj.filteringTimeParameter + "NANOSECOND"
    #     if obj.isRcAnalyze:
    #         DataDisplay_temp = blankSpace + "FILTER LO_PASS" + blankSpace + obj.filteringTimeParameter + "NANOSECOND"
    #
    #     temp_m2d_ap += '%s%s%s%s%s%s%s%s%s' % (Field_temp, FieldIntegral_temp, FieldPower_temp, ParticleStatistics_temp,
    #                                            CollectedParticles_temp, EmittedParticle_temp, AnnihilatingParticle_temp,
    #                                            Alias_temp, DataDisplay_temp) + semicolon + newLine

    # temp_m2d_ap += '%s%s%s%s%s%s%s%s' % (Field_temp, FieldIntegral_temp, FieldPower_temp, ParticleStatistics_temp,
    #                                      CollectedParticles_temp, EmittedParticle_temp, AnnihilatingParticle_temp,
    #                                      Alias_temp) + semicolon + newLine

    return temp_m2d, temp_m2d_ap


# 获取全局变量列表
def getGlobalVariable():
    """
    return:[] globalVariableList 全局变量列表
    [[name,value]......]
    """
    # @fubiao
    globalVariableList = []
    # 定义变量的注释不能用canotBeStr
    canotBeStr = "! ==============================================================================!"
    replaceStr = "! =============================================================================!"

    paramText = FreeCAD.ActiveDocument.Company.replace(canotBeStr, replaceStr)
    # 将注释也加入m3d中，设置name="" val=注释内容
    commentList = re.findall(r"[!|！][^\n]*", paramText)

    # 将以叹号开始的一行替换为";param;",
    paramText = re.sub(r"[!|！][^\n]*", ";param;", paramText)
    paramText = paramText.replace(" ", "").replace("\n", "").replace("\r", "")

    paramList = paramText.split(";")
    # 遇到paramItem为param的时候，就读取一个commentList中的一个内容
    commentIndex = 0
    for paramItem in paramList:
        if paramItem == "param":
            globalVariableList.append([commentList[commentIndex], "!COMMENT"])
            commentIndex = commentIndex + 1
        else:
            paramNameAndValue = paramItem.split("=")
            if len(paramNameAndValue) >= 2:
                paramName = paramNameAndValue[0]
                paramNameLower = paramName.lower()
                if paramNameLower.startswith("function"):
                    if len(paramName) > 8:
                        paramName = paramName[:8].upper() + " " + paramName[8:]
                    else:
                        continue

                globalVariableList.append([paramName, paramNameAndValue[1]])
    return globalVariableList


def getParameterCommands(name, val):
    """
    :param name: 参数名
    :param content: 参数值
    :return:
    """
    # FreeCAD.Console.PrintMessage("LOG 1")
    # 表示为注释
    if val == "!COMMENT":
        return newLine + name + newLine
    if isNum(val):
        val = val.__str__()

    return name + " = " + val + ";" + newLine + newLine


def isNum(var):
    # 判断是否是数字类型
    if isinstance(var, int) or isinstance(var, long) or isinstance(var, float) or isinstance(var, complex):
        return True
    else:
        return False


def getParameterM2D():
    infoList = getGlobalVariable()
    res = ""
    for info in infoList:
        res += getParameterCommands(info[0], info[1])
    return res

