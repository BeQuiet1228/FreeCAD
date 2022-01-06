# -*- coding: utf-8 -*-
from PySide import QtGui
import FreeCAD
from Model3D.Tools import ObjectTools
import FreeCADGui
from Model3D.Command3D.Model3DCommand.BaseUI import BaseDialogMain, BaseDialog
import ExtrudedWidget

class ShowPointWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = ExtrudedWidget.Ui_Form()
        self.ui.setupUi(self)


class ShowDialog(BaseDialogMain.BaseModelDialog):
    def __init__(self, obj, isNew=False, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = BaseDialog.Ui_Dialog()
        self.ui.setupUi(self)

        self.pointWidget = ShowPointWidget()
        self.customAttribute = BaseDialogMain.CustomShowWidget()
        self.setModal(False)
        self.obj = obj
        self.ui.gridLayout_object.addWidget(self.pointWidget)
        self.initDialog()
        # 刷新下拉框
        self.reComboBox()
        self.loadCommonData()
        self.loadCustomData()
        self.getInfoFromObj()
        self.isNew = isNew
        self.isKeepData = False

    def getInfoFromObj(self):
        self.pointWidget.ui.comboBox_Area.setCurrentIndex(self.pointWidget.ui.comboBox_Area.findText(str(self.obj.Area)))
        self.pointWidget.ui.comboBox_Line.setCurrentIndex(self.pointWidget.ui.comboBox_Line.findText(str(self.obj.Line)))

    def setInfoToObj(self):
        self.obj.Area = self.pointWidget.ui.comboBox_Area.currentText()
        self.obj.Line = self.pointWidget.ui.comboBox_Line.currentText()
        self.obj.recompute()

    def reComboBox(self):
        areas = ObjectTools.getAllAreas()
        for areaItem in areas:
            self.pointWidget.ui.comboBox_Area.addItem(areaItem)
        lines = ObjectTools.getAllLines()
        for lineItem in lines:
            self.pointWidget.ui.comboBox_Line.addItem(lineItem)

    def slotOk(self):
        self.setInfoToObj()
        # 判断输入坐标是否符合模型的要求
        judge = self.judgePoint()
        if judge:
            QtGui.QMessageBox.information(None, "", "无法有效绘制挤出体，请检查输入数据。")
        else:
            self.isKeepData = True
            self.close()

    def judgePoint(self):
        objLine = FreeCAD.ActiveDocument.getObjectsByLabel(self.obj.Line)[0]
        objArea = FreeCAD.ActiveDocument.getObjectsByLabel(self.obj.Area)[0]
        if objLine is None or objArea is None:
            return True
        else:
            return False
