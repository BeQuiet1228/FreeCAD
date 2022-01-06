# encoding:utf-8
import FreeCAD
import FreeCADGui
import NetStepSettingInstance
from Model3D.Command3D.Physics3DCommand.NetStepSetting import NetStepSettingDialogMain
from Model3D.Tools import Tools3D


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
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Model3D/Resources3D/ProjectSetting/WorkSpaceSettings.svg"
        MenuText = Tools3D.QT_TRANSLATE_NOOP(
            'NetStepSetting',
            '工作区间设置')
        ToolTip = Tools3D.QT_TRANSLATE_NOOP(
            'NetStepSetting',
            '工作区间设置')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('NetStepSetting_3D', CreateNetStepSettingCommand())
