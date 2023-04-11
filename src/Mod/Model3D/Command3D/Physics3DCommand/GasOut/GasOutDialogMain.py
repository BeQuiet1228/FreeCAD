# -*- coding: utf-8 -*-
from PySide import QtGui
import GasOutDialog
from Model3D.Tools import Tools3D, ObjectTools
from Model3D.Command3D.Model3DCommand.BaseUI import BaseDialogMain


class ShowDialog(BaseDialogMain.BasePhysicsDialog):
    def __init__(self, obj, isNew=False, parent=None):
        BaseDialogMain.BasePhysicsDialog.__init__(self, obj, isNew, parent)

    def setUI(self):
        self.ui = GasOutDialog.Ui_Dialog_GasOutDlg()
        self.ui.setupUi(self)

    def loadDialog(self):
        try:
            self.refreshCombox()
        except:
            Tools3D.sayz("error!123")

    def refreshCombox(self):
        """
        每次加载窗口时都要重新刷新下拉框，以实现动态加载
        一般来说就是ComboBox_Shodow_list需要动态刷新
        """
        ComboBox_Shadow_list = []
        for i in range(self.ui.ComboBox_Vol.count()):
            ComboBox_Shadow_list.append(self.ui.ComboBox_Vol.itemText(i))

        EmmiterList = ObjectTools.getAllVolumes()
        for i in EmmiterList:
            if i not in ComboBox_Shadow_list:
                self.ui.ComboBox_Vol.addItem(i)

    def getInfoFromObj(self):
        try:
            self.ui.LineEdit_Name.setText(self.obj.Label)

            # 根据选择的具体obj设置Dialog
            self.ui.ComboBox_Vol.setCurrentIndex(self.ui.ComboBox_Vol.findText(str(self.obj.absorbVol)))
            self.ui.ComboBox_Current.setCurrentIndex(self.ui.ComboBox_Current.findText(str(self.obj.normal)))

            self.ui.LineEdit_density.setText(self.obj.density)
            self.ui.LineEdit_area.setText(self.obj.area)
            self.ui.LineEdit_threshold.setText(self.obj.threshold)
            self.ui.LineEdit_grid.setText(self.obj.grid)

            # 正向反向
            self.ui.radioButton_opposite.setChecked(self.obj.isNegative)
            self.ui.radioButton_forward.setChecked(self.obj.isPositive)

        except:
            import traceback
            Tools3D.sayz("error:" + traceback.format_exc())

    def setInfoToObj(self):
        try:
            self.obj.Label = Tools3D.setLabel(self.ui.LineEdit_Name.text())
            self.obj.normal = self.ui.ComboBox_Current.currentText()
            self.obj.absorbVol = self.ui.ComboBox_Vol.currentText()

            self.obj.density = self.ui.LineEdit_density.text()
            self.obj.area = self.ui.LineEdit_area.text()
            self.obj.threshold = self.ui.LineEdit_threshold.text()
            self.obj.grid = self.ui.LineEdit_grid.text()

            # 正向反向选择
            self.obj.isNegative = self.ui.radioButton_opposite.isChecked()
            self.obj.isPositive = self.ui.radioButton_forward.isChecked()
        except:
            import traceback
            Tools3D.sayz("error:" + traceback.format_exc())


    def slotOK(self):
        self.setInfoToObj()
        if self.obj.absorbVol == '未指定' or self.obj.absorbVol == u'未指定':
            QtGui.QMessageBox.information(None, "", "请正确选择解吸附体！")
        else:
            self.isKeepData = True
            self.close()
