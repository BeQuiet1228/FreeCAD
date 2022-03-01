#-*- coding: utf-8 -*-
import FreeCAD
import Part,math,copy
from Common.Tools import CoordinateSystemTools
from Common.Tools import PlacementTools, ObjectsTools,DocumentTools

class Polygonal:
    def __init__(self, obj):
        self.curCoordinateSystem=FreeCAD.ActiveDocument.CoordinateSystem
        self.vectorList=[]
        obj.addProperty("App::PropertyInteger","NumbersOfPoints","Object of a PolygonalArea","").NumbersOfPoints=3
        obj.addProperty("App::PropertyString","PropertyOfCoordinateSys","","")
        obj.setEditorMode('PropertyOfCoordinateSys',2)
        if self.curCoordinateSystem==CoordinateSystemTools.CoordinateType.Rectangular:
            obj.addProperty("App::PropertyVectorDistance","Point1","Object of a PolygonalArea","Point1 of the PolygonalArea").Point1=FreeCAD.Vector(0.001,0,0)
            obj.addProperty("App::PropertyVectorDistance","Point2","Object of a PolygonalArea","Point2 of the PolygonalArea").Point2=FreeCAD.Vector(0.001,0.001,0.001)
            obj.addProperty("App::PropertyVectorDistance","Point3","Object of a PolygonalArea","Point3 of the PolygonalArea").Point3=FreeCAD.Vector(0,0,0)
            obj.PropertyOfCoordinateSys="App::PropertyVectorDistance"
            pass
        elif self.curCoordinateSystem==CoordinateSystemTools.CoordinateType.Polar:
            obj.addProperty("App::PropertyPolVecDistance","Point1","Object of a PolygonalArea","Point1 of the PolygonalArea").Point1=FreeCAD.Vector(0.001,0,0)
            obj.addProperty("App::PropertyPolVecDistance","Point2","Object of a PolygonalArea","Point2 of the PolygonalArea").Point2=FreeCAD.Vector(0.001,360,0.001)
            obj.addProperty("App::PropertyPolVecDistance","Point3","Object of a PolygonalArea","Point3 of the PolygonalArea").Point3=FreeCAD.Vector(0,0,0)
            obj.PropertyOfCoordinateSys="App::PropertyPolVecDistance"
            pass
        else:
            obj.addProperty("App::PropertyCylinderVecDistance","Point1","Object of a PolygonalArea","Point1 of the PolygonalArea").Point1=FreeCAD.Vector(0.001,0,0)
            obj.addProperty("App::PropertyCylinderVecDistance","Point2","Object of a PolygonalArea","Point2 of the PolygonalArea").Point2=FreeCAD.Vector(0.001,360,0.001)
            obj.addProperty("App::PropertyCylinderVecDistance","Point3","Object of a PolygonalArea","Point3 of the PolygonalArea").Point3=FreeCAD.Vector(0,0,0)
            obj.PropertyOfCoordinateSys="App::PropertyCylinderVecDistance"
            pass
        self.vectorList=[obj.Point1,obj.Point2,obj.Point3]
        obj.addProperty("App::PropertyString", "Type", "", "Type of Ojecy").Type = ObjectsTools.ObjectType.Area_Polygonal
        ObjectsTools.addNonUniformGridAttribute(self.curCoordinateSystem,obj)
        
        obj.addProperty("App::PropertyInteger","Order","","Order of the Conformal").Order=100

        obj.Proxy = self
        self.placementBefore = obj.Placement
        self.numbersOfPointsBefore=obj.NumbersOfPoints
        self.isPoint1Change=False
        self.isPoint2Change=False

        self.orderBefore=obj.Order
        self.labelBofroe=obj.Label
        
        #flagShape和flagPalcement为在移动过程中不能在属性面板中输入值，在输入值的时候不移动
        self.flagShape=True
        self.flagPlacement=True

        self.flagExcute=False
        obj.setEditorMode('Placement',2)
        obj.setEditorMode('Type',2)
        self.initObject(obj)
        #重绘
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
        # elif prop=="Point1":
        #     FreeCAD.Console.PrintMessage("beforeChange___1\n")
        #     self.isPoint1Change=True
        # elif prop=="Point2":
        #     FreeCAD.Console.PrintMessage("beforeChange___2\n")
        #     self.isPoint2Change=True
        elif prop=="NumbersOfPoints":
            self.numbersOfPointsBefore=obj.NumbersOfPoints
        elif prop=="Order":
            self.orderBefore=obj.Order
        elif prop=="Label":
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
            
        topFiveOfProp=prop[0:5]
        if topFiveOfProp=="Point":
            if self.flagShape:
                self.flagShape=False
                self.flagPlacement=False
                #将物体置为原点
                fp.Placement=FreeCAD.Placement(FreeCAD.Vector(0.0,0.0,0.0),FreeCAD.Rotation(0.0,0.0,0.0,1.0))
                # self.redraw(fp)
                self.vectorList=[]
                for i in range(fp.NumbersOfPoints):
                    pointStr="Point"+str(i+1)
                    if(hasattr(fp,pointStr)):
                        # setattr(fp,pointStr,)
                        self.vectorList.append(getattr(fp,pointStr))
                self.flagShape=True
                self.flagPlacement=True
                self.flagExcute=True
        elif prop=="NumbersOfPoints":
            if self.flagShape:
                self.flagShape=False
                self.flagPlacement=False
                #将物体置为原点
                # fp.Placement=FreeCAD.Placement(FreeCAD.Vector(0.0,0.0,0.0),FreeCAD.Rotation(0.0,0.0,0.0,1.0))
                # self.redraw(fp)
                # self.vectorList=[fp.Point1,fp.Point2]
                if fp.NumbersOfPoints<3:
                    fp.NumbersOfPoints=self.numbersOfPointsBefore
                else:
                    if self.numbersOfPointsBefore>fp.NumbersOfPoints:
                        subNums=self.numbersOfPointsBefore-fp.NumbersOfPoints
                        for i in range(subNums):                          
                            removedProp=self.vectorList.pop()
                            removePropStrName="Point"+str(self.numbersOfPointsBefore-i)
                            fp.removeProperty(removePropStrName)
                        pass
                    elif self.numbersOfPointsBefore<fp.NumbersOfPoints:
                        addNums=fp.NumbersOfPoints-self.numbersOfPointsBefore
                        num=len(self.vectorList)+1
                        for i in range(addNums):
                            fp.addProperty(fp.PropertyOfCoordinateSys,"Point"+str(num),"Object of a PolygonalArea","Point of the PolygonalArea")       
                            setattr(fp,"Point"+str(num),self.vectorList[self.numbersOfPointsBefore-1+i])
                            num=num+1
                            self.vectorList.append(self.vectorList[self.numbersOfPointsBefore-1+i])
                        pass
                    else:
                        pass
                self.flagShape=True
                self.flagPlacement=True
                self.flagExcute=True
        elif prop=="Placement":
            if self.flagPlacement:
                self.flagPlacement=False
                self.flagShape=False
                #设置属性自定义属性只读
                for i in range(len(self.vectorList)):
                    fp.setEditorMode("Point"+str(i+1),1)
                #坐标转换
                FreeCAD.Console.PrintMessage(self.vectorList)
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
                for i in range(len(self.vectorList)):
                    pointStr="Point"+str(i+1)
                    if(hasattr(fp,pointStr)):
                        setattr(fp,pointStr,resultVectors[i])

                self.vectorList=[]
                for i in range(fp.NumbersOfPoints):
                    pointStr="Point"+str(i+1)
                    if(hasattr(fp,pointStr)):
                        # setattr(fp,pointStr,)
                        self.vectorList.append(getattr(fp,pointStr))
                # self.vectorList=[fp.Point1,fp.Point2]
                self.flagPlacement=True
                self.flagShape=True
                self.flagExcute=False
                # 重塑
                pass
        # elif prop=="Normal":
        #     self.isPoint2Change=True
        #     self.flagExcute=True
        #     pass
        ObjectsTools.fucNonUniformGrid(self.curCoordinateSystem,fp,prop)
        # elif prop=="X" or prop=="Y" or prop=="Z" or prop=="R" or prop=="Theta":
        #     #控制非均匀网格是否显示
        #     ObjectsTools.fucNonUniformGrid(self.curCoordinateSystem,fp)

    def redraw(self,obj):
        # try:
            # 重绘
        FreeCAD.Console.PrintMessage(self.vectorList)
        tempPoints=CoordinateSystemTools.otherToRec(self.curCoordinateSystem,self.vectorList)
        FreeCAD.Console.PrintMessage(tempPoints)
        # FreeCAD.Console.PrintMessage(tempPoints)
        if not obj.NumbersOfPoints ==0:
        #     FreeCAD.Console.PrintMessage(tempPoints)
            drawPoints=copy.copy(tempPoints)
        #     # drawPoints=self.vectorList
            drawPoints.append(tempPoints[0])
        #     wireOfPolygonal=Part.makePolygon(drawPoints)
        #     obj.Shape=Part.makeFace(wireOfPolygonal,"Part::FaceMakerSimple")
            wireOfPolygonal=Part.makePolygon(drawPoints)
            try:
                obj.Shape=Part.makeFace(wireOfPolygonal,"Part::FaceMakerExtrusion")
            except:
                try:
                    obj.Shape=self.getIntersectShape(tempPoints)
                except:
                    obj.Shape=wireOfPolygonal

    def removeSamePointsNor(self,pointsList):
        lastPoint=None
        resultList=[]
        i=0
        for pointItem in pointsList:
            i=i+1
            if pointsList.index(pointItem) ==0:
                lastPoint=pointItem
                resultList.append(lastPoint)
                continue
            else:
                if pointItem==lastPoint:

                    continue
                else:
                    resultList.append(pointItem)
                    lastPoint=pointItem
        if pointsList[len(pointsList)-1]!=lastPoint:
            resultList.append(lastPoint)
        return resultList





    def checkTwoWiresIntersect(self,w1,w2):
        '''
        判断两个点是否相交
        return [intersectPoint1,intersectPoint2],若返回为空，则不想交
        '''
        s=w1.section(w2)
        intersectPoints=s.Vertexes
        return intersectPoints






    def getIntersectShape(self,tempPoints):
        '''
        算法思路： 变量所有点，当前点与前一个点连成的线段，如果和前一个点所有的线段有交点，这从已遍历的点中寻找最近与当前线段相交的点，并求出交点；
        将交点之间的点形成一个面，然后将所有点去掉已经形成了面的点，再从头开始遍历，直到剩余的点小于3或者剩下的三个点形成的线段重合为止
        '''
        faceList=[]
        tempPoints=self.removeSamePointsNor(tempPoints)
        time=0
        while(len(tempPoints)>=3 and time<10):
            pointsPre=[]
            if len(tempPoints)==3:
                if tempPoints[0]==tempPoints[2]:
                    break
                else:
                    wires=Part.makePolygon(tempPoints)
                    face=Part.makeFace(wires)
            time=time+1
            for i in range(0,len(tempPoints)):
                #第一个点
                if i<=1:
                    pointsPre.append(tempPoints[i])
                else:
                    wiresPre=Part.makePolygon(pointsPre)
                    wiresThisSec=Part.makePolygon([tempPoints[i-1],tempPoints[i]])
                    # 判断是否存在交点
                    intersectPoints=self.checkTwoWiresIntersect(wiresPre,wiresThisSec)
                    # Part.show(wiresPre)
                    # Part.show(wiresThisSec)
                    #有一个交点是正常的
                    if len(intersectPoints)==1:
                        pointsPre.append(tempPoints[i])
                        continue
                    else:
                        #找到与当前线段相交的最近的那个线段，注意这里减一，从当前点后退到两个点
                        for IndexPointItemPre in range(len(pointsPre)-2,0,-1):
                            if IndexPointItemPre !=0:
                                wiresCurSec=Part.makePolygon([pointsPre[IndexPointItemPre],pointsPre[IndexPointItemPre-1]])
                                intersectPointsFind=self.checkTwoWiresIntersect(wiresCurSec,wiresThisSec)
                                # 与当前的这个不相及，再上一个
                                if len(intersectPointsFind)==0:
                                    continue
                                # 有相交了，就是当前的交点,一个相交点
                                else:
                                    intersectPoint=intersectPointsFind[0]
                                    interPoint=FreeCAD.Vector(intersectPoint.X,intersectPoint.Y,intersectPoint.Z)

                                    pointsInThisFace=pointsPre[IndexPointItemPre:len(pointsPre)]
                                    pointsInThisFace.insert(0,interPoint)
                                    pointsInThisFace.append(interPoint)
                                    if len(pointsInThisFace)<3:
                                        # 不能形成面,,,注意要将这些点去掉，暂时还没去
                                        pass
                                    else:
                                        wiresPoly=Part.makePolygon(pointsInThisFace)
                                        # 再次测试一下 是否形成闭合的环
                                        if wiresPoly.isClosed():
                                            face=Part.makeFace(wiresPoly,"Part::FaceMakerSimple")
                                            #将这个面加入面列表
                                            faceList.append(face)
                                        else:
                                            sayzError(" make face error")
                                    # 先插入一个相交点
                                    tempPoints.insert(i,interPoint)
                                    #去掉已经形成面的点集
                                    tempPoints=pointsPre[0:IndexPointItemPre]+tempPoints[i:len(tempPoints)]
                                    # 去掉tempPoints中相邻点之间重复的点
                                    tempPoints=self.removeSamePointsNor(tempPoints)
                                    # 退出第二重循环
                                    break
                        break
        shape=Part.makeCompound(faceList)
        return shape

    def execute(self, fp):

        #设置自定义属性可编辑
        for i in range(len(self.vectorList)):
            fp.setEditorMode("Point"+str(i+1),0)
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
 

class ViewProviderPolygonal:
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
        return "Flat Lines"
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
