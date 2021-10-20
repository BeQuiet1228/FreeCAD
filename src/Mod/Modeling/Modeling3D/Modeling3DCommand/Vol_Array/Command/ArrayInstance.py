#-*- coding: utf-8 -*-
import FreeCAD
import Part
from Common.Tools import CoordinateSystemTools
from Common.Tools import ObjectsTools,DocumentTools
from Common.Tools import PlacementTools

from File.FileCommand.M3DFile import M3DFileUtil


class Array:
    def __init__(self, obj):
        ''' Add some custom properties to our Conformal feature '''
        self.curCoordinateSystem=FreeCAD.ActiveDocument.CoordinateSystem

        self.vectorList=[]
        obj.addProperty("App::PropertyString","BaseObjType","Object of a ParamArray","Type of a BaseObj",0,True,False)
        obj.addProperty("App::PropertyString","BaseObjData","Object of a ParamArray","Type of a BaseObj",0,True,False)
        obj.addProperty("App::PropertyInteger","IFrom","Object of a ParamArray","start i")
        obj.addProperty("App::PropertyInteger","ITo","Object of a ParamArray","start i")

        # #直角坐标系下：
        # if self.curCoordinateSystem=='Rectangular':
        #     obj.addProperty("App::PropertyVectorDistance","Point1","Object of a Conformal","Point1 of the Conformal").Point1=FreeCAD.Vector(0,0,0)
        #     obj.addProperty("App::PropertyVectorDistance","Point2","Object of a Conformal","Point2 of the Conformal").Point2=FreeCAD.Vector(1,1,1)
        #     self.vectorList.append(obj.Point1)
        #     self.vectorList.append(obj.Point2)

        # #极坐标系下：
        # elif self.curCoordinateSystem=='Polar':
        #     obj.addProperty("App::PropertyPolVecDistance","Point1","Object of a Conformal","Point1 of the Conformal").Point1=FreeCAD.Vector(0,0,0)
        #     obj.addProperty("App::PropertyPolVecDistance","Point2","Object of a Conformal","Point2 of the Conformal").Point2=FreeCAD.Vector(0,360,1)
        #     self.vectorList.append(obj.Point1)
        #     self.vectorList.append(obj.Point2)

        # #圆柱坐标系下：
        # elif self.curCoordinateSystem=='Cylindrical':
        #     FreeCAD.Console.PrintMessage("Cylindrical System"+ "\n")
        #     obj.addProperty("App::PropertyCylinderVecDistance","Point1","Object of a Conformal","Point1 of the Conformal").Point1=FreeCAD.Vector(0,0,0)
        #     obj.addProperty("App::PropertyCylinderVecDistance","Point2","Object of a Conformal","Point2 of the Conformal").Point2=FreeCAD.Vector(0,360,1)
        #     self.vectorList.append(obj.Point1)
        #     self.vectorList.append(obj.Point2)
        ObjectsTools.addPropertyForVol(obj,ObjectsTools.ObjectType.Vol_ParamArray,self.curCoordinateSystem)
        #为物体新增加步骤顺序属性
        obj.addProperty("App::PropertyInteger","Order","","Order of the Array").Order=100
        #
        obj.Proxy = self
        self.placementBefore = obj.Placement
        self.orderBefore=obj.Order
        self.labelBofroe=obj.Label
        #flagShape和flagPalcement为在移动过程中不能在属性面板中输入值，在输入值的时候不移动
        self.flagShape=True
        self.flagPlacement=True
        self.flagExcute=False
        #控制Label和Order互斥更新
        self.flagLabel=True
        self.flagOrder=True

        obj.setEditorMode('Placement',2)
        # obj.setEditorMode('Type',2)
        #初始化
        self.initObject(obj)
        #重绘
        self.redraw(obj)
        self.flagLabel=True
        
    
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
            # self.flagLabel=False
            ObjectsTools.updateWhenOrderChanged(fp,self.orderBefore,fp.Order)
            # self.flagLabel=True
            pass
        elif prop=="Label":
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
        # elif prop=="Point1" or prop=="Point2" :
        #     if self.flagShape:
        #         self.flagShape=False
        #         self.flagPlacement=False
        #         #将物体置为原点
        #         fp.Placement=FreeCAD.Placement(FreeCAD.Vector(0.0,0.0,0.0),FreeCAD.Rotation(0.0,0.0,0.0,1.0))
        #         # self.redraw(fp)
        #         self.vectorList=[fp.Point1,fp.Point2]
        #         self.flagShape=True
        #         self.flagPlacement=True
        #         self.flagExcute=True
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
                self.flagExcute=False
                pass
        # elif prop=="Attribute":
        ObjectsTools.fucAttributeChange(fp,prop)
        
        ObjectsTools.fucNonUniformGrid(self.curCoordinateSystem,fp,prop)
        # elif prop=="X" or prop=="Y" or prop=="Z" or prop=="R" or prop=="Theta":
        #     #控制非均匀网格是否显示
        #     ObjectsTools.fucNonUniformGrid(self.curCoordinateSystem,fp)
            
    def redraw(self,obj):
        objs=obj.Shapes
        # FreeCAD.Console.PrintMessage(objs)
        theFirstShape=None
        otherShapes=[]

        for objItem in objs:
            # FreeCAD.Console.PrintMessage("1\n")
            if objItem.Shape and theFirstShape==None:
                # FreeCAD.Console.PrintMessage("2\n")
                theFirstShape=objItem.Shape
                # FreeCAD.Console.PrintMessage("3\n")
            else:

                # FreeCAD.Console.PrintMessage("4\n")
                otherShapes.append(objItem.Shape)
        # FreeCAD.Console.PrintMessage(otherShapes)
        if theFirstShape==None:
            # FreeCAD.Console.PrintMessage("5\n")
            return
        else:
            if len(otherShapes)==0:
                # FreeCAD.Console.PrintMessage("6\n")
                obj.Shape=theFirstShape
            else:
                # FreeCAD.Console.PrintMessage("7\n")
                obj.Shape=theFirstShape.multiFuse(otherShapes)
        # objs=obj.Shapes
        # shapes=[]
        # for objItem in objs:
        #     if objItem.Shape:
        #         shapes.append(objItem.Shape)
        # obj.Shape=Part.makeCompound(shapes)
        pass
    def execute(self, fp):
        ''' Print a short message when doing a recomputation, this method is mandatory '''
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
def syna(msg):
    FreeCAD.Console.PrintMessage("\n")
    FreeCAD.Console.PrintMessage(msg)
    FreeCAD.Console.PrintMessage("\n")
