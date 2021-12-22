# encoding:utf-8
import FreeCAD
import FreeCADGui
import DefTimerInstance
from Modeling.Modeling2D.Modeling2DCommand.DefTimer import DefTimerDlgMain
from Modeling.Modeling2D.Tools import Tools2D


class CreateDefTimerCommand:
    """
    注册DefTimer命令
    """
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        if FreeCAD.activeDocument() is None:
            return
        obj = DefTimerInstance.getObject()
        # 在这里打开Ui
        Form = DefTimerDlgMain.ShowDialog(obj)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling2D/modeling2DResources/默认定时器.svg"
        MenuText = Tools2D.QT_TRANSLATE_NOOP(
            'CreateDefTimer',
            '默认定时器')
        ToolTip = Tools2D.QT_TRANSLATE_NOOP(
            'CreateDefTimer',
            '默认定时器')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreateDefTimer', CreateDefTimerCommand())



