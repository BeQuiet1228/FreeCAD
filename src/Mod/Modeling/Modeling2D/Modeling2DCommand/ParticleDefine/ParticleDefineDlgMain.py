# -*- coding: utf-8 -*-
import traceback

from PySide import QtGui
import FreeCAD
import FreeCADGui

from Modeling.Modeling2D.Modeling2DCommand.ParticleDefine import ParticleDefineDialog
from Modeling.Modeling2D.Tools import ToolsUI, Tools2D


class ShowDialog(QtGui.QDialog):
    def __init__(self, obj, isNew=False, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = ParticleDefineDialog.Ui_Dialog()
        self.ui.setupUi(self)

        self.obj = obj
        self.isNew = isNew
        self.initDialog()
        self.isKeepData = False

    def slotCancel(self):
        self.isKeepData = False
        self.close()

    def slotOK(self):
        self.isKeepData = True
        self.close()

    def initDialog(self):
        self.loadData()
        self.ui.pb_ok.clicked.connect(self.slotOK)
        self.ui.pb_cancel.clicked.connect(self.slotCancel)

    def keepData(self):
        try:
            Tools2D.setLabelToObj(self.obj, self.ui.LineEdit_Name.text())
            self.obj.powerUnit = self.ui.LineEdit_Unitl.text().replace(" ", "")
            self.obj.mass = self.ui.LineEdit_Quality.text().replace(" ", "")
            self.obj.protonMassUnit = self.ui.comboBox.currentText()
        except:
            Tools2D.sayz("ParticleDefine设置数据时出现异常")
            Tools2D.sayz(traceback.format_exc())

    def loadData(self):
        try:
            self.ui.LineEdit_Name.setText(self.obj.Label)
            self.ui.LineEdit_Unitl.setText(self.obj.powerUnit)
            self.ui.LineEdit_Quality.setText(self.obj.mass)
            self.ui.comboBox.setCurrentIndex(self.ui.comboBox.findText(self.obj.protonMassUnit))
        except:
            Tools2D.sayz("ParticleDefine加载数据时出现异常")
            Tools2D.sayz(traceback.format_exc())

    # 点击关闭对话框，删除创建的对象
    def closeEvent(self, event):
        if self.isKeepData:
            self.keepData()
            FreeCADGui.runCommand("CreateM2D")
        else:
            if self.isNew:
                FreeCAD.ActiveDocument.removeObject(self.obj.Label)
