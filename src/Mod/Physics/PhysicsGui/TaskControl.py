# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TaskControl.ui'
#
# Created: Tue Jan 22 20:51:01 2019
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_DockWidget(object):
    def setupUi(self, DockWidget):
        DockWidget.setObjectName("DockWidget")
        DockWidget.resize(283, 338)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.formLayoutWidget = QtGui.QWidget(self.dockWidgetContents)
        self.formLayoutWidget.setGeometry(QtCore.QRect(30, 20, 221, 271))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")

        self.Run = QtGui.QPushButton(self.formLayoutWidget)
        self.Run.setObjectName("Run")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.Run)
        self.Run.clicked.connect(self.runButton)

        self.Stop = QtGui.QPushButton(self.formLayoutWidget)
        self.Stop.setObjectName("Stop")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.Stop)
        self.Stop.clicked.connect(self.stopButton)

        self.Device = QtGui.QPushButton(self.formLayoutWidget)
        self.Device.setObjectName("Device")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.Device)
        self.Device.clicked.connect(self.deviceButton)

        self.Time = QtGui.QPushButton(self.formLayoutWidget)
        self.Time.setObjectName("Time")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.Time)
        self.Time.clicked.connect(self.timeButton)

        self.Tile = QtGui.QPushButton(self.formLayoutWidget)
        self.Tile.setObjectName("Tile")
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.Tile)
        self.Tile.clicked.connect(self.tileButton)

        self.Refresh = QtGui.QPushButton(self.formLayoutWidget)
        self.Refresh.setObjectName("Refresh")
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.Refresh)
        self.Refresh.clicked.connect(self.refreshButton)

        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout.setLayout(5, QtGui.QFormLayout.LabelRole, self.verticalLayout)
        self.Label_iteration = QtGui.QLabel(self.formLayoutWidget)
        self.Label_iteration.setObjectName("Label_iteration")
        self.formLayout.setWidget(6, QtGui.QFormLayout.LabelRole, self.Label_iteration)
        self.LineEdit_iteration = QtGui.QLineEdit(self.formLayoutWidget)
        self.LineEdit_iteration.setEnabled(False)
        self.LineEdit_iteration.setObjectName("LineEdit_iteration")
        self.formLayout.setWidget(6, QtGui.QFormLayout.FieldRole, self.LineEdit_iteration)
        self.Label_iteration_time = QtGui.QLabel(self.formLayoutWidget)
        self.Label_iteration_time.setObjectName("Label_iteration_time")
        self.formLayout.setWidget(7, QtGui.QFormLayout.LabelRole, self.Label_iteration_time)
        self.LineEdit_iteration_time = QtGui.QLineEdit(self.formLayoutWidget)
        self.LineEdit_iteration_time.setEnabled(False)
        self.LineEdit_iteration_time.setObjectName("LineEdit_iteration_time")
        self.formLayout.setWidget(7, QtGui.QFormLayout.FieldRole, self.LineEdit_iteration_time)
        self.Label_consuming_time = QtGui.QLabel(self.formLayoutWidget)
        self.Label_consuming_time.setObjectName("Label_consuming_time")
        self.formLayout.setWidget(8, QtGui.QFormLayout.LabelRole, self.Label_consuming_time)
        self.LineEdit_consuming_time = QtGui.QLineEdit(self.formLayoutWidget)
        self.LineEdit_consuming_time.setEnabled(False)
        self.LineEdit_consuming_time.setObjectName("LineEdit_consuming_time")
        self.formLayout.setWidget(8, QtGui.QFormLayout.FieldRole, self.LineEdit_consuming_time)

        self.TurnPage = QtGui.QPushButton(self.formLayoutWidget)
        self.TurnPage.setObjectName("TurnPage")
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.TurnPage)
        self.TurnPage.clicked.connect(self.turnPageButton)

        self.Mesh = QtGui.QPushButton(self.formLayoutWidget)
        self.Mesh.setObjectName("Mesh")
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.Mesh)
        self.Mesh.clicked.connect(self.meshButton)

        self.Label_particle_number = QtGui.QLabel(self.formLayoutWidget)
        self.Label_particle_number.setObjectName("Label_particle_number")
        self.formLayout.setWidget(9, QtGui.QFormLayout.LabelRole, self.Label_particle_number)
        self.LineEdit_particle_number = QtGui.QLineEdit(self.formLayoutWidget)
        self.LineEdit_particle_number.setEnabled(False)
        self.LineEdit_particle_number.setObjectName("LineEdit_particle_number")
        self.formLayout.setWidget(9, QtGui.QFormLayout.FieldRole, self.LineEdit_particle_number)
        self.Label_running_state = QtGui.QLabel(self.formLayoutWidget)
        self.Label_running_state.setObjectName("Label_running_state")
        self.formLayout.setWidget(10, QtGui.QFormLayout.LabelRole, self.Label_running_state)
        self.LineEdit_running_state = QtGui.QLineEdit(self.formLayoutWidget)
        self.LineEdit_running_state.setEnabled(False)
        self.LineEdit_running_state.setObjectName("LineEdit_running_state")
        self.formLayout.setWidget(10, QtGui.QFormLayout.FieldRole, self.LineEdit_running_state)
        DockWidget.setWidget(self.dockWidgetContents)

        self.retranslateUi(DockWidget)
        QtCore.QMetaObject.connectSlotsByName(DockWidget)

    def retranslateUi(self, DockWidget):
        DockWidget.setWindowTitle(QtGui.QApplication.translate("DockWidget", "TaskControl", None, QtGui.QApplication.UnicodeUTF8))
        self.Run.setText(QtGui.QApplication.translate("DockWidget", "Run", None, QtGui.QApplication.UnicodeUTF8))
        self.Stop.setText(QtGui.QApplication.translate("DockWidget", "Stop", None, QtGui.QApplication.UnicodeUTF8))
        self.Device.setText(QtGui.QApplication.translate("DockWidget", "Device", None, QtGui.QApplication.UnicodeUTF8))
        self.Time.setText(QtGui.QApplication.translate("DockWidget", "Time(OFF)", None, QtGui.QApplication.UnicodeUTF8))
        self.Tile.setText(QtGui.QApplication.translate("DockWidget", "Tile", None, QtGui.QApplication.UnicodeUTF8))
        self.Refresh.setText(QtGui.QApplication.translate("DockWidget", "Refresh", None, QtGui.QApplication.UnicodeUTF8))
        self.Label_iteration.setText(QtGui.QApplication.translate("DockWidget", "Iterations(times)", None, QtGui.QApplication.UnicodeUTF8))
        self.Label_iteration_time.setText(QtGui.QApplication.translate("DockWidget", "Iteration time(ns)", None, QtGui.QApplication.UnicodeUTF8))
        self.Label_consuming_time.setText(QtGui.QApplication.translate("DockWidget", "Consuming time(h:m:s)", None, QtGui.QApplication.UnicodeUTF8))
        self.TurnPage.setText(QtGui.QApplication.translate("DockWidget", "TurnPage", None, QtGui.QApplication.UnicodeUTF8))
        self.Mesh.setText(QtGui.QApplication.translate("DockWidget", "Mesh", None, QtGui.QApplication.UnicodeUTF8))
        self.Label_particle_number.setText(QtGui.QApplication.translate("DockWidget", "Particle number(pieces)", None, QtGui.QApplication.UnicodeUTF8))
        self.Label_running_state.setText(QtGui.QApplication.translate("DockWidget", "Running state(thread)", None, QtGui.QApplication.UnicodeUTF8))

    def runButton(self):
        print("run");

    def stopButton(self):
        print("stop");

    def deviceButton(self):
        print("device");

    def timeButton(self):
        print("time");

    def turnPageButton(self):
        print("turnPage");

    def meshButton(self):
        print("mesh");

    def tileButton(self):
        print("tile");

    def refreshButton(self):
        print("refresh");