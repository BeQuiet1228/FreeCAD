# -*- coding: utf-8 -*-
import PointWidget
from PySide import QtGui
import FreeCAD
import Part
import FreeCADGui
import traceback
from Model3D.Command3D.Model3DCommand.BaseUI import BaseDialogMain, BaseDialog
from Model3D.Tools import Tools3D, ObjectTools

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
        self.pointWidget.ui.lineEdit_point3x.setText(str(self.obj.user_point3_x).replace(' ', ''))
        self.pointWidget.ui.lineEdit_point3y.setText(str(self.obj.user_point3_y).replace(' ', ''))
        self.pointWidget.ui.lineEdit_point3z.setText(str(self.obj.user_point3_z).replace(' ', ''))
        self.pointWidget.ui.lineEdit_point4x.setText(str(self.obj.user_point4_x).replace(' ', ''))
        self.pointWidget.ui.lineEdit_point4y.setText(str(self.obj.user_point4_y).replace(' ', ''))
        self.pointWidget.ui.lineEdit_point4z.setText(str(self.obj.user_point4_z).replace(' ', ''))
    def setInfoToObj(self):
        self.obj.user_point1_x = self.pointWidget.ui.lineEdit_point1x.text().replace(' ', '')
        self.obj.user_point1_y = self.pointWidget.ui.lineEdit_point1y.text().replace(' ', '')
        self.obj.user_point1_z = self.pointWidget.ui.lineEdit_point1z.text().replace(' ', '')
        self.obj.user_point2_x = self.pointWidget.ui.lineEdit_point2x.text().replace(' ', '')
        self.obj.user_point2_y = self.pointWidget.ui.lineEdit_point2y.text().replace(' ', '')
        self.obj.user_point2_z = self.pointWidget.ui.lineEdit_point2z.text().replace(' ', '')
        self.obj.user_point3_x = self.pointWidget.ui.lineEdit_point3x.text().replace(' ', '')
        self.obj.user_point3_y = self.pointWidget.ui.lineEdit_point3y.text().replace(' ', '')
        self.obj.user_point3_z = self.pointWidget.ui.lineEdit_point3z.text().replace(' ', '')
        self.obj.user_point4_x = self.pointWidget.ui.lineEdit_point4x.text().replace(' ', '')
        self.obj.user_point4_y = self.pointWidget.ui.lineEdit_point4y.text().replace(' ', '')
        self.obj.user_point4_z = self.pointWidget.ui.lineEdit_point4z.text().replace(' ', '')
        Tools3D.setPlaceToObj(self.obj, "Point1Y", self.pointWidget.ui.lineEdit_point1y.text())
        Tools3D.setPlaceToObj(self.obj, "Point1X", self.pointWidget.ui.lineEdit_point1x.text())
        Tools3D.setPlaceToObj(self.obj, "Point1Z", self.pointWidget.ui.lineEdit_point1z.text())
        Tools3D.setPlaceToObj(self.obj, "Point2Y", self.pointWidget.ui.lineEdit_point2y.text())
        Tools3D.setPlaceToObj(self.obj, "Point2X", self.pointWidget.ui.lineEdit_point2x.text())
        Tools3D.setPlaceToObj(self.obj, "Point2Z", self.pointWidget.ui.lineEdit_point2z.text())
        Tools3D.setPlaceToObj(self.obj, "Point3Y", self.pointWidget.ui.lineEdit_point3y.text())
        Tools3D.setPlaceToObj(self.obj, "Point3X", self.pointWidget.ui.lineEdit_point3x.text())
        Tools3D.setPlaceToObj(self.obj, "Point3Z", self.pointWidget.ui.lineEdit_point3z.text())
        Tools3D.setPlaceToObj(self.obj, "Point4Y", self.pointWidget.ui.lineEdit_point4y.text())
        Tools3D.setPlaceToObj(self.obj, "Point4X", self.pointWidget.ui.lineEdit_point4x.text())
        Tools3D.setPlaceToObj(self.obj, "Point4Z", self.pointWidget.ui.lineEdit_point4z.text())
        self.obj.recompute()

    def slotOk(self):
        self.setInfoToObj()
        # 判断输入坐标是否符合模型的要求
        judge = self.judgePoint()
        if judge:
            QtGui.QMessageBox.information(None, "", "无法有效绘制四面体，请检查输入数据。")
        else:
            self.isKeepData = True
            self.close()

    def judgePoint(self):
        point1 = Tools3D.transToRecVector(self.obj.Point1X.Value, self.obj.Point1Y.Value, self.obj.Point1Z.Value)
        point2 = Tools3D.transToRecVector(self.obj.Point2X.Value, self.obj.Point2Y.Value, self.obj.Point2Z.Value)
        point3 = Tools3D.transToRecVector(self.obj.Point3X.Value, self.obj.Point3Y.Value, self.obj.Point3Z.Value)
        point4 = Tools3D.transToRecVector(self.obj.Point4X.Value, self.obj.Point4Y.Value, self.obj.Point4Z.Value)
        if ObjectTools.isFourPointsOnTheSamePlane([point1, point2, point3, point4]):
            return True
        if point1 == point2:
            return True
        if point1 == point3:
            return True
        if point1 == point4:
            return True
        if point2 == point3:
            return True
        if point2 == point4:
            return True
        if point3 == point4:
            return True
        else:
            return False
