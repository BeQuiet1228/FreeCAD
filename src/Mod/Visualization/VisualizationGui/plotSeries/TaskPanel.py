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

import matplotlib
from matplotlib.lines import Line2D
import matplotlib.colors as Colors
import FreeCAD,FreeCADGui
from StyledComboBox import StyledComboBox

class TaskPanel:
    def __init__(self):
        path = App.ConfigGet("AppHomePath") + "Mod/Visualization/VisualizationGui"
        self.ui = path + "/plotSeries/TaskPanel.ui"
        self.skip = False
        self.item = 0
        self.plt = None

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

    def setupUi(self,graphType):
        mw = self.getMainWindow()

        form = mw.findChild(QtGui.QWidget, "TaskPanel")

        form.items = self.widget(QtGui.QListWidget, "items")
        form.label = self.widget(QtGui.QLineEdit, "label")
        form.isLabel = self.widget(QtGui.QCheckBox, "isLabel")
        form.style = self.widget(StyledComboBox, "lineStyle")
        form.marker = self.widget(StyledComboBox, "markers")
        form.width = self.widget(QtGui.QDoubleSpinBox, "lineWidth")
        form.size = self.widget(QtGui.QSpinBox, "markerSize")
        form.color = self.widget(QtGui.QPushButton, "color")
        form.remove = self.widget(QtGui.QPushButton, "remove")
        self.form = form
        self.retranslateUi()
        if graphType != 'phasepace':
            self.fillStyles()
        self.updateUI(graphType)
        QtCore.QObject.connect(
            form.items,
            QtCore.SIGNAL("currentRowChanged(int)"),
            self.onItem)
        QtCore.QObject.connect(
            form.label,
            QtCore.SIGNAL("editingFinished()"),
            self.onData)
        QtCore.QObject.connect(
            form.isLabel,
            QtCore.SIGNAL("stateChanged(int)"),
            self.onData)
        QtCore.QObject.connect(
            form.style,
            QtCore.SIGNAL("currentIndexChanged(int)"),
            self.onData)
        QtCore.QObject.connect(
            form.marker,
            QtCore.SIGNAL("currentIndexChanged(int)"),
            self.onData)
        QtCore.QObject.connect(
            form.width,
            QtCore.SIGNAL("valueChanged(double)"),
            self.onData)
        QtCore.QObject.connect(
            form.size,
            QtCore.SIGNAL("valueChanged(int)"),
            self.onData)
        QtCore.QObject.connect(
            form.color,
            QtCore.SIGNAL("pressed()"),
            self.onColor)
        QtCore.QObject.connect(
            form.remove,
            QtCore.SIGNAL("pressed()"),
            self.onRemove)
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
        """Set the user interface locale strings."""
        self.form.setWindowTitle(QtGui.QApplication.translate(
            "plot_series",
            "Configure series",
            None))
        self.widget(QtGui.QCheckBox, "isLabel").setText(
            QtGui.QApplication.translate(
                "plot_series",
                "No label",
                None))
        self.widget(QtGui.QPushButton, "remove").setText(
            QtGui.QApplication.translate(
                "plot_series",
                "Remove series",
                None))
        self.widget(QtGui.QLabel, "styleLabel").setText(
            QtGui.QApplication.translate(
                "plot_series",
                "Line style",
                None))
        self.widget(QtGui.QLabel, "markerLabel").setText(
            QtGui.QApplication.translate(
                "plot_series",
                "Marker",
                None))
        self.widget(QtGui.QListWidget, "items").setToolTip(
            QtGui.QApplication.translate(
                "plot_series",
                "List of available series",
                None))
        self.widget(QtGui.QLineEdit, "label").setToolTip(
            QtGui.QApplication.translate(
                "plot_series",
                "Line title",
                None))
        self.widget(QtGui.QCheckBox, "isLabel").setToolTip(
            QtGui.QApplication.translate(
                "plot_series",
                "If checked, series will not be considered for legend",
                None))
        self.widget(StyledComboBox, "lineStyle").setToolTip(
            QtGui.QApplication.translate(
                "plot_series",
                "Line style",
                None))
        self.widget(StyledComboBox, "markers").setToolTip(
            QtGui.QApplication.translate(
                "plot_series",
                "Marker style",
                None))
        self.widget(QtGui.QDoubleSpinBox, "lineWidth").setToolTip(
            QtGui.QApplication.translate(
                "plot_series",
                "Line width",
                None))
        self.widget(QtGui.QSpinBox, "markerSize").setToolTip(
            QtGui.QApplication.translate(
                "plot_series",
                "Marker size",
                None))
        self.widget(QtGui.QPushButton, "color").setToolTip(
            QtGui.QApplication.translate(
                "plot_series",
                "Line and marker color",
                None))
        self.widget(QtGui.QPushButton, "remove").setToolTip(
            QtGui.QApplication.translate(
                "plot_series",
                "Removes this series",
                None))

    def fillStyles(self):
        """Fill the style combo boxes with the available ones."""
        mw = self.getMainWindow()
        form = mw.findChild(QtGui.QWidget, "TaskPanel")
        form.style = self.widget(StyledComboBox, "lineStyle")
        form.marker = self.widget(StyledComboBox, "markers")
        # Line styles
        linestyles = Line2D.lineStyles.keys()
        for i in range(0, len(linestyles)):
            style = linestyles[i]
            string = "\'" + str(style) + "\'"
            string += " (" + Line2D.lineStyles[style] + ")"
            form.style.addItem(string)
        # Markers
        markers = Line2D.markers.keys()
        for i in range(0, len(markers)):
            marker = markers[i]
            string = "\'" + str(marker) + "\'"
            string += " (" + Line2D.markers[marker] + ")"
            form.marker.addItem(string)

    def onItem(self, row):
        """Executed when the selected item is modified."""
        if not self.skip:
            self.skip = True

            self.item = row

            self.updateUI()
            self.skip = False

    def onData(self):
        """Executed when the selected item data is modified."""
        if not self.skip:
            self.skip = True
            plt = vPlot.getPlot()
            if not plt:
                self.updateUI()
                return
            mw = self.getMainWindow()
            form = mw.findChild(QtGui.QWidget, "TaskPanel")
            form.label = self.widget(QtGui.QLineEdit, "label")
            form.isLabel = self.widget(QtGui.QCheckBox, "isLabel")
            form.style = self.widget(StyledComboBox, "lineStyle")
            form.marker = self.widget(StyledComboBox, "markers")
            form.width = self.widget(QtGui.QDoubleSpinBox, "lineWidth")
            form.size = self.widget(QtGui.QSpinBox, "markerSize")
            # Ensure that selected serie exist
            if self.item >= len(vPlot.series()):
                self.updateUI()
                return
            # Set label
            serie = vPlot.series()[self.item]
            if(form.isLabel.isChecked()):
                serie.name = None
                form.label.setEnabled(False)
            else:
                serie.name = form.label.text()
                form.label.setEnabled(True)
            # Set line style and marker
            style = form.style.currentIndex()
            linestyles = Line2D.lineStyles.keys()
            serie.line.set_linestyle(linestyles[style])
            marker = form.marker.currentIndex()
            markers = Line2D.markers.keys()
            serie.line.set_marker(markers[marker])
            # Set line width and marker size
            serie.line.set_linewidth(form.width.value())
            serie.line.set_markersize(form.size.value())
            plt.update()
            # Regenerate series labels
            self.setList()
            self.skip = False

    def onColor(self):
        """ Executed when color palette is requested. """
        plt = vPlot.getPlot()
        if not plt:
            self.updateUI()
            return
        mw = self.getMainWindow()
        form = mw.findChild(QtGui.QWidget, "TaskPanel")
        form.color = self.widget(QtGui.QPushButton, "color")

        # Ensure that selected serie exist
        if self.item >= len(vPlot.series()):
            self.updateUI()
            return
        # Show widget to select color
        col = QtGui.QColorDialog.getColor()
        # Send color to widget and serie
        if col.isValid():
            serie = plt.series[self.item]
            form.color.setStyleSheet(
                "background-color: rgb({}, {}, {});".format(col.red(),
                                                            col.green(),
                                                            col.blue()))
            serie.line.set_color((col.redF(), col.greenF(), col.blueF()))
            plt.update()

    def onRemove(self):
        """Executed when the data serie must be removed."""
        plt = vPlot.getPlot()
        if not plt:
            self.updateUI()
            return
        # Ensure that selected serie exist
        if self.item >= len(vPlot.series()):
            self.updateUI()
            return
        # Remove serie
        vPlot.removeSerie(self.item)
        self.setList()
        self.updateUI()
        plt.update()

    def onMdiArea(self, subWin):
        """Executed when a new window is selected on the mdi area.

        Keyword arguments:
        subWin -- Selected window.
        """
        plt = vPlot.getPlot()
        if plt != subWin:
            self.updateUI()

    def updateUI(self,graphType):
        """ Setup UI controls values if possible """
        mw = self.getMainWindow()
        form = mw.findChild(QtGui.QWidget, "TaskPanel")
        form.items = self.widget(QtGui.QListWidget, "items")
        form.label = self.widget(QtGui.QLineEdit, "label")
        form.isLabel = self.widget(QtGui.QCheckBox, "isLabel")
        form.style = self.widget(StyledComboBox, "lineStyle")
        form.marker = self.widget(StyledComboBox, "markers")
        form.width = self.widget(QtGui.QDoubleSpinBox, "lineWidth")
        form.size = self.widget(QtGui.QSpinBox, "markerSize")
        form.color = self.widget(QtGui.QPushButton, "color")
        form.remove = self.widget(QtGui.QPushButton, "remove")
        plt = vPlot.getPlot()
        form.items.setEnabled(bool(plt))
        form.label.setEnabled(bool(plt))
        form.isLabel.setEnabled(bool(plt))
        form.style.setEnabled(bool(plt))
        form.marker.setEnabled(bool(plt))
        form.width.setEnabled(bool(plt))
        form.size.setEnabled(bool(plt))
        form.color.setEnabled(bool(plt))
        form.remove.setEnabled(bool(plt))
        if not plt:
            self.plt = plt
            form.items.clear()
            return
        self.skip = True
        # Refill list
        if self.plt != plt or len(vPlot.series()) != form.items.count():
            self.plt = plt
            self.setList()
        # Ensure that have series
        if not len(vPlot.series()):
            form.label.setEnabled(False)
            form.isLabel.setEnabled(False)
            form.style.setEnabled(False)
            form.marker.setEnabled(False)
            form.width.setEnabled(False)
            form.size.setEnabled(False)
            form.color.setEnabled(False)
            form.remove.setEnabled(False)
            return
        # Set label
        serie = vPlot.series()[self.item]
        if serie.name is None:
            form.isLabel.setChecked(True)
            form.label.setEnabled(False)
            form.label.setText("")
        else:
            form.isLabel.setChecked(False)
            form.label.setText(serie.name)
        # Set line style and marker

        form.style.setCurrentIndex(0)
        linestyles = Line2D.lineStyles.keys()
        for i in range(0, len(linestyles)):
            style = linestyles[i]
            if style == serie.line.get_linestyle():
                form.style.setCurrentIndex(i)
        form.marker.setCurrentIndex(0)
        markers = Line2D.markers.keys()
        # phasepace图没有修改线形的功能
        if graphType != 'phasepace':
            for i in range(0, len(markers)):
                marker = markers[i]
                if marker == serie.line.get_marker():
                    form.marker.setCurrentIndex(i)
            # Set line width and marker size
            form.width.setValue(serie.line.get_linewidth())
            form.size.setValue(serie.line.get_markersize())
        # Set color
        # phaseoace图和别的图设置颜色的函数略不同
        if graphType == 'phasepace':
            #获得颜色数组
            facecolor = serie.line.get_facecolor()
            color = (facecolor[0][0],facecolor[0][1],facecolor[0][2])
            color = Colors.colorConverter.to_rgb(color)

        else:
            color = Colors.colorConverter.to_rgb(serie.line.get_color())
        form.color.setStyleSheet("background-color: rgb({}, {}, {});".format(
            int(color[0] * 255),
            int(color[1] * 255),
            int(color[2] * 255)))
        self.skip = False

    def setList(self):
        """Setup the UI control values if it is possible."""
        mw = self.getMainWindow()
        form = mw.findChild(QtGui.QWidget, "TaskPanel")
        form.items = self.widget(QtGui.QListWidget, "items")
        form.items.clear()
        series = vPlot.series()
        for i in range(0, len(series)):
            serie = series[i]
            string = 'serie ' + str(i) + ': '
            if serie.name is None:
                string = string + '\"No label\"'
            else:
                string = string + serie.name
            form.items.addItem(string)
        # Ensure that selected item is correct
        if len(series) and self.item >= len(series):
            self.item = len(series) - 1
            form.items.setCurrentIndex(self.item)

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

    series = vPlot.series()
    if len(series)>0:
        #只有rannge,observe,phasepace图可以使用这个功能
        if series[0].type == 'range' or series[0].type == 'observe' or series[0].type == 'phasepace':

            if panel.setupUi(series[0].type):
                Gui.Control.closeDialog(panel)
                return None
    return panel
def sayz(msg):
    FreeCAD.Console.PrintMessage(msg)
    FreeCAD.Console.PrintMessage('\n')