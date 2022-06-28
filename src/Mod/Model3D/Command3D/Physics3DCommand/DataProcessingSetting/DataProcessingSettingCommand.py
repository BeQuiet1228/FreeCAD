# encoding:utf-8
import FreeCAD
import FreeCADGui
import DataProcessingSettingInstance
from Model3D.Tools import Tools3D
import DataProcessingSettingDialogMain


class CreateDataProcessingSettingCommand:
    """
    注册FreeSpace命令
    """
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        if FreeCAD.activeDocument() == None:
            return
        obj = DataProcessingSettingInstance.getObject()
        # 在这里打开Ui
        Form = DataProcessingSettingDialogMain.ShowDialog(obj, True)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Model3D/Resources3D/ProjectSetting/DataProcessingSetting.svg"
        MenuText = Tools3D.QT_TRANSLATE_NOOP(
            'DataProcessingSetting',
            '数据导出设置')
        ToolTip = Tools3D.QT_TRANSLATE_NOOP(
            'DataProcessingSetting',
            'make DataProcessingSetting')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreateDataProcessingSetting', CreateDataProcessingSettingCommand())