# -*- coding: utf-8 -*-
import FreeCAD, Part, math
from FreeCAD import Base
from pivy import coin
import DocumentTools
import CoordinateSystemTools
import ObjectsTools
import re
import UnitTools

# 判断是数还是字符串
def isNumber(n):
    result=True
    try:
        num=float(n)
        result = num == num
    except ValueError:
        result=False
    return result

# 获取当前激活场景中所有的模型对象及具体信息
def getModelingCommands():
    """
        return:[] modlelingCommandList
        """
    modlelingCommandList=[]
    # 按顺序获取当前模型的列表
    # FreeCAD.Console.PrintError('\n进入获取模型命令的函数\n')
    objectList = ObjectsTools.getListOfOrderedObjects(FreeCAD.ActiveDocument.Name)
    for objItem in objectList:
        # FreeCAD.Console.PrintError('\nlist:  '+str(objItem.Type)+'\n')
        # try:
        # 点
        # FreeCAD.Console.PrintMessage("\n")
        # FreeCAD.Console.PrintMessage(__get)
        if objItem.Type == ObjectsTools.ObjectType.Point:
            # 正常的模型传1，被阵列体的模型传0
            modlelingCommandList.append([objItem.Type,__getPointInfo(objItem,1)])
        # 线或面
        elif (objItem.Type == ObjectsTools.ObjectType.Line_Conformal or
                objItem.Type == ObjectsTools.ObjectType.Area_Conformal or
                objItem.Type == ObjectsTools.ObjectType.Area_Rectangular):
            modlelingCommandList.append([objItem.Type,__getLineOrAreaInfo(objItem,objItem.Type,1)])
        # 斜线
        elif objItem.Type == ObjectsTools.ObjectType.Line_Oblique:
            modlelingCommandList.append([objItem.Type, __getObliqueLineInfo(objItem,1)])
        # 多边形面
        elif objItem.Type == ObjectsTools.ObjectType.Area_Polygonal:
            modlelingCommandList.append([objItem.Type, __getPolygonalAreaInfo(objItem,1)])
        # 投影体
        elif objItem.Type == ObjectsTools.ObjectType.Vol_Conformal:
            modlelingCommandList.append([objItem.Type,__getConformalVolumeInfo(objItem,1)])
        # 圆锥或圆台
        elif objItem.Type == ObjectsTools.ObjectType.Vol_SpecialCone:
            modlelingCommandList.append([objItem.Type,__getSpecialConeVolumeInfo(objItem,1)])
        # 环形体
        elif objItem.Type == ObjectsTools.ObjectType.Vol_Annular:
            modlelingCommandList.append([objItem.Type,__getAnnularVolumeInfo(objItem,1)])
        # 圆柱
        elif objItem.Type == ObjectsTools.ObjectType.Vol_Cylinder:
            modlelingCommandList.append([objItem.Type,__getCylinderVolumeInfo(objItem,1)])
        # 平行六面体
        elif objItem.Type == ObjectsTools.ObjectType.Vol_Parallelepipedal:
            modlelingCommandList.append([objItem.Type,__getParallelepipedalVolumeInfo(objItem,1)])
        # 球体
        elif objItem.Type == ObjectsTools.ObjectType.Vol_Spherical:
            modlelingCommandList.append([objItem.Type,__getSphericalVolumeInfo(objItem,1)])
        # 棱锥体
        elif objItem.Type == ObjectsTools.ObjectType.Vol_Pyramid:
            modlelingCommandList.append([objItem.Type, __getPyramidVolumeInfo(objItem,1)])
        # 部分圆环体
        elif objItem.Type == ObjectsTools.ObjectType.Vol_Toroidal_Section:
            modlelingCommandList.append([objItem.Type, __getToroidalSectionVolumeInfo(objItem,1)])
        # 楔形体
        elif objItem.Type == ObjectsTools.ObjectType.Vol_Wedge:
            modlelingCommandList.append([objItem.Type, __getWedgeVolumeInfo(objItem,1)])
        # 四面体
        elif objItem.Type == ObjectsTools.ObjectType.Vol_Tetrahedron:
            modlelingCommandList.append([objItem.Type, __getTetrahedronVolumeInfo(objItem,1)])
        # 菱形体
        elif objItem.Type == ObjectsTools.ObjectType.Vol_Rhombus:
            modlelingCommandList.append([objItem.Type, __getRhombusVolumeInfo(objItem,1)])
        # 部分环面体
        elif objItem.Type == ObjectsTools.ObjectType.Vol_Annular_Section:
            modlelingCommandList.append([objItem.Type, __getAnnularSectionVolumeInfo(objItem,1)])
        # 挤出体
        elif objItem.Type == ObjectsTools.ObjectType.Vol_Extruded:
            # 参数完整是才传给m3d
            if not __getExtrudedVolumeInfo(objItem,1) == "error":
                modlelingCommandList.append([objItem.Type, __getExtrudedVolumeInfo(objItem,1)])
        # 螺旋体
        elif objItem.Type == ObjectsTools.ObjectType.Vol_Helical:
            modlelingCommandList.append([objItem.Type, __getHelicalVolumeInfo(objItem,1)])
        # 草图拉伸
        elif objItem.Type==ObjectsTools.ObjectType.Vol_Draft_Extrude:
            m3dType=__getDraftExtrudeVolumeInfo(objItem,1)[0]
            modlelingCommandList.append([m3dType, __getDraftExtrudeVolumeInfo(objItem,1)[1:]])
        # 阵列体
        elif objItem.Type == ObjectsTools.ObjectType.Vol_Array:

            curCoordinateSys = objItem.Document.CoordinateSystem
            # 获取阵列体参数
            infoList = __getArrayObjectInfo(curCoordinateSys, objItem)
            objs = FreeCAD.ActiveDocument.getObjectsByLabel(infoList[1])
            # 获取阵列体基础几何体参数
            if len(objs):
                obj = objs[0]
                modlelingCommand = []
                # 点
                if objItem.BaseType == ObjectsTools.ObjectType.Point:
                    modlelingCommand = [objItem.BaseType, __getPointInfo(obj,0)]
                # 线或面
                elif (objItem.BaseType == ObjectsTools.ObjectType.Line_Conformal or
                        objItem.BaseType == ObjectsTools.ObjectType.Area_Conformal or
                        objItem.BaseType == ObjectsTools.ObjectType.Area_Rectangular):
                    modlelingCommand = [objItem.BaseType, __getLineOrAreaInfo(obj, objItem.BaseType,0)]
                # 斜线
                elif objItem.BaseType == ObjectsTools.ObjectType.Line_Oblique:
                    modlelingCommand = [objItem.BaseType, __getObliqueLineInfo(obj,0)]
                # 多边形面
                elif objItem.BaseType == ObjectsTools.ObjectType.Area_Polygonal:
                    modlelingCommand = [objItem.BaseType, __getPolygonalAreaInfo(obj,0)]
                # 投影体
                elif objItem.BaseType == ObjectsTools.ObjectType.Vol_Conformal:
                    modlelingCommand = [objItem.BaseType, __getConformalVolumeInfo(obj,0)]
                # 圆锥或圆台
                elif objItem.BaseType == ObjectsTools.ObjectType.Vol_SpecialCone:
                    modlelingCommand = [objItem.BaseType, __getSpecialConeVolumeInfo(obj,0)]
                # 环形体
                elif objItem.BaseType == ObjectsTools.ObjectType.Vol_Annular:
                    modlelingCommand = [objItem.BaseType, __getAnnularVolumeInfo(obj,0)]
                # 圆柱
                elif objItem.BaseType == ObjectsTools.ObjectType.Vol_Cylinder:
                    modlelingCommand = [objItem.BaseType, __getCylinderVolumeInfo(obj,0)]
                # 平行六面体
                elif objItem.BaseType == ObjectsTools.ObjectType.Vol_Parallelepipedal:
                    modlelingCommand = [objItem.BaseType, __getParallelepipedalVolumeInfo(obj,0)]
                # 球体
                elif objItem.BaseType == ObjectsTools.ObjectType.Vol_Spherical:
                    modlelingCommand = [objItem.BaseType, __getSphericalVolumeInfo(obj,0)]
                # 棱锥体
                elif objItem.BaseType == ObjectsTools.ObjectType.Vol_Pyramid:
                    modlelingCommand = [objItem.BaseType, __getPyramidVolumeInfo(obj,0)]
                # 部分圆环体
                elif objItem.BaseType == ObjectsTools.ObjectType.Vol_Toroidal_Section:
                    modlelingCommand = [objItem.BaseType, __getToroidalSectionVolumeInfo(obj,0)]
                # 楔形体
                elif objItem.BaseType == ObjectsTools.ObjectType.Vol_Wedge:
                    modlelingCommand = [objItem.BaseType, __getWedgeVolumeInfo(obj,0)]
                # 四面体
                elif objItem.BaseType == ObjectsTools.ObjectType.Vol_Tetrahedron:
                    modlelingCommand = [objItem.BaseType, __getTetrahedronVolumeInfo(obj,0)]
                # 菱形体
                elif objItem.BaseType == ObjectsTools.ObjectType.Vol_Rhombus:
                    modlelingCommand = [objItem.BaseType, __getRhombusVolumeInfo(obj,0)]
                # 部分环面体
                elif objItem.BaseType == ObjectsTools.ObjectType.Vol_Annular_Section:
                    modlelingCommand = [objItem.BaseType, __getAnnularSectionVolumeInfo(obj,0)]
                # 挤出体
                elif objItem.BaseType == ObjectsTools.ObjectType.Vol_Extruded:
                    # 参数完整是才传给m3d
                    if not __getExtrudedVolumeInfo(obj,0) == "error":
                        modlelingCommand = [objItem.BaseType, __getExtrudedVolumeInfo(obj,0)]
                # 螺旋体
                elif objItem.BaseType == ObjectsTools.ObjectType.Vol_Helical:
                    modlelingCommand = [objItem.BaseType, __getHelicalVolumeInfo(obj,0)]

                if modlelingCommand != []:
                    modlelingCommandList.append([objItem.Type, infoList, modlelingCommand])
        #参数阵列体
        elif objItem.Type == ObjectsTools.ObjectType.Vol_ParamArray:
            modlelingCommandList.append([objItem.Type,__getParamArrayVolumeInfo(objItem,1)])
        # 函数体
        elif objItem.Type==ObjectsTools.ObjectType.Vol_Function:
            modlelingCommandList.append([objItem.Type, __getFunctionVolumeInfo(objItem,1)])
        # except AttributeError:
        #     FreeCAD.Console.PrintMessage(str(objItem.Label)+" object has no attribute 'Type'")
        elif objItem.Type==ObjectsTools.ObjectType.Vol_Revolution or objItem.Type==ObjectsTools.ObjectType.Vol_Draft_Revolution:
            modlelingCommandList.append([ObjectsTools.ObjectType.Vol_Revolution, __getRevolutionVolumeInfo(objItem, 1)])
    return modlelingCommandList

