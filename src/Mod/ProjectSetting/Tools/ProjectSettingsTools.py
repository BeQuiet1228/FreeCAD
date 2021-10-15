#-*- coding: utf-8 -*-
import json
import FreeCAD
from Modeling.Common.Tools import CoordinateSystemTools,ObjectsTools
from Modeling.Common.Tools.ObjectsTools import getRangeOfAllObjs
#json格式数据需要保持原有顺序输出
from collections import OrderedDict
'''
新建文档时，对所有的工程设置进行初始化
将初始化信息写入json
'''
def initPrjectSettings():
    # 直角坐标系
    if FreeCAD.ActiveDocument.CoordinateSystem==CoordinateSystemTools.CoordinateType.Rectangular: 
        # ObjectsTools.setDX1DX2DX3("1mm","1mm","1mm")
        # Comment = json.loads(FreeCAD.ActiveDocument.Comment,object_pairs_hook=OrderedDict)
        Comment={"RunOptions": {"checkBoxShowStructChart": True, "CheckBoxPausedWhenStart": False}, 
                "WorkSpaceSettings": {"end_Z": "0mm", "end_Y": "0mm", "end_X": "0mm", "name": "SIMUVOLUME", "start_Z": "0mm", "start_X": "0mm", "start_Y": "0mm", "stride_Z": "1mm", "stride_X": "1mm", "stride_Y": "1mm","commit":False,"WhetherToHitOkOrNot":False},
                "TimeDomainComputing": {"checkBoxCharCont": False, "filedAri": u"\u65f6\u504fFDTD", "lineEditStride": "0.01", "radioEM": True, "computeTime": "20", "radioTE": False, "checkBoxStride": False, "settingMode": False, "radioTM": False,"Types":"ALL","EveryNum":"1","MaxNum":"50000","isChecked_part":False,"checkBoxStep":False,"computeTimeInterval":"1","is_re":False,"is_nonre":True}, 
                "ModelingInfo": {"remarks": "NONE", "modeling": "NONE", "company": "NONE", "author": "NONE"},
                "DataProcessingSetting": {"checkBox_prefix": False, "lineEdit_prefix": "", "contor_plot": False, "phase_space": False, "vector_data": False, "text_form": True, "binary_form": False, "space_obser": False, "time_obser": False, "checkBox_suffix": False, "lineEdit_suffix": ""}}
        FreeCAD.ActiveDocument.Comment = json.dumps(Comment)
    elif FreeCAD.ActiveDocument.CoordinateSystem==CoordinateSystemTools.CoordinateType.Polar:
        # Comment = json.loads(FreeCAD.ActiveDocument.Comment,object_pairs_hook=OrderedDict)
                # {"RunOptios": {"checkBoxShowStructChart": true, "CheckBoxPausedWhenStart": false}, 
                # "WorkSpaceSettings": {"end_Z": "0mm", "end_Y": "0mm", "end_X": "0mm", "start_Z": "0mm", "name": "SIMUVOLUME", "start_X": "0mm", "start_Y": "0mm", "stride_Z": "1mm", "stride_X": "1mm", "stride_Y": "1mm"}, 
                # "TimeDomainComputing": {"checkBoxCharCont": false, "filedAri": "\\u65f6\\u504fFDTD", "radioTE": false, "lineEditStride": "0.01", "radioEM": true, "checkBoxStride": false, "computeTime": "20", "settingMode": false, "radioTM": false},
                # "DataProcessingSetting": {"contor_plot": False, "vector_data": False, "binary_form": false, "checkBox_suffix": false, "lineEdit_suffix": "", "checkBox_prefix": false, "lineEdit_prefix": "", "phase_space": False, "text_form": true, "space_obser": False, "time_obser": False}, 
                # "ModelingInfo": {"remarks": "NONE", "modeling": "NONE", "company": "NONE", "author": "NONE"}}
        # ObjectsTools.setDX1DX2DX3("1mm","30deg","1mm")
        Comment={"RunOptions": {"checkBoxShowStructChart": True, "CheckBoxPausedWhenStart": False}, 
                 "WorkSpaceSettings": {"end_Z": "0mm", "end_Y": "360deg", "end_X": "0mm", "name": "SIMUVOLUME", "start_Z": "0mm", "start_X": "0mm", "start_Y": "0deg", "stride_Z": "1mm", "stride_X": "1mm", "stride_Y": "18deg","commit":False,"WhetherToHitOkOrNot":False},
                 "TimeDomainComputing": {"checkBoxCharCont": False, "filedAri": u"\u65f6\u504fFDTD", "lineEditStride": "0.01", "radioEM": True, "computeTime": "20", "radioTE": False, "checkBoxStride": False, "settingMode": False, "radioTM": False,"Types":"ALL","EveryNum":"1","MaxNum":"50000","isChecked_part":False,"checkBoxStep":False,"computeTimeInterval":"1","is_re":False,"is_nonre":True}, 
                 "DataProcessingSetting": {"checkBox_prefix": False, "lineEdit_prefix": "", "contor_plot": False, "phase_space": False, "vector_data": False, "text_form": True, "binary_form": False, "space_obser": False, "time_obser": False, "checkBox_suffix": False, "lineEdit_suffix": ""}, 
                 "ModelingInfo": {"remarks": "NONE", "modeling": "NONE", "company": "NONE", "author": "NONE"}}
        FreeCAD.ActiveDocument.Comment = json.dumps(Comment)
    else:
        # ObjectsTools.setDX1DX2DX3("1mm","1mm","30deg")
        Comment={"RunOptions": {"checkBoxShowStructChart": True, "CheckBoxPausedWhenStart": False}, 
                "ModelingInfo": {"remarks": "NONE", "modeling": "NONE", "company": "NONE", "author": "NONE"}, 
                "TimeDomainComputing": {"checkBoxCharCont": False, "filedAri": u"\u65f6\u504fFDTD", "lineEditStride": "0.01", "radioEM": True, "computeTime": "20", "radioTE": False, "checkBoxStride": False, "settingMode": False, "radioTM": False,"Types":"ALL","EveryNum":"1","MaxNum":"50000","isChecked_part":False,"checkBoxStep":False,"computeTimeInterval":"1","is_re":False,"is_nonre":True}, 
                "DataProcessingSetting": {"checkBox_prefix": False, "lineEdit_prefix": "", "contor_plot": False, "phase_space": False, "vector_data": False, "text_form": True, "binary_form": False, "space_obser": False, "time_obser": False, "checkBox_suffix": False, "lineEdit_suffix": ""}, 
                "WorkSpaceSettings": {"end_Z": "360deg", "end_Y": "0mm", "end_X": "0mm", "name": "SIMUVOLUME", "start_Z": "0deg", "start_X": "0mm", "start_Y": "0mm", "stride_Z": "18deg", "stride_X": "1mm", "stride_Y": "1mm","commit":False,"WhetherToHitOkOrNot":False}}
        FreeCAD.ActiveDocument.Comment = json.dumps(Comment)

