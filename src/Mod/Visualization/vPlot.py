# -*- coding: UTF-8 -*-
#***************************************************************************
#*                                                                         *
#*   Copyright (c) 2011, 2012                                              *
#*   Jose Luis Cercos Pita <jlcercos@gmail.com>                            *
#*                                                                         *
#*   This program is free software; you can redistribute it and/or modify  *
#*   it under the terms of the GNU Lesser General Public License (LGPL)    *
#*   as published by the Free Software Foundation; either version 2 of     *
#*   the License, or (at your option) any later version.                   *
#*   for detail see the LICENCE text file.                                 *
#*                                                                         *
#*   This program is distributed in the hope that it will be useful,       *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
#*   GNU Library General Public License for more details.                  *
#*                                                                         *
#*   You should have received a copy of the GNU Library General Public     *
#*   License along with this program; if not, write to the Free Software   *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
#*   USA                                                                   *
#*                                                                         *
#***************************************************************************

import FreeCAD

import PySide
from PySide import QtCore, QtGui
from distutils.version import LooseVersion as V
import math
import json
from Modeling.Common.Tools import DocumentTools as DocTools

try:
    import matplotlib
    matplotlib.use('Qt4Agg')
    matplotlib.rcParams['backend.qt4']='PySide'
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
    if V(matplotlib.__version__) < V("1.4.0"):
       from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
    else:
       from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
    from matplotlib.figure import Figure
    from matplotlib import gridspec
    from matplotlib import cm
    import matplotlib.patches as mpatches
    from mpl_toolkits.mplot3d.axes3d import Axes3D
    import numpy as np
    from pylab import *
    from matplotlib.patches import Rectangle
    from matplotlib.patches import Wedge
    from matplotlib.collections import PatchCollection,LineCollection
except ImportError:
    msg = PySide.QtGui.QApplication.translate(
        "plot_console",
        "matplotlib not found, so Plot module can not be loaded",
        None)
    FreeCAD.Console.PrintMessage(msg + '\n')
    raise ImportError("matplotlib not installed")

# 解决无法显示中文的问题
mpl.rcParams['font.sans-serif'] = ['SimHei']

# 解决无法显示负号的问题
plt.rcParams['axes.unicode_minus'] = False

LIST = {}
# 全局变量LicenseURL用来标志是否关闭所有文档，
# 每次关闭文档后会重置LicenseURL
try:
    FreeCAD.ActiveDocument.LicenseURL="emptyLIST"
except:
    FreeCAD.Console.PrintMessage("此时没有激活的工程，是直接打开绘图1")
flag = True

# 适配分辨率
import Physics.PhysicsCommand.AdaptiveDPIUtil as AdaptiveDPIUtil
x_dpi, y_dpi = AdaptiveDPIUtil.get_win_dpi()
if x_dpi <=1024:
    textSize = 12
    labelSize = 16
    axisSize = 14
elif x_dpi <=1440:
    textSize = 14
    labelSize = 18
    axisSize = 16
elif x_dpi <=1920:
    textSize = 16
    labelSize = 20
    axisSize = 18
else:
    textSize = 18
    labelSize = 22
    axisSize = 20
def getMainWindow():
    """ Return the FreeCAD main window. """
    toplevel = PySide.QtGui.QApplication.topLevelWidgets()
    mwdf =  None
    for i in toplevel:
        if i.metaObject().className() == "MainWindowDef":
            mwdf = i
            break
    wid = None
    for i in mwdf.children():
        if i.metaObject().className() == "QWidget":
            wid = i 
            break
    for i in wid.children():
        if i.metaObject().className() == "Gui::MainWindow":
            return i
    return None

def getMdiArea():
    """ Return FreeCAD MdiArea. """
    mw = getMainWindow()
    if not mw:
        return None
    childs = mw.children()
    for c in childs:
        if isinstance(c, PySide.QtGui.QMdiArea):
            return c
    return None

def getPlot():
    """ Return the selected Plot document if exist. """
    # Get active tab
    mdi = getMdiArea()
    if not mdi:
        return None
    sub = mdi.activeSubWindow()
    if not sub:
        return None
    # Explore childrens looking for Plot class
    for i in sub.children():
        if i.metaObject().className() == "Plot":
            return i
    return None

# 将控制部分等比显示得图存在LIST中
def saveFigToList(fig):
    global LIST
    # LIST[fig.winTitle] = fig
    if not LIST.has_key(fig.winTitle+fig.fileName):
        sayz("cunle")
        LIST[fig.winTitle+fig.fileName] = fig

def closePlot():
    """ closePlot(): Close the active plot window. """
    # Get active tab
    mdi = getMdiArea()
    if not mdi:
        return None
    sub = mdi.activeSubWindow()
    if not sub:
        return None
    # Explore childrens looking for Plot class
    for i in sub.children():
        if i.metaObject().className() == "Plot":

            global LIST
            # 将plot对象所在内存地址存在LIST中
            if not LIST.has_key(i.winTitle+i.fileName):
                LIST[i.winTitle+i.fileName] = i
            # 解除QMdiSunWindow与plot对象的绑定关系
            #  if an internal widget is passed in the child widget is set to 0 but the QMdiSubWindow is not removed.
            mdi.removeSubWindow(i)
            # 关闭
            sub.close()


# 判断是否存在该图,存在就显示出来
def isExisted(winTitle,fileName):

    mdi = getMdiArea()
    if not mdi:
        return None
    global LIST

    if LIST.has_key(winTitle+fileName):
        win = LIST[winTitle+fileName]
        if win:
            # 关闭现在的图
            closePlot()
            # 打开切换后的图
            sub = mdi.addSubWindow(win)
            sub.show()
            win.setVisible(True)


def clear():
    global LIST
    # import gc
    # del LIST
    # gc.collect()
    LIST={}

def figure(IsTriggerCloseEvent,winTitle="plot",fileName="fileName"):
    """Create a new plot subwindow/tab.

    Keyword arguments:
    IsTriggerCloseEvent--为True时，代表为控制部分绘图结果，关闭时需要同时删除树结构中item
                        为False，代表为打开hdf5文件绘制结果，关闭时不做操作
    winTitle -- Plot tab title.
    """
    closePlot()
    mdi = getMdiArea()
    if not mdi:
        return None
    global flag
    global LIST

    #如果LicenseURL不等于emptyLIST,代表之前关闭文档被重置了，此时需要清空LIST
    LIST = {}
    try:
        if FreeCAD.ActiveDocument.LicenseURL !="emptyLIST":
            LIST = {}
            FreeCAD.ActiveDocument.LicenseURL = "emptyLIST"
    except:
        sayz("此时没有激活的工程，是直接打开绘图2")
    if LIST.has_key(winTitle+fileName):

        win = LIST[winTitle+fileName]
        flag = True
    else:
        win = Plot(IsTriggerCloseEvent, winTitle,fileName)
        flag = False

    sub = mdi.addSubWindow(win)
    sub.show()
    return win,flag


def plot(x, y, name=None):
    """Plots a new serie (as line plot)

    Keyword arguments:
    x -- X values
    y -- Y values
    name -- Data serie name (for legend).
    """
    # Get active plot, or create another one if don't exist
    plt = getPlot()
    if not plt:
        plt = figure()
    # Call to plot
    return plt.plot(x, y, name)

def series():
    """Return all the lines from a selected plot."""
    plt = getPlot()
    if not plt:
        return []
    return plt.series

def removeSerie(index):
    """Remove a data serie from the active plot.

    Keyword arguments:
    index -- Index of the serie to remove.
    """
    # Get active series
    plt = getPlot()
    if not plt:
        return
    plots = plt.series
    if not plots:
        return
    # Remove line from plot
    axes = plots[index].axes
    axes.lines.pop(plots[index].lid)
    # Remove serie from list
    del plt.series[index]
    # Update GUI
    plt.update()

def legend(status=True, pos=None, fontsize=None):
    """Show/Hide the legend from the active plot.

    Keyword arguments:
    status -- True if legend must be shown, False otherwise.
    pos -- Legend position.
    fontsize -- Font size
    """
    plt = getPlot()
    if not plt:
        return
    plt.legend = status
    if fontsize:
        plt.legSiz = fontsize
    # Hide all legends
    for axes in plt.axesList:
        axes.legend_ = None
    # Legend must be activated on last axes
    axes = plt.axesList[-1]
    if status:
        # Setup legend handles and names
        lines = series()
        handles = []
        names = []
        for l in lines:
            if l.name is not None:
                handles.append(l.line)
                names.append(l.name)
        # Show the legend (at selected position or at best)
        if pos:
            l = axes.legend(handles, names, bbox_to_anchor=pos)
            plt.legPos = pos
        else:
            l = axes.legend(handles, names, loc='best')
            # Update canvas in order to compute legend data
            plt.canvas.draw()
            # Get resultant position
            try:
                fax = axes.get_frame().get_extents()
            except:
                fax = axes.patch.get_extents()
            fl = l.get_frame()
            plt.legPos = (
                (fl._x + fl._width - fax.x0) / fax.width,
                (fl._y + fl._height - fax.y0) / fax.height)
        # Set fontsize
        for t in l.get_texts():
            t.set_fontsize(plt.legSiz)
    plt.update()

def grid(status=True):
    """Show/Hide the grid from the active plot.

    Keyword arguments:
    status -- True if grid must be shown, False otherwise.
    """
    plt = getPlot()
    if not plt:
        return
    plt.grid = status
    axes = plt.axleft
    axes.grid(status)
    plt.update()

def title(string):
    """Setup the plot title.

    Keyword arguments:
    string -- Plot title.
    """
    plt = getPlot()
    if not plt:
        return
    axes = plt.axleft
    axes.set_title(string)
    plt.update()

def xlabel(string):
    """Setup the x label.

    Keyword arguments:
    string -- Title to set.
    """
    plt = getPlot()
    if not plt:
        return
    axes = plt.axleft
    axes.set_xlabel(string)
    plt.update()

def ylabel(string):
    """Setup the y label.

    Keyword arguments:
    string -- Title to set.
    """
    plt = getPlot()
    if not plt:
        return
    axes = plt.axleft
    axes.set_ylabel(string)
    plt.update()

def axesList():
    """Return the plot axes sets list. """
    plt = getPlot()
    if not plt:
        return []
    return plt.axesList

def axes():
    """Return the active plot axes."""
    plt = getPlot()
    if not plt:
        return None
    return plt.axleft

def addNewAxes(rect=None, frameon=True, patchcolor='none'):
    """Add new axes to plot, setting it as the active one.

    Keyword arguments:
    rect -- Axes area, None to copy from the last axes data.
    frameon -- True to show frame, False otherwise.
    patchcolor -- Patch color, 'none' for transparent plot.
    """
    plt = getPlot()
    if not plt:
        return None
    fig = plt.fig
    if rect is None:
        rect = plt.axes.get_position()
    ax = fig.add_axes(rect, frameon=frameon)
    ax.xaxis.set_ticks_position('bottom')
    ax.spines['top'].set_color('none')
    ax.yaxis.set_ticks_position('left')
    ax.spines['right'].set_color('none')
    ax.patch.set_facecolor(patchcolor)
    plt.axesList.append(ax)
    plt.setActiveAxes(-1)
    plt.update()
    return ax

def save(path, figsize=None, dpi=None):
    """Save plot.

    Keyword arguments:
    path -- Destination file path.
    figsize -- w,h figure size tuple in inches.
    dpi -- Dots per inch.
    """
    plt = getPlot()
    if not plt:
        return
    # Backup figure options
    fig = plt.fig
    sizeBack = fig.get_size_inches()
    dpiBack = fig.get_dpi()
    # Save figure with new options
    if figsize:
        fig.set_size_inches(figsize[0], figsize[1])
    if dpi:
        fig.set_dpi(dpi)
    plt.canvas.print_figure(path)
    # Restore figure options
    fig.set_size_inches(sizeBack[0], sizeBack[1])
    fig.set_dpi(dpiBack)
    plt.update()

def addNavigationToolbar():
    """Add the matplotlib QT navigation toolbar to the plot.
    """
    plt = getPlot()
    if not plt:
        return
    # Check that the navigation toolbar has not been already created
    if plt.mpl_toolbar is not None:
        return
    # Create the navigation toolbar and add it
    plt.mpl_toolbar = NavigationToolbar(plt.canvas, plt)
    vbox = plt.layout()
    vbox.addWidget(plt.mpl_toolbar)

