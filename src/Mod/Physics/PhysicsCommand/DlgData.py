#-*- coding: utf-8 -*-
import json

import PySide

from Modeling.Common.Tools import ObjectsTools
import FreeCAD
#json格式数据需要保持原有顺序输出
from collections import OrderedDict


class DlgData:
    def __init__(self,data,id):
        self.data=data
        self.id = id
    def addData(self,key,value):
        self.data[key] = value
    def getData(self,key):
        try:
            self.data[key]
        except :
            return "NULL"
        else:
            return self.data[key]
            
def Em_loadData(UI,DlgData,Type):     
    try:  
        UI.LineEdit_Name.setText(DlgData.data['name'])
        UI.ComboBox_Shadow.setCurrentIndex(UI.ComboBox_Shadow.findText(DlgData.data['Emitter']))
        if Type == "EMB_TYPE":
            # 束电流密度
            UI.LineEdit_BeamJ.setText(DlgData.data['BeamJ'])    
            # 束电压参量
            UI.LineEdit_BeamV.setText(DlgData.data['BeamV'])        
        if Type == "EME_TYPE":
            # 爆炸式发射
            UI.checkBox_TField.setChecked(DlgData.data['TField_Checked'])  
            UI.LineEdit_TField.setEnabled(DlgData.data['TField_Checked'])
            UI.LineEdit_TField.setText(DlgData.data['TField'])
            # 空间余场
            UI.checkBox_RField.setChecked(DlgData.data['RField_Checked'])
            UI.LineEdit_RField.setEnabled(DlgData.data['RField_Checked'])
            UI.LineEdit_RField.setText(DlgData.data['RField'])
            # 最小电荷
            UI.checkBox_Charg.setChecked(DlgData.data['Charg_Checked'])
            UI.LineEdit_Charg.setEnabled(DlgData.data['Charg_Checked'])
            UI.LineEdit_Charg.setText(DlgData.data['Charg'])
            # 等离子
            UI.checkBox_FRate.setChecked(DlgData.data['FRate_Checked'])
            UI.LineEdit_FRate.setEnabled(DlgData.data['FRate_Checked'])
            UI.LineEdit_FRate.setText(DlgData.data['FRate'])
        if Type == "EMG_TYPE":
            # 束电流I(T) 
            UI.LineEdit_IT.setText(DlgData.data['Beam_Current'])     
            # 引导磁场
            UI.LineEdit_magnetic.setText(DlgData.data['Guiding_Magnetic_Field'])        
            # 引导半径
            UI.LineEdit_radius.setText(DlgData.data['Guiding_Radius'])    
            # 纵向动量
            UI.LineEdit_VerticalMomentum.setText(DlgData.data['Vertical_Momentum'])  
            # 横向动量
            UI.LineEdit_HorizontalMomentum.setText(DlgData.data['Horizontal_Momentum'])   
            # 引导轴线方向
            # 修改old打开时，引导轴方向不正确的问题 @lzg
            if DlgData.data['Axias'] == "X":
                UI.radioButton_AxiasX.setChecked(True)
            elif DlgData.data['Axias'] == "Y":
                UI.radioButton_AxiasY.setChecked(True)
            else:
                UI.radioButton_AxiasZ.setChecked(True)                                
            # 发射中心坐标      
            UI.LineEdit_LaunchX.setText(DlgData.data['LaunchCoordinate_X'])   
            UI.LineEdit_LaunchY.setText(DlgData.data['LaunchCoordinate_Y'])  
            UI.LineEdit_LaunchZ.setText(DlgData.data['LaunchCoordinate_Z'])                           
        if Type == "EMH_TYPE":
            # Fowler-Nordheim常数.A
            UI.LineEdit_FNA.setText(DlgData.data['Fowler_Nordheim_A'])     
            # Fowler-Nordheim常数.B
            UI.LineEdit_FNB.setText(DlgData.data['Fowler_Nordheim_B'])    
            # 工作函数PHI
            UI.LineEdit_PHI.setText(DlgData.data['PHI']) 
        if Type == "EMT_TYPE":
            # 工作函数WF
            UI.LineEdit_WF.setText(DlgData.data['WF'])       
            # 工作温度TP
            UI.LineEdit_TP.setText(DlgData.data['TP'])              
        # 粒子类型
        UI.checkBox_particleType.setChecked(DlgData.data['particleType_Checked'])
        UI.ComboBox_particleType.setEnabled(DlgData.data['particleType_Checked'])
        UI.ComboBox_particleType.setCurrentIndex(DlgData.data['particleType'])
        # 产生率
        UI.checkBox_generationRate.setChecked(DlgData.data['generationRate_Checked'])
        UI.spinBox_generationRate.setEnabled(DlgData.data['generationRate_Checked'])
        UI.spinBox_generationRate.setValue(DlgData.data['generationRate'])        

        # 发射间隔
        UI.checkBox_transmittingInterval.setChecked(DlgData.data['transmittingInterval_Checked'])
        UI.radioButton_random.setEnabled(DlgData.data['transmittingInterval_Checked'])
        UI.radioButton_strictTiming.setEnabled(DlgData.data['transmittingInterval_Checked'])  
        UI.spinBox_timesStep.setEnabled(DlgData.data['transmittingInterval_Checked'])
        UI.spinBox_timesStep.setValue(DlgData.data['stepMultiple'])

        # 沿表面分布
        UI.checkBox_surface.setChecked(DlgData.data['surface_Checked'])
        UI.radioButton_randomm.setEnabled(DlgData.data['surface_Checked'])
        UI.radioButton_uniform.setEnabled(DlgData.data['surface_Checked'])  
        UI.radioButton_fixed.setEnabled(DlgData.data['surface_Checked']) 

        # 沿外表面分布 
        UI.checkBox_outSurface.setChecked(DlgData.data['outSurface_Checked'])
        UI.radioButton_randommm.setEnabled(DlgData.data['outSurface_Checked'])
        UI.radioButton_alongOutsideFixed.setEnabled(DlgData.data['outSurface_Checked'])
        UI.LineEdit_Dn.setEnabled(DlgData.data['outSurface_Checked'])

        # 偏移
        UI.LineEdit_Dn.setText(DlgData.data['Dn'])

        # 发射区域选项
        UI.ComboBox_notInclued.setCurrentIndex(UI.ComboBox_notInclued.findText(DlgData.data['Zone1']))
        UI.ComboBox_notIncludedd.setCurrentIndex(UI.ComboBox_notIncludedd.findText(DlgData.data['Zone2']))
        UI.ComboBox_included.setCurrentIndex(UI.ComboBox_included.findText(DlgData.data['Zone11']))
        UI.ComboBox_includedd.setCurrentIndex(UI.ComboBox_includedd.findText(DlgData.data['Zone22']))
        if DlgData.data['outSurface'] == "RANDOM":
            UI.radioButton_randommm.setChecked(True) 
        else:
            UI.radioButton_alongOutsideFixed.setChecked(True) 
        if DlgData.data['surface'] == "RANDOM":
            UI.radioButton_randomm.setChecked(True)
        if DlgData.data['surface'] == "UNIFORM":
            UI.radioButton_uniform.setChecked(True)
        if DlgData.data['surface'] == "FIXED":
            UI.radioButton_fixed.setChecked(True)  
        if DlgData.data['transmittingInterval'] == "RANDOM_TIMING":
            UI.radioButton_random.setChecked(True)
        else:
            UI.radioButton_strictTiming.setChecked(True)                                
    except KeyError as reason:
        sayz("!!!Error:Em_loadData,KeyError,Maybe lack of key:%s"%str(reason))
