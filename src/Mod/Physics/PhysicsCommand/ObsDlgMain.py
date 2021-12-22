#-*- coding: utf-8 -*-

import json
import FreeCAD
from PySide import QtCore
from PySide import QtGui
import Physics.PhysicsGui.ObsDlg
import Simulation
from DlgData import DlgData, sayz,getDlgData
from Modeling.Common.CommonCommand.NewDocument import ObjectDict
from Modeling.Common.Tools import DocumentTools,ObjectsTools
import ObservePalMain
import DoManager
import File.FileCommand.M3DFile.M3DFileUtil
import File.FileCommand.TextUI.FileTextView
from Modeling.Common.Tools.PhysicsDialog import *
from PhysicsTools import CompleterTools
flag = 0
#json格式数据需要保持原有顺序输出
from collections import OrderedDict
def show(type,className,itemUserName):
    global  ObjectDict

    if type == "new":
        ObjectDict[className] = ObsShow("new",className)
        ObjectDict[className].setModal(False)
        ObjectDict[className].show()
        ObjectDict[className].exec_()
    elif type == "old":
        if className in ObjectDict.keys():
            #增加了撤销操作后，数据可能发生变化，所以每次需要重新加载数据，
            JSON_CADComment = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict)
            oldData = DlgData(JSON_CADComment[itemUserName], itemUserName)
            ObjectDict[className].loadData(oldData)

            ObjectDict[className].refreshCombox()
            ObjectDict[className].ComboBox_Shadow_clicked()
            ObjectDict[className].flagUpdateItemName=True
            ObjectDict[className].setNameUnable()
            ObjectDict[className].setModal(False)
            ObjectDict[className].show()
            ObjectDict[className].exec_()             
        else:
            ObjectDict[className] = ObsShow(className,className)
            ObjectDict[className].flagUpdateItemName = True
            ObjectDict[className].setNameUnable()
            ObjectDict[className].setModal(False)
            ObjectDict[className].show()
            ObjectDict[className].exec_()   
        

