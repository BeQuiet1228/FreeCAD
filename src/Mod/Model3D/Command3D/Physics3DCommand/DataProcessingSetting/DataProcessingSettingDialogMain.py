# -*- coding: utf-8 -*-
import FreeCADGui
import FreeCAD
from Model3D.Tools import Tools3D
import DataProcessingSettingDialog
from PySide import QtGui
import traceback

class ShowDialog(QtGui.QDialog):
    def __init__(self, obj, isNew=False, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = DataProcessingSettingDialog.Ui_Dialog_DataProcessingSettingDlg()
        self.ui.setupUi(self)

        self.setModal(False)
        self.obj = obj

        self.ui.pushButton_ok.clicked.connect(self.slotOK)
        self.ui.checkBox_set_prefix.clicked.connect(self.checkBox_p_clicked)
        self.ui.checkBox_set_suffix.clicked.connect(self.checkBox_s_clicked)
        self.getInfoFromObj()
        self.isNew = isNew
        self.isKeepData = False

    def getInfoFromObj(self):
        """
        从obj获取数据加载到对话框、注意异常处理
        """
        try:
            self.ui.checkBox_Time_obser.setChecked(self.obj.isCheckBox_Time_obser)
            self.ui.checkBox_space_obser.setChecked(self.obj.isCheckBox_space_obser)
            self.ui.checkBox_contor_plot.setChecked(self.obj.isCheckBox_contor_plot)
            self.ui.checkBox_vector_data.setChecked(self.obj.isCheckBox_vector_data)
            self.ui.checkBox_phase_space.setChecked(self.obj.isCheckBox_phase_space)
            self.ui.checkBox_set_prefix.setChecked(self.obj.isCheckBox_set_prefix)
            self.ui.checkBox_set_suffix.setChecked(self.obj.isCheckBox_set_suffix)
            self.ui.lineEdit_prefix.setText(str(self.obj.prefiX).replace(' ', ''))
            self.ui.lineEdit_suffix.setText(str(self.obj.suffiX).replace(' ', ''))
            self.ui.radioButton_text_format.setChecked(self.obj.isCheckBox_text)
            self.ui.radioButton_binary_format.setChecked(self.obj.isCheckBox_binary)
            self.checkBox_p_clicked()
            self.checkBox_s_clicked()
        except:
            import traceback
            Tools3D.sayz("error:" + traceback.format_exc())

    def setInfoToObj(self):
        """
        从对话框读取数据，设置obj的属性值
        """
        try:
            self.obj.isCheckBox_Time_obser = self.ui.checkBox_Time_obser.isChecked()
            self.obj.isCheckBox_space_obser = self.ui.checkBox_space_obser.isChecked()
            self.obj.isCheckBox_contor_plot = self.ui.checkBox_contor_plot.isChecked()
            self.obj.isCheckBox_vector_data = self.ui.checkBox_vector_data.isChecked()
            self.obj.isCheckBox_phase_space = self.ui.checkBox_phase_space.isChecked()
            self.obj.isCheckBox_set_prefix = self.ui.checkBox_set_prefix.isChecked()
            self.obj.isCheckBox_set_suffix = self.ui.checkBox_set_suffix.isChecked()
            self.obj.prefiX = self.ui.lineEdit_prefix.text()
            self.obj.suffiX = self.ui.lineEdit_suffix.text()
            self.obj.isCheckBox_text = self.ui.radioButton_text_format.isChecked()
            self.obj.isCheckBox_binary = self.ui.radioButton_binary_format.isChecked()


        except:
            import traceback
            Tools3D.sayz("error:" + traceback.format_exc())

    def checkBox_p_clicked(self):
        self.ui.lineEdit_prefix.setEnabled(self.ui.checkBox_set_prefix.isChecked())

    def checkBox_s_clicked(self):
        self.ui.lineEdit_suffix.setEnabled(self.ui.checkBox_set_suffix.isChecked())

    def slotOK(self):
        # self.keepData()
        self.isKeepData = True
        self.close()


    def closeEvent(self, event):
        if self.isKeepData:
            try:
                self.setInfoToObj()
                FreeCADGui.runCommand("CreateM3D_new")
            except AttributeError:
                Tools3D.sayz("--异常--在读取Object属性时出现异常")
                Tools3D.sayz(traceback.format_exc())
            except Exception as e:
                Tools3D.sayz("--" + str(e))
            else:
                FreeCAD.Console.PrintMessage("设置Object信息\n")
        else:
            if self.isNew:
                FreeCAD.ActiveDocument.removeObject(self.obj.Label)