def Em_keepData(UI,DlgData,Type):
    if Type == "EMB_TYPE":
        # 束电流密度
        # 因需要将LineEdit切换为TextEdit，此处.text()进行修改 @lizhenguang
        DlgData.addData("BeamJ",UI.LineEdit_BeamJ.toPlainText())        
        # 束电压参量
        DlgData.addData("BeamV",UI.LineEdit_BeamV.toPlainText())   
        DlgData.addData("Dlg_Type","EMB_Type")  
        DlgData.addData("Same_Parent_Diff","EmB")  
        
    if Type == "EME_TYPE":
        # 爆炸式发射
        DlgData.addData("TField_Checked",UI.checkBox_TField.isChecked())
        DlgData.addData("TField",UI.LineEdit_TField.toPlainText())        
        # 空间余场
        DlgData.addData("RField_Checked",UI.checkBox_RField.isChecked())
        DlgData.addData("RField",UI.LineEdit_RField.toPlainText())
        # 最小电荷
        DlgData.addData("Charg_Checked",UI.checkBox_Charg.isChecked())
        DlgData.addData("Charg",UI.LineEdit_Charg.toPlainText())  
        # 等离子
        DlgData.addData("FRate_Checked",UI.checkBox_FRate.isChecked())
        DlgData.addData("FRate",UI.LineEdit_FRate.toPlainText()) 
        DlgData.addData("Dlg_Type","EME_Type") 
        DlgData.addData("Same_Parent_Diff","EmE") 
    if Type == "EMG_TYPE":
        # 束电流I(T) 
        DlgData.addData("Beam_Current",UI.LineEdit_IT.text())        
        # 引导磁场
        DlgData.addData("Guiding_Magnetic_Field",UI.LineEdit_magnetic.text())         
        # 引导半径
        DlgData.addData("Guiding_Radius",UI.LineEdit_radius.text())       
        # 纵向动量
        DlgData.addData("Vertical_Momentum",UI.LineEdit_VerticalMomentum.text())   
        # 横向动量
        DlgData.addData("Horizontal_Momentum",UI.LineEdit_HorizontalMomentum.text())   
        # 速度分布
        
        # FreeCAD.Console.PrintError('\n开始添加数据')
        DlgData.addData("isCheckedVelocity",UI.isCheckvelocity.isChecked())
        DlgData.addData("velocity_spread", UI.lineEdit_velocity.text())
        # FreeCAD.Console.PrintError('\n添加数据成功')
        # 引导轴线方向
        DlgData.addData("isX1",UI.radioButton_AxiasX.isChecked())
        DlgData.addData("isX2",UI.radioButton_AxiasY.isChecked())
        DlgData.addData("isX3",UI.radioButton_AxiasZ.isChecked())
        if UI.radioButton_AxiasX.isChecked():
            DlgData.addData("Axias","X")
        elif UI.radioButton_AxiasY.isChecked():
            DlgData.addData("Axias","Y") 
        else:
            DlgData.addData("Axias","Z")             
        # 发射中心坐标      
        DlgData.addData("LaunchCoordinate_X",UI.LineEdit_LaunchX.text())      
        DlgData.addData("LaunchCoordinate_Y",UI.LineEdit_LaunchY.text())
        DlgData.addData("LaunchCoordinate_Z",UI.LineEdit_LaunchZ.text())  
        DlgData.addData("Dlg_Type","EMG_Type")  
        DlgData.addData("Same_Parent_Diff","EmG") 
        # FreeCAD.Console.PrintError('\n添加数据成功')
    if Type == "EMH_TYPE":
        # Fowler-Nordheim常数.A
        DlgData.addData("Fowler_Nordheim_A",UI.LineEdit_FNA.text())        
        # Fowler-Nordheim常数.B
        DlgData.addData("Fowler_Nordheim_B",UI.LineEdit_FNB.text())   
        # 工作函数PHI
        # @lizhenguang
        DlgData.addData("PHI",UI.LineEdit_PHI.toPlainText()) 
        DlgData.addData("Dlg_Type","EMH_Type")  
        DlgData.addData("Same_Parent_Diff","EmH")        
    if Type == "EMT_TYPE":
        # 工作函数WF
        DlgData.addData("WF",UI.LineEdit_WF.toPlainText())        
        # 工作温度TP
        DlgData.addData("TP",UI.LineEdit_TP.toPlainText()) 
        DlgData.addData("Dlg_Type","EMT_Type")    
        DlgData.addData("Same_Parent_Diff","EmT")
