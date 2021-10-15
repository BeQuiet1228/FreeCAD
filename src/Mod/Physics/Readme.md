# Physics架构
#### @Author:wzj
#### @Date:2019.05.05
[新建工程](#新建工程)

[打开工程](#打开工程)

[新建Port面板](#新建port面板)

[加载Port面板](#加载port面板)

[双击分支树 item 之后发生了什么？](#双击分支树-item-之后发生了什么)


## 新建工程
一般的，当我们第一次新建工程时，触发[NewDocument](../Modeling/Common/CommonCommand/NewDocument.py)
``` python
class NewDocument:
    def Activated(self):  
        app = QtGui.qApp
        aw = app.activeWindow()       
        if aw:
            tr = aw.findChild(QtGui.QTreeWidget,'treeWidget_OperatingPanel') 
            if not tr:                  
                tree = FigTree()
                tree.show() 
        省略 省略 省略
```
实现的功能主要为：查找当前活动窗口 **aw = app.activeWindow()** -->查找它的**treeWidget_OperatingPanel** 孩子，如果没有 **if not tr:** 就新建一个分支树面板 **tree = FigTree()**
## 打开工程
一般的，当我们打开工程时，触发[OpenDocument](../Modeling/Common/CommonCommand/NewDocument.py)
``` python
class OpenDocument:
    '''
    @Author:wzj
    @Date:2019-04-25
    @Brief:这个函数用于加载工程项目时读取项目里面的信息并作相应处理 OpenDocument-->打开 NewDocument-->新建
    '''        
    def Activated(self):
        try:
            app = QtGui.qApp
            aw = app.activeWindow()       
            if aw:
                tr = aw.findChild(QtGui.QTreeWidget,'treeWidget_OperatingPanel') 
                if not tr:                   
                    tree = FigTree()
                    tree.show()                 
            FigTreeShow()
        except:
            pass
        省略 省略 省略
```
实现的功能主要为：查找当前活动窗口 **aw = app.activeWindow()** -->查找它的**treeWidget_OperatingPanel**孩子，如果没有**if not tr:**就新建一个分支树面板**tree = FigTree()**
## 新建Port面板
一般的，几乎每一个窗口都有相似的架构，我们以Port面板来详细讲述一下这种独特的架构。
``` python
def show(type,className):
```
![Port面板](https://s2.ax1x.com/2019/05/05/E0ecdI.png)

当我们点击面板上的**Port**按钮后，触发[Simulation](./PhysicsCommand/Simulation.py)中`FreeCADGui.addCommand('Port', Port())`-->
``` python
class Port:
    def Activated(self):         
        className = "Port" + str(IndexCount["Port"])
        PortDlgMain.show("new",className)                
        IndexCount["Port"]+=1
```
其中那个*IndexCount*是一个全局变量，初始值为1

`PortDlgMain.show("new",className)`
触发[PortDlgmain](./PhysicsCommand/PortDlgMain.py)

``` python
def show(type,className):
    global  ObjectDict  
    if type == "new":
        ObjectDict[className] = PortMain("new",className)
        ObjectDict[className].show()
        ObjectDict[className].exec_()
    elif type == "old":
        if className in ObjectDict.keys(): 
            ObjectDict[className].refreshCombox()
            ObjectDict[className].show()
            ObjectDict[className].exec_()             
        else:
            ObjectDict[className] = PortMain(className,className)
            ObjectDict[className].show()
            ObjectDict[className].exec_()   
```


`global  ObjectDict`
这是一个非常重要的全局变量用来存储每一个面板窗口的对象名称，它的定义在[global  ObjectDict的定义](../Modeling/Common/CommonCommand/NewDocument.py)中。
---
>>Q&A1:为什么把它的定义放在那么远的文件里面？

>那是因为如果把他的定义放在physics文件夹里面会动态刷新，把它的值由刷新成初始值。这块我调了一天，暂时先这样解决吧。

由于我们这是第一次点击Port面板，所以是希望它能新建**new**一个面板，所以**type**为“new” --->`PortMain("new",className)`生成一个新的Port面板对象，对象名字叫 ` ObjectDict[className] ` 这里比较巧妙用到了之前那个递增的全局变量 [className](./PhysicsCommand/Simulation.py):每次新建一个Port面板，className都会自加1，**！！！确保对象名字没有重复！！！**

>>Q&A2:为什么要这么做呢？

>那是因为每次新建一个窗口**(面板)**对象之后-->这个对象一直存活于堆中-->下一次我想打开它进行修改就可以直接调用这个对象的show()方法继续显示。省的再重新创建一个新的窗口对象加载元素值这样麻烦了----- 不过在打开保存好的工程项目时，我们还是要一个一个重新load元素的值的。当然这是后话了。

``        ObjectDict[className].show()
        ObjectDict[className].exec_()``
这两句话是让窗口显示时处于最高优先级位置：只有关闭掉这个窗口才能进行其他操作，类似与word未保存退出时那个警告窗口。

---
当我们在面板XGB乱点一通之后，点击确定按钮触发`self.ui.pushButton_ok.clicked.connect(lambda: self.onConfirm(JSON_CADComment,className)`　采用lambda表达式是为了传参数进去。
``` python
    def onConfirm(self,FreeCAD_Comment_Dict,className):
        global flag 
        count = 1
        #这个name必须确保唯一性！！！
        #也就是他的窗口编辑框里面的值
        name = self.ui.LineEdit_Name.text() 
        self.close()    
        if flag == 0:
            while name in FreeCAD_Comment_Dict.keys(): 
               name = self.ui.LineEdit_Name.text() + str(count) 
               count+=1             
            self.ui.LineEdit_Name.setText(name)       
            addItem([0,0], name, className)
            flag = 1
        newData = DlgData({},name)           
        self.keepData(newData)
```
常规的逻辑是我第一次打开port面板按下确定按钮之后，创建一个item条目添加到TreeWidget下的“波导窗口”下面，等我双击该条目之后，显示该Port面板并进行内容修改，修改完之后再次点击确定按钮，这个时候就不能再新建一个重名的item了---因为我是基于原来的Port面板进行修改。为了解决这个问题，我们引入**信号量flag**这个机制：它的作用就是为了解决上述这个问题。当新建面板成功之后，flag置为1 `flag = 1` 所以就执行不了 `addItem([0,0], name, className)`  完美！！！

## 加载Port面板
上述章节讲述了新建port 面板的细节，当我们保存工程项目之后，下一次打开它的时候，分支树(TreeWidget)应该同步加载工程项目中的面板信息，将其添加到相应的栏目下面。
为了实现这个功能，我们在C++代码添加了一个 `Customize_Open`函数，每次打开项目都会触发[OpenDocument](../Modeling/Common/CommonCommand/NewDocument.py) -->继而触发`FigTreeShow()`-->然后将FreeCAD.ActiveDocument.Comment储存的窗口数据信息读取出来，按照`Dlg_Type`这个key来添加到对应的栏目下面。

## 双击分支树 item 之后发生了什么？
双击分支树之后，触发`self.ui.treeWidget_OperatingPanel.itemDoubleClicked['QTreeWidgetItem*', 'int'].connect(self.onShow)`-->

``` python 
def onShow(self, item, column):
        JSON_CADComment = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict)
        sayz(JSON_CADComment.keys())
        parent = item.parent()
        if parent is not None:
            parent = parent.text(0)
        itemClassName = item.data(0, QtCore.Qt.UserRole)
        itemUserName = item.data(1, QtCore.Qt.UserRole)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        # 创建QMenu
        self.contextMenu = QtGui.QMenu(self)
        self.actionA = self.contextMenu.addAction(u'修改数据')
        self.actionB = self.contextMenu.addAction(u'删除数据')
        # 将动作与处理函数相关联, 使用lambda可以传递额外的参数
        self.actionA.triggered.connect(lambda: self.onClick(parent,itemClassName,itemUserName,item,column))
        self.contextMenu.move(QtGui.QCursor().pos())
        self.contextMenu.show()      
        if parent == u'波导端口':
            self.actionB.triggered.connect(lambda: self.onDelete(itemUserName,[0,0],item)) 
```
# Log
## 2019-05-18
### 与MX学姐接口方面
- 还差Free Sol ExP Foil Ind 五个面板的接口函数没有写
### 分支树方面
- 还存在双击父亲item弹出菜单这个bug，亟待修复
- 每次切换两个激活工程项目时，需要重新从全局变量里加载项目结构信息，这是很蠢且很浪费时间的一个操作，后期这块需要优化
### 其他方面
- 还差Obs面板一些测试没有通过
- 面板有一个根据加载场上点的信息自动填充起点止点信息这个功能还没有实现
- 目前每个工程面板数据信息是存储在FreeCAD.Comment这个全局变量里面，为了保险起见，需要将它隐藏到用户不可修改的变量里去。这个需要修复
- 目前还存在一些窗口一些界面设计bug需要修复

## 2019-05-29
- 修复了之前甲方说的那个添加不了分支树的bug，这个bug是由于我是靠获取activeWindow来查找treeStruct，然而用户可能由于将键盘focus到了别的应用中或者别的窗口中导致激活的窗口已经不是freecad了，所以造成添加不上这个bug。通过查看MX学姐程序了解到可以遍历topLevelWidgets上的widget来获取我想要的treeStruct
```python
    toplevel = QApplication.topLevelWidgets()
    for i in toplevel:
        if i.metaObject().className() == "Gui::MainWindow":    
            MyTreeStruct = i.findChild(QtGui.QTreeWidget,'treeWidget_OperatingPanel')          
            item = QtGui.QTreeWidgetItem()
            item.setText(0, itemName)
            item.setData(0, QtCore.Qt.UserRole, itemData)   #itemUserName 
            item.setData(1, QtCore.Qt.UserRole, itemName)   #itemClassName   
            if type(level) != list:
                MyTreeStruct.topLevelItem(level).addChild(item)
            else:
                MyTreeStruct.topLevelItem(level[0]).child(level[1]).addChild(item)
```
我感觉它的这个findChild是可以嵌套查询好几层的，原先我试过"QWidget" "QTreeWidget"

# 测试注意
! ==============================================================================!
! PARAMETER
后面要空一行
每个属性后面要加空行
每个等号要前后有空格
degree可以用.来代替
