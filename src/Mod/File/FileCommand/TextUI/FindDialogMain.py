#-*- coding: utf-8 -*-
import FreeCAD
from PySide import QtGui
import M3DFileEditor.M3DFileEditorGui.FindDialog
from File.FileCommand.TextUI.FileTextView import FileView

class FindMain(QtGui.QDialog):
    def __init__(self,parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = M3DFileEditor.M3DFileEditorGui.FindDialog.Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.findButton.clicked.connect(self.findClick)

    def findClick(self):
        # 获得要查找的字符
        findText = self.ui.findText.text()

        # 获得是否大小写敏感
        isSensitive = self.ui.checkSensitive.isChecked()

        # 获得是否查找整个单词
        isWhole = self.ui.checkWhole.isChecked()

        # 获得编辑框
        fileview = FileView()

        # 进行查找
        # 默认是大小写不敏感，不是whole word，向后查找
        fileview.find(findText, isSensitive, isWhole)

def sayz(msg):
    FreeCAD.Console.PrintMessage(msg)
    FreeCAD.Console.PrintMessage('\n')