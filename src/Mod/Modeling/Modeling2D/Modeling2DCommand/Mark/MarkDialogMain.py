#-*- coding: utf-8 -*-
import MarkDialog
from PySide import QtGui
import FreeCAD
import FreeCADGui
from Modeling.Modeling2D.Tools import Tools2D


class ShowDialog(QtGui.QDialog):
    def __init__(self, obj, isNew=False, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = MarkDialog.Ui_Dialog()
        self.ui.setupUi(self)
        self.obj = obj
        self.isNew = isNew
        self.initDialog()
        self.loadData()
        self.isKeepData = False

    def initDialog(self):
        try:
            self.ui.pb_cancel.clicked.connect(self.onCancel)
            self.ui.pb_ok.clicked.connect(self.onConfirm)
            self.refreshCombox()
        except:
            import traceback
            Tools2D.sayz("error:" + traceback.format_exc())

    def onCancel(self):
        self.isKeepData = False
        self.close()

    # 点击确定按钮
    def onConfirm(self):
        self.isKeepData = True
        self.close()

    def loadData(self):
        try:
            # self.userNameBefore = self.obj.Label
            # # Mark对象
            self.ui.comboBox_obj.setCurrentIndex(self.ui.comboBox_obj.findText(str(self.obj.markObject)))
            # Mark方向
            self.ui.comboBox_x.setCurrentIndex(self.ui.comboBox_x.findText(str(self.obj.direction)))
            # Mark位置
            self.ui.checkBox_min.setChecked(self.obj.isMINIMUM)
            self.ui.checkBox_mid.setChecked(self.obj.isMIDPOINT)
            self.ui.checkBox_max.setChecked(self.obj.isMAXIMUM)
            # Mark大小
            self.ui.lineEdit_size.setText(self.obj.size)

        except KeyError as reason:
            Tools2D.sayz("!!!Error:KeyError,Maybe lack of key:%s"%str(reason))

    def keepData(self):
        try:
            # Mark对象
            self.obj.markObject = self.ui.comboBox_obj.currentText()
            # Mark方向
            self.obj.direction = self.ui.comboBox_x.currentText()
            # Mark位置
            self.obj.isMINIMUM = self.ui.checkBox_min.isChecked()
            self.obj.isMIDPOINT = self.ui.checkBox_mid.isChecked()
            self.obj.isMAXIMUM = self.ui.checkBox_max.isChecked()
            # Mark大小
            self.obj.size = self.ui.lineEdit_size.text()

        except:
            import traceback
            Tools2D.sayz("error:" + traceback.format_exc())
        pass

    def refreshCombox(self):  
        '''
        每次加载窗口时都要重新加载下拉列表，以实现动态加载
        一般来说就是ComboBox_Shadow_list需要动态刷新
        '''
        ComboBox_list=[]
        MarkObj = []
        for i in range(self.ui.comboBox_obj.count()):
            ComboBox_list.append(self.ui.comboBox_obj.itemText(i))
        MarkList = Tools2D.getAllObjects()
        for i in MarkList:
            if hasattr(i, "Order"):
                MarkObj.append(i.Label)
        for i in MarkObj:
            if i not in ComboBox_list:
                self.ui.comboBox_obj.addItem(i)

    # 点击关闭对话框，删除创建的对象
    def closeEvent(self, event):
        if self.isKeepData:
            self.keepData()
            FreeCADGui.runCommand("CreateM2D")
        else:
            if self.isNew:
                FreeCAD.ActiveDocument.removeObject(self.obj.Label)

