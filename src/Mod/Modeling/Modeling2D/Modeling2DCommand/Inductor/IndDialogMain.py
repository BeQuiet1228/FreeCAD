# -*- coding: utf-8 -*-
import IndDialog
from PySide import QtGui
import FreeCAD
import FreeCADGui
 
from Modeling.Modeling2D.Tools.Tools2D import sayz
from Modeling.Common.Tools import DocumentTools,ObjectsTools
from Physics.PhysicsTools import CompleterTools
from Modeling.Modeling2D.Tools import Tools2D


class ShowDialog(QtGui.QDialog):
    def __init__(self, obj, isNew=False, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = IndDialog.Ui_Dialog_IndDlg()
        self.ui.setupUi(self)
        self.obj = obj
        self.isKeepData = False
        self.isNew = isNew
        self.initDialog()
        self.loadData()
        self.setModal(False)

    def initDialog(self):
        try:
            self.defaultValue = []
            #代码补全
            # 这段代码暂时注释
            # CompleterTools.setLineEditsCompleter(CompleterTools.getAllLineEdits(self.ui))
            self.ui.pb_cancel.clicked.connect(self.onCancel)
            self.ui.pb_ok.clicked.connect(self.onConfirm)
            # 输入框变化时
            self.ui.LineEdit_start_x.textChanged.connect(self.LineEdit_start_x_textChanged)
            self.ui.LineEdit_start_y.textChanged.connect(self.LineEdit_start_y_textChanged)
            # self.ui.LineEdit_start_z.textChanged.connect(self.LineEdit_start_z_textChanged)
            self.ui.radioButton_x.clicked.connect(self.radioButton_x_clicked)
            self.ui.radioButton_y.clicked.connect(self.radioButton_y_clicked)
            # self.ui.radioButton_z.clicked.connect(self.radioButton_z_clicked)
            self.ui.checkBox_induc.clicked.connect(self.checkBox_induc_clicked)
            self.ui.LineEdit_end_y.setEnabled(True)
            # 获取当前坐标系及坐标系单位
            coord = Tools2D.getCoordinate()
            self.x = coord[0]
            self.y = coord[1]
            # self.z = coord[2]
            # self.x_unit = coord[3]
            # self.y_unit = coord[4]
            # self.z_unit = coord[5]

            # #修改线圈直径的单位
            # diam = 1.0
            # unit = FreeCAD.Units.getDefaultUnits()
            # if unit[0]==0:
            #     self.ui.LineEdit_diam.setText(str(diam)+"mm")
            # elif unit[0]==1:
            #     self.ui.LineEdit_diam.setText(str(diam/10)+"cm")
            # else:
            #     self.ui.LineEdit_diam.setText(str(diam/1000)+"m")

            # 根据坐标系初始化面板
            self.ui.label_X.setText(self.x)
            self.ui.label_Y.setText(self.y)
            # self.ui.label_Z.setText(self.z)
            self.ui.radioButton_x.setText(self.x)
            self.ui.radioButton_y.setText(self.y)

            # self.ui.LineEdit_start_x.setText("0" + self.x_unit)
            # self.ui.LineEdit_start_y.setText("0" + self.y_unit)
            # self.ui.LineEdit_end_x.setText("0" + self.x_unit)
            # self.ui.LineEdit_end_y.setText("0" + self.y_unit)
            # 关闭Z轴设置
            self.ui.label_Z.hide()
            self.ui.radioButton_z.hide()
            self.ui.LineEdit_start_z.hide()
            self.ui.LineEdit_end_z.hide()
            # 刷新下拉框
            self.refreshCombo()
            # 正投影面下拉框选择事件
            self.ui.ComboBox_Shadow.currentIndexChanged.connect(self.ComboBox_Shadow_clicked)
        except:
            import traceback
            sayz("error:" + traceback.format_exc())

    def refreshCombo(self):
        # 每次加载窗口时都要重新加载下拉列表，以实现动态加载
        ComboBox_Shadow_list=[]
        for i in range(self.ui.ComboBox_Shadow.count()):
            ComboBox_Shadow_list.append(self.ui.ComboBox_Shadow.itemText(i))
        volumeList = Tools2D.getAllConformalLineLabel()
        for i in volumeList:
            if i not in ComboBox_Shadow_list:
                self.ui.ComboBox_Shadow.addItem(i)           

    def ComboBox_Shadow_clicked(self):
        try:
            ObjectsTools.findObjByLabelWithoutOrderAndVisible(self.ui.ComboBox_Shadow.currentIndex())
            if self.ui.ComboBox_Shadow.currentIndex() == 0:
                # self.ui.LineEdit_start_x.setText(self.obj.point1_X)
                # self.ui.LineEdit_start_y.setText(self.obj.point1_Y)
                # self.ui.LineEdit_end_x.setText(self.obj.point2_X)
                # self.ui.LineEdit_end_y.setText(self.obj.point2_Y)

                self.ui.LineEdit_start_x.setEnabled(True)
                self.ui.LineEdit_start_y.setEnabled(True)
                if self.ui.radioButton_x.isChecked():
                    self.ui.LineEdit_end_x.setEnabled(False)
                    self.ui.LineEdit_end_y.setEnabled(True)
                elif self.ui.radioButton_y.isChecked():
                    self.ui.LineEdit_end_x.setEnabled(True)
                    self.ui.LineEdit_end_y.setEnabled(False)
                self.ui.radioButton_x.setEnabled(True)
                self.ui.radioButton_y.setEnabled(True)
            else:
                objName = self.ui.ComboBox_Shadow.currentText()
                if objName in self.defaultValue:
                    pass
                else:
                    modelData = Tools2D.getValueOfAreaObjByLabel(objName)
                    self.ui.LineEdit_start_x.setText(modelData["point1.x"])
                    self.ui.LineEdit_start_y.setText(modelData["point1.y"])
                    self.ui.LineEdit_end_x.setText(modelData["point2.x"])
                    self.ui.LineEdit_end_y.setText(modelData["point2.y"])
                    # 法向
                    if modelData["normal"] == "X" or modelData["normal"] == "x":
                        self.ui.radioButton_x.setChecked(True)
                    elif modelData["normal"] == "Y" or modelData["normal"] == "y":
                        self.ui.radioButton_y.setChecked(True)
                    else:
                        Tools2D.sayz("get Area_Conformal error")
                self.ui.LineEdit_start_x.setEnabled(False)
                self.ui.LineEdit_start_y.setEnabled(False)
                self.ui.LineEdit_end_x.setEnabled(False)
                self.ui.LineEdit_end_y.setEnabled(False)

                # 法向不可编辑
                self.ui.radioButton_x.setEnabled(False)
                self.ui.radioButton_y.setEnabled(False)
        except:
            import traceback
            Tools2D.sayz("error:" + traceback.format_exc())

    # 点击取消按钮关闭窗口
    def onCancel(self):
        self.isKeepData = False
        self.close()

    # 点击确定按钮
    def onConfirm(self):
        self.isKeepData = True
        self.close()

    def loadData(self): 
        try:
            self.ui.LineEdit_Name.setText(self.obj.Label)
            self.ui.ComboBox_Shadow.setCurrentIndex(self.ui.ComboBox_Shadow.findText(self.obj.inductorType))
            self.ui.LineEdit_start_x.setText(self.obj.point1_X)
            self.ui.LineEdit_start_y.setText(self.obj.point1_Y)

            self.ui.LineEdit_end_x.setText(self.obj.point2_X)
            self.ui.LineEdit_end_y.setText(self.obj.point2_Y)
            # 法向选择
            self.ui.radioButton_x.setChecked(self.obj.isCheckNormal1)
            self.ui.radioButton_y.setChecked(self.obj.isCheckNormal2)
            # 线圈直径
            self.ui.LineEdit_diam.setText(self.obj.coilDiameter)
            # 自感系数
            self.ui.checkBox_induc.setChecked(self.obj.isCheckSelfInductor)
            self.ui.LineEdit_induc.setEnabled(self.obj.isCheckSelfInductor)
            self.ui.LineEdit_induc.setText(self.obj.selfInductorCoefficient)
        except KeyError as reason:
            sayz("!!!Error:KeyError,Maybe lack of key:%s"%str(reason))              

    def keepData(self):
        try:
            # 名字
            Tools2D.setLabelToObj(self.obj, self.ui.LineEdit_Name.text())
            self.obj.inductorType = self.ui.ComboBox_Shadow.currentText()
            self.obj.point1_X = self.ui.LineEdit_start_x.text()
            self.obj.point1_Y = self.ui.LineEdit_start_y.text()
            self.obj.point2_X = self.ui.LineEdit_end_x.text()
            self.obj.point2_Y = self.ui.LineEdit_end_y.text()
            # 法向选择
            self.obj.isCheckNormal1 = self.ui.radioButton_x.isChecked()    
            self.obj.isCheckNormal2 = not(self.obj.isCheckNormal1)     

            # 线圈直径
            self.obj.coilDiameter = self.ui.LineEdit_diam.text()
            # 自感系数
            self.obj.isCheckSelfInductor = self.ui.checkBox_induc.isChecked()
            self.obj.selfInductorCoefficient = self.ui.LineEdit_induc.text()
            # Comment[DlgData.id] = DlgData.data
        except:
            import traceback
            sayz("error:" + traceback.format_exc())

    # x法向修改时，修改起点即修改终点
    def LineEdit_start_x_textChanged(self):
        if not self.ui.LineEdit_end_x.isEnabled():
            self.ui.LineEdit_end_x.setText(self.ui.LineEdit_start_x.text())

    # y法向修改时，修改起点即修改终点
    def LineEdit_start_y_textChanged(self):
        if not self.ui.LineEdit_end_y.isEnabled():
            self.ui.LineEdit_end_y.setText(self.ui.LineEdit_start_y.text())

    # 点击法向x按钮
    def radioButton_x_clicked(self):
        self.ui.LineEdit_end_x.setEnabled(False)
        self.ui.LineEdit_end_y.setEnabled(True)
        self.ui.LineEdit_end_z.setEnabled(False)
        self.ui.LineEdit_end_x.setText(self.ui.LineEdit_start_x.text())
        self.ui.LineEdit_end_z.setText(self.ui.LineEdit_start_z.text())

    # 点击法向y按钮
    def radioButton_y_clicked(self):
        self.ui.LineEdit_end_y.setEnabled(False)
        self.ui.LineEdit_end_x.setEnabled(True)
        self.ui.LineEdit_end_z.setEnabled(False)
        self.ui.LineEdit_end_y.setText(self.ui.LineEdit_start_y.text())
        self.ui.LineEdit_end_z.setText(self.ui.LineEdit_start_z.text())

    def checkBox_induc_clicked(self):
        self.ui.LineEdit_induc.setEnabled(self.ui.checkBox_induc.isChecked())

    def closeEvent(self, event):
        if self.isKeepData:
            self.keepData()
            FreeCADGui.runCommand("CreateM2D")
        else:
            if self.isNew:
                FreeCAD.ActiveDocument.removeObject(self.obj.Label)
