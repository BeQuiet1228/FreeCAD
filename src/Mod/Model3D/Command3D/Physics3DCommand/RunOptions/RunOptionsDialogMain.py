# -*- coding: utf-8 -*-
import FreeCADGui
import FreeCAD
from Model3D.Tools import Tools3D,ObjectTools
from Model3D.Command3D.Model3DCommand.BaseUI import BaseDialogMain
import RunOptionsDialog
from PySide import QtGui
import traceback

class ShowDialog(QtGui.QDialog):
    def __init__(self, obj, isNew=False, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = RunOptionsDialog.Ui_Dialog_RunOptionsDlg()
        self.ui.setupUi(self)

        self.setModal(False)
        self.obj = obj

        self.ui.pushButton_ok.clicked.connect(self.slotOK)
        self.getInfoFromObj()
        self.isNew = isNew
        self.isKeepData = False


    def getInfoFromObj(self):
        """
        从obj获取数据加载到对话框、注意异常处理
        """
        try:
            self.ui.checkBox_show_structureChart.setChecked(self.obj.isCheckBox_show_structureChart)
            self.ui.checkBox_paused_when_start.setChecked(self.obj.isCheckBox_paused_when_start)
        except:
            import traceback
            Tools3D.sayz("error:" + traceback.format_exc())

    def setInfoToObj(self):
        """
        从对话框读取数据，设置obj的属性值
        """
        try:
            self.obj.isCheckBox_paused_when_start = self.ui.checkBox_paused_when_start.isChecked()
            self.obj.isCheckBox_show_structureChart = self.ui.checkBox_show_structureChart.isChecked()

        except:
            import traceback
            Tools3D.sayz("error:" + traceback.format_exc())

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