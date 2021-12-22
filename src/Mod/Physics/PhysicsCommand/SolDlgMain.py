#-*- coding: utf-8 -*-
import Physics.PhysicsGui.SolDlg
from PySide import QtGui
import json
import FreeCAD
import Simulation
from DlgData import DlgData, sayz,getDlgData
from Modeling.Common.Tools import DocumentTools
import BoundPalMain
from Modeling.Common.CommonCommand.NewDocument import ObjectDict
from PhysicsTools import CompleterTools
from Modeling.Common.Tools.PhysicsDialog import *
import DoManager
#json格式数据需要保持原有顺序输出
from collections import OrderedDict
flag = 0

def show(type,className,itemUserName):
    if type == "new":
        ObjectDict[className] = SolShow("new",className)
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
            ObjectDict[className] = SolShow(className,className)
            ObjectDict[className].flagUpdateItemName = True
            ObjectDict[className].setNameUnable()
            ObjectDict[className].setModal(False)
            ObjectDict[className].show()
            ObjectDict[className].exec_()  
        
class SolShow(PhysicsDialog):
    def __init__(self,DialogID,className,parent=None):
        PhysicsDialog.__init__(self, parent)
        self.ui = Physics.PhysicsGui.SolDlg.Ui_Dialog_SolDlg()
        self.ui.setupUi(self)
        #代码补全
        CompleterTools.setLineEditsCompleter(CompleterTools.getAllLineEdits(self.ui))
        self.ui.pushButton.clicked.connect(self.onCancel)
        global flag
        flag = 0
        self.ui.ComboBox_uniformParam.currentIndexChanged.connect(self.ComboBox_uniformParam_clicked)
        self.ui.horizontalSlider.valueChanged.connect(self.horizontalSlider_valueChanged)

        self.ui.checkBox_x.clicked.connect(self.checkBox_x_clicked)
        self.ui.checkBox_y.clicked.connect(self.checkBox_y_clicked)
        self.ui.checkBox_z.clicked.connect(self.checkBox_z_clicked)

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

        #加入内外半径随默认单位的变化
        unit = FreeCAD.Units.getDefaultUnits()
        if unit[0]==0:
            self.ui.LineEdit_radiusIn.setText("1mm")
            self.ui.LineEdit_radiusOut.setText("1mm")
        elif unit[0]==1:
            self.ui.LineEdit_radiusIn.setText("0.1cm")
            self.ui.LineEdit_radiusOut.setText("0.1cm")
        else:
            self.ui.LineEdit_radiusIn.setText("0.001m")
            self.ui.LineEdit_radiusOut.setText("0.001m")


    # 点击取消按钮关闭窗口
    def onCancel(self):
        # getDlgData()
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
        # FreeCAD.Console.PrintError('213123123123123123123123')
        FileStr = fileUtil.getLatestM3DFileStr()
        # 进行文本的更新
        File.FileCommand.TextUI.FileTextView.FileView().updateText(FileStr)
        
    def loadData(self,DlgData): 
        try:      
            self.ui.LineEdit_Name.setText(DlgData.data['name'])
            # 设置标记的旧名字
            self.userNameBefore = DlgData.data['name']
            # Z中心
            self.ui.LineEdit_CenterZ.setText(DlgData.data['Center_Z'])
            # R中心
            self.ui.LineEdit_CenterR.setText(DlgData.data['Center_R'])
            # 线圈半长
            self.ui.LineEdit_halfRadius.setText(DlgData.data['Half_Circle'])
            # 内半径
            self.ui.LineEdit_radiusIn.setText(DlgData.data['Radius_In'])
            # 外半径
            self.ui.LineEdit_radiusOut.setText(DlgData.data['Radius_Out'])
            # 线圈匝数
            self.ui.LineEdit_num.setText(DlgData.data['Turns'])
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
            # 材料设置
            self.ui.ComboBox_material.setCurrentIndex(self.ui.ComboBox_material.findText(DlgData.data['Material']))
            # 模型颜色

            # 透明度
            
            # 匀场因子
            self.ui.ComboBox_uniformParam.setCurrentIndex(self.ui.ComboBox_uniformParam.findText(DlgData.data['Shimming_Factor']))
            # R因子
            self.ui.LineEdit_Rparam.setText(DlgData.data['Factor_R'])
            # Z因子
            self.ui.LineEdit_Zparam.setText(DlgData.data['Factor_Z'])
            # 占空比
            self.ui.LineEdit_duty.setText(DlgData.data['Duty'])
            # 内半径
            self.ui.LineEdit_RadiusIn.setText(DlgData.data['_RADIUSIN'])
            # 外半径
            self.ui.LineEdit_RadiusOut.setText(DlgData.data['_RADIUSOUT'])
            # 磁导率
            self.ui.LineEdit_Permeability.setText(DlgData.data['Permeability'])
            # 线圈电流
            self.ui.LineEdit_current.setText(DlgData.data['Coil_Current'])
            # theta角度
            self.ui.LineEdit_theta.setText(DlgData.data['THETA'])
            # phi角度    
            self.ui.LineEdit_phi.setText(DlgData.data['PHI'])  
        except KeyError as reason:
            sayz("!!!Error:KeyError,Maybe lack of key:%s"%str(reason))              

    def keepData(self,DlgData):
        DlgData.addData("name",DlgData.id)
        DlgData.addData("Dlg_Type","Sol_Type")
        DlgData.addData("Same_Parent_Diff","Sol") 
        # Z中心
        DlgData.addData("Center_Z",self.ui.LineEdit_CenterZ.text())
        # R中心
        DlgData.addData("Center_R",self.ui.LineEdit_CenterR.text())
        # 线圈半长
        DlgData.addData("Half_Circle",self.ui.LineEdit_halfRadius.text())
        # 内半径
        DlgData.addData("Radius_In",self.ui.LineEdit_radiusIn.text())
        # 外半径
        DlgData.addData("Radius_Out",self.ui.LineEdit_radiusOut.text())
        # 线圈匝数
        DlgData.addData("Turns",self.ui.LineEdit_num.text())
        # DX编辑框
        DlgData.addData("DX_R_Checked",self.ui.checkBox_x.isChecked())
        DlgData.addData("DX_Y_Checked",self.ui.checkBox_y.isChecked())
        DlgData.addData("DX_Z_Checked",self.ui.checkBox_z.isChecked())

        DlgData.addData("DX_R",self.ui.LineEdit_DX1.text())
        DlgData.addData("DX_Y",self.ui.LineEdit_DX2.text())
        DlgData.addData("DX_Z",self.ui.LineEdit_DX3.text())        
        # 材料设置
        DlgData.addData("Material",self.ui.ComboBox_material.currentText())
        # 模型颜色

        # 透明度

        # 匀场因子
        DlgData.addData("Shimming_Factor",self.ui.ComboBox_uniformParam.currentText())
        if self.ui.ComboBox_uniformParam.currentText() == "None":
            DlgData.addData("Shimming_Factor", "none")
        elif self.ui.ComboBox_uniformParam.currentText() == "RZ因子":
            DlgData.addData("Shimming_Factor", "rz")
        else:
            DlgData.addData("Shimming_Factor", "other")
        # R因子
        DlgData.addData("Factor_R",self.ui.LineEdit_Rparam.text())
        # Z因子
        DlgData.addData("Factor_Z",self.ui.LineEdit_Zparam.text())
        # 占空比
        DlgData.addData("Duty",self.ui.LineEdit_duty.text())
        # 内半径
        DlgData.addData("_RADIUSIN",self.ui.LineEdit_RadiusIn.text())
        # 外半径
        DlgData.addData("_RADIUSOUT",self.ui.LineEdit_RadiusOut.text())
        # 磁导率
        DlgData.addData("Permeability",self.ui.LineEdit_Permeability.text())
        # 线圈电流
        DlgData.addData("Coil_Current",self.ui.LineEdit_current.text())
        # theta角度
        DlgData.addData("THETA",self.ui.LineEdit_theta.text())
        # phi角度    
        DlgData.addData("PHI",self.ui.LineEdit_phi.text())    


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
    def ComboBox_uniformParam_clicked(self):
        if self.ui.ComboBox_uniformParam.currentIndex() == 1:
            self.ui.LineEdit_Rparam.setEnabled(True)
            self.ui.LineEdit_Zparam.setEnabled(True)
            self.ui.LineEdit_duty.setEnabled(False)
            self.ui.LineEdit_RadiusIn.setEnabled(False)
            self.ui.LineEdit_RadiusOut.setEnabled(False)
            self.ui.LineEdit_Permeability.setEnabled(False)
        if self.ui.ComboBox_uniformParam.currentIndex() == 2:
            self.ui.LineEdit_Rparam.setEnabled(False)
            self.ui.LineEdit_Zparam.setEnabled(False)
            self.ui.LineEdit_duty.setEnabled(True)
            self.ui.LineEdit_RadiusIn.setEnabled(True)
            self.ui.LineEdit_RadiusOut.setEnabled(True)
            self.ui.LineEdit_Permeability.setEnabled(True)
    def horizontalSlider_valueChanged(self):
        pass
        # if self.ui.horizontalSlider.valueChanged():
        #     self.ui.LineEdit_transparency.setText(True)
        # else:
        #     self.ui.LineEdit_transparency.setEnabled(False)

    def setNameUnable(self):
        self.ui.LineEdit_Name.setEnabled(False)

