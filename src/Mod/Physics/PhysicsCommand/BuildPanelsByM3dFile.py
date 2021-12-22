# -*- coding: utf-8 -*-
import FreeCAD
from PySide import QtGui
import PortDlgMain
import Simulation
from DlgData import DlgData
import json
from Modeling.Common.CommonCommand.NewDocument import ObjectDict
from Modeling.Common.Tools import ObjectsTools
from PhysicsTools import CompleterTools,SetColorTools
#json格式数据需要保持原有顺序输出
from collections import OrderedDict
# 获取M3D传来的具体信息转换为Comment

def setPanelsByParameter(DataList):
    # FreeCAD.Console.PrintMessage("\nDataList:\n")
    # FreeCAD.Console.PrintMessage("BUILDPannel: "+str(DataList)+"\n")
    # FreeCAD.Console.PrintMessage("\nDataList:\n")
    try:
        for data in DataList:
            if data[0] == "Port_Type":
                # FreeCAD.Console.PrintError(data[1])
                newData = DlgData({}, data[1][0])
                newData.addData("Dlg_Type", data[0])
                newData.addData("name", data[1][0])#ok
                newData.addData("direction",data[1][1])#ok
                newData.addData("vport_Checked", data[1][2])#ok
                newData.addData("vport", data[1][3])#ok
                newData.addData("scale_Checked", data[1][4])#ok
                newData.addData("scale", data[1][5])#ok
                newData.addData("Ft_Checked", data[1][6])#ok
                newData.addData("Ft", data[1][7])#ok
                ObjectsTools.findObjByLabelWithoutOrderAndInvisible(str(data[1][7]))
                newData.addData("GE2_Checked", data[1][8])#ok
                newData.addData("geFirstName", data[1][9])#ok
                newData.addData("geFirstVal", data[1][10])#ok
                newData.addData("GE2", data[1][10])#ok
                newData.addData("GE3_Checked", data[1][11])#ok
                newData.addData("geSecondName", data[1][12])#ok
                newData.addData("geSecondVal", data[1][13])#ok
                newData.addData("GE3", data[1][13])#ok
                newData.addData("FT_Checked", data[1][14])#ok
                newData.addData("isNewConformalLine", data[1][15])  # ok
                newData.addData("FT+", data[1][16])#ok
                newData.addData("lap_Checked", data[1][17])#ok
                newData.addData("Laplace1", data[1][18])#ok
                newData.addData("Laplace2", data[1][19])#ok
                newData.addData("isAppointArea", data[1][20])#ok
                newData.addData("Orthogonal_projection_surface", data[1][21])#ok
                # 设置颜色
                SetColorTools.setColor(data[1][21],physicsType="Port")
                # ObjectsTools.findObjByLabelWithoutOrderAndInvisible(data[1][21])

                newData.addData("start_R", data[1][22][0])#ok
                newData.addData("start_Y", data[1][22][1])#ok
                newData.addData("start_Z", data[1][22][2])#ok
                newData.addData("end_R", data[1][23][0])#ok
                newData.addData("end_Y", data[1][23][1])#ok
                newData.addData("end_Z", data[1][23][2])#ok
                newData.addData("normal", getNormalFlag(data[1][22], data[1][23]))#ok
                newData.addData("DX_R_Checked", data[1][24])#ok
                newData.addData("DX_Y_Checked", data[1][25])#ok
                newData.addData("DX_Z_Checked", data[1][26])#ok
                newData.addData("DX_R", data[1][27])#ok
                newData.addData("DX_Y", data[1][28])#ok
                newData.addData("DX_Z", data[1][29])#ok
                newData.addData("Laplace1_number", data[1][30])
                newData.addData("Laplace2_number", data[1][31])
                newData.addData("Laplace3", data[1][32])#ok
                newData.addData("Laplace4", data[1][33])
                newData.addData("Laplace5", data[1][34])
                newData.addData("Laplace3_number", data[1][35])
                newData.addData("Laplace4_number", data[1][36])
                newData.addData("Laplace5_number", data[1][37])
                newData.addData("Laplace_num", data[1][38])
                # 为添加ciucuit的m3d新添加的几个变量 @lizhenguang
                newData.addData("circuit_Checked", data[1][39])
                newData.addData("circuit", data[1][40])
                newData.addData('observe_name',data[1][41])
                setBeginVariable(newData)
                sayz("Ft_Checked---------------------------------------------")
                sayz(data[1][6])
            if data[0] == "Free_Type":
                newData=DlgData({}, data[1][0])
                newData.addData("Dlg_Type",data[0])
                newData.addData("name",data[1][0])
                newData.addData("Orthogonal_projection_surface",data[1][1])
                SetColorTools.setColor(data[1][1],physicsType="Free")
                # ObjectsTools.findObjByLabelWithoutOrderAndInvisible(data[1][1])
                newData.addData("start_R",data[1][2][0])
                newData.addData("start_Y",data[1][2][1])
                newData.addData("start_Z",data[1][2][2])
                newData.addData("end_R",data[1][3][0])
                newData.addData("end_Y",data[1][3][1])
                newData.addData("end_Z",data[1][3][2])
                newData.addData("normal", data[1][4])
                newData.addData("direction",data[1][5])
                newData.addData("Absorption_Component",data[1][6])
                newData.addData("VPort_Checked",data[1][7][0])
                newData.addData("VPort",data[1][7][1])
                newData.addData("DX_R_Checked",data[1][8])
                newData.addData("DX_Y_Checked",data[1][9])
                newData.addData("DX_Z_Checked",data[1][10])
                newData.addData("DX_R",data[1][11])
                newData.addData("DX_Y",data[1][12])
                newData.addData("DX_Z",data[1][13])
                setBeginVariable(newData)
                pass
            if data[0] == "Sym_Type":
                newData = DlgData({}, data[1][0])
                newData.addData("Dlg_Type", data[0])
                newData.addData("name", data[1][0])
                newData.addData("Orthogonal_projection_surface", data[1][1])
                SetColorTools.setColor(data[1][1],physicsType="Syn")
                # ObjectsTools.findObjByLabelWithoutOrderAndInvisible(data[1][1])
                newData.addData("start_R", data[1][2][0])
                newData.addData("start_Y", data[1][2][1])
                newData.addData("start_Z", data[1][2][2])
                newData.addData("end_R", data[1][3][0])
                newData.addData("end_Y", data[1][3][1])
                newData.addData("end_Z", data[1][3][2])
                newData.addData("isX", data[1][4][0])
                newData.addData("isY", data[1][4][1])
                newData.addData("isZ", data[1][4][2])
                newData.addData("isNegative", data[1][5][0])
                newData.addData("isPositive", data[1][5][1])
                newData.addData("SymmetricalType", data[1][6][0])
                newData.addData("Symmetric_projection_surface", data[1][6][1])
                ObjectsTools.findObjByLabelWithoutOrderAndInvisible(data[1][6][1])
                newData.addData("Normal_Period", data[1][7])
                newData.addData("DX_R_Checked", data[1][8][0])
                newData.addData("DX_Y_Checked", data[1][8][1])
                newData.addData("DX_Z_Checked", data[1][8][2])
                newData.addData("DX_R", data[1][9][0])
                newData.addData("DX_Y", data[1][9][1])
                newData.addData("DX_Z", data[1][9][2])
                setBeginVariable(newData)
            if data[0] == "Cntr_Type":
                newData = DlgData({}, data[1][0])
                newData.addData("Dlg_Type", data[0])
                newData.addData("name", data[1][0])
                newData.addData("Observation_field",data[1][1])
                newData.addData("Timer2MX", data[1][2])
                newData.addData("Timer", getTimerFlag(data[1][2]))
                newData.addData("Contour_Checked", data[1][3])
                newData.addData("isAppointArea", data[1][4])
                newData.addData("Orthogonal_projection_surface", data[1][5])
                ObjectsTools.findObjByLabelWithoutOrderAndInvisible(data[1][5])
                newData.addData("start_R", data[1][6][0])
                newData.addData("start_Y", data[1][6][1])
                newData.addData("start_Z", data[1][6][2])
                newData.addData("end_R", data[1][7][0])
                newData.addData("end_Y", data[1][7][1])
                newData.addData("end_Z", data[1][7][2])
                newData.addData("normal", getNormalFlag(data[1][6], data[1][7]))
                setBeginVariable(newData)
            if data[0] == "Vec_Type":
                newData = DlgData({}, data[1][2])
                newData.addData("Dlg_Type", data[0])
                newData.addData("Observation_field_1", data[1][0])
                newData.addData("Observation_field_2", data[1][1])
                newData.addData("name", data[1][2])
                newData.addData("Timer2MX", data[1][3])
                newData.addData("Timer", getTimerFlag(data[1][3]))
                newData.addData("Vector_Checked", data[1][4])
                newData.addData("Vector_1", data[1][5])
                newData.addData("Vector_2", data[1][6])
                newData.addData("isAppointArea", data[1][7])
                newData.addData("Orthogonal_projection_surface", data[1][8])
                ObjectsTools.findObjByLabelWithoutOrderAndInvisible(data[1][8])
                newData.addData("start_R", data[1][9][0])
                newData.addData("start_Y", data[1][9][1])
                newData.addData("start_Z", data[1][9][2])
                newData.addData("end_R", data[1][10][0])
                newData.addData("end_Y", data[1][10][1])
                newData.addData("end_Z", data[1][10][2])
                newData.addData("normal", getNormalFlag(data[1][9], data[1][10]))
                setBeginVariable(newData)
            if data[0] == "Pha_Type":
                newData = DlgData({}, data[1][0])
                newData.addData("Dlg_Type", data[0])
                newData.addData("name", data[1][0])
                newData.addData("Horizon",data[1][1])
                newData.addData("Vertical", data[1][2])
                newData.addData("Timer2MX", data[1][3])
                newData.addData("Timer", getTimerFlag(data[1][3]))
                newData.addData("Observation_particle", getSpeciesIndex(data[1][4]))
                newData.addData("Species", data[1][4])
                newData.addData("Thick_Checked", data[1][5])
                newData.addData("Thick", data[1][6])
                newData.addData("Thickness_1", data[1][7])
                newData.addData("Thickness_2", data[1][8])
                newData.addData("Suffix_Checked", data[1][9])
                newData.addData("phase", data[1][10])
                setBeginVariable(newData)
            if data[0] == "Ran_Type":
                newData = DlgData({}, data[1][0])
                newData.addData("Dlg_Type", data[0])
                newData.addData("name", data[1][0])
                newData.addData("ObserveField",data[1][1])
                newData.addData("Timer2MX", data[1][2])
                newData.addData("Timer", getTimerFlag(data[1][2]))
                newData.addData("Fourier_Checked", data[1][3])
                newData.addData("Fourier", getFFTFlagForRan(data[1][4], data[1][5]))
                newData.addData("isMagnitude", data[1][4])
                newData.addData("isComplex", data[1][5])
                newData.addData("isAppointArea", data[1][6])
                newData.addData("Type", data[1][7])
                ObjectsTools.findObjByLabelWithoutOrderAndInvisible(data[1][7])
                newData.addData("start_R", data[1][8][0])
                newData.addData("start_Y", data[1][8][1])
                newData.addData("start_Z", data[1][8][2])
                newData.addData("end_R", data[1][9][0])
                newData.addData("end_Y", data[1][9][1])
                newData.addData("end_Z", data[1][9][2])
                newData.addData("normal", getNormalFlag(data[1][8], data[1][9]))
                # 以下，他们本身的命令格式应该就有问题，先这样
                newData.addData("observe", "Field")
                newData.addData("Field", getRanFieldFlag(data[1][1])[0])
                newData.addData("Field_Integral", getRanFieldFlag(data[1][1])[1])
                newData.addData("Field_Power", getRanFieldFlag(data[1][1])[2])
                newData.addData("Field_Energy", getRanFieldFlag(data[1][1])[3])
                setBeginVariable(newData)
            if data[0] == "Obs_Type":
                newData = DlgData({}, data[1][0])
                newData.addData("Dlg_Type", data[0])
                newData.addData("name", data[1][0])
                newData.addData("observe", getobverse(data[1][1], data[1][2], data[1][3], data[1][4], data[1][5], data[1][6],data[1][7],data[1][8]))
                newData.addData("observe_field",data[1][9])
                newData.addData("Field", getObserveFieldFlag(data[1][9])[0])
                newData.addData("Field_Integral", getObserveFieldFlag(data[1][9])[1])
                newData.addData("Field_Power", getObserveFieldFlag(data[1][9])[2])
                newData.addData("Field_Energy", getObserveFieldFlag(data[1][9])[3])
                newData.addData("phase1", getObserveFieldFlag(data[1][9])[4])
                newData.addData("Particle_Statistics", getObserveFieldFlag(data[1][9])[5])
                newData.addData("Particle", getObserveFieldFlag(data[1][9])[6])
                newData.addData("ParticleType", getObserveFieldFlag(data[1][9])[7])
                newData.addData("Fourier_Checked", data[1][10])
                newData.addData("freq_Checked", data[1][12])
                newData.addData("Fourier", getFFTFlagForObs(data[1][11]))
                newData.addData("fftType", data[1][11])
                newData.addData("freq1", data[1][13])
                newData.addData("freq2", data[1][14])
                newData.addData("limit_Checked", data[1][15])
                newData.addData("limit1", data[1][16])
                newData.addData("limit2", data[1][17])
                newData.addData("interval_Checked", data[1][18])
                newData.addData("interval", data[1][19])
                newData.addData("dataSmooth_Checked", data[1][20])
                newData.addData("dataSmooth", data[1][21])
                newData.addData("timeParam", data[1][22])
                newData.addData("TimeType", data[1][23])
                newData.addData("isAppoint", data[1][24])
                newData.addData("Type", data[1][25])
                ObjectsTools.findObjByLabelWithoutOrderAndInvisible(data[1][25])
                newData.addData("start_R", data[1][26][0])
                newData.addData("start_Y", data[1][26][1])
                newData.addData("start_Z", data[1][26][2])
                newData.addData("end_R", data[1][27][0])
                newData.addData("end_Y", data[1][27][1])
                newData.addData("end_Z", data[1][27][2])
                newData.addData("normal", getNormalFlag(data[1][26], data[1][27]))
                newData.addData("name2",data[1][28])
                setBeginVariable(newData)
            if data[0] == "DefTimer_Type" or data[0] == "Timer_Type":
                newData = DlgData({}, data[1][0])
                newData.addData("Dlg_Type", data[0])
                newData.addData("name", data[1][0])
                newData.addData("Type", data[1][1])
                newData.addData("isByTimeSteps",data[1][2][0])
                newData.addData("isBySimulation",data[1][2][1])
                newData.addData("start", data[1][3])
                newData.addData("end", data[1][4])
                newData.addData("period", data[1][5])
                newData.addData("discreteTime",data[1][6])
                setBeginVariable(newData)

            if data[0] == "Populate_Type":
                # FreeCAD.Console.PrintError("\n进入到设置populate的过程")
                newData = DlgData({}, data[1][0])
                newData.addData("Dlg_Type",data[0])
                newData.addData("name",data[1][0])
                newData.addData("ParticalType",data[1][1])
                newData.addData("Orthogonal_projection_surface",data[1][2])
                newData.addData("X1",data[1][3])
                newData.addData("Y1",data[1][4])
                newData.addData("Z1",data[1][5])
                newData.addData("X2",data[1][6])
                newData.addData("Y2",data[1][7])
                newData.addData("Z2",data[1][8])
                newData.addData("density",data[1][9])
                newData.addData("temp",data[1][10])
                setBeginVariable(newData)
            if data[0] == "EmSE_Type":
                newData = DlgData({}, data[1][0])
                newData.addData("Dlg_Type",data[0])
                newData.addData("name",data[1][0])
                newData.addData("energy_sec",data[1][1])
                newData.addData("max_num_sec",data[1][2])
                newData.addData("WEIGHT_FACTOR",data[1][3])
                newData.addData("ENERGY_DISTRIBUTION",data[1][4])
                newData.addData("min_energy",data[1][5])
                newData.addData("max_energy",data[1][6])
                newData.addData("ANGLE_DISTRIBUTION",data[1][7])
                newData.addData("isCheck_WF",data[1][8])
                newData.addData("isCheck_ED",data[1][9])
                newData.addData("isCheck_AD",data[1][10])
                newData.addData("notInclude1",data[1][11])
                newData.addData("notInclude2",data[1][12])
                newData.addData("include1",data[1][13])
                newData.addData("include2",data[1][14])
                newData.addData("Emitter",data[1][15])
                newData.addData("isEmit",data[1][16])
                newData.addData("isExclude1",data[1][17])
                newData.addData("isExclude2",data[1][18])
                newData.addData("isInclude1",data[1][19])
                newData.addData("isInclude2",data[1][020])
                setBeginVariable(newData)


            if data[0] == "Gasgas_Type":
                newData = DlgData({}, data[1][0])
                newData.addData("Dlg_Type",data[0])
                newData.addData("name",data[1][0])
                newData.addData("Types",data[1][1])
                newData.addData("pressure",data[1][2])
                newData.addData("temperature",data[1][3])
                setBeginVariable(newData)
                

            if data[0] == "EMB_Type":
                newData = DlgData({}, data[1][0])
                #新增“Same_Parent_Diff”属性
                newData.addData("Same_Parent_Diff","EmB")
                newData.addData("Dlg_Type", data[0])
                newData.addData("name", data[1][0])
                newData.addData("BeamJ",data[1][1])
                newData.addData("BeamV", data[1][2])
                newData.addData("particleType_Checked", data[1][3])
                newData.addData("Species", data[1][4])
                newData.addData("particleType", getParticleTypeIndex(data[1][4]))
                newData.addData("generationRate_Checked", data[1][5])
                newData.addData("generationRate", int(data[1][6]))
                newData.addData("transmittingInterval_Checked", data[1][7])
                newData.addData("transmittingInterval", data[1][8])
                newData.addData("stepMultiple", int(data[1][9]))
                newData.addData("surface_Checked", data[1][10])
                newData.addData("surface", data[1][11])
                newData.addData("outSurface_Checked", data[1][12])
                newData.addData("outSurface", data[1][13])
                newData.addData("Dn", data[1][14])
                newData.addData("isEmit", data[1][15])
                newData.addData("Emitter", data[1][16])
                ObjectsTools.findObjByLabelWithoutOrderAndInvisible(data[1][16])
                newData.addData("isExclude1", data[1][17])
                newData.addData("Zone1", data[1][18])
                ObjectsTools.findObjByLabelWithoutOrderAndInvisible(data[1][18])
                newData.addData("isExclude2", data[1][19])
                newData.addData("Zone2", data[1][20])
                ObjectsTools.findObjByLabelWithoutOrderAndInvisible(data[1][19])
                newData.addData("isInclude1", data[1][21])
                newData.addData("Zone11", data[1][22])
                ObjectsTools.findObjByLabelWithoutOrderAndInvisible(data[1][22])
                newData.addData("isInclude2", data[1][23])
                newData.addData("Zone22", data[1][24])
                ObjectsTools.findObjByLabelWithoutOrderAndInvisible(data[1][24])

                setBeginVariable(newData)
            if data[0] == "EME_Type":
                newData = DlgData({}, data[1][0])
                newData.addData("Same_Parent_Diff","EmE")
                newData.addData("Dlg_Type", data[0])
                newData.addData("name", data[1][0])
                newData.addData("TField_Checked",data[1][1])
                newData.addData("TField", data[1][2])
                newData.addData("RField_Checked", data[1][3])
                newData.addData("RField", data[1][4])
                newData.addData("Charg_Checked", data[1][5])
                newData.addData("Charg", data[1][6])
                newData.addData("FRate_Checked", data[1][7])
                newData.addData("FRate", data[1][8])
                newData.addData("particleType_Checked", data[1][9])
                newData.addData("Species", data[1][10])
                newData.addData("particleType", getParticleTypeIndex(data[1][10]))
                newData.addData("generationRate_Checked", data[1][11])
                newData.addData("generationRate", int(data[1][12]))
                newData.addData("transmittingInterval_Checked", data[1][13])
                newData.addData("transmittingInterval", data[1][14])
                newData.addData("stepMultiple", int(data[1][15]))
                newData.addData("surface_Checked", data[1][16])
                newData.addData("surface", data[1][17])
                newData.addData("outSurface_Checked", data[1][18])
                newData.addData("outSurface", data[1][19])
                newData.addData("Dn", data[1][20])
                newData.addData("isEmit", data[1][21])
                newData.addData("Emitter", data[1][22])
                ObjectsTools.findObjByLabelWithoutOrderAndInvisible(data[1][22])
                newData.addData("isExclude1", data[1][23])
                newData.addData("Zone1", data[1][24])
                ObjectsTools.findObjByLabelWithoutOrderAndInvisible(data[1][24])
                newData.addData("isExclude2", data[1][25])
                newData.addData("Zone2", data[1][26])
                ObjectsTools.findObjByLabelWithoutOrderAndInvisible(data[1][26])
                newData.addData("isInclude1", data[1][27])
                newData.addData("Zone11", data[1][28])
                ObjectsTools.findObjByLabelWithoutOrderAndInvisible(data[1][28])
                newData.addData("isInclude2", data[1][29])
                newData.addData("Zone22", data[1][30])
                ObjectsTools.findObjByLabelWithoutOrderAndInvisible(data[1][30])
                setBeginVariable(newData)
            if data[0] == "EMG_Type":
                newData = DlgData({}, data[1][0])
                newData.addData("Same_Parent_Diff","EmG")
                newData.addData("Dlg_Type", data[0])
                newData.addData("name", data[1][0])
                newData.addData("Beam_Current",data[1][1])
                newData.addData("Guiding_Magnetic_Field", data[1][2])
                newData.addData("Vertical_Momentum", data[1][3])
                newData.addData("Horizontal_Momentum", data[1][4])
                newData.addData("Guiding_Radius", data[1][5])
                newData.addData("LaunchCoordinate_X", data[1][6][0])
                newData.addData("LaunchCoordinate_Y", data[1][6][1])
                newData.addData("LaunchCoordinate_Z", data[1][6][2])
                newData.addData("isX1", data[1][7])
                newData.addData("isX2", data[1][8])
                newData.addData("isX3", data[1][9])
                newData.addData("particleType_Checked", data[1][10])
                newData.addData("Species", data[1][11])
                newData.addData("particleType", getParticleTypeIndex(data[1][11]))
                newData.addData("generationRate_Checked", data[1][12])
                newData.addData("generationRate", int(data[1][13]))
                newData.addData("transmittingInterval_Checked", data[1][14])
                newData.addData("transmittingInterval", data[1][15])
                newData.addData("stepMultiple", int(data[1][16]))
                newData.addData("surface_Checked", data[1][17])
                newData.addData("surface", data[1][18])
                newData.addData("outSurface_Checked", data[1][19])
                newData.addData("outSurface", data[1][20])
                newData.addData("Dn", data[1][21])
                newData.addData("isEmit", data[1][22])
                newData.addData("Emitter", data[1][23])
                ObjectsTools.findObjByLabelWithoutOrderAndInvisible(data[1][23])
                newData.addData("isExclude1", data[1][24])
                newData.addData("Zone1", data[1][25])
                ObjectsTools.findObjByLabelWithoutOrderAndInvisible(data[1][25])
                newData.addData("isExclude2", data[1][26])
                newData.addData("Zone2", data[1][27])
                ObjectsTools.findObjByLabelWithoutOrderAndInvisible(data[1][27])
                newData.addData("isInclude1", data[1][28])
                newData.addData("Zone11", data[1][29])
                ObjectsTools.findObjByLabelWithoutOrderAndInvisible(data[1][29])
                newData.addData("isInclude2", data[1][30])
                newData.addData("Zone22", data[1][31])
                ObjectsTools.findObjByLabelWithoutOrderAndInvisible(data[1][31])
                # 因遗漏Axias，在此添加@lzg
                if data[1][7] == True:
                    newData.addData("Axias","X")
                elif data[1][8] == True:
                    newData.addData("Axias","Y")
                else :
                    newData.addData("Axias","Z")
                setBeginVariable(newData)
            if data[0] == "EMH_Type":
                newData = DlgData({}, data[1][0])
                newData.addData("Same_Parent_Diff","EmH")
                newData.addData("Dlg_Type", data[0])
                newData.addData("name", data[1][0])
                newData.addData("Fowler_Nordheim_A",data[1][1])
                newData.addData("Fowler_Nordheim_B", data[1][2])
                newData.addData("PHI", data[1][3])
                newData.addData("particleType_Checked", data[1][4])
                newData.addData("Species", data[1][5])
                newData.addData("particleType", getParticleTypeIndex(data[1][5]))
                newData.addData("generationRate_Checked", data[1][6])
                newData.addData("generationRate", int(data[1][7]))
                newData.addData("transmittingInterval_Checked", data[1][8])
                newData.addData("transmittingInterval", data[1][9])
                newData.addData("stepMultiple", int(data[1][10]))
                newData.addData("surface_Checked", data[1][11])
                newData.addData("surface", data[1][12])
                newData.addData("outSurface_Checked", data[1][13])
                newData.addData("outSurface", data[1][14])
                newData.addData("Dn", data[1][15])
                newData.addData("isEmit", data[1][16])
                newData.addData("Emitter", data[1][17])
                ObjectsTools.findObjByLabelWithoutOrderAndInvisible(data[1][17])
                newData.addData("isExclude1", data[1][18])
                newData.addData("Zone1", data[1][19])
                ObjectsTools.findObjByLabelWithoutOrderAndInvisible(data[1][19])
                newData.addData("isExclude2", data[1][20])
                newData.addData("Zone2", data[1][21])
                ObjectsTools.findObjByLabelWithoutOrderAndInvisible(data[1][21])
                newData.addData("isInclude1", data[1][22])
                newData.addData("Zone11", data[1][23])
                ObjectsTools.findObjByLabelWithoutOrderAndInvisible(data[1][23])
                newData.addData("isInclude2", data[1][24])
                newData.addData("Zone22", data[1][25])
                ObjectsTools.findObjByLabelWithoutOrderAndInvisible(data[1][25])
                setBeginVariable(newData)
            if data[0] == "EMT_Type":
                newData = DlgData({}, data[1][0])
                newData.addData("Same_Parent_Diff","EMT")
                newData.addData("Dlg_Type", data[0])
                newData.addData("name", data[1][0])
                newData.addData("WF",data[1][1])
                newData.addData("TP", data[1][2])
                newData.addData("particleType_Checked", data[1][3])
                newData.addData("Species", data[1][4])
                newData.addData("particleType", getParticleTypeIndex(data[1][4]))
                newData.addData("generationRate_Checked", data[1][5])
                newData.addData("generationRate", int(data[1][6]))
                newData.addData("transmittingInterval_Checked", data[1][7])
                newData.addData("transmittingInterval", data[1][8])
                newData.addData("stepMultiple", int(data[1][9]))
                newData.addData("surface_Checked", data[1][10])
                newData.addData("surface", data[1][11])
                newData.addData("outSurface_Checked", data[1][12])
                newData.addData("outSurface", data[1][13])
                newData.addData("Dn", data[1][14])
                newData.addData("isEmit", data[1][15])
                newData.addData("Emitter", data[1][16])
                ObjectsTools.findObjByLabelWithoutOrderAndInvisible(data[1][16])
                newData.addData("isExclude1", data[1][17])
                newData.addData("Zone1", data[1][18])
                ObjectsTools.findObjByLabelWithoutOrderAndInvisible(data[1][18])
                newData.addData("isExclude2", data[1][19])
                newData.addData("Zone2", data[1][20])
                ObjectsTools.findObjByLabelWithoutOrderAndInvisible(data[1][20])
                newData.addData("isInclude1", data[1][21])
                newData.addData("Zone11", data[1][22])
                ObjectsTools.findObjByLabelWithoutOrderAndInvisible(data[1][22])
                newData.addData("isInclude2", data[1][23])
                newData.addData("Zone22", data[1][24])
                ObjectsTools.findObjByLabelWithoutOrderAndInvisible(data[1][24])
                setBeginVariable(newData)
                #@fubiao
            if data[0] == "Sol_Type":
                newData=DlgData({}, data[1][0])
                newData.addData("Same_Parent_Diff","Sol")
                newData.addData("Dlg_Type",data[0])
                newData.addData("name",data[1][0])
                newData.addData("Center_Z",data[1][1][0])
                newData.addData("Center_R",data[1][1][1])
                newData.addData("Half_Circle",data[1][1][2])
                newData.addData("Radius_In",data[1][1][3])
                newData.addData("Radius_Out",data[1][1][4])
                newData.addData("Turns",data[1][1][5])
                newData.addData("DX_R_Checked",data[1][2][0])
                newData.addData("DX_Y_Checked",data[1][2][1])
                newData.addData("DX_Z_Checked",data[1][2][2])
                newData.addData("DX_R",data[1][2][3])
                newData.addData("DX_Y",data[1][2][4])
                newData.addData("DX_Z",data[1][2][5])
                newData.addData("Material",data[1][3])
                newData.addData("Shimming_Factor",data[1][4][0])
                newData.addData("Factor_R",data[1][4][1])
                newData.addData("Factor_Z",data[1][4][2])
                newData.addData("Duty",data[1][4][3])
                newData.addData("_RADIUSIN",data[1][4][4])
                newData.addData("_RADIUSOUT",data[1][4][5])
                newData.addData("Permeability",data[1][4][6])
                newData.addData("Coil_Current",data[1][4][7])
                newData.addData("THETA",data[1][4][8])
                newData.addData("PHI",data[1][4][9])
                setBeginVariable(newData)
                pass
            if data[0] == "Exp_Tpye":
                newData=DlgData({}, data[1][0])
                newData.addData("Same_Parent_Diff","ExP")
                newData.addData("Dlg_Type",data[0])
                newData.addData("name",data[1][0])
                newData.addData("Current_Source",data[1][1])
                newData.addData("start_R",data[1][2][0])
                newData.addData("start_Y",data[1][2][1])
                newData.addData("start_Z",data[1][2][2])
                newData.addData("end_R",data[1][2][3])
                newData.addData("end_Y",data[1][2][4])
                newData.addData("end_Z",data[1][2][5])
                newData.addData("Specified_Current_Density",data[1][3])
                newData.addData("JFUNC",data[1][4])
                setBeginVariable(newData)
                pass
            if data[0] == "Foil_Type":
                # FreeCAD.Console.PrintError(data[1])
                # FreeCAD.Console.PrintError('\n')
                #  待修改
                newData=DlgData({}, data[1][0])
                newData.addData("Same_Parent_Diff","Foil")
                newData.addData("Dlg_Type",data[0])
                newData.addData("name",data[1][0])
                newData.addData("Orthogonal_projection_surface",data[1][1])
                SetColorTools.setColor(data[1][1],physicsType="Foil")
                # ObjectsTools.findObjByLabelWithoutOrderAndInvisible(data[1][1])
                newData.addData("start_R",data[1][2][0])
                newData.addData("start_Y",data[1][2][1])
                newData.addData("start_Z",data[1][2][2])
                newData.addData("end_R",data[1][2][3])
                newData.addData("end_Y",data[1][2][4])
                newData.addData("end_Z",data[1][2][5])
                newData.addData("thick",data[1][3])
                newData.addData("checkBox_CustomMaterial",data[1][4])
                newData.addData("CustomMaterial",data[1][5])
                newData.addData("checkBox_DefaultMaterial",data[1][6])
                newData.addData("defaultMaterial",data[1][7])
                setBeginVariable(newData)
                pass
            if data[0] == "Ind_Type":
                newData=DlgData({}, data[1][0])
                newData.addData("Same_Parent_Diff","Ind")
                newData.addData("Dlg_Type",data[0])
                newData.addData("name",data[1][0])
                newData.addData("Orthogonal_projection_surface",data[1][1])
                SetColorTools.setColor(data[1][1],physicsType="Ind")
                # ObjectsTools.findObjByLabelWithoutOrderAndInvisible(data[1][1])
                newData.addData("start_R",data[1][2][0])
                newData.addData("start_Y",data[1][2][1])
                newData.addData("start_Z",data[1][2][2])
                newData.addData("end_R",data[1][2][3])
                newData.addData("end_Y",data[1][2][4])
                newData.addData("end_Z",data[1][2][5])
                newData.addData("Diam",data[1][3])
                newData.addData("INDUC_Checked",data[1][4])
                newData.addData("INDUC",data[1][5])
                setBeginVariable(newData)
                pass
    except KeyError as reason:
        sayz("!!!Error:KeyError,Maybe lack of key:%s" % str(reason))

    from Physics.PhysicsCommand.BoundPalMain import BoundSettingTreeShow
    from Physics.PhysicsCommand.ObservePalMain import ObserveSettingTreeShow
    BoundSettingTreeShow()
    ObserveSettingTreeShow()


