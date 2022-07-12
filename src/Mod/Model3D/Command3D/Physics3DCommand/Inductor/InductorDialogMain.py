# -*- coding: utf-8 -*-
import InductorDialog
from Model3D.Tools import Tools3D, ObjectTools
from Model3D.Command3D.Model3DCommand.BaseUI import BaseDialogMain


class ShowDialog(BaseDialogMain.BasePhysicsDialog):
    def __init__(self, obj, isNew=False, parent=None):
        BaseDialogMain.BasePhysicsDialog.__init__(self, obj, isNew, parent)

    def setUI(self):
        self.ui = InductorDialog.Ui_Dialog_IndDlg()
        self.ui.setupUi(self)

    def loadDialog(self):
        try:
            # 输入框变化时
            self.ui.LineEdit_start_x.textChanged.connect(self.LineEdit_start_x_textChanged)
            self.ui.LineEdit_start_y.textChanged.connect(self.LineEdit_start_y_textChanged)
            self.ui.LineEdit_start_z.textChanged.connect(self.LineEdit_start_z_textChanged)

            self.ui.radioButton_x.clicked.connect(self.radioButton_clicked)
            self.ui.radioButton_y.clicked.connect(self.radioButton_clicked)
            self.ui.radioButton_z.clicked.connect(self.radioButton_clicked)
            self.ui.checkBox_induc.clicked.connect(self.checkBox_induc_clicked)
            Tools3D.switchPointLabel(self.ui)
            Tools3D.switchRadioButtonLabel(self.ui)

            # 刷新下拉框
            self.refreshCombox()
            # 正投影面下拉框选择事件
            self.ui.ComboBox_Shadow.currentIndexChanged.connect(self.ComboBox_Shadow_clicked)

            self.ComboBox_Shadow_clicked()
        except:
            Tools3D.sayz("error!")

    def refreshCombox(self):
        # 每次加载窗口时都要重新加载下拉列表，以实现动态加载
        ComboBox_Shadow_list = []
        for i in range(self.ui.ComboBox_Shadow.count()):
            ComboBox_Shadow_list.append(self.ui.ComboBox_Shadow.itemText(i))
        volumeList = ObjectTools.getLabelsByType(ObjectTools.ObjectType.Line_Conformal)
        for i in volumeList:
            if i not in ComboBox_Shadow_list:
                self.ui.ComboBox_Shadow.addItem(i)

    def ComboBox_Shadow_clicked(self):
        if self.ui.ComboBox_Shadow.currentIndex() == 0:
            self.ui.LineEdit_Name.setEnabled(True)
            Tools3D.setCoordEnabled(self.ui, ObjectTools.ObjectType.Line_Conformal)
        else:
            objName = self.ui.ComboBox_Shadow.currentText()
            Tools3D.setModelCoordinate(self.ui, objName)
            Tools3D.setIsEdit(self.ui, False)

    def getInfoFromObj(self):
        try:
            self.ui.LineEdit_Name.setText(self.obj.Label)
            # 设置标记的旧名字
            self.ui.ComboBox_Shadow.setCurrentIndex(self.ui.ComboBox_Shadow.findText(self.obj.inductorType))
            Tools3D.setCoorToUI(self.ui, self.obj)
            Tools3D.setRadioButtonToUI(self.ui, self.obj)
            self.ComboBox_Shadow_clicked()
            # 线圈直径
            self.ui.LineEdit_diam.setText(self.obj.coilDiameter)
            # 自感系数
            self.ui.checkBox_induc.setChecked(self.obj.isCheckSelfInductor)
            self.ui.LineEdit_induc.setText(self.obj.selfInductorCoefficient)

            if self.ui.ComboBox_Shadow.currentIndex() == 0:
                self.radioButton_clicked()
        except:
            import traceback
            Tools3D.sayz("error:" + traceback.format_exc())

    def setInfoToObj(self):
        try:
            self.obj.inductorType = self.ui.ComboBox_Shadow.currentText()
            self.obj.Label = Tools3D.setLabel(self.ui.LineEdit_Name.text())
            # 法向选择
            # self.obj.isCheckNormal1 = self.ui.radioButton_x.isChecked()
            # self.obj.isCheckNormal2 = self.ui.radioButton_y.isChecked() and not self.obj.isCheckNormal1
            # self.obj.isCheckNormal3 = not self.obj.isCheckNormal1 and not self.obj.isCheckNormal2
            Tools3D.getUICoordinate(self.obj, self.ui)
            Tools3D.getUIRadioButton(self.obj, self.ui)
            # 线圈直径
            self.obj.coilDiameter = self.ui.LineEdit_diam.text()
            # 自感系数
            self.obj.isCheckSelfInductor = self.ui.checkBox_induc.isChecked()
            self.obj.selfInductorCoefficient = self.ui.LineEdit_induc.text()
        except:
            import traceback
            Tools3D.sayz("error:" + traceback.format_exc())

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

    def radioButton_clicked(self):
        if self.ui.radioButton_x.isChecked():
            self.ui.LineEdit_end_x.setEnabled(True)
            self.ui.LineEdit_end_y.setEnabled(False)
            self.ui.LineEdit_end_z.setEnabled(False)
            self.ui.LineEdit_end_y.setText(self.ui.LineEdit_start_y.text())
            self.ui.LineEdit_end_z.setText(self.ui.LineEdit_start_z.text())

        elif self.ui.radioButton_y.isChecked():
            self.ui.LineEdit_end_y.setEnabled(True)
            self.ui.LineEdit_end_x.setEnabled(False)
            self.ui.LineEdit_end_z.setEnabled(False)
            self.ui.LineEdit_end_x.setText(self.ui.LineEdit_start_x.text())
            self.ui.LineEdit_end_z.setText(self.ui.LineEdit_start_z.text())

        elif self.ui.radioButton_z.isChecked():
            self.ui.LineEdit_end_z.setEnabled(True)
            self.ui.LineEdit_end_x.setEnabled(False)
            self.ui.LineEdit_end_y.setEnabled(False)
            self.ui.LineEdit_end_x.setText(self.ui.LineEdit_start_x.text())
            self.ui.LineEdit_end_y.setText(self.ui.LineEdit_start_y.text())

    def checkBox_induc_clicked(self):
        self.ui.LineEdit_induc.setEnabled(self.ui.checkBox_induc.isChecked())