def delNavigationToolbar():
    """Remove the matplotlib QT navigation toolbar from the plot.
    """
    plt = getPlot()
    if not plt:
        return
    # Check that the navigation toolbar already exist
    if plt.mpl_toolbar is None:
        return
    # Remove the widget from the layout
    vbox = plt.layout()
    vbox.removeWidget(plt.mpl_toolbar)
    # Destroy the navigation toolbar
    plt.mpl_toolbar.deleteLater()
    plt.mpl_toolbar = None

# 等位图
def contour_plot(cutA, cutB, x_lable, y_lable, system, time, component,
                 range_start, range_end, range_min, range_max, step, a, b, c, tag, isRatio):
    plt = getPlot()
    if not plt:
        plt, flag = figure(False)

    return plt.contour_plot(cutA, cutB, x_lable, y_lable, system, time, component,
                                range_start, range_end, range_min, range_max, step, a, b, c, tag, isRatio)

# 时间变化图
def observe_plot(x_lable, y_lable, type, range_min, range_max, x, y):
    plt = getPlot()
    if not plt:
        plt, flag = figure(False)
    return plt.observe_plot(x_lable, y_lable, type, range_min, range_max, x, y)

# 相空间图
def phasespace_plot(cutA, cutB, x_label, y_label, particle, time, x, y,z=None):
    plt = getPlot()
    if not plt:
        plt, flag = figure(False)
    plt.phasespace_plot(cutA, cutB, x_label, y_label, particle, time, x, y,None,z)

# 空间变化图
def range_plot(x_label, y_label, time, component, range_min, range_max, x, y):
    plt = getPlot()
    if not plt:
        plt, flag = figure(False)
    return plt.range_plot(x_label, y_label, time, component, range_min, range_max, x, y)

# 矢量图
def vector_plot(cutA, cutB, x_label, y_label, component, time,cut_position, max_vector, a, b, c):
    plt = getPlot()
    if not plt:
        plt, flag = figure(False)
    return plt.vector_plot(cutA, cutB, x_label, y_label, component, time, cut_position, max_vector, a, b, c)

# 三维等位图
def contour_3D(x_lable, y_lable, system,time, component,
                 range_start, range_end, range_min, range_max, step, a, b, c):
    plt = getPlot()
    if not plt:
        plt, flag = figure(False)
    return plt.contour_3D(x_lable, y_lable,system, time, component,
                            range_start, range_end, range_min, range_max, step, a, b, c)

# 剖面结构图
def cut_plot(ab, abAll,figName, baseDataPath, cutpos, system, isExchange):
    plt = getPlot()
    if not plt:
        plt, flag = figure(False)
    return plt.cut_plot(ab, abAll, figName, baseDataPath, cutpos, system, isExchange)

class Line():
    def __init__(self, axes, x, y, name):
        """Construct a new plot serie.

        Keyword arguments:
        axes -- Active axes
        x -- X values
        y -- Y values
        name -- Data serie name (for legend).
        """
        self.axes = axes
        self.x = x
        self.y = y
        self.name = name
        # self.lid = len(axes.lines)
        self.line, = axes.plot(x, y)

    def setp(self, prop, value):
        """Change a line property value.

        Keyword arguments:
        prop -- Property name.
        value -- New property value.
        """
        plt.setp(self.line, prop, value)

    def getp(self, prop):
        """Get line property value.

        Keyword arguments:
        prop -- Property name.
        """
        return plt.getp(self.line, prop)

# 判断y值大小，以确定单位
def getUnit(value):

    if max(abs(value)) >= 10 ** 12:
        unit = "T"
        pow = 12
    elif 10 ** 9 <= max(abs(value)) < 10 ** 12:
        unit = "G"
        pow = 9
    elif 10 ** 6 <= max(abs(value)) < 10 ** 9:
        unit = "M"
        pow = 6
    elif 10 ** 3 <= max(abs(value)) < 10 ** 6:
        unit = "k"
        pow = 3
    elif 10 ** -3 <= max(abs(value)) < 10 ** 3 or max(abs(value)) == 0 :
        unit = ""
        pow = 0
    elif 10 ** -6 <= max(abs(value)) < 10 ** -3:
        unit = "m"
        pow = -3
    elif 10 ** -9 <= max(abs(value)) < 10 ** -6:
        unit = "μ"
        pow = -6
    elif 10 ** -12 <= max(abs(value)) < 10 ** -9:
        unit = "n"
        pow = -9
    elif 10 ** -15 <= max(abs(value)) < 10 ** -12:
        unit = "p"
        pow = -12
    elif max(abs(value)) <= 10 ** -15:
        unit = "f"
        pow = -15
    else:
        unit = ""
        pow = 0

    return unit,pow

def getRange(fun,startR,endR,startAngle,endAngle):
    angleList = np.linspace(startAngle,endAngle,101)
    if fun=="sin":
        angle_max = np.max(np.sin(angleList))
        angle_min = np.min(np.sin(angleList))
        R_max = max(startR*angle_max,endR*angle_max)
        R_min = min(startR * angle_min, endR * angle_min)
    else:
        angle_max = np.max(np.cos(angleList))
        angle_min = np.min(np.cos(angleList))
        R_max = max(startR * angle_max, endR * angle_max)
        R_min = min(startR * angle_min, endR * angle_min)
    return [R_min,R_max]

# 等位图
class Contour():
    def  __init__(self, ax0, cutA, cutB, x_label, y_label, a, b, c, level, tag,isRatio,system,range_start, range_end):
        # 判断a、b、c的数据量关系是否符合要求
        FreeCAD.Console.PrintMessage("Contour+++++++++++++++++++++\n")
        if a is not None and b is not None and c is not None and len(c) == len(a) * len(b)\
                and not (True in np.isinf(a)) and not (True in np.isinf(b)) and not (True in np.isinf(c))\
                and not (True in np.isnan(a)) and not (True in np.isnan(b)) and not (True in np.isnan(c)):
            self.x = a
            self.y = b
            self.z = c
            self.type = 'contour'
            a = np.array(a)
            b = np.array(b)
            c = np.array(c)
            # #将nan和inf替换为0
            # a[np.isnan(a)] = 0
            # a[np.isinf(a)] = 0
            # b[np.isnan(b)] = 0
            # b[np.isinf(b)] = 0
            # c[np.isnan(c)] = 0
            # c[np.isinf(c)] = 0

            #针对角度数据少的图进行插值
            if "R*cos(Phi)" in x_label or "R*cos(Phi)" in y_label:
                #如果间隔大于0.628就插值，插值间隔为0.628
                if(len(b)>1 and b[1]>0.7 ):
                    length=len(b)
                    
                    
                    for i in range(length-1,0,-1):
                        num = int((b[i]-b[i-1])/0.628)
                        diff = (b[i]-b[i-1])/(num)
                        insertArray =[]

                        for n in range(1,num):
                            insertArray.append(b[i-1]+diff*n)
 
                        b=np.insert(b,i,insertArray)

                        c=np.insert(c,len(a)*(i),c.tolist()[len(a)*(i-1):len(a)*i]*(num-1))
            

            A, B = np.meshgrid(a, b)
            # 如果坐标轴是R*cos(Phi)或R*sin(Phi)则要进行计算
            if "R*cos(Phi)" in x_label:
                X = A * np.cos(B)
            elif "R*sin(Phi)" in x_label:
                X = A * np.sin(B)
            else:
                X = A

            if "R*sin(Phi)" in y_label:
                Y= A * np.sin(B)
            elif "R*cos(Phi)" in y_label:
                Y = A * np.cos(B)
            else:
                Y = B
            Z = c.reshape(len(b), len(a))
            plt.cla()

            if isRatio:
                colorlist = []
                if type(level) == np.ndarray:
                    color_num = len(level)
                else:
                    color_num = level
                cmap = matplotlib.cm.get_cmap('nipy_spectral')
                for i in range(1, color_num):
                    rgba = cmap(float(i) / color_num)
                    sayz(float(i) / color_num)
                    colorlist.append(rgba)

                if tag == 'line':
                    self.contour = ax0.contour(X, Y, Z, levels=level,   colors = colorlist, linewidths=1.5)
                elif tag == 'shade':
                    self.contour = ax0.contourf(X, Y, Z, levels=level, colors = colorlist)

            else:
                if tag == 'line':
                    self.contour = ax0.contour(X, Y, Z, levels=level,  cmap='nipy_spectral',linewidths=1.5)
                elif tag == 'shade':
                    self.contour = ax0.contourf(X, Y, Z, levels=level, cmap='nipy_spectral')
            if cutA and cutB:
                ax0.scatter(cutA, cutB, s=10, c="black", marker="s")

            self.unit_y, self.pow_y = getUnit(Y.ravel())
            self.unit_x, self.pow_x = getUnit(X.ravel())

            FreeCAD.Console.PrintMessage("Contour+++++++++++++++++++++\n")
            if system == "cylindrical":
                #柱坐标顺序为zrt
                startList = range_start.split('[')[1].split(']')[0].split(',')
                if len(startList) == 2:
                    startList.append("0")
                startZ = float(startList[0])
                startX = float(startList[1])
                startY = float(startList[2])
                endList = range_end.split('[')[1].split(']')[0].split(',')
                if len(endList) == 2:
                    endList.append("0")
                endZ = float(endList[0])
                endX = float(endList[1])
                endY = float(endList[2])
            else:
                #极坐标顺序为rtz，直角坐标顺序为xyz
                startList = range_start.split('[')[1].split(']')[0].split(',')
                if len(startList) == 2:
                    startList.append("0")
                startX = float(startList[0])
                startY = float(startList[1])
                startZ = float(startList[2])
                endList = range_end.split('[')[1].split(']')[0].split(',')
                if len(endList) == 2:
                    endList.append("0")
                endX = float(endList[0])
                endY = float(endList[1])
                endZ = float(endList[2])
            FreeCAD.Console.PrintMessage("Contour+++++++++++++++++++++\n")
            # 根据刻度的科学计数法得到的单位修改XY坐标轴
            if "R*cos(Phi)" in x_label:
                x_label = "R*cos(Phi)(" + self.unit_x + "m)"
                xlim = getRange("cos", startX, endX, startY, endY)
            elif "R*sin(Phi)" in x_label:
                x_label = "R*sin(Phi)(" + self.unit_x + "m)"
                xlim = getRange("sin", startX, endX, startY, endY)
            elif "Z" in x_label:
                x_label = "Z(" + self.unit_x + "m)"
                xlim = [startZ, endZ]
            elif "X" in x_label:
                x_label = "X(" + self.unit_x + "m)"
                xlim = [startX, endX]
            elif "Y" in x_label:
                x_label = "Y(" + self.unit_x + "m)"
                xlim = [startY, endY]
            elif "R" in x_label:
                x_label = "R(" + self.unit_x + "m)"
                xlim = [startX, endX]
            elif "(" in x_label:
                xlim = [startX, endX]
                x_label = x_label.split("(")[0] + "(" + self.unit_x + "m)"

            if "R*sin(Phi)" in y_label:
                y_label = "R*sin(Phi)(" + self.unit_y + "m)"
                ylim = getRange("sin", startX, endX, startY, endY)
            elif "R*cos(Phi)" in y_label:
                y_label = "R*cos(Phi)(" + self.unit_y + "m)"
                ylim = getRange("cos", startX, endX, startY, endY)
            elif "Z" in y_label:
                y_label = "Z(" + self.unit_y + "m)"
                ylim = [startZ, endZ]
            elif "X" in y_label:
                y_label = "X(" + self.unit_y + "m)"
                ylim = [startX, endX]
            elif "Y" in y_label:
                y_label = "Y(" + self.unit_y + "m)"
                ylim = [startY, endY]
            elif "R" in y_label:
                y_label = "R(" + self.unit_y + "m)"
                ylim = [startX, endX]
            elif "(" in y_label:
                ylim = [startX, endX]
                y_label = y_label.split("(")[0] + "(" + self.unit_y + "m)"
            ax0.set_xlim(xlim)
            ax0.set_ylim(ylim)

            FreeCAD.Console.PrintMessage("Contour+++++++++++++++++++++\n")
            # g%为去掉多余的0
            def formatnum_y(y, pos):

                return '$%g$' % (y / 10 ** self.pow_y)


            # 设置y轴刻度值格式
            formatter1 = FuncFormatter(formatnum_y)
            ax0.yaxis.set_major_formatter(formatter1)

            # g%为去掉多余的0
            def formatnum_x(x, pos):
                return '$%g$' % (x / 10 ** self.pow_x)

            # 设置y轴刻度值格式
            formatter2 = FuncFormatter(formatnum_x)
            ax0.xaxis.set_major_formatter(formatter2)
            FreeCAD.Console.PrintMessage("Contour+++++++++++++++++++++\n")
            # 颜色标注
            # 设置为科学计数法，保留两位小数
            cb = plt.colorbar(self.contour, ax=ax0, ticks=level,format='%.2e')
            cb.ax.zorder = -1
            # 设置字体，大小
            for l in cb.ax.yaxis.get_ticklabels():
                l.set_family('Times New Roman')
                l.set_size(axisSize)
        else:
            DocTools.errorMessage(u"内核导出Hdf5数据中有非法数据，可能计算模型设计有误，请检查模型！\n")
        # 坐标轴标注
        ax0.set_xlabel(x_label, fontdict={'family': 'Times New Roman', 'size': labelSize})
        ax0.set_ylabel(y_label, fontdict={'family': 'Times New Roman', 'size': labelSize})

    # 去掉刻度及坐标轴
    def noaxis(self):
        plt.xticks([])
        plt.yticks([])
        plt.axis('off')

    # 图像信息
    def figinfo(self, ax1, time, component, range_start, range_end, range_min, range_max, step):
        FreeCAD.Console.PrintMessage("figinfo+++++++++++++++++++++\n")
        plt.xticks([])
        plt.yticks([])
        plt.axis('off')
        FreeCAD.Console.PrintMessage("figinfo+++++++++++++++++++++\n")
        ax1.text(0.0, 0.95, U'图形名称：等位图', transform=ax1.transAxes,fontdict={'size': textSize, 'color': 'black'})
        FreeCAD.Console.PrintMessage("figinfo+++++++++++++++++++++\n")
        ax1.text(0.0, 0.65, U'等值范围：', transform=ax1.transAxes,fontdict={'size': textSize, 'color': 'black'})
        FreeCAD.Console.PrintMessage("figinfo+++++++++++++++++++++\n")
        ax1.text(0.0, 0.6, 'min: ' + range_min, transform=ax1.transAxes,fontdict={'family': 'Times New Roman','size': textSize, 'color': 'black'})
        FreeCAD.Console.PrintMessage("figinfo+++++++++++++++++++++\n")
        ax1.text(0.0, 0.55, 'max: ' + range_max, transform=ax1.transAxes,fontdict={'family': 'Times New Roman','size': textSize, 'color': 'black'})
        FreeCAD.Console.PrintMessage("figinfo+++++++++++++++++++++\n")
        ax1.text(0.0, 0.5, U'等值步长：', transform=ax1.transAxes,fontdict={'size': textSize, 'color': 'black'})
        FreeCAD.Console.PrintMessage("figinfo+++++++++++++++++++++\n")
        ax1.text(0.0, 0.5, '                   '+ step, transform=ax1.transAxes, fontdict={'family': 'Times New Roman','size': textSize, 'color': 'black'})
        FreeCAD.Console.PrintMessage("figinfo+++++++++++++++++++++\n")
        ax1.text(0.0, 0.9, U'观察时间：', transform=ax1.transAxes,
                   fontdict={'size': textSize, 'color': 'black'})
        FreeCAD.Console.PrintMessage("figinfo+++++++++++++++++++++\n")
        ax1.text(0.0, 0.9, '                   '+time, transform=ax1.transAxes,
                 fontdict={'family': 'Times New Roman','size': textSize, 'color': 'black'})
        FreeCAD.Console.PrintMessage("figinfo+++++++++++++++++++++\n")
        ax1.text(0.0, 0.85, U'观察分量：', transform=ax1.transAxes,
                   fontdict={'size': textSize, 'color': 'black'})
        FreeCAD.Console.PrintMessage("figinfo+++++++++++++++++++++\n")
        ax1.text(0.0, 0.85, U'                   '+component, transform=ax1.transAxes,
                 fontdict={'family': 'Times New Roman','size': textSize, 'color': 'black'})
        FreeCAD.Console.PrintMessage("figinfo+++++++++++++++++++++\n")
        ax1.text(0.0, 0.8, U'等值区域：', transform=ax1.transAxes,fontdict={'size': textSize, 'color': 'black'})
        FreeCAD.Console.PrintMessage("figinfo+++++++++++++++++++++\n")
        ax1.text(0.0, 0.75, range_start, transform=ax1.transAxes,fontdict={'family': 'Times New Roman','size': textSize, 'color': 'black'})
        FreeCAD.Console.PrintMessage("figinfo+++++++++++++++++++++\n")
        ax1.text(0.0, 0.7, range_end,transform=ax1.transAxes, fontdict={'family': 'Times New Roman','size': textSize, 'color': 'black'})