def setBeginVariable(DlgData):
    Begin = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict)
    Begin[DlgData.id] = DlgData.data
    FreeCAD.ActiveDocument.Begin = json.dumps(Begin)




def getTimerFlag(Timer2MX):
    if Timer2MX == u"DefTimer":
        timer = u"默认定时器"
    elif Timer2MX == u"TSYS$FIRST":
        timer = u"仅开始时刻"
    elif Timer2MX == u"TSYS$LAST":
        timer = u"仅结束时刻"
    else:
        timer = Timer2MX
    return timer

def getSpeciesIndex(species):
    if species == u"ELECTRON":
        index = 1
    elif species == u"PROTON":
        index = 2
    elif species == u"ALL":
        index = 0
    else:
        index = -1

    return index

def getNormalFlag(starts, stops):

    if starts[2] == stops[2]:
        return "Z"
    if starts[1] == stops[1]:
        return "theta"
    if starts[0] == stops[0]:
        return "R"

def getFFTFlagForRan(isMagnitude, isComplex):
    if isMagnitude:
        return "real"
    if isComplex:
        return "complex"

def getFFTFlagForObs(fftType):
    if fftType == "MAGNITUDE":
        return "real"
    if fftType == "COMPLEX":
        return "complex"
    
def getParticleTypeIndex(Species):
    if Species == "ELECTRON":
        return 0
    if Species == "PROTON":
        return 1

