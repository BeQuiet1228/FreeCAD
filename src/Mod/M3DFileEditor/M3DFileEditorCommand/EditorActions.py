# -*- coding: utf-8 -*-
import FreeCAD
import FreeCADGui
from PySide import QtGui


def set_FilePath(value2):
    FreeCAD.ConfigSet("EditorFilePath",value2)
def get_FilePath(defFilePath=""):
    try:
        return FreeCAD.ConfigGet("EditorFilePath")
    except :
        FreeCAD.Console.PrintError("error edit file path\n")
        # return defFilePath

# set_value2(2)

# class FilePath():
#     filePath="E:\\qqData\\Example\\Example\\CIRCUIT_P\\CIRCUIT_P.m3d"

# curFilePath=FilePath()

class EditorOpen:
    def Activated(self):
        sayz("open")
        # import Tkinter, tkFileDialog
        # root = Tkinter.Tk()
        # root.withdraw()
        # root.filename = tkFileDialog.askopenfilename(initialdir = "/",title = "Select file",
        #                                                              filetypes = (("m3d files","*.m3d"),("all files","*.*")))

        # @maxin, 更换为用pyside打开文件
        fileName, selectedFilter = QtGui.QFileDialog.getOpenFileName(None, u"打开M3D文件", "", u"M3D Files (*.m3d)")
        if fileName != '':
            # curFilePath.filePath=fileName
            set_FilePath(fileName)
            FreeCAD.Console.PrintMessage("\nOpen: "+get_FilePath()+"\n")
            import os
            dirName = os.path.dirname(get_FilePath())
            FreeCAD.clientSetWorkpath(dirName)
            sayz(fileName)
            import M3DFileEditor
            fileEditor = M3DFileEditor.M3DFileEditorCommand.FileTextEditor.FileEditor()
            # 获取文件中字符串
            str = fileEditor.readFile(fileName)
            # @fubiao
            EditorDisplay().Activated()
            subWindow = fileEditor.getThisSubWindow()
            #尝试几种打开方式
            try:
                subWindow.widget().ui.textEdit.setText(str.decode("utf-8"))
            except:
                try:
                    subWindow.widget().ui.textEdit.setText(str.decode("gbk"))
                except:
                    subWindow.widget().ui.textEdit.setText()
            
        else:
            sayz("您没有选择任何文件")


    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/M3DFileEditor/M3DFileEditorResources/m3d-open.svg"
        MenuText = "open"
        ToolTip = "open"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

class EditorSave:
    def Activated(self):
        sayz("Save")
        # import Tkinter, tkFileDialog
        # root = Tkinter.Tk()
        # root.withdraw()
        # root.filename = tkFileDialog.asksaveasfilename(initialdir="/", title="Select file",
        #                                                filetypes=(("m3d files", "*.m3d"), ("all files", "*.*")))

        defaultDir = ""
        # if FilePath.filePath:
        if get_FilePath():
            defaultDir = get_FilePath()
        else:
            #不存在路径的话，就另存为
            EditorSaveAs().Activated()
            return
        # fileName, _ = QtGui.QFileDialog.getSaveFileName(None, u"保存M3D文件", defaultDir, u"M3D Files (*.m3d)")

        if get_FilePath():
            # FilePath.filePath = fileName
            # curFilePath.filePath=fileName
            FreeCAD.Console.PrintMessage("\nSave to: "+get_FilePath()+"\n")
            import M3DFileEditor
            fileEditor = M3DFileEditor.M3DFileEditorCommand.FileTextEditor.FileEditor()
            subWindow = fileEditor.getThisSubWindow()
            # 获取文件中字符串
            m3dStr = subWindow.widget().ui.textEdit.toPlainText()
            try:
                fileEditor.writeToFile(get_FilePath(), m3dStr)
                import os
                # 更新工作目录
                dirName = os.path.dirname(get_FilePath())
                FreeCAD.clientSetWorkpath(dirName)
            except:
                QtGui.QMessageBox.warning(None, u"M3D保存失败", u"保存M3D文件时出错，请重试！")
        else:
            sayz("您没有保存文件")


        # if root.filename != '':
        #     if not root.filename.endswith('.m3d'):
        #         root.filename = root.filename + '.m3d'
        #     sayz(root.filename)
        #     import M3DFileEditor
        #     fileEditor = M3DFileEditor.M3DFileEditorCommand.FileTextEditor.FileEditor()
        #     subWindow = fileEditor.getThisSubWindow()
        #     # 获取文件中字符串
        #     str = subWindow.widget().ui.textEdit.toPlainText()
        #     fileEditor.writeToFile(root.filename,str)
        # else:
        #     sayz("您没有保存文件")

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/M3DFileEditor/M3DFileEditorResources/m3d-save.svg"
        MenuText = "Save"
        ToolTip = "Save"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}
