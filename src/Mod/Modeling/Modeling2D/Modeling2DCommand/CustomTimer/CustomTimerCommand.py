# encoding:utf-8
import FreeCAD
import FreeCADGui
import CustomTimerInstance
from Modeling.Modeling2D.Modeling2DCommand.CustomTimer import CustomTimerDlgMain
from Modeling.Modeling2D.Tools import Tools2D


class CreateCustomTimerCommand:
    """
    注册CustomTimer命令
    """
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        if FreeCAD.activeDocument() is None:
            return
        obj = CustomTimerInstance.getObject()
        # 在这里打开Ui
        Form = CustomTimerDlgMain.ShowDialog(obj, True)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling2D/modeling2DResources/自定义定时器.svg"
        MenuText = Tools2D.QT_TRANSLATE_NOOP(
            'CreateCustomfTimer',
            '自定义定时器')
        ToolTip = Tools2D.QT_TRANSLATE_NOOP(
            'CreateCustomTimer',
            '自定义定时器')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreateCustomTimer', CreateCustomTimerCommand())



