#-*- coding: utf-8 -*-
import Physics.PhysicsGui.PortDlg
from PySide import QtGui

class PortShow(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = Physics.PhysicsGui.PortDlg.Ui_Dialog_PortDlg()
        self.ui.setupUi(self)
        self.ui.pushButton_ok.clicked.connect(self.onCancel)
        self.ui.pushButton.clicked.connect(self.onCancel)
        self.ui.radioButton_x.clicked.connect(self.radioButton_x_clicked)
        self.ui.radioButton_y.clicked.connect(self.radioButton_y_clicked)
        self.ui.radioButton_z.clicked.connect(self.radioButton_z_clicked)
        self.ui.checkBox_x.clicked.connect(self.checkBox_x_clicked)
        self.ui.checkBox_y.clicked.connect(self.checkBox_y_clicked)
        self.ui.checkBox_z.clicked.connect(self.checkBox_z_clicked)

    # 点击取消按钮关闭窗口
    def onCancel(self):
        self.close()

    # 点击法向x按钮
    def radioButton_x_clicked(self):
        self.ui.lineEdit_end_x.setEnabled(False)
        self.ui.lineEdit_end_y.setEnabled(True)
        self.ui.lineEdit_end_z.setEnabled(True)

    # 点击法向y按钮
    def radioButton_y_clicked(self):
        self.ui.lineEdit_end_y.setEnabled(False)
        self.ui.lineEdit_end_x.setEnabled(True)
        self.ui.lineEdit_end_z.setEnabled(True)

    # 点击法向z按钮
    def radioButton_z_clicked(self):
        self.ui.lineEdit_end_z.setEnabled(False)
        self.ui.lineEdit_end_x.setEnabled(True)
        self.ui.lineEdit_end_y.setEnabled(True)

    def checkBox_x_clicked(self):
        self.ui.lineEdit_DX1.setEnabled(True)
        self.ui.lineEdit_DX2.setEnabled(False)
        self.ui.lineEdit_DX3.setEnabled(False)

    def checkBox_y_clicked(self):
        self.ui.lineEdit_DX1.setEnabled(False)
        self.ui.lineEdit_DX2.setEnabled(True)
        self.ui.lineEdit_DX3.setEnabled(False)

    def checkBox_z_clicked(self):
        self.ui.lineEdit_DX1.setEnabled(False)
        self.ui.lineEdit_DX2.setEnabled(False)
        self.ui.lineEdit_DX3.setEnabled(True)

def show():
    p = PortShow()
    p.show()
    p.exec_()