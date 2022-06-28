# -*- coding: utf-8 -*-
import FreeCAD
import FreeCADGui as Gui
import re
import time, thread
import CoordinateSystemTools,ObjectsTools
import Modeling
import ObjectsTools
# from Modeling.Modeling2D.Tools import InitDoc
from ProjectSetting.Tools import ProjectSettingsTools
import UnitTools
import time
from PySide import QtGui, QtCore
from PySide.QtGui import QApplication, QMainWindow, QDockWidget, QTreeWidgetItem


def sayz(msg):
    FreeCAD.Console.PrintMessage("\n")
    FreeCAD.Console.PrintMessage(msg)
    FreeCAD.Console.PrintMessage("\n")
def sayzError(msg):
    FreeCAD.Console.PrintMessage("\n")
    FreeCAD.Console.PrintError(msg)
    FreeCAD.Console.PrintMessage("\n")

# 与建模无关的属性
propsNotThingWithModeling=["X","Y","Z","R","Theta","X_Value","Y_Value","Z_Value","R_Value","Theta_Value",\
                            "Type","Proxy","ConductivitySIGMA","ConductivitySIGMAValue","RelativeDielectricConstant",\
                            "SetEPS","SetEPS2","SetEPS3","Label","Group","flagRedrawvalue","Shape","Axis","Placement"]

# 上一次自动刷新的模型列表
global lastObjsList
lastObjsList=[]
# 改变的模型,可能改变了多个模型：Order改变时或者ParamObj改变与之改变属性有关系的模型都会改变
# {obj:prop,...},不用字典
changedObjsAndProps={}

global changedObjs
changedObj=[]
# 改变的属性，可能改变了多个属性
global changedProps
changedProp=[]
######################################################init document when create##############################
# 初始化文档
def initDocument(doc):
    ''' 
    author:   @fubiao
    @ doc :   document
    @ return: void
    function: 0、新增结果对象；
              1、为文档增加监听；
              2、将默认的json加到comment中；
              3、添加默认定时器
    '''
    #新增结果object
    obj=ObjectsTools.initResultIbj(doc)

    #监听
    # obs=DocumentObservers()
    FreeCAD.addDocumentObserver(DocumentObservers()) 

    FreeCAD.addDocumentObserver(TransparencyObserver())

    #测试
    # FreeCAD.addDocumentObserver(NeedsRecomputeObserver())
    #新增加json文件到comment中去
    ProjectSettingsTools.initPrjectSettings()

    #添加默认定时器
    #init TimerDef
    from Modeling.Common.CommonCommand.NewDocument import ObjectDict
    from Physics.PhysicsCommand.DefaultTimerDlgMain import DefaultTimerMain

    ObjectDict["TimerDef1"] = DefaultTimerMain("new","TimerDef1")
    ObjectDict["TimerDef1"].initToDoc()
    #end
    #初始化分组创建
    ObjectsTools.initGroup()
    # 新建3D,弹出工作区间对话框
    import FreeCADGui
    FreeCADGui.runCommand("WorkSpaceSettings")
    FreeCADGui.runCommand("TimeDomainComputingMenu")

# 初始化参量对象，这个不能直接加载initDocument中，因为解析时，也会执行上面的函数，报错
def initParamObj(doc):
    if doc.CoordinateSystem==CoordinateSystemTools.CoordinateType.Rectangular:
        ObjectsTools.setDX1DX2DX3("1mm","1mm","1mm")
    elif doc.CoordinateSystem==CoordinateSystemTools.CoordinateType.Polar:
        ObjectsTools.setDX1DX2DX3("1mm","30deg","1mm")
    elif doc.CoordinateSystem==CoordinateSystemTools.CoordinateType.Cylindrical:
        ObjectsTools.setDX1DX2DX3("1mm","1mm","30deg")

def finalSettingByRebuildByM3d():
    Gui.doCommand("from Modeling.Common.Tools import DocumentTools")
    FreeCAD.ActiveDocument.flagNeedUpdateBoolean=0
    updateBoolean()
    # FreeCAD.addDocumentObserver(AfterReBuildByM3dObserver())
    FreeCAD.addDocumentObserver(NeedsRecomputeObserver())

def otherDocInit():
    doc=FreeCAD.ActiveDocument
    initDocument(doc)
    initParamObj(doc)
    Gui.doCommand("from Modeling.Common.Tools import DocumentTools")
    # FreeCAD.addDocumentObserver(AfterReBuildByM3dObserver())
    FreeCAD.addDocumentObserver(NeedsRecomputeObserver())
    # # 切换一下工作台，刷新建模部分的图标 by pingyue
    # nowWorkbenchText=Gui.activeWorkbench().name()
    # Gui.activateWorkbench("Modeling2DWorkbench")
    # Gui.activateWorkbench("Modeling3DWorkbench")
    # Gui.activateWorkbench(nowWorkbenchText)

def initWhenOpenFCStdFile():
    if FreeCAD.ActiveDocument.Comment == "2D":
        sayz("当前工程为2D相关工程，进行文件初始化，添加必要监视器")
        FreeCAD.addDocumentObserver(Modeling.Modeling2D.Tools.InitDoc.DocumentObservers())
        # 如果当前工程没有对应的M2D显示界面则创建一个新的
        Gui.runCommand("CreateM2D")
        Modeling.Modeling2D.Modeling2DCommand.Grid.GridCommand.showGrid()
    elif FreeCAD.ActiveDocument.Comment == "new3D":
        sayz("当前工程为3D相关工程，进行文件初始化，添加必要监视器")
        from Model3D.Tools import InitDoc3D
        FreeCAD.addDocumentObserver(InitDoc3D.DocumentObservers())
        # 如果当前工程没有对应的M2D显示界面则创建一个新的
        Gui.runCommand("CreateM3D_new")
        # Modeling.Modeling2D.Modeling2DCommand.Grid.GridCommand.showGrid()
    else:
        Gui.doCommand("import Modeling")
        Gui.doCommand("FreeCAD.addDocumentObserver(Modeling.Common.Tools.DocumentTools.DocumentObservers())")
        Gui.doCommand("FreeCAD.addDocumentObserver(Modeling.Common.Tools.DocumentTools.TransparencyObserver())")
        Gui.doCommand("from Modeling.Common.Tools import DocumentTools")
        # FreeCAD.addDocumentObserver(AfterReBuildByM3dObserver())
        FreeCAD.addDocumentObserver(NeedsRecomputeObserver())
        updateBoolean()
        # 现在初始界面是Start，这个可以不用了@fubiao
        # # 切换一下工作台，刷新建模部分的图标 by pingyue
        # nowWorkbenchText=Gui.activeWorkbench().name()
        # Gui.activateWorkbench("Modeling2DWorkbench")
        # Gui.activateWorkbench("Modeling3DWorkbench")
        # Gui.activateWorkbench(nowWorkbenchText)
        # 如果LicenseURL等于emptyLIST,需要重置LicenseURL，来清空LIST
    FreeCAD.Console.PrintMessage(FreeCAD.ActiveDocument.LicenseURL)
    try:
        if FreeCAD.ActiveDocument.LicenseURL == "emptyLIST":
            FreeCAD.ActiveDocument.LicenseURL = "clearLIST"
            # FreeCAD.Console.PrintMessage(FreeCAD.ActiveDocument.LicenseURL)
    except:
        FreeCAD.Console.PrintMessage("此时没有激活的工程，是直接打开绘图3，不需要重置emptyLIST")


