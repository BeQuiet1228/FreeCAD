# encoding:utf-8
import FreeCAD
import FreeCADGui
import CollectionOutputInstance
from Model3D.Tools import Tools3D
import CollectionOutputDialogMain

class CreateCollectionOutputCommand:
    """
    注册MacroParticle命令
    """
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        if FreeCAD.activeDocument() == None:
            return
        obj = CollectionOutputInstance.getObject()
        # 在这里打开Ui
        Form = CollectionOutputDialogMain.ShowDialog(obj, True)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Model3D/Resources3D/ProjectSetting/宏粒子合并.svg"
        MenuText = Tools3D.QT_TRANSLATE_NOOP(
            'CreateCollectionOutput',
            '收集体导出')
        ToolTip = Tools3D.QT_TRANSLATE_NOOP(
            'CreateCollectionOutput',
            'Absorption Space')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreateCollectionOutput_3D', CreateCollectionOutputCommand())