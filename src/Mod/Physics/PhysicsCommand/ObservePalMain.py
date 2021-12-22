# -*- coding: UTF-8 -*-
import PySide
from PySide import QtGui, QtCore
from PySide.QtGui import QApplication, QMainWindow, QDockWidget, QTreeWidgetItem
import Physics.PhysicsGui.ObservePal
import FreeCAD
import Simulation
import json
import copy
import DoManager
#json格式数据需要保持原有顺序输出
from collections import OrderedDict

# from Modeling.Common.CommonCommand.NewDocument import ObjectDict,NewDocument
class ObserveSettingTree(QDockWidget):
    def __init__(self, parent=None):
        super(ObserveSettingTree, self).__init__(parent)
        self.ui = Physics.PhysicsGui.ObservePal.Ui_DockWidget_observeSettingTree()
        self.ui.setupUi(self)
        self.ui.treeWidget_observeSettingTree.header().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.ui.treeWidget_observeSettingTree.header().setStretchLastSection(False)
        self.ui.treeWidget_observeSettingTree.setAutoScroll(False)
        self.ui.treeWidget_observeSettingTree.expandAll()

        i = getMainWindow()
        qtab = i.findChild(QtGui.QTabWidget, 'combiTab')
        qtab.insertTab(qtab.count()-1, self, u'观测设置')
        tabBar = qtab.tabBar()
        tabBar.setTabButton(qtab.count()-2, QtGui.QTabBar.RightSide, None)

        # toplevel = QApplication.topLevelWidgets()
        # for i in toplevel:
        #     if i.metaObject().className() == "Gui::MainWindow":
        #         qtab = i.findChild(QtGui.QTabWidget, 'combiTab')
        #         qtab.insertTab(qtab.count()-1,self, u'观测设置')
        #         # 新建文档时保持在模型选项卡
        #         # qtab.setCurrentWidget(self)
        #         tabBar = qtab.tabBar()
        #         tabBar.setTabButton(qtab.count()-2, QtGui.QTabBar.RightSide, None)

        # 去除标题栏
        self.setTitleBarWidget(QtGui.QWidget(None))
        # app = QtGui.qApp
        # aw = app.activeWindow()

        # #aw == PySide.QtGui.QWidget object
        # # 获取Combo View
        # if aw:
        #     dw = aw.findChild(QtGui.QDockWidget, 'Combo View')
        #     # 获取Combo View 下的comiTab
        #     if dw:
        #         qtab = dw.findChild(QtGui.QTabWidget, 'combiTab')
        #         # 将结果目录作为一个tab添加到Combo View下
        #         qtab.addTab(self, u'源与边界与观测设置')
        #         # 设置 Tab 为不可关闭的
        #         # qtab.setTabsClosable(False)
        #         qtab.setCurrentWidget(self)
        #     else:
        #         print 'combiTab is not found'
        # else:
        #     print 'Combo View is not found'

        # 右键弹出菜单，双击修改数据
        self.ui.treeWidget_observeSettingTree.itemDoubleClicked['QTreeWidgetItem*', 'int'].connect(self.onDoubleClick)
        self.ui.treeWidget_observeSettingTree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.treeWidget_observeSettingTree.customContextMenuRequested['QPoint'].connect(self.onShow)

        self.treeWidget_monitor = TreeWidget_KeyMonitor()
        self.ui.treeWidget_observeSettingTree.installEventFilter(self.treeWidget_monitor)
        
        # self.ui.treeWidget_OperatingPanel.itemActivated['QTreeWidgetItem*', 'int'].connect(self.onDelete)

    def onShow(self, pos):
        # FreeCAD.Console.PrintMessage(item.data(0,QtCore.Qt.UserRole))
        # FreeCAD.Console.PrintMessage(item.data(1,QtCore.Qt.UserRole))
        item = self.ui.treeWidget_observeSettingTree.itemAt(pos)
        # 防止非物理设置右击
        if item is None:
            return
        JSON_CADComment = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict)
        parent = item.parent()
        if parent is not None:
            parent = parent.text(0)
        else:
            return
        itemClassName = item.data(0, QtCore.Qt.UserRole)
        itemUserName = item.data(1, QtCore.Qt.UserRole)
        # self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        # 创建QMenu
        self.contextMenu = QtGui.QMenu(self)
        self.actionA = self.contextMenu.addAction(u'修改数据')
        if not item.data(0, QtCore.Qt.UserRole) == "DefTimer":
            # 菜单中添加复制
            self.actionC = self.contextMenu.addAction(u'复制')
            self.actionC.triggered.connect(lambda: self.onCopy(parent, itemClassName, itemUserName))
            self.actionB = self.contextMenu.addAction(u'删除数据')
        # 将动作与处理函数相关联, 使用lambda可以传递额外的参数
        self.actionA.triggered.connect(lambda: self.onClick(parent, itemClassName, itemUserName))
        self.contextMenu.move(QtGui.QCursor().pos())
        self.contextMenu.show()
        level = item.data(2, QtCore.Qt.UserRole)

        if parent == u'等值观测':
            self.actionB.triggered.connect(lambda: self.onDelete(itemUserName, level, item))
        if parent == u'矢量观测':
            self.actionB.triggered.connect(lambda: self.onDelete(itemUserName, level, item))
        if parent == u'粒子观测':
            self.actionB.triggered.connect(lambda: self.onDelete(itemUserName, level, item))
        if parent == u'空间观测':
            self.actionB.triggered.connect(lambda: self.onDelete(itemUserName, level, item))
        if parent == u'时间观测':
            self.actionB.triggered.connect(lambda: self.onDelete(itemUserName, level, item))
        if parent == u'默认定时器':
            # 默认定时器不可删除
            pass
            # self.actionB.triggered.connect(lambda: self.onDelete(itemUserName,[1,0],item))
        if parent == u'定时器':
            self.actionB.triggered.connect(lambda: self.onDelete(itemUserName, level, item))


    def onDelete(self, itemUserName, level, item):

        itemData,oldData = deleteItem(item)

        # app = QtGui.qApp
        # aw = app.activeWindow()
        # if aw:
        #     tr = aw.findChild(QtGui.QTreeWidget,'treeWidget_OperatingPanel')

        JSON_CADComment = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict)
        oldJson = copy.copy(JSON_CADComment)
        try:
            JSON_CADComment.pop(itemUserName)
            FreeCAD.ActiveDocument.Begin = json.dumps(JSON_CADComment)
        except KeyError as reason:
            sayz("!!!Error:KeyError,Maybe lack of key:%s" % str(reason))
        FreeCAD.ActiveDocument.Begin = json.dumps(JSON_CADComment)

        jsonData = JSON_CADComment

        if itemData is not None:
            #更新两个栈
            record = [jsonData,itemData,oldJson,oldData]
            DoManager.newOperation(record)

        import File.FileCommand.M3DFile.M3DFileUtil
        # 更新m3d文档 by mx
        # 获得m3d的util
        fileUtil = File.FileCommand.M3DFile.M3DFileUtil.M3DFileUtil()
        # 获得最近的m3d字符串
        FileStr = fileUtil.getLatestM3DFileStr()
        # 进行文本的更新
        File.FileCommand.TextUI.FileTextView.FileView().updateText(FileStr)

    def onClick(self, parent, itemClassName, itemUserName):

        # FreeCAD.Console.PrintMessage(itemUserName)
        # 因为EmX这几个共用父亲名字的加载的时候他们itemData字段给的是Emx值，所以这块要格外区别一下
        # 0716 itemClassName 是从JSON里面加载的窗口的名字  itemUserName也是

        if parent == u'等值观测':
            Simulation.modifyData("Cntr",itemClassName,itemUserName)
        if parent == u'矢量观测':
            Simulation.modifyData("Vec",itemClassName,itemUserName)
        if parent == u'粒子观测':
            Simulation.modifyData("Pha",itemClassName,itemUserName)
        if parent == u'空间观测':
            Simulation.modifyData("Ran",itemClassName,itemUserName)
        if parent == u'时间观测':
            Simulation.modifyData("Obs",itemClassName,itemUserName)
        if parent == u'定时器':
            Simulation.modifyData("Timer",itemClassName,itemUserName)
        if parent == u'默认定时器':
            Simulation.modifyData("DefTimer",itemClassName,itemUserName)

    def onDoubleClick(self, item):
        if item.data(0, QtCore.Qt.UserRole) == None:
            return
        JSON_CADComment = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict)
        parent = item.parent()
        if parent is not None:
            parent = parent.text(0)
        else:
            return
        itemClassName = item.data(0, QtCore.Qt.UserRole)
        itemUserName = item.text(0)
        self.onClick(parent, itemClassName, itemUserName)

    def onCopy(self, parent, itemClassName, itemUserName):

        JSON_CADComment = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict)

        from Physics.PhysicsCommand import CntrDlgMain, VecDlgMain, PhaDlgMain, RanDlgMain, ObsDlgMain, TimerDlgMain
        import Physics.PhysicsCommand.DlgData as DlgData

        if parent == u'等值观测':
            newDlgClass=CntrDlgMain.CntrShow
            dataType="Cntr"
        elif parent == u'矢量观测':
            newDlgClass=VecDlgMain.VectorShow
            dataType="Vec"
        elif parent == u'粒子观测':
            newDlgClass=PhaDlgMain.PhaShow
            dataType="Pha"
        elif parent == u'空间观测':
            newDlgClass=RanDlgMain.RanShow
            dataType="Ran"
        elif parent == u'时间观测':
            newDlgClass=ObsDlgMain.ObsShow
            dataType="Obs"
        elif parent == u'定时器':
            newDlgClass=TimerDlgMain.TimerMain
            dataType="Timer"

        # 更改IndexCount，创建新对话框，然后调用onConfirm来实现复制
        Simulation.IndexCount[dataType] += 1
        newDlgName = dataType+str(Simulation.IndexCount[dataType])
        newDlg = newDlgClass("new", newDlgName)

        newDlg.ui.LineEdit_Name.setText(itemUserName)

        oldData = DlgData.DlgData(JSON_CADComment[itemUserName], itemUserName)
        newDlg.loadData(oldData)
        newDlg.onConfirm(JSON_CADComment, newDlgName)
        from Modeling.Common.CommonCommand.NewDocument import ObjectDict
        ObjectDict[newDlgName] = newDlg

        import File.FileCommand.M3DFile.M3DFileUtil
        # 更新m3d文档 by mx
        # 获得m3d的util
        fileUtil = File.FileCommand.M3DFile.M3DFileUtil.M3DFileUtil()
        # 获得最近的m3d字符串
        FileStr = fileUtil.getLatestM3DFileStr()
        # 进行文本的更新
        File.FileCommand.TextUI.FileTextView.FileView().updateText(FileStr)


    def show(self, *args, **kwargs):
        super(ObserveSettingTree, self).show()
        self.setAutoFillBackground(True)


