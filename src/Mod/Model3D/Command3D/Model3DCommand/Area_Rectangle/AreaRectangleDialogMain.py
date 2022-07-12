# -*- coding: utf-8 -*-
from PySide import QtGui
import FreeCAD
import Part
import FreeCADGui
from Model3D.Command3D.Model3DCommand.BaseUI import BaseDialogMain, BaseDialog
from Model3D.Tools import Tools3D
import PointWidget


coord = {"Rectangular": ["X", "Y", "Z"],
         "Polar": ["Z", "R", "Theta"],
         "Cylinder": ["Z", "Theta", "R"]}


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
        self.DirChoose()
        self.SoltNormal()

    def getInfoFromObj(self):
        self.pointWidget.ui.comboBox_dir.setCurrentIndex(self.pointWidget.ui.comboBox_dir.findText(str(self.obj.Normal)))
        self.pointWidget.ui.lineEdit_point1x.setText(str(self.obj.user_point1_x).replace(' ', ''))
        self.pointWidget.ui.lineEdit_point1y.setText(str(self.obj.user_point1_y).replace(' ', ''))
        self.pointWidget.ui.lineEdit_point1z.setText(str(self.obj.user_point1_z).replace(' ', ''))
        self.pointWidget.ui.lineEdit_point2x.setText(str(self.obj.user_point2_x).replace(' ', ''))
        self.pointWidget.ui.lineEdit_point2y.setText(str(self.obj.user_point2_y).replace(' ', ''))
        self.pointWidget.ui.lineEdit_point2z.setText(str(self.obj.user_point2_z).replace(' ', ''))

    def setInfoToObj(self):
        self.obj.Normal = self.pointWidget.ui.comboBox_dir.currentText()
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
        self.obj.recompute()

    def DirChoose(self):
        self.pointWidget.ui.comboBox_dir.currentIndexChanged.connect(self.SoltNormal)
        self.pointWidget.ui.lineEdit_point1x.textChanged.connect(self.SoltNormal)
        self.pointWidget.ui.lineEdit_point1y.textChanged.connect(self.SoltNormal)
        self.pointWidget.ui.lineEdit_point1z.textChanged.connect(self.SoltNormal)

    def SoltNormal(self):
        point1x = self.pointWidget.ui.lineEdit_point1x.text()
        point1y = self.pointWidget.ui.lineEdit_point1y.text()
        point1z = self.pointWidget.ui.lineEdit_point1z.text()
        if self.pointWidget.ui.comboBox_dir.currentIndex() == 0:
            self.pointWidget.ui.lineEdit_point2x.setText(point1x)
            self.pointWidget.ui.lineEdit_point2x.setEnabled(False)
            self.pointWidget.ui.lineEdit_point2y.setEnabled(True)
            self.pointWidget.ui.lineEdit_point2z.setEnabled(True)
        elif self.pointWidget.ui.comboBox_dir.currentIndex() == 1:
            self.pointWidget.ui.lineEdit_point2y.setText(point1y)
            self.pointWidget.ui.lineEdit_point2x.setEnabled(True)
            self.pointWidget.ui.lineEdit_point2y.setEnabled(False)
            self.pointWidget.ui.lineEdit_point2z.setEnabled(True)
        elif self.pointWidget.ui.comboBox_dir.currentIndex() == 2:
            self.pointWidget.ui.lineEdit_point2z.setText(point1z)
            self.pointWidget.ui.lineEdit_point2x.setEnabled(True)
            self.pointWidget.ui.lineEdit_point2y.setEnabled(True)
            self.pointWidget.ui.lineEdit_point2z.setEnabled(False)
        else:
            pass

    def slotOk(self):
        self.setInfoToObj()
        # 判断输入坐标是否符合模型的要求
        judge = self.judgePoint()
        if judge:
            QtGui.QMessageBox.information(None, "", "无法有效绘制矩形面，请检查坐标。")
        else:
            self.isKeepData = True
            self.close()

    def judgePoint(self):
        coordinate = FreeCAD.ActiveDocument.CoordinateSystem
        if self.obj.Normal == coord[coordinate][0]:
            if self.obj.Point1Y == self.obj.Point2Y or self.obj.Point1Z == self.obj.Point2Z:
                return True
            else:
                return False
        elif self.obj.Normal == coord[coordinate][1]:
            if self.obj.Point1X == self.obj.Point2X or self.obj.Point1Z == self.obj.Point2Z:
                return True
            else:
                return False
        elif self.obj.Normal == coord[coordinate][2]:
            if self.obj.Point1X == self.obj.Point2X or self.obj.Point1Y == self.obj.Point2Y:
                return True
            else:
                return False
