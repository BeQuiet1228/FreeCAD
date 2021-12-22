# -*- coding: utf-8 -*-
import FreeCADGui
import FreeCAD
from Model3D.Tools import Tools3D, ObjectTools
from Model3D.Command3D.Model3DCommand.BaseUI import BaseDialogMain
import SymtryDialog


class ShowDialog(BaseDialogMain.BasePhysicsDialog):
    def __init__(self, obj, isNew=False, parent=None):
        BaseDialogMain.BasePhysicsDialog.__init__(self, obj, isNew, parent)

    def setUI(self):
        self.ui = SymtryDialog.Ui_Dialog_SymDlg()
        self.ui.setupUi(self)

    def loadDialog(self):
        """
        此处写对话框的逻辑,注意异常处理
        """
        try:
            #代码补全
            self.defaultValue = ["OSYS$MIDPLANE1","OSYS$MIDPLANE2","OSYS$MIDPLANE3"]
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

            self.ui.LineEdit_start_x.textChanged.connect(self.LineEdit_start_x_textChanged)
            self.ui.LineEdit_start_y.textChanged.connect(self.LineEdit_start_y_textChanged)
            self.ui.LineEdit_start_z.textChanged.connect(self.LineEdit_start_z_textChanged)

            self.ui.radioButton_x.clicked.connect(self.radioButton_clicked)
            self.ui.radioButton_y.clicked.connect(self.radioButton_clicked)
            self.ui.radioButton_z.clicked.connect(self.radioButton_clicked)
            # 刷新下拉框
            self.refreshCombox()
            # 正投影面下拉框选择事件
            self.ui.ComboBox_Shadow.currentIndexChanged.connect(self.ComboBox_Shadow_clicked)
            self.ComboBox_Shadow_clicked()

        except:
            import traceback
            Tools3D.sayz("error:" + traceback.format_exc())

    def onButtonClick(self, n):
        Tools3D.sayz("Button {0} is click".format(n))

    def refreshCombox(self):
        '''
        每次加载窗口时都要重新加载下拉列表，以实现动态加载
        一般来说就是ComboBox_Shadow_list需要动态刷新
        '''
        ComboBox_Shadow_list = []
        ComboBox_type_list = []
        for i in range(self.ui.ComboBox_Shadow.count()):
            ComboBox_Shadow_list.append(self.ui.ComboBox_Shadow.itemText(i))
        for i in range(self.ui.ComboBox_type.count()):
            ComboBox_type_list.append(self.ui.ComboBox_type.itemText(i))
        Orthogonal_list = ObjectTools.getLabelsByType(ObjectTools.ObjectType.Area_Conformal)
        Orthogonal_list.append("OSYS$MIDPLANE1")
        Orthogonal_list.append("OSYS$MIDPLANE2")
        Orthogonal_list.append("OSYS$MIDPLANE3")
        for i in Orthogonal_list:
            if i not in ComboBox_Shadow_list:
                self.ui.ComboBox_Shadow.addItem(i)
            if i not in ComboBox_type_list:
                self.ui.ComboBox_type.addItem(i)

    def ComboBox_Shadow_clicked(self):
        if self.ui.ComboBox_Shadow.currentIndex() == 0:
            Tools3D.setCoordEnabled(self.ui, ObjectTools.ObjectType.Area_Conformal)
        else:
            objName = self.ui.ComboBox_Shadow.currentText()
            if objName in self.defaultValue:
                pass
            else:
                Tools3D.setModelCoordinate(self.ui, objName)
            Tools3D.setIsEdit(self.ui, False)

            # 对称类型可选
            self.ui.ComboBox_type.setEnabled(True)
            # 法向周期不可编辑
            self.ui.LineEdit_Normal.setEnabled(False)
            # 法向不可编辑
            self.ui.radioButton_x.setEnabled(False)
            self.ui.radioButton_y.setEnabled(False)
            self.ui.radioButton_z.setEnabled(False)

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
            # 当选中的正交投影面的坐标改变了，此处要刷新一下
            self.ComboBox_Shadow_clicked()
            # 对称类型
            self.ui.ComboBox_symmetric.setCurrentIndex(
                self.ui.ComboBox_symmetric.findText(str(self.obj.symmetricalType)))
            self.ui.ComboBox_type.setCurrentIndex(self.ui.ComboBox_type.findText(str(self.obj.assignType)))
            # 法向周期
            self.ui.LineEdit_Normal.setText(self.obj.theNormalCycle)
            self.checkBox_x_clicked()
            self.checkBox_y_clicked()
            self.checkBox_z_clicked()

            if self.ui.ComboBox_Shadow.currentIndex() == 0:
                self.radioButton_clicked()

            # 正向反向选择
            if self.obj.isNegative == True:
                self.ui.radioButton_opposite.setChecked(True)
            if self.obj.isPositive == True:
                self.ui.radioButton_forward.setChecked(True)
        except:
            import traceback
            Tools3D.sayz("error:" + traceback.format_exc())

    def setInfoToObj(self):
        """
        从对话框读取数据，设置obj的属性值
        """
        try:
            self.obj.orthogonalProjectionPlane = self.ui.ComboBox_Shadow.currentText()
            Tools3D.getUICoordinate(self.obj, self.ui)
            Tools3D.getUIRadioButton(self.obj, self.ui)
            # 法向选择
            # 正向反向选择
            self.obj.isNegative = self.ui.radioButton_opposite.isChecked()
            self.obj.isPositive = self.ui.radioButton_forward.isChecked()
            # 对称类型
            self.obj.symmetricalType = self.ui.ComboBox_symmetric.currentText()
            self.obj.assignType = self.ui.ComboBox_type.currentText()
            # 法向周期
            self.obj.theNormalCycle = self.ui.LineEdit_Normal.text()
            # DX编辑框
            Tools3D.getUIGrid(self.obj, self.ui)
            temp = ""
            if self.obj.symmetricalType == "周期对称" or self.obj.symmetricalType == u"周期对称":
                coodinate = FreeCAD.ActiveDocument.CoordinateSystem
                if self.obj.isCheckNormal1:
                    temp = self.obj.point1_X.replace(" ", "") + "+" + self.obj.theNormalCycle.replace(" ", "")
                    self.obj.setExpression("helper", temp)
                elif self.obj.isCheckNormal2:
                    temp = self.obj.point1_Y.replace(" ", "") + "+" + self.obj.theNormalCycle.replace(" ", "")
                    if coodinate == u'Polar':
                        self.obj.setExpression("helper1", temp)
                    else:
                        self.obj.setExpression("helper", temp)
                elif self.obj.isCheckNormal3:
                    temp = self.obj.point1_Z.replace(" ", "") + "+" + self.obj.theNormalCycle.replace(" ", "")
                    if coodinate == u"Cylindrical":
                        self.obj.setExpression("helper1", temp)
                    else:
                        self.obj.setExpression("helper", temp)
                # self.obj.setExpression("helper", temp)
        except:
            import traceback
            Tools3D.sayz("error:" + traceback.format_exc())

    def setPrivateInfoToObj(self):
        pass

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
            self.ui.LineEdit_end_z.setText(self.ui.LineEdit_start_z.text())

    def checkBox_x_clicked(self):
        if self.ui.checkBox_x.isChecked():
            self.ui.LineEdit_DX1.setEnabled(True)
        else:
            self.ui.LineEdit_DX1.setEnabled(False)

    def checkBox_y_clicked(self):
        if self.ui.checkBox_y.isChecked():
            self.ui.LineEdit_DX2.setEnabled(True)
        else:
            self.ui.LineEdit_DX2.setEnabled(False)

    def checkBox_z_clicked(self):
        if self.ui.checkBox_z.isChecked():
            self.ui.LineEdit_DX3.setEnabled(True)
        else:
            self.ui.LineEdit_DX3.setEnabled(False)