# 事件监听器
##########################定义一个监测类，当对象删除或者创建时执行相应的动作#########
class DocumentObservers(object):
    def __init__(self):
        pass

    def slotDeletedObject(self,obj):
        FreeCAD.Console.PrintError("obs测试: "+str(obj.Label)+"\n")
        #为所有的物体重新编号
        if ObjectsTools.hasThePropertyByObj(obj,"Order"):
            for index in range(obj.Order+1,ObjectsTools.getNumOfObjects(FreeCAD.ActiveDocument.Name)):
                objs=ObjectsTools.getListOfOrderedObjects(FreeCAD.ActiveDocument.Name)
                objs[index].Order=objs[index].Order-1
        if ObjectsTools.hasThePropertyByObj(obj,"Type"):
            # 删除阵列体基本对象的操作应该放在事务中，否则会导致撤销异常
            # 该操作已经移动到了C++部分的StdCmdDelete中 @pingyue
            # """
            # start
            # add by chenjian
            # 删除循环体的同时删除其基本对象
            # """
            # if obj.Type == ObjectsTools.ObjectType.Vol_Array:
            #     baseObj = obj.Base
            #     if baseObj:
            #         FreeCAD.activeDocument().removeObject(baseObj.Name)
            #         FreeCAD.activeDocument().recompute()
            # """
            # end
            # """

            #用于更新Vol_Extruded的属性
            if obj.Type[0]=="L" :
                objs=ObjectsTools.getAllObjectsByTypes(FreeCAD.ActiveDocument.Name,[ObjectsTools.ObjectType.Vol_Extruded])
                if len(objs):
                    for objItem in objs:
                        lineCur=str(objItem.Line)
                        lineList=ObjectsTools.getLinesByDoc(FreeCAD.ActiveDocument)
                        lineList.remove(str(obj.Label))
                        objItem.Line=lineList
                        if str(obj.Label)!=lineCur:
                            objItem.Line=lineCur
                        # if objItem.
                        # line=objItem.Line
                        # if line in lineList:
                        #     objItem.Line=lineList
                        #     objItem.Line=
                        
            elif obj.Type[0:3]=="Are":
                objs=ObjectsTools.getAllObjectsByTypes(FreeCAD.ActiveDocument.Name,
                                                       [ObjectsTools.ObjectType.Vol_Extruded,
                                                       ObjectsTools.ObjectType.Vol_Revolution,
                                                       ObjectsTools.ObjectType.Vol_Draft_Extrude,
                                                       ObjectsTools.ObjectType.Vol_Draft_Revolution])
                if len(objs):
                    for objItem in objs:
                        areaCur=str(objItem.Area)
                        areaList=ObjectsTools.getAreasByDoc(FreeCAD.ActiveDocument)
                        areaList.remove(str(objItem.Label))
                        objItem.Area=areaList
                        if str(obj.Label)!=areaCur:
                            objItem.Area=areaCur
            #
            else:
                pass


    def slotChangedObject(self,obj,prop):
        # FreeCAD.Console.PrintMessage("slotChangedObject "+str(obj.Name)+" prop"+str(prop)+"\n")
        # if obj.TypeId=="App::DocumentObjectGroup":
        # self.recomputeObj(obj,prop)
        ##############################对挤出体参数的更新#########################
        # Type发生改变，只能是新增，不会一直变
        # FreeCAD.Console.PrintMessage("objName: "+str(obj.Name)+"  prop: "+str(prop)+"  value: "+str(getattr(obj,prop))+"\n")
        if prop=="Type":
            # if ObjectsTools.hasThePropertyByObj(obj,"Label") :
            #     if obj.Type[0]=="L":
            #     #找到文档中所有的需要对Line或者Area更新的地方：Vol_Extruded
            #         objs=ObjectsTools.getAllObjectsByTypes(FreeCAD.ActiveDocument.Name,[ObjectsTools.ObjectType.Vol_Extruded])
            #         if len(objs):
            #             for objItem in objs:
            #                 FreeCAD.Console.PrintMessage("TEST\n")
            #                 FreeCAD.Console.PrintMessage("objItem.Line1 "+str(objItem.Line)+"\n")
            #                 lineCur=str(objItem.Line)
            #                 linesList=ObjectsTools.getLinesByDoc(FreeCAD.ActiveDocument)
            #                 FreeCAD.Console.PrintMessage("linesList 1 "+str(linesList)+"\n")
            #                 linesList.remove(lineCur)
            #                 linesList.insert(0,lineCur)

            #                 FreeCAD.Console.PrintMessage("linesList 2 "+str(linesList)+"\n")

            #                 objItem.Line=linesList
            #                 FreeCAD.Console.PrintMessage("objItem.Line2 "+str(objItem.Line)+"\n")
            #     elif obj.Type[0:3]=="Are":
            #         objs=ObjectsTools.getAllObjectsByTypes(FreeCAD.ActiveDocument.Name,[ObjectsTools.ObjectType.Vol_Extruded,ObjectsTools.ObjectType.Vol_Draft_Extrude])
            #         if len(objs):
            #             for objItem in objs:
            #                 objItem.Area=ObjectsTools.getAreasByDoc(FreeCAD.ActiveDocument)
            #FreeCAD.ActiveDocument.recompute()
            # 如果group为空，则对它进行分组
            if obj.getParentGroup()==None:
                ObjectsTools.addTheirGroupForObj(obj)
                pass

        if prop=="Label":
            if ObjectsTools.hasThePropertyByObj(obj,"Type") :
                if obj.Type[0]=="L":
                    objs=ObjectsTools.getAllObjectsByTypes(FreeCAD.ActiveDocument.Name,[ObjectsTools.ObjectType.Vol_Extruded])
                    if len(objs):
                        for objItem in objs:
                            # 记录当前这个三维体的Line属性的值
                            lineCur=str(objItem.Line)
                            linesList=ObjectsTools.getLinesByDoc(FreeCAD.ActiveDocument)
                            objItem.Line=linesList
                            try:
                                # 将保存的属性值重新赋值
                                objItem.Line=lineCur
                            except:
                                lineCur=str(obj.Label)
                                objItem.Line=lineCur
                                FreeCAD.Console.PrintError("areaCureObj "+str(lineCur)+"\n") 
                            #跳过刷新
                            objItem.purgeTouched()                               
                elif obj.Type[0:3]=="Are":
                    objs=ObjectsTools.getAllObjectsByTypes(FreeCAD.ActiveDocument.Name,
                                                          [ObjectsTools.ObjectType.Vol_Extruded,
                                                          ObjectsTools.ObjectType.Vol_Revolution,
                                                          ObjectsTools.ObjectType.Vol_Draft_Extrude,
                                                          ObjectsTools.ObjectType.Vol_Draft_Revolution])
                    if len(objs):
                        for objItem in objs:
                            areaCur=str(objItem.Area)
                            objItem.Area=ObjectsTools.getAreasByDoc(FreeCAD.ActiveDocument)
                            #这里使用trycatch，如果当前objItem中有个属性是obj，会出错
                            try:
                                objItem.Area=areaCur
                            except:
                                areaCur=str(obj.Label)
                                objItem.Area=areaCur
                                FreeCAD.Console.PrintError("areaCureObj "+str(areaCur)+"\n")
                            #跳过刷新
                            objItem.purgeTouched()
        #如果是对线或者面的形状进行了改变
        if prop=="Shape":
            if ObjectsTools.hasThePropertyByObj(obj,"Type") :
                if obj.Type[0]=="L":
                    objs=ObjectsTools.getAllObjectsByTypes(FreeCAD.ActiveDocument.Name,[ObjectsTools.ObjectType.Vol_Extruded])
                    if len(objs):
                        for objItem in objs:
                            FreeCAD.Console.PrintMessage("objItem.Line: "+str(objItem.Line)+"\n")
                            if objItem.Line==obj.Label:
                                #这里加一个判断，判断这个含有面的三维体的属性是不是需要更新布尔运算
                                if objItem.Attribute==ObjectsTools.Attribute.NotDefine:
                                    objItem.Proxy.redraw(objItem)
                                else:
                                    updateBooleanOrder(objItem,"Area","A")
                                    objItem.Proxy.redraw(objItem)
                                # pass
                                # objItem.Proxy.redraw(objItem)
                elif obj.Type[0:3]=="Are":
                    FreeCAD.Console.PrintMessage("changed area shape: "+str(obj.Label)+"\n")
                    objs=ObjectsTools.getAllObjectsByTypes(FreeCAD.ActiveDocument.Name,
                                                            [ObjectsTools.ObjectType.Vol_Extruded,
                                                            ObjectsTools.ObjectType.Vol_Revolution,
                                                            ObjectsTools.ObjectType.Vol_Draft_Extrude,
                                                            ObjectsTools.ObjectType.Vol_Draft_Revolution])
                    if len(objs):
                        for objItem in objs:
                            if objItem.Area==obj.Label:
                                #这里加一个判断，判断这个含有面的三维体的属性是不是需要更新布尔运算
                                if objItem.Attribute==ObjectsTools.Attribute.NotDefine:
                                    objItem.Proxy.redraw(objItem)
                                else:
                                    updateBooleanOrder(objItem,"Area","A")
                                    objItem.Proxy.redraw(objItem)
                                    # updateBoolean()
            # 如果是对分组进行copy，则不用再创建分组
            if obj.TypeId=="App::DocumentObjectGroup":
                ObjectsTools.resetGroup(obj)
                # FreeCAD.ActiveDocument.removeObject(obj.Name)
        # 属性改变时及时更新工作区域
        # if "Point" in prop:
        #     ProjectSettingsTools.updateRangeOfWorkSpaceSettings()
        import json
        FreeCAD.ActiveDocument.License = json.dumps('True')
        #################################挤出体参数更新结束#################################################
        # 为了解决复制对象时，Order跟随复制
        if  ObjectsTools.hasThePropertyByObj(obj,"Order") and prop=="Type":
            if ObjectsTools.hasThePropertyByObj(obj,"Order"):
                numOfObjects=len(ObjectsTools.getAllObjectszofThisDoc(FreeCAD.ActiveDocument.Name))
                if obj.Order<numOfObjects:
                    #更新Order
                    obj.Order=numOfObjects
                    pass
    # 文档关闭，关闭物理设置与任务控制面板


