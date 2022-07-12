# -*- coding: utf-8 -*-
from Model3D.Tools import Tools3D
from Model3D.Command3D.Model3DCommand.BaseUI import BaseDialogMain
import GyroDialog
import traceback


class ShowDialog(BaseDialogMain.BaseEmitDialog):
    def __init__(self, obj, isNew=False, parent=None):
        BaseDialogMain.BaseEmitDialog.__init__(self, obj, isNew, parent)

    def setUI(self):
        self.ui = GyroDialog.Ui_Dialog_EmgDlg()
        self.ui.setupUi(self)

    def privateDialog(self):
        self.ui.isCheckvelocity.clicked.connect(self.isCheckvelocity_clicked)
        # 获取当前坐标系及坐标系单位
        coord = Tools3D.getCoordinate()
        self.x = coord[0]
        self.y = coord[1]
        self.z = coord[2]
        # 根据坐标系初始化面板
        self.ui.radioButton_AxiasX.setText(self.x)
        self.ui.radioButton_AxiasY.setText(self.y)
        self.ui.radioButton_AxiasZ.setText(self.z)

    def isCheckvelocity_clicked(self):
        self.ui.lineEdit_velocity.setEnabled(self.ui.isCheckvelocity.isChecked())

    def loadPrivateData(self):
        try:
            self.ui.LineEdit_IT.setText(self.obj.beamCurrent)
            self.ui.LineEdit_magnetic.setText(self.obj.guidingMagneticField)
            self.ui.LineEdit_radius.setText(self.obj.guideRadius)
            self.ui.LineEdit_VerticalMomentum.setText(self.obj.longitudinalMomentum)
            self.ui.LineEdit_HorizontalMomentum.setText(self.obj.theHorizontalMomentum)
            self.ui.radioButton_AxiasX.setChecked(self.obj.isCheckX)
            self.ui.radioButton_AxiasY.setChecked(self.obj.isCheckY)
            self.ui.radioButton_AxiasZ.setChecked(self.obj.isCheckZ)
            self.ui.LineEdit_LaunchX.setText(self.obj.launchCenterCoordinatesX)
            self.ui.LineEdit_LaunchY.setText(self.obj.launchCenterCoordinatesY)
            self.ui.LineEdit_LaunchZ.setText(self.obj.launchCenterCoordinatesZ)

            self.ui.isCheckvelocity.setChecked(self.obj.isVelocityDistribution)
            self.ui.lineEdit_velocity.setText(self.obj.velocityDistribution)
            self.isCheckvelocity_clicked()

        except:
            Tools3D.sayz("error:" + traceback.format_exc())

    def setPrivateInfoToObj(self):
        self.obj.beamCurrent = self.ui.LineEdit_IT.text()
        self.obj.guidingMagneticField = self.ui.LineEdit_magnetic.text()
        self.obj.guideRadius = self.ui.LineEdit_radius.text()
        self.obj.longitudinalMomentum = self.ui.LineEdit_VerticalMomentum.text()
        self.obj.theHorizontalMomentum = self.ui.LineEdit_HorizontalMomentum.text()
        self.obj.isCheckX = self.ui.radioButton_AxiasX.isChecked()
        self.obj.isCheckY = self.ui.radioButton_AxiasY.isChecked()
        self.obj.isCheckZ = self.ui.radioButton_AxiasZ.isChecked()
        self.obj.launchCenterCoordinatesX = self.ui.LineEdit_LaunchX.text()
        self.obj.launchCenterCoordinatesY = self.ui.LineEdit_LaunchY.text()
        self.obj.launchCenterCoordinatesZ = self.ui.LineEdit_LaunchZ.text()
        self.obj.velocityDistribution = self.ui.lineEdit_velocity.text()
        self.obj.isVelocityDistribution = self.ui.isCheckvelocity.isChecked()
