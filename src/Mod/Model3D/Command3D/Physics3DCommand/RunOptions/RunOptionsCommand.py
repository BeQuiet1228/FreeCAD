# encoding:utf-8
import FreeCAD
import FreeCADGui
import RunOptionsInstance
from Model3D.Tools import Tools3D
import RunOptionsDialogMain

class CreateRunOptionsCommand:
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
        obj = RunOptionsInstance.getObject()
        # 在这里打开Ui
        Form = RunOptionsDialogMain.ShowDialog(obj, True)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Model3D/Resources3D/ProjectSetting/RunOptions.svg"
        MenuText = Tools3D.QT_TRANSLATE_NOOP(
            'RunOptions',
            '运行处理选项')
        ToolTip = Tools3D.QT_TRANSLATE_NOOP(
            'RunOptions',
            'make RunOptions')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreateRunOptions', CreateRunOptionsCommand())