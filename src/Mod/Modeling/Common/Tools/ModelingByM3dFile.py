# -*- coding: utf-8 -*-
import FreeCAD, Part
# import CoordinateSystemTools
# import ObjectsTools
import FreeCADGui
# import DocumentTools
# import UnitTools
from Modeling.Common.Tools import UnitTools,ObjectsTools,CoordinateSystemTools,DocumentTools
import Modeling3DCommand as Model
import Modeling.Modeling3D.Modeling3DCommand.Vol_Array.Command.ArrayInstance as Instance

def syna(msg):
    FreeCAD.Console.PrintMessage("\n")
    FreeCAD.Console.PrintMessage(msg)
    FreeCAD.Console.PrintMessage("\n")

# 判断是数还是字符串
def isNumber(n):
    result=True
    try:
        num=float(n)
        result = num == num
    except ValueError:
        result=False
    return result
# 根据所有的模型对象及具体信息在场景中建模
def modelingByParameter(modlelingParameterList):
    """
        parameter:[] modlelingParameterList
        """
    # 为支持参数阵列体，在函数中加入全局变量数据
    import datetime
    startTime=datetime.datetime.now()
    order = 0
    # 用来存放文件中所有面线的名称和order
    labelList = []
    # 用来存放所有的Extruded
    extrudedObjList = []
    # 用来存放阵列体的基础挤出体
    baseExtrudedObjList = []
    # 用来存放所有的旋转体
    revolutionObjList = []
    # 用来存放阵列体的基础旋转体？
    baseRevolutionObjList = []
    # 用来存放基础挤出体对应的阵列体参数
    arrayParameterList = []
    # 用来存放基础挤出体对应的阵列体序号
    orderList = []
    # 进度条
    progress_bar=FreeCAD.Base.ProgressIndicator()
    progress_bar.start("Import M3d File...",len(modlelingParameterList))
    for parameterList in modlelingParameterList:

        if not parameterList:
            continue
        # try:
        # 点
        if parameterList[0] == ObjectsTools.ObjectType.Point:
            __createPoint(parameterList[1],order)
        # _Conformal线
        elif parameterList[0] == ObjectsTools.ObjectType.Line_Conformal:
            __createConformalLine(parameterList[1],order)
            labelList.append([parameterList[1][0],order])
        # 斜线
        elif parameterList[0] == ObjectsTools.ObjectType.Line_Oblique:
            __createObliqueLine(parameterList[1],order)
            labelList.append([parameterList[1][0],order])
        # Conformal面
        elif parameterList[0] == ObjectsTools.ObjectType.Area_Conformal:
            __createConformalArea(parameterList[1], order)
            labelList.append([parameterList[1][0], order])
        # Rectangular面
        elif parameterList[0] == ObjectsTools.ObjectType.Area_Rectangular:
            __createRectangularArea(parameterList[1], order)
            labelList.append([parameterList[1][0], order])
        # 多边形面
        elif parameterList[0] == ObjectsTools.ObjectType.Area_Polygonal:
            __createPolygonalArea(parameterList[1],order)
            labelList.append([parameterList[1][0],order])
        # 投影体
        elif parameterList[0] == ObjectsTools.ObjectType.Vol_Conformal:
            __createConformalVolume(parameterList[1],order)
        # 圆锥或圆台
        elif parameterList[0] == ObjectsTools.ObjectType.Vol_SpecialCone:
            __createSpecialConeVolume(parameterList[1],order)
        # 环形体
        elif parameterList[0] == ObjectsTools.ObjectType.Vol_Annular:
            __createAnnularVolume(parameterList[1],order)
        # 圆柱
        elif parameterList[0] == ObjectsTools.ObjectType.Vol_Cylinder:
            __createCylinderVolume(parameterList[1],order)
        # 平行六面体
        elif parameterList[0] == ObjectsTools.ObjectType.Vol_Parallelepipedal:
            __createParallelepipedalVolume(parameterList[1],order)
        # 球体
        elif parameterList[0] == ObjectsTools.ObjectType.Vol_Spherical:
            __createSphericalVolume(parameterList[1],order)
        # 棱锥体
        elif parameterList[0] == ObjectsTools.ObjectType.Vol_Pyramid:
            __createPyramidVolume(parameterList[1],order)
        # 部分圆环体
        elif parameterList[0] == ObjectsTools.ObjectType.Vol_Toroidal_Section:
            __createToroidal_SectionVolume(parameterList[1],order)
        # 楔形体
        elif parameterList[0] == ObjectsTools.ObjectType.Vol_Wedge:
            __createWedgeVolume(parameterList[1],order)
        # 四面体
        elif parameterList[0] == ObjectsTools.ObjectType.Vol_Tetrahedron:
            __createTetrahedronVolume(parameterList[1],order)
        # 菱形体
        elif parameterList[0] == ObjectsTools.ObjectType.Vol_Rhombus:
            __createRhombusVolume(parameterList[1],order)
        # 部分环面体
        elif parameterList[0] == ObjectsTools.ObjectType.Vol_Annular_Section:
            __createAnnular_SectionVolume(parameterList[1],order)
        # 挤出体
        elif parameterList[0] == ObjectsTools.ObjectType.Vol_Extruded:
            objParameter = __createExtrudedVolume(parameterList[1],order)
            extrudedObjList.append(objParameter)
        # 旋转体
        elif parameterList[0] == ObjectsTools.ObjectType.Vol_Revolution:
            objParameter = __createRevolutionVolume(parameterList[1],order)
            revolutionObjList.append(objParameter)
        # 螺旋体
        elif parameterList[0] == ObjectsTools.ObjectType.Vol_Helical:
            __createHelicalVolume(parameterList[1],order)
        # 函数体
        elif parameterList[0] == ObjectsTools.ObjectType.Vol_Function:
            __createFunctionVolume(parameterList[1],order)

        # 阵列体
        elif parameterList[0] == ObjectsTools.ObjectType.Vol_Array:

            baseObj = None
            # parameterList[2][0]为基础模型的类型
            # 点
            if parameterList[2][0] == ObjectsTools.ObjectType.Point:
                baseObj =__createPoint(parameterList[2][1], order)

            # _Conformal线
            elif parameterList[2][0] == ObjectsTools.ObjectType.Line_Conformal:
                baseObj =__createConformalLine(parameterList[2][1], order)
                labelList.append([parameterList[2][1][0], order])

            # 斜线
            elif parameterList[2][0] == ObjectsTools.ObjectType.Line_Oblique:
                baseObj =__createObliqueLine(parameterList[2][1], order)
                labelList.append([parameterList[2][1][0], order])

            # Conformal面
            elif parameterList[2][0] == ObjectsTools.ObjectType.Area_Conformal:
                baseObj =__createConformalArea(parameterList[2][1], order)
                labelList.append([parameterList[2][1][0], order])

            # Rectangular面
            elif parameterList[2][0] == ObjectsTools.ObjectType.Area_Rectangular:
                baseObj =__createRectangularArea(parameterList[2][1], order)
                labelList.append([parameterList[2][1][0], order])

            # 多边形面
            elif parameterList[2][0] == ObjectsTools.ObjectType.Area_Polygonal:
                baseObj =__createPolygonalArea(parameterList[2][1], order)
                labelList.append([parameterList[2][1][0], order])

            # 投影体
            elif parameterList[2][0] == ObjectsTools.ObjectType.Vol_Conformal:
                baseObj =__createConformalVolume(parameterList[2][1], order)

            # 圆锥或圆台
            elif parameterList[2][0] == ObjectsTools.ObjectType.Vol_SpecialCone:
                baseObj =__createSpecialConeVolume(parameterList[2][1], order)

            # 环形体
            elif parameterList[2][0] == ObjectsTools.ObjectType.Vol_Annular:
                baseObj =__createAnnularVolume(parameterList[2][1], order)

            # 圆柱
            elif parameterList[2][0] == ObjectsTools.ObjectType.Vol_Cylinder:
                baseObj =__createCylinderVolume(parameterList[2][1], order)

            # 平行六面体
            elif parameterList[2][0] == ObjectsTools.ObjectType.Vol_Parallelepipedal:
                baseObj =__createParallelepipedalVolume(parameterList[2][1], order)

            # 球体
            elif parameterList[2][0] == ObjectsTools.ObjectType.Vol_Spherical:
                baseObj =__createSphericalVolume(parameterList[2][1], order)

            # 棱锥体
            elif parameterList[2][0] == ObjectsTools.ObjectType.Vol_Pyramid:
                baseObj =__createPyramidVolume(parameterList[2][1], order)

            # 部分圆环体
            elif parameterList[2][0] == ObjectsTools.ObjectType.Vol_Toroidal_Section:
                baseObj =__createToroidal_SectionVolume(parameterList[2][1], order)

            # 楔形体
            elif parameterList[2][0] == ObjectsTools.ObjectType.Vol_Wedge:
                baseObj =__createWedgeVolume(parameterList[2][1], order)

            # 四面体
            elif parameterList[2][0] == ObjectsTools.ObjectType.Vol_Tetrahedron:
                baseObj =__createTetrahedronVolume(parameterList[2][1], order)

            # 菱形体
            elif parameterList[2][0] == ObjectsTools.ObjectType.Vol_Rhombus:
                baseObj =__createRhombusVolume(parameterList[2][1], order)

            # 部分环面体
            elif parameterList[2][0] == ObjectsTools.ObjectType.Vol_Annular_Section:
                baseObj =__createAnnular_SectionVolume(parameterList[2][1], order)

            # 挤出体
            elif parameterList[2][0] == ObjectsTools.ObjectType.Vol_Extruded:
                objParameter = __createExtrudedVolume(parameterList[2][1], order)
                extrudedObjList.append(objParameter)
                baseExtrudedObjList.append(objParameter)
                arrayParameterList.append(parameterList[1])
                orderList.append(order)

            # 旋转体
            elif parameterList[2][0] == ObjectsTools.ObjectType.Vol_Revolution:
                objParameter = __createRevolutionVolume(parameterList[2][1], order)
                revolutionObjList.append(objParameter)
                baseRevolutionObjList.append(objParameter)
                arrayParameterList.append(parameterList[1])
                orderList.append(order)

            # 螺旋体
            elif parameterList[2][0] == ObjectsTools.ObjectType.Vol_Helical:
                baseObj =__createHelicalVolume(parameterList[2][1], order)

            # print("**************"+baseObj.Label+str(order)+str(baseObj != None)+"**************")
            if baseObj != None:
                baseObj.Label=baseObj.Label.replace("Arr_","").replace("\'i\'","")
                curCoordinateSys = baseObj.Document.CoordinateSystem
                __arrayListModify(baseObj)
                __createArrayObject(curCoordinateSys, baseObj, parameterList[1])

        #参数阵列体
        elif parameterList[0]==ObjectsTools.ObjectType.Vol_ParamArray:
            doc=FreeCAD.ActiveDocument
            grp=doc.Array
            paramObj=ObjectsTools.getParamObj()
            objName=parameterList[2][1][0].replace("\'i\'","")
            objsList=[]
            # baseObj=[None]*(int(parameterList[1][-5])-1)
            i_start=int(parameterList[1][-5][0])
            i_end=int(parameterList[1][-5][1])
            # FreeCAD.Console.PrintMessage("\n开始： "+str(i_start)+" 结束： "+str(i_end)+"\n")
            if parameterList[2][0] == ObjectsTools.ObjectType.Vol_Annular:
                basetype="环形体"
                basedata=parameterList[2][1][1]+" "+parameterList[2][1][2]+" "+parameterList[2][1][3]+" "+parameterList[2][1][4]
                temp_parameterList = parameterList[2][1][:]
                #按照do的次数进行循环
                for i in range(i_start,i_end+1):
                    for j in range(4):
                        temp_parameterList[j+1]=VarReplace(parameterList[2][1][j+1],i)
                        # FreeCAD.Console.PrintMessage("\n测试结果:\n")
                        # FreeCAD.Console.PrintMessage(temp_parameterList)
                    objItem=doc.addObject("Part::FeaturePython", objName+str(i))
                    objInstance = Model.Vol_Annular.AnnularInstance.Annular(objItem, needOrder=False,
                                                                            thistype=ObjectsTools.ObjectType.none)
                    Model.Vol_Annular.AnnularInstance.ViewProviderAnnular(objItem.ViewObject)
                    objItem.removeProperty("Type")

                    #手动赋值
                    if FreeCAD.ActiveDocument.CoordinateSystem ==CoordinateSystemTools.CoordinateType.Rectangular or FreeCAD.ActiveDocument.CoordinateSystem == CoordinateSystemTools.CoordinateType.Polar:
                        setValue(objItem,"Point_1.x",temp_parameterList[1][0])
                        setValue(objItem, "Point_1.y", temp_parameterList[1][1])
                        setValue(objItem, "Point_1.z", temp_parameterList[1][2])

                        setValue(objItem, "Point_2.x", temp_parameterList[2][0])
                        setValue(objItem, "Point_2.y", temp_parameterList[2][1])
                        setValue(objItem, "Point_2.z", temp_parameterList[2][2])

                    else:
                        setValue(objItem, "Point_1.x", temp_parameterList[1][1])
                        setValue(objItem, "Point_1.y", temp_parameterList[1][2])
                        setValue(objItem, "Point_1.z", temp_parameterList[1][0])

                        setValue(objItem, "Point_2.x", temp_parameterList[2][1])
                        setValue(objItem, "Point_2.y", temp_parameterList[2][2])
                        setValue(objItem, "Point_2.z", temp_parameterList[2][0])

                    setValue(objItem, "RadiusInside", temp_parameterList[3])
                    setValue(objItem, "RadiusOutside", temp_parameterList[4])

                    objItem.recompute()
                    objsList.append(objItem)
                pass
            elif parameterList[2][0]==ObjectsTools.ObjectType.Vol_Cylinder:
                basedata=parameterList[2][1][1]+" "+parameterList[2][1][2]+" "+parameterList[2][1][3]
                basetype="圆柱体"
                temp_parameterList=parameterList[2][1][:]
                for i in range(i_start,i_end+1):
                    for j in range(3):
                        temp_parameterList[j+1]=VarReplace(parameterList[2][1][j+1],i)

                    objItem = doc.addObject("Part::FeaturePython", objName + str(i))
                    objInstance = Model.Vol_Cylinder.CylinderInstance.Cylinder(objItem, needOrder=False,
                                                                            thistype=ObjectsTools.ObjectType.none)
                    Model.Vol_Cylinder.CylinderInstance.ViewProviderCylinder(objItem.ViewObject)
                    objItem.removeProperty("Type")

                    #手动赋值：
                    FreeCAD.Console.PrintMessage("这里能获得正确的坐标吗？\n")
                    FreeCAD.Console.PrintMessage(FreeCAD.ActiveDocument.CoordinateSystem)
                    FreeCAD.Console.PrintMessage("\n")
                    if FreeCAD.ActiveDocument.CoordinateSystem ==CoordinateSystemTools.CoordinateType.Rectangular or FreeCAD.ActiveDocument.CoordinateSystem == CoordinateSystemTools.CoordinateType.Polar:
                        setValue(objItem, ObjectsTools.PropertiesOfObj.Cylinder.Point_1+".x", temp_parameterList[1][0])
                        setValue(objItem, ObjectsTools.PropertiesOfObj.Cylinder.Point_1+".y", temp_parameterList[1][1])
                        setValue(objItem, ObjectsTools.PropertiesOfObj.Cylinder.Point_1+".z", temp_parameterList[1][2])

                        setValue(objItem, ObjectsTools.PropertiesOfObj.Cylinder.Point_2+".x", temp_parameterList[2][0])
                        setValue(objItem, ObjectsTools.PropertiesOfObj.Cylinder.Point_2+".y", temp_parameterList[2][1])
                        setValue(objItem, ObjectsTools.PropertiesOfObj.Cylinder.Point_2+".z", temp_parameterList[2][2])
                    else:
                        setValue(objItem, ObjectsTools.PropertiesOfObj.Cylinder.Point_1 + ".x",
                                 temp_parameterList[1][1])
                        setValue(objItem, ObjectsTools.PropertiesOfObj.Cylinder.Point_1 + ".y",
                                 temp_parameterList[1][2])
                        setValue(objItem, ObjectsTools.PropertiesOfObj.Cylinder.Point_1 + ".z",
                                 temp_parameterList[1][0])

                        setValue(objItem, ObjectsTools.PropertiesOfObj.Cylinder.Point_2 + ".x",
                                 temp_parameterList[2][1])
                        setValue(objItem, ObjectsTools.PropertiesOfObj.Cylinder.Point_2 + ".y",
                                 temp_parameterList[2][2])
                        setValue(objItem, ObjectsTools.PropertiesOfObj.Cylinder.Point_2 + ".z",
                                 temp_parameterList[2][0])

                    setValue(objItem, ObjectsTools.PropertiesOfObj.Cylinder.Radius, temp_parameterList[3])

                    objItem.recompute()
                    objsList.append(objItem)
                pass

            elif parameterList[2][0]==ObjectsTools.ObjectType.Vol_Conformal:
                basetype="正投影体"
                basedata=parameterList[2][1][1]+" "+parameterList[2][1][2]
                temp_parameterList = parameterList[2][1][:]
                for i in range(i_start, i_end + 1):
                    for j in range(2):
                        temp_parameterList[j + 1] = VarReplace(parameterList[2][1][j + 1], i)

                    objItem = doc.addObject("Part::FeaturePython", objName + str(i))
                    objInstance = Model.Vol_Conformal.ConformalInstance.Conformal(objItem, needOrder=False,
                                                                            thistype=ObjectsTools.ObjectType.none)
                    Model.Vol_Conformal.ConformalInstance.ViewProviderConformal(objItem.ViewObject)
                    objItem.removeProperty("Type")

                    # 手动赋值：
                    if FreeCAD.ActiveDocument.CoordinateSystem ==CoordinateSystemTools.CoordinateType.Rectangular or FreeCAD.ActiveDocument.CoordinateSystem == CoordinateSystemTools.CoordinateType.Polar:
                        setValue(objItem, ObjectsTools.PropertiesOfObj.Conformal.Point1 + ".x", temp_parameterList[1][0])
                        setValue(objItem, ObjectsTools.PropertiesOfObj.Conformal.Point1 + ".y", temp_parameterList[1][1])
                        setValue(objItem, ObjectsTools.PropertiesOfObj.Conformal.Point1 + ".z", temp_parameterList[1][2])

                        setValue(objItem, ObjectsTools.PropertiesOfObj.Conformal.Point2 + ".x", temp_parameterList[2][0])
                        setValue(objItem, ObjectsTools.PropertiesOfObj.Conformal.Point2 + ".y", temp_parameterList[2][1])
                        setValue(objItem, ObjectsTools.PropertiesOfObj.Conformal.Point2 + ".z", temp_parameterList[2][2])
                    else:
                        setValue(objItem, ObjectsTools.PropertiesOfObj.Conformal.Point1 + ".x",
                                 temp_parameterList[1][1])
                        setValue(objItem, ObjectsTools.PropertiesOfObj.Conformal.Point1 + ".y",
                                 temp_parameterList[1][2])
                        setValue(objItem, ObjectsTools.PropertiesOfObj.Conformal.Point1 + ".z",
                                 temp_parameterList[1][0])

                        setValue(objItem, ObjectsTools.PropertiesOfObj.Conformal.Point2 + ".x",
                                 temp_parameterList[2][1])
                        setValue(objItem, ObjectsTools.PropertiesOfObj.Conformal.Point2 + ".y",
                                 temp_parameterList[2][2])
                        setValue(objItem, ObjectsTools.PropertiesOfObj.Conformal.Point2 + ".z",
                                 temp_parameterList[2][0])

                    objItem.recompute()
                    objsList.append(objItem)
            # fubiao
            elif parameterList[2][0]==ObjectsTools.ObjectType.Vol_SpecialCone:
                basetype="环形体"
                basedata=parameterList[2][1][1]+" "+parameterList[2][1][2]+" "+parameterList[2][1][3]+" "+parameterList[2][1][4]
                temp_parameterList = parameterList[2][1][:]
                #按照do的次数进行循环
                for i in range(i_start,i_end+1):
                    for j in range(4):
                        temp_parameterList[j+1]=VarReplace(parameterList[2][1][j+1],i)
                        # FreeCAD.Console.PrintMessage("\n测试结果:\n")
                        # FreeCAD.Console.PrintMessage(temp_parameterList)
                    objItem=doc.addObject("Part::FeaturePython", objName+str(i))
                    objInstance = Model.Vol_SpecialCone.SpecialConeInstance.SpecialCone(objItem, needOrder=False,
                                                                            thistype=ObjectsTools.ObjectType.none)
                    Model.Vol_SpecialCone.SpecialConeInstance.ViewProviderSpecialCone(objItem.ViewObject)
                    objItem.removeProperty("Type")

                    #手动赋值
                    if FreeCAD.ActiveDocument.CoordinateSystem ==CoordinateSystemTools.CoordinateType.Rectangular or FreeCAD.ActiveDocument.CoordinateSystem == CoordinateSystemTools.CoordinateType.Polar:
                        setValue(objItem,"PointBottom.x",temp_parameterList[1][0])
                        setValue(objItem, "PointBottom.y", temp_parameterList[1][1])
                        setValue(objItem, "PointBottom.z", temp_parameterList[1][2])

                        setValue(objItem, "PointTop.x", temp_parameterList[2][0])
                        setValue(objItem, "PointTop.y", temp_parameterList[2][1])
                        setValue(objItem, "PointTop.z", temp_parameterList[2][2])

                    else:
                        setValue(objItem, "PointBottom.x", temp_parameterList[1][1])
                        setValue(objItem, "PointBottom.y", temp_parameterList[1][2])
                        setValue(objItem, "PointBottom.z", temp_parameterList[1][0])

                        setValue(objItem, "PointTop.x", temp_parameterList[2][1])
                        setValue(objItem, "PointTop.y", temp_parameterList[2][2])
                        setValue(objItem, "PointTop.z", temp_parameterList[2][0])

                    setValue(objItem, "RadiusBottom", temp_parameterList[3])
                    setValue(objItem, "RadiusTop", temp_parameterList[4])

                    objItem.recompute()
                    objsList.append(objItem)


            if len(objsList)!=0:
                FreeCAD.ActiveDocument.openTransaction("Array")
                obj=FreeCAD.ActiveDocument.addObject("Part::CustomFeaturePython",objName)
                obj.Shapes=objsList
                objInstance=Instance.Array(obj)
                #对属性进行设置
                obj.BaseObjType=basetype
                obj.BaseObjData=basedata
                obj.Attribute = parameterList[2][1][-16]
                setValue(obj,"IFrom",[str(i_start)])
                setValue(obj,"ITo",[str(i_end)])
                obj.Label = objName
                FreeCAD.ActiveDocument.commitTransaction()
                import Modeling.Modeling3D.Modeling3DCommand.Vol_Annular.CreateAnnular as CreateAnnular
                new_obj=CreateAnnular.createAnnular()
                FreeCAD.Console.PrintMessage("这个有用吗？\n")
                FreeCAD.Console.PrintMessage(new_obj.Document.CoordinateSystem)
                FreeCAD.Console.PrintMessage("\n")
                __setMark(new_obj,parameterList[2][1][-15:])
                doc.removeObject(new_obj.Name)
            doc.recompute()
            DocumentTools.updateBoolean()


    # except :
    #     FreeCAD.Console.PrintMessage(parameterList)

        order = order + 1
        progress_bar.next()
    progress_bar.stop()
    endTime=datetime.datetime.now()
    FreeCAD.Console.PrintMessage("m3d  time :"+str((endTime-startTime).seconds)+"\n")

    # 为所有Extruded挤出体的面线参数赋值
    for extrudedObj in extrudedObjList:
        [obj, areaLabel, lineLabel] = extrudedObj
        for label in labelList:
            if areaLabel == label[0]:
                obj.Area = '[' + str(label[1]) + ']_' + label[0]
            if lineLabel == label[0]:
                obj.Line = '[' + str(label[1]) + ']_' + label[0]

    # 创建所有Extruded挤出体的阵列体
    for index in range(len(baseExtrudedObjList)):
        [obj, areaLabel, lineLabel] = baseExtrudedObjList[index]
        parameter = arrayParameterList[index]
        curCoordinateSys = obj.Document.CoordinateSystem
        order = orderList[index]
        # print("**************" + obj.Label + str(order)  + str(obj.Order)+"**************")
        __arrayListModify(obj)
        __createArrayObject(curCoordinateSys, obj, parameter)
    try:
        doc.recompute()
    except:
        FreeCAD.ActiveDocument.recompute()

    # 为所有旋转体的面参数赋值
    for revolutionObj in revolutionObjList:
        [obj, areaLabel] = revolutionObj
        for label in labelList:
            if areaLabel == label[0]:
                obj.Area = '[' + str(label[1]) + ']_' + label[0]

    # 创建所有旋转体的阵列体？
    for index in range(len(baseRevolutionObjList)):
        [obj, areaLabel, lineLabel] = baseRevolutionObjList[index]
        parameter = arrayParameterList[index]
        curCoordinateSys = obj.Document.CoordinateSystem
        order = orderList[index]
        # print("**************" + obj.Label + str(order)  + str(obj.Order)+"**************")
        __arrayListModify(obj)
        __createArrayObject(curCoordinateSys, obj, parameter)
    try:
        doc.recompute()
    except:
        FreeCAD.ActiveDocument.recompute()

