# encoding:utf-8
import FreeCAD
import FreeCADGui
import DraftExtrudedInstance
import DraftExtrudedDialogMain
from Model3D.Tools import Tools3D, ObjectTools
from PySide import QtGui


class CreateExtDraftrudedCommand:
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        if FreeCAD.activeDocument() is None:
           return
        conformal_area = ObjectTools.getLabelsByType(ObjectTools.ObjectType.Area_Conformal)
        rectangular_area = ObjectTools.getLabelsByType(ObjectTools.ObjectType.Area_Rectangular)
        AreaList = conformal_area + rectangular_area
        if len(AreaList) == 0:
            Tools3D.sayz(u"草图拉伸体必须先定义一个投影面")
            QtGui.QMessageBox.information(None, "", "草图拉伸体必须先定义一个投影面。")
            return
        obj = DraftExtrudedInstance.getObject()
        # 在这里打开Ui
        Form = DraftExtrudedDialogMain.ShowDialog(obj, True)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Model3D/Resources3D/Model/DraftExtrusion.svg"
        MenuText = Tools3D.QT_TRANSLATE_NOOP(
            '草图挤出体',
            '投影挤出体')
        ToolTip = Tools3D.QT_TRANSLATE_NOOP(
            '创建挤出体',
            '创建一个挤出体')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreateDraftExtruded_3D', CreateExtDraftrudedCommand())