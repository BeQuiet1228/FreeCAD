# -*- coding: utf-8 -*-

import FreeCAD as App
import FreeCADGui
import File.FileGui.FileTextEditor
import File.FileCommand.M3DFile.CHIPICCommand
import File.FileCommand.M3DFile.M3DFileUtil

import PySide


class FileEditor(PySide.QtGui.QWidget):
    def __init__(self,
                 parent=None):
        """
        Keyword arguments:
        parent -- Widget parent.

        """
        PySide.QtGui.QWidget.__init__(self, parent)
        self.ui = File.FileGui.FileTextEditor.Ui_Form()
        self.ui.setupUi(self)
        self.__StatusTip = "MyM3DFileEditor"
        self.setStatusTip(self.__StatusTip)
        self.setWindowTitle("M3D File Editor")

        # 设置textEdit的一些属性
        self.ui.textEdit.setReadOnly(False)
        self.ui.textEdit.setFontWeight(63)
        self.ui.textEdit.setFontFamily(u"Arial")
        self.ui.textEdit.setText("")

        # 给textEdit设置Highlighter
        from File.FileCommand.TextUI.MyQSyntaxHighlighter import Highlighter
        highlighter = Highlighter(self.ui.textEdit.document())


    def isThisSubWindow(self):
        # 获得中间窗口
        mdi = self.__getMdiArea()

        # 判断是否已经新建m3d文件显示的子窗口
        subWindowList = mdi.subWindowList()
        isExist = False
        for subWindow in subWindowList:
            if isinstance(subWindow.widget(), FileEditor):
                if subWindow.widget().statusTip() == self.__StatusTip:
                    isExist = True

        return isExist

    def addThisSubWindow(self):
        # 获得中间窗口
        mdi = self.__getMdiArea()
        # 添加
        sub = mdi.addSubWindow(self)

    def getThisSubWindow(self):
        # 获得中间窗口
        mdi = self.__getMdiArea()

        # 遍历所有窗口
        flag = False  # 标志是否找到了
        subWindowList = mdi.subWindowList()
        for subWindow in subWindowList:
            if isinstance(subWindow.widget(), FileEditor):
                if subWindow.widget().statusTip() == self.__StatusTip:
                    flag = True
                    return subWindow

    def showThisSubWindow(self):
        # 获得中间窗口
        mdi = self.__getMdiArea()

        # 如果存在m3d文件显示的子窗口
        if not self.isThisSubWindow():
            # 增加子窗口
            self.addThisSubWindow()

        # 获得子窗口
        sub = self.getThisSubWindow()
        # 显示
        sub.show()

    def __getMainWindow(self):
        """ Return the FreeCAD main window. """
        toplevel = PySide.QtGui.QApplication.topLevelWidgets()
        for i in toplevel:
            if i.metaObject().className() == "Gui::MainWindow":
                return i
        return None

    def __getMdiArea(self):
        """ Return FreeCAD MdiArea. """
        mw = self.__getMainWindow()
        if not mw:
            return None
        childs = mw.children()
        for c in childs:
            if isinstance(c, PySide.QtGui.QMdiArea):
                return c
        return None

    def redo(self):
        # 重做
        sub = self.getThisSubWindow()
        sub.widget().ui.textEdit.redo()

    def undo(self):
        # 撤销
        sub = self.getThisSubWindow()
        sub.widget().ui.textEdit.undo()

    def cut(self):
        # 剪切
        sub = self.getThisSubWindow()
        sub.widget().ui.textEdit.cut()

    def copy(self):
        # 复制
        sub = self.getThisSubWindow()
        sub.widget().ui.textEdit.copy()

    def paste(self):
        # 粘贴
        sub = self.getThisSubWindow()
        sub.widget().ui.textEdit.paste()

    def find(self, str, isSensitive, isWhole):
        sub = self.getThisSubWindow()
        editor = sub.widget().ui.textEdit

        # 设置查找模式
        findFlag = 0
        if isSensitive and not isWhole:
            findFlag = PySide.QtGui.QTextDocument.FindCaseSensitively
        elif not isSensitive and isWhole:
            findFlag = PySide.QtGui.QTextDocument.FindWholeWords
        elif isSensitive and isWhole:
            findFlag = PySide.QtGui.QTextDocument.FindCaseSensitively and PySide.QtGui.QTextDocument.FindWholeWords

        # 进行查找
        # 默认是大小写不敏感，不是whole word，向后查找
        flag = editor.find(str, findFlag)
        if flag == False:
            # 如果没找到，则从头再找
            editor.moveCursor(PySide.QtGui.QTextCursor.Start)
            editor.find(str, findFlag)

    def replace(self, findStr, replaceStr, isSensitive, isWhole):
        sub = self.getThisSubWindow()
        editor = sub.widget().ui.textEdit

        # 设置查找模式
        findFlag = 0
        if isSensitive and not isWhole:
            findFlag = PySide.QtGui.QTextDocument.FindCaseSensitively
        elif not isSensitive and isWhole:
            findFlag = PySide.QtGui.QTextDocument.FindWholeWords
        elif isSensitive and isWhole:
            findFlag = PySide.QtGui.QTextDocument.FindCaseSensitively and PySide.QtGui.QTextDocument.FindWholeWords

        flag = editor.find(findStr, findFlag)
        if flag == True:
            # 如果找到，则替换
            editor.insertPlainText(replaceStr)
        else:
            # 没有找到，从头再找
            editor.moveCursor(PySide.QtGui.QTextCursor.Start)
            flag2 = editor.find(findStr, findFlag)
            if flag2 == True:
                editor.insertPlainText(replaceStr)


    def replaceAll(self, findStr, replaceStr, isSensitive, isWhole, recur_depth = 0):
        sub = self.getThisSubWindow()
        editor = sub.widget().ui.textEdit

        # 设置查找模式
        findFlag = 0
        if isSensitive and not isWhole:
            findFlag = PySide.QtGui.QTextDocument.FindCaseSensitively
        elif not isSensitive and isWhole:
            findFlag = PySide.QtGui.QTextDocument.FindWholeWords
        elif isSensitive and isWhole:
            findFlag = PySide.QtGui.QTextDocument.FindCaseSensitively and PySide.QtGui.QTextDocument.FindWholeWords

        # 第一次执行时把光标移到最前面，并且不再循环查找
        # 可以避免 "ab" -> "abcd" 这种情况下导致的无限递归
        if recur_depth == 0:
            editor.moveCursor(PySide.QtGui.QTextCursor.Start)

        flag = editor.find(findStr, findFlag)
        if flag == True:
            # 如果找到，则替换
            editor.insertPlainText(replaceStr)
            self.replaceAll(findStr, replaceStr, isSensitive, isWhole, recur_depth + 1)
        # else:
        #     # 没有找到，从头再找
        #     editor.moveCursor(PySide.QtGui.QTextCursor.Start)
        #     flag2 = editor.find(findStr, findFlag)
        #     if flag2 == True:
        #         editor.insertPlainText(replaceStr)
        #         self.replaceAll(findStr, replaceStr, isSensitive, isWhole)


    def readFile(self,filename):
        f = open(filename, "r")  # 设置文件对象
        str = f.read()  # 将txt文件的所有内容读入到字符串str中
        f.close()  # 将文件关闭
        return str

    def writeToFile(self,filename,str):
        with open(filename.decode('utf8').encode('gbk'), 'w') as f:  # 设置文件对象
            f.write(str)  # 将字符串写入文件中


def sayz(msg):
    App.Console.PrintMessage(msg)
    App.Console.PrintMessage('\n')