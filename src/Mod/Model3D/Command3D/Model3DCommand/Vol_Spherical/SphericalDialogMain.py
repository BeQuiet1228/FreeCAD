# -*- coding: utf-8 -*-
from PySide import QtGui
import FreeCAD
import Part
import FreeCADGui
from Model3D.Command3D.Model3DCommand.BaseUI import BaseDialogMain, BaseDialog
from Model3D.Tools import Tools3D
import PointWidget


class ShowPointWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = PointWidget.Ui_Form()
        self.ui.setupUi(self)


class ShowDialog(BaseDialogMain.BaseModelDialog):
    def __init__(self, obj, isNew=False, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = BaseDialog.Ui_Dialog()
        self.ui.setupUi(self)

        self.pointWidget = ShowPointWidget()
        self.setCompleter(self.pointWidget.ui)
        self.customAttribute = BaseDialogMain.CustomShowWidget()
        self.setModal(False)
        self.obj = obj
        self.ui.gridLayout_object.addWidget(self.pointWidget)
        self.initDialog()
        self.loadCommonData()
        self.loadCustomData()
        self.getInfoFromObj()
        self.isNew = isNew
        self.isKeepData = False
        Tools3D.switchPointLabel_Model(self.pointWidget.ui)

    def getInfoFromObj(self):
        self.pointWidget.ui.lineEdit_pointx.setText(str(self.obj.user_point1_x).replace(' ', ''))
        self.pointWidget.ui.lineEdit_pointy.setText(str(self.obj.user_point1_y).replace(' ', ''))
        self.pointWidget.ui.lineEdit_pointz.setText(str(self.obj.user_point1_z).replace(' ', ''))
        self.pointWidget.ui.lineEdit_radius.setText(str(self.obj.user_radius1).replace(' ', ''))

    def setInfoToObj(self):
        # self.obj.PointX = self.pointWidget.ui.lineEdit_pointx.text()
        # self.obj.PointY = self.pointWidget.ui.lineEdit_pointy.text()
        # self.obj.Radius = self.pointWidget.ui.lineEdit_radius.text()
        self.obj.user_point1_x = self.pointWidget.ui.lineEdit_pointx.text().replace(' ', '')
        self.obj.user_point1_y = self.pointWidget.ui.lineEdit_pointy.text().replace(' ', '')
        self.obj.user_point1_z = self.pointWidget.ui.lineEdit_pointz.text().replace(' ', '')
        self.obj.user_radius1 = self.pointWidget.ui.lineEdit_radius.text()
        Tools3D.setPlaceToObj(self.obj, "Point1X", self.pointWidget.ui.lineEdit_pointx.text())
        Tools3D.setPlaceToObj(self.obj, "Point1Y", self.pointWidget.ui.lineEdit_pointy.text())
        Tools3D.setPlaceToObj(self.obj, "Point1Z", self.pointWidget.ui.lineEdit_pointz.text())
        Tools3D.setPlaceToObj(self.obj, "Radius", self.pointWidget.ui.lineEdit_radius.text())
        self.obj.recompute()

    def slotOk(self):
        self.setInfoToObj()
        # 判断输入坐标是否符合模型的要求
        judge = self.judgePoint()
        if judge:
            QtGui.QMessageBox.information(None, "", "无法有效绘制圆，请检查输入数据。")
        else:
            self.isKeepData = True
            self.close()

    def judgePoint(self):
        if self.obj.Radius.Value <= 0:
            return True
        else:
            return False