class TreeWidget_KeyMonitor(QtCore.QObject):

    # def __init__(self,parent,name):
    #     if parent is not None:
    #         parent.installEventFilter(self)

    def __init__(self):
        super(TreeWidget_KeyMonitor, self).__init__()
        self.copied = False
        self.mainWindow = FreeCAD.Gui.getMainWindow()
        self.item = None

    def eventFilter(self, obj, event):
        # 拦截 Ctrl+C 快捷键
        if event.type() == QtCore.QEvent.ShortcutOverride and event.key() == QtCore.Qt.Key_C and event.modifiers() == QtCore.Qt.ControlModifier:
            event.accept()
            if True:
                i = getMainWindow()
                if True:
                    self.observeTreeWidget = i.findChild(QtGui.QTreeWidget, 'treeWidget_observeSettingTree')
            if self.observeTreeWidget is not None:
                self.item = self.observeTreeWidget.currentItem()

                if self.item is not None:
                    # 默认定时器不允许复制
                    if self.item.parent() is not None and self.item.parent().text(0) != u"默认定时器":
                        self.copied = True
                        if self.mainWindow is not None:
                            self.mainWindow.statusBar().showMessage("Press Ctrl+V to paste "+self.item.text(0))
                            return True
                    else:
                        self.mainWindow.statusBar().showMessage("Warning: "+self.item.text(0)+" cannot be copied!", 3000)
                        self.item = None

        # 拦截 Ctrl+X 快捷键
        if event.type() == QtCore.QEvent.ShortcutOverride and event.key() == QtCore.Qt.Key_X and event.modifiers() == QtCore.Qt.ControlModifier:
            event.accept()
            return True

        # 拦截 Ctrl+V 快捷键
        if event.type() == QtCore.QEvent.ShortcutOverride and event.key() == QtCore.Qt.Key_V and event.modifiers() == QtCore.Qt.ControlModifier:
            event.accept()
            if self.item is not None and self.copied == True:
                parent = self.item.parent()
                if parent is not None:
                    parentText = parent.text(0)
                    itemClassName = self.item.data(0, QtCore.Qt.UserRole)
                    itemUserName = self.item.text(0)
                    self.dockWidget = self.observeTreeWidget.parent().parent()
                    self.dockWidget.onCopy(parentText, itemClassName, itemUserName)
                    # self.copied = False # 如果只允许复制一次
                    return True

        # 拦截 Ctrl+D 快捷键
        if event.type() == QtCore.QEvent.ShortcutOverride and ((event.key() == QtCore.Qt.Key_D and event.modifiers() == QtCore.Qt.ControlModifier) or event.key() == QtCore.Qt.Key_Delete):
            event.accept()
            sayz("Ctrl+D or Delete ")
            if True:
                i = getMainWindow()
                if True:
                    self.observeTreeWidget = i.findChild(QtGui.QTreeWidget, 'treeWidget_observeSettingTree')
            if self.observeTreeWidget is not None:
                item = self.observeTreeWidget.currentItem()
                if item is not None:
                    itemUserName = item.data(1, QtCore.Qt.UserRole)
                    level = item.data(2, QtCore.Qt.UserRole)
                    parent = item.parent()
                    if parent is not None:
                        parent = parent.text(0)
                    else:
                        return
                    self.dockWidget = self.observeTreeWidget.parent().parent()
                    if parent == u'等值观测':
                        self.dockWidget.onDelete(itemUserName, level, item)
                    if parent == u'矢量观测':
                        self.dockWidget.onDelete(itemUserName, level, item)
                    if parent == u'粒子观测':
                        self.dockWidget.onDelete(itemUserName, level, item)
                    if parent == u'空间观测':
                        self.dockWidget.onDelete(itemUserName, level, item)
                    if parent == u'时间观测':
                        self.dockWidget.onDelete(itemUserName, level, item)
                    if parent == u'默认定时器':
                        # 默认定时器不可删除
                        pass
                    if parent == u'定时器':
                        self.dockWidget.onDelete(itemUserName, level, item)

            return True
        # 拦截 Ctrl+Z 快捷键
        if event.type() == QtCore.QEvent.ShortcutOverride and event.key() == QtCore.Qt.Key_Z and event.modifiers() == QtCore.Qt.ControlModifier:

            event.accept()
            sayz("Ctrl+Z ")
            DoManager.undo()
            return True

        # 拦截 Ctrl+Y 快捷键
        if event.type() == QtCore.QEvent.ShortcutOverride and event.key() == QtCore.Qt.Key_Y and event.modifiers() == QtCore.Qt.ControlModifier:
            event.accept()
            sayz("Ctrl+Y ")
            DoManager.redo()
            return True
        return QtGui.QTreeWidget.eventFilter(self, obj, event)