# 获取全局变量列表
def getGlobalVariable():

    """return:[] globalVariableList 全局变量列表
                   [[name,value]......]
    """
    # @fubiao
    globalVariableList = []
    #定义变量的注释不能用canotBeStr
    canotBeStr="! ==============================================================================!"
    replaceStr="! =============================================================================!"
    
    paramText=FreeCAD.ActiveDocument.Company.replace(canotBeStr,replaceStr)
    # 将注释也加入m3d中，设置name="" val=注释内容
    commentList=re.findall(r"[!|！][^\n]*",paramText)

    #将以叹号开始的一行替换为";param;",
    paramText=re.sub(r"[!|！][^\n]*",";param;",paramText)
    paramText=paramText.replace(" ","").replace("\n","").replace("\r","")

    # realExpression=""
    # flag=True
    # for letter in paramText:
    #     if letter=="!"or letter==u"！":
    #         flag=not flag
    #     else:
    #         if flag:
    #             realExpression=realExpression+letter

    paramList=paramText.split(";")
    #遇到paramItem为param的时候，就读取一个commentList中的一个内容
    commentIndex=0
    for paramItem in paramList:
        if paramItem=="param":
            globalVariableList.append([commentList[commentIndex],"!COMMENT"])
            commentIndex=commentIndex+1
        else:
            paramNameAndValue=paramItem.split("=")
            if len(paramNameAndValue)>=2:
                paramName=paramNameAndValue[0]
                paramNameLower=paramName.lower()
                if paramNameLower.startswith("function"):
                    if len(paramName)>8:
                        paramName=paramName[:8].upper()+" "+paramName[8:]
                    else:
                        continue

                globalVariableList.append([paramName,paramNameAndValue[1]])
    # globalVariableList = []
    # objectList=FreeCAD.ActiveDocument.findObjects('App::FeaturePython')
    # for obj in objectList:
    #     propertiesList = obj.PropertiesList
    #     whiteList = ['Proxy','ExpressionEngine','DynamicData','Label','Shape']
    #     # 获得表达式列表
    #     expressionList=obj.ExpressionEngine
    #     for prop in propertiesList:
    #         if prop in whiteList:
    #             continue
    #         value = getattr(obj,prop)
    #         for expressionItem in expressionList:
    #             # 如果该属性在表达式列表中，取表达式中的值
    #             if expressionItem[0]==prop:
    #                 value=expressionItem[1]
    #                 break
    #         if  "=" in str(value):
    #             funStr=value.split("=")
    #             FreeCAD.Console.PrintMessage("funStr[0]: "+str(funStr[0])+" "+"funStr[1]: "+str(funStr[1])+"\n")
    #             globalVariableList.append([funStr[0],funStr[1]])
    #         elif len(str(value).split(' '))>1:
    #             value = str(value).split(' ')[0] + str(value).split(' ')[1]
    #             globalVariableList.append([prop, value])
    #         # fubiao 处理string 字符串函数
    #         elif prop!="Type" and value!="Variable":
    #             globalVariableList.append([prop, value])
    return globalVariableList

"获得当前激活场景中所有的模型对象,返回模型对象"
"所有的对象均有“type”属性"
def __getAllOfObjs():
    """
    return:[] objsList
    """
    actDoc=FreeCAD.ActiveDocument
    objectList=FreeCAD.ActiveDocument.findObjects('Part::FeaturePython')
    # 剔除没有Type属性的物体
    for objItem in objectList:
        if not ObjectsTools.hasTheProperty(objItem.Label,"Type"):
            objectList.remove(objItem)
    return objectList


# 获得带单位的点坐标
def __getUnitPoint(obj,point):
    """
    obj:该坐标点属于的对象，需要用于判断该点的坐标系
    point：vector属性
    return:[str(x1),str(x2),str(x3)] 
    """
    curCoordinateSys=obj.Document.CoordinateSystem
    resultPoint=[]
    x1="0mm"
    x2="0mm"
    x3="0mm"

    if curCoordinateSys==CoordinateSystemTools.CoordinateType.Rectangular:
        if isNumber(point[0]):
            x1=str(point[0])+UnitTools.DefaultUnits().getDefaultLengthUnit()
        else:
            x1=str(point[0])
        if isNumber(point[1]):
            x2=str(point[1])+UnitTools.DefaultUnits().getDefaultLengthUnit()
        else:
            x2=str(point[1])
            pass
        if isNumber(point[2]):
            x3=str(point[2])+UnitTools.DefaultUnits().getDefaultLengthUnit()
        else:
            x3=str(point[2])
    elif  curCoordinateSys==CoordinateSystemTools.CoordinateType.Polar:
        if isNumber(point[0]):
            x1=str(point[0])+UnitTools.DefaultUnits().getDefaultLengthUnit()
        else:
            x1=str(point[0])
        if isNumber(point[1]):
            x2=str(point[1])+UnitTools.DefaultUnits().getDefaultAngleUnit()
        else:
            x2=str(point[1])
        if isNumber(point[2]):
            x3=str(point[2])+UnitTools.DefaultUnits().getDefaultLengthUnit()
        else:
            x3=str(point[2])
    elif curCoordinateSys==CoordinateSystemTools.CoordinateType.Cylindrical:
        if isNumber(point[2]):
            x1=str(point[2])+UnitTools.DefaultUnits().getDefaultLengthUnit()
        else:
            x1=str(point[2])
        if isNumber(point[0]):
            x2=str(point[0])+UnitTools.DefaultUnits().getDefaultLengthUnit()
        else:
            x2=str(point[0])
        if isNumber(point[1]):
            x3=str(point[1])+UnitTools.DefaultUnits().getDefaultAngleUnit()
        else:
            x3=str(point[1])
    else:
        pass
    resultPoint=[x1,x2,x3]
    return resultPoint

