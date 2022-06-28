# -*- coding: utf-8 -*-
import traceback
from Model3D.Tools import Tools3D
from Model3D.Command3D.Model3DCommand.BaseUI import BaseDialogMain
import NewMaterialDialog


class ShowDialog(BaseDialogMain.BasePhysicsDialog):
    def __init__(self, obj, isNew=False, parent=None):
        BaseDialogMain.BasePhysicsDialog.__init__(self, obj, isNew, parent)

    def setUI(self):
        self.ui = NewMaterialDialog.Ui_Dialog_NewMaterialDlg()
        self.ui.setupUi(self)

    def loadDialog(self):
        """
        此处写对话框的逻辑,注意异常处理
        """
        try:
            self.ischeck_conductivityClicked()
            self.ischeck_dirlectricClicked()
            self.ui.checkBox_conductivity.clicked.connect(self.ischeck_conductivityClicked)
            self.ui.checkBox_dielectric_constant.clicked.connect(self.ischeck_dirlectricClicked)
        except:
            Tools3D.sayz("NewMaterial加载数据时出现异常")
            Tools3D.sayz("error:" + traceback.format_exc())

    def getInfoFromObj(self):
        """
        从obj获取数据加载到对话框、注意异常处理
        """
        try:
            self.ui.LineEdit_Name.setText(self.obj.Label)
            self.ui.LineEdit_atomic_number.setText(self.obj.atomicNumber)
            self.ui.LineEdit_atomic_mass_number.setText(self.obj.atomicMassNumber)
            self.ui.LineEdit_atomic_desity.setText(self.obj.atomicDesity)
            self.ui.LineEdit_conductivity.setText(self.obj.conductivity)
            self.ui.LineEdit_dielectric_constant.setText(self.obj.dielectricConstant)
            self.ui.checkBox_conductivity.setChecked(self.obj.isconductivity)
            self.ui.checkBox_dielectric_constant.setChecked(self.obj.isdielectricConstant)
            self.ischeck_conductivityClicked()
            self.ischeck_dirlectricClicked()
        except:
            Tools3D.sayz("NewMaterial加载数据时出现异常")
            Tools3D.sayz("error:" + traceback.format_exc())

    def setInfoToObj(self):
        """
        从对话框读取数据，设置obj的属性值
        """
        try:
            self.obj.Label = Tools3D.setLabel(self.ui.LineEdit_Name.text())
            self.obj.atomicNumber = self.ui.LineEdit_atomic_number.text().replace(" ", "")
            self.obj.atomicMassNumber = self.ui.LineEdit_atomic_mass_number.text().replace(" ", "")
            self.obj.atomicDesity = self.ui.LineEdit_atomic_desity.text().replace(" ", "")
            self.obj.conductivity = self.ui.LineEdit_conductivity.text().replace(" ", "")
            self.obj.dielectricConstant = self.ui.LineEdit_dielectric_constant.text().replace(" ", "")
            self.obj.isconductivity = self.ui.checkBox_conductivity.isChecked()
            self.obj.isdielectricConstant = self.ui.checkBox_dielectric_constant.isChecked()
        except:
            Tools3D.sayz("NewMaterial加载数据时出现异常")
            Tools3D.sayz("error:" + traceback.format_exc())

    def ischeck_conductivityClicked(self):
        self.ui.LineEdit_conductivity.setEnabled(self.ui.checkBox_conductivity.isChecked())

    def ischeck_dirlectricClicked(self):
        self.ui.LineEdit_dielectric_constant.setEnabled(self.ui.checkBox_dielectric_constant.isChecked())