def __arrayListModify(obj):
    group = obj.InList
    activeDoc = FreeCAD.ActiveDocument
    # 选中物体同时属于当前模型组和阵列组
    if len(group) == 1:
        # 与 obj 同类别的所有模型
        groupObjs = activeDoc.getObject(group[0].Name)
        if len(groupObjs.Group) == 1:
            activeDoc.removeObject(group[0].Name)
            activeDoc.recompute()
        elif len(groupObjs.Group) > 1:
            # 当 obj 的所在类别中包含不止一个模型时，将 obj 移除当前类别
            activeDoc.getObject(group[0].Name).removeObject(activeDoc.getObject(obj.Name))

# 新建3D空白文档
def newDoc(CoordinateSystem):
    # 切换一下工作台，刷新建模部分的图标 by pingyue
    nowWorkbenchText=FreeCADGui.activeWorkbench().name()
    FreeCADGui.activateWorkbench("Modeling2DWorkbench")
    FreeCADGui.activateWorkbench("Modeling3DWorkbench")
    FreeCADGui.activateWorkbench(nowWorkbenchText)
    ###

    # from PySide import QtGui, QtCore
    # window = FreeCADGui.getMainWindow()
    # actionList = window.findChildren(QtGui.QAction)
    # cmdlst = ["Create Point",
    #           "Create ConformalLine",
    #           "Create ObliqueLine",
    #           "Create ConformalArea",
    #           "Create FunctionArea",
    #           "Create Rectangular",
    #           "Create Polygonal",
    #           # "PolygonalCommand",
    #           "Create Conformal",
    #           "Create Annular",
    #           # "CreateTorusFace",
    #           "Create Cylinder",
    #           # "CreateCone",
    #           "Create SpecialCone",
    #           #   "CreateTorus",
    #           #   "CreateOrthographicBody",
    #           "Create Parallelepipedal",
    #           "Create Spherical",
    #           "Create Wedge",
    #           "Create Pyramid",
    #           "Create Rhombus",
    #           "Create Extruded",
    #           "Create Tetrahedron",
    #           "Create Toroidal_Section",
    #           "Create Annular_Section",
    #           "Create Helical",
    #           "Create Revolution",
    #           "Object_Array",
    #           "Create Function",
    #           "Create Param Array",
    #           "Create Draft Model",
    #           "Create Revolution Draft Model",
    #           # "TestCommand"
    #           "Paste the Objects",
    #           "Copy the Objects",
    #           "Cut the Objects",
    #           "Clip",
    #           ]
    # # 强制启用这些按钮
    # for action in actionList:
    #     if action.text () in cmdlst:
    #         action.setDisabled (False)
    #     if CoordinateSystem != "Rectangular" and action.text() == "Create Rectangular":
    #         action.setDisabled (True)
    #     # if action.text() == "Paste the Objects":
    #     #     action.setEnabled (False)


    doc = FreeCAD.newDocument()

    FreeCADGui.ActiveDocument.ActiveView.setAxisCross(True)

    FreeCAD.ActiveDocument.CoordinateSystem = CoordinateSystem

    # 初始化当前文档
    DocumentTools.initDocument(doc)

    import File
    File.FileCommand.TextUI.FileTextView.FileView().showThisSubWindow()


