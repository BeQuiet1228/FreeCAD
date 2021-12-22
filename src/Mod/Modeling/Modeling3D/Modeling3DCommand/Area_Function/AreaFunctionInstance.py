# -*- coding: utf-8 -*-
import FreeCAD, Part, math, PartChipic
from FreeCAD import Base
import FreeCADGui
from pivy import coin
from PySide import QtGui, QtCore
from Common.Tools import CoordinateSystemTools
from Common.Tools import PlacementTools,ObjectsTools
import os
import subprocess
import time
import math
class AreaFunction:
    def __init__(self, obj):
                # typeOfObj=ObjectsTools.ObjectType.Area_Function,
                # order=100,
                # attribute=ObjectsTools.Attribute.NotDefine,
                # valueDX1="DX1",
                # valueDX2="DX2",
                # valueDX3="DX3",
                # isDx1=True,
                # isDx2=True,
                # isDx3=True,
                # Point_1X=None,
                # Point_1Y=None,
                # Point_1Z=None,
                # Point_2X=None,
                # Point_2Y=None,
                # Point_2Z=None,
                # Expression=None,
                # Precision=16
                # ):
        self.curCoordinateSystem=FreeCAD.ActiveDocument.CoordinateSystem
        self.vectorList=[]
        obj.addProperty("App::PropertyString","Expression","Object of a Function","").Expression="x+y+z-1"
        ''' Add some custom properties to our box feature '''
        if self.curCoordinateSystem==CoordinateSystemTools.CoordinateType.Rectangular:
            obj.addProperty("App::PropertyVectorDistance", "Point_1", "Object of a Function", "Length of the box").Point_1 = FreeCAD.Vector(-2,-2,-2)
            obj.addProperty("App::PropertyVectorDistance", "Point_2", "Object of a Function", "Length of the box").Point_2 = FreeCAD.Vector(2,2,2)
            self.vectorList=[obj.Point_1,obj.Point_2]
        # '''极坐标系下的属性面板'''
        elif self.curCoordinateSystem==CoordinateSystemTools.CoordinateType.Polar:
            obj.addProperty("App::PropertyPolVecDistance", "Point_1", "Object of a Function", "Length of the box").Point_1 = FreeCAD.Vector(-1,-1,-1)
            obj.addProperty("App::PropertyPolVecDistance", "Point_2", "Object of a Function", "Length of the box").Point_2 = FreeCAD.Vector(0.01,360,0.01)
            obj.Expression="r+z-1"
            self.vectorList=[obj.Point_1,obj.Point_2]
        elif self.curCoordinateSystem==CoordinateSystemTools.CoordinateType.Cylindrical:
            obj.addProperty("App::PropertyCylinderVecDistance", "Point_1", "Object of a Function", "Length of the box").Point_1 = FreeCAD.Vector(0,0,0)
            obj.addProperty("App::PropertyCylinderVecDistance", "Point_2", "Object of a Function", "Length of the box").Point_2 = FreeCAD.Vector(1,1,1)
            self.vectorList=[obj.Point_1,obj.Point_2]

        obj.addProperty("App::PropertyInteger", "Precision", "Object of a Function", "Precision of the function").Precision = 20
        # ObjectsTools.addPropertyForVol(obj,ObjectsTools.ObjectType.Area_Function,self.curCoordinateSystem)
        obj.addProperty("App::PropertyString", "Type", "", "Type of Ojecy").Type = ObjectsTools.ObjectType.Area_Function
        ObjectsTools.addNonUniformGridAttribute(self.curCoordinateSystem,obj)
        obj.addProperty("App::PropertyInteger","Order","","Order of the Area Function").Order=100

        self.orderBefore=obj.Order
        self.labelBofroe=obj.Label

        obj.Proxy = self
        self.placementBefore = obj.Placement
        #flagShape和flagPalcement为在移动过程中不能在属性面板中输入值，在输入值的时候不移动
        self.flagShape=True
        self.flagPlacement=True
        self.flagExcute=False
        obj.setEditorMode('Placement',2)
        obj.setEditorMode("Type",2)

        self.initOrder(obj)
        # # 初始化参数
        # self.initObj(obj,
        #             order,
        #             attribute,
        #             valueDX1,
        #             valueDX2,
        #             valueDX3,
        #             isDx1,
        #             isDx2,
        #             isDx3,
        #             Point_1X,
        #             Point_1Y,
        #             Point_1Z,
        #             Point_2X,
        #             Point_2Y,
        #             Point_2Z,
        #             Expression,
        #             Precision)
        self.initOrder(obj)
        #初始化重绘
        self.redraw(obj)
    
    def initOrder(self,obj):
        ObjectsTools.setInitOrderForObject(obj)
        # obj.Label="["+str(obj.Order)+"]"+"_"+obj.Label
        pass

    # def initObj(self,
    #             obj,
    #             order,
    #             attribute,
    #             valueDX1,
    #             valueDX2,
    #             valueDX3,
    #             isDx1,
    #             isDx2,
    #             isDx3,
    #             Point_1X,
    #             Point_1Y,
    #             Point_1Z,
    #             Point_2X,
    #             Point_2Y,
    #             Point_2Z,
    #             Expression,
    #             Precision):
    #     obj.Order=order
    #     obj.Attribute=attribute
    #     ObjectsTools.
    #     pass
    def onBeforeChange(self, obj, prop):
        if hasattr(obj,"Placement"):
            obj.setEditorMode('Placement',2)
        if hasattr(obj,"Type"):
            obj.setEditorMode("Type",2)
        if prop == "Placement":
            self.placementBefore = FreeCAD.Placement(obj.Placement)
        if prop=="Order":
            self.orderBefore=obj.Order
        if prop=="Label":
            self.labelBofroe=obj.Label
        
    def onChanged(self, fp, prop):
        #物体对象的Order发生改变时
        if prop=="Order":
            # if self.flagOrder:
                # self.flagLabel=False
            ObjectsTools.updateWhenOrderChanged(fp,self.orderBefore,fp.Order)
                # self.flagLabel=True
            pass
        if prop=="Label":
            if not hasattr(self,"flagLabel"):
                self.flagLabel=True
            # 此处flagLabel的作用是updateWhenLabelChanged函数中会改变Label的值\
            # 为了不让onChanged函数循环执行导致程序崩溃
            if self.flagLabel:
                self.flagLabel=False
                # fp.Label="Test"
                #这里加个判断是为了解决b=FreeCAD.ActiveDocument.copyObject(o)，copy时不能读到labelBofore
                if not ObjectsTools.hasThePropertyByObj(fp,"labelBofroe"):
                    ObjectsTools.updateWhenLableChanged(fp,fp.Label,fp.Label)
                else:
                    ObjectsTools.updateWhenLableChanged(fp,self.labelBofroe,fp.Label)
                pass
                self.flagLabel=True

        ''' Print the name of the property that has changed '''
        if prop == "Point_1" or prop == "Point_2" or prop=="Expression" or prop=="Precision":
            if self.flagShape:
                self.flagShape=False
                self.flagPlacement=False
                #将物体置为原点
                fp.Placement=FreeCAD.Placement(FreeCAD.Vector(0.0,0.0,0.0),FreeCAD.Rotation(0.0,0.0,0.0,1.0))
                self.vectorList=[fp.Point_1,fp.Point_2]
                self.flagShape=True
                self.flagPlacement=True
                self.flagExcute=True
        elif prop == "Placement" :
            if self.flagPlacement:
                self.flagPlacement=False
                self.flagShape=False
                #设置属性自定义属性只读
                fp.setEditorMode("Point_1",1)
                fp.setEditorMode("Point_2",1)
                #坐标转换
                vectorList=CoordinateSystemTools.otherToRec(self.curCoordinateSystem,self.vectorList)
                #转换结束
                pos = fp.Placement.Base.sub(self.placementBefore.Base)
                resultVectors=[]
                #
                #位移
                if pos!=FreeCAD.Vector(0.0,0.0,0.0):
                    resultVectors=PlacementTools.moveAdd(pos,vectorList)
                #旋转
                else:
                    resultVectors=PlacementTools.rotate(self.placementBefore,fp.Placement,vectorList)
                resultVectors=CoordinateSystemTools.recToOther(self.curCoordinateSystem,resultVectors)
                #转换完成
                fp.Point_1=resultVectors[0]
                fp.Point_2=resultVectors[1]
                self.vectorList=[fp.Point_1,fp.Point_2]
                self.flagPlacement=True
                self.flagShape=True
                self.flagExcute=False
                # 重塑
                pass
        ObjectsTools.fucNonUniformGrid(self.curCoordinateSystem,fp,prop)

    # def time_me(fn):
    #     def _wrapper(*args, **kwargs):
    #         start = time.clock()
    #         fn(*args, **kwargs)
    #         FreeCAD.Console.PrintError("Function time: "+str(time.clock()-start)+"\n")
    #         # print "%s cost %s second"%(fn.__name__, time.clock() - start)
    #     return _wrapper
    # @time_me
    def redraw(self,obj):
        from Modeling3D.Tools import  OtherTools
        expressionStr=OtherTools.parseExpressionStr(obj.Expression.replace(" ",""))
        import re
        expressionStr=re.sub(r"\b[r|R]\b","(sqrt(x*x+y*y))",expressionStr)
        expressionStr=re.sub(r"\btheta\b","(atan(y/x))",expressionStr,flags=re.IGNORECASE)
        expressionStr=OtherTools.parseFunctionObjStr(expressionStr)

        try:
            #[tempPoint1,tempPoint2]=ObjectsTools.getRMinMaxPoints(obj.Point_1,obj.Point_2,self.curCoordinateSystem) #ZD
            tempPoint1=obj.Point_1
            tempPoint2=obj.Point_2
            #todo type
            type=10
            #obj.Shape=Part.makeFuncMesh(0,expressionStr,tempPoint1[0],tempPoint2[0],tempPoint1[1],tempPoint2[1],tempPoint1[2],tempPoint2[2],FreeCAD.getUserAppDataDir()+"\\tempFunc.json",str(obj.Precision))
            obj.Shape=PartChipic.makeFuncMesh(type,expressionStr,tempPoint1[0],tempPoint2[0],tempPoint1[1],tempPoint2[1],tempPoint1[2],tempPoint2[2],self.curCoordinateSystem,str(obj.Precision),"")
        except:
            from Modeling.Common.Tools import DocumentTools
            DocumentTools.printErrorMessage("Redraw Function Failed!")

    def execute(self, fp):
        #设置自定义属性可编辑
        fp.setEditorMode("Point_1",0)
        fp.setEditorMode("Point_2",0)
        if self.flagExcute:
            self.redraw(fp)
            self.flagExcute=False

    def __getstate__(self):
        state={}
        state["curCoordinateSystem"]=self.curCoordinateSystem
        state["flagShape"]=self.flagShape
        state["flagPlacement"]=self.flagPlacement
        state["flagExcute"]=self.flagExcute
        state["vectorList"]=[]
        for i in range(len(self.vectorList)):
            v=[self.vectorList[i].x,self.vectorList[i].y,self.vectorList[i].z]
            state["vectorList"].append(v)
        return state
    
    def __setstate__(self,state):
        self.curCoordinateSystem=state["curCoordinateSystem"]
        self.flagShape=True
        self.flagPlacement=state["flagPlacement"] 
        self.flagExcute=state["flagExcute"]
        vectorList=[]
        
        for i in range(len(state["vectorList"])):
            v=FreeCAD.Vector(state["vectorList"][i][0],state["vectorList"][i][1],state["vectorList"][i][2])
            vectorList.append(v)
        self.vectorList=vectorList


