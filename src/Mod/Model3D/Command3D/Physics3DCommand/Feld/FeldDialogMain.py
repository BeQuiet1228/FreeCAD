# -*- coding: utf-8 -*-
from Model3D.Tools import Tools3D
from Model3D.Command3D.Model3DCommand.BaseUI import BaseDialogMain
import FeldDialog


class ShowDialog(BaseDialogMain.BaseEmitDialog):
    def __init__(self, obj, isNew=False, parent=None):
        BaseDialogMain.BaseEmitDialog.__init__(self, obj, isNew, parent)

    def setUI(self):
        self.ui = FeldDialog.Ui_Dialog_EmhDlg()
        self.ui.setupUi(self)

    def privateDialog(self):
        coord = Tools3D.getCoordinate()
        self.x = coord[0]
        self.y = coord[1]
        self.z = coord[2]
        # 根据坐标系初始化面板
        self.ui.label_10.setText(u"工作函数.PHI(T," + self.x + "," + self.y + "," + self.z + ")= ")

    def loadPrivateData(self):
        try:
            self.ui.LineEdit_FNA.setText(self.obj.constantA)
            self.ui.LineEdit_FNB.setText(self.obj.constantB)
            self.ui.LineEdit_PHI.setText(self.obj.workingFunctionPHI)
        except KeyError as reason:
            Tools3D.sayz("!!!Error:KeyError,Maybe lack of key:%s" % str(reason))

    def setPrivateInfoToObj(self):
        self.obj.constantA = self.ui.LineEdit_FNA.text()
        self.obj.constantB = self.ui.LineEdit_FNB.text()
        self.obj.workingFunctionPHI = self.ui.LineEdit_PHI.text()