def setGlobalVariable(globalVariableList):

    """return:[] globalVariableList 全局变量列表
                   [[name,value]......]
    """
    # @fubiao
    DX1="1mm"
    DX2="1mm"
    DX3="1mm"
    ObjectsTools.setDX1DX2DX3(DX1,DX2,DX3)
    paramStr=""
    #这里globalVariableList[:-3]都是用户自己定义的，需要显示，后三个为DX1，DX2，DX3不需要显示
    for globalVariable in globalVariableList[:-3]:
        if globalVariable[0]==globalVariable[1]:
            continue
        if str(globalVariable[1])=="!COMMENT":
            paramStr=paramStr+str(globalVariable[0])+"\n"
        # elif str(globalVariable[0])=="DX1":
        #     DX1=globalVariable[1]
            
        # elif str(globalVariable[0])=="DX2":
        #     DX2=globalVariable[1]
        # elif str(globalVariable[0])=="DX3":
        #     DX3=globalVariable[1]
        else:
            paramStr=paramStr+str(globalVariable[0])+"="+str(globalVariable[1])+";\n"

    FreeCAD.ActiveDocument.Company=paramStr
    # 处理后三个
    for globalVariable in globalVariableList[-3:]:
        if str(globalVariable[0])=="DX1":
            DX1=globalVariable[1]
        elif str(globalVariable[0])=="DX2":
            DX2=globalVariable[1]
        elif str(globalVariable[0])=="DX3":
            DX3=globalVariable[1]
    # FreeCAD.Console.PrintMessage("modelingByM3d: "+str(FreeCAD.ActiveDocument.Company)+"\n")
    from CustomParameter.CustomParameterCommand.DlgCustomParameterMain import CustomeParameterMain
    cp=CustomeParameterMain(flagIsFromM3d=True)
    cp.onOkBtn()
    ObjectsTools.setDX1DX2DX3(DX1,DX2,DX3)
    # import DynamicData.DynamicDataCmd as DynamicDataCmd
    # # 新建一个全局变量
    # DynamicDataObject = DynamicDataCmd.DynamicDataCreateObjectCommandClass()
    # DynamicDataObject.Activated()
    # # 获取当前选中的的obj
    # # obj = FreeCAD.Gui.Selection.getSelectionEx()[0].Object
    # # 获取全局变量obj列表的第一个
    # obj = FreeCAD.ActiveDocument.findObjects('App::FeaturePython')[0]
    # groupName = obj.Label
    # FreeCAD.Console.PrintMessage("globalVariableList: "+str(globalVariableList)+"\n")
    # for globalVariable in globalVariableList:
    #     propertyName = globalVariable[0]
    #     if "mm" in globalVariable[1]:
    #         value = float(globalVariable[1].split("mm")[0])
    #         item = "Length"
    #         tooltip = "[Length]"
    #     elif "deg" in globalVariable[1]:
    #         value = float(globalVariable[1].split("deg")[0])
    #         item = "Angle"
    #         tooltip = "[Angle]"
    #     elif "." in globalVariable[1]:
    #         value = float(globalVariable[1])
    #         item = "Float"
    #         tooltip = "[Float]"
    #     elif globalVariable[1].isdigit():
    #         value = int(globalVariable[1])
    #         item = "Integer"
    #         tooltip = "[Integer]"
    #     elif globalVariable[0] != "":
    #         value = str(globalVariable[1])
    #         item = "String"
    #         tooltip = "[String]"

    #     # 添加对应属性
    #     obj.addProperty('App::Property' + item, propertyName, groupName, tooltip)
    #     setattr(obj, propertyName,value)