class ObsShow(PhysicsDialog):
    def __init__(self,DialogID,className,parent=None):
        PhysicsDialog.__init__(self, parent)
        self.ui = Physics.PhysicsGui.ObsDlg.Ui_Dialog_ObsDlg()
        self.ui.setupUi(self)
        #代码补全
        self.defaultValue = ["OSYS$MIDPLANE1","OSYS$MIDPLANE2","OSYS$MIDPLANE3","OSYS$VOLUME"]
        CompleterTools.setLineEditsCompleter(CompleterTools.getAllLineEdits(self.ui))
        global flag
        flag = 0
        # 获取当前坐标系及坐标系单位
        coord = Simulation.getCoordinate()
        self.x = coord[0]
        self.y = coord[1]
        self.z = coord[2]
        self.x_unit = coord[3]
        self.y_unit = coord[4]
        self.z_unit = coord[5]

        # 根据坐标系初始化面板
        self.ui.label_X.setText(self.x)
        self.ui.label_Y.setText(self.y)
        self.ui.label_Z.setText(self.z)
        self.ui.radioButton_x.setText(self.x)
        self.ui.radioButton_y.setText(self.y)
        self.ui.radioButton_z.setText(self.z)
        self.ui.LineEdit_start_x.setText("0" + self.x_unit)
        self.ui.LineEdit_start_y.setText("0" + self.y_unit)
        self.ui.LineEdit_start_z.setText("0" + self.z_unit)
        self.ui.LineEdit_end_x.setText("0" + self.x_unit)
        self.ui.LineEdit_end_y.setText("0" + self.y_unit)
        self.ui.LineEdit_end_z.setText("0" + self.z_unit)


        # 初始化：时间观测点添加下拉选项
        self.addShadowItem("Point")

        # 输入框变化时
        self.ui.LineEdit_start_x.textChanged.connect(self.LineEdit_start_x_textChanged)
        self.ui.LineEdit_start_y.textChanged.connect(self.LineEdit_start_y_textChanged)
        self.ui.LineEdit_start_z.textChanged.connect(self.LineEdit_start_z_textChanged)

        self.ui.pushButton.clicked.connect(self.onCancel)
        self.ui.radioButton_x.clicked.connect(self.radioButton_x_clicked)
        self.ui.radioButton_y.clicked.connect(self.radioButton_y_clicked)
        self.ui.radioButton_z.clicked.connect(self.radioButton_z_clicked)

        # 场
        self.ui.radioButton_field.clicked.connect(self.radioButton_field_clicked)
        # 场积分
        self.ui.radioButton_integral.clicked.connect(self.radioButton_integral_clicked)
        # 场功率
        self.ui.radioButton_power.clicked.connect(self.radioButton_power_clicked)
        # 场能量
        self.ui.radioButton_energy.clicked.connect(self.radioButton_energy_clicked)
        # 粒子统计
        self.ui.radioButton_particleStatistics.clicked.connect(self.radioButton_particleStatistics_clicked)
        # 粒子统计类型下拉框
        self.ui.comboBox_EMIT_EPS.currentIndexChanged.connect(self.comboBox_EMIT_EPS_clicked)
        #收集的粒子，发射的粒子、湮灭的粒子
        self.ui.radioButton_collected.clicked.connect(self.radioButton_clicked)
        self.ui.radioButton_emitted.clicked.connect(self.radioButton_clicked)
        self.ui.radioButton_destroyed.clicked.connect(self.radioButton_clicked)
        # 进行快速傅里叶变换
        self.ui.checkBox_Fourier.clicked.connect(self.checkBox_Fourier_clicked)
        # 频率范围
        self.ui.checkBox_freq.clicked.connect(self.checkBox_freq_clicked)
        # 时间范围
        self.ui.checkBox_limit.clicked.connect(self.checkBox_limit_clicked)
        #观察间隔
        self.ui.checkBox_interval.clicked.connect(self.checkBox_interval_clicked)
        # 数据平滑处理
        self.ui.checkBox_dataSmooth.clicked.connect(self.checkBox_dataSmooth_clicked)


        # 类型下拉框
        self.ui.ComboBox_type.currentIndexChanged.connect(self.ComboBox_type_clicked)
        self.ComboBox_type_clicked()
        self.ui.ComboBox_Shadow.currentIndexChanged.connect(self.ComboBox_Shadow_clicked)
        # 正投影面下拉框选择事件
        self.ui.ComboBox_Shadow.currentIndexChanged.connect(self.ComboBox_Shadow_clicked)
        # 加载每个Project都具有的Comment【里面存储着对话框的所有数据】----》JSON对象----》应用于加载窗口
        JSON_CADComment = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict)  

        # self.ui.pushButton_ok.clicked.connect(lambda: self.onConfirm(JSON_CADComment,className)) 
        self.initDialog(JSON_CADComment,className)
        
        FreeCAD.Console.PrintMessage("DialogID: "+str(DialogID)+"\n")
        if DialogID != "new":
            oldData = DlgData(JSON_CADComment[DialogID],DialogID)
            self.loadData(oldData)
            FreeCAD.Console.PrintMessage("OldData: "+str(oldData)+"\n")            
            flag = 1  
        self.userNameBefore=self.ui.LineEdit_Name.text()
                #用于判断是否进行名称更新
        self.flagUpdateItemName=False
        self.ComboBox_Shadow_clicked()
        self.refreshComboxType()
        # 适配分辨率
        import AdaptiveDPIUtil
        new_x, new_y = AdaptiveDPIUtil.get_new_dpi(self.width(), self.height())
        self.resize(500, new_y)


    # ComboBox_Shadow根据ComboBox_type添加选项
    def addShadowItem(self, type):
        # 显示观测类型
        if self.ui.groupBox_Port.isHidden():
            self.ui.groupBox_Port.setGeometry(QtCore.QRect(10, 60, 401, 181))
            self.ui.groupBox_Port_2.setGeometry(QtCore.QRect(10, 250, 401, 241))
            self.ui.groupBox_2.setGeometry(QtCore.QRect(10, 500, 401, 101))
            self.ui.groupBox_Port.show()
        # 添加前清空所有选项
        self.ui.ComboBox_Shadow.clear()
        self.ui.ComboBox_Shadow.addItem(u"未指定")
        Orthogonal_list = DocumentTools.getActiveDocTypes(type)
        if type == "Area_Conformal":
            Orthogonal_list.append("OSYS$MIDPLANE1")
            Orthogonal_list.append("OSYS$MIDPLANE2")
            Orthogonal_list.append("OSYS$MIDPLANE3")
        if type == "Vol_Conformal":
            # 此处不需要为导体，任意类型都可被选择为时间观测体 @lizgenguang start
            # Orthogonal_list = DocumentTools.getActiveDocTypes(type, False)
            # @wangzhenguo 这里把所有体添加进来
            Orthogonal_list = DocumentTools.getAllVols()
            Orthogonal_list.append("OSYS$VOLUME")
            # @lizgenguang end
        for i in Orthogonal_list:
            self.ui.ComboBox_Shadow.addItem(i)
    def refreshCombox(self):
        '''
        每次加载窗口时都要重新加载下拉列表，以实现动态加载
        一般来说就是ComboBox_Shadow_list需要动态刷新
        '''
        ComboBox_Shadow_list=[]
        # for i in range(self.ui.ComboBox_Shadow.count()):
        #     ComboBox_Shadow_list.append(self.ui.ComboBox_Shadow.itemText(i))
        # volumeList = DocumentTools.getActiveDocTypes("Vol_Conformal")
        # for i in volumeList:
        #     if i not in ComboBox_Shadow_list:
        #         self.ui.ComboBox_Shadow.addItem(i)       
    # 类型下拉框的点击事件
    def ComboBox_type_clicked(self):
        # 点
        if self.ui.ComboBox_type.currentIndex() == 0:
            self.addShadowItem(ObjectsTools.ObjectType.Point)
            self.ui.groupBox_Port.setEnabled(True)
            # 观测点止点不可编辑
            self.ui.LineEdit_start_x.setEnabled(True)
            self.ui.LineEdit_start_y.setEnabled(True)
            self.ui.LineEdit_start_z.setEnabled(True)
            self.ui.LineEdit_end_x.setEnabled(False)
            self.ui.LineEdit_end_y.setEnabled(False)
            self.ui.LineEdit_end_z.setEnabled(False)
            # 法向不可选
            self.ui.radioButton_x.setChecked(False)
            self.ui.radioButton_y.setChecked(False)
            self.ui.radioButton_z.setChecked(False)
            self.ui.radioButton_x.setEnabled(False)
            self.ui.radioButton_y.setEnabled(False)
            self.ui.radioButton_z.setEnabled(False)
            # 设置分类项按钮是否可点击
            self.ui.radioButton_field.setEnabled(True)
            # self.ui.radioButton_field.setChecked(True)
            self.radioButton_field_clicked()
            self.ui.radioButton_integral.setEnabled(False)
            self.ui.radioButton_power.setEnabled(False)
            self.ui.radioButton_energy.setEnabled(False)
            # @WZG 2021.1.23 设置粒子统计 ，收集的粒子，发射的粒子，湮灭的粒子 4个按钮可选状态
            self.ui.radioButton_particleStatistics.setEnabled(False)
            self.ui.radioButton_collected.setEnabled(False)
            self.ui.radioButton_emitted.setEnabled(False)
            self.ui.radioButton_destroyed.setEnabled(False)

        # 线
        elif self.ui.ComboBox_type.currentIndex() == 1:
            self.addShadowItem("Line_Conformal")
            self.ui.groupBox_Port.setEnabled(True)
            # 法向R选中
            self.ui.radioButton_x.setChecked(True)
            # 观测点止点不可编辑
            self.ui.LineEdit_start_x.setEnabled(True)
            self.ui.LineEdit_start_y.setEnabled(True)
            self.ui.LineEdit_start_z.setEnabled(True)
            self.ui.LineEdit_end_x.setEnabled(True)
            self.ui.LineEdit_end_y.setEnabled(False)
            self.ui.LineEdit_end_z.setEnabled(False)
            # 设置分类项按钮是否可点击
            self.ui.radioButton_field.setEnabled(True)
            self.ui.radioButton_integral.setEnabled(True)
            # self.ui.radioButton_integral.setChecked(True)
            self.radioButton_field_clicked()
            self.ui.radioButton_power.setEnabled(False)
            self.ui.radioButton_energy.setEnabled(False)
            # @WZG 2021.1.23 设置粒子统计 ，收集的粒子，发射的粒子，湮灭的粒子 4个按钮可选状态
            self.ui.radioButton_particleStatistics.setEnabled(False)
            self.ui.radioButton_collected.setEnabled(False)
            self.ui.radioButton_emitted.setEnabled(False)
            self.ui.radioButton_destroyed.setEnabled(False)

        # 面
        elif self.ui.ComboBox_type.currentIndex() == 2:
            self.addShadowItem("Area_Conformal")
            self.ui.groupBox_Port.setEnabled(True)
            # 法向R选中
            self.ui.radioButton_x.setChecked(True)
            # 观测点止点不可编辑
            self.ui.LineEdit_start_x.setEnabled(True)
            self.ui.LineEdit_start_y.setEnabled(True)
            self.ui.LineEdit_start_z.setEnabled(True)
            self.ui.LineEdit_end_x.setEnabled(False)
            self.ui.LineEdit_end_y.setEnabled(True)
            self.ui.LineEdit_end_z.setEnabled(True)
            # 设置分类项按钮是否可点击
            self.ui.radioButton_field.setEnabled(True)
            self.ui.radioButton_integral.setEnabled(True)
            self.ui.radioButton_power.setEnabled(True)
            self.radioButton_field_clicked()
            # self.ui.radioButton_power.setChecked(True)
            self.ui.radioButton_energy.setEnabled(False)
            # @WZG 2021.1.23 设置粒子统计 ，收集的粒子，发射的粒子，湮灭的粒子 4个按钮可选状态
            self.ui.radioButton_particleStatistics.setEnabled(False)
            self.ui.radioButton_collected.setEnabled(True)
            self.ui.radioButton_emitted.setEnabled(True)
            self.ui.radioButton_destroyed.setEnabled(True)
        # 体
        elif self.ui.ComboBox_type.currentIndex() == 3:
            self.addShadowItem("Vol_Conformal")
            self.ui.groupBox_Port.setEnabled(True)
            # 观测点止点可编辑
            self.ui.LineEdit_start_x.setEnabled(True)
            self.ui.LineEdit_start_y.setEnabled(True)
            self.ui.LineEdit_start_z.setEnabled(True)
            self.ui.LineEdit_end_x.setEnabled(True)
            self.ui.LineEdit_end_y.setEnabled(True)
            self.ui.LineEdit_end_z.setEnabled(True)
            # 法向不可选
            self.ui.radioButton_x.setChecked(False)
            self.ui.radioButton_y.setChecked(False)
            self.ui.radioButton_z.setChecked(False)
            self.ui.radioButton_x.setEnabled(False)
            self.ui.radioButton_y.setEnabled(False)
            self.ui.radioButton_z.setEnabled(False)
            # 设置分类项按钮是否可点击
            self.ui.radioButton_field.setEnabled(False)
            self.ui.radioButton_integral.setEnabled(False)
            self.ui.radioButton_power.setEnabled(False)
            self.ui.radioButton_energy.setEnabled(True)
            self.ui.radioButton_energy.setChecked(True)
            self.radioButton_energy_clicked()
            # @WZG 2021.1.23 设置粒子统计 ，收集的粒子，发射的粒子，湮灭的粒子 4个按钮可选状态
            self.ui.radioButton_particleStatistics.setEnabled(True)
            self.ui.radioButton_collected.setEnabled(True)
            self.ui.radioButton_emitted.setEnabled(True)
            self.ui.radioButton_destroyed.setEnabled(True)


    def ComboBox_Shadow_clicked(self):
        ObjectsTools.findObjByLabelWithoutOrderAndVisible(self.ui.ComboBox_Shadow.currentText())
        if self.ui.ComboBox_Shadow.currentIndex() <= 0:
            self.ui.LineEdit_start_x.setEnabled(True)
            self.ui.LineEdit_start_y.setEnabled(True)
            self.ui.LineEdit_start_z.setEnabled(True)
            self.ui.radioButton_x.setEnabled(True)
            self.ui.radioButton_y.setEnabled(True)
            self.ui.radioButton_z.setEnabled(True)
            if self.ui.radioButton_x.isChecked() == True:
                # 点
                if self.ui.ComboBox_type.currentIndex() == 0:
                    self.ui.LineEdit_end_x.setEnabled(False)
                    self.ui.LineEdit_end_y.setEnabled(False)
                    self.ui.LineEdit_end_z.setEnabled(False)
                    # 法向不可选
                    self.ui.radioButton_x.setChecked(False)
                    self.ui.radioButton_y.setChecked(False)
                    self.ui.radioButton_z.setChecked(False)
                    self.ui.radioButton_x.setEnabled(False)
                    self.ui.radioButton_y.setEnabled(False)
                    self.ui.radioButton_z.setEnabled(False)
                # 线
                elif self.ui.ComboBox_type.currentIndex() == 1:
                    self.ui.LineEdit_end_x.setEnabled(True)
                    self.ui.LineEdit_end_y.setEnabled(False)
                    self.ui.LineEdit_end_z.setEnabled(False)
                # 面
                elif self.ui.ComboBox_type.currentIndex() == 2:
                    self.ui.LineEdit_end_x.setEnabled(False)
                    self.ui.LineEdit_end_y.setEnabled(True)
                    self.ui.LineEdit_end_z.setEnabled(True)
                # 体
                elif self.ui.ComboBox_type.currentIndex() == 3:
                    self.ui.LineEdit_end_x.setEnabled(True)
                    self.ui.LineEdit_end_y.setEnabled(True)
                    self.ui.LineEdit_end_z.setEnabled(True)
                    # 法向不可选
                    self.ui.radioButton_x.setChecked(False)
                    self.ui.radioButton_y.setChecked(False)
                    self.ui.radioButton_z.setChecked(False)
                    self.ui.radioButton_x.setEnabled(False)
                    self.ui.radioButton_y.setEnabled(False)
                    self.ui.radioButton_z.setEnabled(False)
            if self.ui.radioButton_y.isChecked() == True:
                # 点
                if self.ui.ComboBox_type.currentIndex() == 0:
                    self.ui.LineEdit_end_x.setEnabled(False)
                    self.ui.LineEdit_end_y.setEnabled(False)
                    self.ui.LineEdit_end_z.setEnabled(False)
                    # 法向不可选
                    self.ui.radioButton_x.setChecked(False)
                    self.ui.radioButton_y.setChecked(False)
                    self.ui.radioButton_z.setChecked(False)
                    self.ui.radioButton_x.setEnabled(False)
                    self.ui.radioButton_y.setEnabled(False)
                    self.ui.radioButton_z.setEnabled(False)
                # 线
                elif self.ui.ComboBox_type.currentIndex() == 1:
                    self.ui.LineEdit_end_x.setEnabled(False)
                    self.ui.LineEdit_end_y.setEnabled(True)
                    self.ui.LineEdit_end_z.setEnabled(False)
                # 面
                elif self.ui.ComboBox_type.currentIndex() == 2:
                    self.ui.LineEdit_end_x.setEnabled(True)
                    self.ui.LineEdit_end_y.setEnabled(False)
                    self.ui.LineEdit_end_z.setEnabled(True)
                # 体
                elif self.ui.ComboBox_type.currentIndex() == 3:
                    self.ui.LineEdit_end_x.setEnabled(True)
                    self.ui.LineEdit_end_y.setEnabled(True)
                    self.ui.LineEdit_end_z.setEnabled(True)
                    # 法向不可选
                    self.ui.radioButton_x.setChecked(False)
                    self.ui.radioButton_y.setChecked(False)
                    self.ui.radioButton_z.setChecked(False)
                    self.ui.radioButton_x.setEnabled(False)
                    self.ui.radioButton_y.setEnabled(False)
                    self.ui.radioButton_z.setEnabled(False)
            if self.ui.radioButton_z.isChecked() == True:
                self.ui.LineEdit_end_x.setEnabled(True)
                self.ui.LineEdit_end_y.setEnabled(True)
                self.ui.LineEdit_end_z.setEnabled(False)
                # 点
                if self.ui.ComboBox_type.currentIndex() == 0:
                    self.ui.LineEdit_end_x.setEnabled(False)
                    self.ui.LineEdit_end_y.setEnabled(False)
                    self.ui.LineEdit_end_z.setEnabled(False)
                    # 法向不可选
                    self.ui.radioButton_x.setChecked(False)
                    self.ui.radioButton_y.setChecked(False)
                    self.ui.radioButton_z.setChecked(False)
                    self.ui.radioButton_x.setEnabled(False)
                    self.ui.radioButton_y.setEnabled(False)
                    self.ui.radioButton_z.setEnabled(False)
                # 线
                elif self.ui.ComboBox_type.currentIndex() == 1:
                    self.ui.LineEdit_end_x.setEnabled(False)
                    self.ui.LineEdit_end_y.setEnabled(False)
                    self.ui.LineEdit_end_z.setEnabled(True)
                # 面
                elif self.ui.ComboBox_type.currentIndex() == 2:
                    self.ui.LineEdit_end_x.setEnabled(True)
                    self.ui.LineEdit_end_y.setEnabled(True)
                    self.ui.LineEdit_end_z.setEnabled(False)
                # 体
                elif self.ui.ComboBox_type.currentIndex() == 3:
                    self.ui.LineEdit_end_x.setEnabled(True)
                    self.ui.LineEdit_end_y.setEnabled(True)
                    self.ui.LineEdit_end_z.setEnabled(True)
                    # 法向不可选
                    self.ui.radioButton_x.setChecked(False)
                    self.ui.radioButton_y.setChecked(False)
                    self.ui.radioButton_z.setChecked(False)
                    self.ui.radioButton_x.setEnabled(False)
                    self.ui.radioButton_y.setEnabled(False)
                    self.ui.radioButton_z.setEnabled(False)
        else:
            self.ui.radioButton_x.setEnabled(False)
            self.ui.radioButton_y.setEnabled(False)
            self.ui.radioButton_z.setEnabled(False)
            if self.ui.ComboBox_type.currentIndex() == 0:
                objName = self.ui.ComboBox_Shadow.currentText()
                FreeCAD.Console.PrintMessage("objName: "+str(objName)+"\n")
                modelData = DocumentTools.getValueOfPointObjByLabel(objName)
                FreeCAD.Console.PrintMessage("modelData: "+str(modelData)+"\n")
                self.ui.LineEdit_start_x.setText(str(modelData[1]) + self.x_unit)
                self.ui.LineEdit_start_y.setText(str(modelData[2]) + self.y_unit)
                self.ui.LineEdit_start_z.setText(str(modelData[3]) + self.z_unit)
                self.ui.LineEdit_start_x.setEnabled(False)
                self.ui.LineEdit_start_y.setEnabled(False)
                self.ui.LineEdit_start_z.setEnabled(False)
                self.ui.LineEdit_end_x.setEnabled(False)
                self.ui.LineEdit_end_y.setEnabled(False)
                self.ui.LineEdit_end_z.setEnabled(False)
                # 法向不可选
                self.ui.radioButton_x.setEnabled(False)
                self.ui.radioButton_y.setEnabled(False)
                self.ui.radioButton_z.setEnabled(False)
                self.ui.radioButton_x.setChecked(False)
                self.ui.radioButton_y.setChecked(False)
                self.ui.radioButton_z.setChecked(False)
            elif self.ui.ComboBox_type.currentIndex() == 1:
                objName = self.ui.ComboBox_Shadow.currentText()
                modelData = DocumentTools.getValueOfLineObjByLable(objName)
                self.ui.LineEdit_start_x.setText(str(modelData[1]))
                self.ui.LineEdit_start_y.setText(str(modelData[2]))
                self.ui.LineEdit_start_z.setText(str(modelData[3]))
                self.ui.LineEdit_end_x.setText(str(modelData[4]))
                self.ui.LineEdit_end_y.setText(str(modelData[5]))
                self.ui.LineEdit_end_z.setText(str(modelData[6]))
                self.ui.LineEdit_start_x.setEnabled(False)
                self.ui.LineEdit_start_y.setEnabled(False)
                self.ui.LineEdit_start_z.setEnabled(False)
                self.ui.LineEdit_end_x.setEnabled(False)
                self.ui.LineEdit_end_y.setEnabled(False)
                self.ui.LineEdit_end_z.setEnabled(False)
                if modelData[7] == 1:
                    self.ui.radioButton_x.setChecked(True)
                elif modelData[7] == 2:
                    self.ui.radioButton_y.setChecked(True)
                elif modelData[7] == 3:
                    self.ui.radioButton_z.setChecked(True)
                elif modelData[7] == 0:
                    FreeCAD.Console.PrintMessage("get Line_Conformal error")
            elif self.ui.ComboBox_type.currentIndex() == 2:
                objName = self.ui.ComboBox_Shadow.currentText()
                if objName in self.defaultValue:
                    pass
                else:
                    modelData = DocumentTools.getValueOfAreaObjByLable(objName)
                    self.ui.LineEdit_start_x.setText(str(modelData[1]))
                    self.ui.LineEdit_start_y.setText(str(modelData[2]) )
                    self.ui.LineEdit_start_z.setText(str(modelData[3]))
                    self.ui.LineEdit_end_x.setText(str(modelData[4]))
                    self.ui.LineEdit_end_y.setText(str(modelData[5]))
                    self.ui.LineEdit_end_z.setText(str(modelData[6]))
                # self.ui.LineEdit_start_x.setEnabled(False)
                # self.ui.LineEdit_start_y.setEnabled(False)
                # self.ui.LineEdit_start_z.setEnabled(False)
                # self.ui.LineEdit_end_x.setEnabled(False)
                # self.ui.LineEdit_end_y.setEnabled(False)
                # self.ui.LineEdit_end_z.setEnabled(False)
                    if modelData[7] == 1:
                        self.ui.radioButton_x.setChecked(True)
                    elif modelData[7] == 2:
                        self.ui.radioButton_y.setChecked(True)
                    elif modelData[7] == 3:
                        self.ui.radioButton_z.setChecked(True)
                    elif modelData[7] == 0:
                        FreeCAD.Console.PrintMessage("get Area_Conformal error")
                self.ui.LineEdit_start_x.setEnabled(False)
                self.ui.LineEdit_start_y.setEnabled(False)
                self.ui.LineEdit_start_z.setEnabled(False)
                self.ui.LineEdit_end_x.setEnabled(False)
                self.ui.LineEdit_end_y.setEnabled(False)
                self.ui.LineEdit_end_z.setEnabled(False)
            elif self.ui.ComboBox_type.currentIndex() == 3:
                objName = self.ui.ComboBox_Shadow.currentText()
                if objName in self.defaultValue:
                    pass
                else:
                    #  @WZG 2021.1.23 这里的体如果不是正投影体，则不往坐标对话框里填数据
                    vol_conformal_list = DocumentTools.getActiveDocTypes("Vol_Conformal", False)
                    if objName in vol_conformal_list:
                        modelData = DocumentTools.getValueOfVolComformalObjByLable(objName)
                        self.ui.LineEdit_start_x.setText(str(modelData[1]))
                        self.ui.LineEdit_start_y.setText(str(modelData[2]))
                        self.ui.LineEdit_start_z.setText(str(modelData[3]))
                        self.ui.LineEdit_end_x.setText(str(modelData[4]))
                        self.ui.LineEdit_end_y.setText(str(modelData[5]))
                        self.ui.LineEdit_end_z.setText(str(modelData[6]))
                    else:
                        pass

                self.ui.LineEdit_start_x.setEnabled(False)
                self.ui.LineEdit_start_y.setEnabled(False)
                self.ui.LineEdit_start_z.setEnabled(False)
                self.ui.LineEdit_end_x.setEnabled(False)
                self.ui.LineEdit_end_y.setEnabled(False)
                self.ui.LineEdit_end_z.setEnabled(False)
                # 法向不可选
                self.ui.radioButton_x.setEnabled(False)
                self.ui.radioButton_y.setEnabled(False)
                self.ui.radioButton_z.setEnabled(False)
                self.ui.radioButton_x.setChecked(False)
                self.ui.radioButton_y.setChecked(False)
                self.ui.radioButton_z.setChecked(False)
            elif self.ui.ComboBox_type.currentIndex() == 4:
                pass

            # 点击取消按钮关闭窗口
    def onCancel(self):
        #由于每次打开前都会重新加载数据，这儿就先注释了
        # if self.flagUpdateItemName:
        #     JSON_CADComment = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict)
        #     oldData = DlgData(JSON_CADComment[self.userNameBefore],self.userNameBefore)
        #     self.loadData(oldData)
        self.close()

    def onConfirm(self,FreeCAD_Comment_Dict,className):
        oldJson = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict)
        #存储只修改数据而没有修改item名的情况
        oldData = ["modify",self.userNameBefore,className]
        itemData = ["modify",self.userNameBefore,className]
        global flag 
        count = 1
        name = self.ui.LineEdit_Name.text()
        self.close()

        if flag == 0:              
            while name in FreeCAD_Comment_Dict.keys(): 
               name = self.ui.LineEdit_Name.text() + str(count) 
               count+=1       
            self.ui.LineEdit_Name.setText(name)

            itemData,oldData = ObservePalMain.addItem(u"时间观测", name, className)

            flag = 1
                #防止修改名称使得json重复
        if self.flagUpdateItemName:
            if not name == self.userNameBefore:
                JSON_CADComment = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict)
                if self.userNameBefore in JSON_CADComment:
                    JSON_CADComment.pop(self.userNameBefore)
                    FreeCAD.ActiveDocument.Begin = json.dumps(JSON_CADComment)
                    # 判断更新的名称是否有重名
                    while name in FreeCAD_Comment_Dict.keys():
                        name = self.ui.LineEdit_Name.text() + str(count)
                        count += 1
                    #更新名称
                    # if self.flagUpdateItemName:
                    itemData,oldData= ObservePalMain.updateItemName(name)
                    self.flagUpdateItemName=False
        self.userNameBefore=name
        newData = DlgData({},name)           
        isModify=self.keepData(newData)

        if isModify and itemData is not None:
            jsonData = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict)

            # 更新两个栈
            record = [jsonData, itemData,oldJson,oldData]
            DoManager.newOperation(record)


        # 更新m3d文档 by mx
        # 获得m3d的util
        fileUtil = File.FileCommand.M3DFile.M3DFileUtil.M3DFileUtil()
        # 获得最近的m3d字符串
        FileStr = fileUtil.getLatestM3DFileStr()
        # 进行文本的更新
        File.FileCommand.TextUI.FileTextView.FileView().updateText(FileStr)

    def loadData(self,DlgData):     
        try:  
            self.ui.LineEdit_Name.setText(DlgData.data['name'])
            #设置标记的旧名字
            self.userNameBefore = DlgData.data['name']
            # FreeCAD.Console.PrintError('\n'+str(type(DlgData.data))+'\n')
            if not 'name2' in DlgData.data:
                DlgData.data['name2'] = ''
            self.ui.lineEdit_name2.setText(DlgData.data['name2'])
            if DlgData.data['TimeType']=="POINT":
                self.ui.ComboBox_type.setCurrentIndex(self.ui.ComboBox_type.findText(u"时间观测点"))
            if DlgData.data['TimeType']=="LINE":
                self.ui.ComboBox_type.setCurrentIndex(self.ui.ComboBox_type.findText(u"时间观测线"))
            if DlgData.data['TimeType']=="AREA":
                self.ui.ComboBox_type.setCurrentIndex(self.ui.ComboBox_type.findText(u"时间观测面"))
            if DlgData.data['TimeType']=="VOLUME":
                self.ui.ComboBox_type.setCurrentIndex(self.ui.ComboBox_type.findText(u"时间观测体"))
            self.ui.ComboBox_Shadow.setCurrentIndex(self.ui.ComboBox_Shadow.findText(DlgData.data['Type']))

            # 坐标点
            self.ui.LineEdit_start_x.setText(DlgData.data['start_R'])
            self.ui.LineEdit_start_y.setText(DlgData.data['start_Y'])
            self.ui.LineEdit_start_z.setText(DlgData.data['start_Z'])
            self.ui.LineEdit_end_x.setText(DlgData.data['end_R'])
            self.ui.LineEdit_end_y.setText(DlgData.data['end_Y'])
            self.ui.LineEdit_end_z.setText(DlgData.data['end_Z'])

            # 法向选择
            if DlgData.data['normal'] == "R":
                self.ui.radioButton_x.setChecked(True)
            if DlgData.data['normal'] == "theta":
                self.ui.radioButton_y.setChecked(True)
            if DlgData.data['normal'] == "Z":
                self.ui.radioButton_z.setChecked(True)

            # 傅里叶
            self.ui.checkBox_Fourier.setChecked(DlgData.data['Fourier_Checked'])
            self.ui.radioButton_real.setEnabled(DlgData.data['Fourier_Checked'])
            self.ui.radioButton_complex.setEnabled(DlgData.data['Fourier_Checked'])  
      
            # 频率
            self.ui.checkBox_freq.setChecked(DlgData.data['freq_Checked'])
            self.ui.LineEdit_freq1.setEnabled(DlgData.data['freq_Checked'])
            self.ui.LineEdit_freq2.setEnabled(DlgData.data['freq_Checked'])
            if DlgData.data['Fourier'] == "real":
                self.ui.radioButton_real.setChecked(True)
            else:
                self.ui.radioButton_complex.setChecked(True)
            self.ui.LineEdit_freq1.setText(DlgData.data['freq1'])
            self.ui.LineEdit_freq2.setText(DlgData.data['freq2'])
            # 时间
            self.ui.checkBox_limit.setChecked(DlgData.data['limit_Checked'])
            self.ui.LineEdit_limit1.setEnabled(DlgData.data['limit_Checked'])
            self.ui.LineEdit_limit2.setEnabled(DlgData.data['limit_Checked'])
            self.ui.LineEdit_limit1.setText(DlgData.data['limit1'])
            self.ui.LineEdit_limit2.setText(DlgData.data['limit2'])
            #观察间隔
            self.ui.checkBox_interval.setChecked(DlgData.data['interval_Checked'])
            self.ui.lineEdit_interval.setEnabled(DlgData.data['interval_Checked'])
            self.ui.lineEdit_interval.setText(DlgData.data['interval'])
            # 参数
            self.ui.checkBox_dataSmooth.setChecked(DlgData.data['dataSmooth_Checked'])
            if DlgData.data['dataSmooth'] == "STEP":
                self.ui.radioButton_time.setChecked(True)
            if DlgData.data['dataSmooth'] == "LO_PASS":
                self.ui.radioButton_RC.setChecked(True)
            self.ui.LineEdit_timeParam.setEnabled(DlgData.data['dataSmooth_Checked'])
            self.ui.LineEdit_timeParam.setText(DlgData.data['timeParam'])

            # 观测项
            if DlgData.data['observe'] == "Field":
                self.ui.radioButton_field.setChecked(True)
                self.ui.ComboBox_E1.setEnabled(True)
                self.ui.ComboBox_EDL.setEnabled(False)
                self.ui.ComboBox_SDA.setEnabled(False)
                self.ui.ComboBox_EM.setEnabled(False)
                self.ui.LineEdit_phase1.setEnabled(False)
                self.ui.comboBox_EMIT_EPS.setEnabled(False)
                self.ui.comboBox_CHARGE.setEnabled(False)
                self.ui.comboBox.setEnabled(False) 
                self.ui.ComboBox_E1.setCurrentIndex(self.ui.ComboBox_E1.findText(DlgData.data['Field']))
            elif DlgData.data['observe'] == "Field_Integral":
                self.ui.radioButton_integral.setChecked(True)
                self.ui.ComboBox_E1.setEnabled(False)
                self.ui.ComboBox_EDL.setEnabled(True)
                self.ui.ComboBox_SDA.setEnabled(False)
                self.ui.ComboBox_EM.setEnabled(False)
                self.ui.LineEdit_phase1.setEnabled(False)
                self.ui.comboBox_EMIT_EPS.setEnabled(False)
                self.ui.comboBox_CHARGE.setEnabled(False)
                self.ui.comboBox.setEnabled(False) 
                self.ui.ComboBox_EDL.setCurrentIndex(self.ui.ComboBox_EDL.findText(DlgData.data['Field_Integral']))
            elif DlgData.data['observe'] == "Field_Power":
                self.ui.radioButton_power.setChecked(True)
                self.ui.ComboBox_E1.setEnabled(False)
                self.ui.ComboBox_EDL.setEnabled(False)
                self.ui.ComboBox_SDA.setEnabled(True)
                self.ui.ComboBox_EM.setEnabled(False)
                self.ui.LineEdit_phase1.setEnabled(False)
                self.ui.comboBox_EMIT_EPS.setEnabled(False)
                self.ui.comboBox_CHARGE.setEnabled(False)
                self.ui.comboBox.setEnabled(False) 
                self.ui.ComboBox_SDA.setCurrentIndex(self.ui.ComboBox_SDA.findText(DlgData.data['Field_Power']))
            elif DlgData.data['observe'] == "Field_Energy":
                self.ui.radioButton_energy.setChecked(True) 
                self.ui.ComboBox_E1.setEnabled(False)
                self.ui.ComboBox_EDL.setEnabled(False)
                self.ui.ComboBox_SDA.setEnabled(False)
                self.ui.ComboBox_EM.setEnabled(True)
                self.ui.LineEdit_phase1.setEnabled(False)
                self.ui.comboBox_EMIT_EPS.setEnabled(False)
                self.ui.comboBox_CHARGE.setEnabled(False)
                self.ui.comboBox.setEnabled(False) 
                self.ui.ComboBox_EM.setCurrentIndex(self.ui.ComboBox_EM.findText(DlgData.data['Field_Energy']))
            elif DlgData.data['observe'] == "Particle_Statistics":
                self.ui.radioButton_particleStatistics.setChecked(True) 
                self.ui.ComboBox_E1.setEnabled(False)
                self.ui.ComboBox_EDL.setEnabled(False)
                self.ui.ComboBox_SDA.setEnabled(False)
                self.ui.ComboBox_EM.setEnabled(False)
                self.ui.comboBox_EMIT_EPS.setEnabled(True)
                self.ui.comboBox_CHARGE.setEnabled(False)
                
                self.ui.comboBox_EMIT_EPS.setCurrentIndex(self.ui.comboBox_EMIT_EPS.findText(DlgData.data['Particle_Statistics']))
                if self.ui.ComboBox_EM.findText(DlgData.data['Particle_Statistics'])==0:
                    self.ui.comboBox.setEnabled(False) 
                    self.ui.LineEdit_phase1.setEnabled(True)
                    self.ui.LineEdit_phase1.setText(DlgData.data['phase1'])
                else:
                    self.ui.comboBox.setEnabled(True) 
                    self.ui.LineEdit_phase1.setEnabled(False)
                    self.ui.comboBox.setCurrentIndex(self.ui.comboBox.findText(DlgData.data['ParticleType']))
            elif DlgData.data['observe'] == "Particle_Collected":
                self.ui.radioButton_collected.setChecked(True) 
                self.ui.ComboBox_E1.setEnabled(False)
                self.ui.ComboBox_EDL.setEnabled(False)
                self.ui.ComboBox_SDA.setEnabled(False)
                self.ui.ComboBox_EM.setEnabled(False)
                self.ui.comboBox_EMIT_EPS.setEnabled(False)
                self.ui.comboBox_CHARGE.setEnabled(True)
                self.ui.comboBox.setEnabled(True)
                self.ui.LineEdit_phase1.setEnabled(False)
                self.ui.comboBox_CHARGE.setCurrentIndex(self.ui.comboBox_CHARGE.findText(DlgData.data['Particle']))
                self.ui.comboBox.setCurrentIndex(self.ui.comboBox.findText(DlgData.data['ParticleType']))
            elif DlgData.data['observe'] == "Particle_Emitted":
                self.ui.radioButton_emitted.setChecked(True) 
                self.ui.ComboBox_E1.setEnabled(False)
                self.ui.ComboBox_EDL.setEnabled(False)
                self.ui.ComboBox_SDA.setEnabled(False)
                self.ui.ComboBox_EM.setEnabled(False)
                self.ui.comboBox_EMIT_EPS.setEnabled(False)
                self.ui.comboBox_CHARGE.setEnabled(True)
                self.ui.comboBox.setEnabled(True)
                self.ui.LineEdit_phase1.setEnabled(False)
                self.ui.comboBox_CHARGE.setCurrentIndex(self.ui.comboBox_CHARGE.findText(DlgData.data['Particle']))
                self.ui.comboBox.setCurrentIndex(self.ui.comboBox.findText(DlgData.data['ParticleType']))
            elif DlgData.data['observe'] == "Particle_Destroyed":
                self.ui.radioButton_destroyed.setChecked(True) 
                self.ui.ComboBox_E1.setEnabled(False)
                self.ui.ComboBox_EDL.setEnabled(False)
                self.ui.ComboBox_SDA.setEnabled(False)
                self.ui.ComboBox_EM.setEnabled(False)
                self.ui.comboBox_EMIT_EPS.setEnabled(False)
                self.ui.comboBox_CHARGE.setEnabled(True)
                self.ui.comboBox.setEnabled(True)
                self.ui.LineEdit_phase1.setEnabled(False)
                self.ui.comboBox_CHARGE.setCurrentIndex(self.ui.comboBox_CHARGE.findText(DlgData.data['Particle']))
                self.ui.comboBox.setCurrentIndex(self.ui.comboBox.findText(DlgData.data['ParticleType']))
        except KeyError as reason:
            sayz("!!!Error:KeyError,Maybe lack of key:%s"%str(reason))               

    def keepData(self,DlgData):
        
        DlgData.addData("name",DlgData.id)
        # 添加一个别名  @lizhenguang
        DlgData.addData("name2",self.ui.lineEdit_name2.text().replace(' ',''))
        DlgData.addData("Dlg_Type","Obs_Type")
        if self.ui.ComboBox_type.currentIndex() == 0:
            DlgData.addData("TimeType","POINT") 
        elif self.ui.ComboBox_type.currentIndex() == 1:
            DlgData.addData("TimeType","LINE")
        elif self.ui.ComboBox_type.currentIndex() == 2:
            DlgData.addData("TimeType","AREA")
        elif self.ui.ComboBox_type.currentIndex() == 3:
            DlgData.addData("TimeType","VOLUME") 
        DlgData.addData("Type",self.ui.ComboBox_Shadow.currentText())  
        if self.ui.ComboBox_Shadow.currentIndex() == 0: 
            DlgData.addData("isAppoint",False)
        else:
            ObjectsTools.findObjByLabelWithoutOrderAndInvisible(self.ui.ComboBox_Shadow.currentText())
            DlgData.addData("isAppoint",True)         
        DlgData.addData("start_R",self.ui.LineEdit_start_x.text())
        DlgData.addData("start_Y",self.ui.LineEdit_start_y.text())
        DlgData.addData("start_Z",self.ui.LineEdit_start_z.text())        
        DlgData.addData("end_R",self.ui.LineEdit_end_x.text())
        DlgData.addData("end_Y",self.ui.LineEdit_end_y.text())
        DlgData.addData("end_Z",self.ui.LineEdit_end_z.text())
        # 法向选择
        if self.ui.radioButton_x.isChecked():             
            DlgData.addData("normal","R")
        elif self.ui.radioButton_y.isChecked():             
            DlgData.addData("normal","theta")
        else:             
            DlgData.addData("normal","Z")

        # 观测项
        if self.ui.radioButton_field.isChecked():          
            DlgData.addData("observe","Field")
            DlgData.addData("isField",True)
            fieldd = [self.ui.ComboBox_E1.currentText()]
        elif self.ui.radioButton_integral.isChecked():          
            DlgData.addData("observe","Field_Integral")
            DlgData.addData("isFieldIntegral",True)
            fieldd = [self.ui.ComboBox_EDL.currentText()]
        elif self.ui.radioButton_power.isChecked():          
            DlgData.addData("observe","Field_Power")
            DlgData.addData("isFieldPower",True)
            fieldd = [self.ui.ComboBox_SDA.currentText()]
        elif self.ui.radioButton_energy.isChecked():          
            DlgData.addData("observe","Field_Energy") 
            DlgData.addData("isFieldEnergy",True) 
            fieldd = [self.ui.ComboBox_EM.currentText() ]
        elif self.ui.radioButton_particleStatistics.isChecked():             
            DlgData.addData("observe","Particle_Statistics")   
            DlgData.addData("isParticleStatistics",True)
            if self.ui.comboBox_EMIT_EPS.currentIndex() == 0:
                fieldd = [self.ui.comboBox_EMIT_EPS.currentText(),self.ui.LineEdit_phase1.text()]
            else:
                fieldd = [self.ui.comboBox_EMIT_EPS.currentText(),self.ui.comboBox.currentText()]
        elif self.ui.radioButton_collected.isChecked():             
            DlgData.addData("observe","Particle_Collected")   
            DlgData.addData("isParticleCollected",True)
            fieldd = [self.ui.comboBox_CHARGE.currentText(),self.ui.comboBox.currentText()]
        elif self.ui.radioButton_emitted.isChecked():             
            DlgData.addData("observe","Particle_Emitted")   
            DlgData.addData("isParticleEmitted",True)
            fieldd = [self.ui.comboBox_CHARGE.currentText(),self.ui.comboBox.currentText()]
        elif self.ui.radioButton_destroyed.isChecked():             
            DlgData.addData("observe","Particle_Destroyed")   
            DlgData.addData("isParticleDestroyed",True)
            fieldd =[self.ui.comboBox_CHARGE.currentText(),self.ui.comboBox.currentText()]
        DlgData.addData("observe_field",fieldd)      
                                                   
        # 分类  
        DlgData.addData("Field",self.ui.ComboBox_E1.currentText())
        DlgData.addData("Field_Integral",self.ui.ComboBox_EDL.currentText())
        DlgData.addData("Field_Power",self.ui.ComboBox_SDA.currentText())
        DlgData.addData("Field_Energy",self.ui.ComboBox_EM.currentText())
        DlgData.addData("phase1",self.ui.LineEdit_phase1.text())
        DlgData.addData("Particle_Statistics",self.ui.comboBox_EMIT_EPS.currentText())
        DlgData.addData("Particle",self.ui.comboBox_CHARGE.currentText())
        DlgData.addData("ParticleType",self.ui.comboBox.currentText())

        # 傅里叶       
        DlgData.addData("Fourier_Checked",self.ui.checkBox_Fourier.isChecked())              
        if self.ui.radioButton_real.isChecked():             
            DlgData.addData("Fourier","real")
            DlgData.addData("fftType","MAGNITUDE")
        else:             
            DlgData.addData("Fourier","complex") 
            DlgData.addData("fftType","COMPLEX") 
            
        # 频率范围
        DlgData.addData("freq_Checked",self.ui.checkBox_freq.isChecked())        
        DlgData.addData("freq1",self.ui.LineEdit_freq1.text())           
        DlgData.addData("freq2",self.ui.LineEdit_freq2.text())                 
        # 时间范围
        DlgData.addData("limit_Checked",self.ui.checkBox_limit.isChecked())        
        DlgData.addData("limit1",self.ui.LineEdit_limit1.text())           
        DlgData.addData("limit2",self.ui.LineEdit_limit2.text())
        # 观察间隔
        DlgData.addData("interval_Checked",self.ui.checkBox_interval.isChecked())        
        DlgData.addData("interval",self.ui.lineEdit_interval.text())           
        # 参数
        DlgData.addData("dataSmooth_Checked",self.ui.checkBox_dataSmooth.isChecked())
        if self.ui.radioButton_time.isChecked():             
            DlgData.addData("dataSmooth","STEP")
        else:             
            DlgData.addData("dataSmooth","LO_PASS") 
        DlgData.addData("timeParam",self.ui.LineEdit_timeParam.text())
        Comment = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict)
        old = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict)
        Comment[DlgData.id] = DlgData.data

        FreeCAD.ActiveDocument.Begin = json.dumps(Comment)

        #返回面板中的内容是否改变
        return cmp(old,Comment)!=0
    # x法向修改时，修改起点即修改终点
    def LineEdit_start_x_textChanged(self):
        if not self.ui.LineEdit_end_x.isEnabled():
            self.ui.LineEdit_end_x.setText(self.ui.LineEdit_start_x.text())

    # y法向修改时，修改起点即修改终点
    def LineEdit_start_y_textChanged(self):
        if not self.ui.LineEdit_end_y.isEnabled():
            self.ui.LineEdit_end_y.setText(self.ui.LineEdit_start_y.text())

    # z法向修改时，修改起点即修改终点
    def LineEdit_start_z_textChanged(self):
        if not self.ui.LineEdit_end_z.isEnabled():
            self.ui.LineEdit_end_z.setText(self.ui.LineEdit_start_z.text())

    # 点击法向x按钮
    def radioButton_x_clicked(self):
        if self.ui.ComboBox_type.currentIndex() == 1:
            self.ui.LineEdit_end_x.setEnabled(True)
            self.ui.LineEdit_end_y.setEnabled(False)
            self.ui.LineEdit_end_z.setEnabled(False)
            self.ui.LineEdit_end_y.setText(self.ui.LineEdit_start_y.text())
            self.ui.LineEdit_end_z.setText(self.ui.LineEdit_start_z.text())
        elif self.ui.ComboBox_type.currentIndex() == 2:
            self.ui.LineEdit_end_x.setEnabled(False)
            self.ui.LineEdit_end_y.setEnabled(True)
            self.ui.LineEdit_end_z.setEnabled(True)
            self.ui.LineEdit_end_x.setText(self.ui.LineEdit_start_x.text())

    # 点击法向y按钮
    def radioButton_y_clicked(self):
        if self.ui.ComboBox_type.currentIndex() == 1:
            self.ui.LineEdit_end_y.setEnabled(True)
            self.ui.LineEdit_end_x.setEnabled(False)
            self.ui.LineEdit_end_z.setEnabled(False)
            self.ui.LineEdit_end_x.setText(self.ui.LineEdit_start_x.text())
            self.ui.LineEdit_end_z.setText(self.ui.LineEdit_start_z.text())
        elif self.ui.ComboBox_type.currentIndex() == 2:
            self.ui.LineEdit_end_y.setEnabled(False)
            self.ui.LineEdit_end_x.setEnabled(True)
            self.ui.LineEdit_end_z.setEnabled(True)
            self.ui.LineEdit_end_y.setText(self.ui.LineEdit_start_y.text())

    # 点击法向z按钮
    def radioButton_z_clicked(self):
        if self.ui.ComboBox_type.currentIndex() == 1:
            self.ui.LineEdit_end_z.setEnabled(True)
            self.ui.LineEdit_end_x.setEnabled(False)
            self.ui.LineEdit_end_y.setEnabled(False)
            self.ui.LineEdit_end_x.setText(self.ui.LineEdit_start_x.text())
            self.ui.LineEdit_end_y.setText(self.ui.LineEdit_start_y.text())
        elif self.ui.ComboBox_type.currentIndex() == 2:
            self.ui.LineEdit_end_z.setEnabled(False)
            self.ui.LineEdit_end_x.setEnabled(True)
            self.ui.LineEdit_end_y.setEnabled(True)
            self.ui.LineEdit_end_z.setText(self.ui.LineEdit_start_z.text())

    # 场按钮点击事件
    def radioButton_field_clicked(self):
        self.ui.radioButton_field.setChecked(True)
        self.ui.ComboBox_E1.setEnabled(True)
        self.ui.ComboBox_EDL.setEnabled(False)
        self.ui.ComboBox_SDA.setEnabled(False)
        self.ui.LineEdit_phase1.setEnabled(False)
        self.ui.ComboBox_EM.setEnabled(False)
        self.ui.comboBox_EMIT_EPS.setEnabled(False)
        self.ui.comboBox_CHARGE.setEnabled(False)
        self.ui.comboBox.setEnabled(False)
    # 场积分按钮点击事件
    def radioButton_integral_clicked(self):      
        self.ui.radioButton_integral.setChecked(True)  
        self.ui.ComboBox_E1.setEnabled(False)
        self.ui.ComboBox_EDL.setEnabled(True)
        self.ui.ComboBox_SDA.setEnabled(False)
        self.ui.LineEdit_phase1.setEnabled(False)
        self.ui.ComboBox_EM.setEnabled(False)   
        self.ui.comboBox_EMIT_EPS.setEnabled(False)
        self.ui.comboBox_CHARGE.setEnabled(False)
        self.ui.comboBox.setEnabled(False) 
    # 场功率按钮点击事件
    def radioButton_power_clicked(self):
        self.ui.radioButton_power.setChecked(True)
        self.ui.ComboBox_E1.setEnabled(False)        
        self.ui.ComboBox_EDL.setEnabled(False)
        self.ui.ComboBox_SDA.setEnabled(True)
        self.ui.LineEdit_phase1.setEnabled(False)
        self.ui.ComboBox_EM.setEnabled(False)      
        self.ui.comboBox_EMIT_EPS.setEnabled(False)
        self.ui.comboBox_CHARGE.setEnabled(False)
        self.ui.comboBox.setEnabled(False)    
    # 场能量按钮点击事件
    def radioButton_energy_clicked(self): 
        self.ui.radioButton_energy.setChecked(True)
        self.ui.ComboBox_E1.setEnabled(False)        
        self.ui.ComboBox_EDL.setEnabled(False)        
        self.ui.ComboBox_SDA.setEnabled(False)
        self.ui.LineEdit_phase1.setEnabled(False)
        self.ui.ComboBox_EM.setEnabled(True)    
        self.ui.comboBox_EMIT_EPS.setEnabled(False)
        self.ui.comboBox_CHARGE.setEnabled(False)
        self.ui.comboBox.setEnabled(False)       
    # 粒子统计按钮点击事件
    def radioButton_particleStatistics_clicked(self):
        self.ui.ComboBox_E1.setEnabled(False)        
        self.ui.ComboBox_EDL.setEnabled(False)        
        self.ui.ComboBox_SDA.setEnabled(False)            
        self.ui.ComboBox_EM.setEnabled(False)
        self.ui.comboBox_CHARGE.setEnabled(False)
        self.ui.comboBox_EMIT_EPS.setEnabled(True)
        if self.ui.comboBox_EMIT_EPS.currentIndex() == 0:
            self.ui.LineEdit_phase1.setEnabled(True)
            self.ui.comboBox.setEnabled(False)
        else:
            self.ui.LineEdit_phase1.setEnabled(False)
            self.ui.comboBox.setEnabled(True)
    #粒子统计下拉框
    def comboBox_EMIT_EPS_clicked(self):
        if self.ui.comboBox_EMIT_EPS.currentIndex() == 0:
            self.ui.LineEdit_phase1.setEnabled(True)
            self.ui.comboBox.setEnabled(False)
        else:
            self.ui.LineEdit_phase1.setEnabled(False)
            self.ui.comboBox.setEnabled(True)
    # radioButton_collected、radioButton_emitted、radioButton_destroyed按钮点击事件
    def radioButton_clicked(self):
        self.ui.ComboBox_E1.setEnabled(False)        
        self.ui.ComboBox_EDL.setEnabled(False)        
        self.ui.ComboBox_SDA.setEnabled(False)            
        self.ui.ComboBox_EM.setEnabled(False)
        self.ui.comboBox_EMIT_EPS.setEnabled(False)
        self.ui.LineEdit_phase1.setEnabled(False)
        self.ui.comboBox_CHARGE.setEnabled(True)
        self.ui.comboBox.setEnabled(True)

    # 傅里叶快速变换按钮点击事件
    def checkBox_Fourier_clicked(self):
        self.ui.radioButton_real.setEnabled(self.ui.checkBox_Fourier.isChecked())
        self.ui.radioButton_complex.setEnabled(self.ui.checkBox_Fourier.isChecked())
        # 显示频率范围
        self.ui.checkBox_freq.setEnabled(self.ui.checkBox_Fourier.isChecked())        
        # self.ui.LineEdit_freq1.setEnabled(self.ui.checkBox_Fourier.isChecked())
        # self.ui.LineEdit_freq2.setEnabled(self.ui.checkBox_Fourier.isChecked())   
    # 频率范围点击事件
    def checkBox_freq_clicked(self):
        self.ui.LineEdit_freq1.setEnabled(self.ui.checkBox_freq.isChecked())
        self.ui.LineEdit_freq2.setEnabled(self.ui.checkBox_freq.isChecked())
    # 时间范围点击事件
    def checkBox_limit_clicked(self):
        self.ui.LineEdit_limit1.setEnabled(self.ui.checkBox_limit.isChecked())
        self.ui.LineEdit_limit2.setEnabled(self.ui.checkBox_limit.isChecked())
    # 观察间隔点击事件
    def checkBox_interval_clicked(self):
        self.ui.lineEdit_interval.setEnabled(self.ui.checkBox_interval.isChecked())
        self.ui.lineEdit_interval.setValidator(QtGui.QIntValidator())#设置只能输入int类型的数据
    # 数据平滑处理
    def checkBox_dataSmooth_clicked(self):
        self.ui.radioButton_time.setEnabled(self.ui.checkBox_dataSmooth.isChecked())
        self.ui.radioButton_RC.setEnabled(self.ui.checkBox_dataSmooth.isChecked())
        self.ui.LineEdit_timeParam.setEnabled(self.ui.checkBox_dataSmooth.isChecked())

    def setNameUnable(self):
        self.ui.LineEdit_Name.setEnabled(False)

    def refreshComboxType(self):
        '''
        用来加载新型粒子定义
        '''
        new_list = []
        JSON_CADComment = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict)
        for i in JSON_CADComment.keys():
            if JSON_CADComment[i]["Dlg_Type"] == "Species_Type":
                new_list.append(JSON_CADComment[i]["name"])
        self.ui.comboBox.clear()
        self.ui.comboBox.addItem("ALL")
        self.ui.comboBox.addItem("ELECTRON")
        self.ui.comboBox.addItem("PROTON")
        for i in new_list:
            self.ui.comboBox.addItem(i)
