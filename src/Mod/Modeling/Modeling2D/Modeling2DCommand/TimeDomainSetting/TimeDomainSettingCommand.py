# encoding:utf-8
import FreeCAD
import FreeCADGui
import TimeDomainSettingInstance
from Modeling.Modeling2D.Modeling2DCommand.TimeDomainSetting import TimeDomainSettingDlgMain
from Modeling.Modeling2D.Tools import Tools2D


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
        Form = TimeDomainSettingDlgMain.ShowDialog(obj)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling2D/modeling2DResources/时域计算设置.svg"
        MenuText = Tools2D.QT_TRANSLATE_NOOP(
            'TimeDomainSetting',
            '时域计算设置')
        ToolTip = Tools2D.QT_TRANSLATE_NOOP(
            'TimeDomainSetting',
            'TimeDomainSetting')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreateTimeDomainSetting', CreateTimeDomainSettingCommand())
