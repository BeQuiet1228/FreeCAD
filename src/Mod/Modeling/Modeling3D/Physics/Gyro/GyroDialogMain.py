# -*- coding: utf-8 -*-
from PySide import QtGui, QtCore
import GyroDialog
from Modeling.Modeling2D.Tools import Tools2D


class ShowDialog(QtGui.QDialog):
    def __init__(self, obj, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = GyroDialog.Ui_Dialog_EmgDlg()
        self.ui.setupUi(self)

        self.setModal(False)
        self.obj = obj
        self.initDialog()
        self.loadData()

    def initDialog(self):
        try:
            self.ui.radioButton_AxiasZ.hide()
            self.ui.LineEdit_LaunchZ.hide()
            self.ui.groupBox_9.hide()

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
            self.ui.LineEdit_IT.setText(self.obj.beamCurrent)
            self.ui.LineEdit_magnetic.setText(self.obj.guidingMagneticField)
            self.ui.LineEdit_radius.setText(self.obj.guideRadius)
            self.ui.LineEdit_VerticalMomentum.setText(self.obj.longitudinalMomentum)
            self.ui.LineEdit_HorizontalMomentum.setText(self.obj.theHorizontalMomentum)
            self.ui.radioButton_AxiasX.setChecked(self.obj.isCheckX)
            self.ui.radioButton_AxiasY.setChecked(self.obj.isCheckY)
            self.ui.LineEdit_LaunchX.setText(self.obj.launchCenterCoordinatesX)
            self.ui.LineEdit_LaunchY.setText(self.obj.launchCenterCoordinatesY)
            Tools2D.EmissionUiData(self.obj, self.ui).loadDataFromObj()

        except KeyError as reason:
            Tools2D.sayz("!!!Error:KeyError,Maybe lack of key:%s" % str(reason))

    def keepData(self):
        try:
            self.obj.beamCurrent = self.ui.LineEdit_IT.text()
            self.obj.guidingMagneticField = self.ui.LineEdit_magnetic.text()
            self.obj.guideRadius = self.ui.LineEdit_radius.text()
            self.obj.longitudinalMomentum = self.ui.LineEdit_VerticalMomentum.text()
            self.obj.theHorizontalMomentum = self.ui.LineEdit_HorizontalMomentum.text()
            self.obj.isCheckX = self.ui.radioButton_AxiasX.isChecked()
            self.obj.isCheckY = self.ui.radioButton_AxiasY.isChecked()
            self.obj.launchCenterCoordinatesX = self.ui.LineEdit_LaunchX.text()
            self.obj.launchCenterCoordinatesY = self.ui.LineEdit_LaunchY.text()
            Tools2D.EmissionUiData(self.obj, self.ui).getDataFromUi()

        except:
            import traceback
            Tools2D.sayz("error:" + traceback.format_exc())
        pass