# 时间变化图
class Observe():
    def __init__(self, ax0, x_label, y_label, type,x, y, name):
        self.name = name
        self.type = 'observe'
        if x is not None and y is not None and not (True in np.isnan(x)) and not (True in np.isnan(y)
        ) and not (True in np.isinf(x)) and not (True in np.isinf(y)):
            self.x = x
            self.y = y
            self.line,  = ax0.plot(x, y, 'crimson')


            self.unit_y, self.pow_y = getUnit(y)
            self.unit_x, self.pow_x = getUnit(x)

            # g%为去掉多余的0
            def formatnum_y(y, pos):

                return '$%g$' % (y / 10**self.pow_y)
            # 设置y轴刻度值格式
            formatter1 = FuncFormatter(formatnum_y)
            ax0.yaxis.set_major_formatter(formatter1)

            # g%为去掉多余的0
            def formatnum_x(x, pos):
                return '$%g$' % (x / 10 ** self.pow_x)

            # 设置y轴刻度值格式
            formatter2 = FuncFormatter(formatnum_x)
            ax0.xaxis.set_major_formatter(formatter2)

            # 根据type中包含的关键词确定纵坐标标柱
            if "E.DL" in type:
                y_label = "Voltage("+self.unit_y +"V)"
            elif "S.DA" in type:
                y_label = "Power("+self.unit_y+"W)"
            elif "H.DL" in type or "J.DA" in type:
                y_label = "Current("+self.unit_y+"A)"
            elif "Bphi" in type:
                y_label = "Bphi("+self.unit_y+"T)"
            elif "Brho" in type:
                y_label = "Brho("+self.unit_y+"T)"
            elif "Bz" in type:
                y_label = "Bz("+self.unit_y+"T)"
            elif "Ephi" in type:
                y_label = "Ephi("+self.unit_y+"V/m)"
            elif "Erho" in type:
                y_label = "Erho("+self.unit_y+"V/m)"
            elif "Ez" in type:
                y_label = "Ez("+self.unit_y+"V/m)"
            elif "Jphi" in type:
                y_label = "Jphi("+self.unit_y+"A/m²)"
            elif "Jrho" in type:
                y_label = "Jrho("+self.unit_y+"A/m²)"
            elif "Jz" in type:
                y_label = "Jz("+self.unit_y+"A/m²)"
            else:
                y_label=y_label+"(1e"+str(self.pow_y)+")"

            #根据得到的unit替换x_label中的单位
            try:
                import re
                unit = re.findall('[(](.*?)[)]', x_label)[-1]
                x_label = x_label.replace('('+unit+')', '('+self.unit_x+unit+')')
            except:
                sayzerr("x_label don't need repair")
        else:
            DocTools.errorMessage(u"内核导出Hdf5数据中有非法数据，可能计算模型设计有误，请检查模型！\n")
        ax0.set_xlabel(x_label, fontdict={'family': 'Times New Roman', 'size': labelSize})
        ax0.set_ylabel(y_label, fontdict={'family': 'Times New Roman', 'size': labelSize})


    # 去掉刻度及坐标轴
    def noaxis(self):
        plt.xticks([])
        plt.yticks([])
        plt.axis('off')


    # 图像信息
    def figinfo(self, ax1, type, range_min, range_max):
        ax1.text(0.0, 0.95, U'图形名称：时间变化图', transform=ax1.transAxes,fontdict={'size': textSize, 'color': 'black'})
        ax1.text(0.0, 0.9, U'观察类型：', transform=ax1.transAxes,fontdict={'size': textSize, 'color': 'black'})
        ax1.text(0.0, 0.9, '                   '+type, transform=ax1.transAxes, fontdict={'family': 'Times New Roman','size': textSize, 'color': 'black'})
        if range_min !="" and range_max != "":
            ax1.text(0.0, 0.85, U'观察范围：', transform=ax1.transAxes, fontdict={'size': textSize, 'color': 'black'})
            ax1.text(0.0, 0.8, 'min: ' + range_min,transform=ax1.transAxes, fontdict={'family': 'Times New Roman','size': textSize, 'color': 'black'})
            ax1.text(0.0, 0.75, 'max: ' + range_max,transform=ax1.transAxes, fontdict={'family': 'Times New Roman','size': textSize, 'color': 'black'})
        elif range_min !="" :
            ax1.text(0.0, 0.85, U'观察范围：', transform=ax1.transAxes, fontdict={'size': textSize, 'color': 'black'})
            ax1.text(0.0, 0.8, range_min, transform=ax1.transAxes,
                     fontdict={'family': 'Times New Roman', 'size': textSize, 'color': 'black'})

# 相空间图
class Phasespace():
    def __init__(self, ax0, cutA, cutB, x_label, y_label, x, y, name,z=None):
        self.name = name
        self.type = 'phasepace'
        FreeCAD.Console.PrintMessage("Phasespace +++++++++++++++++++++++++++++++++ \n")
        if x is not None and y is not None:
            #  x=np.array(x)
            #  y=np.array(y)
            #将粒子分为两种
            x2 = None
            y2 = None 
            if z == None:
                x=np.array(x)
                y=np.array(y)
            else:
                tempX1 = []
                tempY1 = []
                tempX2 = []
                tempY2 = []
                for i in range(0,len(z)):
                    if z[i] == 1:
                        tempX1.append(x[i])
                        tempY1.append(y[i])
                    else:
                        tempX2.append(x[i])
                        tempY2.append(y[i])
                x=np.array(tempX1)
                y=np.array(tempY1)
                x2=np.array(tempX2)
                y2=np.array(tempY2)
            FreeCAD.Console.PrintMessage("Phasespace +++++++++++++++++++++++++++++++++ \n")
                     
            if not (True in np.isnan(x)) and not (True in np.isnan(y)) and not (True in np.isinf(x)) and not (True in np.isinf(y)):
                if 'sin' in y_label:
                    self.line = ax0.scatter(y * np.cos(x), y * np.sin(x), s=0.1, color='crimson')
                    if x2 != None and y2 != None:
                        self.line = ax0.scatter(y2 * np.cos(x2), y2 * np.sin(x2), s=0.1, color='blue')
                else:
                    self.line = ax0.scatter(x, y, s=0.1, color='crimson')
                    if x2 != None and y2 != None:
                        self.line = ax0.scatter(x2, y2, s=0.1, color='blue')
                if cutA and cutB:
                    ax0.scatter(cutA, cutB, s=10, c="black")
            else:
                
                x1=x[(~np.isnan(x)) & (~np.isnan(y)) & (~np.isinf(x)) & (~np.isinf(y))]
                y=y[(~np.isnan(x)) & (~np.isnan(y)) & (~np.isinf(x)) & (~np.isinf(y))]
                x=x1
                if 'sin' in y_label:
                    self.line = ax0.scatter(y * np.cos(x), y * np.sin(x), s=0.1, color='crimson')
                else:
                    self.line = ax0.scatter(x, y, s=0.1, color='crimson')
                if cutA and cutB:
                    ax0.scatter(cutA, cutB, s=10, c="black")
                DocTools.errorMessage(u"内核导出Hdf5数据中有非法数据，可能计算模型设计有误，请检查模型！\n")
            FreeCAD.Console.PrintMessage("Phasespace +++++++++++++++++++++++++++++++++ \n")
            

        ax0.set_xlabel(x_label, fontdict={'family': 'Times New Roman', 'size': labelSize})
        ax0.set_ylabel(y_label, fontdict={'family': 'Times New Roman', 'size': labelSize})
        FreeCAD.Console.PrintMessage("Phasespace +++++++++++++++++++++++++++++++++ \n")

    # 去掉刻度及坐标轴
    def noaxis(self):
        plt.xticks([])
        plt.yticks([])
        plt.axis('off')

    # 图像信息
    def figinfo(self, ax1, particle, time):
        ax1.text(0.0, 0.95, U'图形名称：相位空间图', transform=ax1.transAxes,fontdict={'size': textSize, 'color': 'black'})
        ax1.text(0.0, 0.9, U'观察时间：', transform=ax1.transAxes,
                 fontdict={'size': textSize, 'color': 'black'})
        ax1.text(0.0, 0.9, '                   '+time, transform=ax1.transAxes,
                 fontdict={'family': 'Times New Roman','size': textSize, 'color': 'black'})
        ax1.text(0.0, 0.85, U'粒子分量：', transform=ax1.transAxes, fontdict={'size': textSize, 'color': 'black'})
        ax1.text(0.0, 0.85, '                   '+particle, transform=ax1.transAxes, fontdict={'family': 'Times New Roman','size': textSize, 'color': 'black'})


