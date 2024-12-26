# -*- coding: utf-8 -*-
from PySide import QtGui
import FreeCAD
import Part
import FreeCADGui
from Model3D.Command3D.Model3DCommand.BaseUI import BaseDialogMain, BaseDialog
from Model3D.Tools import Tools3D
import Vol_STLWidget
import sys
from PySide.QtGui import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QMessageBox



class ShowVol_STLWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Vol_STLWidget.Ui_Form()
        self.ui.setupUi(self)


class ShowDialog(BaseDialogMain.BaseModelDialog):
    def __init__(self, obj, isNew=False, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = BaseDialog.Ui_Dialog()
        self.ui.setupUi(self)

        self.Vol_STLWidget = ShowVol_STLWidget()
        self.setCompleter(self.Vol_STLWidget.ui)
        self.customAttribute = BaseDialogMain.CustomShowWidget()
        self.setModal(False)
        self.obj = obj
        self.ui.gridLayout_object.addWidget(self.Vol_STLWidget)
        self.initDialog()
        self.loadCommonData()
        self.loadCustomData()
        self.getInfoFromObj()
        self.isNew = isNew
        self.isKeepData = False
        self.Vol_STLWidget.ui.pushButton.clicked.connect(self.select_file)
        # Tools3D.switchPointLabel_Model(self.Vol_STLWidget.ui)
        
    def select_file(self):
        # 打开文件选择对话框
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "选择一个 STL 文件", 
            self.obj.FilePath, 
            "STL 文件 (*.stl);;所有文件 (*)"
        )
        
        # 检查是否选择了文件
        if file_path:
            self.Vol_STLWidget.ui.lineEdit.setText(file_path)
        else:
            QMessageBox.warning(self, "警告", "未选择任何文件！")

    def getInfoFromObj(self):
        self.Vol_STLWidget.ui.lineEdit.setText(self.obj.FilePath)
        pass
        # self.Vol_STLWidget.ui.lineEdit_point1x.setText(str(self.obj.user_point1_x).replace(' ', ''))
        # self.Vol_STLWidget.ui.lineEdit_point1y.setText(str(self.obj.user_point1_y).replace(' ', ''))
        # self.Vol_STLWidget.ui.lineEdit_point1z.setText(str(self.obj.user_point1_z).replace(' ', ''))

    def setInfoToObj(self):
        self.obj.FilePath = self.Vol_STLWidget.ui.lineEdit.text()
        self.obj.recompute()
        pass 
        # self.obj.user_point1_x = self.Vol_STLWidget.ui.lineEdit_point1x.text().replace(' ', '')
        # self.obj.user_point1_y = self.Vol_STLWidget.ui.lineEdit_point1y.text().replace(' ', '')
        # self.obj.user_point1_z = self.Vol_STLWidget.ui.lineEdit_point1z.text().replace(' ', '')
        # Tools3D.setPlaceToObj(self.obj, "Point1X", self.Vol_STLWidget.ui.lineEdit_point1x.text())
        # Tools3D.setPlaceToObj(self.obj, "Point1Y", self.Vol_STLWidget.ui.lineEdit_point1y.text())
        # Tools3D.setPlaceToObj(self.obj, "Point1Z", self.Vol_STLWidget.ui.lineEdit_point1z.text())
        # self.obj.recompute()
