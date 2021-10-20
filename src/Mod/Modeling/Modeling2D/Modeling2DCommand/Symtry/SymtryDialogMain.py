#-*- coding: utf-8 -*-
import SymtryDialog
from PySide import QtGui
import FreeCAD
import FreeCADGui
from Physics.PhysicsCommand import Simulation
from Physics.PhysicsCommand.DlgData import sayz
from Modeling.Common.Tools import DocumentTools,ObjectsTools
from Physics.PhysicsTools import CompleterTools
from Modeling.Modeling2D.Tools import Tools2D


class ShowDialog(QtGui.QDialog):
    def __init__(self, obj, isNew=False, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = SymtryDialog.Ui_Dialog_SymDlg()
        self.ui.setupUi(self)
        self.obj = obj
        self.isNew = isNew
        self.initDialog()
        self.loadData()
        self.setModal(False)
        self.isKeepData = False

    def initDialog(self):
        try:
            #代码补全
            self.defaultValue = []
            # 这段代码暂时注释
            # CompleterTools.setLineEditsCompleter(CompleterTools.getAllLineEdits(self.ui))
            self.ui.pb_cancel.clicked.connect(self.onCancel)
            self.ui.pb_ok.clicked.connect(self.onConfirm)
            self.ui.radioButton_forward.setChecked(True)
            # 获取当前坐标系及坐标系单位
            coord = Tools2D.getCoordinate()
            self.x = coord[0]
            self.y = coord[1]
            # self.z = coord[2]

            self.ui.LineEdit_Normal.setText("0")
            # self.ui.LineEdit_Normal.setEnabled(True)

            # 根据坐标系初始化面板
            self.ui.label_X.setText(self.x)
            self.ui.label_Y.setText(self.y)
            # self.ui.label_Z.setText(self.z)
            self.ui.radioButton_x.setText(self.x)
            self.ui.radioButton_y.setText(self.y)
            # self.ui.radioButton_z.setText(self.z)
            self.ui.checkBox_x.setText(self.x)
            self.ui.checkBox_y.setText(self.y)
            # self.ui.checkBox_z.setText(self.z)

            # 关闭Z轴设置
            self.ui.label_Z.hide()
            self.ui.radioButton_z.hide()
            self.ui.checkBox_z.hide()
            self.ui.LineEdit_start_z.hide()
            self.ui.LineEdit_end_z.hide()
            self.ui.LineEdit_DX3.hide()
            # 设置反向不可编辑
            self.ui.radioButton_opposite.setEnabled(False)

            self.ui.LineEdit_start_x.textChanged.connect(self.LineEdit_start_x_textChanged)
            self.ui.LineEdit_start_y.textChanged.connect(self.LineEdit_start_y_textChanged)

            self.ui.radioButton_x.clicked.connect(self.radioButton_x_clicked)
            self.ui.radioButton_y.clicked.connect(self.radioButton_y_clicked)

            self.ui.checkBox_x.clicked.connect(self.checkBox_x_clicked)
            self.ui.checkBox_y.clicked.connect(self.checkBox_y_clicked)

            # 刷新下拉框
            self.refreshCombox()
            # 正投影面下拉框选择事件
            self.ui.ComboBox_Shadow.currentIndexChanged.connect(self.ComboBox_Shadow_clicked)
             #用于判断是否进行名称更新
            # 对称类型的下拉框
            self.Symmetric()
            self.ui.ComboBox_symmetric.currentIndexChanged.connect(self.ComboBox_symmetric_clicked)
            self.flagUpdateItemName=False
            self.ComboBox_Shadow_clicked()
            # # 适配分辨率
            # from Physics.PhysicsCommand import AdaptiveDPIUtil
            # new_x, new_y = AdaptiveDPIUtil.get_new_dpi(self.width(), self.height())
            # self.resize(new_x, new_y)

        except:
            import traceback
            sayz("error:" + traceback.format_exc())

    def refreshCombox(self):  
        '''
        每次加载窗口时都要重新加载下拉列表，以实现动态加载
        一般来说就是ComboBox_Shadow_list需要动态刷新
        '''
        ComboBox_Shadow_list=[]
        ComboBox_type_list=[]
        for i in range(self.ui.ComboBox_Shadow.count()):
            ComboBox_Shadow_list.append(self.ui.ComboBox_Shadow.itemText(i))
        for i in range(self.ui.ComboBox_type.count()):
            ComboBox_type_list.append(self.ui.ComboBox_type.itemText(i))
        Orthogonal_list = Tools2D.getAllConformalLineLabel()
        for i in Orthogonal_list:
            if i not in ComboBox_Shadow_list:
                self.ui.ComboBox_Shadow.addItem(i)
            if i not in ComboBox_type_list:
                self.ui.ComboBox_type.addItem(i)                

    def ComboBox_Shadow_clicked(self):
        ObjectsTools.findObjByLabelWithoutOrderAndVisible(self.ui.ComboBox_Shadow.currentText())
        if self.ui.ComboBox_Shadow.currentIndex() == 0:
            self.ui.ComboBox_type.setEnabled(False)
            self.ui.LineEdit_start_x.setEnabled(True)
            self.ui.LineEdit_start_y.setEnabled(True)
            # self.ui.LineEdit_start_x.setText(self.obj.point1_X)
            # self.ui.LineEdit_start_y.setText(self.obj.point1_Y)
            # self.ui.LineEdit_end_x.setText(self.obj.point2_X)
            # self.ui.LineEdit_end_y.setText(self.obj.point2_Y)
            self.ui.radioButton_x.setEnabled(True)
            self.ui.radioButton_y.setEnabled(True)
            self.ui.LineEdit_end_x.setEnabled(not self.obj.isCheckNormal1)
            self.ui.LineEdit_end_y.setEnabled(not self.obj.isCheckNormal2)
            # if self.ui.radioButton_x.isChecked():
            #     self.ui.LineEdit_end_x.setEnabled(False)
            #     self.ui.LineEdit_end_y.setEnabled(True)
            # elif not self.ui.radioButton_x.isChecked():
            #     self.ui.LineEdit_end_x.setEnabled(True)
            #     self.ui.LineEdit_end_y.setEnabled(False)
        else:
            objName = self.ui.ComboBox_Shadow.currentText()
            if objName in self.defaultValue:
                pass
            else:
                modelData = Tools2D.getValueOfAreaObjByLabel(objName)
                self.ui.LineEdit_start_x.setText(str(modelData["point1.x"]))
                self.ui.LineEdit_start_y.setText(str(modelData["point1.y"]))
                self.ui.LineEdit_end_x.setText(str(modelData["point2.x"]))
                self.ui.LineEdit_end_y.setText(str(modelData["point2.y"]))
                # 法向
                if modelData["normal"] == "X" or modelData["normal"] == "x" or \
                        modelData["normal"] == "Z" or modelData["normal"] == "z":
                    self.ui.radioButton_x.setChecked(True)
                elif modelData["normal"] == "Y" or modelData["normal"] == "y" or \
                        modelData["normal"] == "R" or modelData["normal"] == "r":
                    self.ui.radioButton_y.setChecked(True)
                else:
                    Tools2D.sayz("get Area_Conformal error")
            self.ui.LineEdit_start_x.setEnabled(False)
            self.ui.LineEdit_start_y.setEnabled(False)
            self.ui.LineEdit_end_x.setEnabled(False)
            self.ui.LineEdit_end_y.setEnabled(False)
            # 对称类型可选
            self.ui.ComboBox_type.setEnabled(True)
            # 法向不可编辑
            self.ui.radioButton_x.setEnabled(False)
            self.ui.radioButton_y.setEnabled(False)

    def Symmetric(self):
        symmetric_list = [u"轴对称", u"镜像对称", u"周期对称"]
        for i in symmetric_list:
            self.ui.ComboBox_symmetric.addItem(i)

    def ComboBox_symmetric_clicked(self):
        if self.ui.ComboBox_symmetric.currentIndex() == 0:
            self.ui.LineEdit_Normal.setEnabled(False)
            self.ui.radioButton_opposite.setEnabled(False)
            self.ui.radioButton_forward.setChecked(True)
            # self.ui.radioButton_opposite.setChecked(False)
        elif self.ui.ComboBox_symmetric.currentIndex() == 1:
            self.ui.LineEdit_Normal.setEnabled(False)
            self.ui.radioButton_opposite.setEnabled(True)
        else:
            self.ui.LineEdit_Normal.setEnabled(True)
            self.ui.radioButton_opposite.setEnabled(False)
            self.ui.radioButton_forward.setChecked(True)
            # self.ui.radioButton_opposite.setChecked(False)

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
            self.ui.ComboBox_Shadow.setCurrentIndex(self.ui.ComboBox_Shadow.findText(str(self.obj.orthogonalProjectionPlane)))
            # 坐标
            self.ui.LineEdit_start_x.setText(self.obj.point1_X)
            self.ui.LineEdit_start_y.setText(self.obj.point1_Y)
            self.ui.LineEdit_end_x.setText(self.obj.point2_X)
            self.ui.LineEdit_end_y.setText(self.obj.point2_Y)
            # 法向选择
            self.ui.radioButton_x.setChecked(self.obj.isCheckNormal1)
            self.ui.radioButton_y.setChecked(self.obj.isCheckNormal2)
            self.ui.radioButton_opposite.setChecked(self.obj.isNegative)
            self.ui.radioButton_forward.setChecked(self.obj.isPositive)

            # self.ui.LineEdit_end_x.setEnabled(not self.obj.isCheckNormal1)
            # self.ui.LineEdit_end_y.setEnabled(not self.obj.isCheckNormal2)
            # # 正向反向选择
            # # if self.obj.isNegative == True:
            # #     self.ui.radioButton_opposite.setChecked(True)
            # if self.obj.isPositive == True:
            #     self.ui.radioButton_forward.setChecked(True)

            self.ui.ComboBox_type.setCurrentIndex(self.ui.ComboBox_type.findText(str(self.obj.assignType)))
            self.ui.ComboBox_symmetric.setCurrentIndex(self.ui.ComboBox_symmetric.findText(str(self.obj.symmetricalType)))
            # 法向周期
            self.ui.LineEdit_Normal.setText(self.obj.theNormalCycle)
            # DX编辑框
            self.ui.checkBox_x.setChecked(self.obj.isMarkX)  
            self.checkBox_x_clicked()
            self.ui.checkBox_y.setChecked(self.obj.isMarkY)
            self.checkBox_y_clicked()
            self.ui.LineEdit_DX1.setText(self.obj.MarkX)
            self.ui.LineEdit_DX2.setText(self.obj.MarkY)

        except KeyError as reason:
           Tools2D.sayz("!!!Error:KeyError,Maybe lack of key:%s"%str(reason))

    def keepData(self):
        try:
            # 名字
            Tools2D.setLabelToObj(self.obj, self.ui.LineEdit_Name.text())
            self.obj.orthogonalProjectionPlane = self.ui.ComboBox_Shadow.currentText()
            self.obj.point1_X = self.ui.LineEdit_start_x.text()
            self.obj.point1_Y = self.ui.LineEdit_start_y.text()
            self.obj.point2_X = self.ui.LineEdit_end_x.text()
            self.obj.point2_Y = self.ui.LineEdit_end_y.text()
            # 法向选择
            self.obj.isCheckNormal1 = self.ui.radioButton_x.isChecked()    
            self.obj.isCheckNormal2 = not self.ui.radioButton_x.isChecked()

            # 正向反向选择
            self.obj.isNegative = self.ui.radioButton_opposite.isChecked()
            self.obj.isPositive = self.ui.radioButton_forward.isChecked()
            # 对称类型
            self.obj.symmetricalType = self.ui.ComboBox_symmetric.currentText()                     
            self.obj.assignType = self.ui.ComboBox_type.currentText()
            # 法向周期
            self.obj.theNormalCycle = self.ui.LineEdit_Normal.text()
            # DX编辑框
            self.obj.isMarkX = self.ui.checkBox_x.isChecked()
            self.obj.isMarkY = self.ui.checkBox_y.isChecked()

            self.obj.MarkX = self.ui.LineEdit_DX1.text()
            self.obj.MarkY = self.ui.LineEdit_DX2.text()
            temp = ""
            if self.obj.symmetricalType == "周期对称" or self.obj.symmetricalType == u"周期对称":
                if self.obj.isCheckNormal1:
                    temp = self.obj.point1_X.replace(" ", "") + "+" + self.obj.theNormalCycle.replace(" ", "")
                else:
                    temp = self.obj.point1_Y.replace(" ", "") + "+" + self.obj.theNormalCycle.replace(" ", "")
                self.obj.setExpression("helper", temp)
        except:
            import traceback
            Tools2D.sayz("error:" + traceback.format_exc())
        pass

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
        self.ui.LineEdit_end_z.setEnabled(True)
        self.ui.LineEdit_end_x.setText(self.ui.LineEdit_start_x.text())

    # 点击法向y按钮
    def radioButton_y_clicked(self):
        self.ui.LineEdit_end_y.setEnabled(False)
        self.ui.LineEdit_end_x.setEnabled(True)
        self.ui.LineEdit_end_z.setEnabled(True)
        self.ui.LineEdit_end_y.setText(self.ui.LineEdit_start_y.text())

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

    # 点击关闭对话框，删除创建的对象
    def closeEvent(self, event):
        if self.isKeepData:
            self.keepData()
            FreeCADGui.runCommand("CreateM2D")
        else:
            if self.isNew:
                FreeCAD.ActiveDocument.removeObject(self.obj.Label)
