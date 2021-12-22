#-*- coding: utf-8 -*-
import Physics.PhysicsGui.ExpDlg
from PySide import QtGui
import json
import FreeCAD
import Simulation
from DlgData import DlgData, sayz,getDlgData
from Modeling.Common.Tools import DocumentTools,ObjectsTools
import BoundPalMain
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
        ObjectDict[className] = ExpShow("new",className)
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
            ObjectDict[className].setNameUnable()
            ObjectDict[className].setModal(False)
            ObjectDict[className].show()
            ObjectDict[className].exec_()             
        else:
            ObjectDict[className] = ExpShow(itemUserName,className)
            ObjectDict[className].flagUpdateItemName = True
            ObjectDict[className].setNameUnable()
            ObjectDict[className].setModal(False)
            ObjectDict[className].show()
            ObjectDict[className].exec_()   
        
class ExpShow(PhysicsDialog):
    def __init__(self,DialogID,className,parent=None):
        PhysicsDialog.__init__(self, parent)
        self.ui = Physics.PhysicsGui.ExpDlg.Ui_Dialog_ExpDlg()
        self.ui.setupUi(self)
        #代码补全
        self.defaultValue = ["OSYS$MIDPLANE1","OSYS$MIDPLANE2","OSYS$MIDPLANE3","OSYS$VOLUME"]
        CompleterTools.setLineEditsCompleter(CompleterTools.getAllLineEdits(self.ui))
        self.ui.pushButton.clicked.connect(self.onCancel)
        self.ui.ComboBox_Shadow.currentIndexChanged.connect(self.ComboBox_Shadow_clicked)

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

        self.ui.radioButton_x.clicked.connect(self.ComboBox_Shadow_clicked)
        self.ui.radioButton_y.clicked.connect(self.ComboBox_Shadow_clicked)
        self.ui.radioButton_z.clicked.connect(self.ComboBox_Shadow_clicked)
        global flag
        flag = 0
        # 正投影面下拉框选择事件
        self.ui.ComboBox_Shadow.currentIndexChanged.connect(self.ComboBox_Shadow_clicked)
        self.ui.comboBox.currentIndexChanged.connect(self.combobox_clicked)
        # 加载每个Project都具有的Comment【里面存储着对话框的所有数据】----》JSON对象----》应用于加载窗口
        JSON_CADComment = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict)  
        # self.ui.pushButton_ok.clicked.connect(lambda: self.onConfirm(JSON_CADComment,className)) 
        self.initDialog(JSON_CADComment,className)
        if DialogID != "new":
            oldData = DlgData(JSON_CADComment[DialogID],DialogID)
            self.loadData(oldData)            
            flag = 1  
        self.ComboBox_Shadow_clicked()
        self.combobox_clicked()
        self.userNameBefore=self.ui.LineEdit_Name.text()
                #用于判断是否进行名称更新
        self.flagUpdateItemName=False

        # 适配分辨率
        import AdaptiveDPIUtil
        new_x, new_y = AdaptiveDPIUtil.get_new_dpi(self.width(), self.height())
        self.resize(new_x, new_y)

    # 点击取消按钮关闭窗口
    def onCancel(self):
        # getDlgData()
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
            itemData, oldData = BoundPalMain.addItem(u"其他模型", name, className)
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
                    itemData, oldData = BoundPalMain.updateItemName(name)
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
            self.ui.ComboBox_Shadow.setCurrentIndex(self.ui.ComboBox_Shadow.findText(DlgData.data['Current_Source']))
            self.ui.comboBox.setCurrentIndex(self.ui.comboBox.findText(DlgData.data['source_type']))
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
            # 指定电流密度
            self.ui.ComboBox_Current.setCurrentIndex(self.ui.ComboBox_Current.findText(DlgData.data['Specified_Current_Density']))
            # 函数JFUNC
            self.ui.LineEdit_JFunc.setText(DlgData.data['JFUNC'])
        except KeyError as reason:
            sayz("!!!Error:KeyError,Maybe lack of key:%s"%str(reason))              

    def keepData(self,DlgData):
        DlgData.addData("name",DlgData.id)
        DlgData.addData("Current_Source",self.ui.ComboBox_Shadow.currentText())
        DlgData.addData("source_type",self.ui.comboBox.currentText())
        DlgData.addData("Dlg_Type","ExP_Type")
        DlgData.addData("Same_Parent_Diff","ExP") 
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
        # 指定电流密度
        DlgData.addData("Specified_Current_Density",self.ui.ComboBox_Current.currentText())
        # 函数JFUNC
        DlgData.addData("JFUNC",self.ui.LineEdit_JFunc.text())
        Comment = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict)
        old = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict)
        Comment[DlgData.id] = DlgData.data
        FreeCAD.ActiveDocument.Begin = json.dumps(Comment)
        # 返回面板中的内容是否改变
        return cmp(old, Comment) != 0

    def ComboBox_Shadow_clicked(self):
        if self.ui.ComboBox_Shadow.currentIndex() == 0:
            self.addShadowItem(ObjectsTools.ObjectType.Point)
            self.ui.LineEdit_end_x.setEnabled(False)
            self.ui.LineEdit_end_y.setEnabled(False)
            self.ui.LineEdit_end_z.setEnabled(False)
        if self.ui.ComboBox_Shadow.currentIndex() == 1:
            self.addShadowItem("Line_Conformal")
            self.ui.LineEdit_end_x.setEnabled(self.ui.radioButton_x.isChecked())
            self.ui.LineEdit_end_y.setEnabled(self.ui.radioButton_y.isChecked())
            self.ui.LineEdit_end_z.setEnabled(self.ui.radioButton_z.isChecked())
        if self.ui.ComboBox_Shadow.currentIndex() == 2:
            self.addShadowItem("Area_Conformal")
            self.ui.LineEdit_end_x.setEnabled(not self.ui.radioButton_x.isChecked())
            self.ui.LineEdit_end_y.setEnabled(not self.ui.radioButton_y.isChecked())
            self.ui.LineEdit_end_z.setEnabled(not self.ui.radioButton_z.isChecked())
        if self.ui.ComboBox_Shadow.currentIndex() == 3:
            self.addShadowItem("Vol_Conformal")
            self.ui.LineEdit_end_x.setEnabled(True)
            self.ui.LineEdit_end_y.setEnabled(True)
            self.ui.LineEdit_end_z.setEnabled(True)
    # ComboBox根据ComboBox_Shadow添加选项
    def addShadowItem(self, type):

        # 显示观测类型
        # if self.ui.groupBox_Port.isHidden():
        #     self.ui.groupBox_Port.setGeometry(QtCore.QRect(10, 60, 401, 181))
        #     self.ui.groupBox_Port_2.setGeometry(QtCore.QRect(10, 250, 401, 241))
        #     self.ui.groupBox_2.setGeometry(QtCore.QRect(10, 500, 401, 101))
        #     self.ui.groupBox_Port.show()
        # 添加前清空所有选项
        self.ui.comboBox.clear()
        self.ui.comboBox.addItem(u"未指定")
        Orthogonal_list = DocumentTools.getActiveDocTypes(type)
        if type == "Area_Conformal":
            Orthogonal_list.append("OSYS$MIDPLANE1")
            Orthogonal_list.append("OSYS$MIDPLANE2")
            Orthogonal_list.append("OSYS$MIDPLANE3")
        if type == "Vol_Conformal":
            # 此处不需要为导体，任意类型都可被选择为时间观测体 @lizgenguang start
            Orthogonal_list = DocumentTools.getActiveDocTypes(type, False)
            Orthogonal_list.append("OSYS$VOLUME")
            # @lizgenguang end
        for i in Orthogonal_list:
            self.ui.comboBox.addItem(i)
    def combobox_clicked(self):
        self.ui.radioButton_x.setEnabled(False)
        self.ui.radioButton_y.setEnabled(False)
        self.ui.radioButton_z.setEnabled(False)
        if self.ui.ComboBox_Shadow.currentIndex() == 0:
            objName = self.ui.comboBox.currentText()
            if objName == '未指定':
                self.ui.LineEdit_start_x.setEnabled(True)
                self.ui.LineEdit_start_y.setEnabled(True)
                self.ui.LineEdit_start_z.setEnabled(True)
                self.ui.LineEdit_end_x.setEnabled(False)
                self.ui.LineEdit_end_y.setEnabled(False)
                self.ui.LineEdit_end_z.setEnabled(False)
                # 法向不可选
                self.ui.radioButton_x.setEnabled(False)
                self.ui.radioButton_y.setEnabled(False)
                self.ui.radioButton_z.setEnabled(False)
            else:
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
        elif self.ui.ComboBox_Shadow.currentIndex() == 1:
            objName = self.ui.comboBox.currentText()
            if objName == '未指定':
                self.ui.LineEdit_start_x.setEnabled(True)
                self.ui.LineEdit_start_y.setEnabled(True)
                self.ui.LineEdit_start_z.setEnabled(True)
                self.ui.LineEdit_end_x.setEnabled(self.ui.radioButton_x.isChecked())
                self.ui.LineEdit_end_y.setEnabled(self.ui.radioButton_y.isChecked())
                self.ui.LineEdit_end_z.setEnabled(self.ui.radioButton_z.isChecked())
                # 法向不可选
                self.ui.radioButton_x.setEnabled(True)
                self.ui.radioButton_y.setEnabled(True)
                self.ui.radioButton_z.setEnabled(True)
            else:
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
        elif self.ui.ComboBox_Shadow.currentIndex() == 2:
            objName = self.ui.comboBox.currentText()
            if objName == '未指定':
                self.ui.LineEdit_start_x.setEnabled(True)
                self.ui.LineEdit_start_y.setEnabled(True)
                self.ui.LineEdit_start_z.setEnabled(True)
                self.ui.LineEdit_end_x.setEnabled(self.ui.radioButton_x.isChecked())
                self.ui.LineEdit_end_y.setEnabled(self.ui.radioButton_y.isChecked())
                self.ui.LineEdit_end_z.setEnabled(self.ui.radioButton_z.isChecked())
                # 法向不可选
                self.ui.radioButton_x.setEnabled(True)
                self.ui.radioButton_y.setEnabled(True)
                self.ui.radioButton_z.setEnabled(True)
            else:
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
        elif self.ui.ComboBox_Shadow.currentIndex() == 3:
            objName = self.ui.comboBox.currentText()
            if objName == '未指定':
                self.ui.LineEdit_start_x.setEnabled(True)
                self.ui.LineEdit_start_y.setEnabled(True)
                self.ui.LineEdit_start_z.setEnabled(True)
                self.ui.LineEdit_end_x.setEnabled(True)
                self.ui.LineEdit_end_y.setEnabled(True)
                self.ui.LineEdit_end_z.setEnabled(True)
                # 法向不可选
                self.ui.radioButton_x.setEnabled(False)
                self.ui.radioButton_y.setEnabled(False)
                self.ui.radioButton_z.setEnabled(False)
            else:
                if objName in self.defaultValue:
                    pass
                else:
                    modelData = DocumentTools.getValueOfVolComformalObjByLable(objName)
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
                # 法向不可选
                self.ui.radioButton_x.setEnabled(False)
                self.ui.radioButton_y.setEnabled(False)
                self.ui.radioButton_z.setEnabled(False)
                self.ui.radioButton_x.setChecked(False)
                self.ui.radioButton_y.setChecked(False)
                self.ui.radioButton_z.setChecked(False)
        pass

    def setNameUnable(self):
        self.ui.LineEdit_Name.setEnabled(False)

