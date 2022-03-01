# -*- coding: utf-8 -*-
import traceback

import PySide
from PySide import QtGui, QtCore
# from Modeling.Modeling2D.Modeling2DCommand.Circular import CircularDialog
from Modeling.Modeling2D.Tools import Tools2D
import FreeCADGui
import FreeCAD
from Modeling.Modeling2D.Tools import CompleterTools
import customWidget


# 这是自定义属性的对话框
class CustomShowWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = customWidget.Ui_Form()
        self.ui.setupUi(self)


# 该类是所有模型相关类的父类，子类需要重写__init__、getInfoFromObj、setInfoToObj
class BaseModelDialog(QtGui.QDialog):
    """
    模型对话框类的父类
    """

    def __init__(self, obj, parent=None):
        """
        子类需要重写构造函数而不是继承该构造函数
        """
        QtGui.QDialog.__init__(self, parent)
        # 这里只是假设UI为圆形的UI
        # self.ui = CircularDialog.Ui_Circular()
        self.ui.setupUi(self)
        # width = self.ui.width()
        # height = self.ui.height()

        self.customAttribute = CustomShowWidget()

        self.setModal(False)
        self.obj = obj
        self.initDialog()
        self.getInfoFromObj()
        self.loadCustomData()
        self.isNew = False
        self.isKeepData = False

    def getInfoFromObj(self):
        """
        从Object获取信息，并且设置到Dialog
        子类需要重写该方法，注意异常处理，不要因为输出异常而打不开对话框
        """
        pass

    def setInfoToObj(self):
        """
        从Dialog获取信息，并且赋值到Object
        子类需要重写该方法，注意异常处理，不要因为输出异常而关不掉对话框
        """
        pass

    def initDialog(self):
        """
        初始化界面，设置界面逻辑，绑定信号与槽
        """
        # noinspection PyBroadException
        try:
            # 点线面坐标的代码补全
            CompleterTools.setLineEditsCompleter(CompleterTools.getAllLineEdits(self.ui))
            # 如果是point，那么对点调整视角将使程序崩溃
            if self.obj.Type == Tools2D.ObjectType.Point:
                pass
            else:
                if hasattr(self.obj, "ViewObject") and (not self.obj.ViewObject.Visibility):
                    self.obj.ViewObject.Visibility = True
                FreeCADGui.SendMsgToActiveView("ViewSelection")
            self.setAttributeToDlg()
            # 此处按钮命名需要修改
            self.ui.pb_ok.clicked.connect(self.slotOK)
            self.ui.pb_cancel.clicked.connect(self.slotCancel)
            self.ui.checkBox_isMarkX.stateChanged.connect(self.setIsMarkXState)
            self.ui.checkBox_isMarkY.stateChanged.connect(self.setIsMarkYState)
            # 获取当前坐标系及坐标系单位
            coord = Tools2D.getCoordinate()
            self.x = coord[0]
            self.y = coord[1]
            # 根据坐标系更新面板
            self.ui.label_x.setText(self.x)
            self.ui.label_y.setText(self.y)
            if hasattr(self.ui, "label_9"):
                self.ui.label_9.setText(self.x)
            if hasattr(self.ui, "label_10"):
                self.ui.label_10.setText(self.y)

            # @wangzhenguo 自定义属性对话框的逻辑
            if self.obj.Attribute == "Custom":
                self.customOption()
            self.ui.cb_attribute.currentIndexChanged.connect(self.customOption)

            self.customAttribute.ui.lineEdit_sigma2.hide()
            self.customAttribute.ui.lineEdit_sigma3.hide()
            self.customAttribute.ui.lineEdit_setEps2.hide()
            self.customAttribute.ui.lineEdit_setEps3.hide()
        except:
            Tools2D.sayz(traceback.format_exc())

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

    def setAttributeToDlg(self):
        """
        读取obj的Attribute并设置ui
        """

        if not hasattr(self.obj, "Attribute"):
            return

        if self.obj.Attribute == Tools2D.Attribute.NotDefine:
            self.ui.cb_attribute.setCurrentIndex(0)
        elif self.obj.Attribute == Tools2D.Attribute.Conductor:
            self.ui.cb_attribute.setCurrentIndex(1)
        elif self.obj.Attribute == Tools2D.Attribute.Custom:
            self.ui.cb_attribute.setCurrentIndex(2)
        elif self.obj.Attribute == Tools2D.Attribute.Vacuo or self.obj.Attribute == Tools2D.Attribute.Void:
            self.ui.cb_attribute.setCurrentIndex(3)
        else:
            Tools2D.sayz("Circular--错误--Object被赋予了无法识别的属性")

    def setIsMarkXState(self):
        self.ui.le_markx.setEnabled(self.ui.checkBox_isMarkX.isChecked())

    def setIsMarkYState(self):
        self.ui.le_marky.setEnabled(self.ui.checkBox_isMarkY.isChecked())

    def setOrderToObj(self):
        """
        将order设置到obj，如果order的顺序是不正确的，则会根据规则自动修正
        """
        curNumOfObjects = len(Tools2D.getAllValidModelObj())
        curOrder = int(self.ui.le_order.text())

        if curOrder <= curNumOfObjects - 1:
            if curOrder < self.obj.Order:
                for i in range(int(self.obj.Order) - curOrder):
                    self.obj.Order = self.obj.Order - 1
            elif curOrder > self.obj.Order:
                for i in range(curOrder - self.obj.Order):
                    self.obj.Order = self.obj.Order + 1

    def closeEvent(self, event):
        if self.isKeepData:
            try:
                self.setInfoToObj()
                # self.customOption()
                FreeCADGui.runCommand("CreateM2D")
            except AttributeError:
                Tools2D.sayz("--异常--在读取Object属性时出现异常")
                Tools2D.sayz(traceback.format_exc())
            except Exception as e:
                Tools2D.sayz("--" + str(e))
            else:
                Tools2D.sayz("创建--成功--设置Object信息")
        else:
            if self.isNew:
                FreeCAD.ActiveDocument.removeObject(self.obj.Label)
            else:
                pass

    # @wangzhenguo 自定义属性的逻辑
    def customOption(self):
        if self.ui.cb_attribute.currentIndex() == 2:
            self.ui.Layout_custom.addWidget(self.customAttribute)
            self.customAttribute.show()
            self.customAttribute.ui.comboBox_sigma.currentIndexChanged.connect(self.sigmaOption)
            self.customAttribute.ui.comboBox_setEps.currentIndexChanged.connect(self.setEpsOption)
        else:
            self.customAttribute.hide()
            # self.ui.resize(width, height)

    def sigmaOption(self):
        if self.customAttribute.ui.comboBox_sigma.currentIndex() == 0:
            self.customAttribute.ui.lineEdit_sigma1.show()
            self.customAttribute.ui.lineEdit_sigma2.hide()
            self.customAttribute.ui.lineEdit_sigma3.hide()
        elif self.customAttribute.ui.comboBox_sigma.currentIndex() == 1:
            self.customAttribute.ui.lineEdit_sigma1.show()
            self.customAttribute.ui.lineEdit_sigma2.show()
            self.customAttribute.ui.lineEdit_sigma3.show()
        else:
            self.customAttribute.ui.lineEdit_sigma1.hide()
            self.customAttribute.ui.lineEdit_sigma2.hide()
            self.customAttribute.ui.lineEdit_sigma3.hide()

    def setEpsOption(self):
        if self.customAttribute.ui.comboBox_setEps.currentIndex() == 0:
            self.customAttribute.ui.lineEdit_setEps1.show()
            self.customAttribute.ui.lineEdit_setEps2.hide()
            self.customAttribute.ui.lineEdit_setEps3.hide()
        elif self.customAttribute.ui.comboBox_setEps.currentIndex() == 1:
            self.customAttribute.ui.lineEdit_setEps1.show()
            self.customAttribute.ui.lineEdit_setEps2.show()
            self.customAttribute.ui.lineEdit_setEps3.show()
        else:
            self.customAttribute.ui.lineEdit_setEps1.hide()
            self.customAttribute.ui.lineEdit_setEps2.hide()
            self.customAttribute.ui.lineEdit_setEps3.hide()


