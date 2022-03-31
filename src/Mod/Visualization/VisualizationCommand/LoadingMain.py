# -*- coding: UTF-8 -*-

import FreeCAD
import FreeCADGui
# import data_pb2

from PySide import QtGui
from PySide import QtCore
import os

IconCommonPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Visualization/VisualizationResources/"

def sayz(msg):
    FreeCAD.Console.PrintMessage(msg)
    FreeCAD.Console.PrintMessage('\n')

def sayzerr(msg):
    FreeCAD.Console.PrintError(msg)
    FreeCAD.Console.PrintWarning('\n')

# 子线程解析 h5 文件
class DialogThread(QtCore.QThread):
    # finished = QtCore.Signal(str, str)
    finished = QtCore.Signal(str)
    def __init__(self, filePath, dataType):
        super(DialogThread, self).__init__()
        self.filePath = filePath
        self.dataType = dataType
        self.output = ""
        self.target = None

    def run(self):
        sayz('thread start')
        if self.dataType == 1:
            # hdf5-json
            # exe_path = FreeCAD.ConfigGet("AppHomePath") + "Mod"
            # self.output = os.popen(exe_path + "\\Package\\readHdf5\\readHdf5.exe " + '"' + self.filePath + '"').read()

            self.finished.emit(self.filePath)
        # elif self.dataType == 2:
        #     # hdf5-protobuf
        #     binaryFilePath = self.filePath[:-3]
        #     try:
        #         f = open(binaryFilePath, "rb")
        #         self.target = data_pb2.allData()
        #         self.target.ParseFromString(f.read())
        #         f.close()
        #     except IOError:
        #         sayz("Could not open the file. Please create a new one.")
        #     self.finished.emit(self.target, self.filePath)


# 等待加载窗口
class LoadingWidget(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self._stop_import = True
        # self.ui = loading.LoadingDialog.Ui_Dialog_loading()
        self.ui.setupUi(self)
        qMovie = QtGui.QMovie()
        picPath = IconCommonPath + "/loading.gif"
        qMovie.setFileName(picPath)
        self.ui.label_pic.setMovie(qMovie)
        qMovie.start()

    def childThread(self, filePath, dataType):
        self.thread = DialogThread(filePath, dataType)
        if dataType == 1:
            self.thread.finished.connect(buildTree)
        # elif dataType == 2:
        #     self.thread.finished.connect(buildTree_protobuf)
        self.thread.start()

    def closeEvent(self, event):
        if self._stop_import:
            sayzerr("stop loading")
            self.thread.wait()
        else:
            # super(LoadingWidget, self).closeEvent(event)
            sayz('finish loading')


# 显示加载窗口
def showLoading(filePath, dataType):
    loading = LoadingWidget()
    loading.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    loading.setAttribute(QtCore.Qt.WA_TranslucentBackground)
    # 开启子线程
    loading.childThread(filePath, dataType)
    loading.show()
    # 其他进程不能继续工作
    loading.exec_()

# 关闭加载框
def closeDialog():
    aw = QtGui.QApplication.topLevelWidgets()
    for i in aw:
        if i.objectName() == "Dialog_loading":
            i.close()

# 建立结果目录
def buildTree(filePath):
    closeDialog()
    FreeCAD.Console.PrintMessage("buildTree\n")
    import VisualizationResult as showResult
    showResult.showResultTree(filePath)
    # 激活后处理工作台
    # FreeCADGui.activateWorkbench("VisualWorkbench")

# def buildTree_protobuf(target, filePath):
#     closeDialog()
#     import VisualizationResultProtobuf as showResult
#     showResult.showResultTree(target, filePath)
#     FreeCADGui.activateWorkbench("VisualWorkbench")

