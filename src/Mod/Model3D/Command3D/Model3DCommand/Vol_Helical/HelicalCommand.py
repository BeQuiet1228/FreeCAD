# encoding:utf-8
import FreeCAD
import FreeCADGui
import HelicalInstance
import HelicalDialogMain
from Model3D.Tools import Tools3D


class CreateHelicalCommand:
    """
    注册螺旋体命令
    """
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        if FreeCAD.activeDocument() is None:
            return
        obj = HelicalInstance.getObject()
        # 在这里打开Ui
        Form = HelicalDialogMain.ShowDialog(obj, True)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Model3D/Resources3D/Model/3D_Vol_Helical.svg"
        MenuText = Tools3D.QT_TRANSLATE_NOOP(
            'CreateFoil',
            '螺旋体')
        ToolTip = Tools3D.QT_TRANSLATE_NOOP(
            'CreateFoil',
            '螺旋体')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreateVolHelical_3D', CreateHelicalCommand())


