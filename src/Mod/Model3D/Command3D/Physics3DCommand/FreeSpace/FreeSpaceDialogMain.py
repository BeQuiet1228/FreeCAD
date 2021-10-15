# -*- coding: utf-8 -*-
import FreeCADGui
import FreeCAD
from Model3D.Tools import Tools3D,ObjectTools
from Model3D.Command3D.Model3DCommand.BaseUI import BaseDialogMain
import FreeSpaceDialog


class ShowDialog(BaseDialogMain.BasePhysicsDialog):
    def __init__(self, obj, isNew=False, parent=None):
        BaseDialogMain.BasePhysicsDialog.__init__(self, obj, isNew, parent)

    def setUI(self):
        self.ui = FreeSpaceDialog.Ui_Dialog_FreeDlg()
        self.ui.setupUi(self)

    def loadDialog(self):
        """
        此处写对话框的逻辑,注意异常处理
        """
        try:
            #代码补全
            self.defaultValue = ["OSYS$VOLUME"]
            # 这段代码暂时注释
            # CompleterTools.setLineEditsCompleter(CompleterTools.getAllLineEdits(self.ui))
            self.ui.radioButton_forward.setChecked(True)
            # 获取当前坐标系及坐标系单位

            Tools3D.switchPointLabel(self.ui)
            Tools3D.switchRadioButtonLabel(self.ui)
            Tools3D.switchCheckLabel(self.ui)

            self.ui.checkBox_x.clicked.connect(self.checkBox_x_clicked)
            self.ui.checkBox_y.clicked.connect(self.checkBox_y_clicked)
            self.ui.checkBox_z.clicked.connect(self.checkBox_z_clicked)
            self.ui.ComboBox_Absorption.setCurrentIndex(1)
            self.ui.checkBox_vport.clicked.connect(self.checkBox_vport_clicked)

            # 刷新下拉框
            self.refreshCombox()
            # 正投影面下拉框选择事件
            self.ui.ComboBox_Shadow.currentIndexChanged.connect(self.ComboBox_Shadow_clicked)
            self.ComboBox_Shadow_clicked()

        except:
            import traceback
            Tools3D.sayz("error:" + traceback.format_exc())

    def refreshCombox(self):
        '''
        每次加载窗口时都要重新加载下拉列表，以实现动态加载
        一般来说就是ComboBox_Shadow_list需要动态刷新
        '''
        ComboBox_Shadow_list = []
        for i in range(self.ui.ComboBox_Shadow.count()):
            ComboBox_Shadow_list.append(self.ui.ComboBox_Shadow.itemText(i))
        volumeList = ObjectTools.getLabelsByType(ObjectTools.ObjectType.Vol_Conformal)
        volumeList.append("OSYS$VOLUME")
        for i in volumeList:
            if i not in ComboBox_Shadow_list:
                self.ui.ComboBox_Shadow.addItem(i)

    def ComboBox_Shadow_clicked(self):
        if self.ui.ComboBox_Shadow.currentIndex() == 0:
            # Tools3D.setCoordEnabled(self.ui, ObjectTools.ObjectType.Vol_Conformal)
            self.ui.LineEdit_start_x.setEnabled(True)
            self.ui.LineEdit_start_y.setEnabled(True)
            self.ui.LineEdit_start_z.setEnabled(True)
            self.ui.LineEdit_end_x.setEnabled(True)
            self.ui.LineEdit_end_y.setEnabled(True)
            self.ui.LineEdit_end_z.setEnabled(True)
        else:
            objName = self.ui.ComboBox_Shadow.currentText()
            if objName in self.defaultValue:
                pass
            else:
                Tools3D.setModelCoordinate(self.ui, objName)
            self.ui.LineEdit_start_x.setEnabled(False)
            self.ui.LineEdit_start_y.setEnabled(False)
            self.ui.LineEdit_start_z.setEnabled(False)
            self.ui.LineEdit_end_x.setEnabled(False)
            self.ui.LineEdit_end_y.setEnabled(False)
            self.ui.LineEdit_end_z.setEnabled(False)
            # Tools3D.setIsEdit(self.ui, False)

    def getInfoFromObj(self):
        """
        从obj获取数据加载到对话框、注意异常处理
        """
        try:
            self.ui.LineEdit_Name.setText(self.obj.Label)
            self.ui.ComboBox_Shadow.setCurrentIndex(
                self.ui.ComboBox_Shadow.findText(self.obj.orthogonalProjectionPlane))
            Tools3D.setCoorToUI(self.ui, self.obj)
            Tools3D.setRadioButtonToUI(self.ui, self.obj)
            Tools3D.setGridToUI(self.ui, self.obj)
            self.ui.ComboBox_Absorption.setCurrentIndex(self.ui.ComboBox_Absorption.findText(self.obj.absorb))
            # 自定义传导率
            self.ui.checkBox_vport.setChecked(self.obj.isCustomConductivity)
            self.ui.LineEdit_vport.setEnabled(self.obj.isCustomConductivity)
            self.ui.LineEdit_vport.setText(self.obj.customConductivity)
            # DX编辑框
            self.checkBox_x_clicked()
            self.checkBox_y_clicked()
            self.checkBox_z_clicked()
            # 正向反向选择
            if self.obj.isNegative == True:
                self.ui.radioButton_opposite.setChecked(True)
            if self.obj.isPositive == True:
                self.ui.radioButton_forward.setChecked(True)
            self.ComboBox_Shadow_clicked()

        except KeyError as reason:
            Tools3D.sayz("!!!Error:KeyError,Maybe lack of key:%s" % str(reason))

    def setInfoToObj(self):
        """
        从对话框读取数据，设置obj的属性值
        """
        try:
            self.obj.orthogonalProjectionPlane = self.ui.ComboBox_Shadow.currentText()
            Tools3D.getUICoordinate(self.obj, self.ui)
            Tools3D.getUIRadioButton(self.obj, self.ui)

            # 法向选择
            Tools3D.getUICoordinate(self.obj, self.ui)
            # 正向反向选择
            self.obj.isNegative = self.ui.radioButton_opposite.isChecked()
            self.obj.isPositive = self.ui.radioButton_forward.isChecked()
            self.obj.absorb = self.ui.ComboBox_Absorption.currentText()
            # 自定义传导率
            self.obj.isCustomConductivity = self.ui.checkBox_vport.isChecked()
            self.obj.customConductivity = self.ui.LineEdit_vport.text()
            # DX编辑框
            Tools3D.getUIGrid(self.obj, self.ui)

        except:
            import traceback
            Tools3D.sayz("error:" + traceback.format_exc())
        pass

    def setPrivateInfoToObj(self):
        pass

    def checkBox_x_clicked(self):
        self.ui.LineEdit_DX1.setEnabled(self.ui.checkBox_x.isChecked())
    def checkBox_y_clicked(self):
        self.ui.LineEdit_DX2.setEnabled(self.ui.checkBox_y.isChecked())
    def checkBox_z_clicked(self):
        self.ui.LineEdit_DX3.setEnabled(self.ui.checkBox_z.isChecked())
    def checkBox_vport_clicked(self):
        self.ui.LineEdit_vport.setEnabled(self.ui.checkBox_vport.isChecked())