# 获得点坐标vector
def __getPointVector(obj,unitPoint,propertyName):
    """
        obj:该坐标点属于的对象，需要用于判断该点的坐标系
        unitPoint：[str(x1),str(x2),str(x3)]
        return:vector属性
    """
    ObjectsTools.turnExpressionToProperty(obj,propertyName,unitPoint)
   

# 为几何体设置mark参数
def __setMark(obj, markList):
    [isX1, isX2, isX3, X1Size, X2Size, X3Size,  ismin1, ismid1, ismax1,
                                                ismin2, ismid2, ismax2,
                                                ismin3, ismid3, ismax3] = markList
    paramObj=ObjectsTools.getParamObj()
    paramLabel=paramObj.Name
    paramLabel=paramLabel+"."
    curCoordinateSys = obj.Document.CoordinateSystem


    if curCoordinateSys==CoordinateSystemTools.CoordinateType.Rectangular:
        obj.X=False
        obj.Y=False
        obj.Z=False
        
        obj.min_1 = ismin1
        obj.mid_1 = ismid1
        obj.max_1 = ismax1
    
        obj.min_2 = ismin2
        obj.mid_2 = ismid2
        obj.max_2 = ismax2

        obj.min_3 = ismin3
        obj.mid_3 = ismid3
        obj.max_3 = ismax3
        if isX1:
            obj.X=True
            if UnitTools.getTypeOfData(X1Size) !=UnitTools.SupportUnitType.STRING:
                obj.X_Value=X1Size
            else:
                obj.setExpression("X_Value",u""+paramLabel+str(X1Size))
        if isX2:
            obj.Y=True
            if UnitTools.getTypeOfData(X2Size) !=UnitTools.SupportUnitType.STRING:
                obj.Y_Value=X2Size
            else:
                obj.setExpression("Y_Value",u""+paramLabel+str(X2Size))
        if isX3:
            obj.Z=True
            if UnitTools.getTypeOfData(X3Size) !=UnitTools.SupportUnitType.STRING:
                obj.Z_Value=X3Size
            else:
                obj.setExpression("Z_Value",u""+paramLabel+str(X3Size))
    elif curCoordinateSys==CoordinateSystemTools.CoordinateType.Polar:
        obj.R=False
        obj.Theta=False
        obj.Z=False
        
        obj.min_1 = ismin1
        obj.mid_1 = ismid1
        obj.max_1 = ismax1
    
        obj.min_2 = ismin2
        obj.mid_2 = ismid2
        obj.max_2 = ismax2

        obj.min_3 = ismin3
        obj.mid_3 = ismid3
        obj.max_3 = ismax3

        if isX1:
            obj.R=True
            if UnitTools.getTypeOfData(X1Size) !=UnitTools.SupportUnitType.STRING:
                obj.R_Value=X1Size
            else:
                obj.setExpression("R_Value",u""+paramLabel+str(X1Size))
        if isX2:
            obj.Theta=True
            if UnitTools.getTypeOfData(X2Size) !=UnitTools.SupportUnitType.STRING:
                obj.Theta_Value=X2Size
            else:
                obj.setExpression("Theta_Value",u""+paramLabel+str(X2Size))
        if isX3:
            obj.Z=True
            if UnitTools.getTypeOfData(X3Size) !=UnitTools.SupportUnitType.STRING:
                obj.Z_Value=X3Size
            else:
                obj.setExpression("Z_Value",u""+paramLabel+str(X3Size))       
    elif curCoordinateSys==CoordinateSystemTools.CoordinateType.Cylindrical:
        obj.R=False
        obj.Theta=False
        obj.Z=False
        
        obj.min_1 = ismin1
        obj.mid_1 = ismid1
        obj.max_1 = ismax1
    
        obj.min_2 = ismin2
        obj.mid_2 = ismid2
        obj.max_2 = ismax2

        obj.min_3 = ismin3
        obj.mid_3 = ismid3
        obj.max_3 = ismax3

        if isX1:
            obj.Z=True
            if UnitTools.getTypeOfData(X1Size) !=UnitTools.SupportUnitType.STRING:
                obj.Z_Value=X1Size
            else:
                obj.setExpression("Z_Value",u""+paramLabel+str(X1Size))
        if isX2:
            obj.R=True
            if UnitTools.getTypeOfData(X2Size) !=UnitTools.SupportUnitType.STRING:
                obj.R_Value=X2Size
            else:
                obj.setExpression("R_Value",u""+paramLabel+str(X2Size))
        if isX3:
            obj.Theta=True
            if UnitTools.getTypeOfData(X3Size) !=UnitTools.SupportUnitType.STRING:
                obj.Theta_Value=X3Size
            else:
                obj.setExpression("Theta_Value",u""+paramLabel+str(X3Size)) 
    # if curCoordinateSys == CoordinateSystemTools.CoordinateType.Rectangular:
    #     obj.X = isX1
    #     obj.Y = isX2
    #     obj.Z = isX3
    
    #     if isX1:
    #         X1SizeWithoutUnit=X1Size.split('mm')[0]
    #         if isNumber(X1SizeWithoutUnit):
    #             obj.X_Value.Value = float(X1SizeWithoutUnit)*0.001
    #         else:
    #             obj.setExpression("X_Value",u"dd."+str(X1SizeWithoutUnit))
    #     if isX2:
    #         x2SizeWithoutUnit=X2Size.split('mm')[0]
    #         if isNumber(x2SizeWithoutUnit):
    #             obj.Y_Value.Value = float(x2SizeWithoutUnit)*0.001
    #         else:
    #             obj.setExpression("Y_Value",u"dd."+str(x2SizeWithoutUnit))
    #     if isX3:
    #         X3SizeWithoutUnit=X3Size.split('mm')[0]
    #         if isNumber(X3SizeWithoutUnit):
    #             obj.Z_Value.Value = float(X3SizeWithoutUnit)*0.001
    #         else:
    #             obj.setExpression("Z_Value",u"dd."+str(X3SizeWithoutUnit))

    # elif curCoordinateSys == CoordinateSystemTools.CoordinateType.Polar or CoordinateSystemTools.CoordinateType.Cylindrical:
    #     obj.R = isX1
    #     obj.Theta = isX2
    #     obj.Z = isX3
    #     if isX1:
    #         X1SizeWithoutUnit=X1Size.split('mm')[0]
    #         if isNumber(X1SizeWithoutUnit):
    #             obj.R_Value.Value = float(X1SizeWithoutUnit)*0.001
    #         else:
    #             obj.setExpression("R_Value",u"dd."+str(X1SizeWithoutUnit))
    #     if isX2:
    #         x2SizeWithoutUnit=X2Size.split('deg')[0]
    #         if isNumber(x2SizeWithoutUnit):
    #             obj.Theta_Value.Value = float(x2SizeWithoutUnit)
    #         else:
    #             obj.setExpression("Theta_Value",u"dd."+str(x2SizeWithoutUnit))
    #     if isX3:
    #         X3SizeWithoutUnit=X3Size.split('mm')[0]
    #         if isNumber(X3SizeWithoutUnit):
    #             obj.Z_Value.Value = float(X3SizeWithoutUnit)*0.001
    #         else:
    #             obj.setExpression("Z_Value",u"dd."+str(X3SizeWithoutUnit))