# 获取带单位文本模型网格文件
def __getMarkCommands(obj):
    """
    obj:     物体对象
    return:  [Boolean(isX1),
              Boolean(isX2),
              Boolean(isX3),
              String(X1Size),
              String(X2Size),
              String(X3Size)]
    """
    objectLabel=obj.Label
    objs=FreeCAD.ActiveDocument.getObjectsByLabel(objectLabel)
    isX1=False 
    isX2=False
    isX3=False
    X1Size=""
    X2Size=""
    X3Size=""

    ismin_1 = False
    ismid_1 = False
    ismax_1 = False
    ismin_2 = False
    ismid_2 = False
    ismax_2 = False
    ismin_3 = False
    ismid_3 = False
    ismax_3 = False

    results=[]
    if len(objs):
        obj=objs[0]
        curCoordinateSys=obj.Document.CoordinateSystem
        # 由于老工程体不存在这些属性，放在异常处理处 @lzg
        # try:
        #     ismin_1 = obj.min_1
        #     ismid_1 = obj.mid_1
        #     ismax_1 = obj.max_1
        #     ismin_2 = obj.min_2
        #     ismid_2 = obj.mid_2
        #     ismax_2 = obj.max_2
        #     ismin_3 = obj.min_3
        #     ismid_3 = obj.mid_3
        #     ismax_3 = obj.max_3
        # except:
        #     pass
        if curCoordinateSys==CoordinateSystemTools.CoordinateType.Rectangular:
            isX1=obj.X
            isX2=obj.Y
            isX3=obj.Z
            # 由于老工程体不存在这些属性，放在异常处理处 @lzg
            try:
                ismin_1 = obj.min_1
                ismid_1 = obj.mid_1
                ismax_1 = obj.max_1
                ismin_2 = obj.min_2
                ismid_2 = obj.mid_2
                ismax_2 = obj.max_2
                ismin_3 = obj.min_3
                ismid_3 = obj.mid_3
                ismax_3 = obj.max_3
            except:
                pass
            if isNumber(ObjectsTools.turnPropertyToExpression(obj,"X_Value")):
                X1Size=str(ObjectsTools.turnPropertyToExpression(obj,"X_Value"))+UnitTools.DefaultUnits().getDefaultLengthUnit()
            else:
                X1Size=str(ObjectsTools.turnPropertyToExpression(obj,"X_Value"))
            if isNumber(ObjectsTools.turnPropertyToExpression(obj,"Y_Value")):
                X2Size=str(ObjectsTools.turnPropertyToExpression(obj,"Y_Value"))+UnitTools.DefaultUnits().getDefaultLengthUnit()
            else:
                X2Size=str(ObjectsTools.turnPropertyToExpression(obj,"Y_Value"))
            if isNumber(ObjectsTools.turnPropertyToExpression(obj,"Z_Value")):
                X3Size=str(ObjectsTools.turnPropertyToExpression(obj,"Z_Value"))+UnitTools.DefaultUnits().getDefaultLengthUnit()
            else:
                X3Size=str(ObjectsTools.turnPropertyToExpression(obj,"Z_Value"))
        elif curCoordinateSys==CoordinateSystemTools.CoordinateType.Polar:
            isX1=obj.R
            isX2=obj.Theta
            isX3=obj.Z
            # 由于老工程体不存在这些属性，放在异常处理处 @lzg
            try:
                ismin_1 = obj.min_1
                ismid_1 = obj.mid_1
                ismax_1 = obj.max_1
                ismin_2 = obj.min_2
                ismid_2 = obj.mid_2
                ismax_2 = obj.max_2
                ismin_3 = obj.min_3
                ismid_3 = obj.mid_3
                ismax_3 = obj.max_3
            except:
                pass
            if isNumber(ObjectsTools.turnPropertyToExpression(obj,"R_Value")):
                X1Size=str(ObjectsTools.turnPropertyToExpression(obj,"R_Value"))+UnitTools.DefaultUnits().getDefaultLengthUnit()
            else:
                X1Size=str(ObjectsTools.turnPropertyToExpression(obj,"R_Value"))
            if isNumber(ObjectsTools.turnPropertyToExpression(obj,"Theta_Value")):
                X2Size=str(ObjectsTools.turnPropertyToExpression(obj,"Theta_Value"))+UnitTools.DefaultUnits().getDefaultAngleUnit()
            else:
                X2Size=str(ObjectsTools.turnPropertyToExpression(obj,"Theta_Value"))
            if isNumber(ObjectsTools.turnPropertyToExpression(obj,"Z_Value")):
                X3Size=str(ObjectsTools.turnPropertyToExpression(obj,"Z_Value"))+UnitTools.DefaultUnits().getDefaultLengthUnit()
            else:
                X3Size=str(ObjectsTools.turnPropertyToExpression(obj,"Z_Value"))
        else:
            isX1=obj.Z
            isX2=obj.R
            isX3=obj.Theta
            # 由于老工程体不存在这些属性，放在异常处理处 @lzg
            try:
                ismin_1 = obj.min_3
                ismid_1 = obj.mid_3
                ismax_1 = obj.max_3
                ismin_2 = obj.min_1
                ismid_2 = obj.mid_1
                ismax_2 = obj.max_1
                ismin_3 = obj.min_2
                ismid_3 = obj.mid_2
                ismax_3 = obj.max_2
            except:
                pass
            if isNumber(ObjectsTools.turnPropertyToExpression(obj,"Z_Value")):
                X1Size=str(ObjectsTools.turnPropertyToExpression(obj,"Z_Value"))+UnitTools.DefaultUnits().getDefaultLengthUnit()
            else:
                X1Size=str(ObjectsTools.turnPropertyToExpression(obj,"Z_Value"))

            if isNumber(ObjectsTools.turnPropertyToExpression(obj,"R_Value")):
                X2Size=str(ObjectsTools.turnPropertyToExpression(obj,"R_Value"))+UnitTools.DefaultUnits().getDefaultLengthUnit()
            else:
                X2Size=str(ObjectsTools.turnPropertyToExpression(obj,"R_Value"))

            # sayz(isNumber(ObjectsTools.turnPropertyToExpression(obj,"Theta_Value")))
            if isNumber(ObjectsTools.turnPropertyToExpression(obj,"Theta_Value")):
                X3Size=str(ObjectsTools.turnPropertyToExpression(obj,"Theta_Value"))+UnitTools.DefaultUnits().getDefaultAngleUnit()
            else:
                X3Size=str(ObjectsTools.turnPropertyToExpression(obj,"Theta_Value"))
    else:
        FreeCAD.Console.PrintError(objectLabel+" cann't be found.\n")
    results=[isX1,isX2,isX3,X1Size,X2Size,X3Size,
            ismin_1, ismid_1, ismax_1,
            ismin_2, ismid_2, ismax_2,
            ismin_3, ismid_3, ismax_3]
    return results

# 获取体模型的自定义属性
def __getAttributeValue(obj):

    """
    obj:     物体对象
    return:  [NotDefine],
             或[Conductor]
             或[Vacuo]
             或[Custom,
             Boolean(ConductivitySIGMA),
              Float(ConductivitySIGMAValue),
              String(RelativeDielectricConstant),
              Float(SetEPS),
              Float(SetEPS2)
              Float(SetEPS3)]
    """
    attribute = obj.Attribute
    ConductivitySIGMA = str(obj.ConductivitySIGMA)
    ConductivitySIGMAValue = str(obj.ConductivitySIGMAValue)
    RelativeDielectricConstant = str(obj.RelativeDielectricConstant)
    SetEPS = str(obj.SetEPS)
    SetEPS2 = str(obj.SetEPS2)
    SetEPS3 = str(obj.SetEPS3)
    try:
        CS_SetEPS = str(obj.CS_SetEPS)
        CS_SetEPS2 = str(obj.CS_SetEPS2)
        CS_SetEPS3 = str(obj.CS_SetEPS3)
    except:
        pass
    if attribute == "Custom":
        return [attribute, ConductivitySIGMA, ConductivitySIGMAValue, RelativeDielectricConstant, SetEPS, SetEPS2, SetEPS3,\
                CS_SetEPS,CS_SetEPS2,CS_SetEPS3]
    else:
        return [attribute]

# Point
def __getPointInfo(obj,flag):
    """
    obj:     物体对象
    return:
            [label
             [str(x1),str(x2),str(x3)]
             Boolean(isX1),
             Boolean(isX2),
             Boolean(isX3),
             String(X1Size),
             String(X2Size),
             String(X3Size)]
    """

    if flag:
        label = obj.Label.split('_', 1)[1]
    else:
        label = obj.Label

    pointXYZ = __getUnitPoint(obj, ObjectsTools.turnPropertyToExpression(obj,"Point"))
    grideResults = __getMarkCommands(obj)
    infoList = [label,pointXYZ,grideResults[0],grideResults[1],grideResults[2], grideResults[3], grideResults[4], grideResults[5],
                grideResults[6], grideResults[7], grideResults[8],
                grideResults[9], grideResults[10], grideResults[11],
                grideResults[12], grideResults[13], grideResults[14]]

    return infoList


# Line or Area
def __getLineOrAreaInfo(obj,type,flag):
    """
    obj:     物体对象
    return:
            [label
             Type：线类型( CONFORMAL)；面类型( CONFORMAL \ RECTANGULAR)
             [str(x1),str(x2),str(x3)]:起点坐标列表
             [str(x1),str(x2),str(x3)]:终点坐标列表
             Boolean(isX1),
             Boolean(isX2),
             Boolean(isX3),
             String(X1Size),
             String(X2Size),
             String(X3Size)]
    """

    if flag:
        label = obj.Label.split('_', 1)[1]
    else:
        label = obj.Label

    pointXYZ1 = __getUnitPoint(obj, ObjectsTools.turnPropertyToExpression(obj,"Point1"))
    pointXYZ2 = __getUnitPoint(obj, ObjectsTools.turnPropertyToExpression(obj,"Point2"))
    grideResults = __getMarkCommands(obj)
    infoList = [label,type, pointXYZ1, pointXYZ2, grideResults[0], grideResults[1], grideResults[2], grideResults[3],
                     grideResults[4], grideResults[5],
                     grideResults[6], grideResults[7], grideResults[8],
                     grideResults[9], grideResults[10], grideResults[11],
                     grideResults[12], grideResults[13], grideResults[14]]

    return infoList

