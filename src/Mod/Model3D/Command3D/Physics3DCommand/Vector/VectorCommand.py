# encoding:utf-8
import FreeCAD
import FreeCADGui
import VectorInstance
from Model3D.Command3D.Physics3DCommand.Vector import VectorDialogMain
from Model3D.Tools import Tools3D


class CreateVectorCommand:
    """
    注册Vector命令
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
        obj = VectorInstance.getObject()
        # 在这里打开Ui
        Form = VectorDialogMain.ShowDialog(obj, True)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Physics/PhysicsResources/vec.svg"
        MenuText = Tools3D.QT_TRANSLATE_NOOP(
            'CreateVector',
            '矢量图')
        ToolTip = Tools3D.QT_TRANSLATE_NOOP(
            'CreateVector',
            '矢量图')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreateVector_3D', CreateVectorCommand())
