#-*- coding: utf-8 -*-
import SymtryDialog
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
        self.ui = SymtryDialog.Ui_Dialog_SymDlg()
        self.ui.setupUi(self)
        self.obj = obj
        self.initDialog()
        self.loadData()

    def initDialog(self):
        try:
            #代码补全
            self.defaultValue = ["OSYS$MIDPLANE1","OSYS$MIDPLANE2","OSYS$MIDPLANE3"]
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

            # 关闭Z轴设置
            self.ui.label_Z.hide()
            self.ui.radioButton_z.hide()
            self.ui.checkBox_z.hide()
            self.ui.LineEdit_start_z.hide()
            self.ui.LineEdit_end_z.hide()
            self.ui.LineEdit_DX3.hide()

            self.ui.LineEdit_start_x.textChanged.connect(self.LineEdit_start_x_textChanged)
            self.ui.LineEdit_start_y.textChanged.connect(self.LineEdit_start_y_textChanged)
            self.ui.LineEdit_start_z.textChanged.connect(self.LineEdit_start_z_textChanged)

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
            self.ui.ComboBox_Shadow.setCurrentIndex(self.ui.ComboBox_Shadow.findText(str(self.obj.orthogonalProjectionPlane)))
            self.ui.LineEdit_start_x.setText(self.obj.point1_X)
            self.ui.LineEdit_start_y.setText(self.obj.point1_Y)

            self.ui.LineEdit_end_x.setText(self.obj.point2_X)
            self.ui.LineEdit_end_y.setText(self.obj.point2_Y)
            # 法向选择
            self.ui.radioButton_x.setChecked(self.obj.isCheckNormal1)
            self.ui.radioButton_y.setChecked(self.obj.isCheckNormal2)
            # 正向反向选择
            if self.obj.isNegative == True:
                self.ui.radioButton_opposite.setChecked(True)
            if self.obj.isPositive == True:
                self.ui.radioButton_forward.setChecked(True)

            # 对称类型
            self.ui.ComboBox_symmetric.setCurrentIndex(self.ui.ComboBox_symmetric.findText(str(self.obj.symmetricalType)))
            # self.ui.ComboBox_symmetric.setCurrentIndex(DlgData.data['Symmetric_type'])
            self.ui.ComboBox_type.setCurrentIndex(self.ui.ComboBox_type.findText(str(self.obj.assignType)))
            # 法向周期
            self.ui.LineEdit_Normal.setText(self.obj.theNormalCycle)
            # DX编辑框
            self.ui.checkBox_x.setChecked(self.obj.isMarkX)  
            self.checkBox_x_clicked()
            self.ui.checkBox_y.setChecked(self.obj.isMarkY)
            self.checkBox_y_clicked()
            self.ui.LineEdit_DX1.setText(self.obj.MarkX)
            self.ui.LineEdit_DX2.setText(self.obj.MarkY)    

        except KeyError as reason:
            sayz("!!!Error:KeyError,Maybe lack of key:%s"%str(reason))              

    def keepData(self):
        try:
            self.obj.orthogonalProjectionPlane = self.ui.ComboBox_Shadow.currentText()
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
            # 对称类型
            self.obj.symmetricalType = self.ui.ComboBox_symmetric.currentText()                     
            self.obj.assignType = self.ui.ComboBox_type.currentText()
            # 法向周期
            self.obj.theNormalCycle = self.ui.LineEdit_Normal.text()
            # DX编辑框
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
            