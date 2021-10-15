# -*- coding: utf-8 -*-
import DrivDialog
from PySide import QtGui
import FreeCAD

from Modeling.Modeling2D.Modeling2DCommand.BaseUI import BaseDialog
 
from Modeling.Common.Tools import DocumentTools,ObjectsTools
from Modeling.Modeling2D.Tools import Tools2D


class ShowDialog(BaseDialog.BaseOtherDialog):
    def __init__(self, obj, isNew=False, parent=None):
        BaseDialog.BaseOtherDialog.__init__(self, obj, isNew, parent)
        self.setModal(False)

    def setUI(self):
        self.ui = DrivDialog.Ui_Dialog_ExpDlg()
        self.ui.setupUi(self)

    def helperInitDialog(self):
        self.defaultValue = ["OSYS$AREA"]
        # 法相
        self.ui.radioButton_x.clicked.connect(self.slotRadioButton)
        self.ui.radioButton_y.clicked.connect(self.slotRadioButton)
        # 正投影面下拉框选择事件
        self.ui.ComboBox_Shadow.currentIndexChanged.connect(self.slotComboBoxShadow)
        self.ui.comboBox.currentIndexChanged.connect(self.slotComboBox)
        self.ui.LineEdit_start_x.textChanged.connect(self.slotRadioButton)
        self.ui.LineEdit_start_y.textChanged.connect(self.slotRadioButton)

        # 获取当前坐标系及坐标系单位
        coord = Tools2D.getCoordinate()
        self.x = coord[0]
        self.y = coord[1]
        self.z = coord[2]
        # self.x_unit = coord[3]
        # self.y_unit = coord[4]
        # self.z_unit = coord[5]
        # 根据坐标系初始化面板
        self.ui.label_X.setText(self.x)
        self.ui.label_Y.setText(self.y)
        self.ui.radioButton_x.setText(self.x)
        self.ui.radioButton_y.setText(self.y)
        self.ui.label_3.setText("函数.JFUNC(T,"+self.x+","+self.y+")=")

        # 关闭Z轴设置
        self.ui.label_Z.hide()
        self.ui.LineEdit_end_z.hide()
        self.ui.LineEdit_start_z.hide()
        self.ui.radioButton_z.hide()

        self.loadData()

    def helperCancel(self):
        self.isKeepData = False
        self.close()

    def helperOK(self):
        self.isKeepData = True
        self.close()

    def slotComboBoxShadow(self):
        if self.ui.ComboBox_Shadow.currentIndex() == 0:
            self.addShadowItem(Tools2D.ObjectType.Point)
            self.ui.LineEdit_end_x.setEnabled(False)
            self.ui.LineEdit_end_y.setEnabled(False)
            self.ui.radioButton_x.setEnabled(False)
            self.ui.radioButton_y.setEnabled(False)
        elif self.ui.ComboBox_Shadow.currentIndex() == 1:
            self.addShadowItem(Tools2D.ObjectType.LineConformal)
            self.ui.LineEdit_end_x.setEnabled(not self.ui.radioButton_x.isChecked())
            self.ui.LineEdit_end_y.setEnabled(not self.ui.radioButton_y.isChecked())
            self.ui.radioButton_x.setEnabled(True)
            self.ui.radioButton_y.setEnabled(True)
        elif self.ui.ComboBox_Shadow.currentIndex() == 2:
            self.addShadowItem(Tools2D.ObjectType.AreaConformal)
            self.ui.LineEdit_end_x.setEnabled(True)
            self.ui.LineEdit_end_y.setEnabled(True)
            self.ui.radioButton_x.setEnabled(False)
            self.ui.radioButton_y.setEnabled(False)

    def slotRadioButton(self):
        """
        radioButton相关的槽函数，主要设置lineEdit的编辑状态
        """
        if self.ui.ComboBox_Shadow.currentIndex() == 1:
            self.ui.LineEdit_end_x.setEnabled(not self.ui.radioButton_x.isChecked())
            self.ui.LineEdit_end_y.setEnabled(not self.ui.radioButton_y.isChecked())
            if self.ui.radioButton_x.isChecked():
                self.ui.LineEdit_end_x.setText(self.ui.LineEdit_start_x.text())
            elif self.ui.radioButton_y.isChecked():
                self.ui.LineEdit_end_y.setText(self.ui.LineEdit_start_y.text())
        else:
            # Tools2D.sayz("radioButton点击出现了意外的情况，仅在线电流源时该按钮才能被点击")
            pass

    def loadData(self):
        self.ui.LineEdit_Name.setText(self.obj.Label)
        # 下拉框
        # self.ui.comboBox.setCurrentIndex(self.ui.comboBox.findText(str(self.obj.assignSource)))
        self.slotComboBoxShadow()
        # 坐标
        self.ui.LineEdit_start_x.setText(self.obj.point1_X)
        self.ui.LineEdit_start_y.setText(self.obj.point1_Y)
        self.ui.LineEdit_end_x.setText(self.obj.point2_X)
        self.ui.LineEdit_end_y.setText(self.obj.point2_Y)
        # 根据选择的具体obj设置Dialog
        self.ui.ComboBox_Shadow.setCurrentIndex(self.ui.ComboBox_Shadow.findText(str(self.obj.sourceType)))
        self.ui.comboBox.setCurrentIndex(self.ui.comboBox.findText(str(self.obj.assignSource)))
        self.slotComboBox()
        # 法向选择
        self.ui.radioButton_x.setChecked(self.obj.isCheckNormal1)
        self.ui.radioButton_y.setChecked(self.obj.isCheckNormal2)
        # 指定电流密度
        self.ui.ComboBox_Current.setCurrentIndex(
            self.ui.ComboBox_Current.findText(str(self.obj.electricCurrentDensity)))
        # 函数JFUNC
        self.ui.LineEdit_JFunc.setText(self.obj.function)

    def keepData(self):
        # 名字
        Tools2D.setLabelToObj(self.obj, self.ui.LineEdit_Name.text())
        self.obj.assignSource = self.ui.comboBox.currentText()
        self.obj.sourceType = self.ui.ComboBox_Shadow.currentText()
        self.obj.point1_X = self.ui.LineEdit_start_x.text()
        self.obj.point1_Y = self.ui.LineEdit_start_y.text()
        self.obj.point2_X = self.ui.LineEdit_end_x.text()
        self.obj.point2_Y = self.ui.LineEdit_end_y.text()
        # 法向选择
        self.obj.isCheckNormal1 = self.ui.radioButton_x.isChecked()
        self.obj.isCheckNormal2 = not (self.obj.isCheckNormal1)
        # 指定电流密度
        self.obj.electricCurrentDensity = self.ui.ComboBox_Current.currentText()
        # 函数JFUNC
        self.obj.function = self.ui.LineEdit_JFunc.text()

    def addShadowItem(self, obj_type):
        """
        ComboBox根据ComboBox_Shadow添加选项
        """
        # 添加前清空所有选项
        self.ui.comboBox.clear()
        self.ui.comboBox.addItem(u"未指定")
        Orthogonal_list = Tools2D.getLabelsByType(obj_type)
        if obj_type == Tools2D.ObjectType.AreaConformal:
            Orthogonal_list.append("OSYS$AREA")
            # Orthogonal_list.append("OSYS$MIDPLANE2")
            # Orthogonal_list.append("OSYS$MIDPLANE3")
        # if obj_type == Tools2D.ObjectType.LineConformal:
        #     Orthogonal_list.append("OSYS$VOLUME")
        for i in Orthogonal_list:
            self.ui.comboBox.addItem(i)

    def slotComboBox(self):
        """
        comboBox的槽函数
        """
        # 当清除comboBox的内容的时候也会触发该函数，为避免情况Dialog信息，提前结束该函数
        if self.ui.comboBox.currentIndex() == -1:
            return
        self.ui.radioButton_x.setEnabled(False)
        self.ui.radioButton_y.setEnabled(False)
        objName = self.ui.comboBox.currentText()
        if self.ui.ComboBox_Shadow.currentIndex() == 0:
            if objName == u'未指定':
                self.ui.LineEdit_start_x.setEnabled(True)
                self.ui.LineEdit_start_y.setEnabled(True)
            else:
                modelData = Tools2D.getValueOfAreaObjByLabel(objName)
                self.ui.LineEdit_start_x.setText(modelData["point1.x"])
                self.ui.LineEdit_start_y.setText(modelData["point1.y"])
                self.ui.LineEdit_start_x.setEnabled(False)
                self.ui.LineEdit_start_y.setEnabled(False)
            self.ui.LineEdit_end_x.setEnabled(False)
            self.ui.LineEdit_end_y.setEnabled(False)
            # 法向不可选
            self.ui.radioButton_x.setEnabled(False)
            self.ui.radioButton_y.setEnabled(False)
        elif self.ui.ComboBox_Shadow.currentIndex() == 1:
            if objName == u'未指定':
                self.ui.LineEdit_start_x.setEnabled(True)
                self.ui.LineEdit_start_y.setEnabled(True)
                self.slotRadioButton()
                # 法向不可选
                self.ui.radioButton_x.setEnabled(True)
                self.ui.radioButton_y.setEnabled(True)
            else:
                modelData = Tools2D.getValueOfAreaObjByLabel(objName)
                if objName in self.defaultValue:
                    pass
                else:
                    self.ui.LineEdit_start_x.setText(modelData["point1.x"])
                    self.ui.LineEdit_start_y.setText(modelData["point1.y"])
                    self.ui.LineEdit_end_x.setText(modelData["point2.x"])
                    self.ui.LineEdit_end_y.setText(modelData["point2.y"])
                    # 法向
                    if modelData["normal"] == "X" or modelData["normal"] == "x" or \
                            modelData["normal"] == "Z" or modelData["normal"] == "z":
                        self.ui.radioButton_x.setChecked(True)
                        # self.ui.LineEdit_end_x.setText(self.ui.LineEdit_start_x)
                    elif modelData["normal"] == "Y" or modelData["normal"] == "y" or \
                            modelData["normal"] == "R" or modelData["normal"] == "r":
                        self.ui.radioButton_y.setChecked(True)
                        # self.ui.LineEdit_end_y.setText(self.ui.LineEdit_start_y)
                    else:
                        Tools2D.sayz("get Area_Conformal error")
                self.ui.LineEdit_start_x.setEnabled(False)
                self.ui.LineEdit_start_y.setEnabled(False)
                self.ui.LineEdit_end_x.setEnabled(False)
                self.ui.LineEdit_end_y.setEnabled(False)
        elif self.ui.ComboBox_Shadow.currentIndex() == 2:
            if objName == u'未指定':
                self.ui.LineEdit_start_x.setEnabled(True)
                self.ui.LineEdit_start_y.setEnabled(True)
                self.ui.LineEdit_end_x.setEnabled(True)
                self.ui.LineEdit_end_y.setEnabled(True)
            else:
                if objName in self.defaultValue:
                    pass
                else:
                    modelData = Tools2D.getValueOfAreaObjByLabel(objName)
                    self.ui.LineEdit_start_x.setText(modelData["point1.x"])
                    self.ui.LineEdit_start_y.setText(modelData["point1.y"])
                    self.ui.LineEdit_end_x.setText(modelData["point2.x"])
                    self.ui.LineEdit_end_y.setText(modelData["point2.y"])
                self.ui.LineEdit_start_x.setEnabled(False)
                self.ui.LineEdit_start_y.setEnabled(False)
                self.ui.LineEdit_end_x.setEnabled(False)
                self.ui.LineEdit_end_y.setEnabled(False)
            # 法向不可选
            self.ui.radioButton_x.setEnabled(False)
            self.ui.radioButton_y.setEnabled(False)


