# encoding:utf-8
# 此文件存放模型信息输入、工作区间设置、数据导出设定、运行处理选项、场及函数定义、时域计算设置

import FreeCAD
import M3DShare
from Model3D.Tools import Tools3D
import re

blankSpace = " "
semicolon = ";"
newLine = "\n"
tab = "\t"
comma = ","

def getParamM3D():
    """
    由于参数模块的删除操作，执行后，盛放M3D的容器没有将需要删除的参数删除，导致M3D是实际不符，
    当打开老工程时，M3D容器和FreeCAD的参数容器不统一，导致抛出异常
    以下为适配老工程做适配，将不存在的参数不写入M3D中，但没有改变Company里的参数
    在点击参数模块时，在cpp的recover中进行剔除已删除参数
    """
    docObj = FreeCAD.ActiveDocument.getObject("Param")
    ParamList = docObj.PropertiesList
    exp_list = re.split(r'\n\n', FreeCAD.ActiveDocument.Company)
    temp_m3d_p = ""
    for exp in exp_list:
        searchName = re.split(r'\s', exp)
        if ParamList.count(searchName[0]) is 1:
            temp_m3d_p += exp + "\n\n"
    return temp_m3d_p

def ModelingInfo(obj):
    """
    模型输入
    返回:temp_m3d
    """

    temp_m3d = ""
    temp_m3d += "HEADER" + blankSpace + "ORGANIZATION" + blankSpace + '"' + obj.modeling + '"' + semicolon + newLine + \
                "HEADER" + blankSpace + "AUTHOR" + blankSpace + '"' + obj.author + '"' + semicolon + newLine + \
                "HEADER" + blankSpace + "DEVICE" + blankSpace + '"' + obj.company + '"' + semicolon + newLine + \
                "HEADER" + blankSpace + "REMARKS" + blankSpace + '"' + obj.remarks + '"' + semicolon + newLine
    return temp_m3d


def NetStepSetting(obj):
    """
    工作区间设置
    """
    temp_m3d_p = ""
    temp_m3d_gg = ""
    temp_m3d_p += getParamM3D()
    temp_m3d_p += "DX1" + blankSpace + "=" + blankSpace + obj.stepSizeX + semicolon + newLine
    temp_m3d_p += "DX2" + blankSpace + "=" + blankSpace + obj.stepSizeY + semicolon + newLine
    temp_m3d_p += "DX3" + blankSpace + "=" + blankSpace + obj.stepSizeZ + semicolon + newLine

    if obj.isStartUsing:
        temp_m3d_gg += "VOLUME " + blankSpace + obj.Label + blankSpace + "CONFORMAL"
        temp_m3d_gg += M3DShare.PointCoordinates().point1(obj)
        temp_m3d_gg += M3DShare.PointCoordinates().point2(obj) + semicolon + newLine
        temp_m3d_gg += "MARK" + blankSpace + obj.Label + blankSpace + "X1" + blankSpace + "SIZE" + blankSpace + \
                       "DX1" + semicolon + newLine
        temp_m3d_gg += "MARK" + blankSpace + obj.Label + blankSpace + "X2" + blankSpace + "SIZE" + blankSpace + \
                       "DX2" + semicolon + newLine
        temp_m3d_gg += "MARK" + blankSpace + obj.Label + blankSpace + "X3" + blankSpace + "SIZE" + blankSpace + \
                       "DX3" + semicolon + newLine

    return temp_m3d_p, temp_m3d_gg


