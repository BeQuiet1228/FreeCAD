#-*- coding: utf-8 -*-
import FreeCAD, Part, math
from FreeCAD import Base
from pivy import coin

from Common.Tools import CoordinateSystemTools,DocumentTools,ObjectsTools,PlacementTools
class Toroidal_Section:
    def __init__(self, obj):
        
        # 这里加一个flagRedraw是为了能够通过obj的这个属性的改变，使得这个模型可以间接调用redraw函数
        obj.addProperty("App::PropertyBool","flagRedraw","","").flagRedraw=True
        self.curCoordinateSystem=FreeCAD.ActiveDocument.CoordinateSystem
        self.vectorList=[]
        ''' Add some custom properties to our Toroidal_Section feature '''
        if self.curCoordinateSystem==CoordinateSystemTools.CoordinateType.Rectangular:
            obj.addProperty("App::PropertyVectorDistance","Point1","Object of a Toroidal_Section","Point1 of the Toroidal_Section").Point1=FreeCAD.Vector(0.002,0.002,0)
            obj.addProperty("App::PropertyVectorDistance","Point2","Object of a Toroidal_Section","Point2 of the Toroidal_Section").Point2=FreeCAD.Vector(0.002,0.002,0.002)
            obj.addProperty("App::PropertyVectorDistance","Point3","Object of a Toroidal_Section","Point3 of the Toroidal_Section").Point3=FreeCAD.Vector(0.003,0.003,0)
            obj.addProperty("App::PropertyVectorDistance","Point4","Object of a Toroidal_Section","Point4 of the Toroidal_Section").Point4=FreeCAD.Vector(0.001,0.001,0)
            
            obj.addProperty("App::PropertyLength","MajorRadius","Object of a Toroidal_Section"," Radius of the Toroidal_Section").MajorRadius=0.002
            obj.addProperty("App::PropertyLength","MinorRadius","Object of a Toroidal_Section"," Radius of the Toroidal_Section").MinorRadius=0.0005

        elif self.curCoordinateSystem==CoordinateSystemTools.CoordinateType.Polar:
            obj.addProperty("App::PropertyPolVecDistance","Point1","Object of a Toroidal_Section","Point1 of the Toroidal_Section").Point1=FreeCAD.Vector(0.002,45,0)
            obj.addProperty("App::PropertyPolVecDistance","Point2","Object of a Toroidal_Section","Point2 of the Toroidal_Section").Point2=FreeCAD.Vector(0.002,45,0.002)
            obj.addProperty("App::PropertyPolVecDistance","Point3","Object of a Toroidal_Section","Point3 of the Toroidal_Section").Point3=FreeCAD.Vector(0.003,45,0)
            obj.addProperty("App::PropertyPolVecDistance","Point4","Object of a Toroidal_Section","Point4 of the Toroidal_Section").Point4=FreeCAD.Vector(0.001,45,0)
            
            # obj.addProperty("App::PropertyLength","Radius","Object of a Toroidal_Section","Radius of the Toroidal_Section").Radius=5.0
            obj.addProperty("App::PropertyLength","MajorRadius","Object of a Toroidal_Section"," Radius of the Toroidal_Section").MajorRadius=0.005
            obj.addProperty("App::PropertyLength","MinorRadius","Object of a Toroidal_Section"," Radius of the Toroidal_Section").MinorRadius=0.001
        else:
            obj.addProperty("App::PropertyCylinderVecDistance","Point1","Object of a Toroidal_Section","Point1 of the Toroidal_Section").Point1=FreeCAD.Vector(0.002,45,0)
            obj.addProperty("App::PropertyCylinderVecDistance","Point2","Object of a Toroidal_Section","Point2 of the Toroidal_Section").Point2=FreeCAD.Vector(0.002,45,0.002)
            obj.addProperty("App::PropertyCylinderVecDistance","Point3","Object of a Toroidal_Section","Point3 of the Toroidal_Section").Point3=FreeCAD.Vector(0.003,45,0)
            obj.addProperty("App::PropertyCylinderVecDistance","Point4","Object of a Toroidal_Section","Point4 of the Toroidal_Section").Point4=FreeCAD.Vector(0.001,45,0)
            # obj.addProperty("App::PropertyLength","Radius","Object of a Toroidal_Section","Radius of the Toroidal_Section").Radius=5.0
            obj.addProperty("App::PropertyLength","MajorRadius","Object of a Toroidal_Section"," Radius of the Toroidal_Section").MajorRadius=0.005
            obj.addProperty("App::PropertyLength","MinorRadius","Object of a Toroidal_Section"," Radius of the Toroidal_Section").MinorRadius=0.001
        self.vectorList=[obj.Point1,obj.Point2,obj.Point3,obj.Point4]
        obj.addProperty("App::PropertyInteger","Order","","Order of the Conformal").Order=100
        ObjectsTools.addPropertyForVol(obj,ObjectsTools.ObjectType.Vol_Toroidal_Section,self.curCoordinateSystem)

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
        if prop=="Point1" or prop=="Point2" or prop=="Point3" or prop=="Point4" or prop=="MinorRadius" or prop=="MajorRadius" :
            if self.flagShape:
                self.flagShape=False
                self.flagPlacement=False
                #将物体置为原点
                fp.Placement=FreeCAD.Placement(FreeCAD.Vector(0.0,0.0,0.0),FreeCAD.Rotation(0.0,0.0,0.0,1.0))
                self.vectorList=[fp.Point1,fp.Point2,fp.Point3,fp.Point4]
                self.flagShape=True
                self.flagPlacement=True
                self.flagExcute=True
        
        elif prop == "Placement" :
            if self.flagPlacement:
                self.flagPlacement=False
                self.flagShape=False
                #设置属性自定义属性只读
                fp.setEditorMode("Point1",1)
                fp.setEditorMode("Point2",1)
                fp.setEditorMode("Point3",1)
                fp.setEditorMode("Point4",1)
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
                fp.Point3=resultVectors[2]
                fp.Point4=resultVectors[3]
                self.vectorList=[obj.Point1,obj.Point2,obj.Point3,obj.Point4]
                self.flagPlacement=True
                self.flagShape=True
                self.flagExcute=False
                # 重塑
                pass
        ObjectsTools.fucNonUniformGrid(self.curCoordinateSystem,fp,prop) 
        ObjectsTools.fucAttributeChange(fp,prop)           

    # 1、找到控制角度的点与大弧线之间的交点：投影
    # 2、通过中心和两个端点求出这三个点中间另外一点，
    # 3、通过弧上三个点求出这条弧线，
    # 4、求出圆面，是圆面扫掠弧线形成最终物体
    def redraw(self,obj):
        tempPoints=CoordinateSystemTools.otherToRec(self.curCoordinateSystem,self.vectorList)
        tempPoint_1=tempPoints[0]
        tempPoint_2=tempPoints[1]
        tempPoint_3=tempPoints[2]
        tempPoint_4=tempPoints[3]

        # 法向normal
        normal=tempPoint_2.sub(tempPoint_1)
        try:
            normal=normal.normalize()
        except Base.FreeCADError as e:
            DocumentTools.printErrorMessage(e)
            return
            pass
        # normal=normal.normalize()

        vec3Temp=tempPoint_3.sub(tempPoint_1)
        vec4Temp=tempPoint_4.sub(tempPoint_1)
        # 求方向点point3与弧线的交点
        vec3ProjectToPlan=vec3Temp.projectToPlane(FreeCAD.Vector(0.0,0.0,0.0),normal)

        # k为原点到弧的交点与VecProjectToPlan长度的比例因子
        kMajorRadiusRatioVec3=1.0
        if not vec3ProjectToPlan.Length==0.0:
            kMajorRadiusRatioVec3=obj.MajorRadius.Value/vec3ProjectToPlan.Length

        tempVec3OnArc=kMajorRadiusRatioVec3*vec3ProjectToPlan
        vec3OnArc=tempVec3OnArc.add(tempPoint_1)

        # 求方向点point4与弧线的交点
        vec4ProjectToPlan=vec4Temp.projectToPlane(FreeCAD.Vector(0.0,0.0,0.0),normal)
        # k为原点到弧的交点与VecProjectToPlan长度的比例因子
        try:
            kMajorRadiusRatioVec4=obj.MajorRadius.Value/vec4ProjectToPlan.Length
        except exceptions.ZeroDivisionError as e:
            DocumentTools.printErrorMessage(e)
            return
            pass
        # kMajorRadiusRatioVec4=obj.MajorRadius.Value/vec4ProjectToPlan.Length
        tempVec4OnArc=kMajorRadiusRatioVec4*vec4ProjectToPlan
        vec4OnArc=tempVec4OnArc.add(tempPoint_1)



        # 两个向量，原点与端点
        vec3=vec3OnArc.sub(tempPoint_1)

        vec4=vec4OnArc.sub(tempPoint_1)



        # 求两个点的夹角
        angle=vec3.getAngle(vec4)*180/math.pi

        # 在原点位置将点旋转angle/2度
        # 将度数转化为弧度
        # q=(vNormal*sin(θ/2)，cos(θ/2))  θ是需要旋转的角度
        sinValue=math.sin(angle/4.0*math.pi/180.0)
        cosValue=math.cos(angle/4.0*math.pi/180.0)
        # 四元数
        
        q=FreeCAD.Rotation(sinValue*normal.x,sinValue*normal.y,sinValue*normal.z,cosValue)

        # 在原点旋转后的点
        vOrigin=q.multVec(vec3)

        # 平移到point1的位置
        vPoint1=vOrigin.add(tempPoint_1)

        try:
            arc=Part.ArcOfCircle(vec3OnArc,vPoint1,vec4OnArc)
        except Part.OCCError as e:
            DocumentTools.printErrorMessage(e)
            return
            pass
        # arc=Part.ArcOfCircle(vec3OnArc,vPoint1,vec4OnArc)

        arcShape=arc.toShape()
        # Part.show(arcShape)
        # arcShape.Label="ArcShape"
        path=Part.Wire(arcShape)
        
        # 求圆面的法向量
        normalCircle=vec3.cross(normal).negative()
        circle=Part.makeCircle(obj.MinorRadius,vec3OnArc,normalCircle)

        # Part.show(circle)
        # circle.Label="Circle"
        circleFace=Part.makeFace([Part.Wire(circle)],"Part::FaceMakerBullseye")
        obj.Shape=path.makePipe(circleFace)

        ObjectsTools.doSomethingAfterRecomputerVolShape(obj)

        # tempPoints=CoordinateSystemTools.otherToRec(self.curCoordinateSystem,self.vectorList)
        # tempPoint_0=tempPoints[0]
        # if obj.Radius==0.0:
        #     DocumentTools.errorMessage("",QtGui.QApplication.translate(
        #                                   "Toroidal_SectionInstance",
        #                                   "Radius cann't be 0.",
        #                                   None))
        #     return
        # obj.Shape = Part.makeSphere(obj.Radius, tempPoint_0)
    def execute(self, fp):
        ''' Print a short message when doing a recomputation, this method is mandatory '''
        #设置自定义属性可编辑
        fp.setEditorMode("Point1",0)
        fp.setEditorMode("Point2",0)
        fp.setEditorMode("Point3",0)
        fp.setEditorMode("Point4",0)

        if self.flagExcute:
            self.redraw(fp)
            self.flagExcute=False
        # FreeCAD.Console.PrintMessage("Recompute Python Toroidal_Section feature\n")
        # obj = Part.makeToroidal_Section(fp.Radius, fp.Point1)
        # fp.Shape = obj

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
class ViewProviderToroidal_Section:
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
            static const char * ViewProviderToroidal_Section_xpm[] = {
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
