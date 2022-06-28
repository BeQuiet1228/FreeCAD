# encoding:utf-8
import FreeCAD
import FreeCADGui
import NewMaterialInstance
from Model3D.Tools import Tools3D
import NewMaterialDialogMain

class CreateNewMaterialCommand:
    """
    注册NewMaterial命令
    """
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        if FreeCAD.activeDocument() == None:
            return
        obj = NewMaterialInstance.getObject()
        # 在这里打开Ui
        Form = NewMaterialDialogMain.ShowDialog(obj, True)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Model3D/Resources3D/ProjectSetting/NewMaterical.svg"
        MenuText = Tools3D.QT_TRANSLATE_NOOP(
            'CreateNewMaterial',
            '新材料定义')
        ToolTip = Tools3D.QT_TRANSLATE_NOOP(
            'CreateNewMaterial',
            'Absorption Space')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreateNewMaterial_3D', CreateNewMaterialCommand())
