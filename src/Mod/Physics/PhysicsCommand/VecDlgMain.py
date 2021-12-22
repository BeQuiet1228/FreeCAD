#-*- coding: utf-8 -*-
import json

import FreeCAD
from PySide import QtGui

import Physics.PhysicsGui.VectorDlg
import Simulation
from DlgData import DlgData, sayz,getDlgData

from Modeling.Common.Tools import DocumentTools,ObjectsTools
import ObservePalMain
from Modeling.Common.CommonCommand.NewDocument import ObjectDict
import File.FileCommand.M3DFile.M3DFileUtil
import File.FileCommand.TextUI.FileTextView
from PhysicsTools import CompleterTools
from Modeling.Common.Tools.PhysicsDialog import *
import DoManager
#json格式数据需要保持原有顺序输出
from collections import OrderedDict
flag = 0
def show(type,className,itemUserName):
    if type == "new":
        ObjectDict[className] = VectorShow("new",className)
        ObjectDict[className].setModal(False)
        ObjectDict[className].show()
        ObjectDict[className].exec_()
    elif type == "old":
        if className in ObjectDict.keys():
            # 增加了撤销操作后，数据可能发生变化，所以每次需要重新加载数据，
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
            ObjectDict[className] = VectorShow(className,className)
            ObjectDict[className].flagUpdateItemName = True
            ObjectDict[className].setNameUnable()
            ObjectDict[className].setModal(False)
            ObjectDict[className].show()
            ObjectDict[className].exec_()    
         
