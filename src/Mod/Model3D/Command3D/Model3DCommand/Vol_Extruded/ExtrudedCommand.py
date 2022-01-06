# encoding:utf-8
import FreeCAD
import FreeCADGui
import ExtrudedInstance
import ExtrudedDialogMain
from Model3D.Tools import Tools3D, ObjectTools
from PySide import QtGui


class CreateExtrudedCommand:
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        if FreeCAD.activeDocument() is None:
           return

        area_lst = ObjectTools.getAllAreas()
        Line_list = ObjectTools.getAllLines()
        if len(area_lst) == 0 or len(Line_list) == 0:
            QtGui.QMessageBox.information(None, "", "挤出体必须先定义一个线和一个面。")
            Tools3D.sayz(u"挤出体必须先定义一个线和一个面")
            return

        obj = ExtrudedInstance.getObject()
        # # 在这里打开Ui 挤出体无UI界面
        Form = ExtrudedDialogMain.ShowDialog(obj, True)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Model3D/Resources3D/Model/3D_Vol_Extruded.svg"
        MenuText = Tools3D.QT_TRANSLATE_NOOP(
            '挤出体',
            '挤出体')
        ToolTip = Tools3D.QT_TRANSLATE_NOOP(
            '挤出体',
            '挤出体')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('Create3DExtruded', CreateExtrudedCommand())