# 空间变化图
class Range():
    def __init__(self, ax0, x_label, y_label, x, y, name):
        self.name = name
        self.type = 'range'
        if x is not None and y is not None and not (True in np.isnan(x)) and not (True in np.isnan(y)
        ) and not (True in np.isinf(x)) and not (True in np.isinf(y)):
            self.line, = ax0.plot(x, y, 'crimson')
        else:
            DocTools.errorMessage(u"内核导出Hdf5数据中有非法数据，可能计算模型设计有误，请检查模型！\n")
        ax0.set_xlabel(x_label, fontdict={'family': 'Times New Roman', 'size': labelSize})
        ax0.set_ylabel(y_label, fontdict={'family': 'Times New Roman', 'size': labelSize})

    # 去掉刻度及坐标轴
    def noaxis(self):
        plt.xticks([])
        plt.yticks([])
        plt.axis('off')

    # 图像信息
    def figinfo(self, ax1, time, component, range_min, range_max):
        ax1.text(0.0, 0.95, U'图形名称：空间变化图',transform=ax1.transAxes, fontdict={'size': textSize, 'color': 'black'})
        ax1.text(0.0, 0.9, U'观察时间：', transform=ax1.transAxes,
                 fontdict={'size': textSize, 'color': 'black'})
        ax1.text(0.0, 0.9, '                   '+time, transform=ax1.transAxes,
                 fontdict={'family': 'Times New Roman', 'size': textSize, 'color': 'black'})
        ax1.text(0.0, 0.85, U'分量曲线：', transform=ax1.transAxes,
                 fontdict={'size': textSize, 'color': 'black'})
        ax1.text(0.0, 0.85,  '                   '+component, transform=ax1.transAxes,
                 fontdict={'family': 'Times New Roman','size': textSize, 'color': 'black'})
        ax1.text(0.0, 0.8, U'观察范围：', transform=ax1.transAxes,fontdict={'size': textSize, 'color': 'black'})
        ax1.text(0.0, 0.75, 'min: ' + range_min, transform=ax1.transAxes,fontdict={'family': 'Times New Roman','size': textSize, 'color': 'black'})
        ax1.text(0.0, 0.7, 'max: ' + range_max,transform=ax1.transAxes, fontdict={'family': 'Times New Roman','size': textSize, 'color': 'black'})

# 矢量图
class Vector():
    def __init__(self, ax0, cutA, cutB, x_label, y_label, a, b, c):
        # 判断a、b、c的数据量关系是否符合要求
        if a is not None and b is not None and c is not None and len(c) == 2 * len(a) * len(b) \
                and not (True in np.isinf(a)) and not (True in np.isinf(b)) and not (True in np.isinf(c)) \
                and not (True in np.isnan(a)) and not (True in np.isnan(b)) and not (True in np.isnan(c)):
            # self.x = a
            # self.y = b
            # self.z = c
            self.type = 'vector'
            a = np.array(a)
            b = np.array(b)
            c = np.array(c)
            # 如果坐标轴是三角函数，则对数据进行变换
            # if "R*cos(Phi)" in x_label:
            #     x = a * np.cos(b)
            # elif "R*sin(Phi)" in x_label:
            #     x = a * np.sin(b)
            # else:
            #     x = a
            # if "R*sin(Phi)" in y_label:
            #     y= a * np.sin(b)
            # elif "R*cos(Phi)" in y_label:
            #     y = a * np.cos(b)
            # else:
            #     y = b
            # x, y = np.meshgrid(x, y)
            x, y = np.meshgrid(a, b)
            # x = x.ravel()
            # y = y.ravel()
            u = c[0:len(a) * len(b)]
            v= c[len(a) * len(b):len(c)]
            index = np.where((u != 0) & (v != 0))
            # N = 1/(np.max([np.abs(u),np.abs(v)]))
            # U2, V2 = u*N, v*N
            L = np.sqrt(u**2 + v**2)

            U = u / L 
            V = v / L 
            #If we just plotted U and V all the vectors would have the same length since 
            #they've been normalized.

            m = np.max(L)
            alpha = 500
            #m is the largest vector, it will correspond to a vector with 
            #magnitude alpha in the quiver plot

            S=alpha /(1+np.log(m/L)) 

            U2=S*U 

            V2=S*V
            # U2=u

            # V2=v
            # sayz("ddddddddddddddd")
            # sayz(np.max([np.abs(u),np.abs(v)]))
            # sayz(np.min(np.concatenate((np.abs(u[index]),np.abs(v[index])))))
            # sayz(np.max([np.abs(u),np.abs(v)])/np.min(np.min(np.concatenate((np.abs(u[index]),np.abs(v[index]))))))
            # u = u.reshape(len(b), len(a))
            # v = v.reshape(len(b), len(a))
            
            # 利用自动缩放算法得到其sacle
            q = ax0.quiver(x, y, U2, V2, color='r', minlength=0,visible=False,units='xy',width =0.0007,headwidth = 6,minshaft =2)
            q._init()
            assert isinstance(q.scale, float)
            # sayz("vvvvvvvvvvvvvvvvqqqqqqqqqqqqqqqqq")
            # sayz([q.units,q.angles,q.scale,q.scale_units ])
            # sayz([q.width ,q.headwidth ,q.headlength ,q.minshaft ,q.minlength ])
            # 在自动缩放算法scale得基础上再缩小一下
            self.vector = ax0.quiver(x, y, U2, V2, color='r', minlength=0,  scale=q.scale * 2,units='xy',width =0.0007,headwidth = 6,minshaft =2)
            # sayz("bbbbbbbbbbbbbbbb")
            # sayz([self.vector.units,self.vector.angles,self.vector.scale,self.vector.scale_units])
            # sayz([self.vector.width, self.vector.headwidth, self.vector.headlength, self.vector.minshaft, self.vector.minlength])
            #       # self.vector = ax0.quiver(x, y, u, v, color='r', minlength =0)
        else:
            DocTools.errorMessage(u"内核导出Hdf5数据中有非法数据，可能计算模型设计有误，请检查模型！\n")
        # 坐标轴标注
        ax0.set_xlabel(x_label, fontdict={'family': 'Times New Roman', 'size': labelSize})
        ax0.set_ylabel(y_label, fontdict={'family': 'Times New Roman', 'size': labelSize})

    # 去掉刻度及坐标轴
    def noaxis(self):
        plt.xticks([])
        plt.yticks([])
        plt.axis('off')

    # 图像信息
    def figinfo(self, ax1, component, time, cut_position, max_vector):
        ax1.text(0.0, 0.95, U'图形名称：矢量图', transform=ax1.transAxes,fontdict={'size': textSize, 'color': 'black'})
        ax1.text(0.0, 0.9, U'观察时间：', transform=ax1.transAxes,
                    fontdict={'size': textSize, 'color': 'black'})
        ax1.text(0.0, 0.9, '                   '+time, transform=ax1.transAxes,
                 fontdict={'family': 'Times New Roman','size': textSize, 'color': 'black'})
        ax1.text(0.0, 0.85, U'观察分量：', transform=ax1.transAxes,
                    fontdict={'size': textSize, 'color': 'black'})
        ax1.text(0.0, 0.85, '                   '+component, transform=ax1.transAxes,
                 fontdict={'family': 'Times New Roman','size': textSize, 'color': 'black'})
        ax1.text(0.0, 0.8, U'横切位置：', transform=ax1.transAxes,fontdict={'size': textSize, 'color': 'black'})
        ax1.text(0.0, 0.8, '                   '+cut_position, transform=ax1.transAxes, fontdict={'family': 'Times New Roman','size': textSize, 'color': 'black'})
        ax1.text(0.0, 0.75, U'最大矢量：',transform=ax1.transAxes, fontdict={'size': textSize, 'color': 'black'})
        ax1.text(0.0, 0.75,  '                   '+max_vector,transform=ax1.transAxes, fontdict={'family': 'Times New Roman','size': textSize, 'color': 'black'})


