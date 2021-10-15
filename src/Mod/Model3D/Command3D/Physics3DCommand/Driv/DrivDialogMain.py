# -*- coding: utf-8 -*-
import DrivDialog
from PySide import QtGui
import FreeCAD
from Model3D.Tools import Tools3D, ObjectTools
from Model3D.Command3D.Model3DCommand.BaseUI import BaseDialogMain


class ShowDialog(BaseDialogMain.BasePhysicsDialog):
    def __init__(self, obj, isNew=False, parent=None):
        BaseDialogMain.BasePhysicsDialog.__init__(self, obj, isNew, parent)

    def setUI(self):
        self.ui = DrivDialog.Ui_Dialog_ExpDlg()
        self.ui.setupUi(self)

    def loadDialog(self):
        try:
            self.defaultValue = ["OSYS$AREA"]
            self.ui.radioButton_x.clicked.connect(self.slotRadioButton)
            self.ui.radioButton_y.clicked.connect(self.slotRadioButton)
            self.ui.radioButton_z.clicked.connect(self.slotRadioButton)

            self.ui.ComboBox_Shadow.currentIndexChanged.connect(self.slotComboBoxShadow)
            self.ui.comboBox.currentIndexChanged.connect(self.slotComboBox)
            self.ui.LineEdit_start_x.textChanged.connect(self.slotRadioButton)
            self.ui.LineEdit_start_y.textChanged.connect(self.slotRadioButton)
            self.ui.LineEdit_start_z.textChanged.connect(self.slotRadioButton)

            # 根据坐标系初始化面板
            Tools3D.switchPointLabel(self.ui)
            Tools3D.switchRadioButtonLabel(self.ui)

        except:
            Tools3D.sayz("error!")

    def slotComboBoxShadow(self):
        if self.ui.ComboBox_Shadow.currentIndex() == 0:
            self.addShadowItem(ObjectTools.ObjectType.Point)
            self.ui.LineEdit_end_x.setEnabled(False)
            self.ui.LineEdit_end_y.setEnabled(False)
            self.ui.LineEdit_end_y.setEnabled(False)
            self.ui.radioButton_x.setEnabled(False)
            self.ui.radioButton_y.setEnabled(False)
            self.ui.radioButton_z.setEnabled(False)
        elif self.ui.ComboBox_Shadow.currentIndex() == 1:
            self.addShadowItem(ObjectTools.ObjectType.Line_Conformal)
            self.ui.LineEdit_end_x.setEnabled(self.ui.radioButton_x.isChecked())
            self.ui.LineEdit_end_y.setEnabled(self.ui.radioButton_y.isChecked())
            self.ui.LineEdit_end_z.setEnabled(self.ui.radioButton_z.isChecked())
            self.ui.radioButton_x.setEnabled(True)
            self.ui.radioButton_y.setEnabled(True)
            self.ui.radioButton_z.setEnabled(True)
        elif self.ui.ComboBox_Shadow.currentIndex() == 2:
            self.addShadowItem(ObjectTools.ObjectType.Area_Conformal)
            self.ui.LineEdit_end_x.setEnabled(not self.ui.radioButton_x.isChecked())
            self.ui.LineEdit_end_y.setEnabled(not self.ui.radioButton_y.isChecked())
            self.ui.LineEdit_end_z.setEnabled(not self.ui.radioButton_z.isChecked())
            self.ui.radioButton_x.setEnabled(True)
            self.ui.radioButton_y.setEnabled(True)
            self.ui.radioButton_z.setEnabled(True)
        elif self.ui.ComboBox_Shadow.currentIndex() == 3:
            self.addShadowItem(ObjectTools.ObjectType.Vol_Conformal)
            self.ui.LineEdit_end_x.setEnabled(True)
            self.ui.LineEdit_end_y.setEnabled(True)
            self.ui.LineEdit_end_z.setEnabled(True)
            self.ui.radioButton_x.setEnabled(False)
            self.ui.radioButton_y.setEnabled(False)
            self.ui.radioButton_z.setEnabled(False)



    def slotRadioButton(self):
        """
        radioButton相关的槽函数，主要设置lineEdit的编辑状态
        """
        if self.ui.ComboBox_Shadow.currentIndex() == 1:
            self.ui.LineEdit_end_x.setEnabled(self.ui.radioButton_x.isChecked())
            self.ui.LineEdit_end_y.setEnabled(self.ui.radioButton_y.isChecked())
            self.ui.LineEdit_end_z.setEnabled(self.ui.radioButton_z.isChecked())
            if self.ui.radioButton_x.isChecked():
                self.ui.LineEdit_end_z.setText(self.ui.LineEdit_start_z.text())
                self.ui.LineEdit_end_y.setText(self.ui.LineEdit_start_y.text())
            elif self.ui.radioButton_y.isChecked():
                self.ui.LineEdit_end_x.setText(self.ui.LineEdit_start_x.text())
                self.ui.LineEdit_end_z.setText(self.ui.LineEdit_start_z.text())
            elif self.ui.radioButton_z.isChecked():
                self.ui.LineEdit_end_x.setText(self.ui.LineEdit_start_x.text())
                self.ui.LineEdit_end_y.setText(self.ui.LineEdit_start_y.text())

        elif self.ui.ComboBox_Shadow.currentIndex() == 2:
            self.ui.LineEdit_end_x.setEnabled(not self.ui.radioButton_x.isChecked())
            self.ui.LineEdit_end_y.setEnabled(not self.ui.radioButton_y.isChecked())
            self.ui.LineEdit_end_z.setEnabled(not self.ui.radioButton_z.isChecked())
            if self.ui.radioButton_x.isChecked():
                self.ui.LineEdit_end_x.setText(self.ui.LineEdit_start_x.text())
            elif self.ui.radioButton_y.isChecked():
                self.ui.LineEdit_end_y.setText(self.ui.LineEdit_start_y.text())
            elif self.ui.radioButton_z.isChecked():
                self.ui.LineEdit_end_z.setText(self.ui.LineEdit_start_z.text())
            pass
        elif self.ui.ComboBox_Shadow.currentIndex() == 3:
            pass
        pass


    def getInfoFromObj(self):
        try:
            self.ui.LineEdit_Name.setText(self.obj.Label)
            self.slotComboBox()

            Tools3D.setCoorToUI(self.ui, self.obj)
            # 根据选择的具体obj设置Dialog
            self.ui.ComboBox_Shadow.setCurrentIndex(self.ui.ComboBox_Shadow.findText(str(self.obj.sourceType)))
            self.ui.comboBox.setCurrentIndex(self.ui.comboBox.findText(str(self.obj.orthogonalProjectionPlane)))
            Tools3D.setRadioButtonToUI(self.ui, self.obj)
            # 指定电流密度
            self.ui.ComboBox_Current.setCurrentIndex(
                self.ui.ComboBox_Current.findText(str(self.obj.electricCurrentDensity)))
            # 函数JFUNC
            self.ui.LineEdit_JFunc.setText(self.obj.function)
            # self.slotRadioButton()



        except:
            import traceback
            Tools3D.sayz("error:" + traceback.format_exc())

    def setInfoToObj(self):
        try:
            self.obj.Label = Tools3D.setLabel(self.ui.LineEdit_Name.text())
            self.obj.orthogonalProjectionPlane = self.ui.comboBox.currentText()
            self.obj.sourceType = self.ui.ComboBox_Shadow.currentText()
            Tools3D.getUICoordinate(self.obj, self.ui)
            Tools3D.getUIRadioButton(self.obj, self.ui)
            # 法向选择
            # 指定电流密度
            self.obj.electricCurrentDensity = self.ui.ComboBox_Current.currentText()
            # 函数JFUNC
            self.obj.function = self.ui.LineEdit_JFunc.text()
        except:
            import traceback
            Tools3D.sayz("error:" + traceback.format_exc())

    def addShadowItem(self, obj_type):
        """
        ComboBox根据ComboBox_Shadow添加选项
        """
        # 添加前清空所有选项
        self.ui.comboBox.clear()
        self.ui.comboBox.addItem(u"未指定")
        Orthogonal_list = ObjectTools.getLabelsByType(obj_type)
        Orthogonal_list.append("OSYS$AREA")
        # if obj_type == ObjectTools.ObjectType.Area_Conformal:
        #     Orthogonal_list.append("OSYS$AREA")
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
        self.ui.radioButton_z.setEnabled(False)
        objName = self.ui.comboBox.currentText()
        if self.ui.ComboBox_Shadow.currentIndex() == 0:
            if objName == u'未指定':
                self.ui.LineEdit_start_x.setEnabled(True)
                self.ui.LineEdit_start_y.setEnabled(True)
                self.ui.LineEdit_start_z.setEnabled(True)
            else:
                if objName in self.defaultValue:
                    pass
                else:
                    Tools3D.setModelCoordinate(self.ui, objName)
                Tools3D.setIsEdit(self.ui, False)
                # 法向不可选
                self.ui.radioButton_x.setEnabled(False)
                self.ui.radioButton_y.setEnabled(False)
                self.ui.radioButton_y.setEnabled(False)

        elif self.ui.ComboBox_Shadow.currentIndex() == 1:
            if objName == u'未指定':
                self.ui.LineEdit_start_x.setEnabled(True)
                self.ui.LineEdit_start_y.setEnabled(True)
                self.ui.LineEdit_start_z.setEnabled(True)
                self.slotRadioButton()
                # 法向可选
                self.ui.radioButton_x.setEnabled(True)
                self.ui.radioButton_y.setEnabled(True)
                self.ui.radioButton_y.setEnabled(True)
            else:
                if objName in self.defaultValue:
                    pass
                else:
                    Tools3D.setModelCoordinate(self.ui, objName)
                    Tools3D.sayz("line")
                Tools3D.setIsEdit(self.ui, False)


        elif self.ui.ComboBox_Shadow.currentIndex() == 2:
            if objName == u'未指定':
                self.ui.LineEdit_start_x.setEnabled(True)
                self.ui.LineEdit_start_y.setEnabled(True)
                self.ui.LineEdit_start_z.setEnabled(True)
                self.ui.LineEdit_end_x.setEnabled(True)
                self.ui.LineEdit_end_y.setEnabled(True)
                self.ui.LineEdit_end_z.setEnabled(True)
                self.ui.radioButton_x.setEnabled(True)
                self.ui.radioButton_y.setEnabled(True)
                self.ui.radioButton_y.setEnabled(True)
            else:
                if objName in self.defaultValue:
                    pass
                else:
                    Tools3D.setModelCoordinate(self.ui, objName)
                    Tools3D.sayz("area")
                Tools3D.setIsEdit(self.ui, False)

        elif self.ui.ComboBox_Shadow.currentIndex() == 3:
            if objName == u'未指定':
                self.ui.LineEdit_start_x.setEnabled(True)
                self.ui.LineEdit_start_y.setEnabled(True)
                self.ui.LineEdit_start_z.setEnabled(True)
                self.ui.LineEdit_end_x.setEnabled(True)
                self.ui.LineEdit_end_y.setEnabled(True)
                self.ui.LineEdit_end_z.setEnabled(True)
            else:
                if objName in self.defaultValue:
                    pass
                else:
                    Tools3D.setModelCoordinate(self.ui, objName)
                Tools3D.setIsEdit(self.ui, False)

    # # x法向修改时，修改起点即修改终点
    # def LineEdit_start_x_textChanged(self):
    #     if not self.ui.LineEdit_end_x.isEnabled():
    #         self.ui.LineEdit_end_x.setText(self.ui.LineEdit_start_x.text())
    #
    # # y法向修改时，修改起点即修改终点
    # def LineEdit_start_y_textChanged(self):
    #     if not self.ui.LineEdit_end_y.isEnabled():
    #         self.ui.LineEdit_end_y.setText(self.ui.LineEdit_start_y.text())
    #
    # # z法向修改时，修改起点即修改终点
    # def LineEdit_start_z_textChanged(self):
    #     if not self.ui.LineEdit_end_z.isEnabled():
    #         self.ui.LineEdit_end_z.setText(self.ui.LineEdit_start_z.text())



