# Volume
#### @Author:xqy
#### @Date:2021.5.20

[Volume结构](#Volume结构)

[新建Volume体模型](#新建Volume体模型)


## 新建Volume体模型
一般的，当新定义一个体模型时，其代码结构主要分为Command, Dialog, DialogMain, Instance四部分
###Command:
Command负责激活Volume，从Instance获取object，并从DialogMain中获取ui
``` python
class CreateXXXCommand:
    """
    注册Volume命令
    """
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        # 激活
        if FreeCAD.activeDocument() is None:
            return
        obj = XXXInstance.getObject()
        # 在这里打开Ui
        Form = XXXDialogMain.ShowDialog(obj, True)
        Form.show()
        Form.exec_()

    def GetResources(self):
        # 获取体模型对应的视图信息
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Model3D/Resources3D/Model/XXX.svg"
        MenuText = Tools3D.QT_TRANSLATE_NOOP(
            'CreateXXX',
            'xx体')
        ToolTip = Tools3D.QT_TRANSLATE_NOOP(
            'CreateXXX',
            'xx体')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

# 添加命令
FreeCADGui.addCommand('CreateXXX', CreateXXXCommand())

```
###Dialog:
即填入模型数据的ui界面逻辑。对于体而言，一般来说首先继承父类BaseUI的ui界面，完成模型的Label、Order、Attribute和Uniform Grid属性。

![BaseUI](https://z3.ax1x.com/2021/05/21/gHMFRP.png)

对于每一种体，在BaseUI的Object网格布局中，添加点属性和其他个性化属性。

以球体为例，它包含有一个点属性和一个Radius半径属性：

![SphericalUI](https://z3.ax1x.com/2021/05/24/gjggyj.png)

**创建方法**：首先在QT中完成ui的可视化构建，再通过pySide自带的pyside-uic.exe，将.ui文件转化为.py文件

###DialogMain:
实现Dialog的逻辑。一般来说，首先需要继承父类BaseDialogMain，接着再完成对Object自己UI的逻辑实现。
主要分为两部分，ShowDialog用以Command调用以展示UI，其中会调用ShowPointWidget，以加载Object本身的个性化属性UI。

**ShowDialog()中的结构主要有以下：**

1.init()：初始化，加载各类函数

2.initDialog()：初始化UI，主要用于各类槽函数的绑定和对UI的设置

3.slotOk()、slotCancel()、closeEvent()：用于“OK”、“Cancel”键的点击事件，点击确定保存数据并关闭UI，点击取消删除待创建物体并关闭UI

4.keepCommomData()、 loadCustomData()：物体名称、顺序、网格属性的保存和读取

接着，创建的新模型需要重写父类中的函数主要为：

1.getInfoFromObj():从物体中得到Object数据并保存到UI中，用于二次打开

2.setInfoToObj():将UI中填入的Object数据设置到物体中保存

```python
# -*- coding: utf-8 -*-
from PySide import QtGui
import BaseDialog

class ShowPointWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        # 载入Object本身的个性化属性UI
        QtGui.QWidget.__init__(self, parent)
        self.ui = PointWidget.Ui_Form()
        self.ui.setupUi(self)

class ShowDialog(BaseDialogMain.BaseModelDialog):
    def __init__(self, obj, isNew=False, parent=None):
        # 初始化各类函数
        QtGui.QDialog.__init__(self, parent)
        self.ui = BaseDialog.Ui_Dialog()
        self.ui.setupUi(self)

        self.pointWidget = ShowPointWidget()
        self.setCompleter(self.pointWidget.ui)
        self.ui.gridLayout_object.addWidget(self.pointWidget)
        self.customAttribute = BaseDialogMain.CustomShowWidget()
        self.setModal(False)

        self.initDialog()
        self.loadCommonData()
        self.loadCustomData()
        self.getInfoFromObj()
        
        self.obj = obj
        self.isNew = isNew
        self.isKeepData = False
        
        
    def getInfoFromObj(self):
         """
        从Object获取信息，并且设置到Dialog
        子类需要重写该方法，注意异常处理，不要因为输出异常而打不开对话框
        """
        pass
    

    def setInfoToObj(self):
        """
        从Dialog获取信息，并且赋值到Object
        子类需要重写该方法，注意异常处理，不要因为输出异常而关不掉对话框
        """
        pass

```
###Instance:
Instance主要实现物体属性和模型的建立，最终获取到一个物体。
```python
import FreeCAD
import Part
from Model3D.Tools import Tools3D, ObjectTools, InitDoc3D

class VolXXX:
    def __init__(self, obj):
        obj.Proxy = self

    def onChange(self, fp, prop):
        pass

    def execute(self, fp):
        """
        建模部分，在这里需要将一个Shape赋予fp.Shape，即物体的模型
        """
        # fp.Shape = AShape
        pass


class GetProperty:
    # 获取属性
    def __init__(self):
        FreeCAD.ActiveDocument.openTransaction('CreateXXX')
        self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", ObjectTools.ObjectType.XXX)
        InitDoc3D.addObjectToGroup_helper(self.obj, "XXX", "XX体")
        FreeCAD.ActiveDocument.commitTransaction()
        self.__setProperty(self.obj)

    def __setProperty(self, obj):
        # 设置物体具体的属性
        obj.addProperty("App::PropertyString", "Type").Type = ObjectTools.ObjectType.XXX
        # 例：若物体包含一个点，设置坐标属性的代码如下：
        obj.addProperty("App::PropertyDistance", "Point1X").Point1X = 0
        obj.addProperty("App::PropertyDistance", "Point1Y").Point1Y = 0
        obj.addProperty("App::PropertyDistance", "Point1Z").Point1Z = 0


def getObject():
    """
    返回获取的obj
    """
    # 首先新建一个物体，赋予其属性
    xxxObj = GetProperty()
    # 建立物体模型
    VolXXX(xxxObj.obj)
    # 设置物体代理
    Tools3D.ViewProvider(xxxObj.obj.ViewObject)
    return xxxObj.obj
```
