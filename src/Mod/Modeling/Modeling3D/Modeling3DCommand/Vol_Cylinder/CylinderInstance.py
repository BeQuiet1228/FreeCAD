# -*- coding: utf-8 -*-
import FreeCAD, Part, math
from FreeCAD import Base
from pivy import coin
from PySide import QtGui, QtCore
from Common.Tools import CoordinateSystemTools
from Common.Tools import PlacementTools,ObjectsTools,DocumentTools


class Cylinder:
    def __init__(self, obj,needOrder=True,thistype=""):
        
        self.curCoordinateSystem=FreeCAD.ActiveDocument.CoordinateSystem
        self.vectorList=[]
        ''' Add some custom properties to our box feature '''
        if self.curCoordinateSystem==CoordinateSystemTools.CoordinateType.Rectangular:
            obj.addProperty("App::PropertyVectorDistance", "Point_1", "Object of a Cylinder", "Length of the box").Point_1 = FreeCAD.Vector(0.003,0,0)
            obj.addProperty("App::PropertyVectorDistance", "Point_2", "Object of a Cylinder", "Length of the box").Point_2 = FreeCAD.Vector(0.004,0,0)
            self.vectorList=[obj.Point_1,obj.Point_2]

            obj.addProperty("App::PropertyLength", "Radius", "Object of a Cylinder", "Width of the box").Radius = 0.001
        # '''极坐标系下的属性面板PropertyLength'''
        elif self.curCoordinateSystem==CoordinateSystemTools.CoordinateType.Polar:
            obj.addProperty("App::PropertyPolVecDistance", "Point_1", "Object of a Cylinder", "Length of the box").Point_1 = FreeCAD.Vector(0,0,0)
            obj.addProperty("App::PropertyPolVecDistance", "Point_2", "Object of a Cylinder", "Length of the box").Point_2 = FreeCAD.Vector(0,0,0.001)
            self.vectorList=[obj.Point_1,obj.Point_2]
            obj.addProperty("App::PropertyLength", "Radius", "Object of a Cylinder", "Width of the box").Radius = '10 mm'

        elif self.curCoordinateSystem==CoordinateSystemTools.CoordinateType.Cylindrical:
            obj.addProperty("App::PropertyCylinderVecDistance", "Point_1", "Object of a Cylinder", "Length of the box").Point_1 = FreeCAD.Vector(0,0,0)
            obj.addProperty("App::PropertyCylinderVecDistance", "Point_2", "Object of a Cylinder", "Length of the box").Point_2 = FreeCAD.Vector(0,360,0.001)
            self.vectorList=[obj.Point_1,obj.Point_2]
            obj.addProperty("App::PropertyLength", "Radius", "Object of a Cylinder", "Width of the box").Radius = 0.001
        if needOrder:
            ObjectsTools.addPropertyForVol(obj,ObjectsTools.ObjectType.Vol_Cylinder,self.curCoordinateSystem)
        # else:
        #     ObjectsTools.addPropertyForVol(obj,thistype,self.curCoordinateSystem)
        # ObjectsTools.addNonUniformGridAttribute(self.curCoordinateSystem,obj)
        if needOrder:
            obj.addProperty("App::PropertyInteger","Order","","Order of the Conformal").Order=100
        
        self.placementBefore = obj.Placement
        if needOrder:
            self.orderBefore=obj.Order
        self.labelBofroe=obj.Label
        #flagShape和flagPalcement为在移动过程中不能在属性面板中输入值，在输入值的时候不移动
        self.flagShape=True
        self.flagPlacement=True
        self.flagExcute=False
        obj.setEditorMode('Placement',2)
        # obj.setEditorMode('flagRedraw',2)
        if needOrder:
            self.initObject(obj)
        #初始化重绘
        self.redraw(obj)
        obj.Proxy = self

    def initObject(self,obj):
        ObjectsTools.setInitOrderForObject(obj)
    def onBeforeChange(self, obj, prop):
        # #每一个体都由一个字典来存放会影响模型布尔运算的属性
        # if prop=="Attribute" or prop=="Order" or obj.getGroupOfProperty(prop).startswith("Object of"):
        #     if not hasattr(self,"ShapeProps"):
        #         self.ShapeProps={}
        #     else:
        #         self.ShapeProps={}

        if hasattr(obj,"Placement"):
            obj.setEditorMode('Placement',2)
        if hasattr(obj,"Type"):
            obj.setEditorMode("Type",2)
        # if hasattr(obj,"flagRedraw"):
        #     obj.setEditorMode("flagRedraw",2)
        if prop == "Placement":
            self.placementBefore = FreeCAD.Placement(obj.Placement)
        if prop=="Order":
            self.orderBefore=obj.Order
        if prop=="Label":
            self.labelBofroe=obj.Label

    def onChanged(self, fp, prop):

        ''' Print the name of the property that has changed '''
        # if prop=="flagRedraw":
        #     self.flagExcute=True
        #物体对象的Order发生改变时
        if prop=="Order":
            ObjectsTools.updateWhenOrderChanged(fp,self.orderBefore,fp.Order)
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
        if prop == "Point_1" or prop == "Point_2" or prop == "Radius" or prop == "RadiusOutside":
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
        ObjectsTools.fucAttributeChange(fp,prop)
    def redraw(self,obj):
        try:
            tempPoints=CoordinateSystemTools.otherToRec(self.curCoordinateSystem,self.vectorList)
            tempPoint_0=tempPoints[0]
            tempPoint_1=tempPoints[1]
            #当两个点重合时，形成一个面
            if tempPoint_0==tempPoint_1:
                dir=tempPoint_0
                e1=Part.makeCircle(obj.Radius,tempPoint_0,dir)
                obj.Shape=Part.makeFace([Part.Wire([e1])],"Part::FaceMakerBullseye")
            else:
                FreeCAD.Console.PrintMessage("tempPoint_0:"+str(tempPoint_0)+"\n")
                FreeCAD.Console.PrintMessage("tempPoint_1:"+str(tempPoint_1)+"\n")

                line=Part.makeLine(tempPoint_0,tempPoint_1)
                path=Part.Wire(line)
                dir=tempPoint_1-tempPoint_0
                e1=Part.makeCircle(obj.Radius,tempPoint_0,dir)
                shapeCircle=Part.makeFace([Part.Wire([e1])],"Part::FaceMakerBullseye")
                obj.Shape=path.makePipe(shapeCircle)
            pass
        except:
            DocumentTools.printErrorMessage("Redraw Cylinder Failed!")
        ObjectsTools.doSomethingAfterRecomputerVolShape(obj)
        
    def execute(self, fp):
        FreeCAD.Console.PrintMessage("Cylinder excute\n")
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


class ViewProviderCylinder:
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
        return "Wireframe"

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
