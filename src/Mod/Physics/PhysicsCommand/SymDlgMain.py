#-*- coding: utf-8 -*-

from PySide import QtGui
import Physics.PhysicsGui.SymDlg

import json
import FreeCAD
import Simulation
from DlgData import DlgData, sayz,getDlgData
from Modeling.Common.Tools import DocumentTools,ObjectsTools
import BoundPalMain
from Modeling.Common.CommonCommand.NewDocument import ObjectDict
import File.FileCommand.M3DFile.M3DFileUtil
import File.FileCommand.TextUI.FileTextView
from PhysicsTools import CompleterTools,SetColorTools
from Modeling.Common.Tools.PhysicsDialog import *
import DoManager
#json格式数据需要保持原有顺序输出
from collections import OrderedDict
flag = 0

def show(type,className,itemUserName):
    if type == "new":
        ObjectDict[className] = SymShow("new",className)
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
            ObjectDict[className] = SymShow(className,className)
            ObjectDict[className].flagUpdateItemName = True
            ObjectDict[className].setNameUnable()
            ObjectDict[className].setModal(False)
            ObjectDict[className].show()
            ObjectDict[className].exec_() 
          
class SymShow(PhysicsDialog):
    def __init__(self,DialogID,className,parent=None):
        PhysicsDialog.__init__(self, parent)
        self.ui = Physics.PhysicsGui.SymDlg.Ui_Dialog_SymDlg()
        self.ui.setupUi(self)
        #代码补全
        self.defaultValue = ["OSYS$MIDPLANE1","OSYS$MIDPLANE2","OSYS$MIDPLANE3"]
        CompleterTools.setLineEditsCompleter(CompleterTools.getAllLineEdits(self.ui))
        global flag
        flag = 0
        self.ui.radioButton_forward.setChecked(True)
        # 获取当前坐标系及坐标系单位
        coord = Simulation.getCoordinate()
        self.x = coord[0]
        self.y = coord[1]
        self.z = coord[2]
        self.x_unit = coord[3]
        self.y_unit = coord[4]
        self.z_unit = coord[5]

        #在simulation中包含了坐标信息，以此生成上述unit，但是这里额外添加的内容不受坐标系的影响，故从getDefaultUnits中另外获取
        #如不需修改，请删除下列代码块
        unit = FreeCAD.Units.getDefaultUnits()
        if unit[1]==0:
            self.angle="deg"
        else:
            self.angle="rad"

        self.ui.LineEdit_Normal.setText("0"+self.angle)


        # 根据坐标系初始化面板
        self.ui.label_X.setText(self.x)
        self.ui.label_Y.setText(self.y)
        self.ui.label_Z.setText(self.z)
        self.ui.radioButton_x.setText(self.x)
        self.ui.radioButton_y.setText(self.y)
        self.ui.radioButton_z.setText(self.z)
        self.ui.checkBox_x.setText(self.x)
        self.ui.checkBox_y.setText(self.y)
        self.ui.checkBox_z.setText(self.z)
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
        self.ui.checkBox_x.clicked.connect(self.checkBox_x_clicked)
        self.ui.checkBox_y.clicked.connect(self.checkBox_y_clicked)
        self.ui.checkBox_z.clicked.connect(self.checkBox_z_clicked)
        # 刷新下拉框
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
        self.resize(new_x, new_y)

    def refreshCombox(self):  
        '''
        每次加载窗口时都要重新加载下拉列表，以实现动态加载
        一般来说就是ComboBox_Shadow_list需要动态刷新
        '''
        ComboBox_Shadow_list=[]
        ComboBox_type_list=[]
        for i in range(self.ui.ComboBox_Shadow.count()):
            ComboBox_Shadow_list.append(self.ui.ComboBox_Shadow.itemText(i))
        for i in range(self.ui.ComboBox_type.count()):
            ComboBox_type_list.append(self.ui.ComboBox_type.itemText(i))
        Orthogonal_list = DocumentTools.getActiveDocTypes("Area_Conformal")
        Orthogonal_list.append("OSYS$MIDPLANE1")
        Orthogonal_list.append("OSYS$MIDPLANE2")
        Orthogonal_list.append("OSYS$MIDPLANE3")
        for i in Orthogonal_list:
            if i not in ComboBox_Shadow_list:
                self.ui.ComboBox_Shadow.addItem(i)
            if i not in ComboBox_type_list:
                self.ui.ComboBox_type.addItem(i)                

    def ComboBox_Shadow_clicked(self):
        ObjectsTools.findObjByLabelWithoutOrderAndVisible(self.ui.ComboBox_Shadow.currentText())
        if self.ui.ComboBox_Shadow.currentIndex() == 0:
            self.ui.ComboBox_type.setEnabled(False)
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
            self.ui.radioButton_x.setEnabled(True)
            self.ui.radioButton_y.setEnabled(True)
            self.ui.radioButton_z.setEnabled(True)
            self.ui.LineEdit_Normal.setEnabled(True)
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
            self.ui.LineEdit_start_x.setEnabled(False)
            self.ui.LineEdit_start_y.setEnabled(False)
            self.ui.LineEdit_start_z.setEnabled(False)
            self.ui.LineEdit_end_x.setEnabled(False)
            self.ui.LineEdit_end_y.setEnabled(False)
            self.ui.LineEdit_end_z.setEnabled(False)
            # 对称类型可选
            self.ui.ComboBox_type.setEnabled(True)
            # 法向周期不可编辑
            self.ui.LineEdit_Normal.setEnabled(False)
            # 法向不可编辑
            self.ui.radioButton_x.setEnabled(False)
            self.ui.radioButton_y.setEnabled(False)
            self.ui.radioButton_z.setEnabled(False)

            # 点击取消按钮关闭窗口
    def onCancel(self):
        # if self.flagUpdateItemName:
        #     JSON_CADComment = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict)
        #     oldData = DlgData(JSON_CADComment[self.userNameBefore],self.userNameBefore)
        #     self.loadData(oldData)
        self.close()

    def onConfirm(self,FreeCAD_Comment_Dict,className):
        self.close()
        #设置颜色
        objName = self.ui.ComboBox_Shadow.currentText()
        if objName in self.defaultValue:
            pass
        else:
            SetColorTools.setColor(self.ui.ComboBox_Shadow.currentText(),physicsType="Syn")
        SetColorTools.setColor(self.ui.ComboBox_type.currentText(),physicsType="Syn")


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
            itemData, oldData = BoundPalMain.addItem(u"对称边界", name, className)
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
            self.ui.ComboBox_Shadow.setCurrentIndex(self.ui.ComboBox_Shadow.findText(DlgData.data['Orthogonal_projection_surface']))
            self.ui.LineEdit_start_x.setText(DlgData.data['start_R'])
            self.ui.LineEdit_start_y.setText(DlgData.data['start_Y'])
            self.ui.LineEdit_start_z.setText(DlgData.data['start_Z'])

            self.ui.LineEdit_end_x.setText(DlgData.data['end_R'])
            self.ui.LineEdit_end_y.setText(DlgData.data['end_Y'])
            self.ui.LineEdit_end_z.setText(DlgData.data['end_Z'])
            #法向选择
            self.ui.radioButton_x.setChecked(DlgData.data["isX"])
            self.ui.radioButton_y.setChecked(DlgData.data["isY"])
            self.ui.radioButton_z.setChecked(DlgData.data["isZ"])
            #正反向选择
            self.ui.radioButton_opposite.setChecked(DlgData.data["isNegative"])
            self.ui.radioButton_forward.setChecked(DlgData.data["isPositive"])

            # 对称类型
            self.ui.ComboBox_symmetric.setCurrentIndex(self.ui.ComboBox_symmetric.findText(DlgData.data["SymmetricalType"]))
            # self.ui.ComboBox_symmetric.setCurrentIndex(DlgData.data['Symmetric_type'])
            self.ui.ComboBox_type.setCurrentIndex(self.ui.ComboBox_type.findText(DlgData.data['Symmetric_projection_surface']))
            # 法向周期
            self.ui.LineEdit_Normal.setText(DlgData.data['Normal_Period'])
            # DX编辑框
            self.ui.checkBox_x.setChecked(DlgData.data['DX_R_Checked'])  
            self.checkBox_x_clicked()
            self.ui.checkBox_y.setChecked(DlgData.data['DX_Y_Checked'])
            self.checkBox_y_clicked()
            self.ui.checkBox_z.setChecked(DlgData.data['DX_Z_Checked'])
            self.checkBox_z_clicked()
            self.ui.LineEdit_DX1.setText(DlgData.data['DX_R'])
            self.ui.LineEdit_DX2.setText(DlgData.data['DX_Y'])
            self.ui.LineEdit_DX3.setText(DlgData.data['DX_Z'])      

            # # 法向选择
            # if DlgData.data['normal'] == "R":
            #     self.ui.radioButton_x.setChecked(True)
            # if DlgData.data['normal'] == "theta":
            #     self.ui.radioButton_y.setChecked(True)
            # if DlgData.data['normal'] == "Z":
            #     self.ui.radioButton_z.setChecked(True)
            # # 正向反向选择
            # if DlgData.data['direction'] == "NEGATIVE":
            #     self.ui.radioButton_opposite.setChecked(True)
            # if DlgData.data['direction'] == "POSITIVE":
            #     self.ui.radioButton_forward.setChecked(True)
        except KeyError as reason:
            sayz("!!!Error:KeyError,Maybe lack of key:%s"%str(reason))              

    def keepData(self,DlgData):
        DlgData.addData("name",DlgData.id)
        DlgData.addData("Orthogonal_projection_surface",self.ui.ComboBox_Shadow.currentText())
        # ObjectsTools.findObjByLabelWithoutOrderAndInvisible(self.ui.ComboBox_Shadow.currentText())
        # if self.ui.ComboBox_Shadow.currentIndex() == 0: 
        #     DlgData.addData("isAppointArea",False)
        # else:
        #     DlgData.addData("isAppointArea",True)
        DlgData.addData("Dlg_Type","Sym_Type")
        DlgData.addData("start_R",self.ui.LineEdit_start_x.text())
        DlgData.addData("start_Y",self.ui.LineEdit_start_y.text())
        DlgData.addData("start_Z",self.ui.LineEdit_start_z.text())        
        DlgData.addData("end_R",self.ui.LineEdit_end_x.text())
        DlgData.addData("end_Y",self.ui.LineEdit_end_y.text())
        DlgData.addData("end_Z",self.ui.LineEdit_end_z.text())
        # 法向选择
        DlgData.addData("isX",self.ui.radioButton_x.isChecked())
        DlgData.addData("isY",self.ui.radioButton_y.isChecked())
        DlgData.addData("isZ",self.ui.radioButton_z.isChecked())
        # if self.ui.radioButton_x.isChecked():             
        #     DlgData.addData("normal","R")
        # if self.ui.radioButton_y.isChecked():             
        #     DlgData.addData("normal","theta")
        # if self.ui.radioButton_z.isChecked():             
        #     DlgData.addData("normal","Z")

        # 正向反向选择
        DlgData.addData("isNegative",self.ui.radioButton_opposite.isChecked())
        DlgData.addData("isPositive",self.ui.radioButton_forward.isChecked())
        # if self.ui.radioButton_opposite.isChecked():            
        #     DlgData.addData("direction","NEGATIVE")
        # if self.ui.radioButton_forward.isChecked():
        #     DlgData.addData("direction","POSITIVE")
        # 对称类型
        DlgData.addData("SymmetricalType",self.ui.ComboBox_symmetric.currentText())
        # DlgData.addData("Symmetric_type",self.ui.ComboBox_symmetric.currentIndex())
        # if self.ui.ComboBox_symmetric.currentIndex() == 0:
        #     DlgData.addData("Symmetric_type2MX","AXIAL")
        # if self.ui.ComboBox_symmetric.currentIndex() == 1:
        #     DlgData.addData("Symmetric_type2MX","MIRROR")
        # if self.ui.ComboBox_symmetric.currentIndex() == 2:
        #     DlgData.addData("Symmetric_type2MX","PERIODIC")                        
        DlgData.addData("Symmetric_projection_surface",self.ui.ComboBox_type.currentText())
        # ObjectsTools.findObjByLabelWithoutOrderAndInvisible(self.ui.ComboBox_type.currentText())
        # 法向周期
        DlgData.addData("Normal_Period",self.ui.LineEdit_Normal.text())
        # DX编辑框
        DlgData.addData("DX_R_Checked",self.ui.checkBox_x.isChecked())
        DlgData.addData("DX_Y_Checked",self.ui.checkBox_y.isChecked())
        DlgData.addData("DX_Z_Checked",self.ui.checkBox_z.isChecked())

        DlgData.addData("DX_R",self.ui.LineEdit_DX1.text())
        DlgData.addData("DX_Y",self.ui.LineEdit_DX2.text())
        DlgData.addData("DX_Z",self.ui.LineEdit_DX3.text())
        Comment = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict)
        old = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict)
        Comment[DlgData.id] = DlgData.data
        FreeCAD.ActiveDocument.Begin = json.dumps(Comment)
        # 返回面板中的内容是否改变
        return cmp(old, Comment) != 0
        # sym = M3DFileUtil()
        # sym.addOrUpdateSymmetryCommands(
        # DlgData.id,
        # DlgData.getData("Symmetric_type2MX"),
        # DlgData.getData("direction"),
        # isAppointArea=DlgData.getData("isAppointArea"),
        # areaName=DlgData.getData("Orthogonal_projection_surface"),
        # startPointCoordinates=[DlgData.getData("start_R"),DlgData.getData("start_Y"),DlgData.getData("start_Z")], stopPointCoordinates=[DlgData.getData("end_R"),DlgData.getData("end_Y"),DlgData.getData("end_Z")],
        # appointAreaInMid=DlgData.getData("Symmetric_type")
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

    def checkBox_x_clicked(self):
        if self.ui.checkBox_x.isChecked():
            self.ui.LineEdit_DX1.setEnabled(True)
        else:
            self.ui.LineEdit_DX1.setEnabled(False)

    def checkBox_y_clicked(self):
        if self.ui.checkBox_y.isChecked():
            self.ui.LineEdit_DX2.setEnabled(True)
        else:
            self.ui.LineEdit_DX2.setEnabled(False)

    def checkBox_z_clicked(self):
        if self.ui.checkBox_z.isChecked():
            self.ui.LineEdit_DX3.setEnabled(True)
        else:
            self.ui.LineEdit_DX3.setEnabled(False)

    def setNameUnable(self):
        self.ui.LineEdit_Name.setEnabled(False)