def getobverse(isField, isFieldIntegral, isFieldPower, isFieldEnergy, 
    isParticleStatistics,isParticleCollected,isParticleEmitted,isParticleDestroyed):
    if isField:
        return "Field"
    elif isFieldIntegral:
        return "Field_Integral"
    elif isFieldPower:
        return "Field_Power"
    elif isFieldEnergy:
        return "Field_Energy"
    elif isParticleStatistics:
        return "Particle_Statistics"
    elif isParticleCollected:
        return "Particle_Collected"
    elif isParticleEmitted:
        return "Particle_Emitted"
    elif isParticleDestroyed:
        return "Particle_Destroyed"

def getRanFieldFlag(observeField):
    Field = ["E1", "E2", "E3", "B1", "B2", "B3", "J1", "J2", "J3",
             "Q0", "E1AV", "E2AV", "E3AV", "B1AV", "B2AV", "B3AV",
             "E1ST", "E2ST", "E3ST", "B1ST", "B2ST", "B3ST", "PHST",
             "B", "E"]
    Field_Integral = ["E.DL", "H.DL", "J.DA"]
    Field_Power = ["S.DA"]
    Field_Energy = ["EM", "ELECTRIC", "MAGNETIC"]

    field = Field[0]
    field_Integral = Field_Integral[0]
    field_Power = Field_Power[0]
    field_Energy = Field_Energy[0]
    field_emit = "phase1"

    if observeField in Field:
        field = observeField
    elif observeField in Field_Integral:
        field_Integral = observeField
    elif observeField in Field_Power:
        field_Power = observeField
    elif observeField in Field_Energy:
        field_Energy = observeField
    else:
        field_emit = observeField

    return [field, field_Integral, field_Power, field_Energy, field_emit]

