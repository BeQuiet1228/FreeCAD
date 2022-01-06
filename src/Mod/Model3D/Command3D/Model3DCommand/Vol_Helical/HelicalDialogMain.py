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
        self.pointWidget.ui.lineEdit_point_basex.setText(str(self.obj.user_point1_x).replace(' ', ''))
        self.pointWidget.ui.lineEdit_point_basey.setText(str(self.obj.user_point1_y).replace(' ', ''))
        self.pointWidget.ui.lineEdit_point_basez.setText(str(self.obj.user_point1_z).replace(' ', ''))
        self.pointWidget.ui.lineEdit_point_topx.setText(str(self.obj.user_point2_x).replace(' ', ''))
        self.pointWidget.ui.lineEdit_point_topy.setText(str(self.obj.user_point2_y).replace(' ', ''))
        self.pointWidget.ui.lineEdit_point_topz.setText(str(self.obj.user_point2_z).replace(' ', ''))
        self.pointWidget.ui.lineEdit_point_startx.setText(str(self.obj.user_point3_x).replace(' ', ''))
        self.pointWidget.ui.lineEdit_point_starty.setText(str(self.obj.user_point3_y).replace(' ', ''))
        self.pointWidget.ui.lineEdit_point_startz.setText(str(self.obj.user_point3_z).replace(' ', ''))
        self.pointWidget.ui.lineEdit_radius_inside.setText(str(self.obj.user_radius1).replace(' ', ''))
        self.pointWidget.ui.lineEdit_radius_out.setText(str(self.obj.user_radius2).replace(' ', ''))
        self.pointWidget.ui.lineEdit_pitch.setText(str(self.obj.user_pitch).replace(' ', ''))
        self.pointWidget.ui.lineEdit_width.setText(str(self.obj.user_width).replace(' ', ''))
        # self.pointWidget.ui.lineEdit_point_basex.setText(str(self.obj.PointBaseX).replace(' ', ''))
        # self.pointWidget.ui.lineEdit_point_basey.setText(str(self.obj.PointBaseY).replace(' ', ''))
        # self.pointWidget.ui.lineEdit_point_basez.setText(str(self.obj.PointBaseZ).replace(' ', ''))
        # self.pointWidget.ui.lineEdit_point_topx.setText(str(self.obj.PointTopX).replace(' ', ''))
        # self.pointWidget.ui.lineEdit_point_topy.setText(str(self.obj.PointTopY).replace(' ', ''))
        # self.pointWidget.ui.lineEdit_point_topz.setText(str(self.obj.PointTopZ).replace(' ', ''))
        # self.pointWidget.ui.lineEdit_point_startx.setText(str(self.obj.PointStartX).replace(' ', ''))
        # self.pointWidget.ui.lineEdit_point_starty.setText(str(self.obj.PointStartY).replace(' ', ''))
        # self.pointWidget.ui.lineEdit_point_startz.setText(str(self.obj.PointStartZ).replace(' ', ''))
        # self.pointWidget.ui.lineEdit_radius_inside.setText(str(self.obj.RadiusInside).replace(' ', ''))
        # self.pointWidget.ui.lineEdit_radius_out.setText(str(self.obj.RadiusOut).replace(' ', ''))
        # self.pointWidget.ui.lineEdit_pitch.setText(str(self.obj.Pitch).replace(' ', ''))
        # self.pointWidget.ui.lineEdit_width.setText(str(self.obj.Width).replace(' ', ''))


    def setInfoToObj(self):
        self.obj.user_point1_x = self.pointWidget.ui.lineEdit_point_basex.text()
        self.obj.user_point1_y = self.pointWidget.ui.lineEdit_point_basey.text()
        self.obj.user_point1_z = self.pointWidget.ui.lineEdit_point_basez.text()
        self.obj.user_point2_x = self.pointWidget.ui.lineEdit_point_topx.text()
        self.obj.user_point2_y = self.pointWidget.ui.lineEdit_point_topy.text()
        self.obj.user_point2_z = self.pointWidget.ui.lineEdit_point_topz.text()
        self.obj.user_point3_x = self.pointWidget.ui.lineEdit_point_startx.text()
        self.obj.user_point3_y = self.pointWidget.ui.lineEdit_point_starty.text()
        self.obj.user_point3_z = self.pointWidget.ui.lineEdit_point_startz.text()
        self.obj.user_radius1 = self.pointWidget.ui.lineEdit_radius_inside.text()
        self.obj.user_radius2 = self.pointWidget.ui.lineEdit_radius_out.text()
        self.obj.user_pitch = self.pointWidget.ui.lineEdit_pitch.text()
        self.obj.user_width = self.pointWidget.ui.lineEdit_width.text()
        Tools3D.setPlaceToObj(self.obj, "PointBaseY", self.pointWidget.ui.lineEdit_point_basey.text())
        Tools3D.setPlaceToObj(self.obj, "PointBaseX", self.pointWidget.ui.lineEdit_point_basex.text())
        Tools3D.setPlaceToObj(self.obj, "PointBaseZ", self.pointWidget.ui.lineEdit_point_basez.text())
        Tools3D.setPlaceToObj(self.obj, "PointTopY", self.pointWidget.ui.lineEdit_point_topy.text())
        Tools3D.setPlaceToObj(self.obj, "PointTopX", self.pointWidget.ui.lineEdit_point_topx.text())
        Tools3D.setPlaceToObj(self.obj, "PointTopZ", self.pointWidget.ui.lineEdit_point_topz.text())
        Tools3D.setPlaceToObj(self.obj, "PointStartY", self.pointWidget.ui.lineEdit_point_starty.text())
        Tools3D.setPlaceToObj(self.obj, "PointStartX", self.pointWidget.ui.lineEdit_point_startx.text())
        Tools3D.setPlaceToObj(self.obj, "PointStartZ", self.pointWidget.ui.lineEdit_point_startz.text())
        Tools3D.setPlaceToObj(self.obj, "RadiusInside", self.pointWidget.ui.lineEdit_radius_inside.text())
        Tools3D.setPlaceToObj(self.obj, "RadiusOut", self.pointWidget.ui.lineEdit_radius_out.text())
        Tools3D.setPlaceToObj(self.obj, "Pitch", self.pointWidget.ui.lineEdit_pitch.text())
        Tools3D.setPlaceToObj(self.obj, "Width", self.pointWidget.ui.lineEdit_width.text())

        # self.obj.PointBaseX = self.pointWidget.ui.lineEdit_point_basex.text()
        # self.obj.PointBaseY = self.pointWidget.ui.lineEdit_point_basey.text()
        # self.obj.PointBaseZ = self.pointWidget.ui.lineEdit_point_basez.text()
        # self.obj.PointTopX = self.pointWidget.ui.lineEdit_point_topx.text()
        # self.obj.PointTopY = self.pointWidget.ui.lineEdit_point_topy.text()
        # self.obj.PointTopZ = self.pointWidget.ui.lineEdit_point_topz.text()
        # self.obj.PointStartX = self.pointWidget.ui.lineEdit_point_startx.text()
        # self.obj.PointStartY = self.pointWidget.ui.lineEdit_point_starty.text()
        # self.obj.PointStartZ = self.pointWidget.ui.lineEdit_point_startz.text()
        # self.obj.RadiusInside = self.pointWidget.ui.lineEdit_radius_inside.text()
        # self.obj.RadiusOut = self.pointWidget.ui.lineEdit_radius_out.text()
        # self.obj.Pitch = self.pointWidget.ui.lineEdit_pitch.text()
        # self.obj.Width = self.pointWidget.ui.lineEdit_width.text()
        self.obj.recompute()

    def slotOk(self):
        self.setInfoToObj()
        # 判断输入坐标是否符合模型的要求
        judge = self.judgePoint()
        if judge:
            QtGui.QMessageBox.information(None, "", "无法有效绘制螺旋体，请检查输入数据。")
        else:
            self.isKeepData = True
            self.close()

    def judgePoint(self):
        # 如果两个点X,Y,Z相同，则不能构成体
        if self.obj.PointBaseX.Value == self.obj.PointTopX.Value and self.obj.PointBaseY.Value == self.obj.PointTopY.Value and \
                self.obj.PointTopZ.Value == self.obj.PointBaseZ.Value:
            return True
        elif self.obj.RadiusInside.Value < 0.0 or self.obj.RadiusOut.Value <= 0.0 or self.obj.RadiusInside.Value >= self.obj.RadiusOut.Value:
            return True
        elif self.obj.Pitch.Value <= 0.0:
            return True
        elif self.obj.Width.Value <= 0.0:
            return True
