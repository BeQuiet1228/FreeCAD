# -*- coding: utf-8 -*-
from PySide import QtGui, QtCore
import CoordinateSystemMode
import SelectCoordinateSystem
import NewCoordinateSystem


# 弹出2D,3D对话框
class ShowModeDiaolg(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = CoordinateSystemMode.Ui_Form()
        self.ui.setupUi(self)


# 弹出坐标系对话框
class ShowCoordinateSystemDialog(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self, parent=None)
        self.ui = SelectCoordinateSystem.Ui_Form()
        self.ui.setupUi(self)


# 整合坐标系和2D，3D对话框
class ShowDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = NewCoordinateSystem.Ui_Dialog()
        self.ui.setupUi(self)

        self.a = None
        self.b = None

        self.a = ShowModeDiaolg()
        self.b = ShowCoordinateSystemDialog()
        self.initDialog()
        self.isKeepData = False

    def initDialog(self):
        # 2D,3D对话框
        self.ui.gridLayout.addWidget(self.a, 0, 0, 1, 1)
        self.a.ui.create3DButton.clicked.connect(self.onCreate3D)
        self.a.ui.create2DButton.clicked.connect(self.onCreate2D)
        self.a.ui.create3DTextButton.clicked.connect(self.onCreate3DTextEdit)
        self.a.ui.create2DTextButton.clicked.connect(self.onCreate2DTextEdit)
        self.b.ui.cancelButton.clicked.connect(self.refresh)
        self.b.ui.cartesianButton.clicked.connect(self.onCartesianButton)
        self.b.ui.polarButton.clicked.connect(self.onPolarButton)
        self.b.ui.cylindricalButton.clicked.connect(self.onCylindricalButton)

    def onCreate3D(self):
        self.Result = "3D"
        self.a.hide()
        self.b.show()
        self.ui.gridLayout.addWidget(self.b)
        self.b.ui.polarButton.setEnabled(True)

    def onCreate2D(self):
        self.Result = "2D"
        self.a.hide()
        self.b.show()
        self.ui.gridLayout.addWidget(self.b)
        self.b.ui.polarButton.setEnabled(False)

    def onCreate3DTextEdit(self):
        self.Result = "3DText"
        self.a.hide()
        self.b.show()
        self.ui.gridLayout.addWidget(self.b)
        self.b.ui.polarButton.setEnabled(True)

    def onCreate2DTextEdit(self):
        self.Result = "2DText"
        self.a.hide()
        self.b.show()
        self.ui.gridLayout.addWidget(self.b)
        self.b.ui.polarButton.setEnabled(True)

    def refresh(self):
        self.b.hide()
        self.a.show()

    def onCartesianButton(self):
        self.CoordinateSystem = 'Rectangular'
        self.isKeepData = True
        self.close()

    def onPolarButton(self):
        self.CoordinateSystem = 'Polar'
        self.isKeepData = True
        self.close()

    def onCylindricalButton(self):
        self.CoordinateSystem = 'Cylindrical'
        self.isKeepData = True
        self.close()