class ViewProviderFunction:
    def __init__(self, obj):
        ''' Set this object to the proxy object of the actual view provider '''
        obj.Proxy = self

    def attach(self, obj):
        ''' Setup the scene sub-graph of the view provider, this method is mandatory '''
        return

    def updateData(self, fp, prop):
        ''' If a property of the handled feature has changed we have the chance to handle this here '''
        return

    def getDisplayModes(self, obj):
        ''' Return a list of display modes. '''
        modes = []
        return modes

    def getDefaultDisplayMode(self):
        ''' Return the name of the default display mode. It must be defined in getDisplayModes. '''
        return "Flat Lines"

    def setDisplayMode(self, mode):
        ''' Map the display mode defined in attach with those defined in getDisplayModes.
        Since they have the same names nothing needs to be done. This method is optinal.
        '''
        return mode
    def onChanged(self, vp, prop):
        ''' Print the name of the property that has changed '''
        pass

    def getIcon(self):
        ''' Return the icon in XMP format which will appear in the tree view. This method is optional
        and if not defined a default icon is shown.
        '''
        return """
            /* XPM */
            static const char * ViewProviderBox_xpm[] = {
            "16 16 6 1",
            " 	c None",
            ".	c #141010",
            "+	c #615BD2",
            "@	c #C39D55",
            "#	c #000000",
            "$	c #57C355",
            "        ........",
            "   ......++..+..",
            "   .@@@@.++..++.",
            "   .@@@@.++..++.",
            "   .@@  .++++++.",
            "  ..@@  .++..++.",
            "###@@@@ .++..++.",
            "##$.@@$#.++++++.",
            "#$#$.$$$........",
            "#$$#######      ",
            "#$$#$$$$$#      ",
            "#$$#$$$$$#      ",
            "#$$#$$$$$#      ",
            " #$#$$$$$#      ",
            "  ##$$$$$#      ",
            "   #######      "};
            """

    def __getstate__(self):
        ''' When saving the document this object gets stored using Python's cPickle module.
        Since we have some un-pickable here -- the Coin stuff -- we must define this method
        to return a tuple of all pickable objects or None.
        '''
        return None

    def __setstate__(self, state):
        ''' When restoring the pickled object from document we have the chance to set some
        internals here. Since no data were pickled nothing needs to be done here.
        '''
        return None