# 三维等位图
class Contour3D():
    def __init__(self, ax0, x_label, y_label, a, b, c, range_min, range_max,system,range_start, range_end):
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)
        # a = a[0:10]
        # c = c[0:520]
        X, Y = np.meshgrid(a, b)
        Z = c.reshape(len(b), len(a))
        x = X.flatten()
        y = Y.flatten()
        z = Z.flatten()
        x = np.array(x)[::70]
        y = np.array(y)[::70]
        z = np.array(z)[::70]
        # x = np.linspace(0, len(x), num=600)
        # y = np.linspace(0, len(y), num=600)
        # z = np.linspace(0, len(z), num=600)
        norm = mpl.colors.Normalize(vmin=range_min, vmax=range_max)
        self.contour3D = ax0.plot_trisurf(x, y, z, cmap='nipy_spectral', linewidth=0.01, norm=norm)
        plt.pause(0.001)
        cb = plt.colorbar(self.contour3D, ax=ax0,format='%.2e')
        for l in cb.ax.yaxis.get_ticklabels():
            l.set_family('Times New Roman')
            l.set_size(axisSize)
        cb.ax.zorder = -1
        # 坐标轴标注

        self.unit_y, self.pow_y = getUnit(y)
        self.unit_x, self.pow_x = getUnit(x)
        if system == "cylindrical":
            # 柱坐标顺序为zrt
            startList = range_start.split('[')[1].split(']')[0].split(',')
            startZ = float(startList[0])
            startX = float(startList[1])
            startY = float(startList[2])
            endList = range_end.split('[')[1].split(']')[0].split(',')
            endZ = float(endList[0])
            endX = float(endList[1])
            endY = float(endList[2])
        else:
            # 极坐标顺序为rtz，直角坐标顺序为xyz
            startList = range_start.split('[')[1].split(']')[0].split(',')
            startX = float(startList[0])
            startY = float(startList[1])
            startZ = float(startList[2])
            endList = range_end.split('[')[1].split(']')[0].split(',')
            endX = float(endList[0])
            endY = float(endList[1])
            endZ = float(endList[2])

        # 根据刻度的科学计数法得到的单位修改XY坐标轴
        if "R*cos(Phi)" in x_label:
            x_label = "R*cos(Phi)(" + self.unit_x + "m)"
            xlim = getRange("cos", startX, endX, startY, endY)
        elif "R*sin(Phi)" in x_label:
            x_label = "R*sin(Phi)(" + self.unit_x + "m)"
            xlim = getRange("sin", startX, endX, startY, endY)
        elif "Z" in x_label:
            x_label = "Z(" + self.unit_x + "m)"
            xlim = [startZ, endZ]
        elif "X" in x_label:
            x_label = "X(" + self.unit_x + "m)"
            xlim = [startX, endX]
        elif "Y" in x_label:
            x_label = "Y(" + self.unit_x + "m)"
            xlim = [startY, endY]
        elif "R" in x_label:
            x_label = "R(" + self.unit_x + "m)"
            xlim = [startX, endX]
        elif "(" in x_label:
            xlim = [startX, endX]
            x_label = x_label.split("(")[0] + "(" + self.unit_x + "m)"

        if "R*sin(Phi)" in y_label:
            y_label = "R*sin(Phi)(" + self.unit_y + "m)"
            ylim = getRange("sin", startX, endX, startY, endY)
        elif "R*cos(Phi)" in y_label:
            y_label = "R*cos(Phi)(" + self.unit_y + "m)"
            ylim = getRange("cos", startX, endX, startY, endY)
        elif "Z" in y_label:
            y_label = "Z(" + self.unit_y + "m)"
            ylim = [startZ, endZ]
        elif "X" in y_label:
            y_label = "X(" + self.unit_y + "m)"
            ylim = [startX, endX]
        elif "Y" in y_label:
            y_label = "Y(" + self.unit_y + "m)"
            ylim = [startY, endY]
        elif "R" in y_label:
            y_label = "R(" + self.unit_y + "m)"
            ylim = [startX, endX]
        elif "(" in y_label:
            ylim = [startX, endX]
            y_label = y_label.split("(")[0] + "(" + self.unit_y + "m)"
        ax0.set_xlim(xlim)
        ax0.set_ylim(ylim)
        # g%为去掉多余的0
        def formatnum_y(y, pos):

            return '$%g$' % (y / 10 ** self.pow_y)

        # 设置y轴刻度值格式
        formatter1 = FuncFormatter(formatnum_y)
        ax0.yaxis.set_major_formatter(formatter1)

        # g%为去掉多余的0
        def formatnum_x(x, pos):
            return '$%g$' % (x / 10 ** self.pow_x)

        # 设置x轴刻度值格式
        formatter2 = FuncFormatter(formatnum_x)
        ax0.xaxis.set_major_formatter(formatter2)

        # g%为去掉多余的0
        def formatnum_z(z, pos):
            return '$%.2e$' % (z)

        # 设置z轴刻度值格式
        formatter3 = FuncFormatter(formatnum_z)
        ax0.zaxis.set_major_formatter(formatter3)


        ax0.set_xlabel(x_label, fontdict={'family': 'Times New Roman', 'size': labelSize})
        ax0.set_ylabel(y_label, fontdict={'family': 'Times New Roman', 'size': labelSize})

    # 去掉刻度及坐标轴
    def noaxis(self):
        plt.xticks([])
        plt.yticks([])
        plt.axis('off')

    # 图像信息
    def figinfo(self, ax1, time, component, range_start, range_end, range_min, range_max, step):
        ax1.text(0.0, 0.95, U'图形名称：三维等位图', transform=ax1.transAxes, fontdict={'size': textSize, 'color': 'black'})
        ax1.text(0.0, 0.9, U'观察时间：', transform=ax1.transAxes, fontdict={'size': textSize, 'color': 'black'})
        ax1.text(0.0, 0.9, '                   '+time, transform=ax1.transAxes, fontdict={'family': 'Times New Roman','size': textSize, 'color': 'black'})
        ax1.text(0.0, 0.85, U'观察分量：', transform=ax1.transAxes, fontdict={'size': textSize, 'color': 'black'})
        ax1.text(0.0, 0.85, '                   '+component, transform=ax1.transAxes, fontdict={'family': 'Times New Roman','size': textSize, 'color': 'black'})
        ax1.text(0.0, 0.8, U'等值区域：', transform=ax1.transAxes, fontdict={'size': textSize, 'color': 'black'})
        ax1.text(0.0, 0.75, range_start, transform=ax1.transAxes, fontdict={'family': 'Times New Roman','size': textSize, 'color': 'black'})
        ax1.text(0.0, 0.7, range_end, transform=ax1.transAxes, fontdict={'family': 'Times New Roman','size': textSize, 'color': 'black'})
        ax1.text(0.0, 0.65, U'等值范围：', transform=ax1.transAxes, fontdict={'size': textSize, 'color': 'black'})
        ax1.text(0.0, 0.6, 'min: ' + range_min, transform=ax1.transAxes, fontdict={'family': 'Times New Roman','size': textSize, 'color': 'black'})
        ax1.text(0.0, 0.55, 'max: ' + range_max, transform=ax1.transAxes, fontdict={'family': 'Times New Roman','size': textSize, 'color': 'black'})