def DataProcessingSetting(obj):
    """
        数据导出设置
        返回值：temp_m2d_do
    """
    temp_m3d_do = ""
    temp_m3d_do += "DUMP NAME TIME_" + FreeCAD.ActiveDocument.Name + semicolon + newLine
    if obj.isCheckBox_text:
        temp_m3d_do += "DUMP" + blankSpace + "FORMAT" + blankSpace + "ASCII" + semicolon + newLine
    elif obj.isCheckBox_binary:
        temp_m3d_do += "DUMP" + blankSpace + "FORMAT" + blankSpace + "BINARY" + semicolon + newLine
        
    if obj.isCheckBox_Time_obser:
        temp_m3d_do += "DUMP" + blankSpace + "TYPE" + blankSpace + "OBSERVE" + semicolon + newLine
    if obj.isCheckBox_space_obser:
        temp_m3d_do += "DUMP" + blankSpace + "TYPE" + blankSpace + "RANGE" + semicolon + newLine
    if obj.isCheckBox_contor_plot:
        temp_m3d_do += "DUMP" + blankSpace + "TYPE" + blankSpace + "CONTOUR" + semicolon + newLine
    if obj.isCheckBox_vector_data:
        temp_m3d_do += "DUMP" + blankSpace + "TYPE" + blankSpace + "VECTOR" + semicolon + newLine
    if obj.isCheckBox_phase_space:
        temp_m3d_do += "DUMP" + blankSpace + "TYPE" + blankSpace + "PHASESPACE" + semicolon + newLine
    if obj.isCheckBox_set_prefix:
        temp_m3d_do += "DUMP" + blankSpace + "PREFIX" + blankSpace + '"' + obj.prefiX + '"' + semicolon + newLine
    if obj.isCheckBox_set_suffix:
        temp_m3d_do += "DUMP" + blankSpace + "SUFFIX" + blankSpace + '"' + obj.suffiX + '"' + semicolon + newLine

    return temp_m3d_do


def RunOptions(obj):
    """"
    运行处理选项
    """
    temp_m3d_ro = ""
    if obj.isCheckBox_paused_when_start:
        temp_m3d_ro += "GRAPHICS" + blankSpace + "PAUSE" + semicolon + newLine
    if obj.isCheckBox_show_structureChart:
        temp_m3d_ro += "DISPLAY" + semicolon + newLine
    return temp_m3d_ro


def FieldSetting(obj):
    """
            场及函数定义
            返回值：temp_m2d_cp
        """
    temp_m3d_cp = ""
    temp_m3d_cp += obj.self_definingFunction
    # 修改与坐标系相关的函数参数
    FB1ST = ""
    FB2ST = ""
    FB3ST = ""
    FE1ST = ""
    FE2ST = ""
    FE3ST = ""
    functionParameters = ""
    coodinate = FreeCAD.ActiveDocument.CoordinateSystem
    if coodinate == u'Rectangular' or coodinate == 'Rectangular':
        FB1ST = "FBXST"
        FB2ST = "FBYST"
        FB3ST = "FBZST"
        FE1ST = "FEXST"
        FE2ST = "FEYST"
        FE3ST = "FEZST"
        functionParameters = "(X,Y,Z)"
    elif coodinate == u'Polar' or coodinate == 'Polar':
        FB1ST = "FBRST"
        FB2ST = "FBPST"
        FB3ST = "FBZST"
        FE1ST = "FERST"
        FE2ST = "FEPST"
        FE3ST = "FEZST"
        functionParameters = "(R,P,Z)"
    elif coodinate == u'Cylindrical' or coodinate == 'Cylindrical':
        FB1ST = "FBZST"
        FB2ST = "FBRST"
        FB3ST = "FBPST"
        FE1ST = "FEZST"
        FE2ST = "FERST"
        FE3ST = "FEPST"
        functionParameters = "(Z,R,P)"
    else:
        Tools3D.sayz("请选择正确的坐标系")

    if obj.isMagnetostaticFieldX:
        # 作此判断的目的是在整体生成m3d时，不会多一行
        if len(temp_m3d_cp) != 0:
            temp_m3d_cp += newLine
        temp_m3d_cp += "FUNCTION" + blankSpace + FB1ST + functionParameters + blankSpace + "=" + blankSpace + \
                       obj.magnetostaticFieldX + semicolon + newLine
        temp_m3d_cp += "PRESET" + blankSpace + "B1ST" + blankSpace + "FUNCTION" + blankSpace + \
                       FB1ST + semicolon
    if obj.isMagnetostaticFieldY:
        if len(temp_m3d_cp) != 0:
            temp_m3d_cp += newLine
        temp_m3d_cp += "FUNCTION" + blankSpace + FB2ST + functionParameters + blankSpace + "=" + blankSpace + \
                       obj.magnetostaticFieldY + semicolon + newLine
        temp_m3d_cp += "PRESET" + blankSpace + "B2ST" + blankSpace + "FUNCTION" + blankSpace + \
                       FB2ST + semicolon
    if obj.isMagnetostaticFieldZ:
        if len(temp_m3d_cp) != 0:
            temp_m3d_cp += newLine
        temp_m3d_cp += "FUNCTION" + blankSpace + FB3ST + functionParameters + blankSpace + "=" + blankSpace + \
                       obj.magnetostaticFieldZ + semicolon + newLine
        temp_m3d_cp += "PRESET" + blankSpace + "B3ST" + blankSpace + "FUNCTION" + blankSpace + \
                       FB3ST + semicolon

    if obj.isElectrostaticFieldX:
        if len(temp_m3d_cp) != 0:
            temp_m3d_cp += newLine
        temp_m3d_cp += "FUNCTION" + blankSpace + FE1ST + functionParameters + blankSpace + "=" + blankSpace + \
                       obj.electrostaticFieldX + semicolon + newLine
        temp_m3d_cp += "PRESET" + blankSpace + "E1ST" + blankSpace + "FUNCTION" + blankSpace + \
                       FE1ST + semicolon
    if obj.isElectrostaticFieldY:
        if len(temp_m3d_cp) != 0:
            temp_m3d_cp += newLine
        temp_m3d_cp += "FUNCTION" + blankSpace + FE2ST + functionParameters + blankSpace + "=" + blankSpace + \
                       obj.electrostaticFieldY + semicolon + newLine
        temp_m3d_cp += "PRESET" + blankSpace + "E2ST" + blankSpace + "FUNCTION" + blankSpace + \
                       FE2ST + semicolon
    if obj.isElectrostaticFieldZ:
        if len(temp_m3d_cp) != 0:
            temp_m3d_cp += newLine
        temp_m3d_cp += "FUNCTION" + blankSpace + FE3ST + functionParameters + blankSpace + "=" + blankSpace + \
                       obj.electrostaticFieldZ + semicolon + newLine
        temp_m3d_cp += "PRESET" + blankSpace + "E3ST" + blankSpace + "FUNCTION" + blankSpace + \
                       FE3ST + semicolon + newLine
    return temp_m3d_cp


