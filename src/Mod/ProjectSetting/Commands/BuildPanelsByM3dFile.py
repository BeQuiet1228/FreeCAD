# -*- coding: utf-8 -*-
import FreeCAD
from PySide import QtGui
from ProjectSettingsDlgData import ProjectSettingsDlgData  as DlgData
import json
from Modeling.Common.Tools import ObjectsTools
#json格式数据需要保持原有顺序输出
from collections import OrderedDict

# 获取M3D传来的具体信息转换为Comment
def setPanelsByParameter(DataList):
    for data in DataList:
        if data[0] == "ModelingInfo":
            newData = DlgData({},data[0])
            newData.addData("modeling",data[1][0])
            newData.addData("author",data[1][1])
            newData.addData("company",data[1][2])
            newData.addData("remarks",data[1][3])
            setComment(newData)
        if data[0]=="DataProcessingSetting":
            newData = DlgData({},data[0])
            newData.addData("time_obser",data[1][0])
            newData.addData("space_obser",data[1][1])
            newData.addData("contor_plot",data[1][2])
            newData.addData("vector_data",data[1][3])
            newData.addData("phase_space",data[1][4])
            newData.addData("checkBox_prefix",data[1][5][0])
            newData.addData("lineEdit_prefix",data[1][5][1])
            newData.addData("checkBox_suffix",data[1][6][0])
            newData.addData("lineEdit_suffix",data[1][6][1])
            newData.addData("text_form",data[1][7][0])
            newData.addData("binary_form",data[1][7][1])
            setComment(newData)
        if data[0]=="TimeDomainComputing":
            newData = DlgData({},data[0])
            newData.addData("computeTime",data[1][0])
            newData.addData("filedAri",data[1][1])
            newData.addData("settingMode",data[1][2][0])
            newData.addData("radioEM",data[1][2][1])
            newData.addData("radioTE",data[1][2][2])
            newData.addData("radioTM",data[1][2][3])
            newData.addData("checkBoxStride",data[1][3][0])
            newData.addData("lineEditStride",data[1][3][1])
            newData.addData("checkBoxCharCont",data[1][4])
            newData.addData("Types",data[1][5])
            newData.addData("EveryNum",data[1][6])
            newData.addData("MaxNum",data[1][7])
            newData.addData("isChecked_part",data[1][8])
            newData.addData("checkBoxStep",data[1][9])
            newData.addData("computeTimeInterval",data[1][10])
            newData.addData("is_re",data[1][11])
            newData.addData("is_nonre",data[1][12])
            setComment(newData)
        if data[0]=="FiledSetting":
            newData = DlgData({},data[0])
            newData.addData("check_mag_x",data[1][0][0])
            newData.addData("mag_x",data[1][0][1])
            newData.addData("check_mag_y",data[1][1][0])
            newData.addData("mag_y",data[1][1][1])
            newData.addData("check_mag_z",data[1][2][0])
            newData.addData("mag_z",data[1][2][1])
            newData.addData("check_ele_x",data[1][3][0])
            newData.addData("ele_x",data[1][3][1])
            newData.addData("check_ele_y",data[1][4][0])
            newData.addData("ele_y",data[1][4][1])
            newData.addData("check_ele_z",data[1][5][0])
            newData.addData("ele_z",data[1][5][1])
            newData.addData("filedCustom",data[1][6])
            setComment(newData)
        if data[0]=="NewMaterical":
            newData = DlgData({},data[1][0])
            newData.addData("name",data[1][0])
            newData.addData("Dlg_Type","NewMaterical")
            newData.addData("ato_num",data[1][1])
            newData.addData("ato_mass_num",data[1][2])
            newData.addData("ato_desity",data[1][3])
            newData.addData("checkBox_conductivity",data[1][4][0])
            newData.addData("conductivity",data[1][4][1])
            newData.addData("checkBox_dielectric_constant",data[1][5][0])
            newData.addData("dielectric_constant",data[1][5][1])
            setComment(newData)
        
        if data[0]=="Species":
            FreeCAD.Console.PrintMessage("Species:"+str(data))
            # name
            newData=DlgData({},data[1][0])
            newData.addData("name",data[1][0])
            # type
            newData.addData("Dlg_Type","Species_Type")
            newData.addData("powerUnit",data[1][1])
            newData.addData("quality",data[1][2])
            newData.addData("massUnit",data[1][3])
            newData.addData("className",data[1][0])
            #加到Begin
            Comment = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict)
            Comment[newData.id] = newData.data
            FreeCAD.ActiveDocument.Begin = json.dumps(Comment)

        if data[0]=="WorkSpaceSettings":
            newData = DlgData({},data[0])
            newData.addData("name",data[1][0])
            newData.addData("start_X",data[1][1][0])
            newData.addData("end_X",data[1][1][1])
            newData.addData("stride_X",data[1][1][2])
            newData.addData("start_Y",data[1][2][0])
            newData.addData("end_Y",data[1][2][1])
            newData.addData("stride_Y",data[1][2][2])
            newData.addData("start_Z",data[1][3][0])
            newData.addData("end_Z",data[1][3][1])
            newData.addData("stride_Z",data[1][3][2])
            newData.addData("stride_Z", data[1][3][2])
            newData.addData("commit", data[1][4])
            setComment(newData)
            # 修改DX1-3
            # ObjectsTools.setDX1DX2DX3(data[1][1][2],data[1][2][2],data[1][3][2])
            FreeCAD.Console.PrintMessage("333")
        if data[0]=="RunOptions":
            newData = DlgData({}, data[0])
            newData.addData("checkBoxShowStructChart", data[1][0])
            newData.addData("CheckBoxPausedWhenStart", data[1][1])
            setComment(newData)
    Comm = json.loads(FreeCAD.ActiveDocument.Comment,object_pairs_hook=OrderedDict)

    return Comm


def setComment(DlgData):

    Comment = json.loads(FreeCAD.ActiveDocument.Comment,object_pairs_hook=OrderedDict)
    Comment[DlgData.id] = DlgData.data
    FreeCAD.ActiveDocument.Comment = json.dumps(Comment)