# 为几何体设置attribute参数
def __setAttribute(obj, attributeList):

    obj.Attribute = attributeList[0]
    # FreeCAD.Console.PrintError('\n'+str(attributeList)+'\n')
    if len(attributeList) == 10:
        try:
            obj.ConductivitySIGMA = attributeList[1]
            obj.ConductivitySIGMAValue = float(attributeList[2])
            obj.RelativeDielectricConstant = attributeList[3]
            obj.SetEPS = float(attributeList[4])
            obj.SetEPS2 = float(attributeList[5])
            obj.SetEPS3 = float(attributeList[6])
            obj.CS_SetEPS = float(attributeList[7])
            obj.CS_SetEPS2 = float(attributeList[8])
            obj.CS_SetEPS3 = float(attributeList[9])
        except:
            pass

# 点
def __createPoint(infoList,order):
    import Modeling.Modeling3D.Modeling3DCommand.Point.CreatePoint as CreatePoint
    obj = CreatePoint.createPoint()
    [label, pointXYZ] = infoList[:-15]
    label = '[' + str(order) + ']_' + label
    # 设置网格
    markList = infoList[-15:]
    __setMark(obj, markList)
    obj.Label = label
    #这里将对象的属性名称传入
    __getPointVector(obj, pointXYZ,"Point")
    return obj

