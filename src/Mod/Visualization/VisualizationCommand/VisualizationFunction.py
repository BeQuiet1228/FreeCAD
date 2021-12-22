# -*- coding: UTF-8 -*-

import FreeCAD
import FreeCADGui
import VisualizationGui

from PySide import QtGui

IconCommonPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Visualization/VisualizationResources/"

def QT_TRANSLATE_NOOP(ctx,txt): return txt # dummy function for the QT translator
from DraftTools import translate
class Grid:
    def Activated(self):
        FreeCAD.Console.PrintMessage("Visualization_Grid\n")
        import vPlot
        plt = vPlot.getPlot()
        if not plt:
            msg = "The grid must be activated on top of a plot document"
            FreeCAD.Console.PrintError(msg + "\n")
            return
        flag = plt.isGrid()
        vPlot.grid(not flag)

    def GetResources(self):
        IconPath = IconCommonPath + "/Grid.svg"
        MenuText = QT_TRANSLATE_NOOP("Vis_Grid","Vis_Grid")
        ToolTip = "Grid"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


# x、y轴的标注支持数学公式，按照matplotlib的数学表达式书写规则输入
# https://matplotlib.org/users/mathtext.html
class Labels:
    def Activated(self):
        FreeCAD.Console.PrintMessage("Visualization_Labels\n")
        import VisualizationGui.plotLabels as plotLabels
        plotLabels.load()

        mainWindow = FreeCADGui.getMainWindow()
        dw = mainWindow.findChild(QtGui.QDockWidget, 'Combo View')
        if dw:
            qtab = dw.findChild(QtGui.QTabWidget, 'combiTab')
            qtab.setCurrentIndex(qtab.count() - 1)
    def GetResources(self):
        IconPath = IconCommonPath + "/Labels.svg"
        MenuText = QT_TRANSLATE_NOOP("Vis_Labels","Vis_Labels")
        ToolTip = "Set title and axes labels"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


class Series:
    def Activated(self):
        FreeCAD.Console.PrintMessage("Visualization_Series\n")
        import VisualizationGui.plotSeries as plotSeries
        plotSeries.load()

        mainWindow = FreeCADGui.getMainWindow()
        dw = mainWindow.findChild(QtGui.QDockWidget, 'Combo View')
        if dw:
            qtab = dw.findChild(QtGui.QTabWidget, 'combiTab')
            qtab.setCurrentIndex(qtab.count() - 1)
    def GetResources(self):
        IconPath = IconCommonPath + "/Series.svg"
        MenuText = QT_TRANSLATE_NOOP("Vis_Series","Vis_Series")
        ToolTip = "Configure series drawing style and label"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


class Point:
    def Activated(self):
        FreeCAD.Console.PrintMessage("Visualization_Point\n")
        import VisualizationGui.PlotAnnotation as PlotAnnotation
        PlotAnnotation.annotate()
    def GetResources(self):
        IconPath = IconCommonPath + "/Positions.svg"
        MenuText = QT_TRANSLATE_NOOP("Vis_Point","Vis_Point")
        ToolTip = "Mark point for figure"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

class Axes:
    def Activated(self):
        FreeCAD.Console.PrintMessage("Visualization_Axes\n")
        import VisualizationGui.plotAxes as plotAxes
        plotAxes.load()

        mainWindow = FreeCADGui.getMainWindow()
        dw = mainWindow.findChild(QtGui.QDockWidget, 'Combo View')
        if dw:
            qtab = dw.findChild(QtGui.QTabWidget, 'combiTab')
            qtab.setCurrentIndex(qtab.count() - 1)
    def GetResources(self):
        IconPath = IconCommonPath + "/Axes.svg"
        MenuText = QT_TRANSLATE_NOOP("Vis_Axes","Vis_Axes")
        ToolTip = "Configure the axes range"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

class Geometric_ratio:
    def Activated(self):
        FreeCAD.Console.PrintMessage("GeometricRatioSwitch\n")
        import VisualizationGui.PlotGeometricRatio as PlotGeometricRatio
        PlotGeometricRatio.show()
    def GetResources(self):
        IconPath = IconCommonPath + "/GeometricRatioSwitch.svg"
        MenuText = QT_TRANSLATE_NOOP("Vis_Geometric_Ratio","Vis_Geometric_Ratio")
        ToolTip = "GeometricRatioSwitch"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

