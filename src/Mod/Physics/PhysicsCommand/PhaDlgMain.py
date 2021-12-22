#-*- coding: utf-8 -*-
import json

import FreeCAD
from PySide import QtGui

import Physics.PhysicsGui.PhaDlg
from DlgData import DlgData, sayz,getDlgData

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
        ObjectDict[className] = PhaShow("new",className)
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
            ObjectDict[className].flagUpdateItemName=True
            ObjectDict[className].setNameUnable()
            ObjectDict[className].setModal(False) 
            ObjectDict[className].show()
            ObjectDict[className].exec_()             
        else:
            ObjectDict[className] = PhaShow(className,className)
            ObjectDict[className].flagUpdateItemName = True
            ObjectDict[className].setNameUnable()
            ObjectDict[className].setModal(False)
            ObjectDict[className].show()
            ObjectDict[className].exec_()  
        
class PhaShow(PhysicsDialog):
    def __init__(self,DialogID,className,parent=None):
        PhysicsDialog.__init__(self, parent)
        self.ui = Physics.PhysicsGui.PhaDlg.Ui_Dialog_PhaDlg()
        self.ui.setupUi(self)
        #代码补全
        CompleterTools.setLineEditsCompleter(CompleterTools.getAllLineEdits(self.ui))
        global flag
        flag = 0
        self.ui.pushButton.clicked.connect(self.onCancel)
        self.ui.checkBox_thick.clicked.connect(self.checkBox_thick_clicked)
        self.ui.checkBox_suffix.clicked.connect(self.checkBox_suffix_clicked)
        # 使观测粒子不可选
        # self.ui.ComboBox_Observation_particle.setEnabled(False)
       
        #刷新下拉框
        self.refreshCombox()
        self.refreshComboxType()
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

        # 适配分辨率
        import AdaptiveDPIUtil
        new_x, new_y = AdaptiveDPIUtil.get_new_dpi(self.width(), self.height())
        self.resize(new_x, new_y)

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
        ComboBox_timer_list=[]
        Timer_list=[]
        for i in range(self.ui.ComboBox_timer.count()):
            ComboBox_timer_list.append(self.ui.ComboBox_timer.itemText(i))
        for i in keys:
            if JSON_CADComment[i]["Dlg_Type"] == "Timer_Type":
                Timer_list.append(JSON_CADComment[i]["name"])
        Timer_list.append("TSYS$FIRST")
        Timer_list.append("TSYS$LAST")
        Timer_list.append("TSYS$EIGEN")
        Timer_list.append("TSYS$EIGENMODE")
        Timer_list.append("TSYS$ENERGY")
        for i in Timer_list:
            if i not in ComboBox_timer_list:
                self.ui.ComboBox_timer.addItem(i)  
             
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
            itemData, oldData = ObservePalMain.addItem(u"粒子观测", name, className)
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
            # 观测粒子
            self.ui.ComboBox_Observation_particle.setCurrentIndex(DlgData.data['Observation_particle'])           
            # 定时器
            self.ui.ComboBox_timer.setCurrentIndex(self.ui.ComboBox_timer.findText(DlgData.data['Timer']))
            # 横轴
            self.ui.ComboBox_Horizon.setCurrentIndex(self.ui.ComboBox_Horizon.findText(DlgData.data['Horizon']))
            # 纵轴
            self.ui.ComboBox_Vertical.setCurrentIndex(self.ui.ComboBox_Vertical.findText(DlgData.data['Vertical']))
            # 显示厚度
            self.ui.checkBox_thick.setChecked(DlgData.data['Thick_Checked'])
            self.ui.ComboBox_thick.setEnabled(DlgData.data['Thick_Checked'])
            self.ui.LineEdit_thick1.setEnabled(DlgData.data['Thick_Checked'])
            self.ui.LineEdit_thick2.setEnabled(DlgData.data['Thick_Checked'])
            self.ui.ComboBox_thick.setCurrentIndex(self.ui.ComboBox_thick.findText(DlgData.data['Thick']))
            self.ui.LineEdit_thick1.setText(DlgData.data['Thickness_1'])
            self.ui.LineEdit_thick2.setText(DlgData.data['Thickness_2'])   
            # 后缀
            self.ui.checkBox_suffix.setChecked(DlgData.data['Suffix_Checked'])
            self.ui.LineEdit_phase.setEnabled(DlgData.data['Suffix_Checked'])
            self.ui.LineEdit_phase.setText(DlgData.data['phase']) 
        except KeyError as reason:
            sayz("!!!Error:KeyError,Maybe lack of key:%s"%str(reason))        
    def keepData(self,DlgData):
        DlgData.addData("name",DlgData.id)
        # 观测粒子
        DlgData.addData("Observation_particle",self.ui.ComboBox_Observation_particle.currentIndex())
        DlgData.addData("Dlg_Type","Pha_Type")
        if self.ui.ComboBox_Observation_particle.currentText() == u"全部":  
            DlgData.addData("Species","ALL")         
        elif self.ui.ComboBox_Observation_particle.currentText() == u"电子":  
            DlgData.addData("Species","ELECTRON") 
        elif self.ui.ComboBox_Observation_particle.currentText() == u"质子":
            DlgData.addData("Species","PROTON")
        else:
            DlgData.addData("Species", self.ui.ComboBox_Observation_particle.currentText())
        # 定时器
        DlgData.addData("Timer",self.ui.ComboBox_timer.currentText())  
        if self.ui.ComboBox_timer.currentText() == u"默认定时器":  
            DlgData.addData("Timer2MX","DefTimer")         
        elif self.ui.ComboBox_timer.currentText() == u"仅开始时刻":  
            DlgData.addData("Timer2MX","TSYS$FIRST")
        elif self.ui.ComboBox_timer.currentText() == u"仅结束时刻":
            DlgData.addData("Timer2MX", "TSYS$LAST")
        else:
            DlgData.addData("Timer2MX", self.ui.ComboBox_timer.currentText())
        # 横轴
        DlgData.addData("Horizon",self.ui.ComboBox_Horizon.currentText())
        # 纵轴
        DlgData.addData("Vertical",self.ui.ComboBox_Vertical.currentText())
        # 显示厚度
        DlgData.addData("Thick_Checked",self.ui.checkBox_thick.isChecked())
        DlgData.addData("Thick",self.ui.ComboBox_thick.currentText())
        DlgData.addData("Thickness_1",self.ui.LineEdit_thick1.text())
        DlgData.addData("Thickness_2",self.ui.LineEdit_thick2.text())        
        # 后缀
        DlgData.addData("Suffix_Checked",self.ui.checkBox_suffix.isChecked())
        DlgData.addData("phase",self.ui.LineEdit_phase.text())
        Comment = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict)
        old = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict)
        Comment[DlgData.id] = DlgData.data
        FreeCAD.ActiveDocument.Begin = json.dumps(Comment)
        # 返回面板中的内容是否改变
        return cmp(old, Comment) != 0
        # pha = M3DFileUtil()
        # pha.addOrUpdatePhasespaceCommands(
        # DlgData.id,
        # DlgData.getData("Horizon"),
        # DlgData.getData("Vertical"),
        # DlgData.getData("Timer2MX"),
        # DlgData.getData("Species"),
        # isThickness=DlgData.getData("Thick_Checked"),
        # direction=DlgData.getData("Thick"),
        # thickness1=DlgData.getData("Thickness_1"),
        # thickness2=DlgData.getData("Thickness_2"),
        # isSuffix=DlgData.getData("Suffix_Checked"),
        # suffix=DlgData.getData("phase")   
        # ) 
    def checkBox_thick_clicked(self):
        if self.ui.checkBox_thick.isChecked():
            self.ui.ComboBox_thick.setEnabled(True)
            self.ui.LineEdit_thick1.setEnabled(True)
            self.ui.LineEdit_thick2.setEnabled(True)
        else:
            self.ui.ComboBox_thick.setEnabled(False)
            self.ui.LineEdit_thick1.setEnabled(False)
            self.ui.LineEdit_thick2.setEnabled(False)
    def checkBox_suffix_clicked(self):
        if self.ui.checkBox_suffix.isChecked():
            self.ui.LineEdit_phase.setEnabled(True)
        else:
            self.ui.LineEdit_phase.setEnabled(False)

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
        for i in new_list:
            self.ui.ComboBox_Observation_particle.addItem(i)

     