#用于更新做布尔运算的最小order
def updateBooleanOrder(obj,prop,flagMsg):
    #还需要判断一下obj是否有Order属性
    if hasattr(obj,"Order"):
        if getattr(obj,"Order")<FreeCAD.ActiveDocument.flagNeedUpdateBoolean or FreeCAD.ActiveDocument.flagNeedUpdateBoolean==-1:
            FreeCAD.ActiveDocument.flagNeedUpdateBoolean=getattr(obj,"Order")
            FreeCAD.Console.PrintMessage("NeedsRecomputeObserver: "+str(flagMsg)+" "+str(prop)+" "+str(obj.getGroupOfProperty(prop))+" "+str(FreeCAD.ActiveDocument.flagNeedUpdateBoolean)+"\n")        
class NeedsRecomputeObserver(object):
    def __init__(self):
        ObjectsTools.setImmutableOfParamObjFromUI()
        Gui.SendMsgToActiveView("ViewFit")
        # 去掉工程中不再group中的模型，并显示resuleShape
        ObjectsTools.resetProject()
        pass
    def slotRecomputedObject(self,obj):
        FreeCAD.Console.PrintError("recompute: "+str(obj.Name)+"\n")
        # Gui.SendMsgToActiveView("ViewFit")
        FreeCAD.Console.PrintError("viewFile\n")
    # def slotBeforeChangeObject(self,obj,prop):
    #     if prop=="Attribute" or prop=="Order" or obj.getGroupOfProperty(prop).startswith("Object of"):
    #         if hasattr(obj.Proxy,"ShapeProps"):
    #             obj.Proxy.ShapeProps[prop]=getattr(obj,prop)
    #         else:
    #             if obj.Proxy:
    #                 obj.Proxy.ShapeProps={}
    #                 obj.Proxy.ShapeProps[prop]=getattr(obj,prop)

    #         sayzError("obj:"+str(obj.Name)+" prop:"+str(prop)+"beforechangedValue:"+str(getattr(obj,prop)))
    
    def slotChangedObject(self,obj,prop):
        # FreeCAD.Console.PrintError("NeedsRecomputeObserver\n")
        # FreeCAD.Console.PrintError("NeedsRecomputeObserver\n")
        # if prop=="X" or prop=="Y" or prop=="Z" or prop=="R" or prop=="Theta"\
        #     or prop=="X_Value" or prop=="Y_Value" or prop=="Z_Value" or prop=="R_Value" or prop=="Theta_Value"\
        #         or prop=="Type" or prop=="Proxy" or prop=="ConductivitySIGMA" or prop=="ConductivitySIGMAValue"\
        #             or prop=="RelativeDielectricConstant" or prop=="SetEPS" or prop=="SetEPS2" or prop=="SetEPS3" or prop=="Label" or\
        #                 prop=="Group" or prop=="flagRedrawvalue" or prop=="Shape"or prop:
        
        #不是改变的非均匀网格属性
        if prop=="Attribute" or prop=="Order" or obj.getGroupOfProperty(prop).startswith("Object of"):
            # FreeCAD.Console.PrintMessage("NeedsRecomputeObserver "+str(obj.Label)+" prop:"+str(prop)+" value"+str(getattr(obj,prop))+"\n")
            # 改变的属性是模型的属性状态
            if prop=="Attribute":
                needUpdate=True
                if hasattr(obj.Proxy,"ShapeProps"):
                    #有这个key
                    if obj.Proxy.ShapeProps.has_key(prop):
                        #判断attribute是不是由conductor变为custom？
                        if (obj.Proxy.ShapeProps[prop] in [ObjectsTools.Attribute.Conductor,ObjectsTools.Attribute.Custom]\
                            and getattr(obj,"Attribute") in  [ObjectsTools.Attribute.Conductor,ObjectsTools.Attribute.Custom])\
                                or obj.Proxy.ShapeProps[prop]==getattr(obj,"Attribute"):
                            #不做任何事
                            needUpdate=False
                            pass
                if needUpdate:
                    updateBooleanOrder(obj,prop,"-1")
                    #     #否则表示属性改变了
                    #     else:
                    #         #还需要判断一下obj是否有Order属性
                    #         if hasattr(obj,"Order"):
                    #             if getattr(obj,"Order")<FreeCAD.ActiveDocument.flagNeedUpdateBoolean or FreeCAD.ActiveDocument.flagNeedUpdateBoolean==-1:
                    #                 FreeCAD.ActiveDocument.flagNeedUpdateBoolean=getattr(obj,"Order")
                    #                 # FreeCAD.Console.PrintMessage("NeedsRecomputeObserver1: "+str(prop)+" "+str(obj.getGroupOfProperty(prop))+" "+str(FreeCAD.ActiveDocument.flagNeedUpdateBoolean)+"\n")
                    #     pass
                    # #没有这个key,也不做任何事
                    # else:
                    #     pass
                    # pass

            # 非模型刚性
            else:
                # sayz("prop:"+str(prop))
                if hasattr(obj,"Attribute"):
                    # sayz("'1")
                    if getattr(obj,"Attribute")!=ObjectsTools.Attribute.NotDefine:
                        # sayz("2")
                        if hasattr(obj.Proxy,"ShapeProps"):
                            # sayz(obj.Proxy.ShapeProps)
                            # sayz(getattr(obj,prop))
                            #字典中有这个属性
                            if obj.Proxy.ShapeProps.has_key(prop):
                                # sayzError("obj.Proxy.ShapeProps[prop] "+str(obj.Proxy.ShapeProps[prop]))
                                # sayzError("getattr(obj,prop) "+str(getattr(obj,prop)))
                                #这里是为了验证 前后两个属性真的不相等
                                if obj.Proxy.ShapeProps[prop] !=getattr(obj,prop):
                                    updateBooleanOrder(obj,prop,"0")
                                    # #这里就需要更新flagUpdateBoolean
                                    # if hasattr(obj,"Order"):
                                    #     if getattr(obj,"Order")<FreeCAD.ActiveDocument.flagNeedUpdateBoolean or FreeCAD.ActiveDocument.flagNeedUpdateBoolean==-1:
                                    #         FreeCAD.ActiveDocument.flagNeedUpdateBoolean=getattr(obj,"Order")
                                    #         FreeCAD.Console.PrintMessage("NeedsRecomputeObserver2: "+str(obj.Attribute)+" "+str(prop)+" "+str(obj.getGroupOfProperty(prop))+" "+str(FreeCAD.ActiveDocument.flagNeedUpdateBoolean)+"\n")
                            #如果字典中没有这个属性，也需要重新布尔
                            else:
                                updateBooleanOrder(obj,prop,"1")
                                pass
                        # 如果没有这个ShapeProps，也需要重新刷新
                        else:
                            updateBooleanOrder(obj,prop,"2")
                            pass
                        # sayz("3")
            if hasattr(obj.Proxy,"ShapeProps"):
                obj.Proxy.ShapeProps[prop]=getattr(obj,prop)
            else:
                if obj.Proxy:
                    obj.Proxy.ShapeProps={"Attribute":ObjectsTools.Attribute.NotDefine}
                    obj.Proxy.ShapeProps[prop]=getattr(obj,prop)
                pass
        # if prop in propsNotThingWithModeling:
        #     pass
        # else:
        #     if hasattr(obj,"Attribute"):
        #         if (getattr(obj,"Attribute")==ObjectsTools.Attribute.NotDefine and (prop!="Attribute" and prop!="Order")):
        #             pass
        #         # if (getattr(obj,"Attribute")!=ObjectsTools.Attribute.NotDefine and prop!="Attribute"):
        #         else:
        #             if hasattr(obj,"Order"):
        #                 if getattr(obj,"Order")<FreeCAD.ActiveDocument.flagNeedUpdateBoolean or FreeCAD.ActiveDocument.flagNeedUpdateBoolean==-1:
                            
        #                     FreeCAD.ActiveDocument.flagNeedUpdateBoolean=getattr(obj,"Order")
        #                     FreeCAD.Console.PrintMessage("NeedsRecomputeObserver: "+str(prop)+" "+str(FreeCAD.ActiveDocument.flagNeedUpdateBoolean)+"\n")
        #         # Gui.SendMsgToActiveView("ViewFit")



