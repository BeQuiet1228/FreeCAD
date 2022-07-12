# encoding:utf-8
import FreeCAD
import FreeCADGui
import RunProcessingOptionsInstance
from Modeling.Modeling2D.Modeling2DCommand.RunProcessingOptions import RunProcessingOptionsDlgMain
from Modeling.Modeling2D.Tools import Tools2D


class CreateRunProcessingOptionsCommand:

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        if FreeCAD.activeDocument() is None:
            return
        obj = RunProcessingOptionsInstance.getObject()

        # 在这里打开Ui
        Form = RunProcessingOptionsDlgMain.ShowDialog(obj)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling2D/modeling2DResources/运行处理选项.svg"
        MenuText = Tools2D.QT_TRANSLATE_NOOP(
            'RunProcessingOptions',
            '运行处理选项')
        ToolTip = Tools2D.QT_TRANSLATE_NOOP(
            'RunProcessingOptions',
            'RunProcessingOptions')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreateRunProcessingOptions', CreateRunProcessingOptionsCommand())


