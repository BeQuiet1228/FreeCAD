#-*- coding: utf-8 -*-
import FreeDialog
from PySide import QtGui
import FreeCAD
from Physics.PhysicsCommand import Simulation
from Physics.PhysicsCommand.DlgData import sayz
from Modeling.Common.Tools import DocumentTools,ObjectsTools
from Physics.PhysicsTools import CompleterTools
from Modeling.Modeling2D.Tools import Tools2D

class ShowDialog(QtGui.QDialog):
    def __init__(self,obj,parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = FreeDialog.Ui_Dialog_FreeDlg()
        self.ui.setupUi(self)
        self.obj = obj
        self.initDialog()
        self.loadData()

    def initDialog(self):
        try:
            #代码补全
            self.defaultValue = ["OSYS$VOLUME"]
            # 这段代码暂时注释
            # CompleterTools.setLineEditsCompleter(CompleterTools.getAllLineEdits(self.ui))
            self.ui.pb_cancel.clicked.connect(self.onCancel)
            self.ui.pb_ok.clicked.connect(self.onConfirm)
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
            self.ui.ComboBox_Absorption.setCurrentIndex(1)
            self.ui.checkBox_vport.clicked.connect(self.checkBox_vport_clicked)


            # 关闭Z轴设置
            self.ui.label_Z.hide()
            self.ui.radioButton_z.hide()
            self.ui.checkBox_z.hide()
            self.ui.LineEdit_start_z.hide()
            self.ui.LineEdit_end_z.hide()
            self.ui.LineEdit_DX3.hide()

            self.ui.radioButton_x.clicked.connect(self.onRadioBtnX)
            self.ui.radioButton_y.clicked.connect(self.onRadioBtnY)

            # 刷新下拉框
            self.refreshCombox()
            # 正投影面下拉框选择事件
            self.ui.ComboBox_Shadow.currentIndexChanged.connect(self.ComboBox_Shadow_clicked)

            self.userNameBefore=self.ui.LineEdit_Name.text()
            #用于判断是否进行名称更新
            self.flagUpdateItemName=False
            self.ComboBox_Shadow_clicked()
            # 适配分辨率
            from Physics.PhysicsCommand import AdaptiveDPIUtil
            new_x, new_y = AdaptiveDPIUtil.get_new_dpi(self.width(), self.height())
            self.resize(new_x, new_y)

        except:
            import traceback
            sayz("error:" + traceback.format_exc())

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
        self.close()

    # 点击确定按钮
    def onConfirm(self):
        self.keepData()
        self.close()
   
    def loadData(self): 
        try:      
            self.ui.LineEdit_Name.setText(self.obj.Name)
            # 设置标记的旧名字
            self.userNameBefore = self.obj.Name
            self.ui.ComboBox_Shadow.setCurrentIndex(self.ui.ComboBox_Shadow.findText(self.obj.orthogonalProjectionPlane))
            self.ui.LineEdit_start_x.setText(self.obj.point1_X)
            self.ui.LineEdit_start_y.setText(self.obj.point1_Y)

            self.ui.LineEdit_end_x.setText(self.obj.point2_X)
            self.ui.LineEdit_end_y.setText(self.obj.point2_Y)

            # 吸收分量
            # self.ui.ComboBox_Absorption.setCurrentIndex(DlgData.data['Absorption_Component'])
            self.ui.ComboBox_Absorption.setCurrentIndex(self.ui.ComboBox_Absorption.findText(self.obj.absorb))
            # 自定义传导率
            self.ui.checkBox_vport.setChecked(self.obj.isCustomConductivity)  
            self.ui.LineEdit_vport.setEnabled(self.obj.isCustomConductivity)
            self.ui.LineEdit_vport.setText(self.obj.customConductivity)
            # DX编辑框
            self.ui.checkBox_x.setChecked(self.obj.isMarkX)  
            self.checkBox_x_clicked()
            self.ui.checkBox_y.setChecked(self.obj.isMarkY)
            self.checkBox_y_clicked()
            self.ui.LineEdit_DX1.setText(self.obj.MarkX)
            self.ui.LineEdit_DX2.setText(self.obj.MarkY)

            # 法向选择
            self.ui.radioButton_x.setChecked(self.obj.isCheckNormal1)
            self.ui.radioButton_y.setChecked(self.obj.isCheckNormal2)
            # 正向反向选择
            if self.obj.isNegative == True:
                self.ui.radioButton_opposite.setChecked(True)
            if self.obj.isPositive == True:
                self.ui.radioButton_forward.setChecked(True)

        except KeyError as reason:
            sayz("!!!Error:KeyError,Maybe lack of key:%s"%str(reason))              

    def keepData(self):
        try:
            self.obj.orthogonalProjectionPlane = self.ui.ComboBox_Shadow.currentText()
            # if self.ui.ComboBox_Shadow.currentIndex() == 0: 
            #     DlgData.addData("isAppointArea",False)
            # else:
            #     # ObjectsTools.findObjByLabelWithoutOrderAndInvisible(self.ui.ComboBox_Shadow.currentText())
            #     DlgData.addData("isAppointArea",True)
            # DlgData.addData("Dlg_Type","Free_Type")
            self.obj.point1_X = self.ui.LineEdit_start_x.text()
            self.obj.point1_Y = self.ui.LineEdit_start_y.text()
            self.obj.point2_X = self.ui.LineEdit_end_x.text()
            self.obj.point2_Y = self.ui.LineEdit_end_y.text()
            # 法向选择
            self.obj.isCheckNormal1 = self.ui.radioButton_x.isChecked()    
            self.obj.isCheckNormal2 = not(self.obj.isCheckNormal1)     

            # 正向反向选择
            self.obj.isNegative = self.ui.radioButton_opposite.isChecked()           
            self.obj.isPositive = self.ui.radioButton_forward.isChecked()
            # 吸收分量
            # DlgData.addData("Absorption_Component",self.ui.ComboBox_Absorption.currentIndex())
            self.obj.absorb = self.ui.ComboBox_Absorption.currentText()
            # 自定义传导率
            self.obj.isCustomConductivity = self.ui.checkBox_vport.isChecked()
            self.obj.customConductivity = self.ui.LineEdit_vport.text()
            # DX编辑框
            self.obj.isMarkX = self.ui.checkBox_x.isChecked()
            self.obj.isMarkY = self.ui.checkBox_y.isChecked()

            self.obj.MarkX = self.ui.LineEdit_DX1.text()
            self.obj.MarkX = self.ui.LineEdit_DX2.text()
            # 返回面板中的内容是否改变
            return cmp(old, Comment) != 0

        except:
            import traceback
            sayz("error:" + traceback.format_exc())
        pass

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

           
