#-*- coding: utf-8 -*-
import FreeCAD, Part, math
from FreeCAD import Base
from pivy import coin

from Common.Tools import CoordinateSystemTools,DocumentTools
from Common.Tools import PlacementTools,ObjectsTools


class Rectangular:
    def __init__(self, obj):
        self.curCoordinateSystem=FreeCAD.ActiveDocument.CoordinateSystem
        self.vectorList=[]
        if self.curCoordinateSystem=="Rectangular":
            obj.addProperty("App::PropertyVectorDistance","Point1","Object of a Rectangular","Point1 of the Rectangular").Point1=FreeCAD.Vector(0.001,0,0)
            obj.addProperty("App::PropertyVectorDistance","Point2","Object of a Rectangular","Point2 of the Rectangular").Point2=FreeCAD.Vector(0.001,0.001,0.001)
            obj.addProperty("App::PropertyEnumeration","Normal","Object of a Rectangular","The normal of the line")                              
            obj.Normal=["x","y","z"]
            
            self.vectorList.append(obj.Point1)
            self.vectorList.append(obj.Point2)
        obj.addProperty("App::PropertyString", "Type", "Object of a Rectangular", "Type of Ojecy").Type =  ObjectsTools.ObjectType.Area_Rectangular
        ObjectsTools.addNonUniformGridAttribute(self.curCoordinateSystem,obj)
        obj.addProperty("App::PropertyInteger","Order","","Order of the Conformal").Order=100

        obj.Proxy = self

        self.placementBefore = obj.Placement
        self.orderBefore=obj.Order
        self.labelBofroe=obj.Label
        
        self.isPoint1Change=False
        self.isPoint2Change=False

        self.flagShape=True
        self.flagPlacement=True
        self.flagExcute=False
        obj.setEditorMode('Placement',2)
        obj.setEditorMode('Type',2)
        self.initObject(obj)
        #重绘
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
        elif prop=="Point1":
            self.isPoint1Change=True
        elif prop=="Point2":
            self.isPoint2Change=True
        elif prop=="Normal":
            pass
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
        if prop == "Point1" or prop == "Point2" or prop=="Normal":
            if self.flagShape:
                self.flagShape=False
                self.flagPlacement=False
                fp.Placement=FreeCAD.Placement(FreeCAD.Vector(0.0,0.0,0.0),FreeCAD.Rotation(0.0,0.0,0.0,1.0))
                self.vectorList=[fp.Point1,fp.Point2]
                self.flagExcute=True
                self.flagShape=True
                self.flagPlacement=True
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
                # 重塑
                pass
        elif prop=="Normal":
            self.isPoint2Change=True
            self.flagExcute=True
            pass
        ObjectsTools.fucNonUniformGrid(self.curCoordinateSystem,fp,prop)
        # elif prop=="X" or prop=="Y" or prop=="Z" :
        #     #控制非均匀网格是否显示
        #     ObjectsTools.fucNonUniformGrid(self.curCoordinateSystem,fp)


    def redraw(self,obj):
        try:
            if obj.Normal=="x":
                    otherCornerPoint1=FreeCAD.Vector(obj.Point2.x,obj.Point1.y,obj.Point2.z)
                    otherCornerPoint2=FreeCAD.Vector(obj.Point1.x,obj.Point2.y,obj.Point1.z)
                    # obj.Shape=Part.makePolygon([fp.Point1,otherCornerPoint1,fp.Point2,otherCornerPoint2])
            elif obj.Normal=="y":
                otherCornerPoint1=FreeCAD.Vector(obj.Point2.x,obj.Point1.y,obj.Point1.z)
                otherCornerPoint2=FreeCAD.Vector(obj.Point1.x,obj.Point2.y,obj.Point2.z)
                # obj.Shape=Part.makePolygon([fp.Point1,otherCornerPoint1,fp.Point2,otherCornerPoint2])
            elif obj.Normal=="z":
                otherCornerPoint1=FreeCAD.Vector(obj.Point2.x,obj.Point1.y,obj.Point1.z)
                otherCornerPoint2=FreeCAD.Vector(obj.Point1.x,obj.Point2.y,obj.Point2.z)
                # obj.Shape=Part.makePolygon([fp.Point1,otherCornerPoint1,fp.Point2,otherCornerPoint2])
            obj.Shape=Part.makeFace(Part.makePolygon([obj.Point1,otherCornerPoint1,obj.Point2,otherCornerPoint2,obj.Point1]),"Part::FaceMakerExtrusion")
            pass
        except:
            DocumentTools.printErrorMessage("Redraw Rectrangular Failed!")
    def execute(self, fp):
        ''' Print a short message when doing a recomputation, this method is mandatory '''
        # FreeCAD.Console.PrintMessage("Recompute Python Rectangular feature\n")
        # e1=Part.makeCircle(fp.RadiusInside,fp.CenterPoint)
        # e2=Part.makeCircle(fp.RadiusOutside,fp.CenterPoint)
        # fp.Shape = Part.makeFace([Part.Wire([e1]),Part.Wire([e2])],"Part::FaceMakerBullseye")
        if self.isPoint1Change:
            if fp.Normal=="x" or fp.Normal=="r":
                if self.flagShape:
                    self.flagShape=False
                    self.flagPlacement=False
                    fp.Point2=FreeCAD.Vector(fp.Point1.x,fp.Point2.y,fp.Point2.z)
                    self.flagShape=True
                    self.flagPlacement=True
            elif fp.Normal=="y" or fp.Normal=="theta":
                if self.flagShape:
                    self.flagShape=False
                    self.flagPlacement=False
                    fp.Point2=FreeCAD.Vector(fp.Point2.x,fp.Point1.y,fp.Point2.z)
                    # self.vectorList[1]=fp.Point2
                    self.flagShape=True
                    self.flagPlacement=True
            else:
                if self.flagShape:
                    self.flagShape=False
                    self.flagPlacement=False
                    fp.Point2=FreeCAD.Vector(fp.Point2.x,fp.Point2.y,fp.Point1.z)
                    # self.vectorList[1]=fp.Point2
                    self.flagShape=True
                    self.flagPlacement=True
            self.vectorList=[fp.Point1,fp.Point2]
            self.isPoint1Change=False
            pass
        elif self.isPoint2Change:
            if fp.Normal=="x"or fp.Normal=="r":
                if self.flagShape:
                    self.flagShape=False
                    self.flagPlacement=False
                    fp.Point1=FreeCAD.Vector(fp.Point2.x,fp.Point1.y,fp.Point1.z)
                    # self.vectorList[1]=fp.Point2
                    self.flagShape=True
                    self.flagPlacement=True
            elif fp.Normal=="y" or fp.Normal=="theta":
                if self.flagShape:
                    self.flagShape=False
                    self.flagPlacement=False
                    fp.Point1=FreeCAD.Vector(fp.Point1.x,fp.Point2.y,fp.Point1.z)
                    # self.vectorList[1]=fp.Point2
                    self.flagShape=True
                    self.flagPlacement=True
            else:
                if self.flagShape:
                    self.flagShape=False
                    self.flagPlacement=False
                    fp.Point1=FreeCAD.Vector(fp.Point1.x,fp.Point1.y,fp.Point2.z)
                    # self.vectorList[1]=fp.Point2
                    self.flagShape=True
                    self.flagPlacement=True
            self.vectorList=[fp.Point1,fp.Point2]
            self.isPoint2Change=False
        #设置自定义属性可编辑
        fp.setEditorMode("Point1",0)
        fp.setEditorMode("Point2",0)
        if self.flagExcute:
            self.redraw(fp)
            self.flagExcute=False

    def __getstate__(self):
        state={}
        state["curCoordinateSystem"]=self.curCoordinateSystem
        state["flagShape"]=self.flagShape
        state["flagPlacement"]=self.flagPlacement
        state["flagExcute"]=self.flagExcute
        state["isPoint1Change"]=self.isPoint1Change
        state["isPoint2Change"]=self.isPoint2Change
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
        self.isPoint1Change=state["isPoint1Change"]
        self.isPoint2Change=state["isPoint2Change"]
        vectorList=[]
        
        FreeCAD.Console.PrintMessage(len(state["vectorList"]))
        for i in range(len(state["vectorList"])):
            v=FreeCAD.Vector(state["vectorList"][i][0],state["vectorList"][i][1],state["vectorList"][i][2])
            vectorList.append(v)
        self.vectorList=vectorList

class ViewProviderRectangular:
    def __init__(self, obj):
        ''' Set this object to the proxy object of the actual view provider '''
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
            static const char * ViewProviderRectangular_xpm[] = {
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
#end