class VectorShow(PhysicsDialog):
    count = 0
    def __init__(self, DialogID,className, parent=None):
        PhysicsDialog.__init__(self, parent)
        self.ui = Physics.PhysicsGui.VectorDlg.Ui_Dialog_VectorDlg()
        self.ui.setupUi(self)
        #代码补全
        CompleterTools.setLineEditsCompleter(CompleterTools.getAllLineEdits(self.ui))
        self.defaultValue = ["OSYS$MIDPLANE1","OSYS$MIDPLANE2","OSYS$MIDPLANE3"]
        #!!!!
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

        self.ui.LineEdit_start_x.textChanged.connect(self.LineEdit_start_x_textChanged)
        self.ui.LineEdit_start_y.textChanged.connect(self.LineEdit_start_y_textChanged)
        self.ui.LineEdit_start_z.textChanged.connect(self.LineEdit_start_z_textChanged)

        self.ui.pushButton.clicked.connect(self.onCancel)
        self.ui.radioButton_x.clicked.connect(self.radioButton_x_clicked)
        self.ui.radioButton_y.clicked.connect(self.radioButton_y_clicked)
        self.ui.radioButton_z.clicked.connect(self.radioButton_z_clicked)

        self.ui.checkBox_vector.clicked.connect(self.checkBox_vector_clicked)
        #刷新下拉框
        self.refreshCombox()
        # 正投影面下拉框选择事件
        self.ui.ComboBox_Shadow.currentIndexChanged.connect(self.ComboBox_Shadow_clicked)
        # 加载每个Project都具有的Comment【里面存储着对话框的所有数据】----》JSON对象----》应用于加载窗口    
        JSON_CADComment = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict)

        # self.ui.pushButton_ok.clicked.connect(lambda: self.onConfirm(JSON_CADComment,className)) 
        self.initDialog(JSON_CADComment,className)
        
        if DialogID != "new":
            oldData = DlgData(JSON_CADComment[DialogID],DialogID)
            self.loadData(oldData)            
            flag = 1  
        self.userNameBefore=self.ui.LineEdit_Name.text()
                #用于判断是否进行名称更新
        self.flagUpdateItemName=False
        self.ComboBox_Shadow_clicked()
        # 适配分辨率
        import AdaptiveDPIUtil
        new_x, new_y = AdaptiveDPIUtil.get_new_dpi(self.width(), self.height())
        self.resize(500, new_y)

    def refreshCombox(self):  
        '''
        每次加载窗口时都要重新加载下拉列表，以实现动态加载
        一般来说就是ComboBox_Shadow_list需要动态刷新
        First:先将下拉列表里面的内容读取（append）到Combox_???_list[]中
        Second：读取数据池里面的数据---》Orthogonal_list
        Third：如果》Orthogonal_list中的item不在Combox_???_list[]中，新增它！！！
        '''
        JSON_CADComment = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict)
        keys = JSON_CADComment.keys()
  
        ComboBox_Shadow_list=[]
        ComboBox_timer_list=[]
        Timer_list=[]
        for i in range(self.ui.ComboBox_Shadow.count()):
            ComboBox_Shadow_list.append(self.ui.ComboBox_Shadow.itemText(i))
        Orthogonal_list = DocumentTools.getActiveDocTypes("Area_Conformal")
        Orthogonal_list.append("OSYS$MIDPLANE1")
        Orthogonal_list.append("OSYS$MIDPLANE2")
        Orthogonal_list.append("OSYS$MIDPLANE3")
        for i in range(self.ui.ComboBox_timer.count()):
            ComboBox_timer_list.append(self.ui.ComboBox_timer.itemText(i))
        for i in keys:
            if JSON_CADComment[i]["Dlg_Type"] == "Timer_Type":
                Timer_list.append(JSON_CADComment[i]["name"])
        for i in Timer_list:
            if i not in ComboBox_timer_list:
                self.ui.ComboBox_timer.addItem(i)  

        for i in Orthogonal_list:
            if i not in ComboBox_Shadow_list:
                self.ui.ComboBox_Shadow.addItem(i)  
                 
    def ComboBox_Shadow_clicked(self):
        ObjectsTools.findObjByLabelWithoutOrderAndVisible(self.ui.ComboBox_Shadow.currentText())
        if self.ui.ComboBox_Shadow.currentIndex() == 0:
            self.ui.radioButton_x.setEnabled(True)
            self.ui.radioButton_y.setEnabled(True)
            self.ui.radioButton_z.setEnabled(True)
            self.ui.LineEdit_start_x.setEnabled(True)
            self.ui.LineEdit_start_y.setEnabled(True)
            self.ui.LineEdit_start_z.setEnabled(True)
            if self.ui.radioButton_x.isChecked() == True:
                self.ui.LineEdit_end_x.setEnabled(False)
                self.ui.LineEdit_end_y.setEnabled(True)
                self.ui.LineEdit_end_z.setEnabled(True)
            if self.ui.radioButton_y.isChecked() == True:
                self.ui.LineEdit_end_x.setEnabled(True)
                self.ui.LineEdit_end_y.setEnabled(False)
                self.ui.LineEdit_end_z.setEnabled(True)
            if self.ui.radioButton_z.isChecked() == True:
                self.ui.LineEdit_end_x.setEnabled(True)
                self.ui.LineEdit_end_y.setEnabled(True)
                self.ui.LineEdit_end_z.setEnabled(False)
        else:
            objName = self.ui.ComboBox_Shadow.currentText()
            if objName in self.defaultValue:
                pass
            else:
                modelData = DocumentTools.getValueOfAreaObjByLable(objName)
                self.ui.LineEdit_start_x.setText(str(modelData[1]))
                self.ui.LineEdit_start_y.setText(str(modelData[2]))
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
            self.ui.radioButton_x.setEnabled(False)
            self.ui.radioButton_y.setEnabled(False)
            self.ui.radioButton_z.setEnabled(False)
            self.ui.LineEdit_start_x.setEnabled(False)
            self.ui.LineEdit_start_y.setEnabled(False)
            self.ui.LineEdit_start_z.setEnabled(False)
            self.ui.LineEdit_end_x.setEnabled(False)
            self.ui.LineEdit_end_y.setEnabled(False)
            self.ui.LineEdit_end_z.setEnabled(False)

            # 点击取消按钮关闭窗口
    def onCancel(self):
        # if self.flagUpdateItemName:
        #     JSON_CADComment = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict)
        #     oldData = DlgData(JSON_CADComment[self.userNameBefore],self.userNameBefore)
        #     self.loadData(oldData)
        self.close()
    def onConfirm(self,FreeCAD_Comment_Dict,className):
        oldJson = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict)
        # 存储只修改数据而没有修改item名的情况
        oldData = ["modify", self.userNameBefore, className]
        itemData = ["modify", self.userNameBefore, className]
        global flag 
        count = 1
        name = self.ui.LineEdit_Name.text()  
        self.close()
        if flag == 0:              
            while name in FreeCAD_Comment_Dict.keys(): 
               name = self.ui.LineEdit_Name.text() + str(count) 
               count+=1       
            self.ui.LineEdit_Name.setText(name)
            itemData, oldData = ObservePalMain.addItem(u"矢量观测", name, className)
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
                    itemData, oldData = ObservePalMain.updateItemName(name)
                    self.flagUpdateItemName=False
        self.userNameBefore=name
        newData = DlgData({},name)
        isModify =self.keepData(newData)
        if isModify and itemData is not None:
            jsonData = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict)

            # 更新两个栈
            record = [jsonData, itemData, oldJson, oldData]
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
            # 设置标记的旧名字
            self.userNameBefore = DlgData.data['name']
            self.ui.ComboBox_Shadow.setCurrentIndex(self.ui.ComboBox_Shadow.findText(DlgData.data['Orthogonal_projection_surface']))
            self.ui.LineEdit_start_x.setText(DlgData.data['start_R'])
            self.ui.LineEdit_start_y.setText(DlgData.data['start_Y'])
            self.ui.LineEdit_start_z.setText(DlgData.data['start_Z'])

            self.ui.LineEdit_end_x.setText(DlgData.data['end_R'])
            self.ui.LineEdit_end_y.setText(DlgData.data['end_Y'])
            self.ui.LineEdit_end_z.setText(DlgData.data['end_Z'])

            # 观测场1
            self.ui.ComboBox_C1.setCurrentIndex(self.ui.ComboBox_C1.findText(DlgData.data['Observation_field_1']))
            # 观测场2
            self.ui.ComboBox_C2.setCurrentIndex(self.ui.ComboBox_C2.findText(DlgData.data['Observation_field_2']))    
            # 定时器
            self.ui.ComboBox_timer.setCurrentIndex(self.ui.ComboBox_timer.findText(DlgData.data['Timer']))
            # 等值线
            self.ui.checkBox_vector.setChecked(DlgData.data['Vector_Checked'])
            self.ui.LineEdit_SL1.setEnabled(DlgData.data['Vector_Checked'])
            self.ui.LineEdit_SL2.setEnabled(DlgData.data['Vector_Checked'])
            self.ui.LineEdit_SL1.setText(DlgData.data['Vector_1'])
            self.ui.LineEdit_SL2.setText(DlgData.data['Vector_2'])
            # 法向选择
            if DlgData.data['normal'] == "R":
                self.ui.radioButton_x.setChecked(True)
            if DlgData.data['normal'] == "theta":
                self.ui.radioButton_y.setChecked(True)
            if DlgData.data['normal'] == "Z":
                self.ui.radioButton_z.setChecked(True)            
        except KeyError as reason:
            sayz("!!!Error:KeyError,Maybe lack of key:%s"%str(reason))

    def keepData(self,DlgData):
        DlgData.addData("name",DlgData.id)
        DlgData.addData("Orthogonal_projection_surface",self.ui.ComboBox_Shadow.currentText()) 
        if self.ui.ComboBox_Shadow.currentIndex() == 0: 
            DlgData.addData("isAppointArea",False)
        else:
            ObjectsTools.findObjByLabelWithoutOrderAndInvisible(self.ui.ComboBox_Shadow.currentText())
            DlgData.addData("isAppointArea",True) 
        DlgData.addData("Dlg_Type","Vec_Type")        
        DlgData.addData("start_R",self.ui.LineEdit_start_x.text())
        DlgData.addData("start_Y",self.ui.LineEdit_start_y.text())
        DlgData.addData("start_Z",self.ui.LineEdit_start_z.text())        
        DlgData.addData("end_R",self.ui.LineEdit_end_x.text())
        DlgData.addData("end_Y",self.ui.LineEdit_end_y.text())
        DlgData.addData("end_Z",self.ui.LineEdit_end_z.text())
        # 法向选择
        if self.ui.radioButton_x.isChecked():             
            DlgData.addData("normal","R")
        if self.ui.radioButton_y.isChecked():             
            DlgData.addData("normal","theta")
        if self.ui.radioButton_z.isChecked():             
            DlgData.addData("normal","Z")
        # 观测场1
        DlgData.addData("Observation_field_1",self.ui.ComboBox_C1.currentText())
        # 观测场2
        DlgData.addData("Observation_field_2",self.ui.ComboBox_C2.currentText())           
        # 定时器
        DlgData.addData("Timer", self.ui.ComboBox_timer.currentText())
        if self.ui.ComboBox_timer.currentText() == u"默认定时器":
            DlgData.addData("Timer2MX","DefTimer")
        elif self.ui.ComboBox_timer.currentText() == u"仅开始时刻":
            DlgData.addData("Timer2MX","TSYS$FIRST")
        elif self.ui.ComboBox_timer.currentText() == u"仅结束时刻":
            DlgData.addData("Timer2MX", "TSYS$LAST")
        else:
            DlgData.addData("Timer2MX", self.ui.ComboBox_timer.currentText())
        # 指定
        DlgData.addData("Vector_Checked",self.ui.checkBox_vector.isChecked())        
        DlgData.addData("Vector_1",self.ui.LineEdit_SL1.text())
        DlgData.addData("Vector_2",self.ui.LineEdit_SL2.text())
        Comment = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict)
        old = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict)
        Comment[DlgData.id] = DlgData.data
        FreeCAD.ActiveDocument.Begin = json.dumps(Comment)
        # 返回面板中的内容是否改变
        return cmp(old, Comment) != 0
        # vec = M3DFileUtil()
        # vec.addOrUpdateVectorCommands(
        # DlgData.getData("Observation_field_1"),
        # DlgData.getData("Observation_field_2"),
        # DlgData.id,
        # DlgData.getData("Timer2MX"),
        # isNumber=DlgData.getData("Vector_Checked"),number1=DlgData.getData("Vector_1"),number2=DlgData.getData("Vector_2"),
        # isAppointArea=DlgData.getData("isAppointArea"),areaName=DlgData.getData("Orthogonal_projection_surface"),
        # startPointCoordinates=[DlgData.getData("start_R"),DlgData.getData("start_Y"),DlgData.getData("start_Z")], stopPointCoordinates=[DlgData.getData("end_R"),DlgData.getData("end_Y"),DlgData.getData("end_Z")],
        # )         

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
        self.ui.LineEdit_end_x.setEnabled(False)
        self.ui.LineEdit_end_y.setEnabled(True)
        self.ui.LineEdit_end_z.setEnabled(True)
        self.ui.LineEdit_end_x.setText(self.ui.LineEdit_start_x.text())

    # 点击法向y按钮
    def radioButton_y_clicked(self):
        self.ui.LineEdit_end_y.setEnabled(False)
        self.ui.LineEdit_end_x.setEnabled(True)
        self.ui.LineEdit_end_z.setEnabled(True)
        self.ui.LineEdit_end_y.setText(self.ui.LineEdit_start_y.text())

    # 点击法向z按钮
    def radioButton_z_clicked(self):
        self.ui.LineEdit_end_z.setEnabled(False)
        self.ui.LineEdit_end_x.setEnabled(True)
        self.ui.LineEdit_end_y.setEnabled(True)
        self.ui.LineEdit_end_z.setText(self.ui.LineEdit_start_z.text())

    def checkBox_vector_clicked(self):
        if self.ui.checkBox_vector.isChecked():
            self.ui.LineEdit_SL1.setEnabled(True)
            self.ui.LineEdit_SL2.setEnabled(True)
        else:
            self.ui.LineEdit_SL1.setEnabled(False)
            self.ui.LineEdit_SL2.setEnabled(False)

    def setNameUnable(self):
        self.ui.LineEdit_Name.setEnabled(False)


 