# ConformalLine
def __createConformalLine(infoList,order):
    import Modeling.Modeling3D.Modeling3DCommand.Line_Conformal.CreateConformalLine as CreateConformalLine
    obj = CreateConformalLine.createConformalLine()
    [label, pointXYZ1,pointXYZ2] = infoList[:-15]
    label = '[' + str(order) + ']_' + label
    # 设置网格
    markList = infoList[-15:]
    __setMark(obj, markList)
    obj.Order = order
    obj.Label = label
    __getPointVector(obj, pointXYZ1,"Point1")
    __getPointVector(obj, pointXYZ2,"Point2")

    curCoordinateSys = obj.Document.CoordinateSystem
    if curCoordinateSys == CoordinateSystemTools.CoordinateType.Rectangular:
        if pointXYZ1[1] == pointXYZ2[1] and pointXYZ1[2] == pointXYZ2[2]:
            obj.Normal = 'x'
        elif pointXYZ1[0] == pointXYZ2[0] and pointXYZ1[2] == pointXYZ2[2]:
            obj.Normal = 'y'
        else:
            obj.Normal = 'z'
    elif curCoordinateSys==CoordinateSystemTools.CoordinateType.Polar :
        FreeCAD.Console.PrintMessage(pointXYZ1)
        FreeCAD.Console.PrintMessage(pointXYZ2)
        
        if pointXYZ1[1] == pointXYZ2[1] and pointXYZ1[2] == pointXYZ2[2]:
            obj.Normal = 'r'
        elif pointXYZ1[0] == pointXYZ2[0] and pointXYZ1[2] == pointXYZ2[2]:
            obj.Normal = 'theta'
        else:
            obj.Normal = 'z'
    elif CoordinateSystemTools.CoordinateType.Cylindrical:
        if pointXYZ1[1] == pointXYZ2[1] and pointXYZ1[2] == pointXYZ2[2]:
            obj.Normal = 'z'
        elif pointXYZ1[0] == pointXYZ2[0] and pointXYZ1[2] == pointXYZ2[2]:
            obj.Normal = 'r'
        else:
            obj.Normal = 'theta'
    else:
        pass
    return obj

# ObliqueLine
def __createObliqueLine(infoList,order):
    import Modeling.Modeling3D.Modeling3DCommand.Line_Oblique.CreateObliqueLine as CreateObliqueLine
    obj = CreateObliqueLine.createObliqueLine()
    [label, pointXYZ1,pointXYZ2] = infoList[:-15]
    label = '[' + str(order) + ']_' + label
    # 设置网格
    markList = infoList[-15:]
    __setMark(obj, markList)
    obj.Order = order
    obj.Label = label
    __getPointVector(obj, pointXYZ1,"Point1")
    __getPointVector(obj, pointXYZ2,"Point2")
    # obj.BottomRadius = float(baseradius.split('mm')[0])
    return obj

# ConformalArea
def __createConformalArea(infoList,order):
    import Modeling.Modeling3D.Modeling3DCommand.Area_Conformal.CreateConformalArea as CreateConformalArea
    obj = CreateConformalArea.createConformalArea()
    [label, pointXYZ1,pointXYZ2] = infoList[:-15]
    label = '[' + str(order) + ']_' + label
    # 设置网格
    markList = infoList[-15:]
    __setMark(obj, markList)
    obj.Order = order
    obj.Label = label
    __getPointVector(obj, pointXYZ1,"Point1")
    __getPointVector(obj, pointXYZ2,"Point2")

    curCoordinateSys = obj.Document.CoordinateSystem
    if curCoordinateSys == CoordinateSystemTools.CoordinateType.Rectangular:
        if pointXYZ1[0] == pointXYZ2[0]:
            obj.Normal = 'x'
        elif pointXYZ1[1] == pointXYZ2[1]:
            obj.Normal = 'y'
        else:
            obj.Normal = 'z'
    elif curCoordinateSys == CoordinateSystemTools.CoordinateType.Polar :
        if pointXYZ1[0] == pointXYZ2[0]:
            obj.Normal = 'r'
        elif pointXYZ1[1] == pointXYZ2[1]:
            obj.Normal = 'theta'
        else:
            obj.Normal = 'z'
    elif curCoordinateSys==CoordinateSystemTools.CoordinateType.Cylindrical:
        if pointXYZ1[0] == pointXYZ2[0]:
            obj.Normal = 'z'
        elif pointXYZ1[1] == pointXYZ2[1]:
            obj.Normal = 'r'
        else:
            obj.Normal = 'theta'
    else:
        pass

    return obj

# RectangularArea
def __createRectangularArea(infoList,order):
    import Modeling.Modeling3D.Modeling3DCommand.Area_Rectangular.CreateRectangular as CreateRectangular
    obj = CreateRectangular.createRectangular()
    [label, pointXYZ1,pointXYZ2] = infoList[:-15]
    label = '[' + str(order) + ']_' + label
    # 设置网格
    markList = infoList[-15:]
    __setMark(obj, markList)
    obj.Order = order
    obj.Label = label
    __getPointVector(obj, pointXYZ1,"Point1")
    __getPointVector(obj, pointXYZ2,"Point2")
    return obj

# PolygonalArea多边形面
def __createPolygonalArea(infoList,order):
    import Modeling.Modeling3D.Modeling3DCommand.Area_Polygonal.CreatePolygonal as CreatePolygonal
    obj = CreatePolygonal.createPolygonal()
    # [label, pointXYZList] = infoList[:-15]
    label=infoList[0]
    pointXYZList=infoList[1:-15]
    label = '[' + str(order) + ']_' + label
    # 设置网格
    markList = infoList[-15:]
    __setMark(obj, markList)
    obj.Order = order
    obj.Label = label
    obj.NumbersOfPoints = len(pointXYZList)
    for i in range(len(pointXYZList)):
        pointStr = "Point" + str(i + 1)
        __getPointVector(obj, pointXYZList[i],pointStr)
        # setattr(obj, pointStr, __getPointVector(obj, pointXYZList[i]))
    return obj

# ConformalVolume投影体
def __createConformalVolume(infoList,order):
    import Modeling.Modeling3D.Modeling3DCommand.Vol_Conformal.CreateConformal as CreateConformal
    obj = CreateConformal.createConformal()
    [label, pointXYZ1, pointXYZ2] = infoList[:-16]

    label = '[' + str(order) + ']_' + label
    # 设置网格
    markList = infoList[-15:]
    __setMark(obj, markList)
    # 设置属性
    attributeList = infoList[-16]
    __setAttribute(obj, attributeList)
    obj.Order = order
    obj.Label = label
    __getPointVector(obj, pointXYZ1,"Point1")
    __getPointVector(obj, pointXYZ2,"Point2")
    return obj

# SpecialConeVolume圆锥或圆台
def __createSpecialConeVolume(infoList,order):
    import Modeling.Modeling3D.Modeling3DCommand.Vol_SpecialCone.CreateSpecialCone as CreateSpecialCone
    obj = CreateSpecialCone.createSpecialCone()
    [label, pointXYZ1, pointXYZ2, baseradius, topradius] = infoList[:-16]

    label = '[' + str(order) + ']_' + label
    # 设置网格
    markList = infoList[-15:]
    __setMark(obj, markList)
    # 设置属性
    attributeList = infoList[-16]
    __setAttribute(obj, attributeList)
    obj.Order = order
    obj.Label = label
    __getPointVector(obj, pointXYZ1,"PointBottom")
    __getPointVector(obj, pointXYZ2,"PointTop")
    ObjectsTools.turnExpressionToProperty(obj,"RadiusBottom",baseradius)
    ObjectsTools.turnExpressionToProperty(obj,"RadiusTop",topradius)
    # obj.RadiusBottom = float(baseradius.split('mm')[0])
    # obj.RadiusTop = float(topradius.split('mm')[0])
    return obj

# AnnularVolume环面体
def __createAnnularVolume(infoList,order):
    import Modeling.Modeling3D.Modeling3DCommand.Vol_Annular.CreateAnnular as CreateAnnular
    obj = CreateAnnular.createAnnular()
    # FreeCAD.Console.PrintMessage("\ntest_infolist:\n")
    # FreeCAD.Console.PrintMessage(infoList)
    [label, pointXYZ1, pointXYZ2, radius_inner, radius_outer] = infoList[:-16]
    FreeCAD.Console.PrintMessage("\n关于树状结构:\n")
    FreeCAD.Console.PrintMessage(label)
    label = '[' + str(order) + ']_' + label
    FreeCAD.Console.PrintMessage("\n关于树状结构：\n")
    FreeCAD.Console.PrintMessage(label)
    # 设置网格
    markList = infoList[-15:]
    __setMark(obj, markList)
    # 设置属性
    attributeList = infoList[-16]
    __setAttribute(obj, attributeList)
    obj.Order = order
    obj.Label = label
    __getPointVector(obj, pointXYZ1,"Point_1")
    __getPointVector(obj, pointXYZ2,"Point_2")
    if type(radius_inner)==str:
        ObjectsTools.turnExpressionToProperty(obj,"RadiusInside",radius_inner)
        ObjectsTools.turnExpressionToProperty(obj, "RadiusOutside", radius_outer)
    else:
        ObjectsTools.turnExpressionToProperty(obj, "RadiusInside", radius_inner[0])
        ObjectsTools.turnExpressionToProperty(obj,"RadiusOutside",radius_outer[0])
    # obj.RadiusInside = float(radius_inner.split('mm')[0])
    # obj.RadiusOutside = float(radius_outer.split('mm')[0])

    return obj

