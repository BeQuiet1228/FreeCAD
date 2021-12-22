# -*- coding: UTF-8 -*-
from PySide import QtGui, QtCore
from PySide.QtGui import QApplication, QMainWindow, QDockWidget, QTreeWidgetItem
import FreeCAD
import json
import copy
# from Modeling.Common.CommonCommand.NewDocument import undoStack,redoStack
from Physics.PhysicsCommand.__init__ import undoStack,redoStack
def getItemIndexBytype(MyTreeStruct,type):
    """
    用来根据边界类型得到器所在的根节点位置
    如果树结构中没有该边界类型，返回-1
    """

    # 遍历MyTreeStruct的根节点下
    for j in range(MyTreeStruct.topLevelItemCount()):
        if MyTreeStruct.topLevelItem(j).text(0) == type:
            sayz(MyTreeStruct.topLevelItem(j).text(0))
            return j

    return -1


def findItem(MyTreeStruct,level,itemName):

    for i in range(MyTreeStruct.topLevelItem(level).childCount()):
        if MyTreeStruct.topLevelItem(level).child(i).text(0) == itemName:
            item = MyTreeStruct.topLevelItem(level).child(i)
            return item
    return 0

#对Item进行增删改
def dealItem(itemParam,itemNameBefore):
    if itemParam is None or len(itemParam) !=6:
        sayz("无需修改item")
        return
    #item中的参数，分别是item处理类型，item所在树，item分类，item所处位置，item名字，item对应面板名字
    dealType,treeName, itemType, index, itemName,className = itemParam

    if dealType=="modify":
        toplevel = QApplication.topLevelWidgets()
        for i in toplevel:
            if i.metaObject().className() == "Gui::MainWindow":
                tr = i.findChild(QtGui.QTreeWidget, treeName)
                level = getItemIndexBytype(tr, itemType)
                if level != -1:
                    #itemNameBefore用来找需要修改的item
                    item = findItem(tr, level, itemNameBefore)
                    if item:
                        item.setText(0, itemName)
                        item.setData(1, QtCore.Qt.UserRole, itemName)
                        item.setData(2, QtCore.Qt.UserRole, level)
                        return item.parent().text(0)
                break
    elif dealType=="delete":
        toplevel = QApplication.topLevelWidgets()
        for i in toplevel:
            if i.metaObject().className() == "Gui::MainWindow":
                tr = i.findChild(QtGui.QTreeWidget, treeName)
                level = getItemIndexBytype(tr, itemType)
                if level != -1:
                    item = findItem(tr,level,itemName)
                    
                    if item:
                        parent = item.parent().text(0)
                        tr.topLevelItem(level).removeChild(item)
                        # 如果该根节点下没有item了，就清除它
                        if tr.topLevelItem(level).childCount() == 0:
                            tr.takeTopLevelItem(level)
                        sayz("eeeeee")
                        sayz(parent)
                        return parent

                break
    elif dealType == "add":

        toplevel = QApplication.topLevelWidgets()
        for i in toplevel:
            if i.metaObject().className() == "Gui::MainWindow":
                MyTreeStruct = i.findChild(QtGui.QTreeWidget, treeName)
                item = QtGui.QTreeWidgetItem()
                item.setText(0, itemName)
                item.setData(0, QtCore.Qt.UserRole, className)  # itemUserName
                item.setData(1, QtCore.Qt.UserRole, itemName)  # itemClassName

                # 判断是否存在observeType对应的根节点
                level = getItemIndexBytype(MyTreeStruct, itemType)
                
                if level != -1:
                    item.setData(2, QtCore.Qt.UserRole, level)  # 设置根节点指数
                    item.setData(3, QtCore.Qt.UserRole, index)  # itemUserName
                    item.setIcon(0, QtGui.QIcon(
                        FreeCAD.ConfigGet("AppHomePath") + "Mod/Physics/PhysicsResources/Item.svg"))
                    if index < MyTreeStruct.topLevelItem(level).childCount():
                        MyTreeStruct.topLevelItem(level).insertChild(index,item)
                    else:
                        MyTreeStruct.topLevelItem(level).addChild(item)
                    MyTreeStruct.expandItem(MyTreeStruct.topLevelItem(level))
                else:
                    # 添加该分类对应的根节点
                    rootitem = QtGui.QTreeWidgetItem()
                    rootitem.setText(0, itemType)
                    rootitem.setIcon(0, QtGui.QIcon(
                        FreeCAD.ConfigGet("AppHomePath") + "Mod/Physics/PhysicsResources/Group.svg"))
                    MyTreeStruct.addTopLevelItem(rootitem)
                    MyTreeStruct.expandItem(rootitem)
                    item.setData(2, QtCore.Qt.UserRole, MyTreeStruct.topLevelItemCount() - 1)  # 设置根节点指数
                    item.setData(3, QtCore.Qt.UserRole, 0)  # 设置节点指数
                    item.setIcon(0, QtGui.QIcon(
                        FreeCAD.ConfigGet("AppHomePath") + "Mod/Physics/PhysicsResources/Item.svg"))
                    # 在该根节点下添加item
                    MyTreeStruct.topLevelItem(MyTreeStruct.topLevelItemCount() - 1).addChild(item)

                return item.parent().text(0)

    return None

