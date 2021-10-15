# -*- coding: utf-8 -*-
import FreeCAD, Part, math
from FreeCAD import Base
from pivy import coin
from PySide import QtGui, QtCore
from Common.Tools import CoordinateSystemTools,DocumentTools,ObjectsTools
from Common.Tools import PlacementTools,ObjectsTools

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

class Annular:
    def __init__(self, obj,needOrder=True,thistype=""):
        '''
        needOrder: 是否需要order;
        thistype: 不为空指定type，否则默认type
        '''
        # 这里加一个flagRedraw是为了能够通过obj的这个属性的改变，使得这个模型可以间接调用redraw函数
        obj.addProperty("App::PropertyBool","flagRedraw","","").flagRedraw=True
        self.curCoordinateSystem=FreeCAD.ActiveDocument.CoordinateSystem
        self.vectorList=[]
        ''' Add some custom properties to our box feature '''
        if self.curCoordinateSystem=='Rectangular':
            obj.addProperty("App::PropertyVectorDistance", "Point_1", "Object of a Annular", "Length of the box").Point_1 = FreeCAD.Vector(0.003,0,0)
            obj.addProperty("App::PropertyVectorDistance", "Point_2", "Object of a Annular", "Length of the box").Point_2 = FreeCAD.Vector(0.004,0,0)
            self.vectorList=[obj.Point_1,obj.Point_2]

            obj.addProperty("App::PropertyLength", "RadiusInside", "Object of a Annular", "Width of the box").RadiusInside = 0.001
            obj.addProperty("App::PropertyLength", "RadiusOutside", "Object of a Annular", "Height of the box").RadiusOutside = 0.01
        # '''极坐标系下的属性面板'''
        elif self.curCoordinateSystem=='Polar':
            obj.addProperty("App::PropertyPolVecDistance", "Point_1", "Object of a Annular", "Length of the box").Point_1 = FreeCAD.Vector(0,0,0)
            obj.addProperty("App::PropertyPolVecDistance", "Point_2", "Object of a Annular", "Length of the box").Point_2 = FreeCAD.Vector(0,0,0.001)
            self.vectorList=[obj.Point_1,obj.Point_2]
            obj.addProperty("App::PropertyLength", "RadiusInside", "Object of a Annular", "Width of the box").RadiusInside = "1.0 mm"
            obj.addProperty("App::PropertyLength", "RadiusOutside", "Object of a Annular", "Height of the box").RadiusOutside = "10.0 mm"
        elif self.curCoordinateSystem=='Cylindrical':
            obj.addProperty("App::PropertyCylinderVecDistance", "Point_1", "Object of a Annular", "Length of the box").Point_1 = FreeCAD.Vector(0,0,0)
            obj.addProperty("App::PropertyCylinderVecDistance", "Point_2", "Object of a Annular", "Length of the box").Point_2 = FreeCAD.Vector(0,0,0.001)
            self.vectorList=[obj.Point_1,obj.Point_2]
            obj.addProperty("App::PropertyLength", "RadiusInside", "Object of a Annular", "Width of the box").RadiusInside = "1.0 mm"
            obj.addProperty("App::PropertyLength", "RadiusOutside", "Object of a Annular", "Height of the box").RadiusOutside = "10.0 mm"
        if needOrder:
            obj.addProperty("App::PropertyInteger","Order","","Order of the Conformal").Order=100
        if thistype=="":
            ObjectsTools.addPropertyForVol(obj,ObjectsTools.ObjectType.Vol_Annular,self.curCoordinateSystem)
        else:
            ObjectsTools.addPropertyForVol(obj,thistype,self.curCoordinateSystem)
        obj.Proxy = self
        self.placementBefore = obj.Placement
        # self.placementBaseBefore=FreeCAD.Vector([obj.Placement.Base.x,obj.Placement.Base.y,obj.Placement.Base.z])
        # self.placementRotationBefore=obj.Placement.Rotation.Q
        self.radiusInsideBefore=obj.RadiusInside.Value
        self.radiusOutsideBefore=obj.RadiusOutside.Value
        if needOrder:
            self.orderBefore=obj.Order
        self.labelBofroe=obj.Label

        self.isRadiusInsideChange=False
        self.isRadiusOutsideChange=False
        # 控制onBeforeChange和redraw中半径相等为0 时互斥访问
        self.flagRadius=True
        #flagShape和flagPalcement为在移动过程中不能在属性面板中输入值，在输入值的时候不移动
        self.flagShape=True
        self.flagPlacement=True
        self.flagExcute=False
        obj.setEditorMode('Placement',2)
        obj.setEditorMode('flagRedraw',2)
        if needOrder:
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
        if prop=="Order":
            self.orderBefore=obj.Order
        elif prop=="Label":
            self.labelBofroe=obj.Label
        elif prop == "Placement":
            self.placementBefore = FreeCAD.Placement(obj.Placement)
            # self.placementBaseBefore=FreeCAD.Vector([obj.Placement.Base.x,obj.Placement.Base.y,obj.Placement.Base.z])
            # self.placementRotationBefore=[obj.Placement.Rotation.Q[0],obj.Placement.Rotation.Q[1],obj.Placement.Rotation.Q[2],obj.Placement.Rotation.Q[3]]
        elif prop=="RadiusInside":
            # print self.placementBefore
            if hasattr(self,"flagRadius"):
                if self.flagRadius:
                    self.flagRadius=False
                    self.radiusInsideBefore=obj.RadiusInside.Value
                    self.isRadiusInsideChange=True
                    self.isRadiusOutsideChange=False
                    self.flagRadius=True
        elif prop=="RadiusOutside":
            if hasattr(self,"flagRadius"):
                if self.flagRadius:
                    self.flagRadius=False
                    self.radiusOutsideBefore=obj.RadiusOutside.Value
                    self.isRadiusOutsideChange=True
                    self.isRadiusInsideChange=False
                    self.flagRadius=True
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
        if prop == "Point_1" or prop == "Point_2" or prop == "RadiusInside" or prop == "RadiusOutside":     
            if self.flagShape:
                self.flagShape=False
                self.flagPlacement=False
                #将物体置为原点
                fp.Placement=FreeCAD.Placement(FreeCAD.Vector(0.0,0.0,0.0),FreeCAD.Rotation(0.0,0.0,0.0,1.0))
                self.vectorList=[fp.Point_1,fp.Point_2]
                self.flagShape=True
                self.flagPlacement=True
                self.flagExcute=True           
        elif prop == "Placement" :
            if self.flagPlacement:
                self.flagPlacement=False
                self.flagShape=False
                #设置属性自定义属性只读
                fp.setEditorMode("Point_1",1)
                fp.setEditorMode("Point_2",1)
                #坐标转换
                vectorList=CoordinateSystemTools.otherToRec(self.curCoordinateSystem,self.vectorList)
                #转换结束
                pos = fp.Placement.Base.sub(self.placementBefore.Base)
                # pos = fp.Placement.Base.sub(self.placementBaseBefore)
                resultVectors=[]
                #
                #位移
                if pos!=FreeCAD.Vector(0.0,0.0,0.0):
                    resultVectors=PlacementTools.moveAdd(pos,vectorList)
                #旋转
                else:
                    # resultVectors=PlacementTools.rotate(FreeCAD.Placement(FreeCAD.Vector(self.placementBaseBefore),FreeCAD.Rotation(self.placementRotationBefore[0],self.placementRotationBefore[1],self.placementRotationBefore[2],self.placementRotationBefore[3])),fp.Placement,vectorList)
                    resultVectors=PlacementTools.rotate(self.placementBefore,fp.Placement,vectorList)
                resultVectors=CoordinateSystemTools.recToOther(self.curCoordinateSystem,resultVectors)
                #转换完成
                fp.Point_1=resultVectors[0]
                fp.Point_2=resultVectors[1]
                self.vectorList=[fp.Point_1,fp.Point_2]
                self.flagPlacement=True
                self.flagShape=True
                self.flagExcute=False
                # 重塑
                pass
                # elif prop=="Attribute":
        ObjectsTools.fucAttributeChange(fp,prop)
        
        ObjectsTools.fucNonUniformGrid(self.curCoordinateSystem,fp,prop)
        # elif prop=="X" or prop=="Y" or prop=="Z" or prop=="R" or prop=="Theta":
        #     #控制非均匀网格是否显示
        #     ObjectsTools.fucNonUniformGrid(self.curCoordinateSystem,fp)
    def redraw(self,obj):
        tempPoints=CoordinateSystemTools.otherToRec(self.curCoordinateSystem,self.vectorList)
        tempPoint_0=tempPoints[0]
        tempPoint_1=tempPoints[1]
        if tempPoint_0==tempPoint_1:
            obj.Shape=ObjectsTools.makePoint(tempPoint_0)
            return 
        else:
            dir = tempPoint_1 - tempPoint_0
            wires=[]
            if obj.RadiusInside==0.0 and obj.RadiusOutside==0.0:
                if self.flagRadius:
                        self.flagRadius=False
                        if self.isRadiusInsideChange:
                            obj.RadiusInside=self.radiusInsideBefore
                            self.isRadiusInsideChange=False
                        else:
                            obj.RadiusOutside=self.radiusOutsideBefore
                            self.isRadiusOutsideChange=False
                        # reply = QtGui.QMessageBox.information(None,"","Houston, we have a problem")
                        DocumentTools.errorMessage(QtGui.QApplication.translate("AnnularInstance",
                                                                                "All of the radius of a Annular cann't be 0."))
                        self.flagExcute=False
                        self.flagRadius=True
            else:

                if not  obj.RadiusInside==0.0:
                    e1 = Part.makeCircle(obj.RadiusInside, tempPoint_0, dir)
                    wires.append(e1)
                    pass
                if not  obj.RadiusOutside==0.0:
                    e2 = Part.makeCircle(obj.RadiusOutside, tempPoint_0, dir)
                    wires.append(e2)
                    pass
                try:
                    line = Part.makeLine(tempPoint_0, tempPoint_1)
                    path = Part.Wire(line)
                    
                    # e1 = Part.makeCircle(obj.RadiusInside, tempPoint_0, dir)
                    # e2 = Part.makeCircle(obj.RadiusOutside, tempPoint_0, dir)
                    shapeCircle = Part.makeFace(wires, "Part::FaceMakerBullseye")
                    obj.Shape = path.makePipe(shapeCircle)
                    return 
                except NameError as e:
                    FreeCAD.Console.PrintMessage("Error",e)
        ObjectsTools.doSomethingAfterRecomputerVolShape(obj)
    def execute(self, fp):
        #设置自定义属性可编辑
        fp.setEditorMode("Point_1",0)
        fp.setEditorMode("Point_2",0)

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
    # def __getstate__(self):
    #     # return self.RadiusInside.Value,self.RadiusOutside.Value
    #     state={}
    #     state["curCoordinateSystem"]    =self.curCoordinateSystem
    #     state["flagShape"]              =self.flagShape
    #     state["flagPlacement"]          =self.flagPlacement
    #     state["flagExcute"]             =self.flagExcute
    #     state["flagRadius"]             =self.flagRadius
    #     state["radiusInsideBefore"]     =self.radiusInsideBefore
    #     state["radiusOutsideBefore"]    =self.radiusOutsideBefore
    #     state["orderBefore"]            =self.orderBefore
    #     state["labelBofroe"]            =self.labelBofroe
    #     state["isRadiusInsideChange"]   =self.isRadiusInsideChange
    #     state["isRadiusOutsideChange"]  =self.isRadiusOutsideChange
    #     state["placementBeforeBase"]    =list(self.placementBaseBefore)
    #     state["placementBeforeRotation"]=list(self.placementRotationBefore)
    #     # state["vectorList"]             =self.vectorList
    #     return state
    
    # def __setstate__(self,state):
    #     self.curCoordinateSystem        =state["curCoordinateSystem"]    
    #     self.flagShape                  =state["flagShape"]
    #     self.flagPlacement              =state["flagPlacement"] 
    #     self.flagExcute                 =state["flagExcute"]         
    #     self.flagRadius                 =state["flagRadius"]        
    #     self.radiusInsideBefore         =state["radiusInsideBefore"]  
    #     self.radiusOutsideBefore        =state["radiusOutsideBefore"]  
    #     self.orderBefore                =state["orderBefore"]     
    #     self.labelBofroe                =state["labelBofroe"]      
    #     self.isRadiusInsideChange       =state["isRadiusInsideChange"] 
    #     self.isRadiusOutsideChange      =state["isRadiusOutsideChange"] 
    #     # self.placementBefore.Base       =FreeCAD.Vector(state["placementBeforeBase"][0],state["placementBeforeBase"][1],state["placementBeforeBase"][2])
    #     self.placementBaseBefore       =FreeCAD.Vector(state["placementBeforeBase"])
    #     self.placementRotationBefore   =FreeCAD.Rotation(state["placementBeforeRotation"][0],state["placementBeforeRotation"][1],state["placementBeforeRotation"][2],state["placementBeforeRotation"][3])
       

    


    




class ViewProviderAnnular:
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
