#-*- coding: utf-8 -*-
import json

import FreeCAD
from PySide import QtGui

import Physics.PhysicsGui.DefaultTimerDlg
from DlgData import DlgData, sayz,getDlgData
from Modeling.Common.CommonCommand.NewDocument import ObjectDict
import ObservePalMain
import File.FileCommand.M3DFile.M3DFileUtil
import File.FileCommand.TextUI.FileTextView
from PhysicsTools import CompleterTools
import DoManager
#json格式数据需要保持原有顺序输出
from collections import OrderedDict
flag = 0
def show(type,className,itemUserName):
    FreeCAD.Console.PrintMessage("####")
    FreeCAD.Console.PrintMessage(className)   
    global  ObjectDict  
    if type == "new":
        ObjectDict[className] = DefaultTimerMain("new",className)
        ObjectDict[className].setModal(False)
        ObjectDict[className].show()
        ObjectDict[className].exec_()
    elif type == "old":
        if className in ObjectDict.keys():
            # 增加了撤销操作后，数据可能发生变化，所以每次需要重新加载数据，
            JSON_CADComment = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict)
            oldData = DlgData(JSON_CADComment[itemUserName], itemUserName)
            ObjectDict[className].loadData(oldData)

            ObjectDict[className].flagUpdateItemName=True
            ObjectDict[className].setModal(False)
            ObjectDict[className].show()
            ObjectDict[className].exec_()             
        else:
            ObjectDict[className] = DefaultTimerMain(className,className)
            ObjectDict[className].setModal(False)
            ObjectDict[className].show()
            ObjectDict[className].exec_()   
        

