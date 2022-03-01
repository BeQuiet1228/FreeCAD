# -*- coding: utf-8 -*-
from PySide import QtGui, QtCore

from Modeling.Modeling2D.Modeling2DCommand.AreaFunction import AreaFunctionDialog
from Modeling.Modeling2D.Modeling2DCommand.BaseUI import BaseDialog
from Modeling.Modeling2D.Tools import Tools2D, ToolsUI
import FreeCAD
import traceback


# class ShowDialog(QtGui.QDialog):
#     def __init__(self, obj, isNew=False, parent=None):
#         QtGui.QDialog.__init__(self, parent)
#         self.ui = AreaFunctionDialog.Ui_Sector()
#         self.ui.setupUi(self)
#
#         self.setModal(False)
#         self.obj = obj
#         self.isNew = isNew
#         self.isKeepData = False
#         self.initDialog()
#         self.loadData()
#
#     def initDialog(self):
#         try:
#             self.loadData()
#             self.ui.pb_ok.clicked.connect(self.slotOK)
#             self.ui.pb_cancel.clicked.connect(self.slotCancel)
#         except:
#             Tools2D.sayz("error:" + traceback.format_exc())
#
#     def slotOK(self):
#         self.isKeepData = True
#         self.close()
#
#     def slotCancel(self):
#         self.isKeepData = False
#         self.close()
#
#     def loadData(self):
#         """
#         加载数据到界面
#         :return:
#         """
#         try:
#             # 共有数据
#             ToolsUI.getCommonInfoFromModelObj(self.obj, self.ui)
#             self.ui.le_expression.setText(self.obj.expression)
#         except:
#             Tools2D.sayz("error:" + traceback.format_exc())
#
#     def keepData(self):
#         """
#         将界面的数据保存到obj
#         :return:
#         """
#         try:
#             ToolsUI.setCommonInfoToModelObj(self.obj, self.ui)
#             self.obj.expression = self.ui.le_expression.text()
#         except:
#             Tools2D.sayz("error:" + traceback.format_exc())


class ShowDialog(BaseDialog.BaseModelDialog):
    def __init__(self, obj, isNew=False, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = AreaFunctionDialog.Ui_Sector()
        self.ui.setupUi(self)

        self.customAttribute = BaseDialog.CustomShowWidget()

        # 暂时写在这里
        self.setModal(False)
        self.obj = obj
        # 为老工程做适配，如果没有属性则添加属性
        if not hasattr(self.obj, "C_SIGMA"):
            Tools2D.completionProperties(self.obj)
        self.initDialog()
        self.getInfoFromObj()
        self.isNew = isNew
        self.isKeepData = False

    def getInfoFromObj(self):
        """
        从Object获取信息，并且设置到Dialog
        """
        try:
            # 共有数据
            ToolsUI.getCommonInfoFromModelObj(self.obj, self.ui)
            # 自定义属性
            ToolsUI.getCustomAttributeFromModelObj(self.obj, self.customAttribute.ui)
            # 独有数据
            self.ui.le_expression.setText(self.obj.expression)

        except AttributeError:
            Tools2D.sayz(traceback.format_exc())
        except Exception as e:
            Tools2D.sayz(str(e))
        else:
            Tools2D.sayz("成功--读取Object信息")
        # 加载Mark对应文本框的状态
        self.setIsMarkXState()
        self.setIsMarkYState()

    def setInfoToObj(self):
        """
        从Dialog获取信息，并且赋值到Object
        """
        try:
            ToolsUI.setCommonInfoToModelObj(self.obj, self.ui)
            # 自定义属性
            ToolsUI.setCustomAttributeToModelObj(self.obj, self.customAttribute.ui)
            # user_xxx辅助记录输入信息
            self.obj.expression = self.ui.le_expression.text()
            self.obj.recompute()
        except:
            import traceback
            Tools2D.sayz("error:" + traceback.format_exc())
        pass
