# encoding:utf-8
import FreeCAD
import FreeCADGui
import ModelingInfoInstance
from Model3D.Tools import Tools3D
import ModelingInfoDialogMain

class CreateModelingInfoCommand:
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
        obj = ModelingInfoInstance.getObject()
        # 在这里打开Ui
        Form = ModelingInfoDialogMain.ShowDialog(obj, True)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Model3D/Resources3D/ProjectSetting/ModelingInfo.svg"
        MenuText = Tools3D.QT_TRANSLATE_NOOP(
            'ModelingInfo',
            '模型信息输入')
        ToolTip = Tools3D.QT_TRANSLATE_NOOP(
            'ModelingInfo',
            'make ModelingInfo')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreateModelingInfo', CreateModelingInfoCommand())