def sayz(msg):
    FreeCAD.Console.PrintMessage('-----------------------------------------')
    FreeCAD.Console.PrintMessage(msg)
    FreeCAD.Console.PrintMessage('\n')


# 退出工程，关闭分支树
def ObserveSettingTreeClose():
    if True:
        i = getMainWindow()
        if True:
            tr = i.findChild(QtGui.QTreeWidget, 'treeWidget_observeSettingTree')
            # #这里加个判断,是否找到tr
            if not tr==None:
                # 当树结构中存在item就清除它
                while tr.topLevelItemCount() > 0:
                    # 清除i对应的item并返回它
                    tr.topLevelItem(tr.topLevelItemCount()-1).takeChildren()
                    tr.takeTopLevelItem(tr.topLevelItemCount()-1)


def ObserveSettingTreeShow():
    '''
    @Author:wzn
    @Date:2019-10-12
    @Brief:这个函数用于加载工程项目时读取项目里面的信息并作相应处理 OpenDocument-->打开 NewDocument-->新建
           打开时要加载，新建时要抹除所有item信息，而且关闭当前项目tab时同样要抹除
           test1
           test2
        bbb = aw.findChildren(QtGui.QDockWidget)

           [
                Report view#
                Tree view#
                Property view
                Selection view
                Combo View#
                Python console#
           ]
    '''
    # 先尝试一下如果加载成功则keys----如果加载不成功则给他新建一个工程然后加载
    try:
        JSON_CADComment = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict)
        sayz(JSON_CADComment)
        # if JSON_CADComment == {}:
        #     sayz("JSON_CADComment")

        # if JSON_CADComment == "{}":
        #     sayz("JSON_CADCommentJSON_CADComment")

        # if JSON_CADComment == '{}':
        #     sayz("JSON_CADCommentJSON_CADCommentJSON_CADCommentJSON_CADCommentJSON_CADCommentJSON_CADComment")

        # while json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict) == {}:
        #     sayz("JSON_CADCommentJSON_CADCommentJSON_CADCommentJSON_CADCommentJSON_CADCommentJSON_CADComment")
        # sayz(JSON_CADComment)
        keys = JSON_CADComment.keys()
    except Exception as e:
        sayz("error with" + e)
        # from Modeling.Common.CommonCommand.NewDocument import NewDocument
        # NewDocument().Activated()
        # JSON_CADComment = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict)
    # finally:
    #     keys = JSON_CADComment.keys()

    toplevel = QApplication.topLevelWidgets()
    if True:
        i = getMainWindow()
        if True:
            tr = i.findChild(QtGui.QTreeWidget, 'treeWidget_observeSettingTree')
            #这里加个判断,是否找到tr
            if not tr==None:
                while tr.topLevelItemCount() > 0:
                    # 清除i对应的item并返回它
                    tr.topLevelItem(tr.topLevelItemCount() - 1).takeChildren()
                    tr.takeTopLevelItem(tr.topLevelItemCount() - 1)

    FreeCAD.Console.PrintMessage("ObserveSettingTree: \n")
    # FreeCAD.Console.PrintMessage(JSON_CADComment)

    for i in keys:

        if JSON_CADComment[i]["Dlg_Type"] == "Cntr_Type":
            addItem(u'等值观测', JSON_CADComment[i]["name"], JSON_CADComment[i]["name"])
        if JSON_CADComment[i]["Dlg_Type"] == "Vec_Type":
            addItem(u'矢量观测', JSON_CADComment[i]["name"], JSON_CADComment[i]["name"])
        if JSON_CADComment[i]["Dlg_Type"] == "Pha_Type":
            addItem(u'粒子观测', JSON_CADComment[i]["name"], JSON_CADComment[i]["name"])
        if JSON_CADComment[i]["Dlg_Type"] == "Ran_Type":
            addItem(u'空间观测', JSON_CADComment[i]["name"], JSON_CADComment[i]["name"])

        if JSON_CADComment[i]["Dlg_Type"] == "Obs_Type":
            addItem(u'时间观测', JSON_CADComment[i]["name"], JSON_CADComment[i]["name"])
        if JSON_CADComment[i]["Dlg_Type"] == "DefTimer_Type":
            addItem(u'默认定时器', JSON_CADComment[i]["name"], JSON_CADComment[i]["name"])
        if JSON_CADComment[i]["Dlg_Type"] == "Timer_Type":
            addItem(u'定时器', JSON_CADComment[i]["name"], JSON_CADComment[i]["name"])