#################共有的部分########################

    DlgData.addData("name",DlgData.id)
    DlgData.addData("Emitter",UI.ComboBox_Shadow.currentText())
    if UI.ComboBox_Shadow.currentText() == u'未指定':
        DlgData.addData("isEmit",False)
    else:
        
        ObjectsTools.findObjByLabelWithoutOrderAndInvisible(UI.ComboBox_Shadow.currentText())
        DlgData.addData("isEmit",True)

    # 粒子类型
    DlgData.addData("particleType_Checked",UI.checkBox_particleType.isChecked())      
    if UI.ComboBox_particleType.currentIndex() == 0:
        DlgData.addData("particleType",0)
        DlgData.addData("Species","ELECTRON")
    else:
        DlgData.addData("particleType",1)
        DlgData.addData("Species","PROTON")

    # 产生率
    DlgData.addData("generationRate_Checked",UI.checkBox_generationRate.isChecked())
    DlgData.addData("generationRate",UI.spinBox_generationRate.value())    
  
    # 发射间隔 
    DlgData.addData("transmittingInterval_Checked",UI.checkBox_transmittingInterval.isChecked())
    if UI.radioButton_random.isChecked():
        DlgData.addData("transmittingInterval","RANDOM_TIMING") 
    else:
        DlgData.addData("transmittingInterval","TIMING")  
    DlgData.addData("stepMultiple",UI.spinBox_timesStep.value())    
      
    # 沿表面分布       
    DlgData.addData("surface_Checked",UI.checkBox_surface.isChecked())
    if UI.radioButton_randomm.isChecked():
        DlgData.addData("surface","RANDOM") 
    elif UI.radioButton_uniform.isChecked():
        DlgData.addData("surface","UNIFORM")
    else:
        DlgData.addData("surface","FIXED")        

    # 沿外表面分布       
    DlgData.addData("outSurface_Checked",UI.checkBox_outSurface.isChecked())
    if UI.radioButton_randommm.isChecked():
        DlgData.addData("outSurface","RANDOM") 
    else:
        DlgData.addData("outSurface","FIXED") 
    # 偏移
    # 将LineEdit切换为TextEdit，切换text() @lizhenguang

    if not type(UI.LineEdit_Dn) == PySide.QtGui.QLineEdit:
        DlgData.addData("Dn", UI.LineEdit_Dn.toPlainText())
    else:
        DlgData.addData("Dn", UI.LineEdit_Dn.text())

    # 发射区域选项
    DlgData.addData("Zone1",UI.ComboBox_notInclued.currentText())
    DlgData.addData("Zone2",UI.ComboBox_notIncludedd.currentText())
    DlgData.addData("Zone11",UI.ComboBox_included.currentText())
    DlgData.addData("Zone22",UI.ComboBox_includedd.currentText())
    
    if UI.ComboBox_notInclued.currentText() == u'不指定':
        DlgData.addData("isExclude1",False)
    else:
        DlgData.addData("isExclude1",True)
        ObjectsTools.findObjByLabelWithoutOrderAndInvisible(UI.ComboBox_notInclued.currentText())

    if UI.ComboBox_notIncludedd.currentText() == u'不指定':
        DlgData.addData("isExclude2",False)
    else:
        DlgData.addData("isExclude2",True)
        ObjectsTools.findObjByLabelWithoutOrderAndInvisible(UI.ComboBox_notIncludedd.currentText())

    if UI.ComboBox_included.currentText() == u'不指定':
        DlgData.addData("isInclude1",False)
    else:
        DlgData.addData("isInclude1",True)
        ObjectsTools.findObjByLabelWithoutOrderAndInvisible(UI.ComboBox_included.currentText())

    if UI.ComboBox_includedd.currentText() == u'不指定':
        DlgData.addData("isInclude2",False)
    else:
        DlgData.addData("isInclude2",True)
        ObjectsTools.findObjByLabelWithoutOrderAndInvisible(UI.ComboBox_includedd.currentText())

    Comment = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict)
    old = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict)
    Comment[DlgData.id] = DlgData.data
    FreeCAD.ActiveDocument.Begin = json.dumps(Comment)
    # 返回面板中的内容是否改变
    return cmp(old, Comment) != 0

