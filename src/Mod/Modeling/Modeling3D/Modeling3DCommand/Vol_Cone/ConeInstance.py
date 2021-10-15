#-*- coding: utf-8 -*-
import FreeCAD, Part, math
from FreeCAD import Base
from pivy import coin
from Common.Tools import CoordinateSystemTools
from Common.Tools import PlacementTools,ObjectsTools

'''圆锥由两个点与一个底半径组成'''
class Cone:
    def __init__(self, obj):
        ''' Add some custom properties to our Cone feature '''
        self.curCoordinateSystem=FreeCAD.ActiveDocument.CoordinateSystem
        self.vectorList=[]
        #直角坐标系下：
        if self.curCoordinateSystem=='Rectangular':
            obj.addProperty("App::PropertyVectorDistance","StartPoint","Cone","StartPoint of the Cone").StartPoint=FreeCAD.Vector(0,0,0)
            obj.addProperty("App::PropertyVectorDistance","EndPoint","Cone","EndPoint of the Cone").EndPoint=FreeCAD.Vector(0.01,0.01,0.01)
            self.vectorList.append(obj.StartPoint)
            self.vectorList.append(obj.EndPoint)
            obj.addProperty("App::PropertyLength","BottomRadius","Cone","Radius of the Cone").BottomRadius=0.001

        #极坐标系下：
        elif self.curCoordinateSystem=='Polar':
            obj.addProperty("App::PropertyPolVecDistance","StartPoint","Cone","StartPoint of the Cone").StartPoint=FreeCAD.Vector(0,0,0)
            obj.addProperty("App::PropertyPolVecDistance","EndPoint","Cone","EndPoint of the Cone").EndPoint=FreeCAD.Vector(0.01,45,0.01)
            self.vectorList.append(obj.StartPoint)
            self.vectorList.append(obj.EndPoint)
            obj.addProperty("App::PropertyLength","BottomRadius","Cone","Radius of the Cone").BottomRadius=0.001

        #圆柱坐标系下：
        elif self.curCoordinateSystem=='Cylindrical':
            obj.addProperty("App::PropertyCylinderVecDistance","StartPoint","Cone","StartPoint of the Cone").StartPoint=FreeCAD.Vector(0,0,0)
            obj.addProperty("App::PropertyCylinderVecDistance","EndPoint","Cone","EndPoint of the Cone").EndPoint=FreeCAD.Vector(0.01,45,0.01)
            self.vectorList.append(obj.StartPoint)
            self.vectorList.append(obj.EndPoint)
            obj.addProperty("App::PropertyLength","BottomRadius","Cone","Radius of the Cone").BottomRadius=0.001
        
        ObjectsTools.addPropertyForVol(obj,ObjectsTools.ObjectType.Vol_Cone,self.curCoordinateSystem)

        obj.Proxy = self
        self.placementBefore = obj.Placement
        #flagShape和flagPalcement为在移动过程中不能在属性面板中输入值，在输入值的时候不移动
        self.flagShape=True
        self.flagPlacement=True
        self.flagExcute=True

        obj.setEditorMode('Placement',2)

    def onBeforeChange(self, obj, prop):
        if hasattr(obj,"Placement"):
            obj.setEditorMode('Placement',2)
        if prop == "Placement":
            self.placementBefore = FreeCAD.Placement(obj.Placement)

    def onChanged(self, fp, prop):
        ''' Print the name of the property that has changed '''
        if prop=="StartPoint" or prop=="EndPoint" or prop == "BottomRadius":
            if self.flagShape:
                self.flagShape=False
                self.flagPlacement=False
                #将物体置为原点
                fp.Placement=FreeCAD.Placement(FreeCAD.Vector(0.0,0.0,0.0),FreeCAD.Rotation(0.0,0.0,0.0,1.0))
                self.vectorList=[fp.StartPoint,fp.EndPoint]
                self.flagShape=True
                self.flagPlacement=True
                self.flagExcute=True
        elif prop=="Placement":
            if self.flagPlacement:
                self.flagPlacement=False
                self.flagShape=False
                #设置属性自定义属性只读
                fp.setEditorMode("StartPoint",1)
                fp.setEditorMode("EndPoint",1)
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
                fp.StartPoint=resultVectors[0]
                fp.EndPoint=resultVectors[1]
                self.vectorList=[fp.StartPoint,fp.EndPoint]
                self.flagPlacement=True
                self.flagShape=True
                self.flagExcute=False
                # 重塑
                pass
    def redraw(self,obj):
        tempPoints=CoordinateSystemTools.otherToRec(self.curCoordinateSystem,self.vectorList)
        
        p1=tempPoints[0]
        p2=tempPoints[1]
        if p1==p2:
            obj.Shape=ObjectsTools.makePoint(p1)
        else:
            height = p1.distanceToPoint(p2)
            dir = p2 - p1
            obj.Shape = Part.makeCone(0, obj.BottomRadius, height, p2, -dir)
    def execute(self, fp):
        ''' Print a short message when doing a recomputation, this method is mandatory '''
        #设置自定义属性可编辑
        fp.setEditorMode("StartPoint",0)
        fp.setEditorMode("EndPoint",0)
        if self.flagExcute:
            self.redraw(fp)
            self.flagExcute=False

    def __getstate__(self):
        return self.curCoordinateSystem,self.flagShape,self.flagPlacement,self.flagExcute
    
    def __setstate__(self,state):
        self.curCoordinateSystem,self.flagShape,self.flagPlacement,self.flagExcute=state



class ViewProviderCone:
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
        return None

    def __setstate__(self,state):
        ''' When restoring the pickled object from document we have the chance to set some
        internals here. Since no data were pickled nothing needs to be done here.
        '''
        return None
