# -*- coding: utf-8 -*-
import FreeCAD, Part, math
from FreeCAD import Base
from pivy import coin
from PySide import QtGui, QtCore
from Common.Tools import CoordinateSystemTools
from Common.Tools import PlacementTools,ObjectsTools


class Helical:
    def __init__(self, obj):
        # 这里加一个flagRedraw是为了能够通过obj的这个属性的改变，使得这个模型可以间接调用redraw函数
        obj.addProperty("App::PropertyBool","flagRedraw","","").flagRedraw=True
        self.curCoordinateSystem=FreeCAD.ActiveDocument.CoordinateSystem
        self.vectorList=[]
        ''' Add some custom properties to our box feature '''
        if self.curCoordinateSystem==CoordinateSystemTools.CoordinateType.Rectangular:
            obj.addProperty("App::PropertyVectorDistance", "BasePoint", "Object of a Helical", "Length of the box").BasePoint = FreeCAD.Vector(0,0,0)
            obj.addProperty("App::PropertyVectorDistance", "TopPoint", "Object of a Helical", "Length of the box").TopPoint = FreeCAD.Vector(0.02,0.02,0.02)
            obj.addProperty("App::PropertyVectorDistance", "StartPoint", "Object of a Helical", "Length of the box").StartPoint = FreeCAD.Vector(.001,0.001732,0)
            
            obj.addProperty("App::PropertyLength", "InnerRadius", "Object of a Helical", "Width of the box").InnerRadius = 0.005
            obj.addProperty("App::PropertyLength", "OuterRadius", "Object of a Helical", "Width of the box").OuterRadius = 0.008
            obj.addProperty("App::PropertyLength", "Pitch", "Object of a Helical", "Width of the box").Pitch = 0.003
            obj.addProperty("App::PropertyLength", "Width", "Object of a Helical", "Width of the box").Width = 0.002
            
        # '''极坐标系下的属性面板'''
        elif self.curCoordinateSystem==CoordinateSystemTools.CoordinateType.Polar:
            obj.addProperty("App::PropertyPolVecDistance", "BasePoint", "Object of a Helical", "Length of the box").BasePoint = FreeCAD.Vector(0,0,0)
            obj.addProperty("App::PropertyPolVecDistance", "TopPoint", "Object of a Helical", "Length of the box").TopPoint = FreeCAD.Vector(0,0,0.001)
            obj.addProperty("App::PropertyPolVecDistance", "StartPoint", "Object of a Helical", "Length of the box").StartPoint = FreeCAD.Vector(0.002,0,0)
            
            obj.addProperty("App::PropertyLength", "InnerRadius", "Object of a Helical", "Width of the box").InnerRadius = 0.005
            obj.addProperty("App::PropertyLength", "OuterRadius", "Object of a Helical", "Width of the box").OuterRadius = 0.008
            obj.addProperty("App::PropertyLength", "Pitch", "Object of a Helical", "Width of the box").Pitch = 0.003
            obj.addProperty("App::PropertyLength", "Width", "Object of a Helical", "Width of the box").Width = 0.002

        elif self.curCoordinateSystem==CoordinateSystemTools.CoordinateType.Cylindrical:
            obj.addProperty("App::PropertyCylinderVecDistance", "BasePoint", "Object of a Helical", "Length of the box").BasePoint = FreeCAD.Vector(0,0,0)
            obj.addProperty("App::PropertyCylinderVecDistance", "TopPoint", "Object of a Helical", "Length of the box").TopPoint = FreeCAD.Vector(0,0,0.01)
            obj.addProperty("App::PropertyCylinderVecDistance", "StartPoint", "Object of a Helical", "Length of the box").StartPoint = FreeCAD.Vector(0.002,0,0)
            
            obj.addProperty("App::PropertyLength", "InnerRadius", "Object of a Helical", "Width of the box").InnerRadius = 0.005
            obj.addProperty("App::PropertyLength", "OuterRadius", "Object of a Helical", "Width of the box").OuterRadius = 0.008
            obj.addProperty("App::PropertyLength", "Pitch", "Object of a Helical", "Width of the box").Pitch = 0.003
            obj.addProperty("App::PropertyLength", "Width", "Object of a Helical", "Width of the box").Width = 0.002
        obj.addProperty("App::PropertyInteger","Order","","Order of the Conformal").Order=100

        self.vectorList=[obj.BasePoint,obj.TopPoint,obj.StartPoint]       
        ObjectsTools.addPropertyForVol(obj,ObjectsTools.ObjectType.Vol_Helical,self.curCoordinateSystem)

        obj.Proxy = self
        self.placementBefore = obj.Placement
        self.orderBefore=obj.Order
        self.labelBofroe=obj.Label
        #flagShape和flagPalcement为在移动过程中不能在属性面板中输入值，在输入值的时候不移动
        self.flagShape=True
        self.flagPlacement=True
        self.flagExcute=False
        obj.setEditorMode('Placement',2)
        obj.setEditorMode('flagRedraw',2)
        #初始化重绘
        self.initObject(obj)
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
        elif prop == "BasePoint" or prop == "TopPoint" or prop == "StartPoint" or prop == "InnerRadius" or prop=="OuterRadius" or prop=="Pitch" or prop=="Width":
            if self.flagShape:
                self.flagShape=False
                self.flagPlacement=False
                #将物体置为原点
                fp.Placement=FreeCAD.Placement(FreeCAD.Vector(0.0,0.0,0.0),FreeCAD.Rotation(0.0,0.0,0.0,1.0))
                if hasattr(fp,"TopPoint"):
                    self.vectorList=[fp.BasePoint,fp.TopPoint,fp.StartPoint]
                self.flagShape=True
                self.flagPlacement=True
                self.flagExcute=True
        elif prop == "Placement" :
            if self.flagPlacement:
                self.flagPlacement=False
                self.flagShape=False
                #设置属性自定义属性只读
                fp.setEditorMode("BasePoint",1)
                fp.setEditorMode("TopPoint",1)
                fp.setEditorMode("StartPoint",1)
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
                fp.BasePoint=resultVectors[0]
                fp.TopPoint=resultVectors[1]
                fp.StartPoint=resultVectors[2]
                self.vectorList=[fp.BasePoint,fp.TopPoint,fp.StartPoint]
                self.flagPlacement=True
                self.flagShape=True
                self.flagExcute=False
                # 重塑
                pass
        elif prop=="Shape":
            self.flagPlacement=False
        ObjectsTools.fucNonUniformGrid(self.curCoordinateSystem,fp,prop)
        ObjectsTools.fucAttributeChange(fp,prop)

    def redraw(self,obj):
        try:
            tempPoints=CoordinateSystemTools.otherToRec(self.curCoordinateSystem,self.vectorList)
            tempPoint_Base=tempPoints[0]
            tempPoint_Top=tempPoints[1]
            # 这里不能直接等于赋值，因为这样会使StartPoint发生变化
            tempPoint_Start=FreeCAD.Vector(tempPoints[2].x,tempPoints[2].y,tempPoints[2].z)
            # print "TEST:"+str(obj.StartPoint)
            #这里需要对tempPoint_Start进行处理，因为需要将这个点定位到过base点，法向为top-base的平面上
            startPointToPlane=tempPoint_Start.projectToPlane(tempPoint_Base,tempPoint_Top.sub(tempPoint_Base))
            # print "TEST:"+str(obj.StartPoint)
            #再将这个点移至距base点InnerRadius与OuterRadius中点距离处,这里取中点防止两个点都为0
            # print startPointToPlane
            # print tempPoint_Base
            # print startPointToPlane.distanceToPoint(tempPoint_Base)
            # print ((obj.InnerRadius+obj.OuterRadius)/2)
            if startPointToPlane==tempPoint_Base:
                startPointFormCenter=tempPoint_Base
            else:
                k=((obj.InnerRadius.Value+obj.OuterRadius.Value)/2)/startPointToPlane.distanceToPoint(tempPoint_Base)
                normalOfStartPointToPlaneAndTempPoint_Base=startPointToPlane.sub(tempPoint_Base)
                startPointFormCenter=k*normalOfStartPointToPlaneAndTempPoint_Base.add(tempPoint_Base)
            # print "TTTTTTTTT:"+str(startPointFormCenter)
            # startPointFormCenter=FreeCAD.Vector((obj.InnerRadius+obj.OuterRadius)/2)


            #先将base坐标系移到原点，并以原点为基准确定top和start的位置
            originBase=FreeCAD.Vector(0.0,0.0,0.0)
            originTop=tempPoint_Top-tempPoint_Base
            originStart=startPointFormCenter-tempPoint_Base
            #旋转三个点，使得base和top与Z轴重合
            rot=ObjectsTools.getQuatAfterRotation(tempPoint_Top)

            zTop=rot.multVec(tempPoint_Top)
            zStart=rot.multVec(startPointFormCenter)
            # print rot
            # print startPointFormCenter
            # print zStart
            #将z映射到XOY面上
            if not zStart.z==0:
                zStart=FreeCAD.Vector(zStart.x,zStart.y,0)
            #此时的zStart与x轴正向的角度
            # print "zStart   "+str(zStart)
            angle=ObjectsTools.getAngleWithXByVector(zStart)
            #为了能得到目标螺旋体，需要求出起点位置的矩形，让次矩形沿着螺旋线扫掠，得出
            # recPoint1=zStart
            # recPoint2=FreeCAD.Vector((zStart.Length+obj.Width.Value)*math.cos(angle),(zStart.Length+obj.Width.Value)*math.sin(angle),0)
            # recPoint3=recPoint1+FreeCAD.Vector(0,0,obj.OuterRadius-obj.InnerRadius)
            # recPoint4=recPoint2+FreeCAD.Vector(0,0,obj.OuterRadius-obj.InnerRadius)

            # recWire=Part.makePolygon([recPoint1,recPoint2,recPoint4,recPoint3,recPoint1])
            # recFace=Part.makeFace(recWire,"Part::FaceMakerBullseye")

            #螺旋线
            height=obj.BasePoint.distanceToPoint(obj.TopPoint)
            # print obj.Pitch.Value
            # print height
            # print obj.InnerRadius.Value
            # print angle
            helixLine=Part.makeHelix(obj.Pitch.Value,height,(obj.InnerRadius.Value+obj.OuterRadius.Value)/2)

            #为了能得到目标螺旋体，需要求出起点位置的矩形，让次矩形沿着螺旋线扫掠，得出
            rectPoint1=FreeCAD.Vector(obj.InnerRadius,0,-obj.Width/2)
            rectPoint2=FreeCAD.Vector(obj.OuterRadius,0,-obj.Width/2)
            rectPoint3=FreeCAD.Vector(obj.OuterRadius,0,obj.Width/2)
            rectPoint4=FreeCAD.Vector(obj.InnerRadius,0,obj.Width/2)

            recWire=Part.makePolygon([rectPoint1,rectPoint2,rectPoint3,rectPoint4,rectPoint1])
            recFace=Part.makeFace(recWire,"Part::FaceMakerBullseye")


            path=Part.Wire(helixLine)
            #扫掠
            if self.flagPlacement:
                self.flagPlacement=False
                tempPlacementBefore=self.placementBefore
                obj.Shape=path.makePipeShell([recWire],True,True)
                rot1=FreeCAD.Rotation(FreeCAD.Vector(0,0,1),angle)
                rot2=rot.inverted()
                rot=rot2.multiply(rot1)
                obj.Placement.Rotation=rot
                obj.Placement.move(tempPoint_Base)
                self.placementBefore=tempPlacementBefore
                self.flagPlacement=True
        except:
            DocumentTools.printErrorMessage("Redraw HelicalInstance Failed!")
        ObjectsTools.doSomethingAfterRecomputerVolShape(obj)
        
    def execute(self, fp):
        #设置自定义属性可编辑
        fp.setEditorMode("BasePoint",0)
        fp.setEditorMode("TopPoint",0)
        fp.setEditorMode("StartPoint",0)
        if self.flagExcute:
            if hasattr(fp,"Width"):
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
        # state["Width"]=self
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


class ViewProviderHelical:
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
