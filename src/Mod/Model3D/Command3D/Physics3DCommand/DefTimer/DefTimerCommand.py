# encoding:utf-8
import FreeCAD
import FreeCADGui
import DefTimerInstance
from Model3D.Command3D.Physics3DCommand.DefTimer import DefTimerDialogMain
from Model3D.Tools import Tools3D


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
        Form = DefTimerDialogMain.ShowDialog(obj, True)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Model3D/Resources3D/Physics/default-timer.svg"
        MenuText = Tools3D.QT_TRANSLATE_NOOP(
            'CreateDefTimer',
            '默认定时器')
        ToolTip = Tools3D.QT_TRANSLATE_NOOP(
            'CreateDefTimer',
            '默认定时器')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreateDefTimer_3D', CreateDefTimerCommand())
