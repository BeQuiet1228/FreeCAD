#-*- coding: utf-8 -*-
import FreeCAD, Part, math
from FreeCAD import Base
from pivy import coin
from Common.Tools import CoordinateSystemTools,ObjectsTools
from Common.Tools import PlacementTools

class ObliqueLine:
    def __init__(self, obj):
        ''' Add some custom properties to our ObliqueLine feature '''
        self.curCoordinateSystem=FreeCAD.ActiveDocument.CoordinateSystem
        self.vectorList=[]
        #直角坐标系下：
        if self.curCoordinateSystem=='Rectangular':
            obj.addProperty("App::PropertyVectorDistance","Point1","Object of a ObliqueLine","Point1 of the ObliqueLine").Point1=FreeCAD.Vector(0,0,0)
            obj.addProperty("App::PropertyVectorDistance","Point2","Object of a ObliqueLine","Point2 of the ObliqueLine").Point2=FreeCAD.Vector(0.005,0,0.001)
            # obj.addProperty("App::PropertyEnumeration","Normal","ObliqueLine","The normal of the line")
                                  
            # obj.Normal=["x","y","z"]
            self.vectorList.append(obj.Point1)
            self.vectorList.append(obj.Point2)

        #极坐标系下：
        elif self.curCoordinateSystem=='Polar':
            obj.addProperty("App::PropertyPolVecDistance","Point1","Object of a ObliqueLine","Point1 of the ObliqueLine").Point1=FreeCAD.Vector(0.001,0,0)
            obj.addProperty("App::PropertyPolVecDistance","Point2","Object of a ObliqueLine","Point2 of the ObliqueLine").Point2=FreeCAD.Vector(0.003,360,0.002)
            # obj.addProperty("App::PropertyEnumeration","Normal","ObliqueLine","The normal of the line")
            # obj.Normal=["r","theta","z"]
            self.vectorList.append(obj.Point1)
            self.vectorList.append(obj.Point2)

        #圆柱坐标系下：
        elif self.curCoordinateSystem=='Cylindrical':
            obj.addProperty("App::PropertyCylinderVecDistance","Point1","Object of a ObliqueLine","Point1 of the ObliqueLine").Point1=FreeCAD.Vector(0,0,0)
            obj.addProperty("App::PropertyCylinderVecDistance","Point2","Object of a ObliqueLine","Point2 of the ObliqueLine").Point2=FreeCAD.Vector(0.001,360,0.001)
            # obj.addProperty("App::PropertyEnumeration","Normal","ObliqueLine","The normal of the line")
            # obj.Normal=["z","r""theta"]
            self.vectorList.append(obj.Point1)
            self.vectorList.append(obj.Point2)
        
        obj.addProperty("App::PropertyInteger","Order","","Order of the Conformal").Order=100
        ObjectsTools.addNonUniformGridAttribute(self.curCoordinateSystem,obj)
        obj.addProperty("App::PropertyString", "Type", "Object of a ObliqueLine", "Type of Ojecy").Type = "Line_Oblique"
        obj.Proxy = self
        self.placementBefore = obj.Placement
        self.orderBefore=obj.Order
        self.labelBofroe=obj.Label
        #flagShape和flagPalcement为在移动过程中不能在属性面板中输入值，在输入值的时候不移动
        self.flagShape=True
        self.flagPlacement=True
        #控制是否执行excute函数
        self.flagExcute=False
        obj.setEditorMode('Placement',2)
        obj.setEditorMode('Type',2)
        self.initObject(obj)
        #初始化重绘
        self.redraw(obj)

    def initObject(self,obj):
        ObjectsTools.setInitOrderForObject(obj)
        # obj.Label="["+str(obj.Order)+"]"+"_"+obj.Label
        pass

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
        ''' Print the name of the property that has changed '''
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
        if prop=="Point1" or prop=="Point2" :
            if self.flagShape:
                self.flagShape=False
                self.flagPlacement=False
                #将物体置为原点
                fp.Placement=FreeCAD.Placement(FreeCAD.Vector(0.0,0.0,0.0),FreeCAD.Rotation(0.0,0.0,0.0,1.0))
                #self.redraw(fp)
                self.vectorList=[fp.Point1,fp.Point2]
                self.flagShape=True
                self.flagPlacement=True
                self.flagExcute=True
        elif prop=="Placement":
            if self.flagPlacement:
                self.flagPlacement=False
                self.flagShape=False
                #设置属性自定义属性只读
                fp.setEditorMode("Point1",1)
                fp.setEditorMode("Point2",1)
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
                fp.Point1=resultVectors[0]
                fp.Point2=resultVectors[1]
                self.vectorList=[fp.Point1,fp.Point2]
                self.flagPlacement=True
                self.flagShape=True
                # 重塑
                self.flagExcute=False
                pass
        # elif prop=="Normal":
        #     FreeCAD.Console.PrintMessage("Normal\n")
        #     self.flagExcute=True
        #     #self.redraw(fp)
        ObjectsTools.fucNonUniformGrid(self.curCoordinateSystem,fp,prop)
    
    
    def redraw(self,obj):
        # #先计算属性面板中显示的值
        # # tempPoints=CoordinateSystemTools.otherToRec(self.curCoordinateSystem,self.vectorList)
        # tempPoint_0=self.vectorList[0]
        # tempPoint_1=self.vectorList[1]
        # #FreeCAD.Console.PrintMessage("redraw:"+str(tempPoints)+"\n")
        # if obj.Normal=="x"or obj.Normal=="r":
        #     tempPoint_1=FreeCAD.Vector(tempPoint_1.x,tempPoint_0.y,tempPoint_0.z)
        # elif obj.Normal=="y" or obj.Normal=="theta":
        #     tempPoint_1=FreeCAD.Vector(tempPoint_0.x,tempPoint_1.y,tempPoint_0.z)
        # else:
        #     tempPoint_1=FreeCAD.Vector(tempPoint_0.x,tempPoint_0.y,tempPoint_1.z)
        # if self.flagShape:
        #     self.flagShape=False
        #     self.flagPlacement=False

        #     obj.Point2=tempPoint_1
        #     self.vectorList[1]=obj.Point2

        #     self.flagPlacement=True
        #     self.flagShape=True
        # FreeCAD.Console.PrintMessage("temp1:"+str(tempPoint_0)+"\n temp2:"+str(tempPoint_1)+"\n")
        try:
            # 再计算对应绘制时的值
            tempPoints=CoordinateSystemTools.otherToRec(self.curCoordinateSystem,self.vectorList)
            tempPoint_0=tempPoints[0]
            tempPoint_1=tempPoints[1]
            #出现点重合的情况
            if tempPoint_0==tempPoint_1:
                obj.Shape = Part.Vertex(tempPoint_0)
            else:
                obj.Shape=Part.makeLine(tempPoint_0,tempPoint_1)
        except:
            DocumentTools.printErrorMessage("Redraw ObliqueLine Failed!")

    def execute(self, fp):
        ''' Print a short message when doing a recomputation, this method is mandatory '''
        #设置自定义属性可编辑
        fp.setEditorMode("Point1",0)
        fp.setEditorMode("Point2",0)
        #只有在重新输入了Point1或者Point2的值才会重新绘制
        if self.flagExcute:
            self.redraw(fp)
            self.flagExcute=False
        # #坐标转换：
        # tempPoints=CoordinateSystemTools.otherToRec(self.curCoordinateSystem,self.vectorList)
        # #坐标转换结束
        # tempPlacement=fp.Placement.copy()
        # #移动恢复
        # tempPoint1=tempPoints[0].sub(tempPlacement.Base)
        # tempPoint2=tempPoints[1].sub(tempPlacement.Base)
        # #旋转恢复
        # rot = tempPlacement.Rotation
        # #p1=tempPoint1
        # p1=rot.inverted().multVec(tempPoint1)
        # p2 = rot.inverted().multVec(tempPoint2)
   
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
 

class ViewProviderObliqueLine:
    def __init__(self, obj):
        ''' Set this object to the proxy object of the actual view provider '''
        obj.setEditorMode('DisplayMode',1)
        obj.Proxy = self

    def attach(self, obj):
        ''' Setup the scene sub-graph of the view provider, this method is mandatory '''
        return

    def updateData(self, fp, prop):
        ''' If a property of the handled feature has changed we have the chance to handle this here '''
        return
    def getDisplayModes(self,obj):
        ''' Return a list of display modes. '''
        modes=[]
        return modes

    def getDefaultDisplayMode(self):
        ''' Return the name of the default display mode. It must be defined in getDisplayModes. '''
        return "Flat Lines"
    def setDisplayMode(self,mode):
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

    def __setstate__(self,state):
        ''' When restoring the pickled object from document we have the chance to set some
        internals here. Since no data were pickled nothing needs to be done here.
        '''
        return None