def getMainWindow():
    """ Return the FreeCAD main window. """
    toplevel = PySide.QtGui.QApplication.topLevelWidgets()
    mwdf = None
    for i in toplevel:
        if i.metaObject().className() == "MainWindowDef":
            mwdf = i
            break
    wid = None
    for i in mwdf.children():
        if i.metaObject().className() == "QWidget":
            wid = i
            break
    for i in wid.children():
        if i.metaObject().className() == "Gui::MainWindow":
            return i
    return None


def getItemIndexByObserveType(MyTreeStruct,observeType):
    """
    用来根据边界类型得到器所在的根节点位置
    如果树结构中没有该边界类型，返回-1
    """

    # 遍历MyTreeStruct的根节点下
    for j in range(MyTreeStruct.topLevelItemCount()):
        if MyTreeStruct.topLevelItem(j).text(0) == observeType:
            sayz(MyTreeStruct.topLevelItem(j).text(0))
            return j

    return -1

def addItem(observeType, itemName, itemData):
    # itemName是编辑框里面的内容具有唯一性但是用户可以修改
    # itemData是代码自动生成的面板唯一ID 用户不可以修改
    # QApplication.topLevelWidgets() 打印出顶层部件对象
    # 感觉mw.findChildren(QtGui.QWidget)打印出来的是menu widget dockwidget
    # mw.findChildren(QtGui.QDockWidget)----<Physics.PhysicsCommand.TreeStructMain.FigTree object at>, <PySide.QtGui.QDockWidget object at 0x000000000D616608>
    # 感觉topLevelWidgets()打印出来的是menu widget
    # i.metaObject().className()打印出来的是Gui::MainWindow QWidget QComboBoxPrivateContainer QMdi::ControllerWidget QMenu等值
    # mw = getMainWindow()
    # toplevel = QApplication.topLevelWidgets()
    # for i in toplevel:
    #     if i.metaObject().className() == "Gui::MainWindow":
    #         tr = i.findChild(QtGui.QTreeWidget,'treeWidget_OperatingPanel')
    item = None
    toplevel = QApplication.topLevelWidgets()
    # for i in toplevel:
    if True:
        i = getMainWindow()
        # if i.metaObject().className() == "Gui::MainWindow":
        if True:
            MyTreeStruct = i.findChild(QtGui.QTreeWidget, 'treeWidget_observeSettingTree')
            item = QtGui.QTreeWidgetItem()
            item.setText(0, itemName)
            item.setData(0, QtCore.Qt.UserRole, itemData)  # itemClassName
            item.setData(1, QtCore.Qt.UserRole, itemName)  # itemUserName

            # 判断是否存在observeType对应的根节点
            level = getItemIndexByObserveType(MyTreeStruct,observeType)

            if level != -1:
                item.setData(2, QtCore.Qt.UserRole, level) # 设置根节点指数
                item.setData(3, QtCore.Qt.UserRole, MyTreeStruct.topLevelItem(level).childCount())  # 设置节点指数
                item.setIcon(0, QtGui.QIcon(FreeCAD.ConfigGet("AppHomePath") + "Mod/Physics/PhysicsResources/Item.svg"))
                MyTreeStruct.topLevelItem(level).addChild(item)
                MyTreeStruct.expandItem(MyTreeStruct.topLevelItem(level))
            else:
                # 添加该分类对应的根节点
                rootitem = QtGui.QTreeWidgetItem()
                rootitem.setText(0, observeType)
                rootitem.setIcon(0, QtGui.QIcon(FreeCAD.ConfigGet("AppHomePath") + "Mod/Physics/PhysicsResources/Group.svg"))
                MyTreeStruct.addTopLevelItem(rootitem)
                MyTreeStruct.expandItem(rootitem)
                item.setData(2, QtCore.Qt.UserRole, MyTreeStruct.topLevelItemCount()-1)  # 设置根节点指数
                item.setIcon(0, QtGui.QIcon(FreeCAD.ConfigGet("AppHomePath") + "Mod/Physics/PhysicsResources/Item.svg"))
                # 在该根节点下添加item
                item.setData(3, QtCore.Qt.UserRole, 0)  # 设置节点指数
                MyTreeStruct.topLevelItem(MyTreeStruct.topLevelItemCount()-1).addChild(item)
            # @fubiao
    if item is not None:
        itemType = item.parent().text(0)
        index = item.data(3, QtCore.Qt.UserRole)
        className = item.data(0, QtCore.Qt.UserRole)
        itemName = item.text(0)
        itemData = ["add", 'treeWidget_observeSettingTree',itemType, index, itemName, className]
        #用于恢复时delete Item
        oldData = ["delete", 'treeWidget_observeSettingTree',itemType, index, itemName, className]
        return itemData,oldData
    else:
        return None,None

