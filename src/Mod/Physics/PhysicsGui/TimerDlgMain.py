import Physics.PhysicsGui.DefaultTimerDlg
import sys
from PySide.QtGui import QMainWindow,QApplication
from PySide.QtCore import Qt
from PySide import QtGui

class TimerShow(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = Physics.PhysicsGui.TimerDlg.Ui_TimerDlg()
        self.ui.setupUi(self)

def show():
    dft = TimerShow()
    dft.show()
    dft.exec_()

