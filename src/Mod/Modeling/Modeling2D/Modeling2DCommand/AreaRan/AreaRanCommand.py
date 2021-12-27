# encoding:utf-8
import FreeCAD
import FreeCADGui
import AreaRanInstance
from Modeling.Modeling2D.Modeling2DCommand.AreaRan import AreaRanDlgMain
from Modeling.Modeling2D.Tools import Tools2D


class CreateAreaRanCommand:
    """
    注册AreaRan命令
    """
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        if FreeCAD.activeDocument() == None:
            from Common import CommonCommand
            CommonCommand.NewDocument()
        obj = AreaRanInstance.getObject()
        # 在这里打开Ui
        Form = AreaRanDlgMain.ShowDialog(obj, True)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling2D/modeling2DResources/空间观测.svg"
        MenuText = Tools2D.QT_TRANSLATE_NOOP(
            'CreateAreaRan',
            '空间图')
        ToolTip = Tools2D.QT_TRANSLATE_NOOP(
            'CreateAreaRan',
            'range(space)')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreateAreaRan', CreateAreaRanCommand())