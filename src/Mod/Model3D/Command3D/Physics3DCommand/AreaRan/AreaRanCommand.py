# encoding:utf-8
import FreeCAD
import FreeCADGui
import AreaRanInstance
from Model3D.Command3D.Physics3DCommand.AreaRan import AreaRanDialogMain
from Model3D.Tools import Tools3D


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
        Form = AreaRanDialogMain.ShowDialog(obj, True)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Model3D/Resources3D/Physics/ran.svg"
        MenuText = Tools3D.QT_TRANSLATE_NOOP(
            'CreateAreaRan',
            '空间图')
        ToolTip = Tools3D.QT_TRANSLATE_NOOP(
            'CreateAreaRan',
            '空间图')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreateAreaRan_3D', CreateAreaRanCommand())