# Line_Oblique
def __getObliqueLineInfo(obj,flag):
    """
        obj:     物体对象
        return:
                [label: 斜线
                 [str(x1),str(x2),str(x3)]:底点坐标列表
                 [str(x1),str(x2),str(x3)]:顶点坐标列表
                 BottomRadius: 底半径
                 Boolean(isX1),
                 Boolean(isX2),
                 Boolean(isX3),
                 String(X1Size),
                 String(X2Size),
                 String(X3Size)]
        """

    if flag:
        label = obj.Label.split('_', 1)[1]
    else:
        label = obj.Label

    pointXYZ1 = __getUnitPoint(obj, ObjectsTools.turnPropertyToExpression(obj,"Point1"))
    pointXYZ2 = __getUnitPoint(obj, ObjectsTools.turnPropertyToExpression(obj,"Point2"))
    # baseradius = str(obj.BottomRadius).split(' ')[0]+str(obj.BottomRadius).split(' ')[1]
    grideResults = __getMarkCommands(obj)
    infoList = [label,"OBLIQUE",pointXYZ1, pointXYZ2, grideResults[0], grideResults[1], grideResults[2],
                             grideResults[3],grideResults[4], grideResults[5],
                             grideResults[6], grideResults[7], grideResults[8],
                             grideResults[9], grideResults[10], grideResults[11],
                             grideResults[12], grideResults[13], grideResults[14]]
    # infoList = [label, pointXYZ1, pointXYZ2, baseradius]

    return infoList

# PolygonalArea多边形面
def __getPolygonalAreaInfo(obj,flag):
    """
    obj:     物体对象
    return:
            [label:多边形面的名称
             Type：面类型
             [[str(x1),str(x2),str(x3)],[str(x1),str(x2),str(x3)],……]:点坐标列表
             Boolean(isX1),
             Boolean(isX2),
             Boolean(isX3),
             String(X1Size),
             String(X2Size),
             String(X3Size)]
    """
    if flag:
        label = obj.Label.split('_', 1)[1]
    else:
        label = obj.Label
    pointList = []
    for i in range(obj.NumbersOfPoints):
        pointStr = "Point" + str(i + 1)
        if (hasattr(obj, pointStr)):
            pointList.append( __getUnitPoint(obj, ObjectsTools.turnPropertyToExpression(obj,pointStr)))
    grideResults = __getMarkCommands(obj)
    infoList = [label,pointList, grideResults[0], grideResults[1], grideResults[2], grideResults[3],
                     grideResults[4], grideResults[5],
                     grideResults[6], grideResults[7], grideResults[8],
                     grideResults[9], grideResults[10], grideResults[11],
                     grideResults[12], grideResults[13], grideResults[14]]

    return infoList

# ConformalVolume投影体
def __getConformalVolumeInfo(obj,flag):
    """
        obj:     物体对象
        return:
                [label: 投影体名称
                 [str(x1),str(x2),str(x3)]:近点坐标列表
                 [str(x1),str(x2),str(x3)]:远点坐标列表
                 attributeResults：[]属性列表
                 Boolean(isX1),
                 Boolean(isX2),
                 Boolean(isX3),
                 String(X1Size),
                 String(X2Size),
                 String(X3Size)]
        """
    # FreeCAD.Console.PrintError('\n进入获取正投影体具体命令的函数\n')
    if flag:
        label = obj.Label.split('_', 1)[1]
    else:
        label = obj.Label
    pointXYZ1 = __getUnitPoint(obj,ObjectsTools.turnPropertyToExpression(obj,"Point1"))
    pointXYZ2 = __getUnitPoint(obj,ObjectsTools.turnPropertyToExpression(obj,"Point2"))
    grideResults = __getMarkCommands(obj)
    attributeResults = __getAttributeValue(obj)
    infoList = [label, pointXYZ1, pointXYZ2, attributeResults,grideResults[0], grideResults[1], grideResults[2],
                             grideResults[3],grideResults[4], grideResults[5],
                             grideResults[6], grideResults[7], grideResults[8],
                             grideResults[9], grideResults[10], grideResults[11],
                             grideResults[12], grideResults[13], grideResults[14]]

    return infoList

# SpecialConeVolume圆锥或圆台
def __getSpecialConeVolumeInfo(obj,flag):
    """
        obj:     物体对象
        return:
                [label: 圆锥或圆台名称
                 [str(x1),str(x2),str(x3)]:底点坐标列表
                 [str(x1),str(x2),str(x3)]:顶点坐标列表
                 baseradius: 底半径
                 topradius: 顶半径
                 attributeResults：[]属性列表
                 Boolean(isX1),
                 Boolean(isX2),
                 Boolean(isX3),
                 String(X1Size),
                 String(X2Size),
                 String(X3Size)]
        """
    if flag:
        label = obj.Label.split('_', 1)[1]
    else:
        label = obj.Label
    # pointXYZ1 = __getUnitPoint(obj, obj.PointBottom)
    # pointXYZ2 = __getUnitPoint(obj, obj.PointTop)
    pointXYZ1 = __getUnitPoint(obj, ObjectsTools.turnPropertyToExpression(obj,"PointBottom"))
    pointXYZ2 = __getUnitPoint(obj, ObjectsTools.turnPropertyToExpression(obj,"PointTop"))
    baseradius=ObjectsTools.turnPropertyToExpression(obj,"RadiusBottom")
    topradius=ObjectsTools.turnPropertyToExpression(obj,"RadiusTop")
    # baseradius = str(obj.RadiusBottom).split(' ')[0]+str(obj.RadiusBottom).split(' ')[1]
    # topradius = str(obj.RadiusTop).split(' ')[0]+str(obj.RadiusTop).split(' ')[1]
    grideResults = __getMarkCommands(obj)
    attributeResults = __getAttributeValue(obj)
    infoList = [label, pointXYZ1, pointXYZ2, baseradius, topradius, attributeResults,grideResults[0], grideResults[1], grideResults[2],
                             grideResults[3],grideResults[4], grideResults[5],
                             grideResults[6], grideResults[7], grideResults[8],
                             grideResults[9], grideResults[10], grideResults[11],
                             grideResults[12], grideResults[13], grideResults[14]]

    return infoList

# AnnularVolume环面体
def __getAnnularVolumeInfo(obj,flag):
    """
        obj:     物体对象
        return:
                [label: 环形体名称
                 [str(x1),str(x2),str(x3)]:空间点坐标列表
                 [str(x1),str(x2),str(x3)]:空间点坐标列表
                 radius_inner:环面的内半径
                 radius_outer:环面的外半径
                 attributeResults：[]属性列表
                 Boolean(isX1),
                 Boolean(isX2),
                 Boolean(isX3),
                 String(X1Size),
                 String(X2Size),
                 String(X3Size)]
        """
    if flag:
        label = obj.Label.split('_', 1)[1]
    else:
        label = obj.Label

    # pointXYZ1 = __getUnitPoint(obj, obj.Point_1)
    # pointXYZ2 = __getUnitPoint(obj, obj.Point_2)
    # radius_inner = str(obj.RadiusInside).split(' ')[0] + str(obj.RadiusInside).split(' ')[1]
    # radius_outer = str(obj.RadiusOutside).split(' ')[0] + str(obj.RadiusOutside).split(' ')[1]
    pointXYZ1 = __getUnitPoint(obj,ObjectsTools.turnPropertyToExpression(obj,"Point_1"))
    pointXYZ2 = __getUnitPoint(obj,ObjectsTools.turnPropertyToExpression(obj,"Point_2"))
    radius_inner=ObjectsTools.turnPropertyToExpression(obj,"RadiusInside")
    radius_outer=ObjectsTools.turnPropertyToExpression(obj,"RadiusOutside")
    grideResults = __getMarkCommands(obj)
    attributeResults = __getAttributeValue(obj)
    infoList = [label, pointXYZ1, pointXYZ2, radius_inner, radius_outer, attributeResults,grideResults[0], grideResults[1], grideResults[2],
                             grideResults[3],grideResults[4], grideResults[5],
                             grideResults[6], grideResults[7], grideResults[8],
                             grideResults[9], grideResults[10], grideResults[11],
                             grideResults[12], grideResults[13], grideResults[14]]

    return infoList

