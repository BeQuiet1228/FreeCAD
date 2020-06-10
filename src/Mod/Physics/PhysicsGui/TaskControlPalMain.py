# import Physics.PhysicsGui.TaskControlPal
# from PySide import QtGui,QtCore
#
# class TaskControlPalShow(QtGui.QDockWidget()):
#     def __init__(self, parent=None):
#         QtGui.QDockWidget().__init__(self, parent)
#         self.ui = Physics.PhysicsGui.TaskControlPal.Ui_DockWidget_TaskControl()
#         self.ui.setupUi(self)
#         app = QtGui.qApp
#         FCmw = app.activeWindow()
#         FCmw.addDockWidget(QtCore.Qt.LeftDockWidgetArea, QtGui.QDockWidget())