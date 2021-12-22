# -*- coding: UTF-8 -*-

import FreeCAD
import FreeCADGui
from PySide import QtGui, QtCore
from Modeling.Common.Tools import UnitTools
from File.FileCommand.M3DFile import M3DFileUtil
import PhysicsGui.BatchDlg
import re
from functools import reduce
import os
import time

# 状态值
isBatchRunning=False
requestStopRunning=False
successfullyFinished=False

def sayz(msg):
    FreeCAD.Console.PrintMessage(str(msg)+"\n")

def sayd(msg, title=""):
    QtGui.QMessageBox.information(None, title, msg)

class BatchMain(QtGui.QDialog):
    # 单例，防止创建多个批处理窗口
    __instance=None
    __initFlag=False

    sendNext=QtCore.Signal() # 信号：成功接收到h5，发送下一个M3D文件
    errorOccured=QtCore.Signal(str) # 信号：发生错误

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance=super(BatchMain, cls).__new__(cls, args, kwargs)
        return cls.__instance

    def __init__(self, parent=None):
        if self.__initFlag:
            return
        self.__initFlag=True
        super(BatchMain, self).__init__(parent)
        self.ui = PhysicsGui.BatchDlg.Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowMinimizeButtonHint)

        self.resize(1100, 700)

        self.ui.pushButton_start.clicked.connect(self.onStartBtn)
        self.ui.pushButton_cancel.clicked.connect(self.onCancel)
        self.ui.pushButton_help.clicked.connect(self.onHelp)

        # 定义M3D文件输出路径
        self.path_temp = FreeCAD.clientWorkpath() + FreeCAD.ActiveDocument.Label.encode("gbk") + "_batch_temp.m3d" # to be deleted
        self.path = FreeCAD.clientWorkpath() + FreeCAD.ActiveDocument.Label.encode("gbk") + "_batch.m3d"
        # 用于生成原始M3D文件
        self.m3dFileUtil = M3DFileUtil.M3DFileUtil(commandsManager=[], path=self.path_temp, coordinateSystem="R")
        # self.customParamTools = DlgCustomParameterMain.CustomeParameterMain()

        self.refreshText()

        self.currentM3DText = self.m3dFileUtil.getLatestM3DFileStr()
        self.newM3DText = ""


        # 这里强制访问了M3DFileUtil中的私有类……
        # strInit_parameter = M3DFileUtil.M3DFileUtil._M3DFileUtil__StrInit.strParameter
        # strInit_definedObjects = M3DFileUtil.M3DFileUtil._M3DFileUtil__StrInit.strDefineObjects
        StrInitClass=self.m3dFileUtil.getStrInit()
        strInit_parameter = StrInitClass.strParameter
        strInit_definedObjects = StrInitClass.strDefineObjects
        self.textParams_startPos = self.currentM3DText.find(strInit_parameter) + len(strInit_parameter)
        self.textParams_endPos = self.currentM3DText.find(strInit_definedObjects)

        # 字符串处理范围限制在Parameters这个范围
        self.textBeforeParams_current=self.currentM3DText[:self.textParams_startPos]
        self.textParams_current=self.currentM3DText[self.textParams_startPos:self.textParams_endPos]
        self.textAfterParams_current=self.currentM3DText[self.textParams_endPos:]

        
        self.textParams_new=self.textParams_current

        self.combinations=[]
        self.combinations_index=[]

        self.nameList = []
        self.valueList = []

        self.nameList_current=[]
        self.valueList_current=[]

        self.sendNext.connect(self.newComb)
        self.errorOccured.connect(self.error)

        self.errorFlag = False

        #批处理控制对象
        from Control.controlCommand import TaskControlMain
        self.batchControl=TaskControlMain.BatchControl(self.path)
        # objs = FreeCAD.ActiveDocument.Objects
        # self.paramObj = None
        # for o in objs:
        #     if hasattr(o, "DynamicData"):
        #         self.paramObj = o

        # if self.paramObj is not None:
        #     propertiesList = self.paramObj.DynamicData

    # 重新显示窗口时刷新原M3D文件
    def showNormal(self):
        super(BatchMain, self).showNormal()

        global isBatchRunning
        if isBatchRunning or not self.__initFlag:
            return

        self.refreshText()

        StrInitClass=self.m3dFileUtil.getStrInit()
        strInit_parameter = StrInitClass.strParameter
        strInit_definedObjects = StrInitClass.strDefineObjects
        self.textParams_startPos = self.currentM3DText.find(strInit_parameter) + len(strInit_parameter)
        self.textParams_endPos = self.currentM3DText.find(strInit_definedObjects)

        # 字符串处理范围限制在Parameters这个范围
        self.textBeforeParams_current=self.currentM3DText[:self.textParams_startPos]
        self.textParams_current=self.currentM3DText[self.textParams_startPos:self.textParams_endPos]
        self.textAfterParams_current=self.currentM3DText[self.textParams_endPos:]


    def refreshText(self):
        self.ui.textEdit_original.setText(self.m3dFileUtil.getLatestM3DFileStr())
        self.currentM3DText = self.m3dFileUtil.getLatestM3DFileStr()

    def onHelp(self):
        QtGui.QMessageBox.information(self, u"帮助", u"格式：\n"
                                                   u"[参数名1]=[值序列1];\n"
                                                   u"[参数名2]=[值序列2];\n"
                                                   u"参数名是原M3D文件PARAMETER片段中定义的参数名；\n"
                                                   u"值序列中使用英文逗号隔开每个值；\n"
                                                   u"每个值序列后请务必加上英文分号。\n\n"
                                                   u"示例：\n"
                                                   u"px=10mm,20mm,50mm;\n"
                                                   u"t=20ms,35ms;")
        # self.sendNext.emit()

    def closeEvent(self, e):
        if not self.onCancel():
            e.ignore()

    # 正常关闭时删除之前的单例
    def close(self, *args, **kwargs):
        # 这里必须用类名，不能用self，也不可以del
        BatchMain.__instance=None
        BatchMain.__initFlag=False
        super(BatchMain, self).close()

    def onCancel(self):
        global isBatchRunning
        global requestStopRunning
        if isBatchRunning:
            self.onStop()
            # if requestStopRunning:
            #     self.close()
            return False
        else:
            self.close()
            return True

    def onStartBtn(self):
        global isBatchRunning
        if not isBatchRunning:
            self.onStart()
        else:
            self.onStop()

    def onStop(self):
        global isBatchRunning, requestStopRunning
        if not requestStopRunning:
            r=QtGui.QMessageBox.question(self,u"停止批处理",u"确认停止批处理？",buttons=QtGui.QMessageBox.Yes|QtGui.QMessageBox.No)
            if r==QtGui.QMessageBox.Yes:
                requestStopRunning=True
                isBatchRunning=False
                # 防止批处理终止时意外启动新模拟
                if not self.errorFlag:
                    self.batchControl.taskControl.onRun()
                # self.ui.pushButton_start.setEnabled(False)
                # self.setStatusInfo(self.getStatusInfo()+u"\n正在等待当前任务完成……")
                self.close()

    def onStart(self):
        # original = '''!Comment
        # !
        # px = 30mm;
        # ps = 20v;
        # pr = 70.00512ms;
        # pg = 10kv;
        # '''
        # text = '''!!Comment!
        # !px=70mm,20mm,90m;
        # px=8mm,5mm,6m,7mm,70mm,20mm,90m;
        # ps=800ms,5s;
        # pr=9m;
        # pg=90v,60kv;
        # '''

        text = self.ui.textEdit_params.toPlainText() + ";"
        # 去掉注释行
        text = re.sub(r"[!！][^\n]*", "", text)
        # 去空格和换行符
        text = re.sub(r"[ \n]", "", text)
        # print text
        
        # 找无效字符，除数字 下划线 小数点和运算符之外的字符
        invalidChars=re.findall(r"[^\w\.\+\-\*\/\(\)\=\,\;]",text)
        # QtGui.QMessageBox.information(self, u"", "invalidChars="+str(invalidChars))
        if len(invalidChars)!=0:
            QtGui.QMessageBox.information(self, u"无效字符", "错误: 无效字符 \""+str(invalidChars[0])+"\"")
            return

        self.errorFlag = False

        self.getCurrentParameters()

        self.nameList=[]
        self.valueList=[]
        # 拆分变量名和值
        it = re.finditer(r"(.+?)=(.+?);", text)
        for i in it:
            groups=i.groups()
            name=groups[0]
            index_current=self.indexInList(name, self.nameList_current)
            # QtGui.QMessageBox.information(self, u"", "name=" + name + "self.nameList_current=" + str(self.nameList_current))

            if self.indexInList(name, self.nameList)!=-1:
                QtGui.QMessageBox.information(self, u"变量重复出现", "错误: 变量 \"" + name + "\" 重复出现！请合并变量的值")
                return
            elif index_current==-1:
                QtGui.QMessageBox.information(self, u"没有预先定义的变量", "错误: 全局变量 \"" + name + "\" 没有预先定义！请使用自定义参数功能预先定义")
                return
                
            values = groups[1].split(",")
            currentValue = self.valueList_current[index_current]
            currentUnitType = UnitTools.getTypeOfData(currentValue)
            for v in values:
                newUnitType = UnitTools.getTypeOfData(v)
                # QtGui.QMessageBox.information(self, "", "v="+v+"values="+str(values))
                if newUnitType != currentUnitType:
                    QtGui.QMessageBox.information(self, u"值类型不一致", "错误: 给变量 \"" + name + "\" 赋的值 "+ v + " 与变量原来的值 " + currentValue + " 类型不一致")
                    return
            
            self.nameList.append(name)
            self.valueList.append(groups[1].split(","))

        if len(self.nameList)==0:
            QtGui.QMessageBox.warning(self, u"错误", u"没有检测到有效的参数定义，请重新检查")
            return
        
        # 生成所有参数组合
        self.makeCombinations()

        # 临时文件名列表，用于批处理后删除文件
        self.pathList=[]

        global isBatchRunning, requestStopRunning, successfullyFinished
        isBatchRunning=True
        requestStopRunning=False
        successfullyFinished=False
        self.ui.pushButton_start.setText(u"停止")


        # 开始批处理
        self.nowComb_index=-1 # 不可设为0

        self.newComb()

        # import thread
        # sayz("before create new thread\n")
        # thread.start_new_thread(monitor, (self, self.ui))
        # sayz("after create new thread\n")

        # self.nowComb_index=0
        # while self.nowComb_index<len(self.combinations):
        #     sayz("before emit\nnow self.nowComb_index="+str(self.nowComb_index)+"\n")
        #     self.sendNext.emit()
        #     sayz("after emit\nnow self.nowComb_index="+str(self.nowComb_index)+"\n")
        #     self.nowComb_index+=1


    def resetStatus(self):
        global isBatchRunning, requestStopRunning
        # 删除之前产生的M3D文件
        try:
            for p in self.pathList:
                os.remove(p)
        except OSError:
            QtGui.QMessageBox.warning(self, u"临时文件删除失败", u"没有成功删除所有临时文件，请尝试到 "
                                      + FreeCAD.clientWorkpath() + u" 下手动删除")

        requestStopRunning = False
        isBatchRunning = False
        self.ui.pushButton_start.setText(u"开始")
        self.ui.pushButton_start.setEnabled(True)

    def error(self, errorMsg):
        self.resetStatus()
        self.setStatusInfo(self.getStatusInfo()+"\n"+errorMsg)
        self.errorFlag = True


    def newComb(self):
        global isBatchRunning, requestStopRunning, successfullyFinished

        self.nowComb_index+=1

        # 如果批处理没有在运行，直接忽略该信号
        if not isBatchRunning:
            return

        if requestStopRunning:
            # 批处理被用户终止后的操作

            self.resetStatus()
            successfullyFinished=False
            self.setStatusInfo(self.getStatusInfo()+"\n批处理被用户终止")
            return

        if self.nowComb_index>=len(self.combinations):
            # 批处理成功完成后的操作

            self.resetStatus()

            successfullyFinished=True
            self.setStatusInfo(self.getStatusInfo()+"\n批处理成功完成！")
            from Control.controlCommand import TaskControlMain
            self.batchControl.batchState=TaskControlMain.BatchState.NotStart
            return


        # 使用一个参数组合修改参数
        self.modifyParams(self.nameList, self.combinations[self.nowComb_index])

        # 生成M3D文本
        self.getNewM3DText()

        # 构造文件名
        suffix=""
        for j in range(len(self.nameList)):
            suffix+=self.nameList[j]+self.combinations_index[self.nowComb_index][j]+"_"
        self.path = FreeCAD.clientWorkpath() + FreeCAD.ActiveDocument.Label.encode("gbk") + "-" + suffix[:-1] + ".m3d"
        self.pathList.append(self.path)

        # 写入到文件
        self.writeToFile()

        # 在下方文本框显示状态信息
        msg="正在处理第 " + str(self.nowComb_index + 1) + " 组参数 (共 " + str(len(self.combinations)) + " 组)……\n"
        msg+="参数设置：\n"
        for j in range(len(self.nameList)):
            msg+=self.nameList[j]+" = "+self.combinations[self.nowComb_index][j]+"\n"
        # r=QtGui.QMessageBox.information(self, "New M3D File", msg, buttons=QtGui.QMessageBox.Ok|QtGui.QMessageBox.Abort)
        self.setStatusInfo(msg)

        ######### 发送到服务端等操作
        # 不需要sleep！
        # time.sleep(1)
        self.batchControl.pathFile=self.path
        self.batchControl.run()
        ############################


    def setStatusInfo(self, info):
        self.ui.textEdit_statusInfo.setPlainText(info)

    def getStatusInfo(self):
        return self.ui.textEdit_statusInfo.toPlainText()


    def getNewM3DText(self):
        '''
        生成新的M3D文本
        '''
        self.newM3DText=self.textBeforeParams_current + self.textParams_new + self.textAfterParams_current
        # self.ui.textEdit_new.setText("New:\n"+self.newM3DText)

        return self.newM3DText

    def writeToFile(self):
        try:
            fo = open(self.path, "w+")
            fo.write(self.newM3DText.encode("UTF-8"))
            fo.close()
            # QtGui.QMessageBox.information(self, u"写出文件成功", u"文件已写到 "+self.path)
        except:
            QtGui.QMessageBox.critical(self, u"写入文件失败", u"无法将文件写入 "+self.path)



    # def modifyParam(self, paramName, newValue):
        
    #     if isinstance(newValue, int):
    #         newValue = str(newValue)
    #     regex = re.compile(r"(?<=^" + paramName + r" = ).+?(?=;)", flags=re.M)
        
    #     self.textParams_new = regex.sub(newValue, self.textParams_new) # 可以只替换一次

    def modifyParams(self, paramNameList, newValueList):
        for i in range(len(paramNameList)):
            self.textParams_new=re.sub(r"(?<=^" + paramNameList[i] + r" = ).+?(?=;)", newValueList[i], self.textParams_new, flags=re.M|re.I)


    def makeCombinations(self):
        '''
        根据self.valueList生成参数组合
        '''
        indexes=[]
        for i in range(len(self.valueList)):
            temp_index=[]
            for j in range(len(self.valueList[i])):
                temp_index.append(str(j+1)) # 序号从1开始
            indexes.append(temp_index)

        # QtGui.QMessageBox.information(self, "", "before reduce, values=\n"+str(values))
        combList=reduce(self.comb_recur, self.valueList)
        combList_index=reduce(self.comb_recur, indexes)
        self.combinations=[s.split(",") for s in combList]
        self.combinations_index=[s.split(",") for s in combList_index]

    def comb_recur(self, list1, list2):
        return [i+","+j for i in list1 for j in list2]


    def getCurrentParameters(self):
        '''
        读取原来M3D文件中的变量和值
        '''

        # 去掉注释行
        self.textParams_current = re.sub(r"[!！][^\n]*", "", self.textParams_current)
        # 去空格和换行符
        self.textParams_current = re.sub(r"[ \n]", "", self.textParams_current)

        self.nameList_current=[]
        self.valueList_current=[]
        # 拆分变量名和值，如果M3D文本格式改变会出错！
        it = re.finditer(r"(.+?)=(.+?);", self.textParams_current)
        for i in it:
            groups=i.groups()
            if self.indexInList(groups[0], self.nameList_current)!=-1:
                QtGui.QMessageBox.warning(self,u"from getCurrentParameters", u"原M3D文件中有重复定义的全局变量")
            self.nameList_current.append(groups[0])
            self.valueList_current.append(groups[1])

    def indexInList(self, str, list):
        '''
        不区分大小写的搜索，返回找到的第一个索引值，找不到返回-1
        :param str: 参数
        :param list: 列表
        :return: int
        '''
        for i in range(len(list)):
            if list[i].lower()==str.lower():
                return i
        return -1

# def monitor(obj, objui):
#     ################# 假设有这些信号
#     finish=True
#     BatchState=0
#     #################
#     global requestStopRunning, isBatchRunning
#
#     while True:
#         if finish:
#             # if obj.nowComb_index<len(obj.combinations):
#             sayd(str(obj.nowComb_index))
#             if obj.nowComb_index<5:
#                 sayd("inside")
#
#                 obj.nowComb_index+=1
#                 obj.newComb()
#                 sayd("now: "+str(obj.nowComb_index))
#                 # 当前文件计算完毕后才判断是否要停止
#                 if requestStopRunning:
#                     BatchState=3
#                     obj.setStatusInfo("批处理被用户终止")
#
#                     break
#             else:
#                 obj.setStatusInfo(objui.textEdit_statusInfo.toPlainText() + "\n批处理成功完成！")
#                 break




