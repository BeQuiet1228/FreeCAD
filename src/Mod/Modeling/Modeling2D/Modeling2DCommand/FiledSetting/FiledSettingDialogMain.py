# -*- coding: utf-8 -*-
import FiledSettingDialog
from PySide import QtGui
import FreeCAD
import FreeCADGui
from Modeling.Modeling2D.Tools import Tools2D


class ShowDialog(QtGui.QDialog):
    def __init__(self, obj, isNew=False, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = FiledSettingDialog.Ui_Dialog_FieldSettingDlg()
        self.ui.setupUi(self)
        self.obj = obj
        self.isNew = isNew
        self.helperInitDialog()
        self.loadData()
        self.setModal(False)
        self.isKeepData = False

    def helperInitDialog(self):
        self.ui.pushButton_ok.clicked.connect(self.helperOK)
        # 获取当前坐标系及坐标系单位
        coord = Tools2D.getCoordinate()
        self.x = coord[0]
        self.y = coord[1]
        # 根据坐标系初始化面板
        parameter = "("+self.x+","+self.y+")= "
        self.ui.checkBox_magenetic_x.setText(self.x+u"方向FB"+self.x+"ST"+parameter)
        self.ui.checkBox_magenetic_y.setText(self.y+u"方向FB"+self.y+"ST"+parameter)
        self.ui.checkBox_electric_x.setText(self.x+u"方向FE"+self.x+"ST"+parameter)
        self.ui.checkBox_electric_y.setText(self.y+u"方向FE"+self.y+"ST"+parameter)

    def helperOK(self):
        self.isKeepData = True
        self.close()

    def loadData(self):
        # 电磁场按钮
        self.ui.checkBox_magenetic_x.setChecked(self.obj.isMagnetostaticFieldX)
        self.ui.checkBox_magenetic_y.setChecked(self.obj.isMagnetostaticFieldY)
        self.ui.checkBox_electric_x.setChecked(self.obj.isElectrostaticFieldX)
        self.ui.checkBox_electric_y.setChecked(self.obj.isElectrostaticFieldY)
        # 静电磁场的值
        self.ui.LineEdit_magenetic_x.setText(self.obj.magnetostaticFieldX)
        self.ui.LineEdit_magenetic_y.setText(self.obj.magnetostaticFieldY)
        self.ui.LineEdit_electric_x.setText(self.obj.electrostaticFieldX)
        self.ui.LineEdit_electric_y.setText(self.obj.electrostaticFieldY)
        self.ui.textEdit_filed_custom.setText(self.obj.self_definingFunction)

    def keepData(self):
        # 静电磁场按钮
        self.obj.isMagnetostaticFieldX = self.ui.checkBox_magenetic_x.isChecked()
        self.obj.isMagnetostaticFieldY = self.ui.checkBox_magenetic_y.isChecked()
        self.obj.isElectrostaticFieldX = self.ui.checkBox_electric_x.isChecked()
        self.obj.isElectrostaticFieldY = self.ui.checkBox_electric_y.isChecked()
        # 静电磁场的值
        self.obj.magnetostaticFieldX = self.ui.LineEdit_magenetic_x.toPlainText()
        self.obj.magnetostaticFieldY = self.ui.LineEdit_magenetic_y.toPlainText()
        self.obj.electrostaticFieldX = self.ui.LineEdit_electric_x.toPlainText()
        self.obj.electrostaticFieldY = self.ui.LineEdit_electric_y.toPlainText()
        self.obj.self_definingFunction = self.ui.textEdit_filed_custom.toPlainText()

    def closeEvent(self, event):
        if self.isKeepData:
            self.keepData()
            FreeCADGui.runCommand("CreateM2D")
        else:
            if self.isNew:
                FreeCAD.ActiveDocument.removeObject(self.obj.Label)
