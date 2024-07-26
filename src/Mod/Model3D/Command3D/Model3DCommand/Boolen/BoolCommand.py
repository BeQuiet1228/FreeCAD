# encoding:utf-8
import FreeCAD
import FreeCADGui
from Model3D.Tools import ObjectTools, UpdataBoolen3D, Tools3D
from PySide.QtGui import QApplication, QMessageBox,QCheckBox,QDialog,QVBoxLayout,QLabel,QDialogButtonBox


class CustomMessageBox(QDialog):
    def __init__(self, *args, **kwargs):
        super(CustomMessageBox, self).__init__(*args, **kwargs)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("错误")

        self.layout = QVBoxLayout()
        self.label = QLabel("布尔运算出错，你是否要重新进行布尔运算？")
        self.checkbox = QCheckBox("不再提示!")
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.checkbox)
        self.layout.addWidget(self.buttonBox)

        self.setLayout(self.layout)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def isChecked(self):
        return self.checkbox.isChecked()

class BooleanCommand:
    """
    布尔运算界面按钮
    """
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        # UpdataBoolen3D.UpdateBoolean.boolean(ObjectTools.getAllValidModelObj())
        UpdataBoolen3D.UpdateBoolean.boolean(UpdataBoolen3D.boolResultList())
        if  not FreeCAD.ActiveDocument.ResultShape.Shape.isValid():
            if not hasattr(FreeCAD.ActiveDocument.Param, 'B_test'):
                FreeCAD.ActiveDocument.Param.addProperty("App::PropertyBool", 'B_test')
                FreeCAD.ActiveDocument.Param.B_test = False
            else:
                if FreeCAD.ActiveDocument.Param.B_test:
                    return
            msgBox = CustomMessageBox()
            # msgBox.setText("布尔运算错误")  # 设置要显示的文本
            # msgBox.setInformativeText("布尔运算出错，你是否要重新进行布尔运算？")
            # msgBox.setWindowTitle("错误")  # 设置窗口标题
            # msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)  # 设置按钮

            # 显示消息框并获取用户的点击结果
            retval = msgBox.exec_()
            FreeCAD.ActiveDocument.Param.B_test = msgBox.isChecked()
            if retval == QDialog.Accepted:
                FreeCADGui.runCommand('UpdateBooleanCommand_3D')


    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling2D/modeling2DResources/布尔运算.svg"
        MenuText = Tools3D.QT_TRANSLATE_NOOP(
            'CreateBool',
            '布尔运算')
        ToolTip = Tools3D.QT_TRANSLATE_NOOP(
            'CreateBoolen',
            'Boolean')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('UpdateBooleanCommand_3D', BooleanCommand())



