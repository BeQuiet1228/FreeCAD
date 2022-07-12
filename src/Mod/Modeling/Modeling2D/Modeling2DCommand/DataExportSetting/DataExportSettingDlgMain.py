# -*- coding: utf-8 -*-
import json
import traceback

import FreeCAD
import FreeCADGui
import PySide
from PySide import QtGui, QtCore

from Modeling.Modeling2D.Modeling2DCommand.DataExportSetting import DataExportSettingDialog
from Modeling.Modeling2D.Tools import Tools2D


class ShowDialog(QtGui.QDialog):
    def __init__(self, obj, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = DataExportSettingDialog.Ui_Dialog_DataProcessingSettingDlg()
        self.ui.setupUi(self)

        self.obj = obj
        self.initDialog()
        self.loadData()
        self.setModal(False)

    def initDialog(self):
        # noinspection PyBroadException
        try:
            self.ui.checkBox_set_prefix.clicked.connect(self.onCheckBox_set_prefix)
            self.ui.checkBox_set_suffix.clicked.connect(self.onCheckBox_set_suffix)
            self.ui.pushButton_ok.clicked.connect(self.pushBtn_OK)

            self.onCheckBox_set_prefix()
            self.onCheckBox_set_suffix()
        except Exception as reason:
            Tools2D.sayz("初始化Dialog时出现错误，错误如下：")
            Tools2D.sayz(traceback.format_exc())

    def pushBtn_OK(self):
        self.keepData()
        FreeCADGui.runCommand("CreateM2D")
        self.close()

    def pushBtn_Cancel(self):
        self.close()

    def loadData(self):
        try:
            self.ui.checkBox_Time_obser.setChecked(self.obj.isTimeObservation)
            self.ui.checkBox_space_obser.setChecked(self.obj.isSpaceObservation)
            self.ui.checkBox_contor_plot.setChecked(self.obj.isAllelicChartData)
            self.ui.checkBox_vector_data.setChecked(self.obj.isVectorGraphData)
            self.ui.checkBox_phase_space.setChecked(self.obj.isPhaseSpatialData)
            self.ui.checkBox_set_prefix.setChecked(self.obj.isSetFilePrefix)
            self.ui.checkBox_set_suffix.setChecked(self.obj.isFileSuffixes)
            self.ui.lineEdit_prefix.setText(self.obj.setFilePrefix)
            self.ui.lineEdit_suffix.setText(self.obj.fileSuffixes)
            self.ui.radioButton_text_format.setChecked(self.obj.isTextFormat)
            self.ui.radioButton_binary_format.setChecked(self.obj.isBinaryFormat)
            self.onCheckBox_set_prefix()
            self.onCheckBox_set_suffix()
        except KeyError as reason:
            FreeCAD.Console.PrintMessage(str(reason))

    def keepData(self):
        # noinspection PyBroadException
        try:
            self.obj.isTimeObservation = self.ui.checkBox_Time_obser.isChecked()
            self.obj.isSpaceObservation = self.ui.checkBox_space_obser.isChecked()
            self.obj.isAllelicChartData = self.ui.checkBox_contor_plot.isChecked()
            self.obj.isVectorGraphData = self.ui.checkBox_vector_data.isChecked()
            self.obj.isPhaseSpatialData = self.ui.checkBox_phase_space.isChecked()
            self.obj.isSetFilePrefix = self.ui.checkBox_set_prefix.isChecked()
            self.obj.isFileSuffixes = self.ui.checkBox_set_suffix.isChecked()
            self.obj.setFilePrefix = self.ui.lineEdit_prefix.text()
            self.obj.fileSuffixes = self.ui.lineEdit_suffix.text()
            self.obj.isTextFormat = self.ui.radioButton_text_format.isChecked()
            self.obj.isBinaryFormat = self.ui.radioButton_binary_format.isChecked()
        except Exception as reason:
            Tools2D.sayz(traceback.format_exc())
        else:
            Tools2D.sayz("成功保存数据到Object")

    def onCheckBox_set_prefix(self):
        self.ui.lineEdit_prefix.setEnabled(self.ui.checkBox_set_prefix.isChecked())

    def onCheckBox_set_suffix(self):
        self.ui.lineEdit_suffix.setEnabled(self.ui.checkBox_set_suffix.isChecked())