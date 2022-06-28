# encoding:utf-8
import FreeCAD
import FreeCADGui
import ArrayInstance
import ArrayDialogMain
from Model3D.Tools import Tools3D


class CreateAnnular_SectionCommand:
    """
    注册命令
    """
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        if FreeCAD.activeDocument() is None:
            return
        obj =ArrayInstance.getObject()
        # 在这里打开Ui
        Form = ArrayDialogMain.ShowDialog(obj, True)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Model3D/Resources3D/Model/3D_Vol_ParamArray.svg"
        MenuText = Tools3D.QT_TRANSLATE_NOOP(
            'CreateArray',
            '参数阵列体')
        ToolTip = Tools3D.QT_TRANSLATE_NOOP(
            'CreateArray',
            '参数阵列体')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreateVolArray', CreateAnnular_SectionCommand())