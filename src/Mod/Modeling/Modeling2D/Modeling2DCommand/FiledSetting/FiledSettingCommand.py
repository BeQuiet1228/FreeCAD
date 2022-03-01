# encoding:utf-8
import FreeCAD
import FreeCADGui
import FiledSettingInstance
import FiledSettingDialogMain
from Modeling.Modeling2D.Tools import Tools2D


class CreateFiledSettingCommand:

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        if FreeCAD.activeDocument() == None:
            from Common import CommonCommand
            CommonCommand.NewDocument()
        obj = FiledSettingInstance.getObject()

        # 在这里打开Ui
        Form = FiledSettingDialogMain.ShowDialog(obj, True)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling2D/modeling2DResources/场及函数定义.svg"
        MenuText = Tools2D.QT_TRANSLATE_NOOP(
            'FiledSetting',
            '场及函数定义')
        ToolTip = Tools2D.QT_TRANSLATE_NOOP(
            'FiledSetting',
            'FiledSetting')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreateFiledSetting', CreateFiledSettingCommand())


class ModeInfoSingleton(object):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if ModeInfoSingleton.__instance is None:
            obj = object.__new__(cls)
            ModeInfoSingleton.__instance = obj

        return ModeInfoSingleton.__instance
