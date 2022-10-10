# -*- coding: utf-8 -*-
import FreeCADGui
import FreeCAD
import traceback
from Model3D.Tools import Tools3D, ObjectTools
from Model3D.Command3D.Model3DCommand.BaseUI import BaseDialogMain
import CollectionOutputDialog
import PySide.QtGui as Gui
from PySide.QtCore import *
import Tkinter as ttt
import tkFileDialog as filedialog
import PySide

class ShowDialog(BaseDialogMain.BasePhysicsDialog):
    def __init__(self, obj, isNew=False, parent=None):
        BaseDialogMain.BasePhysicsDialog.__init__(self, obj, isNew, parent)

    def setUI(self):
        self.ui = CollectionOutputDialog.Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.select_path)
        self.ui.input_body.addItem("未指定")
        self.ui.path.setReadOnly(True)

    def loadDialog(self):
        """
        此处写对话框的逻辑,注意异常处理
        """
        self.refrsehCombox()

    def getInfoFromObj(self):
        """
        从obj获取数据加载到对话框、注意异常处理
        """
        try:
            self.ui.input_body.setCurrentIndex(self.ui.input_body.findText(self.obj.collectionType))
            self.ui.path.setText(self.obj.path)
        except:
            Tools3D.sayz("collectionOutPut加载数据时出现异常")
            Tools3D.sayz("error:" + traceback.format_exc())

    def setInfoToObj(self):
        """
        从对话框读取数据，设置obj的属性值
        """
        try:
            self.obj.collectionType = self.ui.input_body.currentText()
            self.obj.path = self.ui.path.text().replace(" ", "")
        except:
            Tools3D.sayz("collectionOutPut加载数据时出现异常")
            Tools3D.sayz("error:" + traceback.format_exc())

    def slotOK(self):
        if self.ui.input_body.currentText() == "未指定":
            Tools3D.sayz("收集体未指定！！！！")
            self.isKeepData = False
            self.close()
        elif self.ui.path.text() == " ":
            Tools3D.sayz("导出路径未指定！！！！")
            self.isKeepData = False
            self.close()
        else:
            self.isKeepData = True
            self.close()

    def refrsehCombox(self):
        """
        刷新下拉框
        """
        comboBox_collection_list = []
        for i in range(self.ui.input_body.count()):
            comboBox_collection_list.append(self.ui.input_body.itemText(i))
        collectionList = ObjectTools.getAllVolumes()
        for i in collectionList:
            if i not in comboBox_collection_list:
                self.ui.input_body.addItem(i)

    def select_path(self):
        path_str = ""
        dialog = Gui.QFileDialog(self)
        # dialog.setFileMode(Gui.QFileDialog.Directory)
        dialog.setFileMode(Gui.QFileDialog.AnyFile)

        if dialog.exec_():
            # 接受选中文件的路径，默认为列表
            filenames = dialog.selectedFiles()
        path_str = filenames[0]
        self.ui.path.setText(path_str)
        self.obj.path = path_str
