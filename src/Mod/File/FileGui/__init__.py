
from PySide import QtCore, QtGui
import FileTextEditor
def Init():
    app = QtGui.qApp
    FCmw = app.activeWindow()  # the active qt window, = the freecad window since we are inside it
    # FCmw = FreeCADGui.getMainWindow() # use this line if the 'addDockWidget' error is declared
    myNewFreeCADWidget = QtGui.QDockWidget()  # create a new dckwidget
    myNewFreeCADWidget.ui = FileTextEditor.Ui_TextEditor()  # load the Ui script
    myNewFreeCADWidget.ui.setupUi(myNewFreeCADWidget)  # setup the ui
    FCmw.addDockWidget(QtCore.Qt.RightDockWidgetArea, myNewFreeCADWidget)  # add the widget to the main window