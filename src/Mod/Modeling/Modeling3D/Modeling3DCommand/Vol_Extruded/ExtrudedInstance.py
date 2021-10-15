#-*- coding: utf-8 -*-
import FreeCAD
import Part
from Common.Tools import CoordinateSystemTools
from Common.Tools import ObjectsTools
from Common.Tools import PlacementTools

from File.FileCommand.M3DFile import M3DFileUtil


class Extruded:
    def __init__(self, obj):
        doc=FreeCAD.ActiveDocument
        # 这里加一个flagRedraw是为了能够通过obj的这个属性的改变，使得这个模型可以间接调用redraw函数
        obj.addProperty("App::PropertyBool","flagRedraw","","").flagRedraw=True
        self.curCoordinateSystem=doc.CoordinateSystem
        obj.addProperty("App::PropertyEnumeration", "Area", "Object of a Extruded", "Area of the Extruded")
        obj.Area=ObjectsTools.getAreasByDoc(doc)
        obj.addProperty("App::PropertyEnumeration", "Line", "Object of a Extruded", "Line of the Extruded")
        obj.Line=ObjectsTools.getLinesByDoc(doc)
        
        ObjectsTools.addPropertyForVol(obj,ObjectsTools.ObjectType.Vol_Extruded,self.curCoordinateSystem)
        obj.addProperty("App::PropertyInteger","Order","","Order of the Extruded").Order=100
        obj.Proxy = self
        self.placementBefore = obj.Placement
        self.orderBefore=obj.Order
        self.labelBofroe=obj.Label
        self.flagShape=True
        self.flagPlacement=True
        self.flagExcute=False
        obj.setEditorMode('Placement',2)
        obj.setEditorMode('flagRedraw',2)
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
        if prop=="Area" or prop=="Line" :
            if self.flagShape:
                self.flagShape=False
                self.flagPlacement=False
                #将物体置为原点
                fp.Placement=FreeCAD.Placement(FreeCAD.Vector(0.0,0.0,0.0),FreeCAD.Rotation(0.0,0.0,0.0,1.0))
                # self.redraw(fp)
                self.flagShape=True
                self.flagPlacement=True
                self.flagExcute=True

        ObjectsTools.fucAttributeChange(fp,prop)
        
        ObjectsTools.fucNonUniformGrid(self.curCoordinateSystem,fp,prop)
        # elif prop=="X" or prop=="Y" or prop=="Z" or prop=="R" or prop=="Theta":
        #     #控制非均匀网格是否显示
        #     ObjectsTools.fucNonUniformGrid(self.curCoordinateSystem,fp)
            
    def redraw(self,obj):
        try :
            objLine=FreeCAD.ActiveDocument.getObjectsByLabel(obj.Line)[0]
            objArea=FreeCAD.ActiveDocument.getObjectsByLabel(obj.Area)[0]
            path=Part.Wire(objLine.Shape)
            obj.Shape=path.makePipeShell([objArea.Shape.Wires[0]],True,True)
            # shape1=path.makePipeShell([objArea.Shape.Wires[0]],True,True)
            # shape2=objArea.Shape
            # shape3=
        except :
            FreeCAD.Console.PrintMessage("ExtrudedInstance failed\n")
        ObjectsTools.doSomethingAfterRecomputerVolShape(obj)
        

    def execute(self, fp):
        ''' Print a short message when doing a recomputation, this method is mandatory '''
        #设置自定义属性可编辑
        if self.flagExcute:
            self.redraw(fp)
            self.flagExcute=False
       

    def __getstate__(self):
        state={}
        state["curCoordinateSystem"]=self.curCoordinateSystem
        state["flagShape"]=self.flagShape
        state["flagPlacement"]=self.flagPlacement
        state["flagExcute"]=self.flagExcute
        return state
    
    def __setstate__(self,state):
        self.curCoordinateSystem=state["curCoordinateSystem"]
        self.flagShape=True
        self.flagPlacement=state["flagPlacement"] 
        self.flagExcute=state["flagExcute"]


 

class ViewProviderExtruded:
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
