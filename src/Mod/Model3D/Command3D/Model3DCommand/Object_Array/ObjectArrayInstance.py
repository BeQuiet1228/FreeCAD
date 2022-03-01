# -*- coding: utf8 -*-
import math
import FreeCADGui
import FreeCAD
import Part
import ArrayDraft
from Model3D.Tools import Tools3D, ObjectTools, ExpressionTools3D, InitDoc3D


class ObjectArray:
    def __init__(self, obj):
        obj.Proxy = self

    def onChanged(self, fp, prop):
        pass

    def execute(self, fp):

        try:
            if fp.BaseType:

                baseObj = ObjectTools.getObjByLabel(fp.BaseType)
                if hasattr(baseObj, "Type"):
                    fp.BaseObjType = baseObj.Type
                # 获取baseObj的上级分组，若baseObj第一次参与阵列，则此时baseObj还未移动到阵列体下，所以有却仅有一个上级，group即自身Type所决定的分组
                group = baseObj.InList
                # 如果baseObj上级数量不为1，表明其同属多个分组之下，报错并退出建模
                if len(group) > 1:
                    return

                # 建模
                fp.Base = baseObj
                if fp.ArrayType == "linear":
                    sh = self.linearArray(fp.Base, fp.BaseObjType,
                                          fp.intervalX.Value, fp.intervalY.Value, fp.intervalZ.Value,
                                          fp.linerNumber)
                elif fp.ArrayType == "ortho":
                    sh = self.rectArray(fp.Base, fp.orthoFace,
                                        fp.interval1.Value, fp.interval2.Value,
                                        fp.number1, fp.number2)
                elif fp.ArrayType == "polar":
                    sh = self.polarArray(fp.Base, fp.centerAxis, fp.numberPolar)
                else:
                    Tools3D.sayz("Array Type Error!")
                    return
                fp.Shape = sh

                # baseObj处理部分
                baseObj.ViewObject.hide()
                if hasattr(baseObj, "Type"):
                    # 有属性"Type"，说明baseObj第一次参与阵列，此时baseObj同属原group和阵列体之下，删除原group下的baseObj
                    group[0].removeObject(baseObj)
                    # 删除Type属性
                    baseObj.removeProperty("Type")

            else:
                Tools3D.sayz("A target object is needed!")
        except:
            Tools3D.sayz("Redraw Array Failed!")

    def linearArray(self, base, baseObjType, stepX, stepY, stepZ, num):
        # 线性阵列
        toolShape = []
        baseShape = base.Shape.copy()
        coordinate = FreeCAD.ActiveDocument.CoordinateSystem
        if num <= 0:
            return
        elif num == 1:
            return baseShape
        else:

            if coordinate == "Rectangular":
                # 直角坐标系(注：直角坐标系建模同样可以使用极柱坐标系建模方法，为了代码简化，另写建模方法)
                for count in range(num):
                    translatevector = FreeCAD.Vector(stepX, stepY, stepZ).multiply(count)
                    if not count == 0:
                        nshape = base.Shape.copy()
                        nshape.translate(translatevector)
                        toolShape.append(nshape)
                return baseShape.multiFuse(toolShape).removeSplitter()

            else:
                # 极坐标系和柱坐标系

                import re
                # propertiesDict: 一个字典，存储base物体所有属性及其值
                propertiesDict = {i: getattr(base, i) for i in base.PropertiesList}
                # pointCoordinateKeys 存放所有点的坐标属性对应的key，如Point1X, Point2Y
                pointCoordinateKeys = []
                for val in propertiesDict:
                    # val 为 key，可以通过 propertiesDict[val] 获取对应的值
                    if re.match(r'(Point)+(\d)+([X-Z])', val):
                        pointCoordinateKeys.append(val)
                # 创建字典objPointsDict, 存储物体所有点的key，及其对应的value
                objPointsDict = {j: propertiesDict[j].Value for j in pointCoordinateKeys}

                # 2021.6.3 xqy
                # 特别说明，仅针对球体的线性阵列，球心在原点的情况，这时R、Theta、Z均为0，阵列体的Shape是无效的，不能参加布尔运算(精度问题)
                # 因此，多传入一个参数baseObjType(二次修改时base自身没有Type属性)。如果基础物体base为球体且R为0，就修改字典中的R为0.01mm
                if baseObjType == "Vol_Spherical":
                    if coordinate == "Polar" and objPointsDict["Point1X"] == 0:
                        objPointsDict["Point1X"] = 0.00001
                    elif coordinate == "Cylindrical" and objPointsDict["Point1Y"] == 0:
                        objPointsDict["Point1Y"] = 0.00001
                    else:
                        pass

                for count in range(num):
                    if not count == 0:
                        objCopy = FreeCAD.ActiveDocument.copyObject(base)

                        for pk in pointCoordinateKeys:
                            # pointValue：当key为pk时，对应value
                            pointValue = objPointsDict[pk]
                            m = re.match(r'(Point)+(\d)+([X-Z])', pk)
                            if m:
                                if m.group(3) == 'X':
                                    pointValue += stepX
                                elif m.group(3) == 'Y':
                                    pointValue += stepY
                                else:
                                    pointValue += stepZ
                            else:
                                Tools3D.sayz("Point Values Set ERROR!")
                            objCopy.setExpression(pk, str(pointValue))
                            objPointsDict[pk] = pointValue

                        objCopy.recompute()
                        toolShape.append(objCopy.Shape.copy())
                        FreeCADGui.activeDocument().getObject(objCopy.Name).Visibility = False
                        FreeCAD.activeDocument().removeObject(objCopy.Name)
                return baseShape.fuse(toolShape).removeSplitter()

    def rectArray(self, base, orthoFace, step1, step2, num1, num2):
        # 矩形阵列

        if num1 <= 0 or num2 <= 0:
            return

        toolShape = []
        baseShape = base.Shape.copy()
        coordinate = FreeCAD.ActiveDocument.CoordinateSystem

        if coordinate == "Rectangular":
            # 直角坐标系
            if orthoFace == "XY":
                stepX = step1
                stepY = step2
                stepZ = 0
                numX = num1
                numY = num2
                numZ = 1
            elif orthoFace == "XZ":
                stepX = step1
                stepY = 0
                stepZ = step2
                numX = num1
                numY = 1
                numZ = num2
            elif orthoFace == "YZ":
                stepX = 0
                stepY = step1
                stepZ = step2
                numX = 1
                numY = num1
                numZ = num2
            else:
                Tools3D.sayz("Ortho Face Error!")
                return

            for xcount in range(numX):
                currentxvector = FreeCAD.Vector(stepX, 0, 0).multiply(xcount)
                if not xcount == 0:
                    nshape = base.Shape.copy()
                    nshape.translate(currentxvector)
                    toolShape.append(nshape)
                for ycount in range(numY):
                    currentyvector = FreeCAD.Vector(currentxvector)
                    currentyvector = currentyvector.add(FreeCAD.Vector(0, stepY, 0).multiply(ycount))
                    if not ycount == 0:
                        nshape = base.Shape.copy()
                        nshape.translate(currentyvector)
                        toolShape.append(nshape)
                    for zcount in range(numZ):
                        currentzvector = FreeCAD.Vector(currentyvector)
                        currentzvector = currentzvector.add(FreeCAD.Vector(0, 0, stepZ).multiply(zcount))
                        if not zcount == 0:
                            nshape = base.Shape.copy()
                            nshape.translate(currentzvector)
                            toolShape.append(nshape)

            return baseShape.multiFuse(toolShape).removeSplitter()

        else:
            # 极坐标系和柱坐标系

            if orthoFace != "RZ":
                Tools3D.sayz("Ortho Face Error!")
                return
            else:
                if num1 == 1:
                    sh1 = baseShape
                else:
                    import re
                    # propertiesDict: 一个字典，存储base物体所有属性及其值
                    propertiesDict = {i: getattr(base, i) for i in base.PropertiesList}
                    # pointCoordinateKeys 存放所有点的坐标属性对应的key，如Point1X, Point2Y
                    pointCoordinateKeys = []
                    for val in propertiesDict:
                        # val 为 key，可以通过 propertiesDict[val] 获取对应的值
                        if re.match(r'(Point)+(\d)+([X-Z])', val):
                            pointCoordinateKeys.append(val)
                    # 创建字典objPointsDict, 存储物体所有点的key，及其对应的value(float类型)
                    objPointsDict = {j: propertiesDict[j].Value for j in pointCoordinateKeys}

                    # 在R轴进行阵列，只有各点的R值发生改变
                    for count1 in range(num1):
                        if not count1 == 0:
                            objCopyR = FreeCAD.ActiveDocument.copyObject(base)

                            for pk in pointCoordinateKeys:

                                # 找到表示R的对应点坐标。极坐标系为Point的X，柱坐标为Point的Y
                                if coordinate == "Polar":
                                    m = re.match(r'Point\dX', pk)
                                else:
                                    m = re.match(r'Point\dY', pk)

                                if m:
                                    pointValue = objPointsDict[pk]
                                    pointValue += step1
                                    objCopyR.setExpression(pk, str(pointValue))
                                    objPointsDict[pk] = pointValue

                            # 重新计算 objCopyR，更新点坐标
                            objCopyR.recompute()
                            toolShape.append(objCopyR.Shape.copy())
                            FreeCADGui.activeDocument().getObject(objCopyR.Name).Visibility = False
                            FreeCAD.activeDocument().removeObject(objCopyR.Name)
                    sh1 = baseShape.fuse(toolShape).removeSplitter()

                # 在z轴进行阵列
                toolShapeZ = []
                baseShapeZ = sh1.copy()
                if num2 == 1:
                    return sh1
                else:
                    for count2 in range(num2):
                        translateVec = FreeCAD.Vector(0, 0, step2).multiply(count2)
                        if not count2 == 0:
                            sh2 = sh1.copy()
                            sh2.translate(translateVec)
                            toolShapeZ.append(sh2)
                    return baseShapeZ.fuse(toolShapeZ).removeSplitter()

    def polarArray(self, base, centerAxis, num):
        # 极阵列

        toolShape = []
        baseShape = base.Shape.copy()

        if num <= 0:
            return
        elif num == 1:
            return baseShape
        else:
            angle = 360.0
            center = FreeCAD.Vector(0, 0, 0)
            fraction = float(angle) / num

            if centerAxis == "X":
                axis = FreeCAD.Vector(1, 0, 0)
            elif centerAxis == "Y":
                axis = FreeCAD.Vector(0, 1, 0)
            elif centerAxis == "Z":
                axis = FreeCAD.Vector(0, 0, 1)
            else:
                Tools3D.sayz("Center Axis Error!")
                return

            import DraftVecUtils
            for i in range(num - 1):
                currangle = fraction + (i * fraction)
                nshape = base.Shape.copy()
                nshape.rotate(DraftVecUtils.tup(center), DraftVecUtils.tup(axis), currangle)
                toolShape.append(nshape)
            return baseShape.fuse(toolShape)


