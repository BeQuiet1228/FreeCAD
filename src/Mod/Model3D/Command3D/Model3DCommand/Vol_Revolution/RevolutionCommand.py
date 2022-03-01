# encoding:utf-8
import FreeCAD
import FreeCADGui
import RevolutionInstance
import RevolutionDialogMain
from Model3D.Tools import Tools3D, ObjectTools
from PySide import QtGui


class CreateRevolutionCommand:
    """
    注册旋转体命令
    """
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        if FreeCAD.activeDocument() is None:
            return

        area_lst = ObjectTools.getAllAreas()
        if len(area_lst) == 0:
            Tools3D.sayz(u"旋转体必须先定义一个面")
            QtGui.QMessageBox.information(None, "", "旋转体必须先定义一个面。")
            return

        obj = RevolutionInstance.getObject()
        # 在这里打开Ui
        Form = RevolutionDialogMain.ShowDialog(obj, True)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Model3D/Resources3D/Model/3DRevolution"
        MenuText = Tools3D.QT_TRANSLATE_NOOP(
            'CreateFoil',
            '旋转体')
        ToolTip = Tools3D.QT_TRANSLATE_NOOP(
            'CreateFoil',
            '旋转体')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreateVolRevolution_3D', CreateRevolutionCommand())