# 剖面图
class Cut():
    def __init__(self, ax0, x_label, y_label, xy, xyAll,baseData, cutpos, system, isExchange):
        FreeCAD.Console.PrintMessage("aaaaaaaaaaaaaaaaaa")
        self.ax0 = ax0
        self.xyAll = xyAll
        self.baseData = baseData
        self.cutpos = cutpos
        self.system = system
        self.isExchange = isExchange
        self.xy=xy
        # 网格
        self.collectionGridList = []
        self.collectionGridEdgeList = []

        # self.cut = ax0.scatter(x, y, s=1, c="black")

        if x_label and y_label:
            #排除等位图
            if x_label != "contour":

                if x_label == "Phi":
                    x_label = "Phi(rad)"
                else:
                    x_label= x_label+"(m)"
                if y_label == "Phi":
                    y_label = "Phi(rad)"
                else:
                    y_label = y_label + "(m)"

                ax0.set_xlabel(x_label, fontdict={'family': 'Times New Roman', 'size': labelSize})
                ax0.set_ylabel(y_label, fontdict={'family': 'Times New Roman', 'size': labelSize})
                self.type = x_label + "-" + y_label

        # 获取baseData
        mx1 = baseData[0]
        mx2 = baseData[1]
        mx3 = baseData[2]

        import time
        t=time.time()

        color =  ["#989491", "#27b77a", "#c3b17e", "#6fc0b9", "#916048", "#2781b5", "#c5b723", "#3f48c9",
              "#3f48c9", "#3f48c9", "#ff7f26", "#ff7f26", "#ff7f26", "#13cd4f", "#13cd4f", "#13cd4f"]
        for k in range(len(xy)):

            x=xy[k][0]
            y=xy[k][1]

            if x !=[[]] and y!= [[]]:
                if cutpos == "X":
                    if system == "cylindrical":
                        max_x2 = max(mx2)
                        ax0.set_xlim([-max_x2, max_x2])
                        ax0.set_ylim([-max_x2, max_x2])
                        patches = []
                        for i in range(len(x)):
                            r = mx2[x[i][len(x[i]) - 1]]
                            theta1 = mx3[y[i][0] - 1] / (2 * pi) * 360
                            theta2 = mx3[y[i][0]] / (2 * pi) * 360
                            width = mx2[x[i][len(x[i]) - 1]] - mx2[x[i][0] - 1]
                            if isExchange:
                                wedge = Wedge((0, 0), r, theta2, theta1, width=width, color=color[k])
                            else:
                                wedge = Wedge((0, 0), r, theta1, theta2, width=width, color=color[k])
                            patches.append(wedge)
                            # ax0.add_patch(wedge)
                        # for i in range(len(x)):
                        #     if x[i] < size2 and y[i] < size3:
                        #         wedge = Wedge((0, 0), mx2[x[i]-1], mx3[y[i] - 1]/(2*pi)*360, mx3[y[i]]/(2*pi)*360, width=mx2[x[i] - 1]-mx2[x[i]], facecolor=color[k], edgecolor="black")
                        #         ax0.add_patch(wedge)
                        if patches != []:
                            collection = PatchCollection(patches, color=color[k])
                            # 角向器件结构位于最底层
                            collection.set_zorder(-1)
                            ax0.add_collection(collection)

                    else:
                        if x_label != "contour":
                            if isExchange:
                                ax0.set_xlim([min(mx3), max(mx3)])
                                ax0.set_ylim([min(mx2), max(mx2)])
                            else:
                                ax0.set_xlim([min(mx2), max(mx2)])
                                ax0.set_ylim([min(mx3), max(mx3)])
                        patches = []
                        for i in range(len(x)):
                            pos1 = mx2[x[i][0] - 1]
                            pos2 = mx3[y[i][0] - 1]
                            width = mx2[x[i][len(x[i]) - 1]] - mx2[x[i][0] - 1]
                            height = mx3[y[i][0]] - mx3[y[i][0] - 1]
                            if isExchange:
                                rect = Rectangle((pos2, pos1), height, width, color=color[k])
                            else:
                                rect = Rectangle((pos1, pos2), width, height, color=color[k])
                            patches.append(rect)
                            # ax0.add_patch(rect)
                            # if x[i] < size2 and y[i] < size3:
                            #     rect = Rectangle((mx2[x[i] - 1], mx3[y[i] - 1]), mx2[x[i]] - mx2[x[i] - 1],
                            #                      mx3[y[i]] - mx3[y[i] - 1], facecolor=color[k], edgecolor="black")
                            #     ax0.add_patch(rect)
                        if patches != []:
                            collection = PatchCollection(patches, color=color[k])
                            # 设置矩形类器件结构位于上层
                            collection.set_zorder(10)
                            ax0.add_collection(collection)
                elif cutpos == "Y":
                    if x_label != "contour":
                        if isExchange:
                            ax0.set_xlim([min(mx1), max(mx1)])
                            ax0.set_ylim([min(mx3), max(mx3)])
                        else:
                            ax0.set_xlim([min(mx3), max(mx3)])
                            ax0.set_ylim([min(mx1), max(mx1)])

                    patches = []
                    # 由于柱坐标的kmt顺序不同，切片时r或theta在前
                    if system == "cylindrical":
                        for i in range(len(x)):
                            pos1 = mx3[x[i][0] - 1]
                            pos2 = mx1[y[i][0] - 1]
                            width = mx3[x[i][len(x[i]) - 1]] - mx3[x[i][0] - 1]
                            height = mx1[y[i][0]] - mx1[y[i][0] - 1]
                            if not isExchange:
                                rect = Rectangle((pos1, pos2), width, height,
                                                 color=color[k],
                                                 # facecolor=color[k], edgecolor="black"
                                                 )
                            else:
                                rect = Rectangle((pos2, pos1), height, width,
                                                 color=color[k],
                                                 # facecolor=color[k], edgecolor="black"
                                                 )
                            patches.append(rect)
                    else:
                        for i in range(len(x)):
                            pos1 = mx1[x[i][0] - 1]
                            pos2 = mx3[y[i][0] - 1]
                            width = mx1[x[i][len(x[i]) - 1]] - mx1[x[i][0] - 1]
                            height = mx3[y[i][0]] - mx3[y[i][0] - 1]

                            if isExchange:
                                rect = Rectangle((pos1, pos2), width, height,
                                                 color=color[k],
                                                 # facecolor=color[k], edgecolor="black"
                                                 )
                            else:
                                rect = Rectangle((pos2, pos1), height, width,
                                                 color=color[k],
                                                 # facecolor=color[k], edgecolor="black"
                                                 )
                            patches.append(rect)
                        # ax0.add_patch(rect)
                        # if x[i] < size3 and y[i] < size1:
                        #     rect = Rectangle((mx3[x[i] - 1], mx1[y[i] - 1]), mx3[x[i]] - mx3[x[i] - 1],
                        #                      mx1[y[i]] - mx1[y[i] - 1], facecolor=color[k], edgecolor="black")
                        #     ax0.add_patch(rect)
                    if patches != []:
                        collection = PatchCollection(patches,color=color[k])
                        # 设置矩形类器件结构位于上层
                        collection.set_zorder(10)
                        ax0.add_collection(collection)
                elif cutpos == "Z":
                    if system == "polar":

                        max_x1 = max(mx1)
                        ax0.set_xlim([-max_x1, max_x1])
                        ax0.set_ylim([-max_x1, max_x1])
                        patches =[]
                        for i in range(len(x)):
                            r = mx1[x[i][len(x[i]) - 1]]
                            theta1 = mx2[y[i][0] - 1] / (2 * pi) * 360
                            theta2 = mx2[y[i][0]] / (2 * pi) * 360
                            width = mx1[x[i][len(x[i]) - 1]] - mx1[x[i][0] - 1]
                            if isExchange:
                                wedge = Wedge((0, 0), r, theta2, theta1, width=width, color=color[k])
                            else:
                                wedge = Wedge((0, 0), r, theta1, theta2, width=width, color=color[k])
                            patches.append(wedge)
                            # ax0.add_patch(wedge)
                            # if x[i] < size1 and y[i] < size2:
                            #     wedge = Wedge((0, 0), mx1[x[i] - 1], mx2[y[i] - 1] / (2 * pi) * 360, mx2[y[i]] / (2 * pi) * 360,
                            #                   width=mx1[x[i]] - mx1[x[i]-1], facecolor=color[k], edgecolor="black")
                            #     ax0.add_patch(wedge)
                        if patches != []:
                            collection = PatchCollection(patches, color=color[k])
                            # 角向器件结构位于最底层
                            collection.set_zorder(-1)
                            ax0.add_collection(collection)
                    else:
                        if x_label != "contour":
                            if isExchange:
                                ax0.set_xlim([min(mx2), max(mx2)])
                                ax0.set_ylim([min(mx1), max(mx1)])
                            else:
                                ax0.set_xlim([min(mx1), max(mx1)])
                                ax0.set_ylim([min(mx2), max(mx2)])
                        patches = []
                        # 由于柱坐标的kmt顺序不同，切片时r或theta在前
                        if system == "cylindrical":
                            for i in range(len(x)):
                                pos1 = mx2[x[i][0] - 1]
                                pos2 = mx1[y[i][0] - 1]
                                width = mx2[x[i][len(x[i]) - 1]] - mx2[x[i][0] - 1]
                                height = mx1[y[i][0]] - mx1[y[i][0] - 1]
                                if not isExchange:
                                    rect = Rectangle((pos2, pos1), height, width,
                                                     color=color[k],
                                                     # facecolor=color[k], edgecolor="black"
                                                     )
                                else:
                                    rect = Rectangle((pos1, pos2), width, height,
                                                     color=color[k],
                                                     # facecolor=color[k], edgecolor="black"
                                                     )
                                patches.append(rect)
                        else:
                            for i in range(len(x)):
                                pos1 = mx1[x[i][0] - 1]
                                pos2 = mx2[y[i][0] - 1]
                                width = mx1[x[i][len(x[i]) - 1]] - mx1[x[i][0] - 1]
                                height = mx2[y[i][0]] - mx2[y[i][0] - 1]
                                if isExchange:
                                    rect = Rectangle((pos2, pos1), height, width,
                                                     color=color[k],
                                                     # facecolor=color[k], edgecolor="black"
                                                     )
                                else:
                                    rect = Rectangle((pos1, pos2), width, height,
                                                     color=color[k],
                                                     # facecolor=color[k], edgecolor="black"
                                                     )
                                patches.append(rect)
                        # for i in range(len(x)):
                        #     if x[i] < size1 and y[i] < size2:
                        #         rect = Rectangle((mx1[x[i] - 1], mx2[y[i] - 1]), mx1[x[i]] - mx1[x[i] - 1],
                        #                          mx2[y[i]] - mx2[y[i] - 1], facecolor=color[k], edgecolor="black")
                        #         ax0.add_patch(rect)
                        if patches != []:
                            collection = PatchCollection(patches, color=color[k])
                            collection.set_zorder(10)
                            ax0.add_collection(collection)
        sayz("没有网格绘制时间")
        sayz(time.time()-t)

    # 优化后合并后绘制大网格及边框，然后在大网格内绘制线划分网格，速度提高
    def drawStructGridFast(self):
        import time
        t = time.time()
        # 获取baseData
        mx1 = np.array(self.baseData[0])
        mx2 = np.array(self.baseData[1])
        mx3 = np.array(self.baseData[2])
        color = ["#989491", "#27b77a", "#c3b17e", "#6fc0b9", "#916048", "#2781b5", "#c5b723", "#3f48c9",
                 "#3f48c9", "#3f48c9", "#ff7f26", "#ff7f26", "#ff7f26", "#13cd4f", "#13cd4f", "#13cd4f"]
        colorEdge=["#000000","#51ffce","#ffffd3","#bfffff","#f5a67d","#4fdbff","#fffe4b","#9097f9",
            "#9097f9","#9097f9","#fbceaf","#fbceaf","#fbceaf","#80f9a0","#80f9a0","#80f9a0"]
        for k in range(len(self.xy)):
            x=self.xy[k][0]
            y=self.xy[k][1]
            xAll = self.xyAll[k][0]
            yAll = self.xyAll[k][1]
            # 分别表示外边框和里面加的网格
            collectionGridEdge = None
            collectionGrid = None
            # sayz("Cut")
            if x != [[]] and y != [[]] and xAll!=[[]] and yAll!=[[]]:
                if self.cutpos == "X":
                    if self.system == "cylindrical":
                        # if self.isExchange:
                        #     max_x2 = max(mx2)
                        # else:
                        #     max_x2 = max(mx2)
                        # self.ax0.set_xlim([-max_x2 - max_x2 / 5, max_x2 + max_x2 / 5])
                        # self.ax0.set_ylim([-max_x2 - max_x2 / 5, max_x2 + max_x2 / 5])
                        patches = []
                        for i in range(len(xAll)):
                            r = mx2[xAll[i]]
                            theta1 = mx3[yAll[i] - 1] / (2 * pi) * 360
                            theta2 = mx3[yAll[i]] / (2 * pi) * 360
                            width = mx2[xAll[i]] - mx2[xAll[i] - 1]
                            if self.isExchange:
                                wedge = Wedge((0, 0), r, theta2, theta1, width=width, facecolor=color[k], edgecolor=colorEdge[k])
                            else:
                                wedge = Wedge((0, 0), r, theta1, theta2, width=width, facecolor=color[k], edgecolor=colorEdge[k])
                            patches.append(wedge)
                            # ax0.add_patch(wedge)
                        # for i in range(len(x)):
                        #     if x[i] < size2 and y[i] < size3:
                        #         wedge = Wedge((0, 0), mx2[x[i]-1], mx3[y[i] - 1]/(2*pi)*360, mx3[y[i]]/(2*pi)*360, width=mx2[x[i] - 1]-mx2[x[i]], facecolor=color[k], edgecolor=colorEdge[k])
                        #         ax0.add_patch(wedge)
                        collectionGridEdge = PatchCollection(patches, facecolor=color[k], edgecolor=colorEdge[k])
                        # 角向器件结构位于最底层
                        collectionGridEdge.set_zorder(0)
                        self.ax0.add_collection(collectionGridEdge)

                    else:
                        # if self.isExchange:
                        #     self.ax0.set_xlim([min(mx3), max(mx3)])
                        #     self.ax0.set_ylim([min(mx2), max(mx2)])
                        # else:
                        #     self.ax0.set_xlim([min(mx2), max(mx2)])
                        #     self.ax0.set_ylim([min(mx3), max(mx3)])
                        patches = []
                        lineList = []
                        for i in range(len(x)):
                            pos1 = mx2[x[i][0] - 1]
                            pos2 = mx3[y[i][0] - 1]
                            width = mx2[x[i][len(x[i]) - 1]] - mx2[x[i][0] - 1]
                            height = mx3[y[i][0]] - mx3[y[i][0] - 1]

                            if self.isExchange:

                                b = mx2[np.array(x[i])]
                                a =np.array([mx3[y[i][0] - 1],mx3[y[i][0]]])
                                rect = Rectangle((pos2, pos1), height, width, color=color[k])
                            else:
                                a = mx2[np.array(x[i])]
                                b = np.array([mx3[y[i][0] - 1],mx3[y[i][0]]])
                                rect = Rectangle((pos1, pos2), width, height, color=color[k])

                            patches.append(rect)
                            # 绘制合并的网格里的线
                            hlines = np.column_stack(np.broadcast_arrays(a[0], b, a[-1], b))

                            vlines = np.column_stack(np.broadcast_arrays(a, b[0], a, b[-1]))

                            lines = np.concatenate([hlines, vlines]).reshape(-1, 2, 2)
                            # 合并到一个array里
                            if lineList == []:
                                lineList = lines
                            else:
                                lineList = np.append(lineList, lines, axis=0)
                        collectionGrid = LineCollection(lineList, color=colorEdge[k], linewidths=1)

                        # 设置矩形类器件结构位于上层
                        collectionGrid.set_zorder(11)
                        self.ax0.add_collection(collectionGrid)
                        collectionGridEdge = PatchCollection(patches, color=color[k], edgecolor=colorEdge[k])
                        # 设置矩形类器件结构位于上层
                        collectionGridEdge.set_zorder(10)
                        self.ax0.add_collection(collectionGridEdge)
                elif self.cutpos == "Y":
                    # if self.isExchange:
                    #     self.ax0.set_xlim([min(mx1), max(mx1)])
                    #     self.ax0.set_ylim([min(mx3), max(mx3)])
                    # else:
                    #     self.ax0.set_xlim([min(mx3), max(mx3)])
                    #     self.ax0.set_ylim([min(mx1), max(mx1)])

                    sayz(self.cutpos)
                    patches = []
                    lineList = []
                    # 由于柱坐标的kmt顺序不同，切片时r或theta在前
                    if self.system == "cylindrical":
                        for i in range(len(x)):
                            pos1 = mx3[x[i][0] - 1]
                            pos2 = mx1[y[i][0] - 1]
                            width = mx3[x[i][len(x[i]) - 1]] - mx3[x[i][0] - 1]
                            height = mx1[y[i][0]] - mx1[y[i][0] - 1]
                            if not self.isExchange:
                                a = mx3[np.array(x[i])]
                                # np.insert(x, 0, mx3[x[i][0] - 1])
                                b = np.array([mx1[y[i][0] - 1],mx1[y[i][0]]])
                                rect = Rectangle((pos1, pos2), width,height,
                                                 color=color[k],
                                                 # facecolor=color[k], edgecolor=colorEdge[k]
                                                 )
                            else:
                                b = mx3[np.array(x[i])]
                                # np.insert(y, 0, mx3[x[i][0] - 1])
                                a = np.array([mx1[y[i][0] - 1],mx1[y[i][0]]])
                                rect = Rectangle((pos2, pos1),  height,width,
                                                 color=color[k],
                                                 # facecolor=color[k], edgecolor=colorEdge[k]
                                                 )
                            patches.append(rect)
                            hlines = np.column_stack(np.broadcast_arrays(a[0], b, a[-1], b))

                            vlines = np.column_stack(np.broadcast_arrays(a, b[0], a, b[-1]))

                            lines = np.concatenate([hlines, vlines]).reshape(-1, 2, 2)
                            if lineList == []:
                                lineList = lines
                            else:
                                lineList = np.append(lineList, lines, axis=0)
                        collectionGrid = LineCollection(lineList, color=colorEdge[k], linewidths=1)

                        # 设置矩形类器件结构位于上层
                        collectionGrid.set_zorder(11)
                        self.ax0.add_collection(collectionGrid)

                    else:

                        for i in range(len(x)):
                            pos1 = mx1[x[i][0] - 1]
                            pos2 = mx3[y[i][0] - 1]
                            width = mx1[x[i][len(x[i]) - 1]] - mx1[x[i][0] - 1]
                            height = mx3[y[i][0]] - mx3[y[i][0] - 1]
                            if self.isExchange:
                                a = mx1[np.array(x[i])]
                                b = np.array([mx3[y[i][0] - 1],mx3[y[i][0]]])
                                rect = Rectangle((pos1, pos2), width, height,
                                                 color=color[k],
                                                 # facecolor=color[k], edgecolor=colorEdge[k]
                                                 )
                            else:
                                b = mx1[np.array(x[i])]
                                a = np.array([mx3[y[i][0] - 1],mx3[y[i][0]]])
                                rect = Rectangle((pos2, pos1), height, width,
                                                 color=color[k],
                                                 # facecolor=color[k], edgecolor=colorEdge[k]
                                                 )
                            patches.append(rect)
                            hlines = np.column_stack(np.broadcast_arrays(a[0], b, a[-1], b))

                            vlines = np.column_stack(np.broadcast_arrays(a, b[0], a, b[-1]))

                            lines = np.concatenate([hlines, vlines]).reshape(-1, 2, 2)
                            if lineList == []:
                                lineList = lines
                            else:
                                lineList = np.append(lineList, lines, axis=0)
                        collectionGrid = LineCollection(np.array(lineList), color=colorEdge[k], linewidths=1)

                        # 设置矩形类器件结构位于上层
                        collectionGrid.set_zorder(11)
                        self.ax0.add_collection(collectionGrid)
                    collectionGridEdge = PatchCollection(patches, color=color[k], edgecolor=colorEdge[k])
                    # 设置矩形类器件结构位于上层
                    collectionGridEdge.set_zorder(10)
                    self.ax0.add_collection(collectionGridEdge)
                elif self.cutpos == "Z":
                    lineList = []
                    if self.system == "polar":
                        # if self.isExchange:
                        #     max_x1 = max(mx2)
                        # else:
                        #     max_x1 = max(mx1)
                        # self.ax0.set_xlim([-max_x1 - max_x1 / 5, max_x1 + max_x1 / 5])
                        # self.ax0.set_ylim([-max_x1 - max_x1 / 5, max_x1 + max_x1 / 5])
                        patches = []
                        for i in range(len(xAll)):
                            r = mx1[xAll[i]]
                            theta1 = mx2[yAll[i] - 1] / (2 * pi) * 360
                            theta2 = mx2[yAll[i]] / (2 * pi) * 360
                            width = mx1[xAll[i]] - mx1[xAll[i] - 1]
                            if self.isExchange:
                                wedge = Wedge((0, 0), r, theta2, theta1, width=width, facecolor=color[k], edgecolor=colorEdge[k])
                            else:
                                wedge = Wedge((0, 0), r, theta1, theta2, width=width, facecolor=color[k], edgecolor=colorEdge[k])
                            patches.append(wedge)
                            # ax0.add_patch(wedge)
                            # if x[i] < size1 and y[i] < size2:
                            #     wedge = Wedge((0, 0), mx1[x[i] - 1], mx2[y[i] - 1] / (2 * pi) * 360, mx2[y[i]] / (2 * pi) * 360,
                            #                   width=mx1[x[i]] - mx1[x[i]-1], facecolor=color[k], edgecolor=colorEdge[k])
                            #     ax0.add_patch(wedge)
                        collectionGridEdge = PatchCollection(patches, facecolor=color[k], edgecolor=colorEdge[k])
                        # 角向器件结构位于最底层
                        collectionGridEdge.set_zorder(0)
                        self.ax0.add_collection(collectionGridEdge)
                    else:
                        # if self.isExchange:
                        #     self.ax0.set_xlim([min(mx2), max(mx2)])
                        #     self.ax0.set_ylim([min(mx1), max(mx1)])
                        # else:
                        #     self.ax0.set_xlim([min(mx1), max(mx1)])
                        #     self.ax0.set_ylim([min(mx2), max(mx2)])
                        patches = []
                        # 由于柱坐标的kmt顺序不同，切片时r或theta在前
                        if self.system == "cylindrical":

                            for i in range(len(x)):
                                pos1 = mx2[x[i][0] - 1]
                                pos2 = mx1[y[i][0] - 1]
                                width = mx2[x[i][len(x[i]) - 1]] - mx2[x[i][0] - 1]
                                height = mx1[y[i][0]] - mx1[y[i][0] - 1]
                                if not self.isExchange:
                                    b = mx2[np.array(x[i])]
                                    a = np.array([mx1[y[i][0] - 1],mx1[y[i][0]]])
                                    rect = Rectangle((pos2, pos1), height, width,
                                                     color=color[k],
                                                     # facecolor=color[k], edgecolor=colorEdge[k]
                                                     )
                                else:
                                    a = mx2[np.array(x[i])]
                                    b = np.array([mx1[y[i][0] - 1],mx1[y[i][0]]])
                                    rect = Rectangle((pos1, pos2), width, height,
                                                     color=color[k],
                                                     # facecolor=color[k], edgecolor=colorEdge[k]
                                                     )
                                patches.append(rect)
                                hlines = np.column_stack(np.broadcast_arrays(a[0], b, a[-1], b))

                                vlines = np.column_stack(np.broadcast_arrays(a, b[0], a, b[-1]))

                                lines = np.concatenate([hlines, vlines]).reshape(-1, 2, 2)
                                if lineList == []:
                                    lineList = lines
                                else:
                                    lineList = np.append(lineList, lines, axis=0)
                            collectionGrid = LineCollection(lineList, color=colorEdge[k], linewidths=1)

                            # 设置矩形类器件结构位于上层
                            collectionGrid.set_zorder(11)
                            self.ax0.add_collection(collectionGrid)

                        else:
                            for i in range(len(x)):
                                pos1 = mx1[x[i][0] - 1]
                                pos2 = mx2[y[i][0] - 1]
                                width = mx1[x[i][len(x[i]) - 1]] - mx1[x[i][0] - 1]
                                height = mx2[y[i][0]] - mx2[y[i][0] - 1]
                                if self.isExchange:
                                    b = mx1[np.array(x[i])]
                                    a = np.array([mx2[y[i][0] - 1],mx2[y[i][0]]])
                                    rect = Rectangle((pos2, pos1), height, width,
                                                     color=color[k],
                                                     # facecolor=color[k], edgecolor=colorEdge[k]
                                                     )
                                else:
                                    a = mx1[np.array(x[i])]
                                    b = np.array([mx2[y[i][0] - 1],mx2[y[i][0]]])
                                    rect = Rectangle((pos1, pos2), width, height,
                                                     color=color[k],
                                                     # facecolor=color[k], edgecolor=colorEdge[k]
                                                     )
                                patches.append(rect)
                                hlines = np.column_stack(np.broadcast_arrays(a[0], b, a[-1], b))

                                vlines = np.column_stack(np.broadcast_arrays(a, b[0], a, b[-1]))

                                lines = np.concatenate([hlines, vlines]).reshape(-1, 2, 2)
                                if lineList == []:
                                    lineList = lines
                                else:
                                    lineList = np.append(lineList, lines, axis=0)
                            collectionGrid = LineCollection(lineList, color=colorEdge[k], linewidths=1)

                            # 设置矩形类器件结构位于上层
                            collectionGrid.set_zorder(11)
                            self.ax0.add_collection(collectionGrid)
                        collectionGridEdge = PatchCollection(patches, color=color[k], edgecolor=colorEdge[k])
                        collectionGridEdge.set_zorder(10)
                        self.ax0.add_collection(collectionGridEdge)

            if collectionGrid != None:
                self.collectionGridList.append(collectionGrid)
            if collectionGridEdge != None:
                self.collectionGridEdgeList.append(collectionGridEdge)

        sayz(time.time() - t)

    def showCutGrid(self):

        # 网格中的线
        for collectionGrid in self.collectionGridList:
            collectionGrid.set_visible(not collectionGrid.get_visible())
        # 大网格的边框
        for collectionGridEdge in self.collectionGridEdgeList:
            collectionGridEdge.set_visible(not collectionGridEdge.get_visible())
    # 去掉刻度及坐标轴
    def noaxis(self):
        plt.xticks([])
        plt.yticks([])
        plt.axis('off')

    # 图像信息
    def figinfo(self, ax1, type):
        #排除等位图中的剖面结构图情况
        if type !="contour-contour":
            ax1.text(0.0, 0.95, U'图形名称：剖面结构图', transform=ax1.transAxes,fontdict={'size': textSize, 'color': 'black'})
            ax1.text(0.0, 0.9, U'剖面类型：', transform=ax1.transAxes,fontdict={'size': textSize, 'color': 'black'})
            ax1.text(0.0, 0.9, '                   '+type, transform=ax1.transAxes, fontdict={'family': 'Times New Roman','size': textSize, 'color': 'black'})