def TimeDomainSetting(obj):
    """
           时间域计算设定
           返回值：temp_m3d_ss
    """
    temp_m3d_ss = ""
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
        if obj.isRelativistic:
            TimeStepInterval_temp += "KINEMATICS" + blankSpace + obj.particleCalculatesTimeStepInterval + blankSpace + \
                                     "RELATIVISTIC"
        temp_m3d_ss += TimeStepInterval_temp + semicolon + newLine
    #场算法
    temp_m3d_ss += "MAXWELL" + blankSpace + fieldAlgorithm_dict.get(obj.fieldAlgorithm) + semicolon + newLine
    # 是否开启设置模式
    if obj.isSettingPattern:
        if obj.isEM:
            SettingPattern_temp = "MODE" + blankSpace + "BOTH"
        if obj.isTE:
            SettingPattern_temp = "MODE" + blankSpace + "TE"
        if obj.isTM:
            SettingPattern_temp = "MODE" + blankSpace + "TM"
        temp_m3d_ss += '{}'.format(SettingPattern_temp) + semicolon + newLine
    # 是否设置步长
    if obj.isSetStep:
        # 设置步长如果是变量，不加NANOSECOND
        if str(obj.setStep).replace('.', '').replace('-', '').replace('e', '').replace('E', '').isdigit():
            SetStep_temp = "TIME_STEP" + blankSpace + obj.setStep + "NANOSECOND"
        else:
            SetStep_temp = "TIME_STEP" + blankSpace + obj.setStep
        temp_m3d_ss += SetStep_temp + semicolon + newLine
    # 是否设置电荷连续性
    if obj.isSetAlgorithm:
        SetAlgorithm_temp = "CONTINUITY" + blankSpace + "CONSERVED"
        temp_m3d_ss += SetAlgorithm_temp + semicolon + newLine
    # 计算时间如果是变量，不加NANOSECOND
    if str(obj.computationTime).replace('.', '').isdigit():
        temp_m3d_ss += "DURATION" + blankSpace + obj.computationTime + "NANOSECOND" + semicolon + newLine
    else:
        temp_m3d_ss += "DURATION" + blankSpace + obj.computationTime + semicolon + newLine

    return temp_m3d_ss