"""
模型中参数point发生变化时实时更新WorkSpaceSettings中的范围
"""
# def updateRangeOfWorkSpaceSettings(minX,minY,minZ,maxX,maxY,maxZ):
#     JSON_CADComment = json.loads(FreeCAD.ActiveDocument.Comment,object_pairs_hook=OrderedDict)
#     DlgData = JSON_CADComment["WorkSpaceSettings"]
#     # DlgData.addData("name", DlgData["name"])
#     # DlgData.addData("stride_X", DlgData["name"])
#     # DlgData.addData("stride_Y", DlgData["name"])
#     # DlgData.addData("stride_Z", DlgData["name"])
#     if FreeCAD.ActiveDocument.CoordinateSystem == CoordinateSystemTools.CoordinateType.Rectangular:
#         DlgData["start_X"] = str(min(minX, float(DlgData["start_X"].split("mm")[0])))+"mm"
#         DlgData["end_X"] = str(max(maxX, float(DlgData["end_X"].split("mm")[0])))+"mm"
#         DlgData["start_Y"] = str(min(minY, float(DlgData["start_Y"].split("mm")[0]))) + "mm"
#         DlgData["end_Y"] = str(max(maxY, float(DlgData["end_Y"].split("mm")[0]))) + "mm"
#         DlgData["start_Z"] = str(min(minZ, float(DlgData["start_Z"].split("mm")[0]))) + "mm"
#         DlgData["end_Z"] = str(max(maxZ, float(DlgData["end_Z"].split("mm")[0]))) + "mm"
#     elif FreeCAD.ActiveDocument.CoordinateSystem == CoordinateSystemTools.CoordinateType.Polar:
#         DlgData["start_X"] = str(min(minX, float(DlgData["start_X"].split("mm")[0]))) + "mm"
#         DlgData["end_X"] = str(max(maxX, float(DlgData["end_X"].split("mm")[0]))) + "mm"
#         DlgData["start_Y"] = str(min(minY, float(DlgData["start_Y"].split("deg")[0]))) + "deg"
#         DlgData["end_Y"] = str(max(maxY, float(DlgData["end_Y"].split("deg")[0]))) + "deg"
#         DlgData["start_Z"] = str(min(minZ, float(DlgData["start_Z"].split("mm")[0]))) + "mm"
#         DlgData["end_Z"] = str(max(maxZ, float(DlgData["end_Z"].split("mm")[0]))) + "mm"
#     else:
#         DlgData["start_X"] = str(min(minX, float(DlgData["start_X"].split("mm")[0]))) + "mm"
#         DlgData["end_X"] = str(max(maxX, float(DlgData["end_X"].split("mm")[0]))) + "mm"
#         DlgData["start_Y"] = str(min(minY, float(DlgData["start_Y"].split("mm")[0]))) + "mm"
#         DlgData["end_Y"] = str(max(maxY, float(DlgData["end_Y"].split("mm")[0]))) + "mm"
#         DlgData["start_Z"] = str(min(minZ, float(DlgData["start_Z"].split("deg")[0]))) + "deg"
#         DlgData["end_Z"] = str(max(maxZ, float(DlgData["end_Z"].split("deg")[0]))) + "deg"
#     FreeCAD.Console.PrintMessage(DlgData)
#
#     FreeCAD.Console.PrintMessage("\n")
#     FreeCAD.Console.PrintMessage(str(max(maxZ, DlgData["end_Z"].split("mm")[0])) + "mm")
#     FreeCAD.Console.PrintMessage(DlgData["end_Z"].split("mm")[0])
#
#
#     FreeCAD.ActiveDocument.Comment = json.dumps(JSON_CADComment)

def updateRangeOfWorkSpaceSettings():
    # 获取工作区域的范围
    minPoint, maxPoint = getRangeOfAllObjs()

    if minPoint!=[] and maxPoint!=[]:
        JSON_CADComment = json.loads(FreeCAD.ActiveDocument.Comment,object_pairs_hook=OrderedDict)
        DlgData = JSON_CADComment["WorkSpaceSettings"]
        DlgData["start_X"] = minPoint[0]
        DlgData["end_X"] = maxPoint[0]
        DlgData["start_Y"] = minPoint[1]
        DlgData["end_Y"] = maxPoint[1]
        DlgData["start_Z"] = minPoint[2]
        DlgData["end_Z"] = maxPoint[2]
        FreeCAD.ActiveDocument.Comment = json.dumps(JSON_CADComment)