class GetProperty:
    def __init__(self):
        FreeCAD.ActiveDocument.openTransaction('CreateObjectArray_3D')
        self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", ObjectTools.ObjectType.Vol_Array)
        self.__setProperty(self.obj)
        InitDoc3D.addObjectToGroup_helper(self.obj, "Array", "阵列体")
        FreeCAD.ActiveDocument.commitTransaction()

    def __setProperty(self, obj):
        obj.addProperty("App::PropertyString", "Type", "", "Type of Object").Type = ObjectTools.ObjectType.Vol_Array
        obj.addProperty("App::PropertyInteger", "Order", "", "Order of the Array").Order = 100
        obj.addProperty("App::PropertyString", "ArrayType").ArrayType = "linear"

        obj.addProperty("App::PropertyLink", "Base").Base = None
        obj.addProperty("App::PropertyBool", "isSetEnabled").isSetEnabled = False
        # BaseObjType：暂存Base物体的Type
        obj.addProperty("App::PropertyString", "BaseObjType")
        # BaseType：Base物体的Label
        obj.addProperty("App::PropertyEnumeration", "BaseType")

        # 可以阵列的体：正投影体、环形体、圆柱体、圆台体、球体、环形区域体
        conformal_list = ObjectTools.getLabelsByType(ObjectTools.ObjectType.Vol_Conformal)
        annular_list = ObjectTools.getLabelsByType(ObjectTools.ObjectType.Vol_Annular)
        cylinder_list = ObjectTools.getLabelsByType(ObjectTools.ObjectType.Vol_Cylinder)
        cone_list = ObjectTools.getLabelsByType(ObjectTools.ObjectType.Vol_SpecialCone)
        spherical_list = ObjectTools.getLabelsByType(ObjectTools.ObjectType.Vol_Spherical)
        annular_section_list = ObjectTools.getLabelsByType(ObjectTools.ObjectType.Vol_Annular_Section)
        baseObj_list = conformal_list + annular_list + cylinder_list + cone_list + spherical_list + annular_section_list
        obj.BaseType = baseObj_list

        # 线性阵列
        obj.addProperty("App::PropertyInteger", "linerNumber").linerNumber = 2
        coordinate = FreeCAD.ActiveDocument.CoordinateSystem
        if coordinate == u'Rectangular':
            obj.addProperty("App::PropertyDistance", "intervalX").intervalX = 0.01
            obj.addProperty("App::PropertyDistance", "intervalY").intervalY = 0.01
            obj.addProperty("App::PropertyDistance", "intervalZ").intervalZ = 0.01
        elif coordinate == "Polar":
            obj.addProperty("App::PropertyDistance", "intervalX").intervalX = 0.01
            obj.addProperty("App::PropertyAngle", "intervalY").intervalY = 30
            obj.addProperty("App::PropertyDistance", "intervalZ").intervalZ = 0.01
        else:
            obj.addProperty("App::PropertyDistance", "intervalX").intervalX = 0.01
            obj.addProperty("App::PropertyDistance", "intervalY").intervalY = 0.01
            obj.addProperty("App::PropertyAngle", "intervalZ").intervalZ = 30

        # 矩形阵列
        obj.addProperty("App::PropertyDistance", "interval1").interval1 = 0.01
        obj.addProperty("App::PropertyDistance", "interval2").interval2 = 0.01
        obj.addProperty("App::PropertyInteger", "number1").number1 = 3
        obj.addProperty("App::PropertyInteger", "number2").number2 = 4
        if coordinate == u'Rectangular':
            obj.addProperty("App::PropertyString", "orthoFace").orthoFace = "XY"
        else:
            obj.addProperty("App::PropertyString", "orthoFace").orthoFace = "RZ"

        # 极阵列
        obj.addProperty("App::PropertyInteger", "numberPolar").numberPolar = 2
        if coordinate == u'Rectangular':
            obj.addProperty("App::PropertyString", "centerAxis").centerAxis = "X"
        else:
            obj.addProperty("App::PropertyString", "centerAxis").centerAxis = "Z"

        Tools3D.addAttributeToObject(obj)
        setHelperProperty(obj)
        getHelperPropertyValue(obj)


