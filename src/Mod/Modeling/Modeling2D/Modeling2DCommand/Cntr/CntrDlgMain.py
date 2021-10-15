# -*- coding: utf-8 -*-
import traceback
import FreeCADGui
import CntrDialog
from PySide import QtGui
import FreeCAD
from Modeling.Modeling2D.Tools import Tools2D, ToolsUI
from Modeling.Modeling2D.Tools.Tools2D import sayz


class ShowDialog(QtGui.QDialog):
    def __init__(self, obj, isNew=False, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = CntrDialog.Ui_Dialog()
        self.ui.setupUi(self)

        # 暂时写在这里
        self.setModal(False)
        self.obj = obj
        self.isNew = isNew
        self.initDialog()
        self.getInfoFromObj()
        self.isKeepData = False

    def initDialog(self):
        """
        初始化界面，设置界面逻辑，绑定信号与槽
        """
        self.defaultValue = []
        # 对话框的初始化
        self.refreshCombox()
        self.initObservationField()
        self.initTimer()
        # 正投影面下拉框选择事件
        self.ui.ComboBox_Shadow.currentIndexChanged.connect(self.ComboBox_Shadow_clicked)
        # 此处按钮命名需要修改
        # self.ui.radioButton_x.toggled.connect(self.radioButton)
        # self.ui.radioButton_y.toggled.connect(self.radioButton)
        # 隐藏法向按钮和标签
        self.ui.radioButton_x.hide()
        self.ui.radioButton_y.hide()
        self.ui.label_2.hide()

        # self.ui.le_start_x.textChanged.connect(self.leStart)
        # self.ui.le_start_y.textChanged.connect(self.leStart)

        self.ui.pb_ok.clicked.connect(self.slotOK)
        self.ui.pb_cancel.clicked.connect(self.slotCancel)

        # 获取当前坐标系及坐标系单位
        coord = Tools2D.getCoordinate()
        self.x = coord[0]
        self.y = coord[1]
        # 根据坐标系初始化面板
        self.ui.label_X.setText(self.x)
        self.ui.label_Y.setText(self.y)
        self.ui.radioButton_x.setText(self.x)
        self.ui.radioButton_y.setText(self.y)

    def getInfoFromObj(self):
        """
        从Object获取信息，并且设置到Dialog
        """
        try:
            self.ui.le_name.setText(self.obj.Label)

            itemIndex = self.ui.ComboBox_Shadow.findText(str(self.obj.orthogonalProjectionLine))
            self.ui.ComboBox_Shadow.setCurrentIndex(itemIndex)

            self.ui.le_start_x.setText(self.obj.point1_X)
            self.ui.le_start_y.setText(self.obj.point1_Y)

            itemIndex1 = self.ui.ComboBox_start.findText(str(self.obj.point1_name))
            self.ui.ComboBox_start.setCurrentIndex(itemIndex1)

            self.ui.le_end_x.setText(self.obj.point2_X)
            self.ui.le_end_y.setText(self.obj.point2_Y)

            itemIndex2 = self.ui.ComboBox_end.findText(str(self.obj.point2_name))
            self.ui.ComboBox_end.setCurrentIndex(itemIndex2)

            self.ui.radioButton_x.setChecked(self.obj.isCheckNormal1)
            self.ui.radioButton_y.setChecked(self.obj.isCheckNormal2)

            itemIndex3 = self.ui.ComboBox.findText(str(self.obj.observationField))
            self.ui.ComboBox.setCurrentIndex(itemIndex3)

            itemIndex4 = self.ui.comboBox_timer.findText(str(self.obj.timer))
            self.ui.comboBox_timer.setCurrentIndex(itemIndex4)

            self.ui.checkBox.setChecked(self.obj.isoline)

        except AttributeError:
            Tools2D.sayz("Circular--异常--在读取Object属性时出现异常")
            Tools2D.sayz(traceback.format_exc())
        except Exception as e:
            Tools2D.sayz("Circular--" + str(e))
        else:
            Tools2D.sayz("Circular--成功--读取Object信息")

    def setInfoToObj(self):
        """
        从Dialog获取信息，并且赋值到Object
        """
        try:
            Tools2D.setLabelToObj(self.obj, self.ui.le_name.text())

            self.obj.orthogonalProjectionLine = self.ui.ComboBox_Shadow.currentText()

            self.obj.point1_name = self.ui.ComboBox_start.currentText()
            self.obj.point1_X = self.ui.le_start_x.text()
            self.obj.point1_Y = self.ui.le_start_y.text()

            self.obj.point2_name = self.ui.ComboBox_end.currentText()
            self.obj.point2_X = self.ui.le_end_x.text()
            self.obj.point2_Y = self.ui.le_end_y.text()

            self.obj.observationField = self.ui.ComboBox.currentText()
            self.obj.timer = self.ui.comboBox_timer.currentText()

            self.obj.isoline = self.ui.checkBox.isChecked()

            pass
        except:
            import traceback
            sayz("error:" + traceback.format_exc())
        pass

    def slotOK(self):
        """
        确定按钮绑定的槽函数
        """
        self.isKeepData = True
        self.close()

    def slotCancel(self):
        """
        取消按钮绑定的槽函数
        """
        self.isKeepData = False
        self.close()

    def refreshCombox(self):
        try:
            ComboBox_Shadow_list = []
            default_list = ["OSYS$AREA"]
            for i in default_list:
                self.ui.ComboBox_Shadow.addItem(i)
            for i in range(self.ui.ComboBox_Shadow.count()):
                ComboBox_Shadow_list.append(self.ui.ComboBox_Shadow.itemText(i))
            volumeList = Tools2D.getLabelsByType(Tools2D.ObjectType.AreaConformal)
            for i in volumeList:
                if i not in ComboBox_Shadow_list:
                    self.ui.ComboBox_Shadow.addItem(i)
        except:
            import traceback
            sayz("error:" + traceback.format_exc())

    def initTimer(self):
        try:
            Timer_list = []
            for i in range(self.ui.comboBox_timer.count()):
                Timer_list.append(self.ui.comboBox_timer.itemText(i))
            volumeList = Tools2D.getLabelsByType(Tools2D.ObjectType.Timer)
            for i in volumeList:
                if i not in Timer_list:
                    self.ui.comboBox_timer.addItem(i)
        except:
            import traceback
            sayz("error:" + traceback.format_exc())

    def ComboBox_Shadow_clicked(self):
        try:
            if self.ui.ComboBox_Shadow.currentIndex() == 0:
                # self.ui.le_start_x.setText(self.obj.point1_X)
                # self.ui.le_start_y.setText(self.obj.point1_Y)
                # self.ui.le_end_x.setText(self.obj.point2_X)
                # self.ui.le_end_y.setText(self.obj.point2_Y)
                self.ui.le_start_x.setEnabled(True)
                self.ui.le_start_y.setEnabled(True)
                self.ui.le_end_x.setEnabled(True)
                self.ui.le_end_y.setEnabled(True)
            elif self.ui.ComboBox_Shadow.currentIndex() == 1:
                self.ui.le_start_x.setEnabled(False)
                self.ui.le_start_y.setEnabled(False)
                self.ui.le_end_x.setEnabled(False)
                self.ui.le_end_y.setEnabled(False)
            else:
                objName = self.ui.ComboBox_Shadow.currentText()
                if objName in self.defaultValue:
                    pass
                else:
                    modelData = Tools2D.getValueOfAreaObjByLabel(objName)
                    self.ui.le_start_x.setText(modelData["point1.x"])
                    self.ui.le_start_y.setText(modelData["point1.y"])
                    self.ui.le_end_x.setText(modelData["point2.x"])
                    self.ui.le_end_y.setText(modelData["point2.y"])
                self.ui.le_start_x.setEnabled(False)
                self.ui.le_start_y.setEnabled(False)
                self.ui.le_end_x.setEnabled(False)
                self.ui.le_end_y.setEnabled(False)
        except:
            import traceback
            Tools2D.sayz("error:" + traceback.format_exc())

    def initObservationField(self):
        list = ["E1", "E2", "E3", "B1", "B2", "B3", "J1", "J2", "J3", "Q0",
                "E1AV", "E2AV", "E3AV", "B1AV", "B2AV", "B3AV", "B1ST", "B2ST",
                "B3ST", "PHST", "|B|", "|E|"]
        for i in range(0, len(list)):
            self.ui.ComboBox.addItem(list[i])

    # 点击关闭对话框，删除创建的对象
    def closeEvent(self, event):
        if self.isKeepData:
            self.setInfoToObj()
            FreeCADGui.runCommand("CreateM2D")
        else:
            if self.isNew:
                FreeCAD.ActiveDocument.removeObject(self.obj.Label)
