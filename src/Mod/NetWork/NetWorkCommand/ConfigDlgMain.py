#-*- coding: utf-8 -*-
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')

import json
import re
import codecs
import FreeCAD
import PySide
from PySide import QtGui,QtCore
import ConfigParser
from NetWorkGui import ConfigDlg
# from Modeling.Common.CommonCommand.NewDocument import ObjectDict
# import ProjectSettingCommand
# from ProjectSettingsDlgData import ProjectSettingsDlgData as DlgData
# import ProjectSettingsDlgData
# from Modeling.Common.Tools import CoordinateSystemTools

# import File.FileCommand.M3DFile.M3DFileUtil
# import File.FileCommand.TextUI.FileTextView

SETTING="setting"
IP="ip"
PORT="port"
WORKPATH="workpath"
class Config(QtGui.QDialog):
    def __init__(self,className):
        QtGui.QDialog.__init__(self)
        self.ui = ConfigDlg.Ui_Dialog_ConfigDlg()
        self.ui.setupUi(self)

        self.close()
        self.ui.pushButton_ok.clicked.connect(self.onOKBtnClicked)
        self.ui.pushButton_cancel.clicked.connect(self.onCancelBtnClicked)
        self.ui.pushBtn_chooseWorkPath.clicked.connect(self.onChooseFileBtnClicked)
        self.ui.lineEdit_IPAddress.setText(str(FreeCAD.clientGetServerIP()))   
        self.ui.lineEdit_Port.setText(str(self.getPort()))
        self.ui.lineEdit_WorkPath.setText(self.getWorkPath())
        # x=FreeCAD.clientGetWorkpath()
        # FreeCAD.Console.PrintMessage(x)
        # FreeCAD.Console.PrintMessage(x.decode("gbk"))
        # self.ui.lineEdit_WorkPath.setText(FreeCAD.clientGetWorkpath().decode("gbk"))

        

    def onOKBtnClicked(self):
        ipAddress=self.ui.lineEdit_IPAddress.text()
        port=self.ui.lineEdit_Port.text()
        uiWorkPath=self.ui.lineEdit_WorkPath.text()
        FreeCAD.Console.PrintMessage("uiWorkPath: ")
        FreeCAD.Console.PrintMessage(uiWorkPath)
        FreeCAD.Console.PrintMessage("uiWorkPath: \n")

        if re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$').match(str(ipAddress)):
            self.setIPAddress(ipAddress)
            self.setPort(port)
            self.setWorkPath(uiWorkPath)
            self.close()
        else:
            import Modeling
            Modeling.Common.Tools.DocumentTools.errorMessage(u"ip输入有误，请重新输入！")

        # config=ConfigParser.ConfigParser()
        # config.readfp(open(str(FreeCAD.getHomePath())+"bin/config.ini"))
        # config.set(SETTING,IP,str(ipAddress))
        # config.write(open(str(FreeCAD.getHomePath())+"bin/config.ini","r+"))
        
        # FreeCAD.clientSetServerIP(ipAddress)
        
    def onCancelBtnClicked(self):  
        self.close()
        pass

    def onChooseFileBtnClicked(self):
        filePath=PySide.QtGui.QFileDialog.getExistingDirectory() 
        self.ui.lineEdit_WorkPath.setText(filePath)

    def setWorkPath(self,uiWorkPath):

        config=ConfigParser.ConfigParser()
        config.readfp(open(str(FreeCAD.getHomePath())+"bin/config.ini"))
        
        import os
        # 如不存在新建
        if not os.path.exists(uiWorkPath):
            try: 
                os.makedirs(uiWorkPath)
            except:
                QtGui.QMessageBox.information(None,"Error","Invalid WorkPath")
                # openConfigDialog()
                print FreeCAD.Console.PrintMessage("无效工作路径，请重新输入\n")
        if not config.has_section(SETTING):
            config.add_section(SETTING)
        config.set(SETTING,WORKPATH,uiWorkPath)
        config.write(open(str(FreeCAD.getHomePath())+"bin/config.ini","w+"))
        FreeCAD.clientSetWorkpath(uiWorkPath)
        FreeCAD.Console.PrintMessage("END")

    def getWorkPath(self):
        workpath=FreeCAD.clientGetWorkpath()
        if workpath=="":
            config=ConfigParser.ConfigParser()
            config.readfp(open(str(FreeCAD.getHomePath())+"bin/config.ini"))
            if not config.has_section(SETTING):
                config.add_section(SETTING)
                config.set(SETTING,WORKPATH,"E:\\PICGUIC")
            else:
                if not config.has_option(SETTING,WORKPATH):
                    config.set(SETTING,WORKPATH,"E:\\PICGUIC")
            workpath=config.get(SETTING,WORKPATH)
        # worktest=worktest.decode("gbk").encode("utf-8")
        return unicode(workpath,"utf8")
    def getIPAddress(self):
        config=ConfigParser.ConfigParser()
        config.readfp(open(str(FreeCAD.getHomePath())+"bin/config.ini"))
        if config.has_section(SETTING):
            if  config.has_option(SETTING,IP):
                pass
            else:
                # 缺省默认
                config.set(SETTING,IP,"127.0.0.1")
                pass
        else:
            config.add_section(SETTING)
            config.set(SETTING,IP,"127.0.0.1")
            pass
        ipAddress=config.get(SETTING,IP)
        return str(ipAddress)
    def getPort(self):
        config=ConfigParser.ConfigParser()
        config.readfp(open(str(FreeCAD.getHomePath())+"bin/config.ini"))
        if not config.has_section(SETTING):
            config.add_section(SETTING)
            config.set(SETTING,PORT,"3200")
        else:
            if not config.has_option(SETTING,PORT):
                config.set(SETTING,PORT,"3200")
        port=config.get(SETTING,PORT)
        return str(port)
    def setIPAddress(self,ipAddress):
        config=ConfigParser.ConfigParser()
        config.readfp(open(str(FreeCAD.getHomePath())+"bin/config.ini"))
        if not config.has_section(SETTING):
            config.add_section(SETTING)
        config.set(SETTING,IP,str(ipAddress))
        config.write(open(str(FreeCAD.getHomePath())+"bin/config.ini","w+"))
        FreeCAD.clientSetServerIP(ipAddress)
    def setPort(self,port):
        config=ConfigParser.ConfigParser()
        config.readfp(open(str(FreeCAD.getHomePath())+"bin/config.ini"))
        if not config.has_section(SETTING):
            config.add_section(SETTING)
        config.set(SETTING,PORT,str(port))
        config.write(open(str(FreeCAD.getHomePath())+"bin/config.ini","w+"))


def openConfigDialog():
    dlg=Config("ConfigDlg")
    dlg.show()
    dlg.exec_()
    pass