def getObject():
    """
       返回获取的obj
    """
    objectArray = GetProperty()
    ObjectArray(objectArray.obj)
    # Tools3D.ViewProvider(objectArray.obj.ViewObject)
    ArrayDraft.ViewProvider_Array(objectArray.obj)
    return objectArray.obj


def setHelperProperty(obj):
    obj.addProperty("App::PropertyString", "user_point_x")
    obj.addProperty("App::PropertyString", "user_point_y")
    obj.addProperty("App::PropertyString", "user_point_z")
    if FreeCAD.ActiveDocument.CoordinateSystem == 'Rectangular':
        setattr(obj, "user_point_x", "10mm")
        setattr(obj, "user_point_y", "10mm")
        setattr(obj, "user_point_z", "10mm")
    elif FreeCAD.ActiveDocument.CoordinateSystem == 'Polar':
        setattr(obj, "user_point_x", "10mm")
        setattr(obj, "user_point_y", "30deg")
        setattr(obj, "user_point_z", "10mm")
    else:
        setattr(obj, "user_point_x", "10mm")
        setattr(obj, "user_point_y", "10mm")
        setattr(obj, "user_point_z", "30deg")

    obj.addProperty("App::PropertyString", "user_linerNumber").user_linerNumber = "2"
    obj.addProperty("App::PropertyString", "user_interval1").user_interval1 = "10mm"
    obj.addProperty("App::PropertyString", "user_interval2").user_interval2 = "10mm"
    obj.addProperty("App::PropertyString", "user_number1").user_number1 = "2"
    obj.addProperty("App::PropertyString", "user_number2").user_number2 = "3"
    obj.addProperty("App::PropertyString", "user_numberPolar").user_numberPolar = "2"


