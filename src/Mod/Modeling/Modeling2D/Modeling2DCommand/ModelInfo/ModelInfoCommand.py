# encoding:utf-8
import FreeCAD
import FreeCADGui
import ModelInfoInstance
import ModelInfoDialogMain
from Modeling.Modeling2D.Tools import Tools2D


class CreateModelInfoCommand:

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        if FreeCAD.activeDocument() == None:
            from Common import CommonCommand
            CommonCommand.NewDocument()
        obj = ModelInfoInstance.getObject()

        # 在这里打开Ui
        Form = ModelInfoDialogMain.ShowDialog(obj)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling2D/modeling2DResources/模型信息输入.svg"
        MenuText = Tools2D.QT_TRANSLATE_NOOP(
            'ModelingInfo',
            '模型信息输入')
        ToolTip = Tools2D.QT_TRANSLATE_NOOP(
            'ModelingInfo',
            'ModelingInfo')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreateModelInfo', CreateModelInfoCommand())


class ModeInfoSingleton(object):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if ModeInfoSingleton.__instance is None:
            obj = object.__new__(cls)
            ModeInfoSingleton.__instance = obj

        return ModeInfoSingleton.__instance
