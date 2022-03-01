# -*- coding: utf-8 -*-
import FreeCAD
import Part
from Common.Tools import CoordinateSystemTools, PlacementTools, ObjectsTools

from File.FileCommand.M3DFile import M3DFileUtil


from Modeling3D import Modeling3D_rc

if FreeCAD.GuiUp:
    import FreeCADGui
    from PySide import QtCore, QtGui
    from DraftTools import translate
    from PySide.QtCore import QT_TRANSLATE_NOOP
else:
    # \cond
    def translate(ctxt,txt):
        return txt
    def QT_TRANSLATE_NOOP(ctxt,txt):
        return txt
    # \endcond

class PointObj:
    def __init__(self, obj):
        self.curCoordinateSystem=FreeCAD.ActiveDocument.CoordinateSystem
        self.vectorList=[]
        ''' Add some custom properties to our box feature '''
        if self.curCoordinateSystem=='Rectangular':
            obj.addProperty("App::PropertyVectorDistance", "Point", "Object of a Point", "Length of the box").Point = FreeCAD.Vector(0.01,0.01,0.01)
            
        # '''极坐标系下的属性面板'''
        elif self.curCoordinateSystem=='Polar':
            obj.addProperty("App::PropertyPolVecDistance", QT_TRANSLATE_NOOP("App::Property","Point"), "Object of a Point", QT_TRANSLATE_NOOP("App::Property","The position of Point")).Point = FreeCAD.Vector(1,0,1)
            # obj.addProperty("App::PropertyPolarVector", "Test", "Point", "Length of the box").Test = FreeCAD.Vector(1,45,1)
        elif self.curCoordinateSystem=='Cylindrical':
            obj.addProperty("App::PropertyCylinderVecDistance", "Point", "Object of a Point", "Length of the box").Point = FreeCAD.Vector(1,0,1)
        self.vectorList.append(obj.Point)
        obj.addProperty("App::PropertyString", "Type", "Object of a Point", "Length of the box").Type = ObjectsTools.ObjectType.Point
        obj.addProperty("App::PropertyInteger","Order","","Order of the Conformal").Order=100
        ObjectsTools.addNonUniformGridAttribute(self.curCoordinateSystem,obj)

        obj.Proxy = self
        self.placementBefore = obj.Placement
        self.orderBefore=obj.Order
        self.labelBofroe=obj.Label
        #flagShape和flagPalcement为在移动过程中不能在属性面板中输入值，在输入值的时候不移动
        self.flagShape=True
        self.flagPlacement=True
        self.flagExcute=False

        obj.setEditorMode('Placement',2)
        obj.setEditorMode('Type',2)
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
        if prop == "Placement":
            self.placementBefore = FreeCAD.Placement(obj.Placement)
            # self.flag=True
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
        elif prop == "Point" :
            try:
                if self.flagShape:
                    self.flagShape=False
                    self.flagPlacement=False
                    # fp.Placement=FreeCAD.Placement((fp.Point.sub(fp.Point_2).multiply(0.5),fp.Placement.Rotation))
                    fp.Placement=FreeCAD.Placement(FreeCAD.Vector(0.0,0.0,0.0),FreeCAD.Rotation(0.0,0.0,0.0,1.0))
                    self.vectorList=[fp.Point]
                    self.flagShape=True
                    self.flagPlacement=True
                    self.flagExcute=True
            except :
                FreeCAD.Console.PrintMessage("Onchange Wrong!\n")
                pass
            
        elif prop == "Placement" :
            if self.flagPlacement:
                self.flagPlacement=False
                self.flagShape=False
                # 设置属性为只读
                fp.setEditorMode("Point",1)
                #坐标转换
                vectorList=CoordinateSystemTools.otherToRec(self.curCoordinateSystem,self.vectorList)
                #转换结束
                pos=fp.Placement.Base.sub(self.placementBefore.Base)
                resultVectors=[]
                if pos != FreeCAD.Vector(0.0,0.0,0.0):
                    resultVectors=PlacementTools.moveAdd(pos,vectorList)
                else:
                    resultVectors=PlacementTools.rotate(self.placementBefore,fp.Placement,vectorList)
                resultVectors=CoordinateSystemTools.recToOther(self.curCoordinateSystem,resultVectors)

                #转换完成
                fp.Point=resultVectors[0]
                self.vectorList=[fp.Point]
                self.flagPlacement=True
                self.flagShape=True
                self.flagExcute=False
        
        ObjectsTools.fucNonUniformGrid(self.curCoordinateSystem,fp,prop)
        # elif prop=="X" or prop=="Y" or prop=="Z" or prop=="R" or prop=="Theta":
        #     #控制非均匀网格是否显示
        #     ObjectsTools.fucNonUniformGrid(self.curCoordinateSystem,fp)
    def redraw(self,obj):
        try:
            tempPoints=CoordinateSystemTools.otherToRec(self.curCoordinateSystem,self.vectorList)
            tempPoint=tempPoints[0]  
            obj.Shape=Part.makeSphere(0.0001,tempPoint)
        except:
            FreeCAD.Console.PrintMessage("Error!  Redraw Point")
            pass
        

    def execute(self, fp):
        # print "print:"+str(fp.Name)+str(fp.Point)+"\n"
        #打印文件的输出
        # pointXYZ=[fp.Point.x,fp.Point.y,fp.Point.z]
        # print  OperationCommands.getPointCommands(fp.Name,pointXYZ)
        # print  DocumentTools.getMarkCommands(fp.Name)
        #结束打印
        fp.setEditorMode("Point",0)
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



class ViewProviderPoint:
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

    def getDisplayModes(self, obj):
        ''' Return a list of display modes. '''
        modes = []
        return modes

    def getDefaultDisplayMode(self):
        ''' Return the name of the default display mode. It must be defined in getDisplayModes. '''
        return "Flat Lines"

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