# 根据当前选择的item更新名称
def updateItemName(itemDataNow):
    itemData=None
    oldData =None
    toplevel = QApplication.topLevelWidgets()
    for i in toplevel:
        if i.metaObject().className() == "Gui::MainWindow":
            MyTreeStruct = i.findChild(QtGui.QTreeWidget, 'treeWidget_observeSettingTree')
            item=MyTreeStruct.selectedItems()[0]
            itemType = item.parent().text(0)
            index = item.data(3, QtCore.Qt.UserRole)
            className = item.data(0, QtCore.Qt.UserRole)
            itemName = item.text(0)

            #存入旧的item信息，用于恢复
            oldData = ["modify", 'treeWidget_observeSettingTree',itemType, index, itemName, className]
            MyTreeStruct.selectedItems()[0].setText(0, itemDataNow)
            MyTreeStruct.selectedItems()[0].setData(1, QtCore.Qt.UserRole, itemDataNow)
            itemData = ["modify", 'treeWidget_observeSettingTree',itemType, index, itemDataNow,className ]
    return itemData,oldData

def deleteItem(item):
    itemData = None
    oldData = None
    if True:
        i = getMainWindow()
        if i.metaObject().className() == "Gui::MainWindow":
            tr = i.findChild(QtGui.QTreeWidget, 'treeWidget_observeSettingTree')
            # 判断是否存在observeType对应的根节点

            itemType = item.parent().text(0)
            index = item.data(3, QtCore.Qt.UserRole)
            className = item.data(0, QtCore.Qt.UserRole)
            itemName = item.text(0)
            level = getItemIndexByObserveType(tr, itemType)
            if level!= -1:
                itemData = ["delete",'treeWidget_observeSettingTree', itemType, index, itemName, className]
                #用于恢复时addItem
                oldData = ["add", 'treeWidget_observeSettingTree',itemType, index, itemName, className]
                tr.topLevelItem(level).removeChild(item)
                # 如果该根节点下没有item了，就清除它
                if tr.topLevelItem(level).childCount() == 0:
                    tr.takeTopLevelItem(level)
    return itemData,oldData

