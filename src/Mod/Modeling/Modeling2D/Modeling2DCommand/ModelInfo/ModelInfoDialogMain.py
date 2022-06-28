# -*- coding: utf-8 -*-
import ModeInfoDialog
from PySide import QtGui
import FreeCAD
import FreeCADGui


class ShowDialog(QtGui.QDialog):
    def __init__(self, obj, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = ModeInfoDialog.Ui_Dialog_ModelingInfoDlg()
        self.ui.setupUi(self)
        self.obj = obj
        self.helperInitDialog()
        self.loadData()
        self.setModal(False)

    def helperInitDialog(self):
        self.ui.pb_ok.clicked.connect(self.helperOK)

    def helperOK(self):
        self.keepData()
        FreeCADGui.runCommand("CreateM2D")
        self.close()

    def loadData(self):
        self.ui.lineEdit_modeling.setText(self.obj.model)
        self.ui.lineEdit_author.setText(self.obj.author)
        self.ui.lineEdit_company.setText(self.obj.organization)
        self.ui.lineEdit_remarks.setText(self.obj.remark)

    def keepData(self):
        self.obj.model = self.ui.lineEdit_modeling.text()
        self.obj.author = self.ui.lineEdit_author.text()
        self.obj.organization = self.ui.lineEdit_company.text()
        self.obj.remark = self.ui.lineEdit_remarks.text()
