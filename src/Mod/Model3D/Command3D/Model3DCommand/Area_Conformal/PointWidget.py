# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PointWidgetac.ui'
#
# Created: Fri May 21 11:56:03 2021
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui
import FreeCAD
from Model3D.Tools import Completer

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(447, 118)
        self.horizontalLayout = QtGui.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.lineEdit_point1x = Completer.AutoCompleteEdit(Form)
        self.lineEdit_point1x.setObjectName("lineEdit_point1x")
        self.gridLayout.addWidget(self.lineEdit_point1x, 2, 1, 1, 3)
        self.label_3 = QtGui.QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)
        self.lineEdit_point1z = Completer.AutoCompleteEdit(Form)
        self.lineEdit_point1z.setObjectName("lineEdit_point1z")
        self.gridLayout.addWidget(self.lineEdit_point1z, 2, 7, 1, 3)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 6, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 0, 4, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 0, 3, 1, 1)
        self.label_x2 = QtGui.QLabel(Form)
        self.label_x2.setObjectName("label_x2")
        self.gridLayout.addWidget(self.label_x2, 0, 2, 1, 1)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem4, 0, 7, 1, 1)
        self.label_y2 = QtGui.QLabel(Form)
        self.label_y2.setObjectName("label_y2")
        self.gridLayout.addWidget(self.label_y2, 0, 5, 1, 1)
        self.label_z2 = QtGui.QLabel(Form)
        self.label_z2.setObjectName("label_z2")
        self.gridLayout.addWidget(self.label_z2, 0, 8, 1, 1)
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem5, 0, 9, 1, 1)
        self.label = QtGui.QLabel(Form)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.comboBox_dir = QtGui.QComboBox(Form)
        self.comboBox_dir.setObjectName("comboBox_dir")
        self.comboBox_dir.addItem("")
        self.comboBox_dir.addItem("")
        self.comboBox_dir.addItem("")
        self.gridLayout.addWidget(self.comboBox_dir, 1, 1, 1, 3)
        self.lineEdit_point2y = Completer.AutoCompleteEdit(Form)
        self.lineEdit_point2y.setObjectName("lineEdit_point2y")
        self.gridLayout.addWidget(self.lineEdit_point2y, 3, 4, 1, 3)
        self.lineEdit_point1y = Completer.AutoCompleteEdit(Form)
        self.lineEdit_point1y.setObjectName("lineEdit_point1y")
        self.gridLayout.addWidget(self.lineEdit_point1y, 2, 4, 1, 3)
        self.lineEdit_point2x = Completer.AutoCompleteEdit(Form)
        self.lineEdit_point2x.setObjectName("lineEdit_point2x")
        self.gridLayout.addWidget(self.lineEdit_point2x, 3, 1, 1, 3)
        self.lineEdit_point2z = Completer.AutoCompleteEdit(Form)
        self.lineEdit_point2z.setObjectName("lineEdit_point2z")
        self.gridLayout.addWidget(self.lineEdit_point2z, 3, 7, 1, 3)
        self.horizontalLayout.addLayout(self.gridLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setTabOrder(self.comboBox_dir, self.lineEdit_point1x)
        Form.setTabOrder(self.lineEdit_point1x, self.lineEdit_point1y)
        Form.setTabOrder(self.lineEdit_point1y, self.lineEdit_point1z)
        Form.setTabOrder(self.lineEdit_point1z, self.lineEdit_point2x)
        Form.setTabOrder(self.lineEdit_point2x, self.lineEdit_point2y)
        Form.setTabOrder(self.lineEdit_point2y, self.lineEdit_point2z)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Form", "Point_1:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Form", "Point_2:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_x2.setText(QtGui.QApplication.translate("Form", "X", None, QtGui.QApplication.UnicodeUTF8))
        self.label_y2.setText(QtGui.QApplication.translate("Form", "Y", None, QtGui.QApplication.UnicodeUTF8))
        self.label_z2.setText(QtGui.QApplication.translate("Form", "Z", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "Normal", None, QtGui.QApplication.UnicodeUTF8))
        if FreeCAD.ActiveDocument.CoordinateSystem == "Rectangular":
            self.comboBox_dir.setItemText(0, QtGui.QApplication.translate("Form", "X", None,
                                                                          QtGui.QApplication.UnicodeUTF8))
            self.comboBox_dir.setItemText(1, QtGui.QApplication.translate("Form", "Y", None,
                                                                          QtGui.QApplication.UnicodeUTF8))
            self.comboBox_dir.setItemText(2, QtGui.QApplication.translate("Form", "Z", None,
                                                                          QtGui.QApplication.UnicodeUTF8))
        elif FreeCAD.ActiveDocument.CoordinateSystem == "Polar":
            self.comboBox_dir.setItemText(0, QtGui.QApplication.translate("Form", "R", None,
                                                                          QtGui.QApplication.UnicodeUTF8))
            self.comboBox_dir.setItemText(1, QtGui.QApplication.translate("Form", "Theta", None,
                                                                          QtGui.QApplication.UnicodeUTF8))
            self.comboBox_dir.setItemText(2, QtGui.QApplication.translate("Form", "Z", None,
                                                                          QtGui.QApplication.UnicodeUTF8))
        else:
            self.comboBox_dir.setItemText(0, QtGui.QApplication.translate("Form", "Z", None,
                                                                          QtGui.QApplication.UnicodeUTF8))
            self.comboBox_dir.setItemText(1, QtGui.QApplication.translate("Form", "R", None,
                                                                          QtGui.QApplication.UnicodeUTF8))
            self.comboBox_dir.setItemText(2, QtGui.QApplication.translate("Form", "Theta", None,
                                                                          QtGui.QApplication.UnicodeUTF8))

