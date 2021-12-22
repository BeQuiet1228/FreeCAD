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

import FreeCAD as App
import FreeCADGui as Gui

from PySide import QtGui, QtCore

import vPlot


class TaskPanel:
    def __init__(self):
        path = App.ConfigGet("AppHomePath") + "Mod/Visualization/VisualizationGui"
        self.ui = path + "/plotAxes/TaskPanel.ui"

    def accept(self):
        return True

    def reject(self):
        return True

    def clicked(self, index):
        pass

    def open(self):
        pass

    def needsFullSpace(self):
        return True

    def isAllowedAlterSelection(self):
        return False

    def isAllowedAlterView(self):
        return True

    def isAllowedAlterDocument(self):
        return False

    def helpRequested(self):
        pass

    def setupUi(self):
        mw = self.getMainWindow()
        form = mw.findChild(QtGui.QWidget, "TaskPanel")
        self.form = form
        form.xMin = self.widget(QtGui.QLineEdit, "LineEdit_Xmin")
        form.xMax = self.widget(QtGui.QLineEdit, "LineEdit_Xmax")
        form.yMin = self.widget(QtGui.QLineEdit, "LineEdit_Ymin")
        form.yMax = self.widget(QtGui.QLineEdit, "LineEdit_Ymax")
        self.retranslateUi()
        self.updateUI()

        QtCore.QObject.connect(form.xMin,
                               QtCore.SIGNAL("editingFinished()"),
                               self.onScales)
        QtCore.QObject.connect(form.xMax,
                               QtCore.SIGNAL("editingFinished()"),
                               self.onScales)
        QtCore.QObject.connect(form.yMin,
                               QtCore.SIGNAL("editingFinished()"),
                               self.onScales)
        QtCore.QObject.connect(form.yMax,
                               QtCore.SIGNAL("editingFinished()"),
                               self.onScales)
        QtCore.QObject.connect(
            vPlot.getMdiArea(),
            QtCore.SIGNAL("subWindowActivated(QMdiSubWindow*)"),
            self.onMdiArea)
        return False

    def getMainWindow(self):
        """ Return the FreeCAD main window. """
        toplevel = QtGui.QApplication.topLevelWidgets()
        mwdf = None
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
        raise RuntimeError("No main window found")

    def widget(self, class_id, name):
        """Return the selected widget.

        Keyword arguments:
        class_id -- Class identifier
        name -- Name of the widget
        """
        mw = self.getMainWindow()
        form = mw.findChild(QtGui.QWidget, "TaskPanel")
        return form.findChild(class_id, name)

    def retranslateUi(self):
        """Set the user interface locale strings.
        """
        form = self.form
        form.setWindowTitle(QtGui.QApplication.translate(
            "plot_axes",
            u"Configure axes",
            None))

    # 坐标轴范围改变事件
    def onScales(self):
        """Executed when axes scales have been modified."""
        # Ensure that we can work
        plt = vPlot.getPlot()
        if not plt:
            self.updateUI()
            return
        # Get again all the subwidgets (to avoid PySide Pitfalls)
        mw = self.getMainWindow()
        form = mw.findChild(QtGui.QWidget, "TaskPanel")
        form.xMin = self.widget(QtGui.QLineEdit, "LineEdit_Xmin")
        form.xMax = self.widget(QtGui.QLineEdit, "LineEdit_Xmax")
        form.yMin = self.widget(QtGui.QLineEdit, "LineEdit_Ymin")
        form.yMax = self.widget(QtGui.QLineEdit, "LineEdit_Ymax")
        xMin = float(form.xMin.text())
        xMax = float(form.xMax.text())
        yMin = float(form.yMin.text())
        yMax = float(form.yMax.text())
        ax = plt.axleft
        ax.set_xlim((xMin, xMax))
        ax.set_ylim((yMin, yMax))
        plt.update()

    def onMdiArea(self, subWin):
        """Executed when window is selected on mdi area.

        Keyword arguments:
        subWin -- Selected window.
        """
        plt = vPlot.getPlot()
        if plt != subWin:
            self.updateUI()

    def updateUI(self):
        """Setup UI controls values if possible"""
        plt = vPlot.getPlot()
        # Get again all the subwidgets (to avoid PySide Pitfalls)
        mw = self.getMainWindow()
        form = mw.findChild(QtGui.QWidget, "TaskPanel")
        form.xMin = self.widget(QtGui.QLineEdit, "LineEdit_Xmin")
        form.xMax = self.widget(QtGui.QLineEdit, "LineEdit_Xmax")
        form.yMin = self.widget(QtGui.QLineEdit, "LineEdit_Ymin")
        form.yMax = self.widget(QtGui.QLineEdit, "LineEdit_Ymax")
        # Enable/disable them
        form.xMin.setEnabled(bool(plt))
        form.xMax.setEnabled(bool(plt))
        form.yMin.setEnabled(bool(plt))
        form.yMax.setEnabled(bool(plt))
        if not plt:
            return
        ax = plt.axleft
        limx = ax.get_xlim()
        form.xMin.setText(str(limx[0]))
        form.xMax.setText(str(limx[1]))
        limy = ax.get_ylim()
        form.yMin.setText(str(limy[0]))
        form.yMax.setText(str(limy[1]))


    # 去掉取消按钮
    def setCancelButtonInvisible(self):
        mw = self.getMainWindow()

        # 确认和取消所在box
        box = mw.findChild(QtGui.QDialogButtonBox)
        # 确认和取消按钮
        button = box.findChildren(QtGui.QPushButton)
        # 将取消按钮设置为不可见
        button[1].setVisible(False)

# 判断窗口名对应的图像窗口是否打开
def isExisted(mdi,winTitle):
    subWindowList = mdi.subWindowList()
    for subWindow in subWindowList:
        if subWindow.windowTitle() == winTitle:
            return subWindow
    return False

def createTask():
    panel = TaskPanel()
    plt = vPlot.getPlot()
    if plt:
        mdi = vPlot.getMdiArea()
        # 获取窗口名对应的子窗口是否打开
        subWindow = isExisted(mdi,plt.winTitle)

    Gui.Control.showDialog(panel)

    # 若存在该节点名称对应的子窗口，则激活该窗口
    if plt:
        if subWindow:
            mdi.setActiveSubWindow(subWindow)

    # 去掉取消按钮
    panel.setCancelButtonInvisible()

    if panel.setupUi():
        Gui.Control.closeDialog(panel)
        return None
    return panel

def sayz(msg):
    App.Console.PrintMessage(msg)
    App.Console.PrintMessage('\n')
