# -*- coding: utf-8 -*-
# create by chenjian

import FreeCAD,FreeCADGui
import VisualizationGui
import VisualizationCommand.LoadingMain as Loading

from PySide import QtGui
from PySide import QtCore
from PySide.QtCore import QThread
import os
def clientSetWorkpath(workpath):
    FreeCAD.clientSetWorkpath(workpath)
def sayz(msg):
    FreeCAD.Console.PrintMessage(msg)
    FreeCAD.Console.PrintMessage('\n')

def sayzerr(msg):
    FreeCAD.Console.PrintError(msg)
    FreeCAD.Console.PrintWarning('\n')

# 使用 hdf5-json 打开文件
def open(filename):
    sayz(filename)
    Loading.showLoading(filename, 1)
    # file_path = os.path.dirname(__file__)
    # exe_path = os.path.dirname(file_path)
    # import time
    # t = time.time()
    # output = os.popen(exe_path + '\\Import\\readHdf5\\readHdf5.exe ' + filename).read()
    # sayz('start importing hdf5')
    # output = os.popen(exe_path + '\\Import\\serializeHdf5\\serializeHdf5Data.exe ' + filename).read()
    # sayz('serializeHdf5Dat1 '+str(time.time() - t))
    # dataname = os.path.splitext(filename)[0]
    # datapath = dataname + '_json'
    # if output == 'analyze success\n':
    #     import VisualizationCommand.VisualizationResultProtobuf as showResult
    #     showResult.showResultTree(filename)
    #     sayz('serializeHdf5Dat2 '+str(time.time() - t))
    #     # 激活后处理工作台
    #     FreeCADGui.activateWorkbench("VisualWorkbench")
    # else:
    #     sayzerr(output)

# 某个部分会直接调用insert，并传递filename
# 使用 hdf5-protobuf 打开文件
def insert(filename, doc):
    sayz(filename)
    # 使用protobuf读取hdf5
    # file_path = os.path.dirname(__file__)
    # exe_path = os.path.dirname(file_path)
    # import time
    # t = time.time()
    # output = os.popen(exe_path+'\\Import\\serializeHdf5\\serializeHdf5Data.exe '+filename).read()
    # sayz('readHdf1 '+str(time.time() - t))
    # if output == 'analyze success\n':
    #     Loading.showLoading(filename, 2)
    #     sayz('readHdf2 '+str(time.time() - t))
    # else:
    #     sayzerr(output)
    # 使用json读取hdf5
    Loading.showLoading(filename, 1)


def readHdf5(filename):
    sayz('start openning hdf5')
    file_path = os.path.dirname(__file__)
    exe_path = os.path.dirname(file_path)
    output = os.popen(exe_path + '\\Import\\readHdf5\\readHdf5.exe ' + filename).read()
    # output = os.popen(exe_path + '\\Import\\serializeHdf5\\serializeHdf5Data.exe ' + filename).read()
    return output

