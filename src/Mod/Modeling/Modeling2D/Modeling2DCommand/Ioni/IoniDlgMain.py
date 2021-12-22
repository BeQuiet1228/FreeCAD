# -*- coding: utf-8 -*-
import traceback

from PySide import QtGui
import FreeCAD
import FreeCADGui

from Modeling.Modeling2D.Modeling2DCommand.Ioni import IoniDialog
from Modeling.Modeling2D.Tools import Tools2D


class ShowDialog(QtGui.QDialog):
    def __init__(self, obj, isNew=False, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = IoniDialog.Ui_Dialog()
        self.ui.setupUi(self)

        self.obj = obj
        self.isNew = isNew
        self.initDialog()
        self.isKeepData = False

    def initDialog(self):
        self.loadData()
        self.ui.pb_ok.clicked.connect(self.slotOK)
        self.ui.pb_cancel.clicked.connect(self.slotCancel)

    def slotCancel(self):
        self.isKeepData = False
        self.close()

    def slotOK(self):
        self.isKeepData = True
        self.close()

    def keepData(self):
        try:
            Tools2D.setLabelToObj(self.obj, self.ui.le_name.text())
            self.obj.ionizationOfGas = self.ui.cb_type.currentText()
            self.obj.gasPressure = self.ui.le_pressure.text()
            self.obj.gasTemperature = self.ui.le_temperature.text()
        except:
            Tools2D.sayz("Ioni设置数据时出现异常")
            Tools2D.sayz(traceback.format_exc())

    def loadData(self):
        try:
            self.ui.le_name.setText(self.obj.Label)
            self.ui.cb_type.setCurrentIndex(self.ui.cb_type.findText(self.obj.ionizationOfGas))
            self.ui.le_pressure.setText(self.obj.gasPressure)
            self.ui.le_temperature.setText(self.obj.gasTemperature)
        except:
            Tools2D.sayz("Ioni加载数据时出现异常")
            Tools2D.sayz(traceback.format_exc())

    # 点击关闭对话框，删除创建的对象
    def closeEvent(self, event):
        if self.isKeepData:
            self.keepData()
            FreeCADGui.runCommand("CreateM2D")
        else:
            if self.isNew:
                FreeCAD.ActiveDocument.removeObject(self.obj.Label)
