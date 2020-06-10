# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TaskControlPal.ui'
#
# Created: Thu Jan 24 17:09:15 2019
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui
import FreeCAD

class Ui_DockWidget_TaskControl(object):
    def setupUi(self, DockWidget_TaskControl):
        DockWidget_TaskControl.setObjectName("DockWidget_TaskControl")
        DockWidget_TaskControl.resize(292, 393)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.gridLayoutWidget = QtGui.QWidget(self.dockWidgetContents)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 271, 351))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.iterationResult = QtGui.QLabel(self.gridLayoutWidget)
        self.iterationResult.setText("")
        self.iterationResult.setObjectName("iterationResult")
        self.verticalLayout_3.addWidget(self.iterationResult)
        self.iterationTimeResult = QtGui.QLabel(self.gridLayoutWidget)
        self.iterationTimeResult.setText("")
        self.iterationTimeResult.setObjectName("iterationTimeResult")
        self.verticalLayout_3.addWidget(self.iterationTimeResult)
        self.consumingTimeResult = QtGui.QLabel(self.gridLayoutWidget)
        self.consumingTimeResult.setText("")
        self.consumingTimeResult.setObjectName("consumingTimeResult")
        self.verticalLayout_3.addWidget(self.consumingTimeResult)
        self.particelNumberResult = QtGui.QLabel(self.gridLayoutWidget)
        self.particelNumberResult.setText("")
        self.particelNumberResult.setObjectName("particelNumberResult")
        self.verticalLayout_3.addWidget(self.particelNumberResult)
        self.runningStateResult = QtGui.QLabel(self.gridLayoutWidget)
        self.runningStateResult.setText("")
        self.runningStateResult.setObjectName("runningStateResult")
        self.verticalLayout_3.addWidget(self.runningStateResult)
        self.gridLayout.addLayout(self.verticalLayout_3, 4, 1, 1, 1)

        # 暂停
        self.stopBtn = QtGui.QPushButton(self.gridLayoutWidget)
        self.stopBtn.setObjectName("stopBtn")
        self.gridLayout.addWidget(self.stopBtn, 0, 1, 1, 1)
        self.stopBtn.clicked.connect(self.onStop)

        # 定时
        self.timerBtn = QtGui.QPushButton(self.gridLayoutWidget)
        self.timerBtn.setObjectName("timerBtn")
        self.gridLayout.addWidget(self.timerBtn, 1, 1, 1, 1)
        self.timerBtn.clicked.connect(self.onTimer)

        # 刷新
        self.refreshBtn = QtGui.QPushButton(self.gridLayoutWidget)
        self.refreshBtn.setObjectName("refreshBtn")
        self.gridLayout.addWidget(self.refreshBtn, 3, 1, 1, 1)
        self.refreshBtn.clicked.connect(self.onRefresh)

        # 网格
        self.meshBtn = QtGui.QPushButton(self.gridLayoutWidget)
        self.meshBtn.setObjectName("meshBtn")
        self.gridLayout.addWidget(self.meshBtn, 2, 1, 1, 1)
        self.meshBtn.clicked.connect(self.onMesh)

        # 翻页
        self.pageBtn = QtGui.QPushButton(self.gridLayoutWidget)
        self.pageBtn.setObjectName("pageBtn")
        self.gridLayout.addWidget(self.pageBtn, 2, 0, 1, 1)
        self.pageBtn.clicked.connect(self.onPage)

        # 平铺
        self.tileBtn = QtGui.QPushButton(self.gridLayoutWidget)
        self.tileBtn.setObjectName("tileBtn")
        self.gridLayout.addWidget(self.tileBtn, 3, 0, 1, 1)
        self.tileBtn.clicked.connect(self.onTile)

        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_iterations = QtGui.QLabel(self.gridLayoutWidget)
        self.label_iterations.setObjectName("label_iterations")
        self.verticalLayout_2.addWidget(self.label_iterations)
        self.label_iteration_time = QtGui.QLabel(self.gridLayoutWidget)
        self.label_iteration_time.setObjectName("label_iteration_time")
        self.verticalLayout_2.addWidget(self.label_iteration_time)
        self.label_consumingTime = QtGui.QLabel(self.gridLayoutWidget)
        self.label_consumingTime.setObjectName("label_consumingTime")
        self.verticalLayout_2.addWidget(self.label_consumingTime)
        self.label_particleNumber = QtGui.QLabel(self.gridLayoutWidget)
        self.label_particleNumber.setObjectName("label_particleNumber")
        self.verticalLayout_2.addWidget(self.label_particleNumber)
        self.label_runningState = QtGui.QLabel(self.gridLayoutWidget)
        self.label_runningState.setObjectName("label_runningState")
        self.verticalLayout_2.addWidget(self.label_runningState)
        self.gridLayout.addLayout(self.verticalLayout_2, 4, 0, 1, 1)

        # 器件结构
        self.deviceBtn = QtGui.QPushButton(self.gridLayoutWidget)
        self.deviceBtn.setObjectName("deviceBtn")
        self.gridLayout.addWidget(self.deviceBtn, 1, 0, 1, 1)
        self.deviceBtn.clicked.connect(self.onDevice)

        # 运行
        self.runBtn = QtGui.QPushButton(self.gridLayoutWidget)
        self.runBtn.setObjectName("runBtn")
        self.gridLayout.addWidget(self.runBtn, 0, 0, 1, 1)
        self.runBtn.clicked.connect(self.onRun)
        self.runBtn.setEnabled(False)

        DockWidget_TaskControl.setWidget(self.dockWidgetContents)

        self.retranslateUi(DockWidget_TaskControl)
        QtCore.QMetaObject.connectSlotsByName(DockWidget_TaskControl)

    def retranslateUi(self, DockWidget_TaskControl):
        DockWidget_TaskControl.setWindowTitle(QtGui.QApplication.translate("DockWidget_TaskControl", "任务控制", None, QtGui.QApplication.UnicodeUTF8))
        self.stopBtn.setText(QtGui.QApplication.translate("DockWidget_TaskControl", "暂停", None, QtGui.QApplication.UnicodeUTF8))
        self.timerBtn.setText(QtGui.QApplication.translate("DockWidget_TaskControl", "定时（OFF）", None, QtGui.QApplication.UnicodeUTF8))
        self.refreshBtn.setText(QtGui.QApplication.translate("DockWidget_TaskControl", "刷新", None, QtGui.QApplication.UnicodeUTF8))
        self.meshBtn.setText(QtGui.QApplication.translate("DockWidget_TaskControl", "网格", None, QtGui.QApplication.UnicodeUTF8))
        self.pageBtn.setText(QtGui.QApplication.translate("DockWidget_TaskControl", "翻页", None, QtGui.QApplication.UnicodeUTF8))
        self.tileBtn.setText(QtGui.QApplication.translate("DockWidget_TaskControl", "平铺", None, QtGui.QApplication.UnicodeUTF8))
        self.label_iterations.setText(QtGui.QApplication.translate("DockWidget_TaskControl", "迭代次数（次）", None, QtGui.QApplication.UnicodeUTF8))
        self.label_iteration_time.setText(QtGui.QApplication.translate("DockWidget_TaskControl", "迭代时间（纳秒）", None, QtGui.QApplication.UnicodeUTF8))
        self.label_consumingTime.setText(QtGui.QApplication.translate("DockWidget_TaskControl", "消耗时间（时: 分: 秒）", None, QtGui.QApplication.UnicodeUTF8))
        self.label_particleNumber.setText(QtGui.QApplication.translate("DockWidget_TaskControl", "粒子数目（个）", None, QtGui.QApplication.UnicodeUTF8))
        self.label_runningState.setText(QtGui.QApplication.translate("DockWidget_TaskControl", "运行状态（1线程）", None, QtGui.QApplication.UnicodeUTF8))
        self.deviceBtn.setText(QtGui.QApplication.translate("DockWidget_TaskControl", "期间结构", None, QtGui.QApplication.UnicodeUTF8))
        self.runBtn.setText(QtGui.QApplication.translate("DockWidget_TaskControl", "运行", None, QtGui.QApplication.UnicodeUTF8))

    def onRun(self):
        self.runBtn.setEnabled(False)
        self.stopBtn.setEnabled(True)
        print("Rerun  simulation ...")
        FreeCAD.clientRerun("Rerun")
        print("Rerun success !")

    def onStop(self):
        self.runBtn.setEnabled(True)
        self.stopBtn.setEnabled(False)
        print("pause  simulation ...")
        FreeCAD.clientPause("pause")
        print("pause success !")

    def onDevice(self):
        print("device")

    def onTimer(self):
        print("time")

    def onPage(self):
        print("turnPage")

    def onMesh(self):
        print("mesh")

    def onTile(self):
        print("tile")

    def onRefresh(self):
        print("refresh")
