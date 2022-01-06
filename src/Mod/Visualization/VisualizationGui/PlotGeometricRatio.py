# -*- coding: UTF-8 -*-

import FreeCAD
import vPlot
import numpy as np
def sayz(msg):
    FreeCAD.Console.PrintMessage(msg)
    FreeCAD.Console.PrintMessage('\n')
def sayzerr(msg):
    FreeCAD.Console.PrintError(msg)
    FreeCAD.Console.PrintWarning('\n')
def show():
    plot = vPlot.getPlot()
    mdi = vPlot.getMdiArea()
    subWindowName = mdi.activeSubWindow().windowTitle()
    # 等比等差绘图切换
    if "_GeometricRatio" not in subWindowName:
        subWindowName = subWindowName+"_GeometricRatio"
    else:
        subWindowName = subWindowName.split("_GeometricRatio")[0]
    sayz("plot.fileName")
    vPlot.isExisted(subWindowName,plot.fileName)