def getHelperPropertyValue(obj):
    length = ExpressionTools3D.currentLengthUnits()
    angle = ExpressionTools3D.currentAngleUnits()
    if FreeCAD.ActiveDocument.CoordinateSystem == "Rectangular":
        obj.user_point_x = str(obj.intervalX.getValueAs(length)) + length
        obj.user_point_y = str(obj.intervalY.getValueAs(length)) + length
        obj.user_point_z = str(obj.intervalZ.getValueAs(length)) + length
    elif FreeCAD.ActiveDocument.CoordinateSystem == "Polar":
        obj.user_point_x = str(obj.intervalX.getValueAs(length)) + length
        obj.user_point_y = str(obj.intervalY.getValueAs(angle)) + angle
        obj.user_point_z = str(obj.intervalZ.getValueAs(length)) + length
    else:
        obj.user_point_x = str(obj.intervalX.getValueAs(length)) + length
        obj.user_point_y = str(obj.intervalY.getValueAs(length)) + length
        obj.user_point_z = str(obj.intervalZ.getValueAs(angle)) + angle
    obj.user_linerNumber = str(obj.linerNumber)
    obj.user_interval1 = str(obj.interval1.getValueAs(length)) + length
    obj.user_interval2 = str(obj.interval2.getValueAs(length)) + length
    obj.user_number1 = str(obj.number1)
    obj.user_number2 = str(obj.number2)
    obj.user_numberPolar = str(obj.numberPolar)