# AnnularSectionVolume部分环面体
def __createAnnular_SectionVolume(infoList,order):
    import Modeling.Modeling3D.Modeling3DCommand.Vol_Annular_Section.CreateAnnular_Section as CreateAnnular_Section
    obj = CreateAnnular_Section.createAnnular_Section()
    [label, pointXYZ1, pointXYZ2, radius_inner, radius_outer, pointXYZ3, pointXYZ4] = infoList[:-16]
    label = '[' + str(order) + ']_' + label
    # 设置网格
    markList = infoList[-15:]
    __setMark(obj, markList)
    # 设置属性
    attributeList = infoList[-16]
    __setAttribute(obj, attributeList)
    obj.Order = order
    obj.Label = label
    __getPointVector(obj, pointXYZ1,"Point1")
    __getPointVector(obj, pointXYZ2,"Point2")
    __getPointVector(obj, pointXYZ3,"Point3")
    __getPointVector(obj, pointXYZ4,"Point4")
    ObjectsTools.turnExpressionToProperty(obj,"InnerRadius",radius_inner)
    ObjectsTools.turnExpressionToProperty(obj,"OuterRadius",radius_outer)

    # obj.InnerRadius = float(radius_inner.split('mm')[0])
    # obj.OuterRadius = float(radius_outer.split('mm')[0])
    return obj

# CylinderVolume圆柱体
def __createCylinderVolume(infoList,order):
    import Modeling.Modeling3D.Modeling3DCommand.Vol_Cylinder.CreateCylinder as CreateCylinder
    obj = CreateCylinder.createCylinder()
    [label, pointXYZ1, pointXYZ2, radius] = infoList[:-16]
    label = '[' + str(order) + ']_' + label
    # 设置网格
    markList = infoList[-15:]
    __setMark(obj, markList)
    # 设置属性
    attributeList = infoList[-16]
    __setAttribute(obj, attributeList)
    obj.Order = order
    obj.Label = label
    __getPointVector(obj, pointXYZ1,"Point_1")
    __getPointVector(obj, pointXYZ2,"Point_2")
    ObjectsTools.turnExpressionToProperty(obj,"Radius",radius)
    # obj.Radius = float(radius.split('mm')[0])
    return obj
# Parallelepipedal平行六面体
def __createParallelepipedalVolume(infoList,order):
    import Modeling.Modeling3D.Modeling3DCommand.Vol_Parallelepipedal.CreateParallelepipedal as CreateParallelepipedal
    obj = CreateParallelepipedal.createParallelepipedal()
    [label, pointXYZ1, pointXYZ2, pointXYZ3, pointXYZ4] = infoList[:-16]
    label = '[' + str(order) + ']_' + label
    # 设置网格
    markList = infoList[-15:]
    __setMark(obj, markList)
    # 设置属性
    attributeList = infoList[-16]
    __setAttribute(obj, attributeList)
    obj.Order = order
    obj.Label = label
    __getPointVector(obj, pointXYZ1,"Point_0")
    __getPointVector(obj, pointXYZ2,"Point_1")
    __getPointVector(obj, pointXYZ3,"Point_2")
    __getPointVector(obj, pointXYZ4,"Point_3")
    return obj

# Spherical球体
def __createSphericalVolume(infoList,order):
    import Modeling.Modeling3D.Modeling3DCommand.Vol_Spherical.CreateSpherical as CreateSpherical
    obj = CreateSpherical.createSpherical()
    [label, pointXYZ, radius] = infoList[:-16]
    label = '[' + str(order) + ']_' + label
    # 设置网格
    markList = infoList[-15:]
    __setMark(obj, markList)
    # 设置属性
    # FreeCAD.Console.PrintError('\n球体参数列表：'+str(infoList)+'\n')
    attributeList = infoList[-16]
    __setAttribute(obj, attributeList)
    obj.Order = order
    obj.Label = label
    __getPointVector(obj, pointXYZ,"CenterPoint")
    ObjectsTools.turnExpressionToProperty(obj,"Radius",radius)
    # obj.Radius = float(radius.split('mm')[0])
    return obj

# Pyramid棱锥体
def __createPyramidVolume(infoList,order):
    import Modeling.Modeling3D.Modeling3DCommand.Vol_Pyramid.CreatePyramid as CreatePyramid
    obj = CreatePyramid.createPyramid()
    [label, pointXYZ1, pointXYZ2, pointXYZ3, pointXYZ4, pointXYZ5] = infoList[:-16]
    label = '[' + str(order) + ']_' + label
    # 设置网格
    markList = infoList[-15:]
    __setMark(obj, markList)
    # 设置属性
    attributeList = infoList[-16]
    __setAttribute(obj, attributeList)
    obj.Order = order
    obj.Label = label
    __getPointVector(obj, pointXYZ1,"Point_1")
    __getPointVector(obj, pointXYZ2,"Point_2")
    __getPointVector(obj, pointXYZ3,"Point_3")
    __getPointVector(obj, pointXYZ4,"Point_4")
    __getPointVector(obj, pointXYZ5,"Point_5")
    return obj

# Toroidal_Section部分圆环体
def __createToroidal_SectionVolume(infoList,order):
    import Modeling.Modeling3D.Modeling3DCommand.Vol_Toroidal_Section.CreateToroidal_Section as CreateToroidal_Section
    obj =  CreateToroidal_Section.createToroidal_Section()
    [label, pointXYZ1, pointXYZ2, majorRadius, minorRadius, pointXYZ3, pointXYZ4] = infoList[:-16]
    label = '[' + str(order) + ']_' + label
    # 设置网格
    markList = infoList[-15:]
    __setMark(obj, markList)
    # 设置属性
    attributeList = infoList[-16]
    __setAttribute(obj, attributeList)
    obj.Order = order
    obj.Label = label
    __getPointVector(obj, pointXYZ1,"Point1")
    __getPointVector(obj, pointXYZ2,"Point2")
    __getPointVector(obj, pointXYZ3,"Point3")
    __getPointVector(obj, pointXYZ4,'Point4')
    ObjectsTools.turnExpressionToProperty(obj,"MajorRadius",majorRadius)
    ObjectsTools.turnExpressionToProperty(obj,"MinorRadius",minorRadius)
    # obj.MajorRadius = float(majorRadius.split('mm')[0])
    # obj.MinorRadius = float(minorRadius.split('mm')[0])
    return obj

# Wedge楔形体
def __createWedgeVolume(infoList,order):
    import Modeling.Modeling3D.Modeling3DCommand.Vol_Wedge.CreateWedge as CreateWedge
    obj = CreateWedge.createWedge()
    [label, pointXYZ1, pointXYZ2, pointXYZ3, pointXYZ4, pointXYZ5, pointXYZ6] = infoList[:-16]
    label = '[' + str(order) + ']_' + label
    # 设置网格
    markList = infoList[-15:]
    __setMark(obj, markList)
    # 设置属性
    attributeList = infoList[-16]
    __setAttribute(obj, attributeList)
    obj.Order = order
    obj.Label = label
    __getPointVector(obj, pointXYZ1,"Point_1")
    __getPointVector(obj, pointXYZ2,"Point_2")
    __getPointVector(obj, pointXYZ3,"Point_3")
    __getPointVector(obj, pointXYZ4,"Point_4")
    __getPointVector(obj, pointXYZ5,"Point_5")
    __getPointVector(obj, pointXYZ6,"Point_6")
    return obj

# Tetrahedron四面体
def __createTetrahedronVolume(infoList,order):
    import Modeling.Modeling3D.Modeling3DCommand.Vol_Tetrahedron.CreateTetrahedron as CreateTetrahedron
    obj = CreateTetrahedron.createTetrahedron()
    [label, pointXYZ1, pointXYZ2, pointXYZ3, pointXYZ4] = infoList[:-16]
    label = '[' + str(order) + ']_' + label
    # 设置网格
    markList = infoList[-15:]
    __setMark(obj, markList)
    # 设置属性
    attributeList = infoList[-16]
    __setAttribute(obj, attributeList)
    obj.Order = order
    obj.Label = label
    __getPointVector(obj, pointXYZ1,"Point_1")
    __getPointVector(obj, pointXYZ2,"Point_2")
    __getPointVector(obj, pointXYZ3,"Point_3")
    __getPointVector(obj, pointXYZ4,"Point_4")
    return obj

