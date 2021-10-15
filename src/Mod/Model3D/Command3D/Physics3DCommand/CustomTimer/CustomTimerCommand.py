# encoding:utf-8
import FreeCAD
import FreeCADGui
import CustomTimerInstance
from Model3D.Tools import Tools3D
import CustomTimerDialogMain

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
        if FreeCAD.activeDocument() == None:
            return
        obj = CustomTimerInstance.getObject()
        # 在这里打开Ui
        Form = CustomTimerDialogMain.ShowDialog(obj, True)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Model3D/Resources3D/Physics/timer.svg"
        MenuText = Tools3D.QT_TRANSLATE_NOOP(
            'CreateCustomTimer',
            '新建定时器')
        ToolTip = Tools3D.QT_TRANSLATE_NOOP(
            'CreateCustomTimer',
            'Absorption Space')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreateCustomTimer_3D', CreateCustomTimerCommand())