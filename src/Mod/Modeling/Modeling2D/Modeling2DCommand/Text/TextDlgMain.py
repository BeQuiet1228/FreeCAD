# -*- coding: utf-8 -*-
import traceback

from PySide import QtGui, QtCore
from Modeling.Modeling2D.Tools import Tools2D
import FreeCAD
import TextDialog
from Modeling.Modeling2D.Tools.InitDoc import addObjectToGroup_helper


class ShowDialog(QtGui.QDialog):
    def __init__(self, obj, isNew=False, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = TextDialog.Ui_Dialog()
        self.ui.setupUi(self)

        self.setModal(False)
        self.obj = obj
        self.isNew = isNew
        self.initDialog()
        self.loadData()
        self.isKeepData = False

    def initDialog(self):
        try:
            # 绑定信号与槽
            self.ui.pb_ok.clicked.connect(self.slotOK)
            self.ui.pb_cancel.clicked.connect(self.slotCancel)
            # 获取当前坐标系及坐标系单位
            coord = Tools2D.getCoordinate()
            self.x = coord[0]
            self.y = coord[1]
            # 根据坐标系更新面板
            self.ui.label_x.setText(self.x)
            self.ui.label_y.setText(self.y)
        except:
            Tools2D.sayz("error:" + traceback.format_exc())

    def slotOK(self):
        try:
            if self.checkChinese():
                return
            addObjectToGroup_helper(self.obj, "AnnotationG", "注释")
            self.isKeepData = True
            self.close()
        except:
            self.close()
            Tools2D.sayz("error:" + traceback.format_exc())

    def slotCancel(self):
        self.isKeepData = False
        self.close()

    def loadData(self):
        try:
            # label
            self.ui.le_name.setText(self.obj.Label)
            # 坐标
            self.ui.point1_x.setValue(self.obj.Position[0])
            self.ui.point1_y.setValue(self.obj.Position[1])
            # annotation
            annotation = self.obj.LabelText
            for i in annotation:
                self.ui.te_annotation.append(i)
        except:
            Tools2D.sayz(traceback.format_exc())

    def keepData(self):
        try:
            Tools2D.setLabelToObj(self.obj, self.ui.le_name.text())
            pos = FreeCAD.Vector(self.ui.point1_x.value(), self.ui.point1_y.value(), 0)
            self.obj.Position = pos
            textList = self.ui.te_annotation.toPlainText().split("\n")
            self.obj.LabelText = textList
            # 设置字体大小
            self.setTheFontSize()
        except:
            import traceback
            Tools2D.sayz("error:" + traceback.format_exc())

    @staticmethod
    def check_contain_chinese(check_str):
        for ch in check_str.decode('utf-8'):
            if u'\u4e00' <= ch <= u'\u9fff':
                return True
        return False

    def checkChinese(self):
        text = self.ui.te_annotation.toPlainText()
        if self.check_contain_chinese(text):
            report = QtGui.QMessageBox()
            report.setText(u'目前注释暂不支持中文')
            report.exec_()
            return True
        return False

    def setTheFontSize(self):
        """
        设置字体大小以及行间距
        """
        # 根据网格调整大小
        # 根据网格大小调整
        gridObj = FreeCAD.ActiveDocument.DiyGrid
        gridSize = min(gridObj.gridSizeX, gridObj.gridSizeY)
        self.obj.ViewObject.FontSize = gridSize/(2.0*100)
        self.obj.ViewObject.LineSpacing = 1

    # 点击关闭对话框，删除创建的对象
    def closeEvent(self, event):
        if self.isKeepData:
            self.keepData()
        else:
            if self.isNew:
                FreeCAD.ActiveDocument.removeObject(self.obj.Label)

