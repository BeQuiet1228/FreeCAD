# encoding:utf-8
import FreeCAD
import FreeCADGui
import DraftRevolutionInstance
import DraftRevolutionDialogMain
from Model3D.Tools import Tools3D, ObjectTools
from PySide import QtGui


class CreateDraftRevolutionCommand:
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        if FreeCAD.activeDocument() is None:
           return

        area_list = ObjectTools.getAllAreas()
        if len(area_list) == 0:
            Tools3D.sayz("草图旋转体必须先定义一个面")
            QtGui.QMessageBox.information(None, "", "草图旋转体必须先定义一个面。")
            return

        obj = DraftRevolutionInstance.getObject()
        # # 在这里打开Ui
        Form = DraftRevolutionDialogMain.ShowDialog(obj, True)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Model3D/Resources3D/Model/DraftRevolution.svg"
        MenuText = Tools3D.QT_TRANSLATE_NOOP(
            '草图挤出体',
            '草图旋转体')
        ToolTip = Tools3D.QT_TRANSLATE_NOOP(
            '创建挤出体',
            '创建一个挤出体')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreateDraftRevolution_3D', CreateDraftRevolutionCommand())