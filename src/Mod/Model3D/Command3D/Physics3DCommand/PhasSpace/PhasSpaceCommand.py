# encoding:utf-8
import FreeCAD
import FreeCADGui
import PhasSpaceInstance
from Model3D.Command3D.Physics3DCommand.PhasSpace import PhasSpaceDialogMain
from Model3D.Tools import Tools3D


class CreatePhasSpaceCommand:
    """
    注册PhasSpace命令
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
        obj = PhasSpaceInstance.getObject()
        # 在这里打开Ui
        Form = PhasSpaceDialogMain.ShowDialog(obj, True)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Model3D/Resources3D/Physics/pha.svg"
        MenuText = Tools3D.QT_TRANSLATE_NOOP(
            'CreatePhasSpace',
            '相空间图')
        ToolTip = Tools3D.QT_TRANSLATE_NOOP(
            'CreatePhasSpace',
            '相空间图')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreatePhasSpace_3D', CreatePhasSpaceCommand())
