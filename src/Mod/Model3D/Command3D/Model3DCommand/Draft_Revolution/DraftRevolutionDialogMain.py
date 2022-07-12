# -*- coding: utf-8 -*-
from PySide import QtGui
import FreeCAD
from Model3D.Tools import ObjectTools, Tools3D
import FreeCADGui
import DraftRevolutionDialog
import CustomWidget


class CustomShowWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = CustomWidget.Ui_Form()
        self.ui.setupUi(self)


class ShowDialog(QtGui.QDialog):
    def __init__(self, obj, isNew=False, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = DraftRevolutionDialog.Ui_Dialog()
        self.ui.setupUi(self)
        self.customAttribute = CustomShowWidget()

        self.setModal(False)
        self.obj = obj
        self.isNew = isNew
        self.isKeepData = False
        self.initDialog()
        self.getInfoFromObj()

    def initDialog(self):
        Tools3D.setLineEditsCompleter(Tools3D.getAllLineEdits(self.ui))
        self.ui.pb_ok.clicked.connect(self.slotOk)
        self.ui.pb_cancel.clicked.connect(self.slotCancel)
        self.reComboBox()
        self.ui.comboBox_attribute.currentIndexChanged.connect(self.slotAttribute)
        self.customAttribute.ui.lineEdit_sigma2.hide()
        self.customAttribute.ui.lineEdit_sigma3.hide()
        self.customAttribute.ui.lineEdit_setEps2.hide()
        self.customAttribute.ui.lineEdit_setEps3.hide()
        coord = Tools3D.getCoordinate()
        x1 = coord[0]
        y1 = coord[1]
        z1 = coord[2]
        self.ui.checkBox_X.setText(x1)
        self.ui.checkBox_Y.setText(y1)
        self.ui.checkBox_Z.setText(z1)
        self.ui.label_7.setText(x1)
        self.ui.label_8.setText(y1)
        self.ui.label_9.setText(z1)


    def reComboBox(self):
        areas = ObjectTools.getAllAreas()
        for areaItem in areas:
            self.ui.comboBox_area.addItem(areaItem)

    def getInfoFromObj(self):
        self.ui.lineEdit_name.setText(self.obj.Label)
        Tools3D.getOrderFromObj(self.obj, self.ui)
        self.ui.lineEdit_point1x.setText(str(self.obj.user_point1_x).replace(' ', ''))
        self.ui.lineEdit_point1y.setText(str(self.obj.user_point1_y).replace(' ', ''))
        self.ui.lineEdit_point1z.setText(str(self.obj.user_point1_z).replace(' ', ''))
        self.ui.lineEdit_point2x.setText(str(self.obj.user_point2_x).replace(' ', ''))
        self.ui.lineEdit_point2y.setText(str(self.obj.user_point2_y).replace(' ', ''))
        self.ui.lineEdit_point2z.setText(str(self.obj.user_point2_z).replace(' ', ''))
        self.ui.comboBox_area.setCurrentIndex(self.ui.comboBox_area.findText(str(self.obj.Area)))
        # 属性
        self.ui.comboBox_attribute.setCurrentIndex(self.ui.comboBox_attribute.findText(str(self.obj.Attribute)))
        self.customAttribute.ui.comboBox_sigma.setCurrentIndex(
            self.customAttribute.ui.comboBox_sigma.findText(str(self.obj.C_SIGMA)))
        self.customAttribute.ui.comboBox_setEps.setCurrentIndex(
            self.customAttribute.ui.comboBox_setEps.findText(str(self.obj.RDC)))
        self.customAttribute.ui.lineEdit_sigma1.setText(str(self.obj.SIGMA1))
        self.customAttribute.ui.lineEdit_sigma2.setText(str(self.obj.SIGMA2))
        self.customAttribute.ui.lineEdit_sigma3.setText(str(self.obj.SIGMA3))
        self.customAttribute.ui.lineEdit_setEps1.setText(str(self.obj.EPS1))
        self.customAttribute.ui.lineEdit_setEps2.setText(str(self.obj.EPS2))
        self.customAttribute.ui.lineEdit_setEps3.setText(str(self.obj.EPS3))
        # 非均匀网格
        self.ui.lineEdit_DX1.setText(str(self.obj.MarkX).replace(' ', ''))
        self.ui.lineEdit_DX2.setText(str(self.obj.MarkY).replace(' ', ''))
        self.ui.lineEdit_DX3.setText(str(self.obj.MarkZ).replace(' ', ''))
        self.ui.checkBox_X.setChecked(self.obj.isMarkX)
        self.ui.checkBox_Y.setChecked(self.obj.isMarkY)
        self.ui.checkBox_Z.setChecked(self.obj.isMarkZ)

    def setInfoToObj(self):
        self.obj.Label = self.ui.lineEdit_name.text()
        Tools3D.setOrderToObj(self.obj, self.ui)
        self.obj.Area = self.ui.comboBox_area.currentText()
        self.obj.Point1X = self.ui.lineEdit_point1x.text()
        self.obj.Point1Y = self.ui.lineEdit_point1y.text()
        self.obj.Point1Z = self.ui.lineEdit_point1z.text()
        self.obj.Point2X = self.ui.lineEdit_point2x.text()
        self.obj.Point2Y = self.ui.lineEdit_point2y.text()
        self.obj.Point2Z = self.ui.lineEdit_point2z.text()
        self.obj.user_point1_x = self.ui.lineEdit_point1x.text().replace(' ', '')
        self.obj.user_point1_y = self.ui.lineEdit_point1y.text().replace(' ', '')
        self.obj.user_point1_z = self.ui.lineEdit_point1z.text().replace(' ', '')
        self.obj.user_point2_x = self.ui.lineEdit_point2x.text().replace(' ', '')
        self.obj.user_point2_y = self.ui.lineEdit_point2y.text().replace(' ', '')
        self.obj.user_point2_z = self.ui.lineEdit_point2z.text().replace(' ', '')
        Tools3D.setPlaceToObj(self.obj, "Point2Y", self.ui.lineEdit_point2y.text())
        Tools3D.setPlaceToObj(self.obj, "Point1X", self.ui.lineEdit_point1x.text())
        Tools3D.setPlaceToObj(self.obj, "Point1Y", self.ui.lineEdit_point1y.text())
        Tools3D.setPlaceToObj(self.obj, "Point1Z", self.ui.lineEdit_point1z.text())
        Tools3D.setPlaceToObj(self.obj, "Point2X", self.ui.lineEdit_point2x.text())
        Tools3D.setPlaceToObj(self.obj, "Point2Z", self.ui.lineEdit_point2z.text())
        # 属性
        self.obj.Attribute = self.ui.comboBox_attribute.currentText()
        self.obj.MarkX = self.ui.lineEdit_DX1.text()
        self.obj.MarkY = self.ui.lineEdit_DX2.text()
        self.obj.MarkZ = self.ui.lineEdit_DX3.text()
        self.obj.isMarkX = self.ui.checkBox_X.isChecked()
        self.obj.isMarkY = self.ui.checkBox_Y.isChecked()
        self.obj.isMarkZ = self.ui.checkBox_Z.isChecked()
        # 非均匀网格
        self.obj.C_SIGMA = self.customAttribute.ui.comboBox_sigma.currentText()
        self.obj.SIGMA1 = self.customAttribute.ui.lineEdit_sigma1.text()
        self.obj.SIGMA2 = self.customAttribute.ui.lineEdit_sigma2.text()
        self.obj.SIGMA3 = self.customAttribute.ui.lineEdit_sigma3.text()
        self.obj.RDC = self.customAttribute.ui.comboBox_setEps.currentText()
        self.obj.EPS1 = self.customAttribute.ui.lineEdit_setEps1.text()
        self.obj.EPS2 = self.customAttribute.ui.lineEdit_setEps2.text()
        self.obj.EPS3 = self.customAttribute.ui.lineEdit_setEps3.text()
        self.obj.recompute()

    def slotOk(self):
        self.isKeepData = True
        self.close()

    def slotCancel(self):
        self.isKeepData = False
        self.close()

    def closeEvent(self, *args, **kwargs):
        if self.isKeepData:
            self.setInfoToObj()
            FreeCADGui.runCommand("CreateM3D_new")
            FreeCADGui.runCommand("UpdateBooleanCommand_3D")
        else:
            if self.isNew:
                FreeCAD.ActiveDocument.removeObject(self.obj.Label)

    def slotAttribute(self):
        if self.ui.comboBox_attribute.currentIndex() == 2:
            self.ui.horizontalLayout_3.addWidget(self.customAttribute)
            self.customAttribute.show()
            self.customAttribute.ui.comboBox_sigma.currentIndexChanged.connect(self.sigmaOption)
            self.customAttribute.ui.comboBox_setEps.currentIndexChanged.connect(self.setEpsOption)
        else:
            self.customAttribute.hide()

    def sigmaOption(self):
        if self.customAttribute.ui.comboBox_sigma.currentIndex() == 0:
            self.customAttribute.ui.lineEdit_sigma1.show()
            self.customAttribute.ui.lineEdit_sigma2.hide()
            self.customAttribute.ui.lineEdit_sigma3.hide()
        elif self.customAttribute.ui.comboBox_sigma.currentIndex() == 1:
            self.customAttribute.ui.lineEdit_sigma1.show()
            self.customAttribute.ui.lineEdit_sigma2.show()
            self.customAttribute.ui.lineEdit_sigma3.show()
        else:
            self.customAttribute.ui.lineEdit_sigma1.hide()
            self.customAttribute.ui.lineEdit_sigma2.hide()
            self.customAttribute.ui.lineEdit_sigma3.hide()

    def setEpsOption(self):
        if self.customAttribute.ui.comboBox_setEps.currentIndex() == 0:
            self.customAttribute.ui.lineEdit_setEps1.show()
            self.customAttribute.ui.lineEdit_setEps2.hide()
            self.customAttribute.ui.lineEdit_setEps3.hide()
        elif self.customAttribute.ui.comboBox_setEps.currentIndex() == 1:
            self.customAttribute.ui.lineEdit_setEps1.show()
            self.customAttribute.ui.lineEdit_setEps2.show()
            self.customAttribute.ui.lineEdit_setEps3.show()
        else:
            self.customAttribute.ui.lineEdit_setEps1.hide()
            self.customAttribute.ui.lineEdit_setEps2.hide()
            self.customAttribute.ui.lineEdit_setEps3.hide()