# AnnularSectionVolume部分环面体
def __getAnnularSectionVolumeInfo(obj,flag):
    """
        obj:     物体对象
        return:
                [label: 环形体名称
                 [str(x1),str(x2),str(x3)]:空间点坐标列表
                 [str(x1),str(x2),str(x3)]:空间点坐标列表
                 [str(x1),str(x2),str(x3)]:定环面中弧形段的起点
                 [str(x1),str(x2),str(x3)]:定环面中弧形段的终点
                 radius_inner:环面的内半径
                 radius_outer:环面的外半径
                 attributeResults：[]属性列表
                 Boolean(isX1),
                 Boolean(isX2),
                 Boolean(isX3),
                 String(X1Size),
                 String(X2Size),
                 String(X3Size)]
        """
    if flag:
        label = obj.Label.split('_', 1)[1]
    else:
        label = obj.Label
    pointXYZ1 = __getUnitPoint(obj, ObjectsTools.turnPropertyToExpression(obj,"Point1"))
    pointXYZ2 = __getUnitPoint(obj, ObjectsTools.turnPropertyToExpression(obj,"Point2"))
    pointXYZ3 = __getUnitPoint(obj, ObjectsTools.turnPropertyToExpression(obj,"Point3"))
    pointXYZ4 = __getUnitPoint(obj, ObjectsTools.turnPropertyToExpression(obj,"Point4"))
    # radius_inner = str(obj.InnerRadius).split(' ')[0] + str(obj.InnerRadius).split(' ')[1]
    # radius_outer = str(obj.OuterRadius).split(' ')[0] + str(obj.OuterRadius).split(' ')[1]
    radius_inner=ObjectsTools.turnPropertyToExpression(obj,"InnerRadius")
    radius_outer=ObjectsTools.turnPropertyToExpression(obj,"OuterRadius")
    grideResults = __getMarkCommands(obj)
    attributeResults = __getAttributeValue(obj)
    infoList = [label, pointXYZ1, pointXYZ2, radius_inner, radius_outer, pointXYZ3, pointXYZ4, attributeResults,grideResults[0], grideResults[1], grideResults[2],
                             grideResults[3],grideResults[4], grideResults[5],
                             grideResults[6], grideResults[7], grideResults[8],
                             grideResults[9], grideResults[10], grideResults[11],
                             grideResults[12], grideResults[13], grideResults[14]]

    return infoList

# CylinderVolume圆柱体
def __getCylinderVolumeInfo(obj,flag):
    """
        obj:     物体对象
        return:
                [label: 圆柱体名称
                 [str(x1),str(x2),str(x3)]:圆柱体轴线端点坐标列表
                 [str(x1),str(x2),str(x3)]:圆柱体轴线端点坐标列表
                 radius:圆柱体的半径
                 attributeResults：[]属性列表
                 Boolean(isX1),
                 Boolean(isX2),
                 Boolean(isX3),
                 String(X1Size),
                 String(X2Size),
                 String(X3Size)]
        """
    if flag:
        label = obj.Label.split('_', 1)[1]
    else:
        label = obj.Label
    pointXYZ1 = __getUnitPoint(obj, ObjectsTools.turnPropertyToExpression(obj,"Point_1"))
    pointXYZ2 = __getUnitPoint(obj, ObjectsTools.turnPropertyToExpression(obj,"Point_2"))
    # radius = str(obj.Radius).split(' ')[0] + str(obj.Radius).split(' ')[1]
    radius=ObjectsTools.turnPropertyToExpression(obj,"Radius")
    grideResults = __getMarkCommands(obj)
    # FreeCAD.Console.PrintError('\n获取属性之前\n')
    attributeResults = __getAttributeValue(obj)
    # FreeCAD.Console.PrintError('\n获取属性之后\n')
    infoList = [label, pointXYZ1, pointXYZ2, radius, attributeResults, grideResults[0], grideResults[1], grideResults[2],
                             grideResults[3],grideResults[4], grideResults[5],
                             grideResults[6], grideResults[7], grideResults[8],
                             grideResults[9], grideResults[10], grideResults[11],
                             grideResults[12], grideResults[13], grideResults[14]]

    return infoList

# Revolution旋转体
def __getRevolutionVolumeInfo(obj,flag):
    """
    :param obj:物体对象 
    :param flag: 
    :return: 
    [label: 旋转体名称
                 [str(x1),str(x2),str(x3)]:axis_base_point端点坐标列表
                 [str(x1),str(x2),str(x3)]:axis_top_point端点坐标列表
                 area:旋转面
                 attributeResults：[]属性列表
                 Boolean(isX1),
                 Boolean(isX2),
                 Boolean(isX3),
                 String(X1Size),
                 String(X2Size),
                 String(X3Size)]
    """
    if flag==1:
        label = obj.Label.split('_',1)[1]
    else:
        label=obj.Label

    pointXYZ1 = __getUnitPoint(obj, ObjectsTools.turnPropertyToExpression(obj, "Point_Base"))
    pointXYZ2 = __getUnitPoint(obj, ObjectsTools.turnPropertyToExpression(obj, "Point_Top"))
    area = obj.Area.split("_",1)
    # Area = re.split("\[|,",area[1][0])
    grideResults = __getMarkCommands(obj)
    attributeResults = __getAttributeValue(obj)
    infoList = [label, pointXYZ1, pointXYZ2, area[1], attributeResults, grideResults[0], grideResults[1],
                grideResults[2],
                grideResults[3], grideResults[4], grideResults[5],
                grideResults[6], grideResults[7], grideResults[8],
                grideResults[9], grideResults[10], grideResults[11],
                grideResults[12], grideResults[13], grideResults[14]]

    return infoList


# Parallelepipedal平行六面体
def __getParallelepipedalVolumeInfo(obj,flag):
    """
        obj:     物体对象
        return:
                [label: 平行六面体名称
                 [str(x1),str(x2),str(x3)]:角点坐标列表
                 [str(x1),str(x2),str(x3)]:角点坐标列表
                 [str(x1),str(x2),str(x3)]:角点坐标列表
                 [str(x1),str(x2),str(x3)]:角点坐标列表
                 attributeResults：[]属性列表
                 Boolean(isX1),
                 Boolean(isX2),
                 Boolean(isX3),
                 String(X1Size),
                 String(X2Size),
                 String(X3Size)]
        """
    if flag:
        label = obj.Label.split('_', 1)[1]
    else:
        label = obj.Label
    pointXYZ1 = __getUnitPoint(obj, ObjectsTools.turnPropertyToExpression(obj,"Point_0"))
    pointXYZ2 = __getUnitPoint(obj, ObjectsTools.turnPropertyToExpression(obj,"Point_1"))
    pointXYZ3 = __getUnitPoint(obj, ObjectsTools.turnPropertyToExpression(obj,"Point_2"))
    pointXYZ4 = __getUnitPoint(obj, ObjectsTools.turnPropertyToExpression(obj,"Point_3"))
    grideResults = __getMarkCommands(obj)
    attributeResults = __getAttributeValue(obj)
    infoList = [label, pointXYZ1, pointXYZ2, pointXYZ3, pointXYZ4, attributeResults, grideResults[0], grideResults[1], grideResults[2],
                             grideResults[3],grideResults[4], grideResults[5],
                             grideResults[6], grideResults[7], grideResults[8],
                             grideResults[9], grideResults[10], grideResults[11],
                             grideResults[12], grideResults[13], grideResults[14]]

    return infoList


# Spherical球体
def __getSphericalVolumeInfo(obj,flag):
    """
        obj:     物体对象
        return:
                [label: 球体名称
                 [str(x1),str(x2),str(x3)]:球心点坐标列表
                 radius:球的半径
                 attributeResults：[]属性列表
                 Boolean(isX1),
                 Boolean(isX2),
                 Boolean(isX3),
                 String(X1Size),
                 String(X2Size),
                 String(X3Size)]
        """
    if flag:
        label = obj.Label.split('_', 1)[1]
    else:
        label = obj.Label
    pointXYZ = __getUnitPoint(obj, ObjectsTools.turnPropertyToExpression(obj,"CenterPoint"))
    # radius = str(obj.Radius).split(' ')[0] + str(obj.Radius).split(' ')[1]
    radius=ObjectsTools.turnPropertyToExpression(obj,"Radius")
    grideResults = __getMarkCommands(obj)
    attributeResults = __getAttributeValue(obj)
    infoList = [label, pointXYZ, radius, attributeResults, grideResults[0], grideResults[1], grideResults[2],
                             grideResults[3],grideResults[4], grideResults[5],
                             grideResults[6], grideResults[7], grideResults[8],
                             grideResults[9], grideResults[10], grideResults[11],
                             grideResults[12], grideResults[13], grideResults[14]]

    return infoList

# Pyramid棱锥体
def __getPyramidVolumeInfo(obj,flag):
    """
        obj:     物体对象
        return:
                [label: 棱锥体名称
                 [str(x1),str(x2),str(x3)]:角点坐标列表
                 [str(x1),str(x2),str(x3)]:角点坐标列表
                 [str(x1),str(x2),str(x3)]:角点坐标列表
                 [str(x1),str(x2),str(x3)]:角点坐标列表
                 [str(x1),str(x2),str(x3)]:棱锥体顶点坐标列表
                 attributeResults：[]属性列表
                 Boolean(isX1),
                 Boolean(isX2),
                 Boolean(isX3),
                 String(X1Size),
                 String(X2Size),
                 String(X3Size)]
        """
    if flag:
        label = obj.Label.split('_', 1)[1]
    else:
        label = obj.Label
    pointXYZ1 = __getUnitPoint(obj, ObjectsTools.turnPropertyToExpression(obj,"Point_1"))
    pointXYZ2 = __getUnitPoint(obj, ObjectsTools.turnPropertyToExpression(obj,"Point_2"))
    pointXYZ3 = __getUnitPoint(obj, ObjectsTools.turnPropertyToExpression(obj,"Point_3"))
    pointXYZ4 = __getUnitPoint(obj, ObjectsTools.turnPropertyToExpression(obj,"Point_4"))
    pointXYZ5 = __getUnitPoint(obj, ObjectsTools.turnPropertyToExpression(obj,"Point_5"))
    grideResults = __getMarkCommands(obj)
    attributeResults = __getAttributeValue(obj)
    infoList = [label, pointXYZ1, pointXYZ2, pointXYZ3, pointXYZ4, pointXYZ5, attributeResults, grideResults[0], grideResults[1], grideResults[2],
                             grideResults[3],grideResults[4], grideResults[5],
                             grideResults[6], grideResults[7], grideResults[8],
                             grideResults[9], grideResults[10], grideResults[11],
                             grideResults[12], grideResults[13], grideResults[14]]

    return infoList

