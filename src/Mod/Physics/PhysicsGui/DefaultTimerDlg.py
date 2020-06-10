# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DefaultTimerDlg.ui'
#
# Created: Wed Jan 23 19:09:19 2019
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_DefaultTimerDlg(object):
    def setupUi(self, DefaultTimerDlg):
        DefaultTimerDlg.setObjectName("DefaultTimerDlg")
        DefaultTimerDlg.resize(367, 355)
        DefaultTimerDlg.setModal(False)
        self.buttonBox = QtGui.QDialogButtonBox(DefaultTimerDlg)
        self.buttonBox.setGeometry(QtCore.QRect(0, 290, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayoutWidget = QtGui.QWidget(DefaultTimerDlg)
        self.formLayoutWidget.setGeometry(QtCore.QRect(20, 20, 151, 31))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.nameLabel = QtGui.QLabel(self.formLayoutWidget)
        self.nameLabel.setObjectName("nameLabel")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.nameLabel)

        # 名称文本框
        self.nameLineEdit = QtGui.QLineEdit(self.formLayoutWidget)
        self.nameLineEdit.setEnabled(False)
        self.nameLineEdit.setObjectName("nameLineEdit")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.nameLineEdit)

        self.formLayoutWidget_2 = QtGui.QWidget(DefaultTimerDlg)
        self.formLayoutWidget_2.setGeometry(QtCore.QRect(190, 20, 160, 31))
        self.formLayoutWidget_2.setObjectName("formLayoutWidget_2")
        self.formLayout_2 = QtGui.QFormLayout(self.formLayoutWidget_2)
        self.formLayout_2.setContentsMargins(0, 0, 0, 0)
        self.formLayout_2.setObjectName("formLayout_2")
        self.typeLabel = QtGui.QLabel(self.formLayoutWidget_2)
        self.typeLabel.setObjectName("typeLabel")
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.typeLabel)

        # 类型下拉框
        self.typeComboBox = QtGui.QComboBox(self.formLayoutWidget_2)
        self.typeComboBox.setObjectName("typeComboBox")
        self.typeComboBox.addItem("")
        self.typeComboBox.addItem("")
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.typeComboBox)

        self.verticalLayoutWidget = QtGui.QWidget(DefaultTimerDlg)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 70, 331, 191))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        # 定时基准
        self.label_setTime = QtGui.QLabel(self.verticalLayoutWidget)
        self.label_setTime.setObjectName("label_setTime")
        self.horizontalLayout.addWidget(self.label_setTime)

        # 按时间步数按钮
        self.radioButton_step = QtGui.QRadioButton(self.verticalLayoutWidget)
        self.radioButton_step.setChecked(True)
        self.radioButton_step.setObjectName("radioButton_step")
        self.horizontalLayout.addWidget(self.radioButton_step)

        # 按模拟时间按钮
        self.radioButton_simulate = QtGui.QRadioButton(self.verticalLayoutWidget)
        self.radioButton_simulate.setObjectName("radioButton_simulate")
        self.horizontalLayout.addWidget(self.radioButton_simulate)

        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_start = QtGui.QLabel(self.verticalLayoutWidget)
        self.label_start.setObjectName("label_start")
        self.horizontalLayout_2.addWidget(self.label_start)

        # 起始时刻文本框
        self.lineEdit_start = QtGui.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_start.setObjectName("lineEdit_start")
        self.horizontalLayout_2.addWidget(self.lineEdit_start)

        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_end = QtGui.QLabel(self.verticalLayoutWidget)
        self.label_end.setObjectName("label_end")
        self.horizontalLayout_3.addWidget(self.label_end)

        # 结束时刻文本框
        self.lineEdit_end = QtGui.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_end.setObjectName("lineEdit_end")
        self.horizontalLayout_3.addWidget(self.lineEdit_end)

        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_period = QtGui.QLabel(self.verticalLayoutWidget)
        self.label_period.setObjectName("label_period")
        self.horizontalLayout_4.addWidget(self.label_period)

        # 定时周期文本框
        self.lineEdit_period = QtGui.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_period.setObjectName("lineEdit_period")
        self.horizontalLayout_4.addWidget(self.lineEdit_period)

        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.retranslateUi(DefaultTimerDlg)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), DefaultTimerDlg.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), DefaultTimerDlg.reject)
        QtCore.QMetaObject.connectSlotsByName(DefaultTimerDlg)

    def retranslateUi(self, DefaultTimerDlg):
        DefaultTimerDlg.setWindowTitle(QtGui.QApplication.translate("DefaultTimerDlg", "默认定时器", None, QtGui.QApplication.UnicodeUTF8))
        self.nameLabel.setText(QtGui.QApplication.translate("DefaultTimerDlg", "名称", None, QtGui.QApplication.UnicodeUTF8))
        self.nameLineEdit.setText(QtGui.QApplication.translate("DefaultTimerDlg", "DefTimer", None, QtGui.QApplication.UnicodeUTF8))
        self.typeLabel.setText(QtGui.QApplication.translate("DefaultTimerDlg", "类型", None, QtGui.QApplication.UnicodeUTF8))
        self.typeComboBox.setItemText(0, QtGui.QApplication.translate("DefaultTimerDlg", "周期型", None, QtGui.QApplication.UnicodeUTF8))
        self.typeComboBox.setItemText(1, QtGui.QApplication.translate("DefaultTimerDlg", "离散型", None, QtGui.QApplication.UnicodeUTF8))
        self.label_setTime.setText(QtGui.QApplication.translate("DefaultTimerDlg", "定时基准", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton_step.setText(QtGui.QApplication.translate("DefaultTimerDlg", "按时间步数", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton_simulate.setText(QtGui.QApplication.translate("DefaultTimerDlg", "按模拟时间", None, QtGui.QApplication.UnicodeUTF8))
        self.label_start.setText(QtGui.QApplication.translate("DefaultTimerDlg", "起始时刻", None, QtGui.QApplication.UnicodeUTF8))
        self.label_end.setText(QtGui.QApplication.translate("DefaultTimerDlg", "结束时刻", None, QtGui.QApplication.UnicodeUTF8))
        self.label_period.setText(QtGui.QApplication.translate("DefaultTimerDlg", "定时周期", None, QtGui.QApplication.UnicodeUTF8))