#更新Begin
def dealJson(jsonData,parent):

    if parent == u'新材料':
        FreeCAD.ActiveDocument.Comment = json.dumps(jsonData)
    elif parent is not None:
        FreeCAD.ActiveDocument.Begin = json.dumps(jsonData)
    import File.FileCommand.M3DFile.M3DFileUtil
    # 更新m3d文档 by mx
    # 获得m3d的util
    fileUtil = File.FileCommand.M3DFile.M3DFileUtil.M3DFileUtil()
    # 获得最近的m3d字符串
    FileStr = fileUtil.getLatestM3DFileStr()
    # 进行文本的更新
    File.FileCommand.TextUI.FileTextView.FileView().updateText(FileStr)

#栈中最多有20个元素
def push(stack,record):
    if len(stack)>=20:
        del stack[0]
    stack.append(record)

#面板增加新操作增删改，需要往undoStack添加record，并清空redoStack
#record数组包含四个元素，分别是执行命令后的Begin数据和item状态，以及执行命令前的Begin数据和item状态
def newOperation(record):
    global undoStack
    global redoStack
    push(undoStack,record)
    #彻底清空
    redoStack[:]=[]
    # sayz("undoStack\n")
    # sayz(len(undoStack))
    # sayz(undoStack)
    # sayz("redoStack\n")
    # sayz(len(redoStack))
    # sayz(redoStack)

def undo():
    global undoStack
    global redoStack
    sayz("undo()")
    if undoStack==[]:
        sayz("undoStack is empty")
    else:
        record = undoStack.pop()
        push(redoStack,record)

        # 撤销分两步：更新begin和增删改item
        jsonData = record[2]
        itemParam = record[3]

        sayz("执行撤销命令:"+itemParam[0]+" "+itemParam[-2]+"面板")

        
        parent = dealItem(itemParam,record[1][-2])
        dealJson(jsonData,parent)
        # sayz("undoStack\n")
        # sayz(len(undoStack))
        # sayz(undoStack)
        # sayz("redoStack\n")
        # sayz(len(redoStack))
        # sayz(redoStack)

def redo():
    global undoStack
    global redoStack
    sayz("redo()")
    if redoStack == []:
        sayz("redoStack is empty")
    else:
        record = redoStack.pop()
        push(undoStack, record)

        # 撤销分两步：更新begin和增删改item
        jsonData = record[0]
        itemParam = record[1]
        sayz("执行恢复命令:" + itemParam[0] + " " + itemParam[-2] + "面板")
        parent = dealItem(itemParam,record[3][-2])
        dealJson(jsonData,parent)
        # sayz("undoStack\n")
        # sayz(len(undoStack))
        # sayz(undoStack)
        # sayz("redoStack\n")
        # sayz(len(redoStack))
        # sayz(redoStack)


def sayz(msg):
    FreeCAD.Console.PrintMessage('-----------------------------------------')
    FreeCAD.Console.PrintMessage(msg)
    FreeCAD.Console.PrintMessage('\n')