# Toroidal_Section部分圆环体
def __getToroidalSectionVolumeInfo(obj,flag):
    """
        obj:     物体对象
        return:
                [label: 部分圆环体名称
                 [str(x1),str(x2),str(x3)]:圆环体中心点坐标列表
                 [str(x1),str(x2),str(x3)]:指定对称轴点坐标列表
                 [str(x1),str(x2),str(x3)]:圆弧段起点坐标列表
                 [str(x1),str(x2),str(x3)]:圆弧段终点坐标列表
                 majorRadius:环面的大半径
                 minorRadius:环面的小半径
                 attributeResults：[]属性列表
                 Boolean(isX1),
                 Boolean(isX2),
                 Boolean(isX3),
                 String(X1Size),
                 String(X2Size),
                 String(X3Size)]
        """
    if flag:
        label = obj.Label.split('_', 1)[1]
    else:
        label = obj.Label
    pointXYZ1 = __getUnitPoint(obj, ObjectsTools.turnPropertyToExpression(obj,"Point1"))
    pointXYZ2 = __getUnitPoint(obj, ObjectsTools.turnPropertyToExpression(obj,"Point2"))
    pointXYZ3 = __getUnitPoint(obj, ObjectsTools.turnPropertyToExpression(obj,"Point3"))
    pointXYZ4 = __getUnitPoint(obj, ObjectsTools.turnPropertyToExpression(obj,"Point4"))
    majorRadius=ObjectsTools.turnPropertyToExpression(obj,"MajorRadius")
    minorRadius=ObjectsTools.turnPropertyToExpression(obj,"MinorRadius")
    # majorRadius = str(obj.MajorRadius).split(' ')[0] + str(obj.MajorRadius).split(' ')[1]
    # minorRadius = str(obj.MinorRadius).split(' ')[0] + str(obj.MinorRadius).split(' ')[1]
    grideResults = __getMarkCommands(obj)
    attributeResults = __getAttributeValue(obj)
    infoList = [label, pointXYZ1, pointXYZ2, majorRadius, minorRadius, pointXYZ3, pointXYZ4, attributeResults, grideResults[0], grideResults[1], grideResults[2],
                             grideResults[3],grideResults[4], grideResults[5],
                             grideResults[6], grideResults[7], grideResults[8],
                             grideResults[9], grideResults[10], grideResults[11],
                             grideResults[12], grideResults[13], grideResults[14]]

    return infoList


# Wedge楔形体
def __getWedgeVolumeInfo(obj,flag):
    """
        obj:     物体对象
        return:
                [label: 楔形体名称
                 [str(x1),str(x2),str(x3)]:角点坐标列表
                 [str(x1),str(x2),str(x3)]:角点坐标列表
                 [str(x1),str(x2),str(x3)]:角点坐标列表
                 [str(x1),str(x2),str(x3)]:角点坐标列表
                 [str(x1),str(x2),str(x3)]:顶点坐标列表
                 [str(x1),str(x2),str(x3)]:顶点坐标列表
                 attributeResults：[]属性列表
                 Boolean(isX1),
                 Boolean(isX2),
                 Boolean(isX3),
                 String(X1Size),
                 String(X2Size),
                 String(X3Size)]
        """
    if flag:
        label = obj.Label.split('_', 1)[1]
    else:
        label = obj.Label
    pointXYZ1 = __getUnitPoint(obj, ObjectsTools.turnPropertyToExpression(obj,"Point_1"))
    pointXYZ2 = __getUnitPoint(obj, ObjectsTools.turnPropertyToExpression(obj,"Point_2"))
    pointXYZ3 = __getUnitPoint(obj, ObjectsTools.turnPropertyToExpression(obj,"Point_3"))
    pointXYZ4 = __getUnitPoint(obj, ObjectsTools.turnPropertyToExpression(obj,"Point_4"))
    pointXYZ5 = __getUnitPoint(obj, ObjectsTools.turnPropertyToExpression(obj,"Point_5"))
    pointXYZ6 = __getUnitPoint(obj, ObjectsTools.turnPropertyToExpression(obj,"Point_6"))
    grideResults = __getMarkCommands(obj)
    attributeResults = __getAttributeValue(obj)
    infoList = [label, pointXYZ1, pointXYZ2, pointXYZ3, pointXYZ4, pointXYZ5, pointXYZ6, attributeResults, grideResults[0], grideResults[1], grideResults[2],
                             grideResults[3],grideResults[4], grideResults[5],
                             grideResults[6], grideResults[7], grideResults[8],
                             grideResults[9], grideResults[10], grideResults[11],
                             grideResults[12], grideResults[13], grideResults[14]]

    return infoList

# Tetrahedron四面体
def __getTetrahedronVolumeInfo(obj,flag):
    """
        obj:     物体对象
        return:
                [label: 四面体名称
                 [str(x1),str(x2),str(x3)]:角点坐标列表
                 [str(x1),str(x2),str(x3)]:角点坐标列表
                 [str(x1),str(x2),str(x3)]:角点坐标列表
                 [str(x1),str(x2),str(x3)]:角点坐标列表
                 attributeResults：[]属性列表
                 Boolean(isX1),
                 Boolean(isX2),
                 Boolean(isX3),
                 String(X1Size),
                 String(X2Size),
                 String(X3Size)]
        """
    if flag:
        label = obj.Label.split('_', 1)[1]
    else:
        label = obj.Label
    pointXYZ1 = __getUnitPoint(obj, ObjectsTools.turnPropertyToExpression(obj,"Point_1"))
    pointXYZ2 = __getUnitPoint(obj, ObjectsTools.turnPropertyToExpression(obj,"Point_2"))
    pointXYZ3 = __getUnitPoint(obj, ObjectsTools.turnPropertyToExpression(obj,"Point_3"))
    pointXYZ4 = __getUnitPoint(obj, ObjectsTools.turnPropertyToExpression(obj,"Point_4"))
    grideResults = __getMarkCommands(obj)
    attributeResults = __getAttributeValue(obj)
    infoList = [label, pointXYZ1, pointXYZ2, pointXYZ3, pointXYZ4, attributeResults, grideResults[0], grideResults[1], grideResults[2],
                             grideResults[3],grideResults[4], grideResults[5],
                             grideResults[6], grideResults[7], grideResults[8],
                             grideResults[9], grideResults[10], grideResults[11],
                             grideResults[12], grideResults[13], grideResults[14]]

    return infoList

# Rhombus菱形体
def __getRhombusVolumeInfo(obj,flag):
    """
        obj:     物体对象
        return:
                [label: 菱形体名称
                 [str(x1),str(x2),str(x3)]:角点坐标列表
                 [str(x1),str(x2),str(x3)]:角点坐标列表
                 [str(x1),str(x2),str(x3)]:角点坐标列表
                 [str(x1),str(x2),str(x3)]:角点坐标列表
                 [str(x1),str(x2),str(x3)]:角点坐标列表
                 [str(x1),str(x2),str(x3)]:角点坐标列表
                 [str(x1),str(x2),str(x3)]:角点坐标列表
                 [str(x1),str(x2),str(x3)]:角点坐标列表
                 attributeResults：[]属性列表
                 Boolean(isX1),
                 Boolean(isX2),
                 Boolean(isX3),
                 String(X1Size),
                 String(X2Size),
                 String(X3Size)]
        """
    if flag:
        label = obj.Label.split('_', 1)[1]
    else:
        label = obj.Label
    pointXYZ1 = __getUnitPoint(obj, ObjectsTools.turnPropertyToExpression(obj,"Point_1"))
    pointXYZ2 = __getUnitPoint(obj, ObjectsTools.turnPropertyToExpression(obj,"Point_2"))
    pointXYZ3 = __getUnitPoint(obj, ObjectsTools.turnPropertyToExpression(obj,"Point_3"))
    pointXYZ4 = __getUnitPoint(obj, ObjectsTools.turnPropertyToExpression(obj,"Point_4"))
    pointXYZ5 = __getUnitPoint(obj, ObjectsTools.turnPropertyToExpression(obj,"Point_5"))
    pointXYZ6 = __getUnitPoint(obj, ObjectsTools.turnPropertyToExpression(obj,"Point_6"))
    pointXYZ7 = __getUnitPoint(obj, ObjectsTools.turnPropertyToExpression(obj,"Point_7"))
    pointXYZ8 = __getUnitPoint(obj, ObjectsTools.turnPropertyToExpression(obj,"Point_8"))
    grideResults = __getMarkCommands(obj)
    attributeResults = __getAttributeValue(obj)
    infoList = [label, pointXYZ1, pointXYZ2, pointXYZ3, pointXYZ4, pointXYZ5, pointXYZ6, pointXYZ7, pointXYZ8, attributeResults, grideResults[0], grideResults[1], grideResults[2],
                             grideResults[3],grideResults[4], grideResults[5],
                             grideResults[6], grideResults[7], grideResults[8],
                             grideResults[9], grideResults[10], grideResults[11],
                             grideResults[12], grideResults[13], grideResults[14]]

    return infoList


