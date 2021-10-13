# -*- coding: utf-8 -*-
from CustomParameter.CustomParameterGui import TableView
from PySide import QtGui, QtCore
import FreeCADGui, FreeCAD
from Modeling.Modeling2D.Tools import Tools2D


class TestTableView(QtGui.QDialog):
    """
    模型对话框类的父类
    """
    def __init__(self, parent=None):
        """
        子类需要重写构造函数而不是继承该构造函数
        """
        QtGui.QDialog.__init__(self, parent)
        self.ui = TableView.Ui_Dialog()
        self.ui.setupUi(self)

        self.model = QtGui.QStandardItemModel(1, 4)

        self.testFunc()

    def testFunc(self):
        # self.ui.tableView.setWindowTitle('QTableView表格视图的例子')
        self.model.setHorizontalHeaderLabels(['Name', 'Expression', 'Value', 'Description'])
        # row 行 / column 列
        # for row in range(4):
        #     for column in range(4):
        #         item = QtGui.QStandardItem('row %s,column %s' % (row, column))
        #         # 设置每个位置的文本值
        #         self.model.setItem(row, column, item)

        self.ui.tableView.setModel(self.model)
        self.model.insertRow(0)


class TestCommand:
    """
    布尔运算界面按钮
    """
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        Form = TestTableView()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Physics/PhysicsResources/foil.svg"
        MenuText = Tools2D.QT_TRANSLATE_NOOP(
            'CreateFoil',
            'Create Foil')
        ToolTip = Tools2D.QT_TRANSLATE_NOOP(
            'CreateFoil',
            'Foil')
        return {'MenuText': "Bool",
                'ToolTip': ToolTip}


FreeCADGui.addCommand('TestCommand123', TestCommand())