# Rhombus菱形体
def __createRhombusVolume(infoList,order):
    import Modeling.Modeling3D.Modeling3DCommand.Vol_Rhombus.CreateRhombus as CreateRhombus
    obj = CreateRhombus.createRhombus()
    [label, pointXYZ1, pointXYZ2, pointXYZ3, pointXYZ4, pointXYZ5, pointXYZ6, pointXYZ7, pointXYZ8] = infoList[:-16]
    label = '[' + str(order) + ']_' + label
    # 设置网格
    markList = infoList[-15:]
    __setMark(obj, markList)
    # 设置属性
    attributeList = infoList[-16]
    __setAttribute(obj, attributeList)
    obj.Order = order
    obj.Label = label
    __getPointVector(obj, pointXYZ1,"Point_1")
    __getPointVector(obj, pointXYZ2,"Point_2")
    __getPointVector(obj, pointXYZ3,"Point_3")
    __getPointVector(obj, pointXYZ4,"Point_4")
    __getPointVector(obj, pointXYZ5,"Point_5")
    __getPointVector(obj, pointXYZ6,"Point_6")
    __getPointVector(obj, pointXYZ7,"Point_7")
    __getPointVector(obj, pointXYZ8,"Point_8")
    return obj

# Extruded挤出体
def __createExtrudedVolume(infoList,order):
    import Modeling.Modeling3D.Modeling3DCommand.Vol_Extruded.CreateExtruded as CreateExtruded
    obj = CreateExtruded.createExtruded()
    [label, areaLabel, lineLabel] = infoList[:-16]
    label = '[' + str(order) + ']_' + label
    # 设置网格
    markList = infoList[-15:]
    __setMark(obj, markList)
    # 设置属性
    attributeList = infoList[-16]
    __setAttribute(obj, attributeList)
    obj.Order = order
    obj.Label = label

    # 将ExtrudedObj和他的面线参数返回
    return [obj,areaLabel, lineLabel]

def __createRevolutionVolume(infoList,order):
    import Modeling.Modeling3D.Modeling3DCommand.Vol_Revolution.Command.CreateRevolution as CreateRevolution
    obj=CreateRevolution.createRevolution()
    [label, pointBase, pointTop, areaLabel] = infoList[:-16]
    label = '[' + str(order) + ']_' + label
    # 设置网格
    markList = infoList[-15:]
    __setMark(obj, markList)
    # 设置属性
    attributeList = infoList[-16]
    __setAttribute(obj, attributeList)
    obj.Order = order
    obj.Label = label
    __getPointVector(obj, pointBase, "Point_Base")
    __getPointVector(obj, pointTop, "Point_Top")

    return [obj, areaLabel]

# Helical螺旋体
def __createHelicalVolume(infoList,order):
    import Modeling.Modeling3D.Modeling3DCommand.Vol_Helical.CreateHelical as CreateHelical
    obj = CreateHelical.createHelical()
    [label, basePoint, topPoint, inner_radius,outer_radius, startPoint, pitch, width] = infoList[:-16]
    label = '[' + str(order) + ']_' + label
    # 设置网格
    markList = infoList[-15:]
    __setMark(obj, markList)
    # 设置属性
    attributeList = infoList[-16]
    __setAttribute(obj, attributeList)
    obj.Order = order
    obj.Label = label
    __getPointVector(obj, basePoint,"BasePoint")
    __getPointVector(obj, topPoint,"TopPoint")
    __getPointVector(obj, startPoint,"StartPoint")
    ObjectsTools.turnExpressionToProperty(obj,"InnerRadius",inner_radius)
    ObjectsTools.turnExpressionToProperty(obj,"OuterRadius",outer_radius)
    ObjectsTools.turnExpressionToProperty(obj,"Pitch",pitch)
    ObjectsTools.turnExpressionToProperty(obj,"Width",width)
    # obj.InnerRadius = float(inner_radius.split('mm')[0])
    # obj.OuterRadius = float(outer_radius.split('mm')[0])
    # obj.Pitch = float(pitch.split('mm')[0])
    # obj.Width = float(width.split('mm')[0])
    return obj
def __createFunctionVolume(infoList,order):
    import Modeling.Modeling3D.Modeling3DCommand.Vol_Function.CreateFunction as CreateFunction
    obj = CreateFunction.createFunction()
    [label, Point_1, Point_2,funStr] = infoList[:-16]
    label = '[' + str(order) + ']_' + label
    # 设置网格
    markList = infoList[-15:]
    __setMark(obj, markList)
    # 设置属性
    attributeList = infoList[-16]
    __setAttribute(obj, attributeList)
    obj.Order = order
    obj.Label = label
    obj.Expression=funStr
    __getPointVector(obj, Point_1,"Point_1")
    __getPointVector(obj, Point_2,"Point_2")

# 循环体
def __createArrayObject(system, baseObj, infoList):
    """
        system: 当前坐标系
        baseObj: 基本模型对象
        infoList: M3d 传过来的参数列表
    """
    import Modeling.Modeling3D.Modeling3DCommand.Object_Array.ArrayDraft as ArrayDraft
    if system == CoordinateSystemTools.CoordinateType.Rectangular:
        [label, baseObjLabel, arrayType, centerAxis, orthoFace, numX, numY, numZ, num, numPolar, stepX, stepY, stepZ] = infoList
        # FreeCAD.Console.PrintMessage("label1: "+str(label)+"\n")
        label=label.replace("Arr_","")
        # FreeCAD.Console.PrintMessage("label2: "+str(label)+"\n")
        if arrayType == "linear":
            objArray = ArrayDraft.makeArray(baseObj, label, arrayType, stepX, stepY, stepZ, num)
        elif arrayType == "ortho":
            if orthoFace == "XY":
                objArray = ArrayDraft.makeArray(baseObj, label, arrayType, orthoFace, stepX, stepY, numX, numY)
            elif orthoFace == "XZ":
                objArray = ArrayDraft.makeArray(baseObj, label, arrayType, orthoFace, stepX, stepZ, numX, numZ)
            elif orthoFace == "YZ":
                objArray = ArrayDraft.makeArray(baseObj, label, arrayType, orthoFace, stepY, stepZ, numY, numZ)
        elif arrayType == "polar":
            objArray = ArrayDraft.makeArray(baseObj, label, arrayType, centerAxis, numPolar)
    elif system == CoordinateSystemTools.CoordinateType.Polar:
        [label, baseObjLabel, arrayType, numR, numZ, num, numPolar, stepR, stepTheta, stepZ] = infoList
        if arrayType == "linear":
            objArray = ArrayDraft.makeArrayPolar(baseObj, label, arrayType, stepR, stepTheta, stepZ, num)
        elif arrayType == "ortho":
            objArray = ArrayDraft.makeArrayPolar(baseObj, label, arrayType, stepR, stepZ, numR, numZ)
        elif arrayType == "polar":
            objArray = ArrayDraft.makeArrayPolar(baseObj, label, arrayType, numPolar)
    else:
        [label, baseObjLabel, arrayType, numR, numZ, num, numPolar, stepZ,stepR, stepTheta] = infoList
        if arrayType == "linear":
            objArray = ArrayDraft.makeArrayPolar(baseObj, label, arrayType, stepR, stepTheta, stepZ, num)
        elif arrayType == "ortho":
            objArray = ArrayDraft.makeArrayPolar(baseObj, label, arrayType, stepR, stepZ, numR, numZ)
        elif arrayType == "polar":
            objArray = ArrayDraft.makeArrayPolar(baseObj, label, arrayType, numPolar)
    ArrayDraft.autogroup(objArray)
    FreeCAD.ActiveDocument.recompute()


def VarReplace(temp_Var_string, num):
    num = num
    Var_string = temp_Var_string.replace("'i'", str(num))

    #直接使用split进行划分
    Point_info = Var_string.split(",")

    return Point_info



def setValue(obj, paramName, paramValue):
    paramObj = ObjectsTools.getParamObj()
    result = UnitTools.getTypeOfPossiblePropertyName(paramObj, "", paramValue, isParamObjSelf=False)
    # FreeCAD.Console.PrintMessage("value: " + str(result) + "\n")
    if result[0] != "" and result[1] != UnitTools.SupportUnitType.STRING:
        obj.setExpression(paramName, result[0])