# Extruded挤出体
def __getExtrudedVolumeInfo(obj,flag):
    """
        obj:     物体对象
        return:
                [label: 挤出体名称
                 areaLabel: 面名称
                 lineLabel: 线名称
                 attributeResults：[]属性列表
                 Boolean(isX1),
                 Boolean(isX2),
                 Boolean(isX3),
                 String(X1Size),
                 String(X2Size),
                 String(X3Size)]
        """
    if flag:
        label = obj.Label.split('_', 1)[1]
    else:
        label = obj.Label
    try:

        # obj属性Area和Line没值时报错，返回error
        areaLabel = obj.Area[4:]
        lineLabel = obj.Line[4:]
        grideResults = __getMarkCommands(obj)
        attributeResults = __getAttributeValue(obj)
        infoList = [label, areaLabel, lineLabel,
                    attributeResults, grideResults[0], grideResults[1], grideResults[2],
                    grideResults[3], grideResults[4], grideResults[5],
                    grideResults[6], grideResults[7], grideResults[8],
                    grideResults[9], grideResults[10], grideResults[11],
                    grideResults[12], grideResults[13], grideResults[14]]
        return infoList
    except AssertionError as e:
        FreeCAD.Console.PrintMessage(obj.Label + "has no Line or Area")
        return "error"

# Helical螺旋体
def __getHelicalVolumeInfo(obj,flag):
    """
        obj:     物体对象
        return:
                [label: 螺旋体名称
                 basePoint[str(x1),str(x2),str(x3)]:基点坐标列表
                 topPoint[str(x1),str(x2),str(x3)]:顶点坐标列表
                 inner_radius:内半径
                 outer_radius:外半径
                 startPoint[str(x1),str(x2),str(x3)]:弧段起点点坐标列表
                 pitch: 螺旋节距
                 width:螺旋线径向宽度
                 attributeResults：[]属性列表
                 Boolean(isX1),
                 Boolean(isX2),
                 Boolean(isX3),
                 String(X1Size),
                 String(X2Size),
                 String(X3Size)]
        """
    if flag:
        label = obj.Label.split('_', 1)[1]
    else:
        label = obj.Label
    basePoint = __getUnitPoint(obj, ObjectsTools.turnPropertyToExpression(obj,"BasePoint"))
    topPoint = __getUnitPoint(obj, ObjectsTools.turnPropertyToExpression(obj,"TopPoint"))
    startPoint = __getUnitPoint(obj, ObjectsTools.turnPropertyToExpression(obj,"StartPoint"))
    inner_radius=ObjectsTools.turnPropertyToExpression(obj,"InnerRadius")
    outer_radius=ObjectsTools.turnPropertyToExpression(obj,"OuterRadius")
    pitch=ObjectsTools.turnPropertyToExpression(obj,"Pitch")
    width=ObjectsTools.turnPropertyToExpression(obj,"Width")
    # inner_radius = str(obj.InnerRadius).split(' ')[0] + str(obj.InnerRadius).split(' ')[1]
    # outer_radius = str(obj.OuterRadius).split(' ')[0] + str(obj.OuterRadius).split(' ')[1]
    # pitch = str(obj.Pitch).split(' ')[0] + str(obj.Pitch).split(' ')[1]
    # width = str(obj.Width).split(' ')[0] + str(obj.Width).split(' ')[1]
    grideResults = __getMarkCommands(obj)
    attributeResults = __getAttributeValue(obj)
    infoList = [label, basePoint, topPoint, inner_radius,outer_radius, startPoint, pitch, width, attributeResults, grideResults[0], grideResults[1], grideResults[2],
                             grideResults[3],grideResults[4], grideResults[5],
                             grideResults[6], grideResults[7], grideResults[8],
                             grideResults[9], grideResults[10], grideResults[11],
                             grideResults[12], grideResults[13], grideResults[14]]

    return infoList

#草图建模-拉伸
def __getDraftExtrudeVolumeInfo(obj,flag):
    if flag:
        label = obj.Label.split('_', 1)[1]
    else:
        label = obj.Label
    # 不同坐标系下，拉伸模型的类型不定
    # 直角坐标系下：
    #   conformal面或者Rectangular面时，拉伸是conformal体
    # 极坐标系和球坐标系：
    #   conformal 矩形面拉伸是Parrallelepipedal体
    #极坐标和柱坐标系下：
    #   conformal 圆形面拉伸是柱体
    #   conformal 环形面拉伸是环形体
    curCoordinateSys=obj.Document.CoordinateSystem
    baseAreas=FreeCAD.ActiveDocument.getObjectsByLabel(obj.Area)
    if len(baseAreas)!=0:
        baseArea=baseAreas[0]
        # 共有的属性
        grideResults = __getMarkCommands(obj)
        attributeResults = __getAttributeValue(obj)

        if curCoordinateSys==CoordinateSystemTools.CoordinateType.Rectangular:
            if baseArea.Type==ObjectsTools.ObjectType.Area_Conformal or baseArea.Type==ObjectsTools.ObjectType.Area_Rectangular:
                boundBox=obj.Shape.BoundBox
                Point1=[boundBox.XMin,boundBox.YMin,boundBox.ZMin]
                Point2=[boundBox.XMax,boundBox.YMax,boundBox.ZMax]
                pointXYZ1 = __getUnitPoint(obj,Point1)
                pointXYZ2 = __getUnitPoint(obj,Point2)
                grideResults = __getMarkCommands(obj)
                attributeResults = __getAttributeValue(obj)

                infoList = [ObjectsTools.ObjectType.Vol_Conformal,label, pointXYZ1, pointXYZ2, attributeResults,grideResults[0], grideResults[1], grideResults[2],
                                        grideResults[3],grideResults[4], grideResults[5],
                                        grideResults[6],grideResults[7], grideResults[8],
                                        grideResults[9],grideResults[10], grideResults[11],
                                        grideResults[12],grideResults[13], grideResults[14]]
        else:
            #平行四面体
            if baseArea.Type==ObjectsTools.ObjectType.Area_Conformal:
                #矩形
                if baseArea.Normal=="theta":
                    boundBox=obj.Shape.BoundBox
                    PointMin=[boundBox.XMin,boundBox.YMin,boundBox.ZMin]
                    PointMax=[boundBox.XMax,boundBox.YMax,boundBox.ZMax]
                    
                    
                    point0R=[PointMax[0],PointMin[1],PointMin[2]]
                    point1R=[PointMax[0],PointMax[1],PointMin[2]]
                    point2R=[PointMax[0],PointMin[1],PointMax[2]]
                    point3R=[PointMin[0],PointMin[1],PointMin[2]]
                    #坐标转化
                    [point0P,point1P,point2P,point3P]=CoordinateSystemTools.recToOtherNotPoints(curCoordinateSys,[point0R,point1R,point2R,point3R])

                        
                    pointXYZ1 = __getUnitPoint(obj, point0P)
                    pointXYZ2 = __getUnitPoint(obj, point1P)
                    pointXYZ3 = __getUnitPoint(obj, point2P)
                    pointXYZ4 = __getUnitPoint(obj, point3P)
                    # grideResults = __getMarkCommands(obj)
                    # attributeResults = __getAttributeValue(obj)
                    infoList = [ObjectsTools.ObjectType.Vol_Parallelepipedal,label, pointXYZ1, pointXYZ2, pointXYZ3, pointXYZ4, attributeResults, grideResults[0], grideResults[1], grideResults[2],
                                            grideResults[3],grideResults[4], grideResults[5],
                                            grideResults[6],grideResults[7], grideResults[8],
                                        grideResults[9],grideResults[10], grideResults[11],
                                        grideResults[12],grideResults[13], grideResults[14]]
                # 弧面形
                elif baseArea.Normal=="r":
                    pass
                # 圆面形
                else:
                    baseAreaP1=baseArea.Point1
                    baseAreaP2=baseArea.Point2
                    # 这里的先保证形成的面是一个圆周
                    if (baseAreaP2.y-baseAreaP1.y)%360.0==0.0:
                        #这里还得判断一下两个点的r是不是有一个为0，如果有一个为0的话，就是柱体，否则没有0就是环形体
                        if baseAreaP1.x==0.0 or baseAreaP2.x==0.0:
                            # 拉伸成圆柱体,圆柱体法向为（0.0,0.0,1.0）
                            cylinderPoint_1=[0.0,0.0,baseArea.Point1.z]
                            cylinderPoint_2=[0.0,360.0,baseArea.Point1.z+obj.Length.Value]
                            if baseAreaP1.x!=0.0:
                                cylinderRadius=baseAreaP1.x
                            elif baseAreaP2.x!=0.0:
                                cylinderRadius=baseAreaP2.x
                            else:
                                return
                            # 圆柱体的内容
                            pointXYZ1 = __getUnitPoint(obj, cylinderPoint_1)
                            pointXYZ2 = __getUnitPoint(obj, cylinderPoint_2)
                            # radius = str(obj.Radius).split(' ')[0] + str(obj.Radius).split(' ')[1]
                            radius=str(cylinderRadius)+"m"
                            pass
                            infoList = [ObjectsTools.ObjectType.Vol_Cylinder,label, pointXYZ1, pointXYZ2, radius, attributeResults, grideResults[0], grideResults[1], grideResults[2],
                                        grideResults[3],grideResults[4], grideResults[5],
                                        grideResults[6],grideResults[7], grideResults[8],
                                        grideResults[9],grideResults[10], grideResults[11],
                                        grideResults[12],grideResults[13], grideResults[14]]
                        else:
                            pass
                            # 拉伸成环形体
                            annularPoint_1=[0.0,0.0,baseArea.Point1.z]
                            annularPoint_2=[0.0,360.0,baseArea.Point1.z+obj.Length.Value]
                            if baseAreaP1.x<baseAreaP2.x:
                                annular_inner=baseAreaP1.x
                                annular_outer=baseAreaP2.x
                            elif baseAreaP1.x<baseAreaP2.x:
                                annular_inner=baseAreaP2.x
                                annular_outer=baseAreaP1.x
                            else:
                                return
                            #环形体
                            pointXYZ1 = __getUnitPoint(obj,annularPoint_1)
                            pointXYZ2 = __getUnitPoint(obj,annularPoint_2)
                            radius_inner=str(annular_inner)+"m"
                            radius_outer=str(annular_outer)+"m"
                            infoList = [ObjectsTools.ObjectType.Vol_Annular,label, pointXYZ1, pointXYZ2, radius_inner, radius_outer, attributeResults,grideResults[0], grideResults[1], grideResults[2],
                                                    grideResults[3],grideResults[4], grideResults[5],
                                                    grideResults[6],grideResults[7], grideResults[8],
                                        grideResults[9],grideResults[10], grideResults[11],
                                        grideResults[12],grideResults[13], grideResults[14]]
                        pass

    FreeCAD.Console.PrintMessage("infoList: "+str(infoList)+"\n")
    return infoList
