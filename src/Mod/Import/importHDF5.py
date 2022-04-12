# -*- coding: utf-8 -*-
# create by chenjian

import FreeCAD,FreeCADGui

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



# 某个部分会直接调用insert，并传递filename
# 使用 hdf5-protobuf 打开文件
def insert(filename, doc):
    sayz(filename)


def readHdf5(filename):
    sayz('start openning hdf5')
    file_path = os.path.dirname(__file__)
    exe_path = os.path.dirname(file_path)
    output = os.popen(exe_path + '\\Import\\readHdf5\\readHdf5.exe ' + filename).read()
    # output = os.popen(exe_path + '\\Import\\serializeHdf5\\serializeHdf5Data.exe ' + filename).read()
    return output