def time_me(fn):
  def _wrapper(*args, **kwargs):
    start = time.clock()
    fn(*args, **kwargs)
    FreeCAD.Console.PrintError("DocumentTool.updateBoolean time: "+str(time.clock()-start)+"\n")
    # print "%s cost %s second"%(fn.__name__, time.clock() - start)
  return _wrapper

# @time_me
def updateBoolean():
    # return
    FreeCAD.Console.PrintMessage("start DocumentTool.updateBoolean()\n")
    FreeCAD.Console.PrintMessage("DocumentTool.updateBoolean() current order before PartGui.pdateBoolean(): "+str(FreeCAD.ActiveDocument.flagNeedUpdateBoolean)+"\n")
    import PartGui,PartChipic
    if FreeCAD.ActiveDocument.flagNeedUpdateBoolean>=0:
        FreeCAD.Console.PrintMessage("DocumentTool.updateBoolean() current order: "+str(FreeCAD.ActiveDocument.flagNeedUpdateBoolean)+"\n")
        #PartGui.updateBoolean(FreeCAD.ActiveDocument.flagNeedUpdateBoolean) #ZD
        PartChipic.updateBoolean(0, 1)
        changedObjsAndProps={}
        FreeCAD.ActiveDocument.flagNeedUpdateBoolean=-1
        # changedObjsAndProps.clear()
 
