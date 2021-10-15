#-*- coding: utf-8 -*-
import FreeCAD, Part, math
from FreeCAD import Base
from pivy import coin

from Common.Tools import CoordinateSystemTools,PlacementTools,ObjectsTools,DocumentTools

class Tetrahedron:
    def __init__(self, obj):
        # 这里加一个flagRedraw是为了能够通过obj的这个属性的改变，使得这个模型可以间接调用redraw函数
        obj.addProperty("App::PropertyBool","flagRedraw","","").flagRedraw=True
        self.curCoordinateSystem=FreeCAD.ActiveDocument.CoordinateSystem
        self.vectorList=[]
        ''' Add some custom properties to our Tetrahedron feature '''
        if self.curCoordinateSystem==CoordinateSystemTools.CoordinateType.Rectangular:
            obj.addProperty("App::PropertyVectorDistance","Point_1","Object of a Tetrahedron","Corner Point_1 of the Tetrahedron").Point_1=FreeCAD.Vector(0,0,0)
            obj.addProperty("App::PropertyVectorDistance","Point_2","Object of a Tetrahedron","Corner Point_2 of the Tetrahedron").Point_2=FreeCAD.Vector(0.05,0,0)
            obj.addProperty("App::PropertyVectorDistance","Point_3","Object of a Tetrahedron","Corner Point_3 of the Tetrahedron").Point_3=FreeCAD.Vector(0.05,0.05,0)
            obj.addProperty("App::PropertyVectorDistance","Point_4","Object of a Tetrahedron","Corner Point_4 of the Tetrahedron").Point_4=FreeCAD.Vector(0,0.05,0)
            # obj.addProperty("App::PropertyVectorDistance","Point_5","Object of a Tetrahedron","peak of the Tetrahedron").Point_5=FreeCAD.Vector(0,0,5)
            self.vectorList=[obj.Point_1,obj.Point_2,obj.Point_3,obj.Point_4]
        elif self.curCoordinateSystem==CoordinateSystemTools.CoordinateType.Polar:
            obj.addProperty("App::PropertyPolVecDistance","Point_1","Object of a Tetrahedron","Corner Point_1 of the Tetrahedron").Point_1=FreeCAD.Vector(0,0,0)
            obj.addProperty("App::PropertyPolVecDistance","Point_2","Object of a Tetrahedron","Corner Point_2 of the Tetrahedron").Point_2=FreeCAD.Vector(0.01,0,0)
            obj.addProperty("App::PropertyPolVecDistance","Point_3","Object of a Tetrahedron","Corner Point_3 of the Tetrahedron").Point_3=FreeCAD.Vector(0.01,90,0)
            obj.addProperty("App::PropertyPolVecDistance","Point_4","Object of a Tetrahedron","Corner Point_4 of the Tetrahedron").Point_4=FreeCAD.Vector(0,0,0.01)
            # obj.addProperty("App::PropertyPolVecDistance","Point_5","Object of a Tetrahedron","peak of the Tetrahedron").Point_5=FreeCAD.Vector(3,45,5)
            self.vectorList=[obj.Point_1,obj.Point_2,obj.Point_3,obj.Point_4]
        else:
            obj.addProperty("App::PropertyCylinderVecDistance","Point_1","Object of a Tetrahedron","Corner Point_1 of the Tetrahedron").Point_1=FreeCAD.Vector(0,0,0)
            obj.addProperty("App::PropertyCylinderVecDistance","Point_2","Object of a Tetrahedron","Corner Point_2 of the Tetrahedron").Point_2=FreeCAD.Vector(0.02,30,0)
            obj.addProperty("App::PropertyCylinderVecDistance","Point_3","Object of a Tetrahedron","Corner Point_3 of the Tetrahedron").Point_3=FreeCAD.Vector(0.04,60,0)
            obj.addProperty("App::PropertyCylinderVecDistance","Point_4","Object of a Tetrahedron","Corner Point_4 of the Tetrahedron").Point_4=FreeCAD.Vector(0.03,80,0)
            # obj.addProperty("App::PropertyCylinderVecDistance","Point_5","Object of a Tetrahedron","peak of the Tetrahedron").Point_5=FreeCAD.Vector(3,45,5)
            self.vectorList=[obj.Point_1,obj.Point_2,obj.Point_3,obj.Point_4]
        obj.addProperty("App::PropertyInteger","Order","","Order of the Conformal").Order=100
        ObjectsTools.addPropertyForVol(obj,ObjectsTools.ObjectType.Vol_Tetrahedron,self.curCoordinateSystem)
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
        if prop=="Point_1" or prop=="Point_2"  or prop=="Point_3"  or prop=="Point_4"  :
            if self.flagShape:
                self.flagShape=False
                self.flagPlacement=False
                #将物体置为原点
                fp.Placement=FreeCAD.Placement(FreeCAD.Vector(0.0,0.0,0.0),FreeCAD.Rotation(0.0,0.0,0.0,1.0))
                self.vectorList=[fp.Point_1,fp.Point_2,fp.Point_3,fp.Point_4]
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
                fp.setEditorMode("Point_3",1)
                fp.setEditorMode("Point_4",1)
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
                fp.Point_1=resultVectors[0]
                fp.Point_2=resultVectors[1]
                fp.Point_3=resultVectors[2]
                fp.Point_4=resultVectors[3]
                self.vectorList=[fp.Point_1,fp.Point_2,fp.Point_3,fp.Point_4]
                self.flagPlacement=True
                self.flagShape=True
                self.flagExcute=False
                # 重塑
                pass
        ObjectsTools.fucNonUniformGrid(self.curCoordinateSystem,fp,prop)
        ObjectsTools.fucAttributeChange(fp,prop)

    def redraw(self,fp):
        try:
            tempPoints=CoordinateSystemTools.otherToRec(self.curCoordinateSystem,self.vectorList)
            tempPoint_1=tempPoints[0]
            tempPoint_2=tempPoints[1]
            tempPoint_3=tempPoints[2]
            tempPoint_4=tempPoints[3]

            
            buttom_wire= Part.makePolygon([tempPoint_1, tempPoint_2, tempPoint_3, tempPoint_1])
            # buttom_wire_right_top = Part.makePolygon([tempPoint_2, tempPoint_3, tempPoint_4, tempPoint_2])
            front_wire = Part.makePolygon([tempPoint_1, tempPoint_2, tempPoint_4, tempPoint_1])
            # back_wire = Part.makePolygon([tempPoint_3, tempPoint_5, tempPoint_4, tempPoint_3])
            left_wire = Part.makePolygon([tempPoint_1, tempPoint_3, tempPoint_4, tempPoint_1])
            right_wire = Part.makePolygon([tempPoint_2, tempPoint_4, tempPoint_3, tempPoint_2])
            bottom_face = Part.makeFace(buttom_wire, "Part::FaceMakerExtrusion")
            # buttom_face_right_top = Part.makeFace(buttom_wire_right_top, "Part::FaceMakerExtrusion")
            front_face = Part.makeFace(front_wire, "Part::FaceMakerExtrusion")
            # back_face = Part.makeFace(back_wire, "Part::FaceMakerExtrusion")
            right_face = Part.makeFace(right_wire, "Part::FaceMakerExtrusion")
            left_face = Part.makeFace(left_wire, "Part::FaceMakerExtrusion")
            # 每个面都划分为三角形
            fp.Shape = Part.makeShell([front_face,
                                bottom_face,
                                right_face,
                                left_face])
            fp.Shape= Part.makeSolid(fp.Shape)
        except:
            DocumentTools.printErrorMessage("Redraw Tetrahedron Failed!")
        ObjectsTools.doSomethingAfterRecomputerVolShape(fp)
        
    def execute(self, fp):
        ''' Print a short message when doing a recomputation, this method is mandatory '''
        '''API中自带有建立楔形体，后面可参看'''
        #设置自定义属性可编辑
        fp.setEditorMode("Point_1",0)
        fp.setEditorMode("Point_2",0)
        fp.setEditorMode("Point_3",0)
        fp.setEditorMode("Point_4",0)
        if self.flagExcute:
            self.redraw(fp)
            self.flagExcute=False
        # buttom_wire_left_bottom = Part.makePolygon([fp.Point_1, fp.Point_2, fp.Point_4, fp.Point_1])
        # buttom_wire_right_top = Part.makePolygon([fp.Point_2, fp.Point_3, fp.Point_4, fp.Point_2])
        # front_wire = Part.makePolygon([fp.Point_1, fp.Point_2, fp.Point_5, fp.Point_1])
        # back_wire = Part.makePolygon([fp.Point_3, fp.Point_5, fp.Point_4, fp.Point_3])
        # left_wire = Part.makePolygon([fp.Point_1, fp.Point_5, fp.Point_4, fp.Point_1])
        # right_wire = Part.makePolygon([fp.Point_2, fp.Point_5, fp.Point_3, fp.Point_2])
        # bottom_face_left_bottom = Part.makeFace(buttom_wire_left_bottom, "Part::FaceMakerExtrusion")
        # buttom_face_right_top = Part.makeFace(buttom_wire_right_top, "Part::FaceMakerExtrusion")
        # front_face = Part.makeFace(front_wire, "Part::FaceMakerExtrusion")
        # back_face = Part.makeFace(back_wire, "Part::FaceMakerExtrusion")
        # right_face = Part.makeFace(right_wire, "Part::FaceMakerExtrusion")
        # left_face = Part.makeFace(left_wire, "Part::FaceMakerExtrusion")
        # # 每个面都划分为三角形
        # fp.Shape = Part.makeShell([front_face,
        #                       bottom_face_left_bottom,
        #                       buttom_face_right_top,
        #                       right_face,
        #                       left_face,
        #                       back_face])
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


class ViewProviderTetrahedron:
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
            static const char * ViewProviderTetrahedron_xpm[] = {
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


    def __setstate__(self,state):
        ''' When restoring the pickled object from document we have the chance to set some
        internals here. Since no data were pickled nothing needs to be done here.
        '''
        return None