def getObserveFieldFlag(observeField):
    Field = ["E1", "E2", "E3", "B1", "B2", "B3", "J1", "J2", "J3",
             "Q0", "E1AV", "E2AV", "E3AV", "B1AV", "B2AV", "B3AV",
             "E1ST", "E2ST", "E3ST", "B1ST", "B2ST", "B3ST", "PHST",
             "B", "E"]
    Field_Integral = ["E.DL", "H.DL", "J.DA"]
    Field_Power = ["S.DA"]
    Field_Energy = ["EM", "ELECTRIC", "MAGNETIC"]
    Particle_Statistics = ["CHARGE", "ENERGY", "VRATIO"]
    Particle=["CHARGE", "CURRENT", "ENERGY","POWER","VOLTAGE"]
    ParticleType=["ELECTRON", "IONS", "ALL"]

    field = Field[0]
    field_Integral = Field_Integral[0]
    field_Power = Field_Power[0]
    field_Energy = Field_Energy[0]
    phase1 = "phase1"
    particle_Statistics =Particle_Statistics[0]
    particle = Particle[0]
    particleType = ParticleType[0]

    if observeField[1] == "":
        observeField = observeField[0]
        if observeField in Field:
            field = observeField
        elif observeField in Field_Integral:
            field_Integral = observeField
        elif observeField in Field_Power:
            field_Power = observeField
        elif observeField in Field_Energy:
            field_Energy = observeField
        
    else:
        if observeField[0] in Particle_Statistics:
            if observeField[0] == "EMIT_EPS":
                phase1 = observeField[1]
            else:
                particle_Statistics = observeField[0]
        elif observeField[0] in Particle:
            particle = observeField[0]
        if observeField[1] in ParticleType:
            particleType = observeField[1]

    return [field, field_Integral, field_Power, field_Energy, phase1,particle_Statistics,particle,particleType]

def getTimeTypeFlag(observeType):
    if observeType == "POINT":
        return 0
    elif observeType == "LINE":
        return 1
    elif observeType == "AREA":
        return 2
    elif observeType == "VOLUME":
        return 3
    elif observeType == "EMIT":
        return 4
    else:
        return -1




def sayz(msg):
    FreeCAD.Console.PrintMessage("--------------------------------------------")
    FreeCAD.Console.PrintMessage('\n')
    FreeCAD.Console.PrintMessage(msg)
    FreeCAD.Console.PrintMessage('\n')