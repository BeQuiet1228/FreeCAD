# -*- coding: UTF-8 -*-

import FreeCAD
import FreeCADGui
from PySide import QtGui

class M3DEditorWorkbench:
    def Activated(self):
        FreeCADGui.activateWorkbench("M3DFileEditorWorkbench")
        mainWindow = FreeCADGui.getMainWindow()
        propertyView = mainWindow.findChild(QtGui.QDockWidget, "Property view")
        propertyView.setVisible(False)

        mdiArea = mainWindow.findChild(QtGui.QMdiArea)
        subWindowList = mdiArea.subWindowList()
        for w in subWindowList:
            if w.widget().statusTip() == "MyM3DFileEditor":
                mdiArea.setActiveSubWindow(w)
 
    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/M3DFileEditor/M3DFileEditorResources/M3DFileEditorWorkbench.svg"
        MenuText = "M3D File Editor"
        ToolTip = "To M3D File Editor Part"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


class Modeling2DWorkbench:
    def Activated(self):
        FreeCADGui.activateWorkbench("Modeling2DWorkbench")
        mainWindow = FreeCADGui.getMainWindow()
        propertyView = mainWindow.findChild(QtGui.QDockWidget, "Property view")
        propertyView.setVisible(True)

        mdiArea = mainWindow.findChild(QtGui.QMdiArea)
        subWindowList = mdiArea.subWindowList()
        for w in subWindowList:
            if w.widget().statusTip() == "3DView":
                mdiArea.setActiveSubWindow(w)

        dw = mainWindow.findChild(QtGui.QDockWidget, 'Combo View')
        if dw:
            dw.setVisible(True)
            qtab = dw.findChild(QtGui.QTabWidget, 'combiTab')
            tabCount = qtab.count()
            for i in range(tabCount):
                if qtab.tabText(i) == "模型" or qtab.tabText(i) == "Model":
                    qtab.setCurrentIndex(i)

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling2D/modeling2DResources/2DModelingWorkbench.svg"
        MenuText = "2D Modeling"
        ToolTip = "To 2D Modeling Part"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


class Modeling3DWorkbench:
    def Activated(self):
        FreeCADGui.activateWorkbench("Modeling3DWorkbench")
        mainWindow = FreeCADGui.getMainWindow()
        propertyView = mainWindow.findChild(QtGui.QDockWidget, "Property view")
        propertyView.setVisible(True)

        mdiArea = mainWindow.findChild(QtGui.QMdiArea)
        subWindowList = mdiArea.subWindowList()
        for w in subWindowList:
            if w.widget().statusTip() == "3DView":
                mdiArea.setActiveSubWindow(w)

        dw = mainWindow.findChild(QtGui.QDockWidget, 'Combo View')
        if dw:
            dw.setVisible(True)
            qtab = dw.findChild(QtGui.QTabWidget, 'combiTab')
            tabCount = qtab.count()
            for i in range(tabCount):
                if qtab.tabText(i) == "模型" or qtab.tabText(i) == "Model":
                    qtab.setCurrentIndex(i)

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling3D/modeling3DResources/3DModelingWorkbench.svg"
        MenuText = "3D Modeling"
        ToolTip = "To 3D Modeling Part"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


class SimulationWorkbench:
    def Activated(self):
        FreeCADGui.activateWorkbench("PhysicsWorkbench")
        mainWindow = FreeCADGui.getMainWindow()
        propertyView = mainWindow.findChild(QtGui.QDockWidget, "Property view")
        propertyView.setVisible(False)

        dw = mainWindow.findChild(QtGui.QDockWidget, 'Combo View')
        if dw:
            dw.setVisible(True)
            qtab = dw.findChild(QtGui.QTabWidget, 'combiTab')
            tabCount = qtab.count()
            for i in range(tabCount):
                if qtab.tabText(i) == "运行结果":
                    qtab.setCurrentIndex(i)


    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Physics/PhysicsResources/physics-workbench.svg"
        MenuText = "Simulation"
        ToolTip = "To Simulation Part"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


class PostProcessingWorkbench:
    def Activated(self):
        FreeCADGui.activateWorkbench("VisualWorkbench")
        mainWindow = FreeCADGui.getMainWindow()
        propertyView = mainWindow.findChild(QtGui.QDockWidget, "Property view")
        propertyView.setVisible(False)

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Visualization/visualizationResources/VisualWorkbench.svg"
        MenuText = "Post Processing"
        ToolTip = "To Post Processing Part"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('M3D File Editor', M3DEditorWorkbench())
FreeCADGui.addCommand('Modeling 2D', Modeling2DWorkbench())
FreeCADGui.addCommand('Modeling 3D', Modeling3DWorkbench())
FreeCADGui.addCommand('Simulation', SimulationWorkbench())
FreeCADGui.addCommand('Post Processing', PostProcessingWorkbench())
