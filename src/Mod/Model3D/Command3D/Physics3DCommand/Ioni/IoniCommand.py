# encoding:utf-8
import FreeCAD
import FreeCADGui
from Model3D.Tools import Tools3D
import IoniInstance
import IoniDialogMain

class CreateIoniCommand:
    """
    注册气体电离命令
    """
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        if FreeCAD.activeDocument() is None:
            return
        obj = IoniInstance.getObject()
        # 在这里打开Ui
        Form = IoniDialogMain.ShowDialog(obj, True)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Model3D/Resources3D/Physics/ioni.svg"
        MenuText = Tools3D.QT_TRANSLATE_NOOP(
            'Ioni',
            '气体电离')
        ToolTip = Tools3D.QT_TRANSLATE_NOOP(
            'Ioni',
            '气体电离')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreateIoni_3D', CreateIoniCommand())