# 透明度检测器
''' 这个监听器主要用于更新模型的透明度。
    更新原则为：
    1、模型透明度只将理想导体与自定义导体计算在内，因为真空需要被减掉，所以不计算在内；
    2、模型A与模型B只有三种情况：
        a. A在B的内部
        b. B在A的内部
        c. A与B相交或者不想交

        注意：
            a中，若A中BoundBox只有一个面与B相同，也算作A在B内；
            b中，若B.....................A...........B..A..;

    3、内部的模型透明度低于外部模型透明度
    4、 2.c 中模型透明度相同
    5、各相邻等级模型之间的透明度之差由公式计算得出：100/总的纳入计算的模型（理想导体和自定义导体）分的等级总数
'''
class TransparencyObserver(object):
    def __init__(self):
        pass
    def slotChangedObject(self,obj,prop):
        # 模型形状发生变化
        if prop=="Shape" and ObjectsTools.hasThePropertyByObj(obj,"Attribute"):
            # 确定模型的属性
            if obj.Attribute==ObjectsTools.Attribute.Conductor or obj.Attribute==ObjectsTools.Attribute.Custom:
                self.reSetTransparency()
            pass
        # 模型属性发生变化
        elif prop=="Attribute" or prop in ObjectsTools.Custom.propList:
            v=obj.ViewObject
            if not hasattr(obj,"Attribute"):
                return
            if getattr(obj,"Attribute")==ObjectsTools.Attribute.Conductor:
                Gui.ActiveDocument.getObject(obj.Name).ShapeColor=(0.80, 0.80, 0.80)
                if hasattr(v,"DisplayMode"):
                    obj.ViewObject.DisplayMode ="Shaded"
            elif getattr(obj,"Attribute")==ObjectsTools.Attribute.Vacuo:
                # Gui.ActiveDocument.getObject(obj.Name).ShapeColor=(0.58, 0.58, 0.58)
                if hasattr(v,"DisplayMode"):
                    obj.ViewObject.DisplayMode ="Shaded"
            elif getattr(obj,"Attribute")==ObjectsTools.Attribute.NotDefine:
                try:
                    Gui.ActiveDocument.getObject(obj.Name).Visibility = True
                    Gui.ActiveDocument.getObject(obj.Name).ShapeColor=(0.80, 0.80, 0.80)
                    # FreeCAD.Console.PrintMessage(obj.ViewObject.DisplayMode)
                    v=obj.ViewObject
                    if hasattr(v,"DisplayMode"):
                        obj.ViewObject.DisplayMode = "Wireframe"
                except FreeCAD.Base.FreeCADError as e:
                    FreeCAD.Console.PrintError("Wireframe error\n")
            elif getattr(obj,"Attribute")==ObjectsTools.Attribute.Custom:
                #左边不是未定义且右边属性是未定义
                if not obj.ConductivitySIGMA==ObjectsTools.Custom.ConductivitySIGMA.NotDefine \
                    and obj.RelativeDielectricConstant==ObjectsTools.Custom.RelativeDielectricConstant.NotDefine:
                    Gui.ActiveDocument.getObject(obj.Name).ShapeColor=(0.764706,0.694118,0.494118,0.0)
                #左边是未定义且右边不是未定义
                elif  obj.ConductivitySIGMA==ObjectsTools.Custom.ConductivitySIGMA.NotDefine \
                    and not obj.RelativeDielectricConstant==ObjectsTools.Custom.RelativeDielectricConstant.NotDefine:
                    Gui.ActiveDocument.getObject(obj.Name).ShapeColor=(0.000000,0.745098,0.498039,0.0)
                #都不是未定义
                elif not obj.ConductivitySIGMA==ObjectsTools.Custom.ConductivitySIGMA.NotDefine \
                    and not obj.RelativeDielectricConstant==ObjectsTools.Custom.RelativeDielectricConstant.NotDefine:
                    Gui.ActiveDocument.getObject(obj.Name).ShapeColor=(0.435294,0.752941,0.713726,0.0)
                else:
                    Gui.ActiveDocument.getObject(obj.Name).ShapeColor=(0.80, 0.80, 0.80)
                    pass
            self.reSetTransparency()
            pass
        pass
    def slotDeletedObject(self,obj):
        if ObjectsTools.hasThePropertyByObj(obj,ObjectsTools.Attribute) :
            if obj.Attribute==ObjectsTools.Attribute.Conductor or obj.Attribute==ObjectsTools.Attribute.Custom:
                self.reSetTransparency()
    def reSetTransparency(self):
        '''
            orderLevelOfBoundBoxList=[numofConducotr,numoflevels,obj1,obj2...]
        '''
        orderLevelOfBoundBoxList=ObjectsTools.lGetNumAndOrderBoundBoxOfConductor()
        #计算透明度的步长
        strideOfTransparency=90
        if orderLevelOfBoundBoxList[1] !=0.0:
            strideOfTransparency=90/orderLevelOfBoundBoxList[1]
        # 初始透明度
        curTransparency=90
        for index in range(len(orderLevelOfBoundBoxList)-1,1,-1):
            # 第一个透明度需要加步长
            if index==2 :
                curTransparency=curTransparency-strideOfTransparency
                Gui.ActiveDocument.getObject(orderLevelOfBoundBoxList[index].obj.Name).Transparency=int(curTransparency)
                pass
            # 若当前obj的level不等于前一个的level，则当前这个透明度也要加步长
            elif orderLevelOfBoundBoxList[index].level != orderLevelOfBoundBoxList[index-1].level:
                curTransparency=curTransparency-strideOfTransparency
                Gui.ActiveDocument.getObject(orderLevelOfBoundBoxList[index].obj.Name).Transparency=int(curTransparency)
                pass
            # 当前objlevel等于前一个level，这两个透明度相同
            else:
                Gui.ActiveDocument.getObject(orderLevelOfBoundBoxList[index].obj.Name).Transparency=Gui.ActiveDocument.getObject(orderLevelOfBoundBoxList[index-1].obj.Name).Transparency
                pass
    # def slotRecomputedObject(self,obj):
    #     if ObjectsTools.hasThePropertyByObj(obj,"Type"):
    #         obj.Label="Test"
    #     import GuiTools
    #     GuiTools.setObjToFitTheView(obj)

        # if obj.getParentGroup()==None and ObjectsTools.hasThePropertyByObj(obj,"Type"):
        #     ObjectsTools.addTheirGroupForObj(obj)
        #     pass

        # objs=FreeCAD.ActiveDocument.Objects
        # for objItem in objs:
        #     if objItem.TypeId=="App::DocumentObjectGroup":
        #         if len(objItem.OutList)==0:
        #             FreeCAD.ActiveDocument.removeObject(objItem.Nmae)
        # if flag :
        #     Gui.Selection.clearSelection()
        #     flag=not flag
        # Gui.Selection.addSelection(obj)
        # Gui.SendMsgToActiveView("ViewSelection")
# 关闭运行结果树的函数，虽然在文档监听中有相关的响应函数，但是，在M3d File Editor中关闭所有文档时，不会关闭该分支树
def closeAll():
    try:
        
        import Physics
        # Physics.PhysicsCommand.TreeStructMain.FigTreeClose()

        import Visualization.VisualizationCommand.VisualizationTree
        FreeCAD.Console.PrintMessage("VisualizationTree\n")
        Visualization.VisualizationCommand.VisualizationTree.cloePlotTree()
        FreeCAD.Console.PrintMessage("cloePlot\n")
        FreeCAD.Console.PrintMessage("show\n")
        closeTab()
        FreeCAD.Console.PrintMessage("closeTab\n")
    except:
        FreeCAD.Console.PrintMessage("Wrong in DocumentTool.closeAll\n")

# 关闭 tab 事件
def closeTab():

    # 获取 qTab，解决新建工程后，找不到 qTab，导致关闭功能失效
    app = QtGui.qApp
    aw = app.activeWindow()
    if aw:
        dw = aw.findChild(QtGui.QDockWidget, 'Combo View')
        # 获取Combo View 下的comiTab
        if dw:
            qtab = dw.findChild(QtGui.QTabWidget, 'combiTab')
            # qtab.clear()
            # 得到tab的数目
            count = qtab.count()
            # 循环遍历所有tab，关闭除fixedTabText以外的所有tab
            for i in range(count):

                # 固定存在的tab
                # fixedTabText = ["模型","任务","Model","Tasks"]
                fixedTabText = "打开结果"
                # 倒着关闭，以防删除后index变化
                index = count-i-1
                # FreeCAD.Console.PrintMessage(qtab.tabText(index))
                # FreeCAD.Console.PrintMessage(index)
                # FreeCAD.Console.PrintMessage(qtab.tabToolTip(index))
                if fixedTabText in qtab.tabText(index):

                    # 删除 Tab 中的控件
                    widget = qtab.widget(index)
                    if widget is not None:
                        widget.deleteLater()
                    # 删除 Tab
                    qtab.removeTab(index)