# freeCAD plot绘图的关键部分
class Plot(PySide.QtGui.QWidget):
    def __init__(self,
                 IsTriggerCloseEvent,
                 winTitle="plot",
                 fileName="fileName",
                 parent=None,
                 flags=PySide.QtCore.Qt.WindowFlags(0)):
        """Construct a new plot widget.

        Keyword arguments:
        winTitle -- Tab title.
        parent -- Widget parent.
        flags -- QWidget flags
        """
        self.IsTriggerCloseEvent = IsTriggerCloseEvent
        self.winTitle = winTitle
        self.fileName = fileName
        PySide.QtGui.QWidget.__init__(self, parent, flags)
        self.setWindowTitle(winTitle)
        # Create matplotlib canvas
        self.fig = plt.figure()
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self)
        # 将窗口以2:1的比例分开
        self.gs = gridspec.GridSpec(1, 2, width_ratios=[2.5, 1])
        # Get axes
        self.axes = self.fig.add_subplot(111)
        self.axesList = [self.axes]
        self.axes.xaxis.set_ticks_position('bottom')
        self.axes.spines['top'].set_color('none')
        self.axes.yaxis.set_ticks_position('left')
        self.axes.spines['right'].set_color('none')

        # 图像显示区域
        self.axleft = plt.subplot(self.gs[0])
        # 将图像显示区域的坐标轴刻度值字体设为Times New Roman，大小设为
        plt.tick_params( labelsize=axisSize)
        labels = self.axleft.get_xticklabels() + self.axleft.get_yticklabels()
        for label in labels:
            label.set_fontname('Times New Roman')

        # 图像信息区域
        self.axright = plt.subplot(self.gs[1])
        # Add the navigation toolbar by default

        self.mpl_toolbar = NavigationToolbar(self.canvas, self)
        # Setup layout
        vbox = PySide.QtGui.QVBoxLayout()
        vbox.addWidget(self.canvas)
        vbox.addWidget(self.mpl_toolbar)
        self.setLayout(vbox)
        # Active series
        self.series = []
        # Indicators
        self.skip = False
        self.legend = False
        self.legPos = (1.0, 1.0)
        self.legSiz = 16
        self.grid = False
        # 器件结构
        self.cut =None

    def closeEvent(self, event):
        # if self.IsTriggerCloseEvent == True:
        #     import Visualization.VisualizationCommand.VisualizationFigTree as VisualizationFigTree
        #     VisualizationFigTree.removeTreeNode(self)
        # 重写关闭触发事件，关闭subwindow时不删除对象
        mdi = getMdiArea()
        if not mdi:
            return None
        sub = mdi.activeSubWindow()
        if not sub:
            return None
        if not LIST.has_key(self.winTitle+self.fileName):
            LIST[self.winTitle+self.fileName] = self
        # 解除QMdiSunWindow与plot对象的绑定关系
        #  if an internal widget is passed in the child widget is set to 0 but the QMdiSubWindow is not removed.
        mdi.removeSubWindow(self)

        # 关闭
        sub.close()

    def plot(self, x, y, name=None):
        """Plot a new line and return it.

        Keyword arguments:
        x -- X values
        y -- Y values
        name -- Serie name (for legend). """
        l = Line(self.axes, x, y, name)
        self.series.append(l)
        # Update window
        self.update()
        return l

    def contour_plot(self, cutA, cutB, x_label, y_label,system, time, component,
                     range_start, range_end, range_min, range_max, step, a, b, c, tag, isRatio):

        FreeCAD.Console.PrintMessage("contour_plot+++++++++++++++++++++\n")
        # 计算等值区域
        range_min_float = float(range_min)
        range_max_float = float(range_max)
        c_min = np.min(c)
        c_max = np.max(c)
        range_min_float = min(range_min_float,c_min)
        range_max_float = max(range_max_float,c_max)
        step_float = float(step)
        FreeCAD.Console.PrintMessage("contour_plot+++++++++++++++++++++\n")
        contour_list = []
        contour_list.append(range_min_float)
        # 根据等值范围，以及步长获得等差的等值线list
        contour = range_min_float
        while (contour >= range_min_float) and (contour <= range_max_float):
            contour = contour + step_float
            if contour < range_max_float:
                contour_list.append(contour)
        contour_list.append(range_max_float)
        level = np.array(contour_list)
        FreeCAD.Console.PrintMessage("contour_plot+++++++++++++++++++++\n")
        # 根据list中c获取等值范围
        c_min = np.min(c)
        c_max = np.max(c)
        # 如果最大值大于10且isRatio为1，则绘制等比等值线对应的等位图
        if c_max >= 10 and isRatio:
            try:
                # 等值线为10的x次，x为最大值的科学计数法指数
                index_max = int(math.log10(c_max))

                if c_min>0:
                    index_min = int(math.log10(math.fabs(c_min)))
                # 如果最小值为负数，x为科学计数法指数的相反数
                elif c_min<0:
                    index_min = -int(math.log10(math.fabs(c_min)))

                else:
                    index_min=0

                # 如果最大最小值超过10，则增大间隔
                interval = (index_max-index_min)/5
                if interval<1:
                    interval=1
                index = np.array(range(index_min, index_max + 1,interval))
                sayz(index)
                # index = np.array(range(index_min,index_max+1))
                index_abs = np.array(map(abs,index))

                level = index/index_abs * (10**index_abs)

                level = np.nan_to_num(level).tolist()
                # 首位最大最小值，以防有空白
                level.insert(0, c_min)
                level.append(c_max)
                level = np.array(level)
            except:
                FreeCAD.Console.PrintError("level 计算失败，使用默认值\n")
        FreeCAD.Console.PrintMessage("contour_plot+++++++++++++++++++++\n")
        # 绘制等值图
        # 判断是否有nan或者-inf或者inf在level中
        if True in np.isnan(level) or True in np.isinf(level):
            sayzerr("The attr19 and attr21 of data is bad")
            level = 8
            # return "error"
        con = Contour(self.axleft, cutA, cutB, x_label, y_label, a, b, c, level, tag,isRatio,system,range_start, range_end)
        FreeCAD.Console.PrintMessage("contour_plot+++++++++++++++++++++\n")
        con.noaxis()
        FreeCAD.Console.PrintMessage("contour_plot+++++++++++++++++++++\n")
        con.figinfo(self.axright, time, component, range_start, range_end, range_min, range_max, step)
        FreeCAD.Console.PrintMessage("contour_plot+++++++++++++++++++++\n")
        self.series.append(con)
        self.update()
        FreeCAD.Console.PrintMessage("contour_plot+++++++++++++++++++++\n")
        #获取图的横纵坐标范围
        data_x_min = self.axleft.get_xlim()
        data_y_min =self.axleft.get_ylim()
        #鼠标滚轮事件
        self.axleft.figure.canvas.mpl_connect('scroll_event',
                                       lambda event: scroll_event(event, self.axleft, data_x_min, data_y_min))
        return con

    def observe_plot(self, x_label, y_label, type, range_min, range_max, x, y, name=None):
        obs = Observe(self.axleft, x_label, y_label, type,x, y, name)
        obs.noaxis()
        obs.figinfo(self.axright, type, range_min, range_max)
        self.series.append(obs)
        self.update()
        data_x_min = self.axleft.get_xlim()
        data_y_min = self.axleft.get_ylim()
        self.axleft.figure.canvas.mpl_connect('scroll_event',
                                    lambda event: scroll_event(event, self.axleft, data_x_min, data_y_min))
        return obs

    def phasespace_plot(self, cutA, cutB, x_label, y_label, particle, time, x, y, name=None,z=None):
        pha = Phasespace(self.axleft, cutA, cutB, x_label, y_label, x, y, name,z)
        pha.noaxis()
        pha.figinfo(self.axright, particle, time)
        self.series.append(pha)
        self.update()
        data_x_min = self.axleft.get_xlim()
        data_y_min = self.axleft.get_ylim()
        self.axleft.figure.canvas.mpl_connect('scroll_event',
                                    lambda event: scroll_event(event, self.axleft, data_x_min, data_y_min))
        return pha

    def range_plot(self, x_label, y_label, time, component, range_min, range_max, x, y, name=None):
        range = Range(self.axleft, x_label, y_label, x, y, name)
        range.noaxis()
        range.figinfo(self.axright, time, component, range_min, range_max)
        self.series.append(range)
        self.update()
        data_x_min = self.axleft.get_xlim()
        data_y_min = self.axleft.get_ylim()
        self.axleft.figure.canvas.mpl_connect('scroll_event',
                                    lambda event: scroll_event(event, self.axleft, data_x_min, data_y_min))
        return range

    def vector_plot(self, cutA, cutB, x_label, y_label, component, time, cut_position, max_vector, a, b, c):
        vector = Vector(self.axleft, cutA, cutB, x_label, y_label, a, b, c)
        vector.noaxis()
        vector.figinfo(self.axright, component, time, cut_position, max_vector)
        self.series.append(vector)
        self.update()
        data_x_min = self.axleft.get_xlim()
        data_y_min = self.axleft.get_ylim()
        self.axleft.figure.canvas.mpl_connect('scroll_event',
                                    lambda event: scroll_event(event, self.axleft, data_x_min, data_y_min))
        return vector

    def contour_3D(self, x_label, y_label, system,time, component,
                         range_start, range_end, range_min, range_max, step, a, b, c):
        # 计算等值区域
        range_min_float = float(range_min)
        range_max_float = float(range_max)
        # 绘制等值图
        self.axleft = plt.subplot(self.gs[0],  projection='3d')
        # 将图像显示区域的坐标轴刻度值字体设为Times New Roman，大小设为
        plt.tick_params(labelsize=axisSize)
        labels = self.axleft.get_xticklabels() + self.axleft.get_yticklabels()+ self.axleft.get_zticklabels()
        for label in labels:
            label.set_fontname('Times New Roman')
        self.axright = plt.subplot(self.gs[1])
        con3d = Contour3D(self.axleft, x_label, y_label, a, b, c, range_min_float, range_max_float,system,range_start, range_end)
        con3d.noaxis()
        con3d.figinfo(self.axright, time, component, range_start, range_end, range_min, range_max, step)
        self.update()
        return con3d
    def Cut2D(self,baseData):
        class polygon:
            def __init__(self):
                self.xy = []
                self.tepe = 0
                self.d = 1
        xData = baseData[1][0]
        yData = baseData[1][1]
        dataSize = len(baseData[1][2])
        data = baseData[1][2]
        i = 0
        poly = polygon()
        polys = []
        xs = []
        ys =[]
        while i < dataSize: 
            if poly.d != data[i + 3]:
                polys.append(poly)
                poly = polygon()
                poly.d = data[i + 3]
            temp = []
            x = xData[int(data[i]) - 1]
            y = yData[int(data[i+1]) - 1]
            xs.append(x)
            ys.append(y)
            temp.append(x)
            temp.append(y)
            poly.xy.append(temp)
            poly.type = data[i+2]
            i = i + 4
        polys.append(poly)
        FreeCAD.Console.PrintMessage(str(len(polys)) +"+++++++++++\n")
        
        from matplotlib.path import Path
        from matplotlib.patches import PathPatch
        edgecolors = ['black','#0000FF','#8A2BE2','#A52A2A','#DEB887','#5F9EA0','#7FFF00','#D2691E','#0000CD','#6495ED','#DC143C','#B22222','#FF00FF','#4B0082','black','#FF00F9']
        paths = []
        for p in polys:
            vertices = []
            codes = [Path.MOVETO] + [Path.MOVETO]
            vertices.append((0,0))
            vertices.append((0,0))
            lineSize = len(p.xy) - 1
            codes += [Path.MOVETO] + [Path.LINETO]*lineSize + [Path.CLOSEPOLY]
            for xy in p.xy:
                vertices.append((xy[0],xy[1]))
            vertices.append((0,0))
            path = Path(vertices, codes)
            #pathpatch = PathPatch(path,facecolor='gray', edgecolor=edgecolors[int(p.type) - 1])
            color = 'gray'
            f = True
            lst = 'solid'
            lineWidth = 1.1
            if p.type != 1:
                f= False
                lst='dotted'
                lineWidth = 5.1
            if p.type == 15:
                f = True
                color = 'white'
                lst = 'solid'
                lineWidth = 1.1
            
            pathpatch = PathPatch(path,facecolor=color,fill = f,linestyle=lst, edgecolor=edgecolors[int(p.type) - 1])
            
            pathpatch.set_linewidth(lineWidth)
            paths.append(pathpatch)
        #这里倒序输入路径，因为h5数据的空类型放到了前面       
        for pp in reversed(paths):
            self.axleft.add_patch(pp)
        self.axleft.autoscale_view()
        self.axleft.set_xlim(min(xs),max(xs))
        self.axleft.set_ylim(min(ys),max(ys))
        self.update()

        plt.xticks([])
        plt.yticks([])
        plt.axis('off')

    def cut_plot(self, ab,abAll, figName, baseData, cutpos, system, isExchange):
        # sayz("cut_plot")
        FreeCAD.Console.PrintMessage(str(figName) + "cut_plot+++++++++++++++++++++\n")
        FreeCAD.Console.PrintMessage(str(len(baseData)) + "||cut_plot+++++++++++++++++++++\n")
        if len(baseData) == 5 and (figName != "contour-contour" and figName != None):
            FreeCAD.Console.PrintMessage(str(figName) + "cut_plot+++++++++++++++++++++\n")
            self.Cut2D(baseData)
            FreeCAD.Console.PrintMessage("cut_plot+++++++++++++++++++++\n")
            self.axright.text(0.0, 0.95, U'图形名称：剖面结构图', transform=self.axright.transAxes,fontdict={'size': textSize, 'color': 'black'})
            self.axright.text(0.0, 0.9, U'剖面类型：2d器件结构图', transform=self.axright.transAxes,fontdict={'size': textSize, 'color': 'black'})
            self.axright.text(0.0, 0.9, '                   ', transform=self.axright.transAxes, fontdict={'family': 'Times New Roman','size': textSize, 'color': 'black'})
            self.update()
            return
        if len(baseData) == 5:
            self.Cut2D(baseData)
            FreeCAD.Console.PrintMessage("cut_plot+++++++++++++++++++++\n")
            return
        elif ab is None or abAll is None:
            return
        # figName:"contour-contour"代表等位图中剖面结构
        # figName:R-Z等,代表剖面结构图
        # figName:None,代表其他图中改的坡面剖面结构图
        elif figName:
            label = figName.split("-", 1)
            x_label = label[0]
            y_label = label[1]
            self.cut = Cut(self.axleft, x_label, y_label, ab, abAll,baseData, cutpos, system, isExchange)
            self.cut.noaxis()
            self.cut.figinfo(self.axright, figName)
        else:
            # sayz("cut----")
            self.cut = Cut(self.axleft, None, None, ab,abAll, baseData, cutpos, system, isExchange)
            self.cut.noaxis()
        self.cut.drawStructGridFast()
        self.update()
        data_x_min = self.axleft.get_xlim()
        data_y_min = self.axleft.get_ylim()
        self.axleft.figure.canvas.mpl_connect('scroll_event',
                                              lambda event: scroll_event(event, self.axleft, data_x_min, data_y_min))
        return self.cut

    def update(self):
        """Update the plot, redrawing the canvas."""
        if not self.skip:
            self.skip = True
            if self.legend:
                legend(self.legend, self.legPos, self.legSiz)
            self.canvas.draw()
            self.skip = False

    def isGrid(self):
        """Return True if Grid is active, False otherwise."""
        return bool(self.grid)

    def isLegend(self):
        """Return True if Legend is active, False otherwise."""
        return bool(self.legend)

    def setActiveAxes(self, index):
        """Change the current active axes.

        Keyword arguments:
        index -- Index of the new active axes set.
        """
        self.axes = self.axesList[index]
        self.fig.sca(self.axes)

#鼠标滚轮触发事件
def scroll_event(event, axes, data_x_min, data_y_min):
    if event.inaxes == axes:
        x_min, x_max = axes.get_xlim()
        y_min, y_max = axes.get_ylim()
        range_x = (x_max - x_min) / 30
        range_y = (y_max - y_min) / 30
        if event.button == 'up':
            axes.set(xlim=(x_min + range_x, x_max - range_x))
            axes.set(ylim=(y_min + range_y, y_max - range_y))
        elif event.button == 'down':
            if x_min > data_x_min[0] and y_min > data_y_min[0]:
                if x_min - range_x < data_x_min[0]:
                    axes.set(xlim=(data_x_min[0], data_x_min[1]))
                    axes.set(ylim=(data_y_min[0], data_y_min[1]))
                else:
                    axes.set(xlim=(x_min - range_x, x_max + range_x))
                    axes.set(ylim=(y_min - range_y, y_max + range_y))
        axes.figure.canvas.draw_idle()  # 重新绘制整个图表

def sayz(msg):
    FreeCAD.Console.PrintMessage(msg)
    FreeCAD.Console.PrintMessage('\n')
def sayzerr(msg):
    FreeCAD.Console.PrintError(msg)
    FreeCAD.Console.PrintWarning('\n')