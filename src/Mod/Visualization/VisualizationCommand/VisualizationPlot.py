# -*- coding: UTF-8 -*-

import math
from pylab import *

import vPlot
import FreeCAD


# 等位图
def drawContour(cutA, cutB, x_lable, y_lable, system,time, component,
                range_start, range_end, range_min, range_max, step, a, b, c, tag,isRatio):
    FreeCAD.Console.PrintMessage("drawContour+++++++++++++++++++++\n")
    # 绘图
    vPlot.contour_plot(cutA, cutB, x_lable, y_lable,system, time, component, range_start, range_end, range_min,
                       range_max, step, a, b, c, tag,isRatio)

# 时间变化图
def drawObserve(x_label, y_label, type, range_min, range_max, x, y):
    vPlot.observe_plot(x_label, y_label, type, range_min, range_max, x, y)

# 相空间图
def drawPhasespace(cutA, cutB, x_label, y_label, particle, time, x, y,z=None):
    vPlot.phasespace_plot(cutA, cutB, x_label, y_label, particle, time, x, y,z)

# 空间变化图
def drawRange(x_label, y_label, time, component, range_min, range_max, x, y):
    vPlot.range_plot(x_label, y_label, time, component, range_min, range_max, x, y)

# 矢量图
def drawVector(cutA, cutB, x_label, y_label, component, time, cut_position, max_vector, a, b, c):
    vPlot.vector_plot(cutA, cutB, x_label, y_label, component, time, cut_position, max_vector, a, b, c)

# 三维等位图
def drawContour3D(x_lable, y_lable,system, time, component,
                range_start, range_end, range_min, range_max, step, a, b, c):
    vPlot.contour_3D(x_lable, y_lable, system,time, component, range_start, range_end, range_min,
                       range_max, step, a, b, c)

# 二维剖面图
def drawCut(ab,xyAll,figName, baseData, cutpos, system, isExchange):
    vPlot.cut_plot(ab,xyAll, figName, baseData, cutpos, system, isExchange)

def sayz(msg):
    FreeCAD.Console.PrintMessage(msg)
    FreeCAD.Console.PrintMessage('\n')