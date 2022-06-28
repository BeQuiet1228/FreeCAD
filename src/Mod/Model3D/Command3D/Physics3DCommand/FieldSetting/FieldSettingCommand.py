# encoding:utf-8
import FreeCAD
import FreeCADGui
import FieldSettingInstance
from Model3D.Tools import Tools3D
import FieldSettingDialogMain

class CreateFieldSettingCommand:
    """
    注册FieldSetting命令
    """
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        if FreeCAD.activeDocument() == None:
            return
        obj = FieldSettingInstance.getObject()
        # 在这里打开Ui
        Form = FieldSettingDialogMain.ShowDialog(obj)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Model3D/Resources3D/ProjectSetting/FiledSetting.svg"
        MenuText = Tools3D.QT_TRANSLATE_NOOP(
            'CreateFieldSetting',
            '场及函数定义')
        ToolTip = Tools3D.QT_TRANSLATE_NOOP(
            'CreateFieldSetting',
            'Absorption Space')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreateFieldSetting_3D', CreateFieldSettingCommand())