#########################################################获取物体的值###########################################
"程序中的物体对象有Name对象和Label对象"
"其中Name属性是唯一不可变的，而Label对象是可变的，并且可以多个物体使用同一个Label（当前设置物体的label不可重复）"
"程序中显示的是物体的Label名称，而不是Name名称"
# 判断一个物体是否有某种属性
def isObjhasTheProp(obj,prop):
    props=obj.PropertiesList
    for porpItem in props:
        if porpItem==prop:
            return True
    return False
def removeOrderFromLabel(label):
    '''
    lable:    物体label
    return:   string
    '''
    if re.match(r"\[[0-9]\d*\]\_",str(label)):
        g=re.search("\_.*",str(label))
        if g:
            resultStr=g.group()[1:len(g.group())]
            return resultStr
#获取文档type类型的物体对象,type为物体的类型，isVacuo为返回的物体列表是否包含真空的物体,并去掉标号
def getActiveDocTypes(type,isOnlyConductor=False):
    '''
    type:            物体的Type
    isOnlyConductor: 是否只包含导体？，默认False，即所有
    return :         list[]
    '''
    objectList=FreeCAD.ActiveDocument.findObjects('Part::FeaturePython')
    # 剔除没有Type属性的物体
    for objItem in objectList:
        if not ObjectsTools.hasThePropertyByObj(objItem,"Type") or not ObjectsTools.hasThePropertyByObj(objItem,"Order"):
            objectList.remove(objItem)
    resultList=[]
    for objItem in objectList:
        if hasattr(objItem,"Type"):
            if objItem.Type==type:
                #只有当objItme有Attribute并且只是导体时，需要筛选，其他情况只要type相等，直接打印
                if ObjectsTools.hasThePropertyByObj(objItem,"Attribute") and isOnlyConductor:
                    if objItem.Attribute==ObjectsTools.Attribute.Conductor or objItem.Attribute==ObjectsTools.Attribute.Custom:
                        resultList.append(removeOrderFromLabel(objItem.Label))
                        pass
                else:
                    resultList.append(removeOrderFromLabel(objItem.Label))
    return resultList

# 获取导体属性的体
def getConductorVols():
    '''
    return :list[vol]
    '''
    objsList=ObjectsTools.getAllObjectszofThisDoc(FreeCAD.ActiveDocument.Name)
    resultList=[]
    for objItem in objsList:
        if ObjectsTools.hasThePropertyByObj(objItem,"Attribute"):
            if objItem.Type[0]=="V" and objItem.Attribute==ObjectsTools.Attribute.Conductor:
                resultList.append(removeOrderFromLabel(objItem.Label))
    return resultList
# 获取自定义属性的体  @ lizhenguang
def getCustomVols():
    '''
    return :list[vol]
    '''
    objsList=ObjectsTools.getAllObjectszofThisDoc(FreeCAD.ActiveDocument.Name)
    resultList=[]
    for objItem in objsList:
        if ObjectsTools.hasThePropertyByObj(objItem,"Attribute"):
            if objItem.Type[0]=="V" and objItem.Attribute==ObjectsTools.Attribute.Custom:
                resultList.append(removeOrderFromLabel(objItem.Label))
    return resultList
# 获取所有的体，Attribute包含所有
def getAllVols(isIncludeVacuo=True):
    '''
    isIncludeVacuo: 是否包含真空类型，True为包括，False不包括
    return        : list[Vol]
    '''
    objsList=ObjectsTools.getAllObjectszofThisDoc(FreeCAD.ActiveDocument.Name)
    resultList=[]
    if isIncludeVacuo:
        for objItem in objsList:
            if ObjectsTools.hasThePropertyByObj(objItem,"Attribute"):
                if objItem.Type[0]=="V":
                    resultList.append(removeOrderFromLabel(objItem.Label))
    else:
        for objItem in objsList:
            if ObjectsTools.hasThePropertyByObj(objItem,"Attribute"):
                if objItem.Type[0]=="V" and  not objItem.Attribute==ObjectsTools.Attribute.Vacuo:
                    resultList.append(removeOrderFromLabel(objItem.Label))
    return resultList
# 获取所有已定义的点线面体 @lzg
def getAllObjs():
    '''
    获取并返回所有已定义的点线面体
    '''
    objsList=ObjectsTools.getAllObjectszofThisDoc(FreeCAD.ActiveDocument.Name)
    resultList=[]
    for objItem in objsList:
        if ObjectsTools.hasThePropertyByObj(objItem,"Order"):
            resultList.append(removeOrderFromLabel(objItem.Label))
    return resultList
# 获取所有的函数体
def getAllFunctions():
    '''
    返回所有的函数体
    '''
    objsList=ObjectsTools.getAllObjectszofThisDoc(FreeCAD.ActiveDocument.Name)
    resultList=[]
    for objItem in objsList:
        if ObjectsTools.hasThePropertyByObj(objItem,"Type"):
            if objItem.Type =="Vol_Function":
                # resultList.append(removeOrderFromLabel(objItem.Label))
                resultList.append(objItem)
    return resultList

            

# 获取点的值，返回点坐标值及坐标系，坐标系始终在数组的第一项
def getValueOfPointObjByLabel(objName,isWithOrder=False):
    # objs=FreeCAD.ActiveDocument.getObjectsByLabel(objName)
        # 存放和objName相等的带有order的objLabel
    objNameList = []
    #如果没有Order,则与去掉Order的顺序列表进行配对，匹配成功则重新为objName加上[Order]_
    if not isWithOrder:
        objsLabel=ObjectsTools.getAllObjectszofThisDocWithoutOrder(FreeCAD.ActiveDocument.Name)
        for i in range(0,len(objsLabel)):
            if objName==objsLabel[i]:
                objNameList.append("[" + str(i) + "]_" + objName)
    for objName in objNameList:
        objs = FreeCAD.ActiveDocument.getObjectsByLabel(objName)
        if objs[0].Type ==ObjectsTools.ObjectType.Point:
            break

    valueList=[]
    # 默认返回坐标系为直角坐标系
    curCoordinateSys=CoordinateSystemTools.CoordinateType.Rectangular
    if len(objs):
        obj=objs[0]
        curCoordinateSys=obj.Document.CoordinateSystem
        # 当obj为点时正常返回
        if obj.Type==ObjectsTools.ObjectType.Point:
            valueList=[obj.Point.x,obj.Point.y,obj.Point.z]
        # 否则报错
        else:
            FreeCAD.Console.PrintError(str(objName)+" is not a Point.")
    else:
        FreeCAD.Console.PrintError(str(objName)+"  can not be found.")
    valueList.insert(0,curCoordinateSys)
    return valueList

