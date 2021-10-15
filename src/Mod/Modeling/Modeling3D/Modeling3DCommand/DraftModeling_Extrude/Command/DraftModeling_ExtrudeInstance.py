#-*- coding: utf-8 -*-
import FreeCAD
import Part
from Common.Tools import CoordinateSystemTools,DocumentTools
from Common.Tools import ObjectsTools
from Common.Tools import PlacementTools

from File.FileCommand.M3DFile import M3DFileUtil


class DraftModeling_Extrude:
    def __init__(self, obj,Area="",Length=""):
        ''' Add some custom properties to our ConformalLine feature '''
        doc=FreeCAD.ActiveDocument
        self.curCoordinateSystem=FreeCAD.ActiveDocument.CoordinateSystem
        obj.addProperty("App::PropertyEnumeration", "Area", "Object of a DraftExtrude", "Area of the Extruded")
        obj.Area=ObjectsTools.getAreasByDoc(doc)
        FreeCAD.Console.PrintError("Areas: "+str(ObjectsTools.getAreasByDoc(doc)))
        obj.addProperty("App::PropertyDistance", "Length", "Object of a DraftExtrude", "Width of the box").Length = 0.001

        obj.addProperty("App::PropertyInteger","Order","","Order of a DraftExtrude").Order=100

        ObjectsTools.addPropertyForVol(obj,ObjectsTools.ObjectType.Vol_Draft_Extrude,self.curCoordinateSystem)


        obj.Proxy = self

        self.placementBefore = obj.Placement

        self.orderBefore=obj.Order
        self.labelBofroe=obj.Label


        #flagShape和flagPalcement为在移动过程中不能在属性面板中输入值，在输入值的时候不移动
        self.flagShape=True
        self.flagPlacement=True
        self.flagExcute=False
        obj.setEditorMode('Placement',2)

        self.initObject(obj)
        #初始化重绘
        self.redraw(obj)
        FreeCAD.Console.PrintMessage("end redraw\n")

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

        if prop == "Area" or prop == "Length":
            if self.flagShape:
                self.flagShape=False
                self.flagPlacement=False
                #将物体置为原点
                fp.Placement=FreeCAD.Placement(FreeCAD.Vector(0.0,0.0,0.0),FreeCAD.Rotation(0.0,0.0,0.0,1.0))
                self.flagShape=True
                self.flagPlacement=True
                self.flagExcute=True
        elif prop == "Placement" :
            return
            # if self.flagPlacement:
            #     self.flagPlacement=False
            #     self.flagShape=False
            #     #设置属性自定义属性只读
            #     fp.setEditorMode("Point_1",1)
            #     fp.setEditorMode("Point_2",1)
            #     #坐标转换
            #     vectorList=CoordinateSystemTools.otherToRec(self.curCoordinateSystem,self.vectorList)
            #     #转换结束
            #     pos = fp.Placement.Base.sub(self.placementBefore.Base)
            #     resultVectors=[]
            #     #
            #     #位移
            #     if pos!=FreeCAD.Vector(0.0,0.0,0.0):
            #         resultVectors=PlacementTools.moveAdd(pos,vectorList)
            #     #旋转
            #     else:
            #         resultVectors=PlacementTools.rotate(self.placementBefore,fp.Placement,vectorList)
            #     resultVectors=CoordinateSystemTools.recToOther(self.curCoordinateSystem,resultVectors)
            #     #转换完成
            #     fp.Point_1=resultVectors[0]
            #     fp.Point_2=resultVectors[1]
            #     self.vectorList=[fp.Point_1,fp.Point_2]
            #     self.flagPlacement=True
            #     self.flagShape=True
            #     self.flagExcute=False
            #     # 重塑
            #     pass
        # ObjectsTools.fucNonUniformGrid(self.curCoordinateSystem,fp,prop)
        ObjectsTools.fucAttributeChange(fp,prop)
    def redraw(self,obj):
        try:
            objArea=FreeCAD.ActiveDocument.getObjectsByLabel(obj.Area)[0]

            shape=Part.makeExtrude(objArea.Name,obj.Length.Value)
            FreeCAD.Console.PrintMessage("objArea: "+str(objArea.Name)+" length: "+str(obj.Length)+"\n")
            obj.Shape=shape
            FreeCAD.Console.PrintMessage("end redraw")
        except:
            DocumentTools.printErrorMessage("Redraw DraftModeling_Extrude Failed!")
    def execute(self, fp):
        FreeCAD.Console.PrintMessage("DraftModeling_Extrude excute\n")
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

class ViewProviderDraftModeling_Extrude:
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