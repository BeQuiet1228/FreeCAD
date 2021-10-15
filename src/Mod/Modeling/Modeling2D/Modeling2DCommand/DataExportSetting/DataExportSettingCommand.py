# encoding:utf-8
import FreeCAD
import FreeCADGui
import DataExportSettingInstance
from Modeling.Modeling2D.Modeling2DCommand.DataExportSetting import DataExportSettingDlgMain
from Modeling.Modeling2D.Tools import Tools2D


class CreateDataExportSettingCommand:

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        if FreeCAD.activeDocument() is None:
            return
        obj = DataExportSettingInstance.getObject()
        # 在这里打开Ui
        Form = DataExportSettingDlgMain.ShowDialog(obj)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling2D/modeling2DResources/数据导出设定.svg"
        MenuText = Tools2D.QT_TRANSLATE_NOOP(
            'DataExportSetting',
            '数据导出设定')
        ToolTip = Tools2D.QT_TRANSLATE_NOOP(
            'DataExportSetting',
            'DataExportSetting')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreateDataExportSetting', CreateDataExportSettingCommand())


class ModeInfoSingleton(object):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if ModeInfoSingleton.__instance is None:
            obj = object.__new__(cls)
            ModeInfoSingleton.__instance = obj

        return ModeInfoSingleton.__instance
