# -*- coding: utf-8 -*-
import FoilDialog
from PySide import QtGui
from Modeling.Modeling2D.Tools import Tools2D
from Modeling.Modeling2D.Modeling2DCommand.BaseUI import BaseDialog


def getNewMaterical():
    NewMaterical_list = Tools2D.getSpecificTypePhyAndProObjects(u"NewMaterial")
    NewMatericalName_list = []
    for ele in NewMaterical_list:
        NewMatericalName_list.append(ele.Label)
    return NewMatericalName_list

         
class ShowDialog(BaseDialog.BaseOtherDialog):
    def __init__(self, obj, isNew=False, parent=None):
        BaseDialog.BaseOtherDialog.__init__(self, obj, isNew, parent)
        self.setModal(False)

    def setUI(self):
        """
        设置ui
        """
        self.ui = FoilDialog.Ui_Dialog_FoilDlg()
        self.ui.setupUi(self)

    def helperInitDialog(self):
        self.defaultValue = []
        # 连接信号与槽
        self.ui.DefaultMaterial.clicked.connect(self.DefaultMaterial_clicked)
        self.ui.CustomMaterial.clicked.connect(self.CustomMaterial_clicked)
        # 法相按钮绑定信号与槽
        self.ui.radioButton_x.clicked.connect(self.setRadioButton)
        self.ui.radioButton_y.clicked.connect(self.setRadioButton)
        self.ui.LineEdit_start_x.textChanged.connect(self.setRadioButton)
        self.ui.LineEdit_start_y.textChanged.connect(self.setRadioButton)
        # 正投影面下拉框选择事件
        self.ui.ComboBox_Shadow.currentIndexChanged.connect(self.ComboBox_Shadow_clicked)
        # 获取当前坐标系及坐标系单位
        coord = Tools2D.getCoordinate()
        self.x = coord[0]
        self.y = coord[1]
        # self.z = coord[2]
        # self.x_unit = coord[3]
        # self.y_unit = coord[4]
        # self.z_unit = coord[5]
        # # 箔片厚度是不受坐标系单位影响的量，如果不需要修改请删除下列代码块
        # unit = FreeCAD.Units.getDefaultUnits()
        # if unit[0] == 0:
        #     self.ui.LineEdit_thick.setText("1mm")
        # elif unit[0] == 1:
        #     self.ui.LineEdit_thick.setText("0.1cm")
        # else:
        #     self.ui.LineEdit_thick.setText("0.001m")
        # 根据坐标系初始化面板
        self.ui.label_X.setText(self.x)
        self.ui.label_Y.setText(self.y)
        self.ui.radioButton_x.setText(self.x)
        self.ui.radioButton_y.setText(self.y)
        # 刷新下拉框
        self.refreshCombox()
        # 加载数据
        self.loadData()

    def helperOK(self):
        self.isKeepData = True
        self.close()

    def helperCancel(self):
        self.isKeepData = False
        self.close()

    def refreshCombox(self):
        """
        每次加载窗口时都要重新加载下拉列表，以实现动态加载
        一般来说就是ComboBox_Shadow_list需要动态刷新
        """
        try:
            ComboBox_Shadow_list=[]
            for i in range(self.ui.ComboBox_Shadow.count()):
                ComboBox_Shadow_list.append(self.ui.ComboBox_Shadow.itemText(i))
            volumeList = Tools2D.getAllConformalLineLabel()
            for i in volumeList:
                if i not in ComboBox_Shadow_list:
                    self.ui.ComboBox_Shadow.addItem(i)     

            ComboBox_Material_list = []
            for i in range(self.ui.ComboBox_Material.count()):
                ComboBox_Material_list.append(self.ui.ComboBox_Material.itemText(i))
            Custom_Material_list = getNewMaterical()
            for i in Custom_Material_list:
                if i not in ComboBox_Material_list:
                    self.ui.ComboBox_Material.addItem(i)
        except:
            import traceback
            Tools2D.sayz("error:" + traceback.format_exc())

    def ComboBox_Shadow_clicked(self):
        try:
            if self.ui.ComboBox_Shadow.currentIndex() == 0:
                self.ui.LineEdit_start_x.setEnabled(True)
                self.ui.LineEdit_start_y.setEnabled(True)
                self.ui.LineEdit_end_x.setEnabled(True)
                self.ui.LineEdit_end_y.setEnabled(True)
                self.ui.radioButton_x.setEnabled(True)
                self.ui.radioButton_y.setEnabled(True)
                self.setRadioButton()
            else:
                objName = self.ui.ComboBox_Shadow.currentText()
                if objName in self.defaultValue:
                    pass
                else:
                    modelData = Tools2D.getValueOfAreaObjByLabel(objName)
                    self.ui.LineEdit_start_x.setText(modelData["point1.x"])
                    self.ui.LineEdit_start_y.setText(modelData["point1.y"])
                    self.ui.LineEdit_end_x.setText(modelData["point2.x"])
                    self.ui.LineEdit_end_y.setText(modelData["point2.y"])
                    # 法向
                    if modelData["normal"] == "X" or modelData["normal"] == "x":
                        self.ui.radioButton_x.setChecked(True)
                    elif modelData["normal"] == "Y" or modelData["normal"] == "y":
                        self.ui.radioButton_y.setChecked(True)
                    else:
                        Tools2D.sayz("get Area_Conformal error")
                self.ui.LineEdit_start_x.setEnabled(False)
                self.ui.LineEdit_start_y.setEnabled(False)
                self.ui.LineEdit_end_x.setEnabled(False)
                self.ui.LineEdit_end_y.setEnabled(False)
                self.ui.radioButton_x.setEnabled(False)
                self.ui.radioButton_y.setEnabled(False)
        except:
            import traceback
            Tools2D.sayz("error:" + traceback.format_exc())

    def loadData(self):
        self.refreshCombox()
        # 名称
        self.ui.LineEdit_Name.setText(self.obj.Label)
        # 下拉框
        self.ui.ComboBox_Shadow.setCurrentIndex(self.ui.ComboBox_Shadow.findText(str(self.obj.foilType)))
        # 坐标
        self.ui.LineEdit_start_x.setText(self.obj.point1_X)
        self.ui.LineEdit_start_y.setText(self.obj.point1_Y)
        self.ui.LineEdit_end_x.setText(self.obj.point2_X)
        self.ui.LineEdit_end_y.setText(self.obj.point2_Y)
        # 法向
        if self.obj.isCheckNormal1:
            self.ui.radioButton_x.setChecked(True)
        if self.obj.isCheckNormal2:
            self.ui.radioButton_y.setChecked(True)
        self.setRadioButton()
        # # 正反
        # if self.obj.isPositive:
        #     self.ui.radioButton_forward.setChecked(True)
        # else:
        #     self.ui.radioButton_opposite.setChecked(True)
        # 铂片厚度
        self.ui.LineEdit_thick.setText(self.obj.foilThickness)
        # 材料名称
        self.ui.CustomMaterial.setChecked(self.obj.isCheckCustom)
        self.ui.ComboBox_Material.setCurrentIndex(self.ui.ComboBox_Material.findText(str(self.obj.customMaterial)))
        self.ui.DefaultMaterial.setChecked(not self.obj.isCheckCustom)
        self.ui.Gold.setText(self.obj.defaultMaterial)
        # 如果选中了物体，那么重新读取一次物体的数据
        self.ComboBox_Shadow_clicked()
        self.ui.ComboBox_Material.setEnabled(self.ui.CustomMaterial.isChecked())
        self.ui.Gold.setEnabled(self.ui.DefaultMaterial.isChecked())

    def keepData(self):
        """
        设置对话框信息到obj
        """
        # 名字
        Tools2D.setLabelToObj(self.obj, self.ui.LineEdit_Name.text())
        # 泊片类型
        self.obj.foilType = self.ui.ComboBox_Shadow.currentText()
        # 坐标
        self.obj.point1_X = self.ui.LineEdit_start_x.text()
        self.obj.point1_Y = self.ui.LineEdit_start_y.text()
        self.obj.point2_X = self.ui.LineEdit_end_x.text()
        self.obj.point2_Y = self.ui.LineEdit_end_y.text()
        # 法相
        self.obj.isCheckNormal1 = self.ui.radioButton_x.isChecked()
        self.obj.isCheckNormal2 = self.ui.radioButton_y.isChecked()
        # # 正反
        # self.obj.isNegative = self.ui.radioButton_opposite.isChecked()
        # self.obj.isPositive = self.ui.radioButton_forward.isChecked()
        # 铂片厚度
        self.obj.foilThickness = self.ui.LineEdit_thick.text()
        # 材料名称
        self.obj.isCheckCustom = self.ui.CustomMaterial.isChecked()
        self.obj.customMaterial = self.ui.ComboBox_Material.currentText()
        self.obj.isCheckDefault = not self.obj.isCheckCustom
        self.obj.defaultMaterial = self.ui.Gold.text()

    def CustomMaterial_clicked(self):
        if self.ui.CustomMaterial.isChecked():
            self.ui.ComboBox_Material.setEnabled(self.ui.CustomMaterial.isChecked())
            self.ui.Gold.setEnabled(self.ui.DefaultMaterial.isChecked())
        else:
            self.ui.ComboBox_Material.setEnabled(False)

    def DefaultMaterial_clicked(self):
        if self.ui.DefaultMaterial.isChecked():
            self.ui.Gold.setEnabled(True)
            self.ui.ComboBox_Material.setEnabled(False)
        else:
            self.ui.Gold.setEnabled(False)

    def setRadioButton(self):
        """
        根据radioButton的状态设置界面信息
        """
        if self.ui.radioButton_x.isChecked():
            self.ui.LineEdit_end_x.setEnabled(False)
            self.ui.LineEdit_end_x.setText(self.ui.LineEdit_start_x.text())
            self.ui.LineEdit_end_y.setEnabled(True)
        else:
            self.ui.LineEdit_end_y.setEnabled(False)
            self.ui.LineEdit_end_y.setText(self.ui.LineEdit_start_y.text())
            self.ui.LineEdit_end_x.setEnabled(True)

    # def setStart(self):
    #     if self.ui.radioButton_x.isChecked():
    #         self.ui.LineEdit_end_x.setText(self.ui.LineEdit_start_x.text())
    #     else:
    #         self.ui.LineEdit_end_y.setText(self.ui.LineEdit_start_y.text())
