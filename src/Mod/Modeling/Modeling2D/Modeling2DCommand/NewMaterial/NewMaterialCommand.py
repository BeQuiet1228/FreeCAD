# encoding:utf-8
import FreeCAD
import FreeCADGui
import NewMaterialInstance
from Modeling.Modeling2D.Modeling2DCommand.NewMaterial import NewMaterialDlgMain
from Modeling.Modeling2D.Tools import Tools2D


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
        if FreeCAD.activeDocument() is None:
            return
        obj = NewMaterialInstance.getObject()
        # 在这里打开Ui
        Form = NewMaterialDlgMain.ShowDialog(obj, True)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling2D/modeling2DResources/新材料定义.svg"
        MenuText = Tools2D.QT_TRANSLATE_NOOP(
            'CreateNewMaterial',
            '新材料定义')
        ToolTip = Tools2D.QT_TRANSLATE_NOOP(
            'CreateNewMaterial',
            '新型材料定义')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreateNewMaterial', CreateNewMaterialCommand())
