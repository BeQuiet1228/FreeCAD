# encoding:utf-8
import FreeCAD
import FreeCADGui

from Modeling.Modeling2D.Modeling2DCommand.View import GridDialog
from Modeling.Modeling2D.Tools import Tools2D
from PySide import QtGui
import Draft


class GridCommand:
    """
    注册Foil命令
    """
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        if FreeCAD.activeDocument() is None:
            return
        Form = ShowDialog()
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Physics/PhysicsResources/foil.svg"
        MenuText = Tools2D.QT_TRANSLATE_NOOP(
            'CreateFoil',
            'Create Foil')
        ToolTip = Tools2D.QT_TRANSLATE_NOOP(
            'CreateFoil',
            'Foil')
        return {'MenuText': "Grid",
                'ToolTip': ToolTip}

# FreeCADGui.addCommand('SetGrid', GridCommand())


class ShowDialog(QtGui.QDialog):
    def __init__(self,parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = None
        self.ui = GridDialog.Ui_Dialog()
        self.ui.setupUi(self)

        self.initDialog()
        self.ui.pb_OK.clicked.connect(self.slot_OK)

    def initDialog(self):
        curValue = Draft.getParam("gridSpacing")
        self.ui.gridSize.setValue(curValue * 1000)

    def slot_OK(self):
        self.close()
        self.setGridSize()

    def setGridSize(self):
        "sets the Draft grid to the given grid size"
        try:
            text = float(self.ui.gridSize.value())
            q = FreeCAD.Units.Quantity(str(text/1000))
        except:
            pass
        else:
            Draft.setParam("gridSpacing", q.Value)
            if hasattr(FreeCADGui, "Snapper"):
                FreeCADGui.Snapper.setGrid()

