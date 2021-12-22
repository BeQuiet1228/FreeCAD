# -*- coding: utf-8 -*-
import traceback

import FreeCAD
from PySide import QtGui

from Modeling.Modeling2D.Modeling2DCommand.NewMaterial import NewMaterialDialog
from Modeling.Modeling2D.Tools import Tools2D
from Modeling.Modeling2D.Modeling2DCommand.BaseUI import BaseDialog


class ShowDialog(BaseDialog.BaseOtherDialog):
    def __init__(self, obj, isNew=False, parent=None):
        BaseDialog.BaseOtherDialog.__init__(self, obj, isNew, parent)

    def setUI(self):
        self.ui = NewMaterialDialog.Ui_Dialog_NewMaterialDlg()
        self.ui.setupUi(self)
        self.setModal(False)

    def helperInitDialog(self):
        self.loadData()
        self.onCheckBox_conductivityClicked()
        self.onCheckBox_dielectric_constantClicked()
        # 信号与槽
        self.ui.checkBox_conductivity.clicked.connect(self.onCheckBox_conductivityClicked)
        self.ui.checkBox_dielectric_constant.clicked.connect(self.onCheckBox_dielectric_constantClicked)

    def helperOK(self):
        self.isKeepData = True
        self.close()

    def helperCancel(self):
        self.isKeepData = False
        self.close()

    def loadData(self):
        try:
            self.ui.le_name.setText(self.obj.Label)
            self.ui.le_atomic_number.setText(self.obj.AtomicNumber)
            self.ui.le_atomic_mass_number.setText(self.obj.AtomicMassNumber)
            self.ui.le_atomic_desity.setText(self.obj.MaterialDensity)
            self.ui.le_conductivity.setText(self.obj.conductivity)
            self.ui.le_dielectric_constant.setText(self.obj.dielectricConstant)
            self.ui.checkBox_conductivity.setChecked(self.obj.isConductivity)
            self.ui.checkBox_dielectric_constant.setChecked(self.obj.isDielectricConstant)
        except:
            Tools2D.sayz("NewMaterial加载数据时出现异常")
            Tools2D.sayz(traceback.format_exc())

    def keepData(self):
        try:
            Tools2D.setLabelToObj(self.obj, self.ui.le_name.text())
            self.obj.AtomicNumber = self.ui.le_atomic_number.text().replace(" ", "")
            self.obj.AtomicMassNumber = self.ui.le_atomic_mass_number.text().replace(" ", "")
            self.obj.MaterialDensity = self.ui.le_atomic_desity.text().replace(" ", "")
            self.obj.conductivity = self.ui.le_conductivity.text().replace(" ", "")
            self.obj.dielectricConstant = self.ui.le_dielectric_constant.text().replace(" ", "")
            self.obj.isConductivity = self.ui.checkBox_conductivity.isChecked()
            self.obj.isDielectricConstant = self.ui.checkBox_dielectric_constant.isChecked()
        except:
            Tools2D.sayz("NewMaterial写入数据时出现异常")
            Tools2D.sayz(traceback.format_exc())

    def onCheckBox_conductivityClicked(self):
        self.ui.le_conductivity.setEnabled(self.ui.checkBox_conductivity.isChecked())

    def onCheckBox_dielectric_constantClicked(self):
        self.ui.le_dielectric_constant.setEnabled(self.ui.checkBox_dielectric_constant.isChecked())
