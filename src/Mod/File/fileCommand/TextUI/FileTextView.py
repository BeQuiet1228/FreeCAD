#-*- coding: utf-8 -*-

import FreeCAD as App
import FreeCADGui
import File.FileGui.FileTextEditor
import File.FileCommand.M3DFile.CHIPICCommand
import File.FileCommand.M3DFile.M3DFileUtil

import PySide

class FileView(PySide.QtGui.QWidget):

    def __init__(self,
                 parent=None):
        """
        Keyword arguments:
        parent -- Widget parent.
        
        """
        PySide.QtGui.QWidget.__init__(self, parent)
        self.ui = File.FileGui.FileTextEditor.Ui_Form()
        self.ui.setupUi(self)

        # 设置textEdit的一些属性
        self.ui.textEdit.setReadOnly(True)
        self.ui.textEdit.setFontWeight(63)
        self.ui.textEdit.setFontFamily(u"Arial")
        self.ui.textEdit.setText("")

        # 给textEdit设置Highlighter
        from File.FileCommand.TextUI.MyQSyntaxHighlighter import Highlighter
        highlighter = Highlighter(self.ui.textEdit.document())

        # 为了显示事件服务
        self.showNum = 0

    def updateText(self, str):
        # 获得面板
        thisSubWindow = self.getThisSubWindow()

        if thisSubWindow == None:
            self.showThisSubWindow()
            thisSubWindow = self.getThisSubWindow()

        fileView = thisSubWindow.widget()

        # 清除原来的文字
        fileView.ui.textEdit.clear()

        # 做初始化设置
        textEdit = fileView.ui.textEdit
        textEdit.setFontWeight(63)  # 设置字体粗细
        textEdit.setFontFamily(u"Arial")  # 设置字体

        # 设置颜色变量
        green = PySide.QtGui.QColor(0, 128, 0, 255)
        black = PySide.QtGui.QColor(0, 0, 0, 255)
        blue = PySide.QtGui.QColor(0, 0, 150, 255)
        gray = PySide.QtGui.QColor(200, 200, 200, 255)
        white = PySide.QtGui.QColor(255, 255, 255, 255)

        # 将要显示的字符串按行分割并赋值给lineStrs
        lineStrs = str.split("\n")

        # 循环遍历每一行字符，并根据需求加上具体的效果
        lineNum = 0
        for lineStr in lineStrs:
            # 为每一行增加行号
            # lineNum = lineNum + 1

            # # 将行号对应的数字转换为4位的字符串
            # if lineNum / 10 >= 100:
            #     lineNumStr = lineNum.__str__()
            # elif lineNum / 10 >= 10:
            #     lineNumStr = " " + lineNum.__str__()
            # elif lineNum / 10 >= 1:
            #     lineNumStr = "  " + lineNum.__str__()
            # else:
            #     lineNumStr = "   " + lineNum.__str__()

            # textEdit.setTextBackgroundColor(gray)
            # textEdit.setTextColor(black)
            # textEdit.append(lineNum.__str__())
            # textEdit.setTextBackgroundColor(white)
            # textEdit.insertPlainText("  ")

            # 不显示行号，则需换行
            textEdit.append("")

            # 如果某一行的首字符为!，则这一行为注释行，颜色为绿色
            if lineStr != "" and lineStr[0] == "!":
                textEdit.setTextColor(green)
                textEdit.insertPlainText(lineStr)
            else:
                # 如果该行的第一个单词为关键字，则显示为蓝色
                words = lineStr.split(" ")
                if File.FileCommand.M3DFile.CHIPICCommand.keywordInCommand.__contains__(words[0]):
                    textEdit.setTextColor(blue)
                    textEdit.insertPlainText(words[0])
                    textEdit.setTextColor(black)
                    textEdit.insertPlainText(lineStr[len(words[0]): len(lineStr)])
                else:
                    textEdit.setTextColor(black)
                    textEdit.insertPlainText(lineStr)


    def closeEvent(self, event):
        """关闭m3d显示界面时，应该关闭该工程"""

        # msgBox = PySide.QtGui.QMessageBox()
        # msgBox.setText("The document has been modified.")
        # msgBox.setInformativeText("Do you want to save your changes?")
        # msgBox.setStandardButtons(PySide.QtGui.QMessageBox.Save | PySide.QtGui.QMessageBox.Discard | PySide.QtGui.QMessageBox.Cancel)
        # msgBox.setDefaultButton(PySide.QtGui.QMessageBox.Save)
        # ret = msgBox.exec_()
        #
        # if ret == PySide.QtGui.QMessageBox.Save:
        #     # Save was clicked
        #
        #     # 重新保存
        #     # 重新保存m3d
        #     fileUtil = File.FileCommand.M3DFile.M3DFileUtil.M3DFileUtil()
        #     fileUtil.writeToFile()
        #     # 重新保存工程
        #
        #     # 关闭工程
        #     App.closeDocument(App.ActiveDocument.Label)
        #
        # elif ret == PySide.QtGui.QMessageBox.Discard:
        #     # Don't save was clicked
        #
        #     # 删除已有m3d文件
        #     fileUtil = File.FileCommand.M3DFile.M3DFileUtil.M3DFileUtil()
        #     fileUtil.deleteFile()
        #     # 关闭工程
        #     App.closeDocument(App.ActiveDocument.Label)
        #
        # elif ret == PySide.QtGui.QMessageBox.Cancel:
        #     # cancel was clicked
        #
        #     # 忽略关闭事件
        #     event.ignore()
        #
        # else:
        #     # should never be reached
        #     print("error, should never be reached")
    def updateM3dFile(self):
        # 获得m3d的util
        fileUtil = File.FileCommand.M3DFile.M3DFileUtil.M3DFileUtil()
        # 获得最近的m3d字符串
        str = fileUtil.getLatestM3DFileStr()
        # 进行文本的更新
        self.ui.textEdit.setText(str)
        # self.updateText(str)
        # 写文件
        fileUtil.writeToFile(isRefresh=True)

    def showEvent(self, event):
        # 对于一个m3d文件显示界面，测试可知，添加->显示->前一个窗口activate三个操作后，showEvent被调用了三次
        # 之后显示该界面调用一次showEvent, 切换到别的界面时又调用一次showEvent
        # 通过showNum来获得刚好显示界面的shoeEvent，以避免频繁刷新

        self.showNum = self.showNum + 1

        if self.showNum > 3:
            # 表示已经新建完m3d文件的显示界面
            if self.showNum == 4:
                # 表示切换m3d的显示界面

                # 获得m3d的util
                fileUtil = File.FileCommand.M3DFile.M3DFileUtil.M3DFileUtil()
                # 获得最近的m3d字符串
                # App.Console.PrintError('\n进入更新showevent函数\n')
                str = fileUtil.getLatestM3DFileStr()
                # 进行文本的更新
                self.ui.textEdit.setText(str)
                # self.updateText(str)
                # 写文件
                fileUtil.writeToFile(isRefresh=True)

            else:
                # 表示切换到其余的界面，重新将showNum置为等待切换的状态
                self.showNum = 3


    def setTitle(self, src):
        # 更换窗口的名字
        sub = self.getThisSubWindow()
        sub.widget().setWindowTitle(src + " M3d")


    def isThisSubWindow(self):
        # 获得中间窗口
        mdi = self.__getMdiArea()

        # 判断是否已经新建m3d文件显示的子窗口
        subWindowList = mdi.subWindowList()
        isExist = False
        for subWindow in subWindowList:
            if isinstance(subWindow.widget(), FileView):
                if subWindow.widget().windowTitle().__contains__(App.ActiveDocument.Label):
                    isExist = True

        return isExist


    def addThisSubWindow(self):
        # 获得中间窗口
        mdi = self.__getMdiArea()
        # 添加
        sub = mdi.addSubWindow(self)
        # 给新添加的窗口换名字
        ActiveDocumentLabel = App.ActiveDocument.Label
        sub.widget().setWindowTitle(ActiveDocumentLabel + " M3d")
        sub.widget().setStatusTip(App.ActiveDocument.Uid)


    def getThisSubWindow(self):
        # 获得中间窗口
        mdi = self.__getMdiArea()

        # 遍历所有窗口
        flag = False # 标志是否找到了
        subWindowList = mdi.subWindowList()
        for subWindow in subWindowList:
            if isinstance(subWindow.widget(), FileView):
                if subWindow.widget().statusTip() == App.ActiveDocument.Uid:
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
        # 使中间的窗口激活前面的子窗口，而不是新加入的子窗口
        mdi.activatePreviousSubWindow()


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

    def getM3dSubWindow(self):
        """ Return the selected Plot document if exist. """
        # Get active tab
        mdi = self.__getMdiArea()
        if not mdi:
            return None
        sub = mdi.activeSubWindow()
        if not sub:
            return None
        return isinstance(sub.widget(), FileView)

    def find(self, str, isSensitive, isWhole):

        # 获得面板
        thisSubWindow = self.getThisSubWindow()

        if thisSubWindow == None:
            self.showThisSubWindow()
            thisSubWindow = self.getThisSubWindow()

        editor = thisSubWindow.widget().ui.textEdit

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









