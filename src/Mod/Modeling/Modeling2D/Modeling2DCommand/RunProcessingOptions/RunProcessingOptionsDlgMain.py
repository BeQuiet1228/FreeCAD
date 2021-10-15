# -*- coding: UTF-8 -*-
import json
import traceback

import FreeCAD
import FreeCADGui
from PySide import QtGui

from Modeling.Modeling2D.Modeling2DCommand.RunProcessingOptions import RunProcessingOptionsDialog
from Modeling.Modeling2D.Tools import Tools2D


class ShowDialog(QtGui.QDialog):
    def __init__(self, obj, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = RunProcessingOptionsDialog.Ui_Dialog_RunOptionsDlg()
        self.ui.setupUi(self)

        self.obj = obj
        self.initDialog()
        self.setModal(False)

    def initDialog(self):
        # noinspection PyBroadException
        try:
            self.ui.pushButton_ok.clicked.connect(self.pushBtn_OK)
            self.loadData()
        except Exception as reason:
            Tools2D.sayz("初始化Dialog时出现错误，错误如下：")
            Tools2D.sayz(traceback.format_exc())
        else:
            Tools2D.sayz("正确初始化对话框")

    def pushBtn_OK(self):
        self.keepData()
        FreeCADGui.runCommand("CreateM2D")
        self.close()

    def pushBtn_Cancel(self):
        self.close()

    def loadData(self):
        # noinspection PyBroadException
        try:
            self.ui.checkBox_show_structureChart.setChecked(self.obj.isDisplayStructureDrawing)
            self.ui.checkBox_paused_when_start.setChecked(self.obj.isHaltedState)
        except KeyError as reason:
            FreeCAD.Console.PrintMessage(str(reason))
        except:
            Tools2D.sayz(traceback.format_exc())

    def keepData(self):
        self.obj.isDisplayStructureDrawing = self.ui.checkBox_show_structureChart.isChecked()
        self.obj.isHaltedState = self.ui.checkBox_paused_when_start.isChecked()

