# encoding:utf-8
import FreeCAD
import FreeCADGui
import FoilInstance
import FoilDialogMain
from Model3D.Tools import Tools3D

class CreateFoilCommand:
    """
    注册Foil命令
    """
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        if FreeCAD.activeDocument() == None:
            return
        obj = FoilInstance.getObject()
        # 在这里打开Ui
        Form = FoilDialogMain.ShowDialog(obj, True)
        Form.show()
        Form.exec_()


    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Model3D/Resources3D/Physics/foil.svg"
        MenuText = Tools3D.QT_TRANSLATE_NOOP(
            'CreateFoil',
            '箔片')
        ToolTip = Tools3D.QT_TRANSLATE_NOOP(
            'CreateFoil',
            'Foil')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('Create_3D_Foil', CreateFoilCommand())