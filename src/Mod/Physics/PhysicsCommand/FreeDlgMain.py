#-*- coding: utf-8 -*-
import FreeCAD
import Physics.PhysicsGui.FreeDlg
from PySide import QtGui
import Simulation
from DlgData import DlgData, sayz,getDlgData
import json
import BoundPalMain

from Modeling.Common.Tools import DocumentTools,ObjectsTools
import File.FileCommand.M3DFile.M3DFileUtil
import File.FileCommand.TextUI.FileTextView
from PhysicsTools import CompleterTools,SetColorTools
from Modeling.Common.CommonCommand.NewDocument import ObjectDict
from Modeling.Common.Tools.PhysicsDialog import *
import DoManager
#json格式数据需要保持原有顺序输出
from collections import OrderedDict
#json格式数据需要保持原有顺序输出
from collections import OrderedDict
flag = 0
def show(type,className,itemUserName):
    global  ObjectDict  
    if type == "new":
        ObjectDict[className] = FreeShow("new",className)
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
            ObjectDict[className] = FreeShow(className,className)
            ObjectDict[className].flagUpdateItemName = True
            ObjectDict[className].setNameUnable()
            ObjectDict[className].setModal(False)
            ObjectDict[className].show()
            ObjectDict[className].exec_()    
        

class FreeShow(PhysicsDialog):
    def __init__(self,DialogID,className,parent=None):
        PhysicsDialog.__init__(self, parent)
        self.ui = Physics.PhysicsGui.FreeDlg.Ui_Dialog_FreeDlg()
        self.ui.setupUi(self)
        #代码补全
        self.defaultValue = ["OSYS$VOLUME"]
        CompleterTools.setLineEditsCompleter(CompleterTools.getAllLineEdits(self.ui))
        self.ui.pushButton.clicked.connect(self.onCancel)
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
        self.ui.checkBox_x.clicked.connect(self.checkBox_x_clicked)
        self.ui.checkBox_y.clicked.connect(self.checkBox_y_clicked)
        self.ui.checkBox_z.clicked.connect(self.checkBox_z_clicked)
        #将吸收分量默认设为All,隐藏法相部分的控件 @lzg
        # self.ui.label.setText('吸收方向')
        # self.ui.radioButton_x.hide()
        # self.ui.radioButton_y.hide()
        # self.ui.radioButton_z.hide()
        self.ui.ComboBox_Absorption.setCurrentIndex(1)

        # FreeSpace不需要设置法相所以将这部分注释掉 
        # self.ui.radioButton_x.clicked.connect(self.onRadioBtnX)
        # self.ui.radioButton_y.clicked.connect(self.onRadioBtnY)
        # self.ui.radioButton_z.clicked.connect(self.onRadioBtnZ)


        self.ui.checkBox_vport.clicked.connect(self.checkBox_vport_clicked)

        # 刷新下拉框
        self.refreshCombox()
        # 正投影面下拉框选择事件
        self.ui.ComboBox_Shadow.currentIndexChanged.connect(self.ComboBox_Shadow_clicked)
        # 加载每个Project都具有的Comment【里面存储着对话框的所有数据】----》JSON对象----》应用于加载窗口
        JSON_CADComment = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict)  

        # self.ui.pushButton_ok.clicked.connect(lambda: self.onConfirm(JSON_CADComment,className)) 
        self.initDialog(JSON_CADComment,className)
        
        # self.onRadioBtnX()
        # self.onRadioBtnY()
        # self.onRadioBtnZ()
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
        for i in range(self.ui.ComboBox_Shadow.count()):
            ComboBox_Shadow_list.append(self.ui.ComboBox_Shadow.itemText(i))
        volumeList = DocumentTools.getActiveDocTypes("Vol_Conformal")
        volumeList.append("OSYS$VOLUME")
        for i in volumeList:
            if i not in ComboBox_Shadow_list:
                self.ui.ComboBox_Shadow.addItem(i)           

    def ComboBox_Shadow_clicked(self):
        ObjectsTools.findObjByLabelWithoutOrderAndVisible(self.ui.ComboBox_Shadow.currentText())
        if self.ui.ComboBox_Shadow.currentIndex() == 0:
            self.ui.LineEdit_start_x.setEnabled(True)
            self.ui.LineEdit_start_y.setEnabled(True)
            self.ui.LineEdit_start_z.setEnabled(True)
            self.ui.LineEdit_end_x.setEnabled(True)
            self.ui.LineEdit_end_y.setEnabled(True)
            self.ui.LineEdit_end_z.setEnabled(True)
            # 不需要法相，所以注释掉这部分 @lzg
            # if self.ui.radioButton_x.isChecked() == True:
            #     self.ui.LineEdit_end_x.setEnabled(False)
            #     self.ui.LineEdit_end_y.setEnabled(True)
            #     self.ui.LineEdit_end_z.setEnabled(True)
            # if self.ui.radioButton_y.isChecked() == True:
            #     self.ui.LineEdit_end_x.setEnabled(True)
            #     self.ui.LineEdit_end_y.setEnabled(False)
            #     self.ui.LineEdit_end_z.setEnabled(True)
            # if self.ui.radioButton_z.isChecked() == True:
            #     self.ui.LineEdit_end_x.setEnabled(True)
            #     self.ui.LineEdit_end_y.setEnabled(True)
            #     self.ui.LineEdit_end_z.setEnabled(False)
            # self.ui.radioButton_x.setEnabled(True)
            # self.ui.radioButton_y.setEnabled(True)
            # self.ui.radioButton_z.setEnabled(True)
        else:
            objName = self.ui.ComboBox_Shadow.currentText()
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
            SetColorTools.setColor(self.ui.ComboBox_Shadow.currentText(),physicsType="Free")

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

            itemData, oldData = BoundPalMain.addItem(u"吸收边界", name, className)
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

            # 吸收分量
            # self.ui.ComboBox_Absorption.setCurrentIndex(DlgData.data['Absorption_Component'])
            self.ui.ComboBox_Absorption.setCurrentIndex(self.ui.ComboBox_Absorption.findText(DlgData.data["Absorption_Component"]))
            # 相对加速比
            self.ui.checkBox_vport.setChecked(DlgData.data['VPort_Checked'])  
            self.ui.LineEdit_vport.setEnabled(DlgData.data['VPort_Checked'])
            self.ui.LineEdit_vport.setText(DlgData.data['VPort'])
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

            # 法向选择
            if DlgData.data['normal'] == "R":
                self.ui.radioButton_x.setChecked(True)
            if DlgData.data['normal'] == "theta":
                self.ui.radioButton_y.setChecked(True)
            if DlgData.data['normal'] == "Z":
                self.ui.radioButton_z.setChecked(True)
            # 正向反向选择
            if DlgData.data['direction'] == "NEGATIVE":
                self.ui.radioButton_opposite.setChecked(True)
            if DlgData.data['direction'] == "POSITIVE":
                self.ui.radioButton_forward.setChecked(True)
        except KeyError as reason:
            sayz("!!!Error:KeyError,Maybe lack of key:%s"%str(reason))              

    def keepData(self,DlgData):
        DlgData.addData("name",DlgData.id)
        DlgData.addData("Orthogonal_projection_surface",self.ui.ComboBox_Shadow.currentText())
        if self.ui.ComboBox_Shadow.currentIndex() == 0: 
            DlgData.addData("isAppointArea",False)
        else:
            # ObjectsTools.findObjByLabelWithoutOrderAndInvisible(self.ui.ComboBox_Shadow.currentText())
            DlgData.addData("isAppointArea",True)
        DlgData.addData("Dlg_Type","Free_Type")
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

        # 正向反向选择
        if self.ui.radioButton_opposite.isChecked():            
            DlgData.addData("direction","NEGATIVE")
        if self.ui.radioButton_forward.isChecked():
            DlgData.addData("direction","POSITIVE")
        # 吸收分量
        # DlgData.addData("Absorption_Component",self.ui.ComboBox_Absorption.currentIndex())
        DlgData.addData("Absorption_Component",self.ui.ComboBox_Absorption.currentText())
        # 相对加速比
        DlgData.addData("VPort_Checked",self.ui.checkBox_vport.isChecked())
        DlgData.addData("VPort",self.ui.LineEdit_vport.text())
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

    def checkBox_x_clicked(self):
        self.ui.LineEdit_DX1.setEnabled(self.ui.checkBox_x.isChecked())
    def checkBox_y_clicked(self):
        self.ui.LineEdit_DX2.setEnabled(self.ui.checkBox_y.isChecked())
    def checkBox_z_clicked(self):
        self.ui.LineEdit_DX3.setEnabled(self.ui.checkBox_z.isChecked())
    def checkBox_vport_clicked(self):
        self.ui.LineEdit_vport.setEnabled(self.ui.checkBox_vport.isChecked())

    def onRadioBtnX(self):
        if self.ui.ComboBox_Shadow.currentIndex() == 0:
            self.ui.LineEdit_end_x.setEnabled(not(self.ui.radioButton_x.isChecked()))
            self.ui.LineEdit_end_y.setEnabled(self.ui.radioButton_x.isChecked())
            self.ui.LineEdit_end_z.setEnabled(self.ui.radioButton_x.isChecked())
    def onRadioBtnY(self):
        if self.ui.ComboBox_Shadow.currentIndex() == 0:
            self.ui.LineEdit_end_x.setEnabled(self.ui.radioButton_y.isChecked())
            self.ui.LineEdit_end_y.setEnabled(not(self.ui.radioButton_y.isChecked()))
            self.ui.LineEdit_end_z.setEnabled(self.ui.radioButton_y.isChecked())
    def onRadioBtnZ(self):
        if self.ui.ComboBox_Shadow.currentIndex() == 0:
            self.ui.LineEdit_end_x.setEnabled(self.ui.radioButton_z.isChecked())
            self.ui.LineEdit_end_y.setEnabled(self.ui.radioButton_z.isChecked())
            self.ui.LineEdit_end_z.setEnabled(not(self.ui.radioButton_z.isChecked()))

    def setNameUnable(self):
        self.ui.LineEdit_Name.setEnabled(False)
