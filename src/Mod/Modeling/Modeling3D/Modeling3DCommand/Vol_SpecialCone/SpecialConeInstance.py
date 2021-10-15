#-*- coding: utf-8 -*-
import FreeCAD
import Part
from Common.Tools import CoordinateSystemTools
from Common.Tools import PlacementTools, ObjectsTools

from File.FileCommand.M3DFile import M3DFileUtil

'''圆台由两个点与一个底半径组成'''
class SpecialCone:
    def __init__(self, obj,needOrder=True,thistype=""):
        ''' Add some custom properties to our SpecialCone feature '''
        # 这里加一个flagRedraw是为了能够通过obj的这个属性的改变，使得这个模型可以间接调用redraw函数
        obj.addProperty("App::PropertyBool","flagRedraw","","").flagRedraw=True
        self.curCoordinateSystem=FreeCAD.ActiveDocument.CoordinateSystem
        self.vectorList=[]
        #直角坐标系下：
        if self.curCoordinateSystem=='Rectangular':
            obj.addProperty("App::PropertyVectorDistance","PointBottom","Object of a SpecialCone","PointBottom of the SpecialCone").PointBottom=FreeCAD.Vector(0,0,0)
            obj.addProperty("App::PropertyVectorDistance","PointTop","Object of a SpecialCone","PointTop of the SpecialCone").PointTop=FreeCAD.Vector(0.001,0.001,0.001)
            self.vectorList.append(obj.PointBottom)
            self.vectorList.append(obj.PointTop)
            obj.addProperty("App::PropertyLength","RadiusTop","Object of a SpecialCone","RadiusTop of the SpecialCone").RadiusTop=0.001
            obj.addProperty("App::PropertyLength","RadiusBottom","Object of a SpecialCone", "RadiusBottom of the SpecialCone").RadiusBottom=0.002

            # # 网格
            # obj.addProperty("App::PropertyBool","X","NonUniformGrid","").X=False
            # obj.addProperty("App::PropertyLength","X_Value","NonUniformGrid","").X_Value=0
            
            # obj.addProperty("App::PropertyBool","Y","NonUniformGrid","").Y=False
            # obj.addProperty("App::PropertyLength","Y_Value","NonUniformGrid","").Y_Value=0
                
            # obj.setEditorMode('X_Value',2)
            # obj.setEditorMode('Y_Value',2)
        #极坐标系下：
        elif self.curCoordinateSystem=='Polar':
            obj.addProperty("App::PropertyPolVecDistance","PointBottom","Object of a SpecialCone","PointBottom of the SpecialCone").PointBottom=FreeCAD.Vector(0,0,0)
            obj.addProperty("App::PropertyPolVecDistance","PointTop","Object of a SpecialCone","PointTop of the SpecialCone").PointTop=FreeCAD.Vector(0,360,1)
            # obj.addProperty("App::PropertyPosition","PointBottom","SpecialCone","PointBottom of the SpecialCone").PointBottom=FreeCAD.Vector(0,0,206)
            # obj.addProperty("App::PropertyPosition","PointTop","SpecialCone","PointTop of the SpecialCone").PointTop=FreeCAD.Vector(0,0,210)

            self.vectorList.append(obj.PointBottom)
            self.vectorList.append(obj.PointTop)
            obj.addProperty("App::PropertyLength","RadiusTop","Object of a SpecialCone","RadiusTop of the SpecialCone").RadiusTop=13
            obj.addProperty("App::PropertyLength","RadiusBottom","Object of a SpecialCone", "RadiusBottom of the SpecialCone").RadiusBottom=17
            # # 网格
            # obj.addProperty("App::PropertyBool","R","NonUniformGrid","").R=False
            # obj.addProperty("App::PropertyLength","R_Value","NonUniformGrid","").R_Value=0
            
            # obj.addProperty("App::PropertyBool","Theta","NonUniformGrid","").Theta=False
            # obj.addProperty("App::PropertyAngle","Theta_Value","NonUniformGrid","").Theta_Value=0
                
            # obj.setEditorMode('R_Value',2)
            # obj.setEditorMode('Theta_Value',2)
        #圆柱坐标系下：
        elif self.curCoordinateSystem=='Cylindrical':
            obj.addProperty("App::PropertyCylinderVecDistance","PointBottom","Object of a SpecialCone","PointBottom of the SpecialCone").PointBottom=FreeCAD.Vector(0,0,0)
            obj.addProperty("App::PropertyCylinderVecDistance","PointTop","Object of a SpecialCone","PointTop of the SpecialCone").PointTop=FreeCAD.Vector(0,360,1)
            self.vectorList.append(obj.PointBottom)
            self.vectorList.append(obj.PointTop)
            obj.addProperty("App::PropertyLength","RadiusTop","Object of a SpecialCone","RadiusTop of the SpecialCone").RadiusTop=1.0
            # # 网格
            # obj.addProperty("App::PropertyBool","R","NonUniformGrid","").R=False
            # obj.addProperty("App::PropertyLength","R_Value","NonUniformGrid","").R_Value=0
            
            # obj.addProperty("App::PropertyBool","Theta","NonUniformGrid","").Theta=False
            # obj.addProperty("App::PropertyAngle","Theta_Value","NonUniformGrid","").Theta_Value=0
                
            # obj.setEditorMode('R_Value',2)
            # obj.setEditorMode('Theta_Value',2)
            # 
            obj.addProperty("App::PropertyLength","RadiusBottom","Object of a SpecialCone", "RadiusBottom of the SpecialCone").RadiusBottom=10.0
        # # 网格
        # obj.addProperty("App::PropertyBool","Z","NonUniformGrid","").Z=False
        # obj.addProperty("App::PropertyLength","Z_Value","NonUniformGrid","").Z_Value=0
        # obj.setEditorMode('Z_Value',2)
        # # 
        # obj.addProperty("App::PropertyString", "Type", "", "Type of Ojecy").Type = ObjectsTools.ObjectType.Vol_SpecialCone
        # obj.addProperty("App::PropertyEnumeration", "Attribute", "Attribute", "SpecialCone of Ojecy")
        # obj.Attribute=[ObjectsTools.Attribute.NotDefine,ObjectsTools.Attribute.Conductor,ObjectsTools.Attribute.Custom,ObjectsTools.Attribute.Vacuo]
        if thistype=="":
            ObjectsTools.addPropertyForVol(obj,ObjectsTools.ObjectType.Vol_SpecialCone,self.curCoordinateSystem)
        else:
            ObjectsTools.addPropertyForVol(obj,thistype,self.curCoordinateSystem)
        if needOrder:
            obj.addProperty("App::PropertyInteger","Order","","Order of the Conformal").Order=100

        obj.Proxy = self
        self.placementBefore = obj.Placement
        if needOrder:
            self.orderBefore=obj.Order
        self.labelBofroe=obj.Label
        #flagShape和flagPalcement为在移动过程中不能在属性面板中输入值，在输入值的时候不移动
        self.flagShape=True
        self.flagPlacement=True
        self.flagExcute=False
        obj.setEditorMode('Placement',2)
        obj.setEditorMode('Type',2)
        obj.setEditorMode('flagRedraw',2)
        if needOrder:
            #初始化
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

        if prop=="PointBottom" or prop=="PointTop" or prop == "RadiusBottom" or prop=="RadiusTop":
            if self.flagShape:
                self.flagShape=False
                self.flagPlacement=False
                #将物体置为原点
                fp.Placement=FreeCAD.Placement(FreeCAD.Vector(0.0,0.0,0.0),FreeCAD.Rotation(0.0,0.0,0.0,1.0))
                self.vectorList=[fp.PointBottom,fp.PointTop]
                self.flagShape=True
                self.flagPlacement=True
                self.flagExcute=True
        elif prop=="Placement":
            if self.flagPlacement:
                self.flagPlacement=False
                self.flagShape=False
                #设置属性自定义属性只读
                fp.setEditorMode("PointBottom",1)
                fp.setEditorMode("PointTop",1)
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
                fp.PointBottom=resultVectors[0]
                fp.PointTop=resultVectors[1]
                self.vectorList=[fp.PointBottom,fp.PointTop]
                self.flagPlacement=True
                self.flagShape=True
                # 重塑
                self.flagExcute=False
                pass
        # elif prop=="Attribute":
        ObjectsTools.fucAttributeChange(fp,prop)
        
        ObjectsTools.fucNonUniformGrid(self.curCoordinateSystem,fp,prop)

    def redraw(self,obj):
        try:
            tempPoints=CoordinateSystemTools.otherToRec(self.curCoordinateSystem,self.vectorList)
            tempPoint_0=tempPoints[0]
            tempPoint_1=tempPoints[1]
            height = tempPoint_0.distanceToPoint(tempPoint_1)
            dir = tempPoint_1 - tempPoint_0
            #圆柱
            if obj.RadiusBottom==obj.RadiusTop:
                if height==0:
                    # obj.Shape=Part.makeCylinder(obj.RadiusBottom,0.1,tempPoint_0,dir)
                    pass
                else:
                    obj.Shape=Part.makeCylinder(obj.RadiusBottom,height,tempPoint_0,dir)
            #圆锥
            else:
                if height==0:
                    # obj.Shape = Part.makeCone(obj.RadiusBottom, obj.RadiusTop, 0.1, tempPoint_0, dir)
                    pass
                else:
                    obj.Shape = Part.makeCone(obj.RadiusBottom, obj.RadiusTop, height, tempPoint_0, dir)
                # obj.Shape = Part.makeCone(obj.RadiusBottom, obj.RadiusTop, height, -dir)
        except:
            DocumentTools.printErrorMessage("Redraw SpecialCone Failed!")
        ObjectsTools.doSomethingAfterRecomputerVolShape(obj)

    def execute(self, fp):
        ''' Print a short message when doing a recomputation, this method is mandatory '''
        #设置自定义属性可编辑
        fp.setEditorMode("PointBottom",0)
        fp.setEditorMode("PointTop",0)
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
        FreeCAD.Console.PrintMessage("state  "+str(state)+"\n")
        self.curCoordinateSystem=state["curCoordinateSystem"]
        self.flagShape=True
        self.flagPlacement=state["flagPlacement"] 
        self.flagExcute=state["flagExcute"]
        vectorList=[]
        
        for i in range(len(state["vectorList"])):
            v=FreeCAD.Vector(state["vectorList"][i][0],state["vectorList"][i][1],state["vectorList"][i][2])
            vectorList.append(v)
        self.vectorList=vectorList

class ViewProviderSpecialCone:
    def __init__(self, obj):
        ''' Set this object to the proxy object of the actual view provider '''
        # print obj.Name
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