#@fubiao saveAs
class EditorSaveAs:
    def Activated(self):
        sayz("SaveAs")

        defaultDir = ""
        # if FilePath.filePath:
        if get_FilePath():
            defaultDir = get_FilePath()
        fileName, _ = QtGui.QFileDialog.getSaveFileName(None, u"保存M3D文件", defaultDir, u"M3D Files (*.m3d)")

        if fileName:
            # FilePath.filePath = fileName
            set_FilePath(fileName)
            FreeCAD.Console.PrintMessage("\nSave to: "+get_FilePath()+"\n")
            import M3DFileEditor
            fileEditor = M3DFileEditor.M3DFileEditorCommand.FileTextEditor.FileEditor()
            subWindow = fileEditor.getThisSubWindow()
            # 获取文件中字符串
            m3dStr = subWindow.widget().ui.textEdit.toPlainText()
            try:
                fileEditor.writeToFile(get_FilePath(), m3dStr)
                import os
                # 更新工作目录
                dirName = os.path.dirname(get_FilePath())
                FreeCAD.clientSetWorkpath(dirName)
            except:
                QtGui.QMessageBox.warning(None, u"M3D保存失败", u"保存M3D文件时出错，请重试！")
        else:
            sayz("您没有保存文件")


    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/M3DFileEditor/M3DFileEditorResources/m3d-saveAs.svg"
        MenuText = "SaveAs"
        ToolTip = "SaveAs"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

class EditorDisplay:
    def Activated(self):
        from M3DFileEditor.M3DFileEditorCommand.FileTextEditor import FileEditor
        fileEditor = FileEditor()

        if not fileEditor.isThisSubWindow():
            fileEditor.showThisSubWindow()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/M3DFileEditor/M3DFileEditorResources/m3d-display.svg"
        MenuText = "display"
        ToolTip = "display"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

class EditorRedo:
    # 重做按钮
    def Activated(self):
        from M3DFileEditor.M3DFileEditorCommand.FileTextEditor import FileEditor
        fileEditor = FileEditor()
        fileEditor.redo()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/M3DFileEditor/M3DFileEditorResources/m3d-redo.svg"
        MenuText = "redo"
        ToolTip = "redo"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

class EditorUndo:
    # 撤回按钮
    def Activated(self):
        from M3DFileEditor.M3DFileEditorCommand.FileTextEditor import FileEditor
        fileEditor = FileEditor()
        fileEditor.undo()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/M3DFileEditor/M3DFileEditorResources/m3d-undo.svg"
        MenuText = "undo"
        ToolTip = "undo"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

class EditorCut:
    # 剪切按钮
    def Activated(self):
        from M3DFileEditor.M3DFileEditorCommand.FileTextEditor import FileEditor
        fileEditor = FileEditor()
        fileEditor.cut()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/M3DFileEditor/M3DFileEditorResources/m3d-cut.svg"
        MenuText = "cut"
        ToolTip = "cut"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

class EditorCopy:
    # 复制按钮
    def Activated(self):
        from M3DFileEditor.M3DFileEditorCommand.FileTextEditor import FileEditor
        fileEditor = FileEditor()
        fileEditor.copy()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/M3DFileEditor/M3DFileEditorResources/m3d-copy.svg"
        MenuText = "copy"
        ToolTip = "copy"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

class EditorPaste:
    # 粘贴按钮
    def Activated(self):
        from M3DFileEditor.M3DFileEditorCommand.FileTextEditor import FileEditor
        fileEditor = FileEditor()
        fileEditor.paste()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/M3DFileEditor/M3DFileEditorResources/m3d-paste.svg"
        MenuText = "paste"
        ToolTip = "paste"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

class EditorFind:
    # 查找按钮
    def Activated(self):
        from M3DFileEditor.M3DFileEditorCommand.FindDialogMain import FindMain
        findDialog = FindMain(FreeCADGui.getMainWindow())
        findDialog.show()
        findDialog.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/M3DFileEditor/M3DFileEditorResources/m3d-find.svg"
        MenuText = "find"
        ToolTip = "find"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

