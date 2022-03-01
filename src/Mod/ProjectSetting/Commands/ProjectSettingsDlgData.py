#-*- coding: utf-8 -*-
import json
import FreeCAD

from string import digits
#json格式数据需要保持原有顺序输出
from collections import OrderedDict

class ProjectSettingsDlgData:
    def __init__(self,data,id):
        self.data=data
        self.id=id

    def addData(self,key,value):
        self.data[key] = value

    def getData(self,key):
        try:
            self.data[key]
        except :
            return "NULL"
        else:
            return self.data[key]


def getDlgData():

    DataList=[]
    Comm = json.loads(FreeCAD.ActiveDocument.Comment,object_pairs_hook=OrderedDict)
    keys = Comm.keys()
    try:
        for i in keys:
            '''
            [[工作区间设置，
             [名称，
             [X范围最小，X范围最大，X范围的步长]，
             [Y范围最小，Y范围最大，Y范围的步长],
             [Z范围最小，Z范围最大，Z范围的步长]],
             是否提交
             ]]
            '''
            try:
                i = i.translate(None, digits)
            except:
                pass
                #加入一个标识决定是否要将其加入m3d中
            if i== "WorkSpaceSettings":
                # FreeCAD.Console.PrintMessage("\n断点2\n")
                # FreeCAD.Console.PrintMessage(Comm[i])
                try:
                    flag = Comm[i]["commit"]
                except:
                    DataList.append([i, [Comm[i]["name"],
                                         [Comm[i]["start_X"], Comm[i]["end_X"], Comm[i]["stride_X"]],
                                         [Comm[i]["start_Y"], Comm[i]["end_Y"], Comm[i]["stride_Y"]],
                                         [Comm[i]["start_Z"], Comm[i]["end_Z"], Comm[i]["stride_Z"]],
                                         True,
                                         ]])
                else:
                    DataList.append([i,[Comm[i]["name"],
                                       [Comm[i]["start_X"],Comm[i]["end_X"],Comm[i]["stride_X"]],
                                       [Comm[i]["start_Y"],Comm[i]["end_Y"],Comm[i]["stride_Y"]],
                                       [Comm[i]["start_Z"],Comm[i]["end_Z"],Comm[i]["stride_Z"]],
                                        flag,
                    ]])
            '''
            [[新材料，
            [名称，
            指定材料的原子序数，
            指定材料的原子质量，
            指定材料的密度，
            [指定材料电导体?，值]，
            [指定材料相对介电常数？，值]]
            ]]
            '''
            # if i== "NewMaterical":
            # if "NewMaterical" in i:i
            if Comm[i].has_key("Dlg_Type") and Comm[i]["Dlg_Type"]=="NewMaterical":
                DataList.append([Comm[i]["Dlg_Type"],[Comm[i]["name"],
                                    Comm[i]["ato_num"],
                                    Comm[i]["ato_mass_num"],
                                    Comm[i]["ato_desity"],
                                    [Comm[i]["checkBox_conductivity"],Comm[i]["conductivity"]],
                                    [Comm[i]["checkBox_dielectric_constant"],Comm[i]["dielectric_constant"]],
                ]])     
            '''
            [[场设置，
            [[静磁场X方向？，值]，
            [静磁场Y方向？，值],
            [静磁场Z方向？，值]，
            [静电场X方向？，值]，
            [静电场Y方向？，值],
            [静电场Z方向？，值]，
            自定义]]
            '''
            if i == "FiledSetting":
                DataList.append([i,[[Comm[i]["check_mag_x"],Comm[i]["mag_x"]],
                                          [Comm[i]["check_mag_y"],Comm[i]["mag_y"]],
                                          [Comm[i]["check_mag_z"],Comm[i]["mag_z"]],
                                          [Comm[i]["check_ele_x"],Comm[i]["ele_x"]],
                                          [Comm[i]["check_ele_y"],Comm[i]["ele_y"]],
                                          [Comm[i]["check_ele_z"],Comm[i]["ele_z"]],
                                    Comm[i]["filedCustom"],
                ]])    
            '''
            [[时域计算设置，
            [场算法，
            [设置模式？，EM？，TE？，TM？]，
            [设置步长？，值]，
            设置电荷连续性？]
            ]]
            '''
            if i== "TimeDomainComputing":
                DataList.append([i,[Comm[i]["computeTime"], 
                                          Comm[i]["filedAri"],
                                          [Comm[i]["settingMode"],Comm[i]["radioEM"],Comm[i]["radioTE"],Comm[i]["radioTM"]],
                                          [Comm[i]["checkBoxStride"],Comm[i]["lineEditStride"]],
                                          Comm[i]["checkBoxCharCont"],
                                          Comm[i]["Types"],Comm[i]["EveryNum"],
                                          Comm[i]["MaxNum"],Comm[i]["isChecked_part"],
                                          Comm[i]["checkBoxStep"],Comm[i]["computeTimeInterval"],
                                          Comm[i]["is_re"],Comm[i]["is_nonre"]
                ]])  

            '''
            [[数据处理设置，
            [时间观测？，
            空间观测？，
            等位图数据？，
            矢量图数据？，
            相位空间数据？，
            [设置文件前缀？，值]，
            [设置文件后缀？，值]，
            [文本格式？，二进制格式？]
            ]]
            '''        
            if i== "DataProcessingSetting":
                DataList.append([i,[Comm[i]["time_obser"],
                                          Comm[i]["space_obser"],
                                          Comm[i]["contor_plot"],
                                          Comm[i]["vector_data"],
                                          Comm[i]["phase_space"],
                                          [Comm[i]["checkBox_prefix"],Comm[i]["lineEdit_prefix"]],
                                          [Comm[i]["checkBox_suffix"],Comm[i]["lineEdit_suffix"]],
                                          [Comm[i]["text_form"],Comm[i]["binary_form"]]
                ]])        
            '''
            [[模型信息，
             [模型，
             作者，
             公司，
             备注，]
             ]]
            '''  
            if i == "ModelingInfo":
                DataList.append([i,[Comm[i]["modeling"],
                                    Comm[i]["author"],
                                    Comm[i]["company"],
                                    Comm[i]["remarks"],
                
                ]])       
            '''
            [[运行选项设置，
            [开始计算时显示结构图，
            开始计算时处于暂停状态，]
            ]]
            '''                        
            if i=="RunOptions":
                DataList.append([i,[Comm[i]["checkBoxShowStructChart"],
                                    Comm[i]["CheckBoxPausedWhenStart"],
                ]])
    except KeyError as reason:
        FreeCAD.Console.PrintError("\n这里出现问题1111")
        sayz("!!!Error:KeyError,Maybe lack of key:%s"%str(reason))
    return DataList




def sayz(msg):
    FreeCAD.Console.PrintMessage("--------------------------------------------")
    FreeCAD.Console.PrintMessage('\n')
    FreeCAD.Console.PrintMessage(msg)
    FreeCAD.Console.PrintMessage('\n')  