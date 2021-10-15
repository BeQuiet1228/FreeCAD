# -*- coding: utf-8 -*-
import traceback
import VectorDialog
import FreeCAD
import FreeCADGui
from Model3D.Command3D.Model3DCommand.BaseUI import BaseDialogMain
from Model3D.Tools import Tools3D, ObjectTools


class ShowDialog(BaseDialogMain.BasePhysicsDialog):
    def __init__(self, obj, isNew=False, parent=None):
        BaseDialogMain.BasePhysicsDialog.__init__(self, obj, isNew, parent)

    def setUI(self):
        self.ui = VectorDialog.Ui_Dialog()
        self.ui.setupUi(self)

    def loadDialog(self):
        try:
            self.default_list = ["OSYS$MIDPLANE1", "OSYS$MIDPLANE2", "OSYS$MIDPLANE3"]
            # 对话框的初始化
            self.refreshCombox()
            self.initObservationField()
            self.initTimer()
            # 正投影面下拉框选择事件
            self.ui.ComboBox_Shadow.currentIndexChanged.connect(self.ComboBox_Shadow_clicked)
            self.ui.checkBox_vector.stateChanged.connect(self.checkBoxVector)

            self.ui.LineEdit_start_x.textChanged.connect(self.LineEdit_start_x_textChanged)
            self.ui.LineEdit_start_y.textChanged.connect(self.LineEdit_start_y_textChanged)
            self.ui.LineEdit_start_z.textChanged.connect(self.LineEdit_start_z_textChanged)
            self.ui.radioButton_x.clicked.connect(self.radioButton_clicked)
            self.ui.radioButton_y.clicked.connect(self.radioButton_clicked)
            self.ui.radioButton_z.clicked.connect(self.radioButton_clicked)

            # 根据坐标系初始化面板
            Tools3D.switchPointLabel(self.ui)
            Tools3D.switchRadioButtonLabel(self.ui)

        except:
            Tools3D.sayz("error:" + traceback.format_exc())

    def getInfoFromObj(self):
        try:
            self.ui.le_name.setText(self.obj.Label)
            Tools3D.setCoorToUI(self.ui, self.obj)
            Tools3D.setRadioButtonToUI(self.ui, self.obj)

            itemIndex = self.ui.ComboBox_Shadow.findText(str(self.obj.orthogonalProjectionPlane))
            self.ui.ComboBox_Shadow.setCurrentIndex(itemIndex)

            itemIndex1 = self.ui.ComboBox_start.findText(str(self.obj.point1_name))
            self.ui.ComboBox_start.setCurrentIndex(itemIndex1)

            itemIndex2 = self.ui.ComboBox_end.findText(str(self.obj.point2_name))
            self.ui.ComboBox_end.setCurrentIndex(itemIndex2)

            # 观测场1
            itemIndex3 = self.ui.ComboBox_C1.findText(str(self.obj.observationField1))
            self.ui.ComboBox_C1.setCurrentIndex(itemIndex3)
            # 观测场2
            itemIndex4 = self.ui.ComboBox_C2.findText(str(self.obj.observationField2))
            self.ui.ComboBox_C2.setCurrentIndex(itemIndex4)
            # 定时器
            itemIndex5 = self.ui.ComboBox_timer.findText(str(self.obj.timer))
            self.ui.ComboBox_timer.setCurrentIndex(itemIndex5)

            self.ui.checkBox_vector.setChecked(self.obj.isVectorNumber)
            self.ui.le_SL1.setText(self.obj.vectorNumber1)
            self.ui.le_SL2.setText(self.obj.vectorNumber2)
            self.ComboBox_Shadow_clicked()

            if self.ui.ComboBox_Shadow.currentIndex() == 0:
                self.radioButton_clicked()

        except AttributeError:
            Tools3D.sayz("Vector--异常--在读取Object属性时出现异常")
            Tools3D.sayz(traceback.format_exc())
        except Exception as e:
            Tools3D.sayz("Vector--" + str(e))
        else:
            Tools3D.sayz("Vector--成功--读取Object信息")

    def setInfoToObj(self):
        try:
            # Tools3D.setLabelToObj(self.obj, self.ui.le_name.text())
            self.obj.Label = Tools3D.setLabel(self.ui.le_name.text())
            self.obj.orthogonalProjectionPlane = self.ui.ComboBox_Shadow.currentText()
            Tools3D.getUICoordinate(self.obj, self.ui)
            Tools3D.getUIRadioButton(self.obj, self.ui)

            self.obj.point1_name = self.ui.ComboBox_start.currentText()
            self.obj.point2_name = self.ui.ComboBox_end.currentText()

            self.obj.observationField1 = self.ui.ComboBox_C1.currentText()
            self.obj.observationField2 = self.ui.ComboBox_C2.currentText()

            self.obj.timer = self.ui.ComboBox_timer.currentText()
            self.obj.isVectorNumber = self.ui.checkBox_vector.isChecked()
            self.obj.vectorNumber1 = self.ui.le_SL1.text()
            self.obj.vectorNumber2 = self.ui.le_SL2.text()

        except:
            Tools3D.sayz("error:" + traceback.format_exc())

    def refreshCombox(self):
        try:
            ComboBox_Shadow_list = []
            for i in self.default_list:
                self.ui.ComboBox_Shadow.addItem(i)
            for i in range(self.ui.ComboBox_Shadow.count()):
                ComboBox_Shadow_list.append(self.ui.ComboBox_Shadow.itemText(i))

            areaList = ObjectTools.getLabelsByType(ObjectTools.ObjectType.Area_Conformal)
            for i in areaList:
                if i not in ComboBox_Shadow_list:
                    self.ui.ComboBox_Shadow.addItem(i)
        except:
            Tools3D.sayz("error:" + traceback.format_exc())

    def initTimer(self):
        try:
            Timer_list = []
            for i in range(self.ui.ComboBox_timer.count()):
                Timer_list.append(self.ui.ComboBox_timer.itemText(i))

            # defTimerList = ObjectTools.getLabelsByType(ObjectTools.ObjectType.DefaultTimer)
            timerList = ObjectTools.getLabelsByType(ObjectTools.ObjectType.CustomTimer)
            # allTimerList = defTimerList + timerList
            for i in timerList:
                if i not in Timer_list:
                    self.ui.ComboBox_timer.addItem(i)
        except:
            Tools3D.sayz("error:" + traceback.format_exc())

    def ComboBox_Shadow_clicked(self):
        try:
            if self.ui.ComboBox_Shadow.currentIndex() == 0:
                Tools3D.setCoordEnabled(self.ui, ObjectTools.ObjectType.Area_Conformal)
            else:
                objName = self.ui.ComboBox_Shadow.currentText()
                if objName in self.default_list:
                    pass
                else:
                    Tools3D.setModelCoordinate(self.ui, objName)
                Tools3D.setIsEdit(self.ui, False)
        except:
            Tools3D.sayz("error:" + traceback.format_exc())

    # x法向修改时，修改起点即修改终点
    def LineEdit_start_x_textChanged(self):
        if not self.ui.LineEdit_end_x.isEnabled():
            self.ui.LineEdit_end_x.setText(self.ui.LineEdit_start_x.text())

    # y法向修改时，修改起点即修改终点
    def LineEdit_start_y_textChanged(self):
        if not self.ui.LineEdit_end_y.isEnabled():
            self.ui.LineEdit_end_y.setText(self.ui.LineEdit_start_y.text())

    # z法向修改时，修改起点即修改终点
    def LineEdit_start_z_textChanged(self):
        if not self.ui.LineEdit_end_z.isEnabled():
            self.ui.LineEdit_end_z.setText(self.ui.LineEdit_start_z.text())

    # 点击法向按钮
    def radioButton_clicked(self):
        if self.ui.radioButton_x.isChecked():
            self.ui.LineEdit_end_x.setEnabled(False)
            self.ui.LineEdit_end_y.setEnabled(True)
            self.ui.LineEdit_end_z.setEnabled(True)
            self.ui.LineEdit_end_x.setText(self.ui.LineEdit_start_x.text())
        elif self.ui.radioButton_y.isChecked():
            self.ui.LineEdit_end_y.setEnabled(False)
            self.ui.LineEdit_end_x.setEnabled(True)
            self.ui.LineEdit_end_z.setEnabled(True)
            self.ui.LineEdit_end_y.setText(self.ui.LineEdit_start_y.text())
        elif self.ui.radioButton_z.isChecked():
            self.ui.LineEdit_end_z.setEnabled(False)
            self.ui.LineEdit_end_x.setEnabled(True)
            self.ui.LineEdit_end_y.setEnabled(True)
            self.ui.LineEdit_end_y.setText(self.ui.LineEdit_start_y.text())
        else:
            pass

    def initObservationField(self):
        list = ["E1", "E2", "E3", "B1", "B2", "B3", "J1", "J2", "J3", "Q0",
                "E1AV", "E2AV", "E3AV", "B1AV", "B2AV", "B3AV", "B1ST", "B2ST",
                "B3ST", "PHST", "|B|", "|E|"]
        for i in range(0, len(list)):
            self.ui.ComboBox_C1.addItem(list[i])
            self.ui.ComboBox_C2.addItem(list[i])

    def checkBoxVector(self):
        self.ui.le_SL1.setEnabled(self.ui.checkBox_vector.isChecked())
        self.ui.le_SL2.setEnabled(self.ui.checkBox_vector.isChecked())
