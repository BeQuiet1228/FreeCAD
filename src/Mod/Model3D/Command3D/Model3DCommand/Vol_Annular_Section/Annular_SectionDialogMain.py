# -*- coding: utf-8 -*-
from PySide import QtGui
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
        self.pointWidget.ui.lineEdit_point3x.setText(str(self.obj.user_point3_x).replace(' ', ''))
        self.pointWidget.ui.lineEdit_point3y.setText(str(self.obj.user_point3_y).replace(' ', ''))
        self.pointWidget.ui.lineEdit_point3z.setText(str(self.obj.user_point3_z).replace(' ', ''))
        self.pointWidget.ui.lineEdit_point4x.setText(str(self.obj.user_point4_x).replace(' ', ''))
        self.pointWidget.ui.lineEdit_point4y.setText(str(self.obj.user_point4_y).replace(' ', ''))
        self.pointWidget.ui.lineEdit_point4z.setText(str(self.obj.user_point4_z).replace(' ', ''))
        self.pointWidget.ui.lineEdit_radius_inner.setText(str(self.obj.user_radius1).replace(' ', ''))
        self.pointWidget.ui.lineEdit_radius_outer.setText(str(self.obj.user_radius2).replace(' ', ''))

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
        self.obj.user_radius1 = self.pointWidget.ui.lineEdit_radius_inner.text()
        self.obj.user_radius2 = self.pointWidget.ui.lineEdit_radius_outer.text()
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
        Tools3D.setPlaceToObj(self.obj, "InnerRadius", self.pointWidget.ui.lineEdit_radius_inner.text())
        Tools3D.setPlaceToObj(self.obj, "OuterRadius", self.pointWidget.ui.lineEdit_radius_outer.text())
        self.obj.recompute()

    def slotOk(self):
        self.setInfoToObj()
        # 判断输入坐标是否符合模型的要求
        judge = self.judgePoint()
        if judge:
            QtGui.QMessageBox.information(None, "", "无法有效绘制圆环体，请检查输入数据。")
            return
        if Tools3D.getCoordinateString() ==  u"Polar":
            if self.obj.Point3Y > self.obj.Point4Y:
                QtGui.QMessageBox.information(None, "", "point3 的theta值大于point4的theta值， 无法有效绘制圆环体。")
                return
            if self.obj.Point3Y > 360 or self.obj.Point4Y > 360:
                QtGui.QMessageBox.information(None, "", "point3 point4的theta值大于360")
                return
        if Tools3D.getCoordinateString() ==  u"Cylindrical":
            if self.obj.Point3Z > self.obj.Point4Z:
                QtGui.QMessageBox.information(None, "", "point3 的theta值大于point4的theta值， 无法有效绘制圆环体。")
                return
            if self.obj.Point3Z > 360 or self.obj.Point4Z > 360:
                QtGui.QMessageBox.information(None, "", "point3 point4的theta值大于360")
                return
        self.isKeepData = True
        self.close()

    def judgePoint(self):
        if self.obj.Point1X.Value == self.obj.Point2X.Value and self.obj.Point1Y.Value == self.obj.Point2Y.Value and \
                self.obj.Point1Z.Value == self.obj.Point2Z.Value:
            return True
        elif self.obj.Point1X.Value == self.obj.Point3X.Value and self.obj.Point1Y.Value == self.obj.Point3Y.Value and \
                self.obj.Point1Z.Value == self.obj.Point3Z.Value:
            return True
        elif self.obj.Point1X.Value == self.obj.Point4X.Value and self.obj.Point1Y.Value == self.obj.Point4Y.Value and \
                self.obj.Point1Z.Value == self.obj.Point4Z.Value:
            return True
        elif self.obj.InnerRadius.Value < 0 or self.obj.OuterRadius.Value <= 0 or self.obj.InnerRadius.Value >= self.obj.OuterRadius.Value:
            return True
        else:
            return False
