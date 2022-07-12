# encoding:utf-8
import FreeCAD
import FreeCADGui
import LineObliqueInstance
from Model3D.Tools import Tools3D
import LineObliqueDialogMain


class CreateLineObliqueCommand:
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
        obj = LineObliqueInstance.getObject()
        # 在这里打开Ui
        Form = LineObliqueDialogMain.ShowDialog(obj, True)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Model3D/Resources3D/Model/3D_LineOblique.svg"
        MenuText = Tools3D.QT_TRANSLATE_NOOP(
            'CreateFoil',
            '斜线')
        ToolTip = Tools3D.QT_TRANSLATE_NOOP(
            'CreateFoil',
            '斜线')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreateLineOblique_3D', CreateLineObliqueCommand())


