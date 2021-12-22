# encoding:utf-8
import FreeCAD
import FreeCADGui
import ObserveInstance
from Modeling.Modeling2D.Modeling2DCommand.Observe import ObserveDlgMain
from Modeling.Modeling2D.Tools import Tools2D


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
        Form = ObserveDlgMain.ShowDialog(obj, True)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Physics/PhysicsResources/obs.svg"
        MenuText = Tools2D.QT_TRANSLATE_NOOP(
            'CreateObserve',
            '时间图')
        ToolTip = Tools2D.QT_TRANSLATE_NOOP(
            'CreateObsever',
            'Observe(time)')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreateObserve', CreateObserveCommand())