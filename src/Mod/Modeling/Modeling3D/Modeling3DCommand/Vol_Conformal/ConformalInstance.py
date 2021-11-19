#-*- coding: utf-8 -*-
import FreeCAD
import Part
from Common.Tools import CoordinateSystemTools
from Common.Tools import ObjectsTools,DocumentTools
from Common.Tools import PlacementTools
import math

from File.FileCommand.M3DFile import M3DFileUtil


class Conformal:
    def __init__(self, obj, needOrder = True, thistype = ""):
        '''
        Add some custom properties to our Conformal feature
        needOrder: 是否需要order;
        thistype: 不为空指定type，否则默认type
        '''
        # 这里加一个flagRedraw是为了能够通过obj的这个属性的改变，使得这个模型可以间接调用redraw函数
        obj.addProperty("App::PropertyBool","flagRedraw","","").flagRedraw=True
        self.curCoordinateSystem=FreeCAD.ActiveDocument.CoordinateSystem
        self.vectorList=[]
        #直角坐标系下：
        if self.curCoordinateSystem=='Rectangular':
            obj.addProperty("App::PropertyVectorDistance","Point1","Object of a Conformal","Point1 of the Conformal").Point1=FreeCAD.Vector(0,0,0)
            obj.addProperty("App::PropertyVectorDistance","Point2","Object of a Conformal","Point2 of the Conformal").Point2=FreeCAD.Vector(0.001,0.001,0.001)
            self.vectorList.append(obj.Point1)
            self.vectorList.append(obj.Point2)

        #极坐标系下：
        elif self.curCoordinateSystem=='Polar':
            obj.addProperty("App::PropertyPolVecDistance","Point1","Object of a Conformal","Point1 of the Conformal").Point1=FreeCAD.Vector(0,0,0)
            obj.addProperty("App::PropertyPolVecDistance","Point2","Object of a Conformal","Point2 of the Conformal").Point2=FreeCAD.Vector(0,360,0.001)
            self.vectorList.append(obj.Point1)
            self.vectorList.append(obj.Point2)

        #圆柱坐标系下：
        elif self.curCoordinateSystem=='Cylindrical':
            obj.addProperty("App::PropertyCylinderVecDistance","Point1","Object of a Conformal","Point1 of the Conformal").Point1=FreeCAD.Vector(0,0,0)
            obj.addProperty("App::PropertyCylinderVecDistance","Point2","Object of a Conformal","Point2 of the Conformal").Point2=FreeCAD.Vector(0,360,0.001)
            self.vectorList.append(obj.Point1)
            self.vectorList.append(obj.Point2)
        if needOrder:
            obj.addProperty("App::PropertyInteger","Order","","Order of the Conformal").Order=100
        if thistype=="":
            ObjectsTools.addPropertyForVol(obj,ObjectsTools.ObjectType.Vol_Conformal,self.curCoordinateSystem)
        else:
            ObjectsTools.addPropertyForVol(obj,thistype,self.curCoordinateSystem)
        #为物体新增加步骤顺序属性
        obj.addProperty("App::PropertyInteger","Order","","Order of the Conformal").Order=100
        
        
        #
        obj.Proxy = self
        self.placementBefore = obj.Placement
        if needOrder:
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
        obj.setEditorMode('flagRedraw',2)
        # obj.setEditorMode('Type',2)
        #初始化
        if needOrder:
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
        if hasattr(obj,"flagRedraw"):
            obj.setEditorMode("flagRedraw",2)
        if prop == "Placement":
            self.placementBefore = FreeCAD.Placement(obj.Placement)
        if prop=="Order":
            self.orderBefore=obj.Order
        if prop=="Label":
            self.labelBofroe=obj.Label

    def onChanged(self, fp, prop):
        ''' Print the name of the property that has changed '''
        if prop=="flagRedraw":
            self.flagExcute=True
        #物体对象的Order发生改变时
        elif prop=="Order":
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
        elif prop=="Point1" or prop=="Point2" :
            if self.flagShape:
                self.flagShape=False
                self.flagPlacement=False
                #将物体置为原点
                fp.Placement=FreeCAD.Placement(FreeCAD.Vector(0.0,0.0,0.0),FreeCAD.Rotation(0.0,0.0,0.0,1.0))
                # self.redraw(fp)
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
                self.flagExcute=False
                pass
        # elif prop=="Attribute":
        ObjectsTools.fucAttributeChange(fp,prop)
        
        ObjectsTools.fucNonUniformGrid(self.curCoordinateSystem,fp,prop)
        # elif prop=="X" or prop=="Y" or prop=="Z" or prop=="R" or prop=="Theta":
        #     #控制非均匀网格是否显示
        #     ObjectsTools.fucNonUniformGrid(self.curCoordinateSystem,fp)
            
    def redraw(self,obj):
        # FreeCAD.Console.PrintMessage("Conformal ReDraw\n")
        # 重绘
        if self.curCoordinateSystem=='Rectangular':
            length = abs(obj.Point1.x - obj.Point2.x)
            width = abs(obj.Point1.y - obj.Point2.y)
            height = abs(obj.Point1.z - obj.Point2.z)
            dir=FreeCAD.Vector(0,0,1)
            try:
                obj.Shape  = Part.makeBox(length, width, height, obj.Point1, dir)
            except:
                DocumentTools.printErrorMessage("Redraw Conformal Failed!")
                return
                pass
            # obj.Shape  = Part.makeBox(length, width, height, obj.Point1, dir)
            pass
        elif self.curCoordinateSystem=='Polar' or self.curCoordinateSystem=='Cylindrical':
            tempP1=CoordinateSystemTools.otherToRecOne(self.curCoordinateSystem,obj.Point1)
            tempP2=CoordinateSystemTools.otherToRecOne(self.curCoordinateSystem,FreeCAD.Vector(obj.Point2.x,obj.Point1.y,obj.Point1.z))
            tempP3=CoordinateSystemTools.otherToRecOne(self.curCoordinateSystem,FreeCAD.Vector(obj.Point2.x,obj.Point1.y,obj.Point2.z))
            tempP4=CoordinateSystemTools.otherToRecOne(self.curCoordinateSystem,FreeCAD.Vector(obj.Point1.x,obj.Point1.y,obj.Point2.z))
            
           #只有一个点的情况
            if tempP1==tempP2 and tempP2==tempP4:
                # obj.Shape=Part.Vertex(FreeCAD.Vector(tempP1.x,tempP1.y,tempP1.z))
                # obj.Shape=Part.makeBox(0.001,0.001,0.001,tempP1)
                # return
                obj.Shape=ObjectsTools.makePoint(tempP1)
            #防止两个点重合出现错误的情况
            elif tempP1==tempP2:
                # tempP2=tempP2.add(FreeCAD.Vector(0.001*math.cos(tempP2.y),0.001*math.sin(tempP2.y),0))
                if tempP3==tempP4:
                    obj.Shape=Part.makeLine(tempP1,tempP3)
                else:
                    obj.Shape=ObjectsTools.getPipeObj(obj.Point1,obj.Point2)
            elif tempP1==tempP4:
                # tempP4=tempP4.add(FreeCAD.Vector(0,0,0.01))
                obj.Shape=ObjectsTools.getArcObj(obj.Point1,obj.Point2)
            else:
                # line1=Part.makeLine(tempP1,tempP2)
                line2=Part.makeLine(tempP1,tempP4)
                shapeCir=ObjectsTools.getArcObj(FreeCAD.Vector(obj.Point1.x,obj.Point1.y,obj.Point2.z),obj.Point2)
                path=Part.Wire(line2)
                obj.Shape=path.makePipe(shapeCir)
                pass
            
        ObjectsTools.doSomethingAfterRecomputerVolShape(obj)

        # ObjectsTools.checkVolShape(obj)
        # elif self.curCoordinateSystem=='Cylindrical':
        #     FreeCAD.Console.PrintMessage("CylindericalSystem\n")
        #     pass 
    def execute(self, fp):
        ''' Print a short message when doing a recomputation, this method is mandatory '''
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


 

class ViewProviderConformal:
    def __init__(self, obj):
        ''' Set this object to the proxy object of the actual view provider '''
        obj.Proxy = self
        obj.Transparency=90

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
        return "Wireframe"
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
        return 

    def __setstate__(self,state):
        ''' When restoring the pickled object from document we have the chance to set some
        internals here. Since no data were pickled nothing needs to be done here.
        '''
        return 
