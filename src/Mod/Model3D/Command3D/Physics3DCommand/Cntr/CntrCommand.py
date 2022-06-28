# encoding:utf-8
import FreeCAD
import FreeCADGui
import CntrInstance
from Model3D.Command3D.Physics3DCommand.Cntr import CntrDialogMain
from Model3D.Tools import Tools3D


class CreateCntrCommand:
    """
    注册Cntr命令
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
        obj = CntrInstance.getObject()
        # 在这里打开Ui
        Form = CntrDialogMain.ShowDialog(obj, True)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Model3D/Resources3D/Physics/cntr.svg"
        MenuText = Tools3D.QT_TRANSLATE_NOOP(
            'CreateCntr',
            '等位图')
        ToolTip = Tools3D.QT_TRANSLATE_NOOP(
            'CreateCntr',
            '等位图')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreateCntr_3D', CreateCntrCommand())