# 函数体
def __getFunctionVolumeInfo(obj,flag):
    """
    obj:     物体对象
    return:
            [label: 函数体名称
                Point_1[str(x1),str(x2),str(x3)]:边界点1
                Point_2[str(x1),str(x2),str(x3)]:边界点2
                functionStr:函数表达式
                attributeResults：[]属性列表
                Boolean(isX1),
                Boolean(isX2),
                Boolean(isX3),
                String(X1Size),
                String(X2Size),
                String(X3Size)]
    """
    if flag:
        label = obj.Label.split('_', 1)[1]
    else:
        label = obj.Label
    Point_1=__getUnitPoint(obj,ObjectsTools.turnPropertyToExpression(obj,"Point_1"))
    Point_2=__getUnitPoint(obj,ObjectsTools.turnPropertyToExpression(obj,"Point_2"))
    functionStr=str(obj.Expression)
    grideResults = __getMarkCommands(obj)
    attributeResults = __getAttributeValue(obj)
    infoList = [label,Point_1,Point_2,functionStr,attributeResults,grideResults[0],grideResults[1],grideResults[2],grideResults[3],
                grideResults[4],grideResults[5],
                grideResults[6], grideResults[7], grideResults[8],
                grideResults[9], grideResults[10], grideResults[11],
                grideResults[12], grideResults[13], grideResults[14]]
    return infoList


def __getArrayObjectInfo(system, obj):
    """
        obj: 物体对象
        return:
        [label: 循环体名称
        baseObj: 基础物体对象名称
        arrayType: 循环类型
        centerAxis: polar 类型的旋转轴
        orthoFace: ortho 类型的矩形面
        numX: X/R 方向循环个数
        numY: Y/Theta 方向循环个数
        numZ: Z 方向循环个数
        num: linear 类型循环个数
        numPolar: polar 类型循环个数
        stepX: X/R 方向步长
        stepY: Y/Theta 方向步长
        stepZ: Z 方向步长]
    """
    label = obj.Label
    baseObj = obj.Base.Label
    arrayType = obj.ArrayType
    num = ObjectsTools.turnPropertyToExpression(obj,"Number")
    numPolar = ObjectsTools.turnPropertyToExpression(obj,"NumberPolar")
    stepZ =ObjectsTools.turnPropertyToExpression(obj,"IntervalZ")
    numZ = ObjectsTools.turnPropertyToExpression(obj,"NumberZ")
    label = obj.Label.split('_', 1)[1]
    if system == CoordinateSystemTools.CoordinateType.Rectangular:
        centerAxis = obj.CenterAxis
        orthoFace = obj.OrthoFace
        numX = ObjectsTools.turnPropertyToExpression(obj,"NumberX")
        numY = ObjectsTools.turnPropertyToExpression(obj,"NumberY")
        stepX = ObjectsTools.turnPropertyToExpression(obj,"IntervalX")
        stepY = ObjectsTools.turnPropertyToExpression(obj,"IntervalY")
        infoList = [label, baseObj, arrayType, centerAxis, orthoFace, numX, numY, numZ, num, numPolar, stepX, stepY, stepZ]
    else:
        numR = ObjectsTools.turnPropertyToExpression(obj,"NumberR")
        stepR = ObjectsTools.turnPropertyToExpression(obj,"IntervalR")
        stepTheta = ObjectsTools.turnPropertyToExpression(obj,"IntervalTheta")
        infoList = [label, baseObj, arrayType, numR, numZ, num, numPolar, stepR, stepTheta, stepZ]
    return infoList


def __getParamArrayVolumeInfo(obj,flag):
    """
    obj:     物体对象
    return:
            [label: 参数阵列体名称
            baseObjType 基础对象类型:注意与CHIPICCommand.py中的Volume.Shape对应
            start: 开始i
            end: 结束i
            baseObjData 基础对象数据[（例如：环形体） [point1.x,point1.y,point1.z],[point2.x,point2.y,point2.z],radiusInner,radiusOutter]
            attributeResults：[]属性列表
            Boolean(isX1),
            Boolean(isX2),
            Boolean(isX3),
            String(X1Size),
            String(X2Size),
            String(X3Size)]
    """
    label=obj.Label.split('_', 1)[1]
    unicodeType=obj.BaseObjType
    if unicodeType==u"点":
        baseObjType="ANNULAR"
        pass
    elif unicodeType==u"正投影线":
        baseObjType="ANNULAR"
        pass
    elif unicodeType==u"斜线":
        baseObjType="ANNULAR"
        pass
    elif unicodeType==u"正投影面":
        baseObjType="ANNULAR"
        pass
    elif unicodeType==u"矩形面":
        baseObjType="ANNULAR"
        pass
    elif unicodeType==u"正投影体":
        baseObjType="CONFORMAL"
        pass
    elif unicodeType==u"环形体":
        baseObjType="ANNULAR"
        pass
    elif unicodeType==u"圆柱体":
        baseObjType="CYLINDRICAL"
        pass
    elif unicodeType==u"圆台体":
        baseObjType="CONE"
        pass
    elif unicodeType==u"平行六面体":
        baseObjType="PARALLELEPIPEDAL"
        pass
    elif unicodeType==u"正投影面":
        baseObjType="ANNULAR"
        pass
    elif unicodeType==u"球形体":
        baseObjType="SPHERICAL"
        pass
    elif unicodeType==u"楔形体":
        baseObjType="WEDGE"
        pass
    elif unicodeType==u"金字塔体":
        baseObjType="PYRAMID"
        pass
    elif unicodeType==u"菱形体":
        baseObjType="RHOMBUS"
        pass
    elif unicodeType==u"四面体":
        baseObjType="TETRAHEDRON"
        pass
    elif unicodeType==u"半圆环体":
        baseObjType="TOROIDAL_SECTION"
        pass
    elif unicodeType==u"环形区域体":
        baseObjType="ANNULAR_SECTION"
        pass
    elif unicodeType==u"挤出体":
        baseObjType="EXTRUDED"
        pass
    elif unicodeType==u"螺旋体":
        baseObjType="HELICAL"
        pass
    elif unicodeType==u"函数体":
        baseObjType="FUNCTIONAL"
        pass
  
    # start=obj.IFrom
    # end=obj.ITo
    start=ObjectsTools.turnPropertyToExpression(obj,"IFrom")
    end=ObjectsTools.turnPropertyToExpression(obj,"ITo")

    baseObjData=obj.BaseObjData
    grideResults = __getMarkCommands(obj)
    attributeResults = __getAttributeValue(obj)
    infoList=[label,baseObjType,start,end,baseObjData,attributeResults,grideResults[0], grideResults[1], grideResults[2],
                             grideResults[3],grideResults[4], grideResults[5]]
    return infoList

def sayz(msg):
    FreeCAD.Console.PrintMessage(msg)
    FreeCAD.Console.PrintMessage("\n")