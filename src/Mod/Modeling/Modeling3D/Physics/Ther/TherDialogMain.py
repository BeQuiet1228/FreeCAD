# -*- coding: utf-8 -*-
from PySide import QtGui, QtCore
import TherDialog
from Modeling.Modeling2D.Tools import Tools2D


class ShowDialog(QtGui.QDialog):
    def __init__(self, obj, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = TherDialog.Ui_Dialog_EmtDlg()
        self.ui.setupUi(self)

        self.setModal(False)
        self.obj = obj
        self.initDialog()
        self.loadData()

    def initDialog(self):
        try:
            self.ui.pb_ok.clicked.connect(self.pb_ok_clicked)
            self.ui.pb_cancel.clicked.connect(self.pb_cancel_clicked)
            Tools2D.EmissionUiData(self.obj, self.ui)

        except:
            import traceback
            Tools2D.sayz("error:" + traceback.format_exc())

    def pb_ok_clicked(self):
        self.keepData()
        self.close()

    def pb_cancel_clicked(self):
        self.close()

    def loadData(self):
        try:
            self.ui.LineEdit_WF.setText(self.obj.workingFunctionWF)
            self.ui.LineEdit_TP.setText(self.obj.workingTemperatureTP)
            Tools2D.EmissionUiData(self.obj, self.ui).loadDataFromObj()

        except KeyError as reason:
            Tools2D.sayz("!!!Error:KeyError,Maybe lack of key:%s" % str(reason))

    def keepData(self):
        try:
            self.obj.workingFunctionWF = self.ui.LineEdit_WF.text()
            self.obj.workingTemperatureTP = self.ui.LineEdit_TP.text()
            Tools2D.EmissionUiData(self.obj, self.ui).getDataFromUi()

        except KeyError as reason:
            Tools2D.sayz("!!!Error:KeyError,Maybe lack of key:%s" % str(reason))