class EditorReplace:
    # 提换按钮
    def Activated(self):
        from M3DFileEditor.M3DFileEditorCommand.ReplaceDialogMain import ReplaceMain
        findDialog = ReplaceMain(FreeCADGui.getMainWindow())
        findDialog.show()
        findDialog.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/M3DFileEditor/M3DFileEditorResources/m3d-replace.svg"
        MenuText = "replace"
        ToolTip = "replace"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

# class Modeling2DWorkbench:
#     def Activated(self):
#         FreeCADGui.activateWorkbench("Modeling2DWorkbench")

#         mainWindow = FreeCADGui.getMainWindow()
#         propertyView = mainWindow.findChild(QtGui.QDockWidget, "Property view")
#         propertyView.setVisible(True)

#     def GetResources(self):
#         IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling2D/modeling2DResources/2DModelingWorkbench.svg"
#         MenuText = "2D Modeling"
#         ToolTip = "To 2D Modeling Part"
#         return {'Pixmap': IconPath,
#                 'MenuText': MenuText,
#                 'ToolTip': ToolTip}

# class Modeling3DWorkbench:
#     def Activated(self):
#         FreeCADGui.activateWorkbench("Modeling3DWorkbench")
#         mainWindow = FreeCADGui.getMainWindow()
#         propertyView = mainWindow.findChild(QtGui.QDockWidget, "Property view")
#         propertyView.setVisible(True)

#     def GetResources(self):
#         IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling3D/modeling3DResources/3DModelingWorkbench.svg"
#         MenuText = "3D Modeling"
#         ToolTip = "To 3D Modeling Part"
#         return {'Pixmap': IconPath,
#                 'MenuText': MenuText,
#                 'ToolTip': ToolTip}

# class SimulationWorkbench:
#     def Activated(self):
#         FreeCADGui.activateWorkbench("PhysicsWorkbench")
#         mainWindow = FreeCADGui.getMainWindow()
#         propertyView = mainWindow.findChild(QtGui.QDockWidget, "Property view")
#         propertyView.setVisible(False)

#     def GetResources(self):
#         IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Physics/PhysicsResources/physics-workbench.svg"
#         MenuText = "Simulation"
#         ToolTip = "To Simulation Part"
#         return {'Pixmap': IconPath,
#                 'MenuText': MenuText,
#                 'ToolTip': ToolTip}

# class PostProcessingWorkbench:
#     def Activated(self):
#         FreeCADGui.activateWorkbench("VisualWorkbench")

#         mainWindow = FreeCADGui.getMainWindow()
#         propertyView = mainWindow.findChild(QtGui.QDockWidget, "Property view")
#         propertyView.setVisible(False)

#     def GetResources(self):
#         IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Visualization/visualizationResources/VisualWorkbench.svg"
#         MenuText = "Post Processing"
#         ToolTip = "To Post Processing Part"
#         return {'Pixmap': IconPath,
#                 'MenuText': MenuText,
#                 'ToolTip': ToolTip}


FreeCADGui.addCommand("EditorOpen", EditorOpen())
FreeCADGui.addCommand("EditorSave", EditorSave())
FreeCADGui.addCommand("EditorSaveAs",EditorSaveAs())
FreeCADGui.addCommand("EditorDisplay", EditorDisplay())
FreeCADGui.addCommand("EditorRedo", EditorRedo())
FreeCADGui.addCommand("EditorUndo", EditorUndo())
FreeCADGui.addCommand("EditorCut", EditorCut())
FreeCADGui.addCommand("EditorCopy", EditorCopy())
FreeCADGui.addCommand("EditorPaste", EditorPaste())
FreeCADGui.addCommand("EditorFind", EditorFind())
FreeCADGui.addCommand("EditorReplace", EditorReplace())
# FreeCADGui.addCommand("Modeling 2D", Modeling2DWorkbench())
# FreeCADGui.addCommand("Modeling 3D", Modeling3DWorkbench())
# FreeCADGui.addCommand("Simulation", SimulationWorkbench())
# FreeCADGui.addCommand("Post Processing", PostProcessingWorkbench())
import SwitchWorkbench



def sayz(msg):
    FreeCAD.Console.PrintMessage(msg)
    FreeCAD.Console.PrintMessage("\n")