# 获取线的值
def getValueOfLineObjByLable(objName,isWithOrder=False):
    '''
    objName:    物体的Label
    isWithOrder:是否包含Label前面的Order,默认不包括False
    retrun     :list[curCoordinate,
                    point1.x,point1.y,point1.z,
                    point2.x,point2.y,point2.z,
                    normalid:0表示异常；1表示x；2表示y；3表示z；4表示没有法向]
    '''
    # 存放和objName相等的带有order的objLabel
    objNameList = []
    #如果没有Order,则与去掉Order的顺序列表进行配对，匹配成功则重新为objName加上[Order]_
    if not isWithOrder:
        objsLabel=ObjectsTools.getAllObjectszofThisDocWithoutOrder(FreeCAD.ActiveDocument.Name)
        for i in range(0,len(objsLabel)):
            if objName==objsLabel[i]:
                objNameList.append("[" + str(i) + "]_" + objName)
    for objName in objNameList:
        objs = FreeCAD.ActiveDocument.getObjectsByLabel(objName)
        if objs[0].Type == "Line_Conformal":
            break

    valueList=[]
    # 默认返回坐标系为直角坐标系
    curCoordinateSys=CoordinateSystemTools.CoordinateType.Rectangular
    normalId=0
    if len(objs):
        obj=objs[0]
        curCoordinateSys=obj.Document.CoordinateSystem
        if obj.Type==ObjectsTools.ObjectType.Line_Conformal or obj.Type==ObjectsTools.ObjectType.Line_Oblique:
            
            if curCoordinateSys==CoordinateSystemTools.CoordinateType.Rectangular:
                if obj.Normal==ObjectsTools.Normal.X:
                    normalId=1
                elif obj.Normal==ObjectsTools.Normal.Y:
                    normalId=2
                else:
                    normalId=3
                valueList=[
                    ObjectsTools.getParamValueOfObj(obj,"Point1.x",UnitTools.SupportUnitType.Length),
                    ObjectsTools.getParamValueOfObj(obj,"Point1.y",UnitTools.SupportUnitType.Length),
                    ObjectsTools.getParamValueOfObj(obj,"Point1.z",UnitTools.SupportUnitType.Length),
                    ObjectsTools.getParamValueOfObj(obj,"Point2.x",UnitTools.SupportUnitType.Length),
                    ObjectsTools.getParamValueOfObj(obj,"Point2.y",UnitTools.SupportUnitType.Length),
                    ObjectsTools.getParamValueOfObj(obj,"Point2.z",UnitTools.SupportUnitType.Length),
                    normalId
                ]
            elif curCoordinateSys==CoordinateSystemTools.CoordinateType.Polar:
                if obj.Normal==ObjectsTools.Normal.R:
                    normalId=1
                elif obj.Normal==ObjectsTools.Normal.Theta:
                    normalId=2
                else:
                    normalId=3
                valueList=[
                    ObjectsTools.getParamValueOfObj(obj,"Point1.x",UnitTools.SupportUnitType.Length),
                    ObjectsTools.getParamValueOfObj(obj,"Point1.y",UnitTools.SupportUnitType.Angle),
                    ObjectsTools.getParamValueOfObj(obj,"Point1.z",UnitTools.SupportUnitType.Length),
                    ObjectsTools.getParamValueOfObj(obj,"Point2.x",UnitTools.SupportUnitType.Length),
                    ObjectsTools.getParamValueOfObj(obj,"Point2.y",UnitTools.SupportUnitType.Angle),
                    ObjectsTools.getParamValueOfObj(obj,"Point2.z",UnitTools.SupportUnitType.Length),
                    normalId
                ]

            else:
                if obj.Normal==ObjectsTools.Normal.Z:
                    normalId=1
                elif obj.Normal==ObjectsTools.Normal.R:
                    normalId=2
                else:
                    normalId=3
                valueList=[
                    ObjectsTools.getParamValueOfObj(obj,"Point1.z",UnitTools.SupportUnitType.Length),
                    ObjectsTools.getParamValueOfObj(obj,"Point1.x",UnitTools.SupportUnitType.Length),
                    ObjectsTools.getParamValueOfObj(obj,"Point1.y",UnitTools.SupportUnitType.Angle),
                    ObjectsTools.getParamValueOfObj(obj,"Point2.z",UnitTools.SupportUnitType.Length),
                    ObjectsTools.getParamValueOfObj(obj,"Point2.x",UnitTools.SupportUnitType.Length),
                    ObjectsTools.getParamValueOfObj(obj,"Point2.y",UnitTools.SupportUnitType.Angle),
                    normalId
                ]


            if obj.Type==ObjectsTools.ObjectType.Line_Oblique:
                normalId=4
                valueList=[valueList[0],
                        valueList[1],
                        valueList[2],
                        valueList[3],
                        valueList[4],
                        valueList[5],
                        normalId]
        # 后续其他类型的线扩展
        else:
            FreeCAD.Console.PrintError(str(objName)+" is not a Line.")
    else:
        FreeCAD.Console.PrintError(str(objName)+" can not be found.")
    valueList.insert(0,curCoordinateSys)
    return valueList
                


#获取正投影面类型对象的值，当normalId为0时，表示异常；1表示x,2表示y,3表示z
def getValueOfAreaObjByLable(objName,isWithOrder=False):
    '''
    objName:    物体的Label
    isWithOrder:是否包含Label前面的Order,默认不包括False
    retrun     :list[]
    '''
    # 存放和objName相等的带有order的objLabel
    objNameList = []
    #如果没有Order,则与去掉Order的顺序列表进行配对，匹配成功则重新为objName加上[Order]_
    if not isWithOrder:
        objsLabel=ObjectsTools.getAllObjectszofThisDocWithoutOrder(FreeCAD.ActiveDocument.Name)
        for i in range(0,len(objsLabel)):
            if objName==objsLabel[i]:
                objNameList.append("["+str(i)+"]_"+objName)
    for objName in objNameList:
        objs=FreeCAD.ActiveDocument.getObjectsByLabel(objName)
        if objs[0].Type =="Area_Conformal":
            break

    normalId=0
    # 默认返回坐标系为直角坐标系
    curCoordinateSys=CoordinateSystemTools.CoordinateType.Rectangular
    valueList=[]
    if len(objs):
        obj=objs[0]
        curCoordinateSys=obj.Document.CoordinateSystem
        if obj.Type==ObjectsTools.ObjectType.Area_Conformal:
            
            if curCoordinateSys==CoordinateSystemTools.CoordinateType.Rectangular:
                if obj.Normal==ObjectsTools.Normal.X:
                    normalId=1
                elif obj.Normal==ObjectsTools.Normal.Y:
                    normalId=2
                else:
                    normalId=3
                # valueList = [obj.Point1.x,
                #              obj.Point1.y,
                #              obj.Point1.z,
                #              obj.Point2.x,
                #              obj.Point2.y,
                #              obj.Point2.z,
                #              normalId]
                valueList=[
                    ObjectsTools.getParamValueOfObj(obj,"Point1.x",UnitTools.SupportUnitType.Length),
                    ObjectsTools.getParamValueOfObj(obj,"Point1.y",UnitTools.SupportUnitType.Length),
                    ObjectsTools.getParamValueOfObj(obj,"Point1.z",UnitTools.SupportUnitType.Length),
                    ObjectsTools.getParamValueOfObj(obj,"Point2.x",UnitTools.SupportUnitType.Length),
                    ObjectsTools.getParamValueOfObj(obj,"Point2.y",UnitTools.SupportUnitType.Length),
                    ObjectsTools.getParamValueOfObj(obj,"Point2.z",UnitTools.SupportUnitType.Length),
                    normalId
                ]
            elif curCoordinateSys==CoordinateSystemTools.CoordinateType.Polar:
                if obj.Normal==ObjectsTools.Normal.R:
                    normalId=1
                elif obj.Normal==ObjectsTools.Normal.Theta:
                    normalId=2
                else:
                    normalId=3
                # valueList = [obj.Point1.x,
                #              obj.Point1.y,
                #              obj.Point1.z,
                #              obj.Point2.x,
                #              obj.Point2.y,
                #              obj.Point2.z,
                #              normalId]
                valueList=[
                    ObjectsTools.getParamValueOfObj(obj,"Point1.x",UnitTools.SupportUnitType.Length),
                    ObjectsTools.getParamValueOfObj(obj,"Point1.y",UnitTools.SupportUnitType.Angle),
                    ObjectsTools.getParamValueOfObj(obj,"Point1.z",UnitTools.SupportUnitType.Length),
                    ObjectsTools.getParamValueOfObj(obj,"Point2.x",UnitTools.SupportUnitType.Length),
                    ObjectsTools.getParamValueOfObj(obj,"Point2.y",UnitTools.SupportUnitType.Angle),
                    ObjectsTools.getParamValueOfObj(obj,"Point2.z",UnitTools.SupportUnitType.Length),
                    normalId
                ]
            else:
                if obj.Normal==ObjectsTools.Normal.Z:
                    normalId=1
                elif obj.Normal==ObjectsTools.Normal.R:
                    normalId=2
                else:
                    normalId=3
                # valueList = [obj.Point1.z,
                #              obj.Point1.x,
                #              obj.Point1.y,
                #              obj.Point2.z,
                #              obj.Point2.x,
                #              obj.Point2.y,
                #              normalId]
                valueList=[
                    ObjectsTools.getParamValueOfObj(obj,"Point1.z",UnitTools.SupportUnitType.Length),
                    ObjectsTools.getParamValueOfObj(obj,"Point1.x",UnitTools.SupportUnitType.Length),
                    ObjectsTools.getParamValueOfObj(obj,"Point1.y",UnitTools.SupportUnitType.Angle),
                    ObjectsTools.getParamValueOfObj(obj,"Point2.z",UnitTools.SupportUnitType.Length),
                    ObjectsTools.getParamValueOfObj(obj,"Point2.x",UnitTools.SupportUnitType.Length),
                    ObjectsTools.getParamValueOfObj(obj,"Point2.y",UnitTools.SupportUnitType.Angle),
                    normalId
                ]
        else:
            FreeCAD.Console.PrintError(str(objName)+" is not a Area.")
    else:
        FreeCAD.Console.PrintError(str(objName)+" can not be found.")
    valueList.insert(0,curCoordinateSys)
    return valueList


