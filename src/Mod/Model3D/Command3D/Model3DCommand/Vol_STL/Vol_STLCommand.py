# encoding:utf-8
import FreeCAD
import FreeCADGui
import Vol_STLInstance
from Model3D.Tools import Tools3D
import Vol_STLDialogMain


class CreateVol_STLCommand:
    """
    注册Foil命令
    """
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        if FreeCAD.activeDocument() is None:
            return
        obj = Vol_STLInstance.getObject()
        # 在这里打开Ui
        Form = Vol_STLDialogMain.ShowDialog(obj, True)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Model3D/Resources3D/Model/3D_Point.svg"
        MenuText = Tools3D.QT_TRANSLATE_NOOP(
            'CreateFoil',
            '导入STL')
        ToolTip = Tools3D.QT_TRANSLATE_NOOP(
            'CreateFoil',
            '导入STL')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreateSTL_Vol', CreateVol_STLCommand())


