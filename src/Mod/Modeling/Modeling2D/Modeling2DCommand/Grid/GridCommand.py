# encoding:utf-8
import FreeCAD
import FreeCADGui
import PySide
from PySide import QtGui
from Modeling.Modeling2D.Modeling2DCommand.Grid import GridDialog, GridInstance
from Modeling.Modeling2D.Tools import Tools2D


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
        obj = GridInstance.getObject()
        Form = ShowDialog(obj)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling2D/modeling2DResources/网格.svg"
        MenuText = Tools2D.QT_TRANSLATE_NOOP(
            'CreateGrid',
            '背景设置')
        ToolTip = Tools2D.QT_TRANSLATE_NOOP(
            'CreateGrid',
            'Grid')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('SetGrid', GridCommand())


class ShowDialog(QtGui.QDialog):
    def __init__(self, obj, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = None
        self.ui = GridDialog.Ui_Dialog()
        self.ui.setupUi(self)
        self.grid = None
        self.obj = obj
        self.setModal(True)

        complementaryAttributes(obj)
        self.initDialog()

    def initDialog(self):
        self.getGridInstance()
        self.getInfoFromObj()
        # 链接信号与槽
        self.ui.p1_x.valueChanged.connect(self.slotSpinBox)
        self.ui.p1_y.valueChanged.connect(self.slotSpinBox)
        self.ui.gridNum.valueChanged.connect(self.slotSpinBox)
        self.ui.gridSizeX.valueChanged.connect(self.slotSpinBox)
        self.ui.gridSizeY.valueChanged.connect(self.slotSpinBox)
        self.ui.pb_OK.clicked.connect(self.slotOK)
        self.ui.pb_cancel.clicked.connect(self.slotCancel)

    def slotOK(self):
        
        Tools2D.sayz('slotOK')
        self.close()
        self.setInfoToGrid()
        self.setInfoToObj()

    def slotCancel(self):
        self.close()

    def getGridInstance(self):
        """
        获取grid对象，可能获取空，为了避免获取到空的对象或者上一个工程的对象，在这里手动创建一次Grid的对象
        注意该对象与当前的Grid对象为同一个对象
        :return: gridIns or None
        """
        if FreeCAD.activeDocument() is None:
            return
        # 通过FreeCADGui的命令创建网格，之后获取的grid对象与当前工程对象为同一个对象
        FreeCADGui.Snapper.show()
        # 获取对象
        self.grid = FreeCADGui.Snapper.grid

    def setInfoToGrid(self):
        Tools2D.sayz('setInfoToGrid')
        # 目前的网格只能画正方形的区域
        p1_x = self.ui.p1_x.value()
        p1_y = self.ui.p1_y.value()
        gridNum = self.ui.gridNum.value()
        gridSizeX = self.ui.gridSizeX.value()
        gridSizeY = self.ui.gridSizeY.value()
        FreeCADGui.ActiveDocument.ActiveView.setGridSpace(gridSizeX,gridSizeY)
        space = (gridSizeX if gridSizeX < gridSizeY else gridSizeY)
        # 设置线的数量，该方法由DraftTrackers提供
        self.grid.setSize(gridNum)
        # 设置网格的大小
        self.grid.setSpacing(space * 0.001)
        # 计算出移动的距离不转换为 m 量级的数据
        # length and width
        lw = gridNum * space
        move_x = (p1_x + lw * 0.5) * 0.001
        move_y = (p1_y + lw * 0.5) * 0.001
        Tools2D.sayz(str(move_x) + "  " + str(move_y))
        # 位移网格
        self.grid.trans.translation.setValue([move_x, move_y, 0])

        if not self.ui.isShow.isChecked():
            self.grid.off()
            self.obj.isShow = False
            Tools2D.sayz("隐藏网格")
        else:
            self.obj.isShow = True

    def getInfoFromObj(self):
        self.ui.p1_x.setValue(self.obj.p1_x)
        self.ui.p1_y.setValue(self.obj.p1_y)
        self.ui.gridNum.setValue(self.obj.gridNum)
        self.ui.gridSizeX.setValue(self.obj.gridSizeX)
        self.ui.gridSizeY.setValue(self.obj.gridSizeY)

        self.ui.p2_x.setEnabled(False)
        self.ui.p2_y.setEnabled(False)

        self.slotSpinBox()

        self.ui.isShow.setChecked(self.obj.isShow)

    def setInfoToObj(self):
        self.obj.p1_x = self.ui.p1_x.value()
        self.obj.p1_y = self.ui.p1_y.value()
        self.obj.gridNum = self.ui.gridNum.value()
        self.obj.gridSizeX = self.ui.gridSizeX.value()
        self.obj.gridSizeY = self.ui.gridSizeY.value()

    def slotSpinBox(self):
        """
        p2的坐标信息是由其他几个选项决定的
        :return: None
        """
        p1_x = self.ui.p1_x.value()
        p1_y = self.ui.p1_y.value()
        gridNum = self.ui.gridNum.value()
        gridSizeX = self.ui.gridSizeX.value()
        gridSizeY = self.ui.gridSizeY.value()
        # length and width
        lwx = gridNum * gridSizeX
        lwy = gridNum * gridSizeY
        self.ui.p2_x.setValue(p1_x + lwx)
        self.ui.p2_y.setValue(p1_y + lwy)


def complementaryAttributes(obj):
    if not hasattr(obj, "gridSizeX"):
        obj.addProperty("App::PropertyInteger", "gridSizeX").gridSizeX = 10
    if not hasattr(obj, "gridSizeY"):
        obj.addProperty("App::PropertyInteger", "gridSizeY").gridSizeY = 10
    if not hasattr(obj, "isShow"):
        obj.addProperty("App::PropertyBool", "isShow").isShow = True


def showGrid():
    if FreeCAD.activeDocument() is None:
        return
    obj = GridInstance.getObject()
    if not obj.isShow:
        return
    FreeCADGui.Snapper.show()
    grid = FreeCADGui.Snapper.grid

    complementaryAttributes(obj)

    p1_x = obj.p1_x
    p1_y = obj.p1_y
    gridNum = obj.gridNum
    gridSizeX = obj.gridSizeX
    gridSizeY = obj.gridSizeY
    FreeCADGui.ActiveDocument.ActiveView.setGridSpace(gridSizeX, gridSizeY)
    space = (gridSizeX if gridSizeX < gridSizeY else gridSizeY)
    # length and width
    lw = gridNum * space
    # 设置线的数量，该方法由DraftTrackers提供
    grid.setSize(gridNum)
    # 设置网格的大小
    grid.setSpacing(space * 0.001)
    # 计算出移动的距离不转换为 m 量级的数据
    move_x = (p1_x + lw * 0.5) * 0.001
    move_y = (p1_y + lw * 0.5) * 0.001
    # Tools2D.sayz(str(move_x) + "  " + str(move_y) + "lw:  " + str(lw))
    # 位移网格
    grid.trans.translation.setValue([move_x, move_y, 0])
    Tools2D.sayz("显示网格")





