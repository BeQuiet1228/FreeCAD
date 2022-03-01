# encoding:utf-8
import FreeCAD
import FreeCADGui
import TimeDomainSettingInstance
from Model3D.Command3D.Physics3DCommand.TimeDomainSetting import TimeDomainSettingDialogMain
from Model3D.Tools import Tools3D


class CreateTimeDomainSettingCommand:

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        if FreeCAD.activeDocument() is None:
            return
        obj = TimeDomainSettingInstance.getObject()
        # 在这里打开Ui
        Form = TimeDomainSettingDialogMain.ShowDialog(obj)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Model3D/Resources3D/ProjectSetting/TimeDomainComputingMenu.svg"
        MenuText = Tools3D.QT_TRANSLATE_NOOP(
            'TimeDomainSetting',
            '时域计算设置')
        ToolTip = Tools3D.QT_TRANSLATE_NOOP(
            'TimeDomainSetting',
            '时域计算设置')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('TimeDomainSetting_3D', CreateTimeDomainSettingCommand())