# 除Model外所有obj的Dialog的基类
class BaseOtherDialog(QtGui.QDialog):
    def __init__(self, obj, isNew=False, parent=None):
        """
        此处代码仅仅作为示范，所有的子类都要重写__init__
        """
        QtGui.QDialog.__init__(self, parent)
        self.ui = None
        self.setUI()

        self.obj = obj
        self.isNew = isNew
        self.isKeepData = False
        self.initDialog()

    def initDialog(self):
        """
        初始化Dialog，设置Dialog的逻辑
        """
        # noinspection PyBroadException
        try:
            self.setCommonItems()
            self.helperInitDialog()
        except Exception as reason:
            Tools2D.sayz("初始化Dialog时出现错误，错误如下：")
            Tools2D.sayz(traceback.format_exc())
        else:
            Tools2D.sayz("正确初始化对话框")

    def helperInitDialog(self):
        """
        该函数会被initDialog调用，当界面初始化时，实际触发的操作写在该函数中
        将槽函数的内容放在此处的主要目的是方便做统一的异常处理
        """
        pass

    def setCommonItems(self):
        self.ui.pb_ok.clicked.connect(self.slotOK)
        self.ui.pb_cancel.clicked.connect(self.slotCancel)

    def setUI(self):
        # self.ui = NewMaterialDialog.Ui_Dialog_NewMaterialDlg()
        # self.ui.setupUi(self)
        pass

    def slotOK(self):
        # noinspection PyBroadException
        try:
            self.helperOK()
            FreeCADGui.runCommand("CreateM2D")
        except Exception as reason:
            Tools2D.sayz("点击确定关闭对话框时出现错误，错误如下：")
            Tools2D.sayz(traceback.format_exc())
        else:
            Tools2D.sayz("成功设置数据到object")

    def helperOK(self):
        """
        该函数会被slotOK调用，当确定键被点击时，实际触发的操作写在该函数中
        将槽函数的内容放在此处的主要目的是方便做统一的异常处理
        """
        pass

    def slotCancel(self):
        # noinspection PyBroadException
        try:
            self.helperCancel()
            Tools2D.sayz("---------------------")
        except Exception as reason:
            Tools2D.sayz("点击取消并关闭对话框时出现错误，错误如下：")
            Tools2D.sayz(traceback.format_exc())

    def helperCancel(self):
        """
        该函数会被slotCancel调用，，当取消键被点击时，实际触发的操作写在该函数中
        将槽函数的内容放在此处的主要目的是方便做统一的异常处理
        """
        pass

    def closeEvent(self, event):
        if self.isKeepData:
            self.keepData()
        else:
            if self.isNew:
                FreeCAD.ActiveDocument.removeObject(self.obj.Label)