# 获取当前激活场景中所有的模型对象及具体信息
def getDlgData():
    # 修改json文件的函数，由于没有找到打开文件的函数，所以暂时放在这里 @ 李振广
    # try:
    #     from Modeling.Common.CommonCommand import NewDocument
    #     NewDocument.ModifythejosnFile()
    # except:
    #     pass

    DataList=[]
    Comm = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict)
    for key, value in Comm.items():
        for k,v in value.items():
            if isinstance(Comm[key][k],basestring):
                Comm[key][k]=Comm[key][k].replace('\n', '').replace('\r', '').replace(' ', '').replace('\t', '')
    keys = Comm.keys()
    try:
        #按面板分类的顺序得到DataList
        #代码修改少，但是面板变多时耗时长，后期如果问题严重还是得优化
        #目前的顺序差不多是图标的顺序
        '''
            [[Sol_Type,[名称，
                       [Z中心，R中中，线圈半长，内半径，外半径，线圈匝数]，
                       [非均匀X?, ...Y?, ...Z?, 非均匀网格X值， ...Y..,  ...Z..],
                       材料设置，
                       [均匀场因子，R因子，Z因子，占空比，内半径，外半径，磁导率，theta角度，phi角度]
                       ]]]
            '''
        for i in keys:
            if Comm[i]["Dlg_Type"]=="Sol_Type":
                # DataList.append([Comm[i]["Dlg_Type"],[Comm[i]["name"],
                #                                      [Comm[i]["Center_Z"],Comm[i]["Center_R"],Comm[i]["Half_Circle"],Comm[i]["Radius_In"],Comm[i]["Radius_Out"],Comm[i]["Turns"]],
                #                                      [Comm[i]["DX_R_Checked"],Comm[i]["DX_Y_Checked"],Comm[i]["DX_Z_Checked"],Comm[i]["DX_R"],Comm[i]["DX_Y"],Comm[i]["DX_Z"]],
                #                                      Comm[i]["Material"],
                #                                      [Comm[i]["Shimming_Factor"],Comm[i]["Factor_R"],Comm[i]["Factor_Z"],Comm[i]["Duty"],Comm[i]["_RADIUSIN"],Comm[i]["_RADIUSOUT"],Comm[i]["Permeability"],Comm[i]["Coil_Current"],Comm[i]["THETA"],Comm[i]["PHI"]]
                #                                      ]])
                DataList.append([Comm[i]["Dlg_Type"],[Comm[i]["Shimming_Factor"], Comm[i]["name"], Comm[i]["Center_Z"], Comm[i]["Center_R"],
                                Comm[i]["Radius_In"], Comm[i]["Radius_Out"], Comm[i]["Coil_Current"], Comm[i]["Half_Circle"],
                                Comm[i]["Turns"], Comm[i]["THETA"], Comm[i]["PHI"], Comm[i]["Factor_R"],
                                Comm[i]["Factor_Z"], Comm[i]["Duty"], Comm[i]["_RADIUSIN"], Comm[i]["_RADIUSOUT"],
                                Comm[i]["Permeability"]]])
        '''
            [[Exp_Type,[名称，
                        类型，
                        [起点坐标R, ...θ, ...Z,止点坐标R, ...θ, ...Z],
                        指定电流密度，
                        函数JFUNC]]]
            '''
        for i in keys:
            if Comm[i]["Dlg_Type"]=="ExP_Type":
                DataList.append([Comm[i]["Dlg_Type"],[Comm[i]["name"],
                                                      Comm[i]["Current_Source"],
                                                      [Comm[i]["start_R"],Comm[i]["start_Y"],Comm[i]["start_Z"],Comm[i]["end_R"],Comm[i]["end_Y"],Comm[i]["end_Z"]],
                                                      Comm[i]["Specified_Current_Density"],
                                                      Comm[i]["JFUNC"],
                                                      Comm[i]["source_type"]
                                                      ]])
            '''
            [[Foil_Type],[名称，
                          类型波箔片，
                          [起点R, ...θ, ...Z, 止点R, ...θ, ...Z]，
                          厚度，
                          [自定义材料？ ， 值（指定材料的值或者默认材料的值）,默认材料？， 默认值]
                          ]]
            '''
        for i in keys:
            if Comm[i]["Dlg_Type"]=="Foil_Type":
                DataList.append([Comm[i]["Dlg_Type"],[Comm[i]["name"],
                                                      Comm[i]["Orthogonal_projection_surface"],
                                                      [Comm[i]["start_R"],Comm[i]["start_Y"],Comm[i]["start_Z"],Comm[i]["end_R"],Comm[i]["end_Y"],Comm[i]["end_Z"]],
                                                      Comm[i]["thick"],
                                                      [Comm[i]["checkBox_CustomMaterial"],Comm[i]["CustomMaterial"],Comm[i]["checkBox_DefaultMaterial"],Comm[i]["defaultMaterial"]],
                                                      ]])
            '''
            [[Ind_Type],[名称，
                         类型电感，
                         [起点R， ...θ， ...Z, 止点R, ...θ, ...Z],
                         线圈直径，
                         [自感系数？， 值]
                         ]]]
            '''
        for i in keys:
            if Comm[i]["Dlg_Type"]=="Ind_Type":
                DataList.append([Comm[i]["Dlg_Type"],[Comm[i]["name"],
                                                      Comm[i]["Orthogonal_projection_surface"],
                                                      [Comm[i]["start_R"],Comm[i]["start_Y"],Comm[i]["start_Z"],Comm[i]["end_R"],Comm[i]["end_Y"],Comm[i]["end_Z"]],
                                                      Comm[i]["Diam"],
                                                      [Comm[i]["INDUC_Checked"],Comm[i]["INDUC"]],
                                                      ]])
        for i in keys:
        
            if Comm[i]["Dlg_Type"] == "Port_Type":
                DataList.append([Comm[i]["Dlg_Type"],[Comm[i]["name"],Comm[i]["direction"],Comm[i]["vport_Checked"],
                Comm[i]["vport"],Comm[i]["scale_Checked"],Comm[i]["scale"],Comm[i]["Ft_Checked"],Comm[i]["Ft"],
                Comm[i]["GE2_Checked"],Comm[i]["geFirstName"],Comm[i]["geFirstVal"],
                Comm[i]["GE3_Checked"],Comm[i]["geSecondName"],Comm[i]["geSecondVal"],
                Comm[i]["FT_Checked"],Comm[i]["isNewConformalLine"],Comm[i]["FT+"],
                Comm[i]["lap_Checked"],Comm[i]["Laplace1"],Comm[i]["Laplace2"],
                Comm[i]["isAppointArea"],Comm[i]["Orthogonal_projection_surface"],
                [Comm[i]["start_R"],Comm[i]["start_Y"],Comm[i]["start_Z"]],
                [Comm[i]["end_R"],Comm[i]["end_Y"],Comm[i]["end_Z"]],
                Comm[i]["DX_R_Checked"],Comm[i]["DX_Y_Checked"], Comm[i]["DX_Z_Checked"],
                Comm[i]["DX_R"],Comm[i]["DX_Y"],Comm[i]["DX_Z"],
                Comm[i]["Laplace1_number"],Comm[i]["Laplace2_number"],
                Comm[i]["Laplace3"],Comm[i]["Laplace4"],Comm[i]["Laplace5"],
                Comm[i]["Laplace3_number"],Comm[i]["Laplace4_number"],Comm[i]["Laplace5_number"],
                Comm[i]["Laplace_num"],
                # 添加归一化电压 @lizhenguang
                Comm[i]["circuit_Checked"],Comm[i]["circuit"],Comm[i]["observe_name"]
                ]])
            '''
            [[Sym_Type,[名称，
                        正交投影提，
                        [起点X,起点Y，起点Z],
                        [止点X,止点Y，止点Z],
                        [法向X?,  法向Y?, 法向Z?],
                        [反向？, 正向？],
                        [对称类型，旁边下拉列表框]，
                        法向周期，
                        [?, ...Y?, ...Z?],
                        [非均匀网格X值，...Y.., ...Z..],
                        ]]]
            '''
        '''
            Free
            [[Free_Type,[名称，
                        正投影面，
                        [起始X,起始Y，起始Z]，
                        [止点X,止点Y，止点Z]，
                        传播方向："R"、"theta"、"Z"
                        正反向：NEGATIVE(反向)，POSITIVE(正向)，
                        吸收分量，
                        [相对加速比？，值]，
                        非均匀网格X?, ...Y?, ...Z?,
                        非均匀网格X值，...Y.. , ...Z..,
                        ]]]
            '''
        for i in keys:
            if Comm[i]["Dlg_Type"]=="Free_Type":
                DataList.append([Comm[i]["Dlg_Type"],[Comm[i]["name"],
                                                      Comm[i]["Orthogonal_projection_surface"],
                                                      [Comm[i]["start_R"],Comm[i]["start_Y"],Comm[i]["start_Z"]],
                                                      [Comm[i]["end_R"],Comm[i]["end_Y"],Comm[i]["end_Z"]],
                                                      Comm[i]["normal"],
                                                      Comm[i]["direction"],
                                                      Comm[i]["Absorption_Component"],
                                                      [Comm[i]["VPort_Checked"],Comm[i]["VPort"]],
                                                      Comm[i]["DX_R_Checked"],Comm[i]["DX_Y_Checked"],Comm[i]["DX_Z_Checked"],
                                                      Comm[i]["DX_R"],Comm[i]["DX_Y"],Comm[i]["DX_Z"]
                                                      ]])                       
            
        for i in keys:
            if Comm[i]["Dlg_Type"] == "Sym_Type":
                DataList.append([Comm[i]["Dlg_Type"],[Comm[i]["name"],
                                                      Comm[i]["Orthogonal_projection_surface"],
                                                      [Comm[i]["start_R"],Comm[i]["start_Y"],Comm[i]["start_Z"]],
                                                      [Comm[i]["end_R"],Comm[i]["end_Y"],Comm[i]["end_Z"]],
                                                      [Comm[i]["isX"],Comm[i]["isY"],Comm[i]["isZ"]],
                                                      [Comm[i]["isNegative"],Comm[i]["isPositive"]],
                                                      [Comm[i]["SymmetricalType"],Comm[i]["Symmetric_projection_surface"]],
                                                      Comm[i]["Normal_Period"],
                                                      [Comm[i]["DX_R_Checked"],Comm[i]["DX_Y_Checked"],Comm[i]["DX_Z_Checked"]],
                                                      [Comm[i]["DX_R"],Comm[i]["DX_Y"],Comm[i]["DX_Z"]],
                                                      ]])     
         # Mark
        for i in keys:
            if Comm[i]["Dlg_Type"] == "Mark_Type":
                DataList.append([Comm[i]["Dlg_Type"],
                                [Comm[i]["name"],
                                Comm[i]["mark_obj"],
                                Comm[i]["direction"],
                                Comm[i]["isChecked_min"],
                                Comm[i]["isChecked_mid"],
                                Comm[i]["isChecked_max"],
                                Comm[i]["size"]
                                ]])
        for i in keys:
            if Comm[i]["Dlg_Type"] == "EMB_Type":
                DataList.append([Comm[i]["Dlg_Type"],[Comm[i]["name"],
                Comm[i]["BeamJ"],
                Comm[i]["BeamV"],
                Comm[i]["particleType_Checked"],Comm[i]["Species"],
                Comm[i]["generationRate_Checked"],Comm[i]["generationRate"], 
                Comm[i]["transmittingInterval_Checked"],Comm[i]["transmittingInterval"],Comm[i]["stepMultiple"],
                Comm[i]["surface_Checked"],Comm[i]["surface"],
                Comm[i]["outSurface_Checked"],Comm[i]["outSurface"],Comm[i]["Dn"],
                Comm[i]["isEmit"],Comm[i]["Emitter"],          
                Comm[i]["isExclude1"],Comm[i]["Zone1"],Comm[i]["isExclude2"],Comm[i]["Zone2"],
                Comm[i]["isInclude1"],Comm[i]["Zone11"],Comm[i]["isInclude2"],Comm[i]["Zone22"],
                ]])
        for i in keys:
            if Comm[i]["Dlg_Type"] == "EME_Type":
                DataList.append([Comm[i]["Dlg_Type"],[Comm[i]["name"],
                Comm[i]["TField_Checked"],Comm[i]["TField"],
                Comm[i]["RField_Checked"],Comm[i]["RField"],
                Comm[i]["Charg_Checked"],Comm[i]["Charg"],
                Comm[i]["FRate_Checked"],Comm[i]["FRate"],
                Comm[i]["particleType_Checked"],Comm[i]["Species"],
                Comm[i]["generationRate_Checked"],Comm[i]["generationRate"], 
                Comm[i]["transmittingInterval_Checked"],Comm[i]["transmittingInterval"],Comm[i]["stepMultiple"],
                Comm[i]["surface_Checked"],Comm[i]["surface"],
                Comm[i]["outSurface_Checked"],Comm[i]["outSurface"],Comm[i]["Dn"],
                Comm[i]["isEmit"],Comm[i]["Emitter"],          
                Comm[i]["isExclude1"],Comm[i]["Zone1"],Comm[i]["isExclude2"],Comm[i]["Zone2"],
                Comm[i]["isInclude1"],Comm[i]["Zone11"],Comm[i]["isInclude2"],Comm[i]["Zone22"],
                ]])
        for i in keys:
            if Comm[i]["Dlg_Type"] == "EMG_Type":
                DataList.append([Comm[i]["Dlg_Type"],[Comm[i]["name"],
                Comm[i]["Beam_Current"],
                Comm[i]["Guiding_Magnetic_Field"],
                Comm[i]["Vertical_Momentum"],
                Comm[i]["Horizontal_Momentum"],   
                Comm[i]["Guiding_Radius"],          
                [Comm[i]["LaunchCoordinate_X"],Comm[i]["LaunchCoordinate_Y"],Comm[i]["LaunchCoordinate_Z"]],
                Comm[i]["isX1"],Comm[i]["isX2"],Comm[i]["isX3"],

                Comm[i]["particleType_Checked"],Comm[i]["Species"],
                Comm[i]["generationRate_Checked"],Comm[i]["generationRate"], 
                Comm[i]["transmittingInterval_Checked"],Comm[i]["transmittingInterval"],Comm[i]["stepMultiple"],
                Comm[i]["surface_Checked"],Comm[i]["surface"],
                Comm[i]["outSurface_Checked"],Comm[i]["outSurface"],Comm[i]["Dn"],
                Comm[i]["isEmit"],Comm[i]["Emitter"],          
                Comm[i]["isExclude1"],Comm[i]["Zone1"],Comm[i]["isExclude2"],Comm[i]["Zone2"],
                Comm[i]["isInclude1"],Comm[i]["Zone11"],Comm[i]["isInclude2"],Comm[i]["Zone22"],
                Comm[i]["isCheckedVelocity"], Comm[i]["velocity_spread"],
                ]]) 
        for i in keys:
            if Comm[i]["Dlg_Type"] == "EMH_Type":
                DataList.append([Comm[i]["Dlg_Type"],[Comm[i]["name"],
                Comm[i]["Fowler_Nordheim_A"],
                Comm[i]["Fowler_Nordheim_B"],
                Comm[i]["PHI"],
                Comm[i]["particleType_Checked"],Comm[i]["Species"],
                Comm[i]["generationRate_Checked"],Comm[i]["generationRate"], 
                Comm[i]["transmittingInterval_Checked"],Comm[i]["transmittingInterval"],Comm[i]["stepMultiple"],
                Comm[i]["surface_Checked"],Comm[i]["surface"],
                Comm[i]["outSurface_Checked"],Comm[i]["outSurface"],Comm[i]["Dn"],
                Comm[i]["isEmit"],Comm[i]["Emitter"],          
                Comm[i]["isExclude1"],Comm[i]["Zone1"],Comm[i]["isExclude2"],Comm[i]["Zone2"],
                Comm[i]["isInclude1"],Comm[i]["Zone11"],Comm[i]["isInclude2"],Comm[i]["Zone22"],
                ]])     
        for i in keys:
            if Comm[i]["Dlg_Type"] == "EMT_Type":
                DataList.append([Comm[i]["Dlg_Type"],[Comm[i]["name"],
                Comm[i]["WF"],
                Comm[i]["TP"],
                Comm[i]["particleType_Checked"],Comm[i]["Species"],
                Comm[i]["generationRate_Checked"],Comm[i]["generationRate"], 
                Comm[i]["transmittingInterval_Checked"],Comm[i]["transmittingInterval"],Comm[i]["stepMultiple"],
                Comm[i]["surface_Checked"],Comm[i]["surface"],
                Comm[i]["outSurface_Checked"],Comm[i]["outSurface"],Comm[i]["Dn"],
                Comm[i]["isEmit"],Comm[i]["Emitter"],          
                Comm[i]["isExclude1"],Comm[i]["Zone1"],Comm[i]["isExclude2"],Comm[i]["Zone2"],
                Comm[i]["isInclude1"],Comm[i]["Zone11"],Comm[i]["isInclude2"],Comm[i]["Zone22"],
                ]])      
        
            # 二次发射
        for i in keys:
            if Comm[i]["Dlg_Type"] == "EmSE_Type":
                DataList.append([Comm[i]["Dlg_Type"],
                                [Comm[i]["name"],
                                Comm[i]["energy_sec"],
                                Comm[i]["max_num_sec"],
                                Comm[i]["WEIGHT_FACTOR"],
                                Comm[i]["ENERGY_DISTRIBUTION"],
                                Comm[i]["min_energy"],         
                                Comm[i]["max_energy"],
                                Comm[i]["ANGLE_DISTRIBUTION"],
                                Comm[i]["isCheck_WF"],
                                Comm[i]["isCheck_ED"],
                                Comm[i]["isCheck_AD"],
                                Comm[i]["notInclude1"],
                                Comm[i]["notInclude2"],
                                Comm[i]["include1"],
                                Comm[i]["include2"],
                                Comm[i]["Emitter"],
                                Comm[i]["isEmit"],
                                Comm[i]["isExclude1"],
                                Comm[i]["isExclude2"],
                                Comm[i]["isInclude1"],
                                Comm[i]["isInclude2"]
                                ]])
            # 归并
        for i in keys:
            if Comm[i]["Dlg_Type"] == "Merge_Type":
                DataList.append([Comm[i]["Dlg_Type"],
                                [Comm[i]["name"],
                                Comm[i]["Types"],
                                Comm[i]["EveryNum"],
                                Comm[i]["MaxNum"]
                                ]])
            # 新型宏粒子
        for i in keys:
            if Comm[i]["Dlg_Type"] == "Species_Type":    
                DataList.append([Comm[i]["Dlg_Type"],
                                [Comm[i]["name"],
                                Comm[i]["powerUnit"],
                                Comm[i]["quality"],
                                Comm[i]["massUnit"]
                                ]])
            # Populate
        for i in keys:
            if Comm[i]["Dlg_Type"] == "Populate_Type":
                DataList.append([Comm[i]["Dlg_Type"],
                                [Comm[i]["name"],
                                Comm[i]["ParticalType"],
                                Comm[i]["Orthogonal_projection_surface"],
                                Comm[i]["X1"],Comm[i]["Y1"],Comm[i]["Z1"],
                                Comm[i]["X2"],Comm[i]["Y2"],Comm[i]["Z2"],
                                Comm[i]["density"],
                                Comm[i]["temp"]
                                ]])
           
            # 气体电离
        for i in keys:
            if Comm[i]["Dlg_Type"] == "Gasgas_Type":
                DataList.append([Comm[i]["Dlg_Type"],
                                [Comm[i]["name"],
                                Comm[i]["Types"],
                                Comm[i]["pressure"],
                                Comm[i]["temperature"]
                                ]])

        for i in keys:
            if Comm[i]["Dlg_Type"] == "Cntr_Type":
                DataList.append([Comm[i]["Dlg_Type"],[Comm[i]["name"],Comm[i]["Observation_field"],Comm[i]["Timer2MX"],
                Comm[i]["Contour_Checked"],
                Comm[i]["isAppointArea"],Comm[i]["Orthogonal_projection_surface"],
                [Comm[i]["start_R"],Comm[i]["start_Y"],Comm[i]["start_Z"]],
                [Comm[i]["end_R"],Comm[i]["end_Y"],Comm[i]["end_Z"]],
                ]])    
        for i in keys:
            if Comm[i]["Dlg_Type"] == "Vec_Type":
                DataList.append([Comm[i]["Dlg_Type"],[Comm[i]["Observation_field_1"],Comm[i]["Observation_field_2"],
                Comm[i]["name"],
                Comm[i]["Timer2MX"],
                Comm[i]["Vector_Checked"],Comm[i]["Vector_1"],Comm[i]["Vector_2"],
                Comm[i]["isAppointArea"],Comm[i]["Orthogonal_projection_surface"],
                [Comm[i]["start_R"],Comm[i]["start_Y"],Comm[i]["start_Z"]],
                [Comm[i]["end_R"],Comm[i]["end_Y"],Comm[i]["end_Z"]],
                ]])          
        for i in keys: 
            if Comm[i]["Dlg_Type"] == "Pha_Type":
                DataList.append([Comm[i]["Dlg_Type"],[Comm[i]["name"],
                Comm[i]["Horizon"],Comm[i]["Vertical"],
                Comm[i]["Timer2MX"],
                Comm[i]["Species"],
                Comm[i]["Thick_Checked"],Comm[i]["Thick"],
                Comm[i]["Thickness_1"],Comm[i]["Thickness_2"],
                Comm[i]["Suffix_Checked"],Comm[i]["phase"],
                ]])          
        for i in keys:
            if Comm[i]["Dlg_Type"] == "Ran_Type":
                DataList.append([Comm[i]["Dlg_Type"],[Comm[i]["name"],
                Comm[i]["ObserveField"],
                Comm[i]["Timer2MX"],
                Comm[i]["Fourier_Checked"],
                Comm[i]["isMagnitude"],Comm[i]["isComplex"],
                Comm[i]["isAppointArea"],Comm[i]["Type"],
                [Comm[i]["start_R"],Comm[i]["start_Y"],Comm[i]["start_Z"]],
                [Comm[i]["end_R"],Comm[i]["end_Y"],Comm[i]["end_Z"]],
                Comm[i]["isParticle"],
                Comm[i]["chooseParticle"],
                Comm[i]["particleType"],
                Comm[i]["particleAxis"]
                ]])     
        for i in keys:
            if Comm[i]["Dlg_Type"] == "Obs_Type":
                DataList.append([Comm[i]["Dlg_Type"],
                                [Comm[i]["name"],
                                # Comm[i]["TimeType"],
                                # Comm[i]["Type"],
                                True if Comm[i]["observe"] == "Field" else False,
                                True if Comm[i]["observe"] == "Field_Integral" else False,
                                True if Comm[i]["observe"] == "Field_Power" else False,
                                True if Comm[i]["observe"] == "Field_Energy" else False,
                                True if Comm[i]["observe"] == "Particle_Statistics" else False,
                                True if Comm[i]["observe"] == "Particle_Collected" else False,
                                True if Comm[i]["observe"] == "Particle_Emitted" else False,
                                True if Comm[i]["observe"] == "Particle_Destroyed" else False,
                                Comm[i]["observe_field"],
                                Comm[i]["Fourier_Checked"],
                                Comm[i]["fftType"],
                                # @fubiao 是否勾选频率范围
                                Comm[i]["freq_Checked"],
                                Comm[i]["freq1"],
                                Comm[i]["freq2"],
                                Comm[i]["limit_Checked"],
                                Comm[i]["limit1"],
                                Comm[i]["limit2"],
                                Comm[i]["interval_Checked"],
                                Comm[i]["interval"],
                                Comm[i]["dataSmooth_Checked"],
                                Comm[i]["dataSmooth"],
                                Comm[i]["timeParam"],
                                Comm[i]["TimeType"],
                                Comm[i]["isAppoint"],
                                Comm[i]["Type"],
                                [Comm[i]["start_R"],Comm[i]["start_Y"],Comm[i]["start_Z"]],
                                [Comm[i]["end_R"],Comm[i]["end_Y"],Comm[i]["end_Z"]],
                                Comm[i]["name2"]                
                ]])        
            '''
            [[DefTimer_Type/Timer_Type,[名称，
                                        类型id：0表示周期型，1表示离散型，
                                        [按时间步数？，按模拟时间]，
                                        起始时刻，
                                        结束时刻，
                                        定时周期，
                                        离散时刻]]]
            '''
        for i in keys:
            if Comm[i]["Dlg_Type"] == "DefTimer_Type" or Comm[i]["Dlg_Type"] == "Timer_Type":
                DataList.append([Comm[i]["Dlg_Type"],[Comm[i]["name"],
                Comm[i]["Type"],
                [Comm[i]["isByTimeSteps"],Comm[i]["isBySimulation"]],
                Comm[i]["start"],
                Comm[i]["end"],
                Comm[i]["period"],  
                Comm[i]["discreteTime"],     
                ]])            
        
            
            
    except KeyError as reason:
        FreeCAD.Console.PrintError("\n这里出现问题1111")
        sayz("!!!Error:KeyError,Maybe lack of key:%s"%str(reason))
        FreeCAD.Console.PrintError("\n这里出现问题")
    return DataList


def sayz(msg):
    FreeCAD.Console.PrintMessage("--------------------------------------------")
    FreeCAD.Console.PrintMessage('\n')
    FreeCAD.Console.PrintMessage(msg)
    FreeCAD.Console.PrintMessage('\n')  