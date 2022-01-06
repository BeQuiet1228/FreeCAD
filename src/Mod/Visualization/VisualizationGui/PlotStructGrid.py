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

    plt = vPlot.getPlot()
    cut = plt.cut

    if cut is not None and cut.collectionGridEdgeList != []:
        cut.showCutGrid()
    elif cut is not None and cut.collectionGridEdgeList == []:
        cut.drawStructGridFast()

    #刷新绘制
    plt.canvas.draw_idle()


