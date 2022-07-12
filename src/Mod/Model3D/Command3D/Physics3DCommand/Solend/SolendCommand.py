# encoding:utf-8
import FreeCAD
import FreeCADGui
import SolendInstance
from Model3D.Tools import Tools3D
import SolendDialogMain

class CreateSolendCommand:
    """
    注册Solend命令
    """
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        if FreeCAD.activeDocument() == None:
            return
        obj = SolendInstance.getObject()
        # 在这里打开Ui
        Form = SolendDialogMain.ShowDialog(obj, True)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Model3D/Resources3D/Physics/sole.svg"
        MenuText = Tools3D.QT_TRANSLATE_NOOP(
            'CreateSolend',
            '螺旋线圈')
        ToolTip = Tools3D.QT_TRANSLATE_NOOP(
            'CreateSolend',
            'Solend')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreateSolend_3D', CreateSolendCommand())