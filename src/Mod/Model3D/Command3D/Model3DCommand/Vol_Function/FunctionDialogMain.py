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
        self.pointWidget.ui.lineEdit_point1x.setText(str(self.obj.user_point1_x).replace(' ', ''))
        self.pointWidget.ui.lineEdit_point1y.setText(str(self.obj.user_point1_y).replace(' ', ''))
        self.pointWidget.ui.lineEdit_point1z.setText(str(self.obj.user_point1_z).replace(' ', ''))
        self.pointWidget.ui.lineEdit_point2x.setText(str(self.obj.user_point2_x).replace(' ', ''))
        self.pointWidget.ui.lineEdit_point2y.setText(str(self.obj.user_point2_y).replace(' ', ''))
        self.pointWidget.ui.lineEdit_point2z.setText(str(self.obj.user_point2_z).replace(' ', ''))
        self.pointWidget.ui.textEdit_expression.setText(str(self.obj.Expression).replace(' ', ''))
        self.pointWidget.ui.spinBox_x.setValue(self.obj.precision_x)
        self.pointWidget.ui.spinBox_y.setValue(self.obj.precision_y)
        self.pointWidget.ui.spinBox_z.setValue(self.obj.precision_z)

    def setInfoToObj(self):
        self.obj.user_point1_x = self.pointWidget.ui.lineEdit_point1x.text().replace(' ', '')
        self.obj.user_point1_y = self.pointWidget.ui.lineEdit_point1y.text().replace(' ', '')
        self.obj.user_point1_z = self.pointWidget.ui.lineEdit_point1z.text().replace(' ', '')
        self.obj.user_point2_x = self.pointWidget.ui.lineEdit_point2x.text().replace(' ', '')
        self.obj.user_point2_y = self.pointWidget.ui.lineEdit_point2y.text().replace(' ', '')
        self.obj.user_point2_z = self.pointWidget.ui.lineEdit_point2z.text().replace(' ', '')
        Tools3D.setPlaceToObj(self.obj, "Point2Y", self.pointWidget.ui.lineEdit_point2y.text())
        Tools3D.setPlaceToObj(self.obj, "Point1X", self.pointWidget.ui.lineEdit_point1x.text())
        Tools3D.setPlaceToObj(self.obj, "Point1Y", self.pointWidget.ui.lineEdit_point1y.text())
        Tools3D.setPlaceToObj(self.obj, "Point1Z", self.pointWidget.ui.lineEdit_point1z.text())
        Tools3D.setPlaceToObj(self.obj, "Point2X", self.pointWidget.ui.lineEdit_point2x.text())
        Tools3D.setPlaceToObj(self.obj, "Point2Z", self.pointWidget.ui.lineEdit_point2z.text())
        self.obj.Expression = self.pointWidget.ui.textEdit_expression.toPlainText()
        self.obj.precision_x = self.pointWidget.ui.spinBox_x.value()
        self.obj.precision_y = self.pointWidget.ui.spinBox_y.value()
        self.obj.precision_z = self.pointWidget.ui.spinBox_z.value()
        self.obj.recompute()
