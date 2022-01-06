# encoding:utf-8
import FreeCAD
import FreeCADGui
import ObjectArrayInstance
import ObjectArrayDialogMain
from Model3D.Tools import Tools3D,ObjectTools
from PySide import QtGui


class CreateObjectArrayCommand:
    """
    注册阵列体命令
    """
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        if FreeCAD.activeDocument() is None:
            return

        vol_list = ObjectTools.getAllVolumes()
        if len(vol_list) == 0:
            Tools3D.sayz(u"阵列体必须先定义一个基础体")
            QtGui.QMessageBox.information(None, "", "阵列体必须先定义一个基础体。")
            return

        obj = ObjectArrayInstance.getObject()
        # 在这里打开Ui
        Form = ObjectArrayDialogMain.ShowDialog(obj, True)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Model3D/Resources3D/Model/3D_Array.svg"
        MenuText = Tools3D.QT_TRANSLATE_NOOP(
            'CreateFoil',
            '阵列体')
        ToolTip = Tools3D.QT_TRANSLATE_NOOP(
            'CreateFoil',
            '阵列体')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreateObjectArray_3D', CreateObjectArrayCommand())