class DefaultTimerMain(QtGui.QDialog):
    def __init__(self,DialogID,className,parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = Physics.PhysicsGui.DefaultTimerDlg.Ui_DefaultTimerDlg()
        self.ui.setupUi(self) 
        #代码补全
        CompleterTools.setLineEditsCompleter(CompleterTools.getAllLineEdits(self.ui))
        self.ui.pushButton.clicked.connect(self.onCancel)    
        global flag
        flag = 0             
        JSON_CADComment = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict)  
        self.ui.pushButton_ok.clicked.connect(lambda: self.onConfirm(JSON_CADComment,className)) 
        self.ui.typeComboBox.currentIndexChanged.connect(self.onChangedType)

        if DialogID != "new":
            oldData = DlgData(JSON_CADComment[DialogID],DialogID)
            self.loadData(oldData)            
            flag = 1  
        self.onChangedType()

        self.userNameBefore=self.ui.LineEdit_Name.text()
        self.flagUpdateItemName=False

        # 适配分辨率
        import AdaptiveDPIUtil
        new_x, new_y = AdaptiveDPIUtil.get_new_dpi(self.width(), self.height())
        self.resize(new_x, new_y)

        
    # 点击取消按钮关闭窗口
    def onCancel(self):
        # if self.flagUpdateItemName:
        #     JSON_CADComment = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict)
        #     oldData = DlgData(JSON_CADComment[self.userNameBefore],self.userNameBefore)
        #     self.loadData(oldData)
        self.close()       
    def onConfirm(self,FreeCAD_Comment_Dict,className):
        self.close()
        oldJson = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict)
        # 存储只修改数据而没有修改item名的情况
        oldData = ["modify", self.userNameBefore, className]
        itemData = ["modify", self.userNameBefore, className]

        global flag 
        count = 1
        name = self.ui.LineEdit_Name.text()            
        if flag == 0:              
            while name in FreeCAD_Comment_Dict.keys(): 
               name = self.ui.LineEdit_Name.text() + str(count) 
               count+=1       
            self.ui.LineEdit_Name.setText(name)
            itemData, oldData = ObservePalMain.addItem(u"默认定时器", name, className)
            flag = 1
                #防止修改名称使得json重复
        if self.flagUpdateItemName:
            if not name == self.userNameBefore:
                JSON_CADComment = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict)
                if self.userNameBefore in JSON_CADComment:
                    JSON_CADComment.pop(self.userNameBefore)
                    FreeCAD.ActiveDocument.Begin = json.dumps(JSON_CADComment) 
                    #更新名称
                    # if self.flagUpdateItemName:
                    itemData, oldData = ObservePalMain.updateItemName(name)
                    self.flagUpdateItemName=False
        self.userNameBefore=name

        newData = DlgData({},name)
        isModify = self.keepData(newData)

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
            self.ui.typeComboBox.setCurrentIndex(DlgData.data['Type'])
            # 定时基准 
            self.ui.radioButton_step.setChecked(DlgData.data['isByTimeSteps'])
            self.ui.radioButton_simulate.setChecked(DlgData.data['isBySimulation'])
            # if DlgData.data['Timing_reference'] == "step":
            #     self.ui.radioButton_step.setChecked(True)
            # if DlgData.data['Timing_reference'] == "simulate":
                # self.ui.radioButton_simulate.setChecked(True)
            # 起始时刻
            self.ui.LineEdit_start.setText(DlgData.data['start'])                                                
            # 结束时刻  
            self.ui.LineEdit_end.setText(DlgData.data['end'])
            # 定时周期      
            self.ui.LineEdit_period.setText(DlgData.data['period'])
            #离散时刻
            self.ui.LineEdit_Discrete_time.setText(DlgData.data['discreteTime'])
        except KeyError as reason:
            sayz("!!!Error:KeyError,Maybe lack of key:%s"%str(reason))     
    def keepData(self,DlgData):
        DlgData.addData("name",self.ui.LineEdit_Name.text())
        DlgData.addData("Type",self.ui.typeComboBox.currentIndex()) 
        DlgData.addData("Dlg_Type","DefTimer_Type")
        DlgData.addData("isByTimeSteps",self.ui.radioButton_step.isChecked())
        DlgData.addData("isBySimulation",self.ui.radioButton_simulate.isChecked())
        # if self.ui.typeComboBox.currentIndex() == 0:
        #     DlgData.addData("MXType","PERIODIC") 
        # else:
        #     DlgData.addData("MXType","DISCRETE") 
        # # 定时基准 
        # if self.ui.radioButton_step.isChecked():             
        #     DlgData.addData("Timing_reference","step")
        #     DlgData.addData("Timing_reference_MX","INTEGER")
        # if self.ui.radioButton_simulate.isChecked():             
        #     DlgData.addData("Timing_reference","simulate")
        #     DlgData.addData("Timing_reference_MX","REAL")
        # 起始时刻
        DlgData.addData("start",self.ui.LineEdit_start.text())                                                   
        # 结束时刻  
        DlgData.addData("end",self.ui.LineEdit_end.text()) 
        # 定时周期      
        DlgData.addData("period",self.ui.LineEdit_period.text())  

        DlgData.addData("discreteTime",self.ui.LineEdit_Discrete_time.text())            
        Comment = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict)
        old = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict)
        Comment[DlgData.id] = DlgData.data
        FreeCAD.ActiveDocument.Begin = json.dumps(Comment)
        # 返回面板中的内容是否改变
        return cmp(old, Comment) != 0
    def onChangedType(self):
        if self.ui.typeComboBox.currentIndex()==0:
            self.ui.LineEdit_Discrete_time.setEnabled(False)
            self.ui.LineEdit_end.setEnabled(True)
            self.ui.LineEdit_period.setEnabled(True)
            self.ui.LineEdit_start.setEnabled(True)
        if self.ui.typeComboBox.currentIndex()==1:
            self.ui.LineEdit_Discrete_time.setEnabled(True)
            self.ui.LineEdit_end.setEnabled(False)
            self.ui.LineEdit_period.setEnabled(False)
            self.ui.LineEdit_start.setEnabled(False)
    def initToDoc(self):
        JSON_CADComment = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict)  
        #初始化新建item
        global flag 
        count = 1
        name = self.ui.LineEdit_Name.text()            
        if flag == 0:              
            while name in JSON_CADComment.keys(): 
               name = self.ui.LineEdit_Name.text() + str(count) 
               count+=1       
            self.ui.LineEdit_Name.setText(name)
            ObservePalMain.addItem(u"默认定时器", name, "DefTimer")
            flag = 1
        newData = DlgData({},name)           
        self.keepData(newData)   

    

