# encoding:utf-8
import FreeCAD
import FreeCADGui
import NetStepSettingInstance
import NetStepSettingDialogMain
from Modeling.Modeling2D.Tools import Tools2D


class CreateNetStepSettingCommand:

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        if FreeCAD.activeDocument() == None:
            from Common import CommonCommand
            CommonCommand.NewDocument()
        obj = NetStepSettingInstance.getObject()

        # 在这里打开Ui
        Form = NetStepSettingDialogMain.ShowDialog(obj)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling2D/modeling2DResources/工作区间设置.svg"
        MenuText = Tools2D.QT_TRANSLATE_NOOP(
            'NetStepSetting',
            '工作区间设置')
        ToolTip = Tools2D.QT_TRANSLATE_NOOP(
            'NetStepSetting',
            'NetStepSetting')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreateNetStepSetting', CreateNetStepSettingCommand())


class ModeInfoSingleton(object):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if ModeInfoSingleton.__instance is None:
            obj = object.__new__(cls)
            ModeInfoSingleton.__instance = obj

        return ModeInfoSingleton.__instance
