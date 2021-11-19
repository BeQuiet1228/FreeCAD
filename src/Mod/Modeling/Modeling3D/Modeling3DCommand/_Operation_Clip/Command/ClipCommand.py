# encoding:utf-8
import ClipDlg
import FreeCAD,FreeCADGui
from PySide import QtCore,QtGui
class ClipCommand:
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        # dlg=ClipDlg.Clip()
        dlg=None
        mw=FreeCADGui.getMainWindow()
        dws=mw.findChildren(QtGui.QDockWidget)
        for dw in dws:
            if dw.windowTitle()=="Clip":
                dlg=dw
                dlg.hideObjects()
                dlg.show()
                break
        if dlg==None:
            dlg=ClipDlg.Clip()
            mw.addDockWidget(QtCore.Qt.DockWidgetArea.RightDockWidgetArea,dlg)
            dlg.show()
        # 找到property view面板
        dwPropertyView=mw.findChild(QtGui.QDockWidget, 'Property view')
        if dwPropertyView:
            mw.tabifyDockWidget(dlg,dwPropertyView)
            dlg.raise_()
        # dlg.setModal(False)
        
        # dlg.exec_()
        # dlg.exec_()
        
        # resultDlg=dlg.result()
        # if not resultDlg==1:
        #     dlg.

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling3D/Modeling3DResources/_Operation_Clip.svg"
        # IconPath=""
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'Clip',
            'Clip')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'Clip',
            'Clip Model')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('Clip',ClipCommand())