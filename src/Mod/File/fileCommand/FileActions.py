# -*- coding: utf-8 -*-
import FreeCAD
import FreeCADGui
import File.FileCommand.M3DFile.M3DFileUtil
import File.FileCommand.TextUI.FileTextView
from PySide import QtGui
from PySide import QtGui, QtCore

# from Modeling.Modeling2D.Tools.Tools2D import sayz


def QT_TRANSLATE_NOOP(ctx,txt): return txt # dummy function for the QT translator


class SaveAs:
    def Activated(self):
        from PySide import QtGui, QtCore
        FreeCAD.Console.PrintMessage("Save file as...\n")
        reply = QtGui.QMessageBox.information(None, "", "save-as button")
    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/File/FileResources/file-save-as.svg"
        MenuText = "File save as"
        ToolTip = "File save as..."
        Accel = "Ctrl+F4"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'Accel': Accel,
                'ToolTip': ToolTip}

class Close:
    def Activated(self):
        from PySide import QtGui, QtCore
        FreeCAD.Console.PrintMessage("Close file\n")
        reply = QtGui.QMessageBox.information(None, "", "close button")
    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/File/FileResources/file-close.svg"
        MenuText = "Close file"
        ToolTip = "Close file"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

class Exit:
    def Activated(self):
        from PySide import QtGui, QtCore
        FreeCAD.Console.PrintMessage("Exit app\n")
        reply = QtGui.QMessageBox.information(None,"","exit button")
    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/File/FileResources/application-exit.svg"
        MenuText = "Exit app"
        ToolTip = "Exit app"
        Accel = "Alt+F4"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'Accel': Accel,
                'ToolTip': ToolTip}

class RecentFile:
    def Activated(self):
        from PySide import QtGui, QtCore
        FreeCAD.Console.PrintMessage("open recent file\n")
        reply = QtGui.QMessageBox.information(None,"","recent file button")
    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/File/FileResources/file-recent.svg"
        MenuText = "Open recent file"
        ToolTip = "Open recent file"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

class saveM3D:
    def Activated(self):
        # change M3D view title
        flag = File.FileCommand.TextUI.FileTextView.FileView().isThisSubWindow()
        if flag:
            File.FileCommand.TextUI.FileTextView.FileView().setTitle(FreeCAD.ActiveDocument.Label)

        import os
        projectName = FreeCAD.ActiveDocument.FileName

        # get m3dFileUtil
        fileUtil = File.FileCommand.M3DFile.M3DFileUtil.M3DFileUtil(path=os.path.splitext(projectName)[0]+".m3d")
        # # save manager
        # fileUtil.saveCommandsManager()
        # save file
        # try:
        if FreeCAD.ActiveDocument.Comment == "new3D":
            FreeCAD.Console.PrintError("保存M3D\n")
        elif FreeCAD.ActiveDocument.Comment == "2D":
            FreeCAD.Console.PrintError("保存M2D")
        else:
            fileUtil.writeToFile()
        # 此处先注释
        # if FreeCAD.ActiveDocument.Comment != "2D":
        #     fileUtil.writeToFile()
        # else:
        #     FreeCAD.Console.PrintError("保存M2D")
        # except:
        #     QtGui.QMessageBox.warning(None, u"M3D保存失败", u"保存M3D文件时出错，请重试！")
        # 更新工作目录
        dirName = os.path.dirname(fileUtil.path)
        FreeCAD.clientSetWorkpath(dirName.decode("gbk"))

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Common/CommonResources/file-save-as.svg"
        MenuText = "saveM3D"
        Accel = "Ctrl+1"
        ToolTip = "saveM3D"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'Accel': Accel,
                'ToolTip': ToolTip}

class saveAsM3D:
    def Activated(self):
        # change M3D view title
        flag = File.FileCommand.TextUI.FileTextView.FileView().isThisSubWindow()
        if flag:
            File.FileCommand.TextUI.FileTextView.FileView().setTitle(FreeCAD.ActiveDocument.Label)

        import os
        projectName = FreeCAD.ActiveDocument.FileName

        # get m3dFileUtil
        fileUtil = File.FileCommand.M3DFile.M3DFileUtil.M3DFileUtil(path=os.path.splitext(projectName)[0]+".m3d")
        # # save manager
        # fileUtil.saveCommandsManager()
        # save file
        try:
            fileUtil.writeToFile()
        except:
            QtGui.QMessageBox.warning(None, u"M3D保存失败", u"保存M3D文件时出错，请重试！")
        # 更新工作目录
        dirName = os.path.dirname(fileUtil.path)
        FreeCAD.clientSetWorkpath(dirName.decode("gbk"))

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Common/CommonResources/file-save-as.svg"
        MenuText = "saveAsM3D"
        Accel = "Ctrl+2"
        ToolTip = "saveAsM3D"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'Accel': Accel,
                'ToolTip': ToolTip}


class M3DView:
    def Activated(self):
        from File.FileCommand.TextUI.FileTextView import FileView
        fileView = FileView()

        if fileView.getThisSubWindow() is None:
            fileView.showThisSubWindow()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/File/FileResources/file-m3dView.svg"
        MenuText = QT_TRANSLATE_NOOP(
                'M3DView',
                'Show M3D')
        ToolTip = "show M3DView if it isn't exist"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

    def IsActive(self):
        return FreeCAD.ActiveDocument is not None

class M3DFind:
    def Activated(self):
        from File.FileCommand.TextUI.FindDialogMain import FindMain
        from File.FileCommand.TextUI.FileTextView import FileView
        fileView = FileView()

        if fileView.getThisSubWindow() is not None:
            findDialog = FindMain(fileView.getThisSubWindow())
            findDialog.show()
            findDialog.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/File/FileResources/file-m3dFind.svg"
        MenuText = QT_TRANSLATE_NOOP(
                'M3DFind',
                'Find M3D')
        ToolTip = "show M3DView if it isn't exist"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

    def IsActive(self):
        from File.FileCommand.TextUI.FileTextView import FileView
        fileView = FileView()
        return fileView.getM3dSubWindow()

FreeCADGui.addCommand('File_SaveAs', SaveAs())
FreeCADGui.addCommand('File_Close', Close())
FreeCADGui.addCommand('App_Exit', Exit())
FreeCADGui.addCommand('File_Recent', RecentFile())
FreeCADGui.addCommand('M3DView', M3DView())
FreeCADGui.addCommand('M3DFind', M3DFind())

# FreeCADGui.addCommand('M3d_Save', saveM3D())
FreeCADGui.addCommand('M3d_SaveAs', saveAsM3D())

