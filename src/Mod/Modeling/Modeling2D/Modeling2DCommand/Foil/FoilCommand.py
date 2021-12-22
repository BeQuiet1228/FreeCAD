# encoding:utf-8
import FreeCAD
import FreeCADGui
import FoilInstance
from Modeling.Modeling2D.Tools import Tools2D
import FoilDialogMain


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
            from Common import CommonCommand
            CommonCommand.NewDocument()
        obj = FoilInstance.getObject()
        # 在这里打开Ui
        Form = FoilDialogMain.ShowDialog(obj, True)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Physics/PhysicsResources/foil.svg"
        MenuText = Tools2D.QT_TRANSLATE_NOOP(
            'CreateFoil',
            '箔片')
        ToolTip = Tools2D.QT_TRANSLATE_NOOP(
            'CreateFoil',
            'Foil')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreateFoil', CreateFoilCommand())


# # 通过名称来添加工程相关的object project@#$
# class Project:
#     def __init__(self):
#         if FreeCAD.ActiveDocument() is None:
#             return
#         pro_obj = FreeCAD.ActiveDocument.getObject("project@#$")
#         if pro_obj is None:
#             pass
#         else:
#             pass
#             # return pro_obj


