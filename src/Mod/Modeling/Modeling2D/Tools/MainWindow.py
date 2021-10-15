# -*- coding: utf-8 -*-
import PySide


def getMainWindow():
    """ Return the FreeCAD main window. """
    toplevel = PySide.QtGui.QApplication.topLevelWidgets()
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
    return None