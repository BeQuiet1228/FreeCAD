# encoding:utf-8
import FreeCAD
import FreeCADGui
import ObserveInstance
from Model3D.Command3D.Physics3DCommand.Observe import ObserveDialogMain
from Model3D.Tools import Tools3D


class CreateObserveCommand:
    """
    注册Observe命令
    """
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        if FreeCAD.activeDocument() is None:
            from Common import CommonCommand
            CommonCommand.NewDocument()
            # return
        obj = ObserveInstance.getObject()
        # 在这里打开Ui
        Form = ObserveDialogMain.ShowDialog(obj, True)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Model3D/Resources3D/Physics/obs.svg"
        MenuText = Tools3D.QT_TRANSLATE_NOOP(
            'CreateObserve',
            '时间图')
        ToolTip = Tools3D.QT_TRANSLATE_NOOP(
            'CreateObserve',
            '时间图')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreateObserve_3D', CreateObserveCommand())
