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
import vPlot

from PySide import QtGui, QtCore

def sayz(msg):
    App.Console.PrintMessage(msg)
    App.Console.PrintMessage('\n')

class TaskPanel:
    def __init__(self):
        path = App.ConfigGet("AppHomePath") + "Mod/Visualization/VisualizationGui"
        self.ui = path + "/plotLabels/TaskPanel.ui"
        self.skip = False
        # app = QtGui.qApp
        # aw = app.activeWindow()
        # # 获取Combo View
        # # Combo View->combiView->
        # if aw:
        #     dw = aw.findChild(QtGui.QDockWidget, 'Combo View')
        #     # 获取Combo View 下的comiTab
        #     if dw:
        #         qtab = dw.findChild(QtGui.QTabWidget, 'combiTab')
        #         tc = qtab.findChildren(QtGui.QScrollArea)
        #         # qt_tabwidget_stackedwidget
        #         for i in tc:
        #             sayz('i: '+i.objectName())
        #             if i:
        #                 q = i.findChildren(QtGui.QToolButton)
        #                 for j in q:
        #                     sayz(j.objectName())
        #                     j.setText('gg')
        #     else:
        #         print 'combiTab is not found'
        # else:
        #     print 'Combo View is not found'

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
        form.title = self.widget(QtGui.QLineEdit, "title")
        form.titleSize = self.widget(QtGui.QSpinBox, "titleSize")
        form.xLabel = self.widget(QtGui.QLineEdit, "titleX")
        form.xSize = self.widget(QtGui.QSpinBox, "xSize")
        form.yLabel = self.widget(QtGui.QLineEdit, "titleY")
        form.ySize = self.widget(QtGui.QSpinBox, "ySize")
        self.form = form
        self.retranslateUi()
        self.updateUI()
        QtCore.QObject.connect(form.title,
                               QtCore.SIGNAL("editingFinished()"),
                               self.onLabels)
        QtCore.QObject.connect(form.xLabel,
                               QtCore.SIGNAL("editingFinished()"),
                               self.onLabels)
        QtCore.QObject.connect(form.yLabel,
                               QtCore.SIGNAL("editingFinished()"),
                               self.onLabels)
        QtCore.QObject.connect(form.titleSize,
                               QtCore.SIGNAL("valueChanged(int)"),
                               self.onFontSizes)
        QtCore.QObject.connect(form.xSize,
                               QtCore.SIGNAL("valueChanged(int)"),
                               self.onFontSizes)
        QtCore.QObject.connect(form.ySize,
                               QtCore.SIGNAL("valueChanged(int)"),
                               self.onFontSizes)
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
        """ Set the user interface locale strings.
        """
        self.form.setWindowTitle(QtGui.QApplication.translate(
            "plot_labels",
            "Set labels",
            None))
        self.widget(QtGui.QLabel, "titleLabel").setText(
            QtGui.QApplication.translate("plot_labels",
                                         "Title",
                                         None))
        self.widget(QtGui.QLabel, "xLabel").setText(
            QtGui.QApplication.translate("plot_labels",
                                         "X label",
                                         None))
        self.widget(QtGui.QLabel, "yLabel").setText(
            QtGui.QApplication.translate("plot_labels",
                                         "Y label",
                                         None))
        self.widget(QtGui.QLineEdit, "title").setToolTip(
            QtGui.QApplication.translate(
                "plot_labels",
                "Title (associated to active axes)",
                None))
        self.widget(QtGui.QSpinBox, "titleSize").setToolTip(
            QtGui.QApplication.translate(
                "plot_labels",
                "Title font size",
                None))
        self.widget(QtGui.QLineEdit, "titleX").setToolTip(
            QtGui.QApplication.translate(
                "plot_labels",
                "X axis title",
                None))
        self.widget(QtGui.QSpinBox, "xSize").setToolTip(
            QtGui.QApplication.translate(
                "plot_labels",
                "X axis title font size",
                None))
        self.widget(QtGui.QLineEdit, "titleY").setToolTip(
            QtGui.QApplication.translate(
                "plot_labels",
                "Y axis title",
                None))
        self.widget(QtGui.QSpinBox, "ySize").setToolTip(
            QtGui.QApplication.translate(
                "plot_labels",
                "Y axis title font size",
                None))

    def onLabels(self):
        """ Executed when labels have been modified. """
        plt = vPlot.getPlot()
        if not plt:
            self.updateUI()
            return
        # Get again all the subwidgets (to avoid PySide Pitfalls)
        mw = self.getMainWindow()
        form = mw.findChild(QtGui.QWidget, "TaskPanel")
        form.title = self.widget(QtGui.QLineEdit, "title")
        form.xLabel = self.widget(QtGui.QLineEdit, "titleX")
        form.yLabel = self.widget(QtGui.QLineEdit, "titleY")

        vPlot.title(unicode(form.title.text()))
        vPlot.xlabel(unicode(form.xLabel.text()))
        vPlot.ylabel(unicode(form.yLabel.text()))
        plt.update()

    def onFontSizes(self, value):
        """ Executed when font sizes have been modified. """
        # Get apply environment
        plt = vPlot.getPlot()
        if not plt:
            self.updateUI()
            return
        # Get again all the subwidgets (to avoid PySide Pitfalls)
        mw = self.getMainWindow()
        form = mw.findChild(QtGui.QWidget, "TaskPanel")
        form.titleSize = self.widget(QtGui.QSpinBox, "titleSize")
        form.xSize = self.widget(QtGui.QSpinBox, "xSize")
        form.ySize = self.widget(QtGui.QSpinBox, "ySize")

        ax = plt.axleft
        ax.title.set_fontsize(form.titleSize.value())
        ax.xaxis.label.set_fontsize(form.xSize.value())
        ax.yaxis.label.set_fontsize(form.ySize.value())
        plt.update()

    def onMdiArea(self, subWin):
        """ Executed when window is selected on mdi area.

        Keyword arguments:
        subWin -- Selected window.
        """
        plt = vPlot.getPlot()
        if plt != subWin:
            self.updateUI()

    def updateUI(self):
        """ Setup UI controls values if possible """
        # Get again all the subwidgets (to avoid PySide Pitfalls)
        mw = self.getMainWindow()
        form = mw.findChild(QtGui.QWidget, "TaskPanel")
        form.title = self.widget(QtGui.QLineEdit, "title")
        form.titleSize = self.widget(QtGui.QSpinBox, "titleSize")
        form.xLabel = self.widget(QtGui.QLineEdit, "titleX")
        form.xSize = self.widget(QtGui.QSpinBox, "xSize")
        form.yLabel = self.widget(QtGui.QLineEdit, "titleY")
        form.ySize = self.widget(QtGui.QSpinBox, "ySize")

        plt = vPlot.getPlot()
        form.title.setEnabled(bool(plt))
        form.titleSize.setEnabled(bool(plt))
        form.xLabel.setEnabled(bool(plt))
        form.xSize.setEnabled(bool(plt))
        form.yLabel.setEnabled(bool(plt))
        form.ySize.setEnabled(bool(plt))
        if not plt:
            return

        ax = plt.axleft
        t = ax.get_title()
        x = ax.get_xlabel()
        y = ax.get_ylabel()
        tt = ax.title.get_fontsize()
        xx = ax.xaxis.label.get_fontsize()
        yy = ax.yaxis.label.get_fontsize()
        # Set labels
        form.title.setText(t)
        form.xLabel.setText(x)
        form.yLabel.setText(y)
        # Set font sizes
        form.titleSize.setValue(tt)
        form.xSize.setValue(xx)
        form.ySize.setValue(yy)

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
        subWindow = isExisted(mdi, plt.winTitle)

    Gui.Control.showDialog(panel)

    if plt:
        # 若存在该节点名称对应的子窗口，则激活该窗口
        if subWindow:
            mdi.setActiveSubWindow(subWindow)

    # 去掉取消按钮
    panel.setCancelButtonInvisible()

    if panel.setupUi():
        Gui.Control.closeDialog(panel)
        return None
    return panel
