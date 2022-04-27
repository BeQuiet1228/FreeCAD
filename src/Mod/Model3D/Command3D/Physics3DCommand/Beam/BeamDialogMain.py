# -*- coding: utf-8 -*-
from Model3D.Tools import Tools3D, ObjectTools
from Model3D.Command3D.Model3DCommand.BaseUI import BaseDialogMain
import BeamDialog


class ShowDialog(BaseDialogMain.BaseEmitDialog):
    def __init__(self, obj, isNew=False, parent=None):
        BaseDialogMain.BaseEmitDialog.__init__(self, obj, isNew, parent)

    def setUI(self):
        self.ui = BeamDialog.Ui_Dialog_EmbDlg()
        self.ui.setupUi(self)

    def privateDialog(self):
        # 获取当前坐标系及坐标系单位
        coord = Tools3D.getCoordinate()
        self.x = coord[0]
        self.y = coord[1]
        self.z = coord[2]
        # 根据坐标系初始化面板
        self.ui.label.setText(u"束电流密度BeamJ(T," + self.x + "," + self.y + "," + self.z +")= ")
        self.ui.label_3.setText(u"束电压参量BeamV(T," + self.x + "," + self.y + "," + self.z +")= ")

    def loadPrivateData(self):
        try:
            self.ui.textEdit_BeamJ.setText(self.obj.beamCurrentDensity)
            self.ui.textEdit_BeamV.setText(self.obj.beamVoltageDensity)
        except KeyError as reason:
            Tools3D.sayz("!!!Error:KeyError,Maybe lack of key:%s" % str(reason))

    def setPrivateInfoToObj(self):
        self.obj.beamCurrentDensity = self.ui.textEdit_BeamJ.toPlainText()
        self.obj.beamVoltageDensity = self.ui.textEdit_BeamV.toPlainText()