class Struct_grid:
    def Activated(self):
        FreeCAD.Console.PrintMessage("Visualization_Axes\n")
        import VisualizationGui.PlotStructGrid as PlotStructGrid
        PlotStructGrid.show()
    def GetResources(self):
        IconPath = IconCommonPath + "/StructGrid.svg"
        MenuText = QT_TRANSLATE_NOOP("Vis_Struct_grid","Vis_Struct_grid")
        ToolTip = "Display Struct Grid"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

# class M3DEditorWorkbench:
#     def Activated(self):
#         FreeCADGui.activateWorkbench("M3DFileEditorWorkbench")
#         mainWindow = FreeCADGui.getMainWindow()
#         propertyView = mainWindow.findChild(QtGui.QDockWidget, "Property view")
#         propertyView.setVisible(False)
 
#     def GetResources(self):
#         IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/M3DFileEditor/M3DFileEditorResources/M3DFileEditorWorkbench.png"
#         MenuText = "M3D File Editor"
#         ToolTip = "To M3D File Editor Part"
#         return {'Pixmap': IconPath,
#                 'MenuText': MenuText,
#                 'ToolTip': ToolTip}

# class Modeling2DWorkbench:
#     def Activated(self):
#         FreeCADGui.activateWorkbench("Modeling2DWorkbench")

#         mainWindow = FreeCADGui.getMainWindow()
#         propertyView = mainWindow.findChild(QtGui.QDockWidget, "Property view")
#         propertyView.setVisible(True)

#     def GetResources(self):
#         IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling2D/modeling2DResources/2DModelingWorkbench.svg"
#         MenuText = "2D Modeling"
#         ToolTip = "To 2D Modeling Part"
#         return {'Pixmap': IconPath,
#                 'MenuText': MenuText,
#                 'ToolTip': ToolTip}


# class Modeling3DWorkbench:
#     def Activated(self):
#         FreeCADGui.activateWorkbench("Modeling3DWorkbench")
#         mainWindow = FreeCADGui.getMainWindow()
#         propertyView = mainWindow.findChild(QtGui.QDockWidget, "Property view")
#         propertyView.setVisible(True)

#     def GetResources(self):
#         IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling3D/modeling3DResources/3DModelingWorkbench.svg"
#         MenuText = "3D Modeling"
#         ToolTip = "To 3D Modeling Part"
#         return {'Pixmap': IconPath,
#                 'MenuText': MenuText,
#                 'ToolTip': ToolTip}


# class SimulationWorkbench:
#     def Activated(self):
#         FreeCADGui.activateWorkbench("PhysicsWorkbench")
#         mainWindow = FreeCADGui.getMainWindow()
#         propertyView = mainWindow.findChild(QtGui.QDockWidget, "Property view")
#         propertyView.setVisible(False)

#     def GetResources(self):
#         IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Physics/PhysicsResources/physics-workbench.svg"
#         MenuText = "Simulation"
#         ToolTip = "To Simulation Part"
#         return {'Pixmap': IconPath,
#                 'MenuText': MenuText,
#                 'ToolTip': ToolTip}


FreeCADGui.addCommand('Vis_Grid', Grid())
FreeCADGui.addCommand('Vis_Labels', Labels())
FreeCADGui.addCommand('Vis_Series', Series())
FreeCADGui.addCommand('Vis_Point', Point())
FreeCADGui.addCommand('Vis_Axes', Axes())
FreeCADGui.addCommand('Vis_Geometric_Ratio', Geometric_ratio())
FreeCADGui.addCommand('Vis_Struct_grid', Struct_grid())
# FreeCADGui.addCommand('M3D File Editor', M3DEditorWorkbench())
# FreeCADGui.addCommand('Modeling 2D', Modeling2DWorkbench())
# FreeCADGui.addCommand('Modeling 3D', Modeling3DWorkbench())
# FreeCADGui.addCommand('Simulation', SimulationWorkbench())
import SwitchWorkbench