# 获取正投影体的值
def getValueOfVolComformalObjByLable(objName,isWithOrder=False):
    '''
    objName    : 物体的Label
    isWithOrder:是否包含Label前面的Order,默认不包括False
    retrun     :list[]
    '''
    # 存放和objName相等的带有order的objLabel
    objNameList = []
    #如果没有Order,则与去掉Order的顺序列表进行配对，匹配成功则重新为objName加上[Order]_
    if not isWithOrder:
        objsLabel=ObjectsTools.getAllObjectszofThisDocWithoutOrder(FreeCAD.ActiveDocument.Name)
        for i in range(0,len(objsLabel)):
            if objName==objsLabel[i]:
                objNameList.append("[" + str(i) + "]_" + objName)
    for objName in objNameList:
        objs = FreeCAD.ActiveDocument.getObjectsByLabel(objName)
        if objs[0].Type == "Vol_Conformal":
            break

    valueList=[]
    # 默认返回坐标系为直角坐标系
    curCoordinateSys=CoordinateSystemTools.CoordinateType.Rectangular
    if len(objs):
        obj=objs[0]
        curCoordinateSys=obj.Document.CoordinateSystem
        if obj.Type==ObjectsTools.ObjectType.Vol_Conformal:
            if curCoordinateSys==CoordinateSystemTools.CoordinateType.Rectangular:
                # valueList=[obj.Point1.x,
                #         obj.Point1.y,
                #         obj.Point1.z,
                #         obj.Point2.x,
                #         obj.Point2.y,
                #         obj.Point2.z]
                valueList=[
                    ObjectsTools.getParamValueOfObj(obj,"Point1.x",UnitTools.SupportUnitType.Length),
                    ObjectsTools.getParamValueOfObj(obj,"Point1.y",UnitTools.SupportUnitType.Length),
                    ObjectsTools.getParamValueOfObj(obj,"Point1.z",UnitTools.SupportUnitType.Length),
                    ObjectsTools.getParamValueOfObj(obj,"Point2.x",UnitTools.SupportUnitType.Length),
                    ObjectsTools.getParamValueOfObj(obj,"Point2.y",UnitTools.SupportUnitType.Length),
                    ObjectsTools.getParamValueOfObj(obj,"Point2.z",UnitTools.SupportUnitType.Length),
                ]
            elif  curCoordinateSys==CoordinateSystemTools.CoordinateType.Rectangular:
                valueList=[
                    ObjectsTools.getParamValueOfObj(obj,"Point1.x",UnitTools.SupportUnitType.Length),
                    ObjectsTools.getParamValueOfObj(obj,"Point1.y",UnitTools.SupportUnitType.Angle),
                    ObjectsTools.getParamValueOfObj(obj,"Point1.z",UnitTools.SupportUnitType.Length),
                    ObjectsTools.getParamValueOfObj(obj,"Point2.x",UnitTools.SupportUnitType.Length),
                    ObjectsTools.getParamValueOfObj(obj,"Point2.y",UnitTools.SupportUnitType.Angle),
                    ObjectsTools.getParamValueOfObj(obj,"Point2.z",UnitTools.SupportUnitType.Length),
                ]
                pass
            else:
                valueList=[
                    ObjectsTools.getParamValueOfObj(obj,"Point1.z",UnitTools.SupportUnitType.Length),
                    ObjectsTools.getParamValueOfObj(obj,"Point1.x",UnitTools.SupportUnitType.Length),
                    ObjectsTools.getParamValueOfObj(obj,"Point1.y",UnitTools.SupportUnitType.Angle),
                    ObjectsTools.getParamValueOfObj(obj,"Point2.z",UnitTools.SupportUnitType.Length),
                    ObjectsTools.getParamValueOfObj(obj,"Point2.x",UnitTools.SupportUnitType.Length),
                    ObjectsTools.getParamValueOfObj(obj,"Point2.y",UnitTools.SupportUnitType.Angle),
                ]
        else:
            FreeCAD.Console.PrintError(str(objName)+" is not a Conformal.")
    else:
        FreeCAD.Console.PrintError(str(objName)+" can not be found.")
    valueList.insert(0,curCoordinateSys)
    return valueList

#########################################################end###############################################
def errorMessage(contentMsg,headMsg="PICGUIC"):
    '''
    headMsg: 窗口标题
    contentMsg：错误信息
    '''
    # setInformativeText
    # replayBox=QtGui.QMessageBox()
    # replayBox.setInformativeText(contentMsg)
    # replayBox.setParent(Gui.getMainWindow())
    # replayBox.setModal(True)
    # replayBox.exec_()

    replay=QtGui.QMessageBox.information(None,"PICGUIC",contentMsg)

    
def printErrorMessage(msg):
    FreeCAD.Console.PrintError(msg)