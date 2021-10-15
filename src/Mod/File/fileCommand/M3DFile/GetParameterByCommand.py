# -*- coding: UTF-8 -*-
###################################################################
# author: wzn
# describe: 将操作命令分割得到参数
###################################################################
import re
from CHIPICCommand import *
import string

NEWLINE = "\n"


class CoordinateSystem(Enum):
    rectangularSys = "R"
    polarSys = "P"
    cylindricalSys = "C"
    rectangular4 = "(T,X,Y,Z)"
    polar4 = "(T,R,P,Z)"
    cylindrical4 = "(T,Z,R,P)"
    rectangular3 = "(X,Y,Z)"
    polar3 = "(R,P,Z)"
    cylindrical3 = "(Z,R,P)"


def isNum(var):
    # 判断是否是数字类型
    if isinstance(var, int) or isinstance(var, long) or isinstance(var, float) or isinstance(var, complex):
        return True
    else:
        return False


def isBool(var):
    # 判断是否是bool类型
    if isinstance(var, bool):
        return True
    else:
        return False


def isList(var):
    # 判断是否是list类型
    if isinstance(var, list):
        return True
    else:
        return False


def getSystem(systemStr):
    """
    :param systemStr: 坐标系字符串
    :return:coordinateSystem:坐标系参数
    """

    system = System()
    type = system.getSystem(systemStr)
    if system.type == System.Type.cartesian:
        coordinateSystem = "R"
    elif system.type == System.Type.polar:
        coordinateSystem = "P"
    elif system.type == System.Type.cylindrical:
        coordinateSystem = "C"
    else:
        return "返回坐标系参数,请检查System命令"

    return coordinateSystem


def getParameter(parameterStr):
    """
    :param
    :param :
    :return:[name,content]: [参数名,参数值]
    """
    #如果遇到预制的注释，跳过
    if parameterStr=="! PARAMETER":
        return None
    "去掉末尾分号"
    parameterStr = parameterStr.split(";")[0]
    #判断是否是注释
    if re.match(r"[!|！].*",parameterStr):
        return [parameterStr,"!COMMENT"]
    seg = parameterStr.split(" = ")
    if len(seg) == 2:
        name = seg[0]
        val = seg[1]

        return [name, val]

def getFunctionParameter(funcStr):
    """
    :param: funcStr为函数表达式命令
    :return: ponitName为点名称，coordinates点坐标列表
    """
    func=Function()
    func.getFunctionObject(funcStr)
    funcName=func.functionName
    funcExpression=func.functionExpression

    return [funcName,funcExpression]

def getPointParameter(poinStr):
    """
    :param: pointStr为点命令
    :return: ponitName为点名称，coordinates点坐标列表
    """

    ## 得到点的参数
    point = Point()
    point.getPoint(poinStr)
    ponitName = point.pName
    coordinates = point.coordinates

    ## 对坐标点的数据类型进行判断
    if not isList(coordinates):
        return "返回coordinates参数：请检查point命令"

    return [ponitName, coordinates]


def getLineParameter(lineStr):
    """
    :param: lineStr 线命令
    :return:lineName为线名称，lineType为线类型(CONFORMAL\OBLIQUE)，startPointName、stopPointName点坐标名称
    """

    ##得到线的参数
    line = Line()
    line.getLine(lineStr)
    lineName = line.lName
    lineType = line.type
    vals = line.vals

    ## 对lineType是否为符合规范的常量进行判断
    if lineType != Line.Type.conformal and lineType != Line.Type.oblique:
        return "返回lineTyp参数：请检查line命令"

    return [lineName, lineType, vals]


def getAreaParameter(areaStr):
    """
    :param: areaStr 面命令
    :return:areaName为面名称，areaType为面类型，pointNameList[startPointName, stopPointName,...]点名称列表
    """

    ##得到面的参数
    area = Area()
    area.getArea(areaStr)
    areaName = area.areaName
    areaType = area.shape
    pointNameList = area.vals

    if areaType != Area.Shape.conformal and areaType != Area.Shape.functional and \
            areaType != Area.Shape.rectangular and areaType != Area.Shape.polygonal:
        return "返回areaType参数：请检查area命令"

    return [areaName, areaType, pointNameList]


def getVolumeParameter(volumeStr):
    """
    :param: volumeStr 体命令
    :return:volumeName为投影体名称，volumeType为CONFORMAL类型，args[]为参数列表,点名称,半径等参数
    """

    ##得到面的参数
    volume = Volume()
    volume.getVolume(volumeStr)

    volumeName = volume.volumeName
    volumeType = volume.shape
    args = volume.args

    return [volumeName, volumeType, args]


def getArrayParameter(coordinateSystem,arrayStr,pointCoordinateStrList):
    """
    :param: volumeStr 体命令
    :return:volumeName为投影体名称，volumeType为CONFORMAL类型，args[]为参数列表,点名称,半径等参数
    """

    ##得到面的参数
    arrayName = ""
    if coordinateSystem == "R":
        system = "CARTESIAN"
    elif coordinateSystem == "P":
        system = "POLAR"
    else:
        system = "CYLINDRICAL"

    array = Array(system)
    
    pointCoordinatesList = []
    for pointCoordinates in pointCoordinateStrList:

        pointCoordinatesList.append(array.decodedCoordinateStr(pointCoordinates))

    for line in arrayStr:
        if line.startswith("!!"):
            arrayName = line.split("!!")[1]
        elif line.startswith("do"):
            array.getArray(line)

    if coordinateSystem == "R":
        args = [array.centerAxis, array.orthoFace, array.numX, array.numY, array.numZ, array.num, array.numPolar,
                array.stepX, array.stepY, array.stepZ]
    else:
        args = [array.numX, array.numZ, array.num, array.numPolar,
                array.stepX, array.stepY, array.stepZ]

    return [arrayName, array.arrayType, args, pointCoordinatesList]


def getMarkParameter(markStr):
    """
    :param: volumeStr Mark命令
    :return:objectName为要设置非均匀网格的几何体名称, direction为对应的坐标轴，cellSize 对应坐标轴上的值
    """
    ##得到Mark的参数
    mark = Mark()
    mark.getMark(markStr)

    objectName = mark.varOrObj
    direction = mark.direction
    modification = mark.modification
    cellSize = mark.cellSize
    # mark补充部分 @lzg
    ismin = mark.ismin
    ismid = mark.ismid
    ismax = mark.ismax

    return [objectName, direction, modification, cellSize, ismin, ismid, ismax]


def getAttributeParameter(attributeStr):
    """
        :param: attributeStr attribute命令
        :return:command 理想导体或真空，objectName几何体名称
        """
    if "VOID" in attributeStr:
        void = Void()
        void.getVoid(attributeStr)
        command = void.command
        objectName = void.volumeName

        return [command, objectName]

    elif "CONDUCTOR" in attributeStr:
        conductor = Conductor()
        conductor.getConductor(attributeStr)
        command = conductor.command
        objectName = conductor.areaOrVolume

        return [command, objectName]

    elif "CONDUCTANCE" in attributeStr:
        # FreeCAD.Console.PrintError('\n进入解析conductance的语句\n')
        conductance = Conductance()
        conductance.getConductance(attributeStr)
        command = conductance.command
        objectName = conductance.volumeName
        if 'X1' in attributeStr:
            sigma = conductance.sigma
            index = 1
        elif 'X2' in attributeStr:
            sigma = conductance.sigma2
            index = 2
        elif 'X3' in attributeStr:
            sigma = conductance.sigma3
            index = 3
        else:
            sigma = conductance.sigma
            index = 0
        isconductance = conductance.isconductance
        return [command, objectName, sigma, index, isconductance]

    elif "DIELECTRIC" in attributeStr:
        dielectric = Dielectric()
        dielectric.getDielectric(attributeStr)
        command = dielectric.command
        objectName = dielectric.volumeName
        if "X1" in attributeStr:
            permittivity = dielectric.permittivity1
            index = 1
        elif "X2" in attributeStr:
            permittivity = dielectric.permittivity2
            index = 2
        elif "X3" in attributeStr:
            permittivity = dielectric.permittivity3
            index = 3
        else:
            permittivity = dielectric.permittivity1
            index = 0
        return [command, objectName,permittivity,index]


#########观测设置###########

def getContourParameter(str):
    """传入Vector一行命令"""
    contour = Contour().getContourObject(str)
    return [contour.areaName, contour.field, contour.timerName, contour.isShade]


def getVectorParameter(str):
    """传入Vector一行命令"""
    vector = Vector().getVectorObject(str)
    return [vector.field1, vector.field2, vector.areaName, vector.timerName, vector.isNumber, vector.number1, vector.number2]


def getPhasespaceParameter(str):
    """传入一行Phasespace命令"""
    phasespace = Phasespace().getPhasespaceObject(str)
    return [phasespace.horizontalAxis, phasespace.verticalAxis, phasespace.timerName, phasespace.species,
            phasespace.isThickness, phasespace.direction, phasespace.thickness1, phasespace.thickness2,
            phasespace.isSuffix, phasespace.suffix]


def getRangeParameter(str):
    """传入一行range命令"""
    range = Range().getRangeObject(str)
    return [range.lineName, range.field, range.timerName,
            range.isFFT, range.isMagnitude, range.isComplex]


def getObserveParameter(str):
    """传入一组Observe命令"""
    strs = str.split("\n")
    
    # 处理observe命令主要部分
    isField = False
    isFieldIntegral = False
    isFieldPower = False
    isFieldEnergy = False
    isParticleStatistics=False
    isParticleCollected=False
    isParticleEmitted=False
    isParticleDestroyed=False
    name2 = ''

    if string.find(strs[0], "FIELD_INTEGRAL") != -1:
        observe = ObserveFieldIntegral().getObserveFieldIntegralObject(strs[0])
        isFieldIntegral = True
        name2 = observe.name2
    elif string.find(strs[0], "FIELD_POWER") != -1:
        observe = ObserveFieldPower().getObserveFieldPowerObject(strs[0])
        isFieldPower = True
        name2 = observe.name2
    elif string.find(strs[0], "FIELD_ENERGY") != -1:
        observe = ObserveFieldEnergy().getObserveFieldEnergyObject(strs[0])
        isFieldEnergy = True
        name2 = observe.name2
    elif string.find(strs[0], "PARTICLE_STATISTICS") != -1:
        observe = ObserveParticleStatistics().getObserveParticleStatisticsObject(strs[0])
        isParticleStatistics = True
        name2 = observe.name2
    elif string.find(strs[0], "COLLECTED") != -1:
        observe = ObserveParticle().getObserveParticleObject(strs[0])
        isParticleCollected = True
        name2 = observe.name2
    elif string.find(strs[0], "EMITTED") != -1:
        observe = ObserveParticle().getObserveParticleObject(strs[0])
        isParticleEmitted = True
        name2 = observe.name2
    elif string.find(strs[0], "DESTROYED") != -1:
        observe = ObserveParticle().getObserveParticleObject(strs[0])
        isParticleDestroyed = True
        name2 = observe.name2
    else:
        observe = ObserveField().getObserveFieldObject(strs[0])
        isField = True
        # @lizhenguang
        name2 = observe.name2

    # 处理observe命令的可选项部分
    isFFT = False
    fftType = "MAGNITUDE"
    isFreq=False
    freqFrom = "0"
    freqTo = "10"
    isTime = False
    timeFrom = "1"
    timeTo = "10"
    isInterval=False
    interval=""
    isFilter = False
    filterType = "STEP"
    timePara = "0.05"
    for tempStr in strs:
        # 如果对应FFT可选项
        if string.find(tempStr, "FFT") != -1:
            observeOptionFFT = ObserveOptionFFT().getObserveOptionFFTObject(tempStr)
            isFFT = True
            
            fftType = observeOptionFFT.fftType
            isFreq=observeOptionFFT.isFreq
            freqFrom = observeOptionFFT.freqFrom
            freqTo = observeOptionFFT.freqTo
        # #@fubiao
        # if string.find(tempStr,"FREQUENCY")!=-1:
        #     observeOptionF=ObserveOptionFreq().getObserveOptionFreqObject(tempStr)
        #     isFreq=True
        #     freqFrom=observeOptionF.freqFrom
        #     freqTo=observeOptionF.freqTo
        # 如果对应Time可选项
        if string.find(tempStr, "TIME") != -1:
            observeOptionT = ObserveOptionTime().getObserveOptionTimeObject(tempStr)
            isTime = True
            timeFrom = observeOptionT.timeFrom
            timeTo = observeOptionT.timeTo
        # 如果对应interval可选项
        if string.find(tempStr, "interval") != -1:
            observeOptioninterval = ObserveOptionInterval().getObserveOptionIntervalObject(tempStr)
            isInterval = True
            interval = observeOptioninterval.interval
        # 如果对应filter可选项
        if string.find(tempStr, "FILTER") != -1:
            observeOptionFilter = ObserveOptionFilter().getObserveOptionFilterObject(tempStr)
            isFilter = True
            filterType = observeOptionFilter.filterType
            timePara = observeOptionFilter.timePara

    return [
            [isField, isFieldIntegral, isFieldPower, isFieldEnergy, 
            isParticleStatistics,isParticleCollected,isParticleEmitted,isParticleDestroyed],  # 命令类型
            [observe.fieldType, observe.object,observe.option if hasattr(observe, 'option') else ""],  # 基本命令里的两个参数
            [isFFT, fftType, isFreq,freqFrom, freqTo],  # 频域
            [isTime, timeFrom, timeTo],  # 时域
            [isInterval,interval],
            [isFilter, filterType, timePara],   # 平滑
            [name2]  # 别名
            ]


def getTimerParameter(str):
    """传入一行Timer命令"""
    timer = Timer().getTimer(str)

    # 处理type
    if timer.type == Timer.Type.periodic:
        type = 0
    elif timer.type == Timer.Type.discrete:
        type = 1
    else:
        type = 2

    # 处理typeNum
    isInteger = True
    isReal = False
    if timer.numType == Timer.NumType.integer:
        isInteger = True
        isReal = False
    if timer.numType == Timer.Type.discrete:
        isInteger = False
        isReal = True

    return [timer.timerName, type, [isInteger, isReal], timer.stratTime, timer.stopTime, timer.timeIncrement,
            timer.triggerTimes]

############发射处理############

def getEmBParameter(str):
    """传入一组EmB命令"""
    strs = str.split("\n")

    # 初始化
    emitName = BeamJ = BeamV = "error"
    isSpecies = species = isNumber = creationRate = isTiming = timingType = stepMultiple = isSurfaceSpacing = \
            surfaceSpacing = isOutwardSpacing = outwardSpacing = "error"
    mobject = "未指定"
    dn = "0.001"
    excludeVolume1 = excludeVolume2 = includeVolume1 = includeVolume2 = "不指定"
    isEmit = isExclude1 = isExclude2 = isInclude1 =isInclude2 = False


    # 逐行分析
    optionStr = ""
    for line in strs:

        if line.startswith("FUNCTION") and "Dn(" in line:
            fun = Function().getFunctionObject(line)
            dn = fun.functionExpression

        if line.startswith("FUNCTION") and "BeamJ(" in line:
            fun = Function().getFunctionObject(line)
            BeamJ = fun.functionExpression

        if line.startswith("FUNCTION") and "BeamV(" in line:
            fun = Function().getFunctionObject(line)
            BeamV = fun.functionExpression

        if line.startswith("\t"):
            if ";" not in line:
                optionStr = optionStr + line + "\n"
            else:
                optionStr = optionStr + line
                emissionOption = EmissionOption().getEmissionExplosiveObject(optionStr)
                emitName = emissionOption.emitName
                isSpecies = emissionOption.isSpecies
                species = emissionOption.species
                isNumber = emissionOption.isNumber
                creationRate = emissionOption.creationRate
                isTiming = emissionOption.isTiming
                timingType = emissionOption.timingType
                stepMultiple = emissionOption.stepMultiple
                isSurfaceSpacing = emissionOption.isSurfaceSpacing
                surfaceSpacing = emissionOption.surfaceSpacing
                isOutwardSpacing = emissionOption.isOutwardSpacing
                outwardSpacing = emissionOption.outwardSpacing

        if line.startswith("EMIT"):
            isEmit = True
            emit = Emit().getEmitObject(line)
            mobject = emit.mobject
            isExclude1 = emit.isExclude1
            excludeVolume1 = emit.excludeVolume1
            isExclude2 = emit.isExclude2
            excludeVolume2 = emit.excludeVolume2
            isInclude1 = emit.isInclude1
            includeVolume1 = emit.includeVolume1
            isInclude2 = emit.isInclude2
            includeVolume2 = emit.includeVolume2

    return [emitName, BeamJ, BeamV,
            isSpecies, species, isNumber, creationRate, isTiming, timingType, stepMultiple, isSurfaceSpacing, 
            surfaceSpacing, isOutwardSpacing, outwardSpacing, dn,
            isEmit, mobject, isExclude1, excludeVolume1, isExclude2, excludeVolume2, isInclude1, 
            includeVolume1, isInclude2, includeVolume2]


def getEmEParameter(str):
    """传入一组EmE命令"""
    strs = str.split("\n")

    # 初始化
    emitName = isTField = TField = isRField = RField = isCharg = Charg = isFRate = FRate = "error"
    isSpecies = species = isNumber = creationRate = isTiming = timingType = stepMultiple = isSurfaceSpacing = \
        surfaceSpacing = isOutwardSpacing = outwardSpacing = "error"
    mobject = "未指定"
    dn = "0.001"
    excludeVolume1 = excludeVolume2 = includeVolume1 = includeVolume2 = "不指定"
    isEmit = isExclude1 = isExclude2 = isInclude1 =isInclude2 = False


    # 逐行分析
    optionStr = ""
    for line in strs:
        if line.startswith("FUNCTION") and "Dn(" in line:
            fun = Function().getFunctionObject(line)
            dn = fun.functionExpression

        if line.startswith("FUNCTION") and "TField(" in line:
            fun = Function().getFunctionObject(line)
            TField = fun.functionExpression

        if line.startswith("FUNCTION") and "RField(" in line:
            fun = Function().getFunctionObject(line)
            RField = fun.functionExpression

        if line.startswith("FUNCTION") and "FRate(" in line:
            fun = Function().getFunctionObject(line)
            FRate = fun.functionExpression

        if line.startswith("FUNCTION") and "Charg(" in line:
            fun = Function().getFunctionObject(line)
            Charg = fun.functionExpression

        if line.startswith("EMISSION"):
            emissionExplosive = EmissionExplosive().getEmissionExplosiveObject(line)
            isTField = emissionExplosive.isTField
            isRField = emissionExplosive.isRField
            isCharg = emissionExplosive.isCharg
            isFRate = emissionExplosive.isFRate

        if line.startswith("\t"):
            if ";" not in line:
                optionStr = optionStr + line + "\n"
            else:
                optionStr = optionStr + line + "\n"
                emissionOption = EmissionOption().getEmissionExplosiveObject(optionStr)
                emitName = emissionOption.emitName
                isSpecies = emissionOption.isSpecies
                species = emissionOption.species
                isNumber = emissionOption.isNumber
                creationRate = emissionOption.creationRate
                isTiming = emissionOption.isTiming
                timingType = emissionOption.timingType
                stepMultiple = emissionOption.stepMultiple
                isSurfaceSpacing = emissionOption.isSurfaceSpacing
                surfaceSpacing = emissionOption.surfaceSpacing
                isOutwardSpacing = emissionOption.isOutwardSpacing
                outwardSpacing = emissionOption.outwardSpacing

        if line.startswith("EMIT"):
            isEmit = True
            emit = Emit().getEmitObject(line)
            mobject = emit.mobject
            isExclude1 = emit.isExclude1
            excludeVolume1 = emit.excludeVolume1
            isExclude2 = emit.isExclude2
            excludeVolume2 = emit.excludeVolume2
            isInclude1 = emit.isInclude1
            includeVolume1 = emit.includeVolume1
            isInclude2 = emit.isInclude2
            includeVolume2 = emit.includeVolume2

    return [emitName, isTField, TField, isRField, RField, isCharg, Charg, isFRate, FRate,
            isSpecies, species, isNumber, creationRate, isTiming, timingType, stepMultiple, isSurfaceSpacing,
            surfaceSpacing, isOutwardSpacing, outwardSpacing, dn,
            isEmit, mobject, isExclude1, excludeVolume1, isExclude2, excludeVolume2, isInclude1,
            includeVolume1, isInclude2, includeVolume2]


def getEmGParameter(str):
    """传入一组EmG命令"""
    strs = str.split("\n")

    # 初始化
    emitName = It = Bg = Pl = Pt = Dgc = pointCoordinates = "error"
    isX1 = isX2 = isX3 = False
    isSpecies = species = isNumber = creationRate = isTiming = timingType = stepMultiple = isSurfaceSpacing = \
        surfaceSpacing = isOutwardSpacing = outwardSpacing = "error"
    mobject = "未指定"
    dn = "0.001"
    excludeVolume1 = excludeVolume2 = includeVolume1 = includeVolume2 = "不指定"
    isEmit = isExclude1 = isExclude2 = isInclude1 = isInclude2 = False

    # 逐行分析
    optionStr = ""
    for line in strs:
        if line.startswith("FUNCTION") and "Dn(" in line:
            fun = Function().getFunctionObject(line)
            dn = fun.functionExpression

        if line.startswith("FUNCTION") and "I(" in line:
            fun = Function().getFunctionObject(line)
            It = fun.functionExpression

        if line.startswith("POINT"):
            point = Point().getPoint(line)
            pointCoordinates = point.coordinates

        if line.startswith("EMISSION"):
            emission = EmissionGyro().getEmissionGyroObject(line)
            Bg = emission.Bg
            Pl = emission.Pl
            Pt = emission.Pt
            Dgc = emission.Dgc
            if emission.direction == emission.Direction.x1:
                isX1 = True
            if emission.direction == emission.Direction.x2:
                isX2 = True
            if emission.direction == emission.Direction.x3:
                isX3 = True

        if line.startswith("\t"):
            if ";" not in line:
                optionStr = optionStr + line + "\n"
            else:
                optionStr = optionStr + line + "\n"
                emissionOption = EmissionOption().getEmissionExplosiveObject(optionStr)
                emitName = emissionOption.emitName
                isSpecies = emissionOption.isSpecies
                species = emissionOption.species
                isNumber = emissionOption.isNumber
                creationRate = emissionOption.creationRate
                isTiming = emissionOption.isTiming
                timingType = emissionOption.timingType
                stepMultiple = emissionOption.stepMultiple
                isSurfaceSpacing = emissionOption.isSurfaceSpacing
                surfaceSpacing = emissionOption.surfaceSpacing
                isOutwardSpacing = emissionOption.isOutwardSpacing
                outwardSpacing = emissionOption.outwardSpacing

        if line.startswith("EMIT"):
            isEmit = True
            emit = Emit().getEmitObject(line)
            mobject = emit.mobject
            isExclude1 = emit.isExclude1
            excludeVolume1 = emit.excludeVolume1
            isExclude2 = emit.isExclude2
            excludeVolume2 = emit.excludeVolume2
            isInclude1 = emit.isInclude1
            includeVolume1 = emit.includeVolume1
            isInclude2 = emit.isInclude2
            includeVolume2 = emit.includeVolume2

    return [emitName, It, Bg, Pl, Pt, Dgc, pointCoordinates, isX1, isX2, isX3,
            isSpecies, species, isNumber, creationRate, isTiming, timingType, stepMultiple, isSurfaceSpacing,
            surfaceSpacing, isOutwardSpacing, outwardSpacing, dn,
            isEmit, mobject, isExclude1, excludeVolume1, isExclude2, excludeVolume2, isInclude1,
            includeVolume1, isInclude2, includeVolume2]


def getEmHParameter(str):
    """传入一组EmH命令"""
    strs = str.split("\n")

    # 初始化
    emitName = A = B = PHI = "error"
    isSpecies = species = isNumber = creationRate = isTiming = timingType = stepMultiple = isSurfaceSpacing = \
        surfaceSpacing = isOutwardSpacing = outwardSpacing = "error"
    mobject = "未指定"
    dn = "0.001"
    excludeVolume1 = excludeVolume2 = includeVolume1 = includeVolume2 = "不指定"
    isEmit = isExclude1 = isExclude2 = isInclude1 = isInclude2 = False

    # 逐行分析
    optionStr = ""
    for line in strs:
        if line.startswith("FUNCTION") and "Dn(" in line:
            fun = Function().getFunctionObject(line)
            dn = fun.functionExpression

        if line.startswith("FUNCTION") and "PHI(" in line:
            fun = Function().getFunctionObject(line)
            PHI = fun.functionExpression

        if line.startswith("EMISSION"):
            emission = EmissionHighfield().getEmissionHighfieldObject(line)
            A = emission.a
            B = emission.b

        if line.startswith("\t"):
            if ";" not in line:
                optionStr = optionStr + line + "\n"
            else:
                optionStr = optionStr + line + "\n"
                emissionOption = EmissionOption().getEmissionExplosiveObject(optionStr)
                emitName = emissionOption.emitName
                isSpecies = emissionOption.isSpecies
                species = emissionOption.species
                isNumber = emissionOption.isNumber
                creationRate = emissionOption.creationRate
                isTiming = emissionOption.isTiming
                timingType = emissionOption.timingType
                stepMultiple = emissionOption.stepMultiple
                isSurfaceSpacing = emissionOption.isSurfaceSpacing
                surfaceSpacing = emissionOption.surfaceSpacing
                isOutwardSpacing = emissionOption.isOutwardSpacing
                outwardSpacing = emissionOption.outwardSpacing

        if line.startswith("EMIT"):
            isEmit = True
            emit = Emit().getEmitObject(line)
            mobject = emit.mobject
            isExclude1 = emit.isExclude1
            excludeVolume1 = emit.excludeVolume1
            isExclude2 = emit.isExclude2
            excludeVolume2 = emit.excludeVolume2
            isInclude1 = emit.isInclude1
            includeVolume1 = emit.includeVolume1
            isInclude2 = emit.isInclude2
            includeVolume2 = emit.includeVolume2

    return [emitName, A, B, PHI,
            isSpecies, species, isNumber, creationRate, isTiming, timingType, stepMultiple, isSurfaceSpacing,
            surfaceSpacing, isOutwardSpacing, outwardSpacing, dn,
            isEmit, mobject, isExclude1, excludeVolume1, isExclude2, excludeVolume2, isInclude1,
            includeVolume1, isInclude2, includeVolume2]
def getEmseParameter(str):
    '''
    传入一组Emse命令
    '''
    strs = str.split("\n")
    # 初始化
    name = ""
    energy_sec = ""
    max_num_sec = ""
    WEIGHT_FACTOR = ""
    ENERGY_DISTRIBUTION = ""
    min_energy = ""
    max_energy = ""
    ANGLE_DISTRIBUTION = ""
    isCheck_WF = isCheck_ED = isCheck_AD = False
    notInclude1 = notInclude2 = include1 = include2 = u"不指定"
    Emitter = u"未指定"
    isEmit = isExclude1 = isExclude2 = isInclude1 = isInclude2 = False
    # 逐行分析
    optionStr = ""
    for line in strs:
        if line.startswith("FUNCTION") and "FED_" in line:
            fun = Function().getFunctionObject(line)
            ENERGY_DISTRIBUTION = fun.functionExpression
            isCheck_ED = True
        if line.startswith("FUNCTION") and "FAD_" in line:
            fun = Function().getFunctionObject(line)
            ANGLE_DISTRIBUTION = fun.functionExpression
            isCheck_AD = True
        if line.startswith("EMISSION"):
            optionStr = optionStr + line + "\n"
        if line.startswith("\t"):
            if ";" not in line:
                optionStr = optionStr + line + "\n"
            else:
                emseOption = EmSE().getEmseObject(optionStr)
                name = emseOption.name
                energy_sec = emseOption.energySec
                max_num_sec = emseOption.maxNum
                WEIGHT_FACTOR = emseOption.WEIGHT_FACTOR
                min_energy = emseOption.min_energy
                max_energy = emseOption.max_energy
                isCheck_WF = emseOption.isCheck_WF
                # emissionOption = EmissionOption().getEmissionExplosiveObject(optionStr)
        if line.startswith("EMIT"):
            isEmit = True
            emit = Emit().getEmitObject(line)
            Emitter = emit.mobject
            isExclude1 = emit.isExclude1
            notInclude1 = emit.excludeVolume1
            isExclude2 = emit.isExclude2
            notInclude2 = emit.excludeVolume2
            isInclude1 = emit.isInclude1
            include1 = emit.includeVolume1
            isInclude2 = emit.isInclude2
            include2 = emit.includeVolume2
    # FreeCAD.Console.PrintError("\nEmse内部字符串解析!!!!:   ")
    # FreeCAD.Console.PrintError(energy_sec)
    # FreeCAD.Console.PrintError(max_num_sec)
    return [name,energy_sec,max_num_sec, WEIGHT_FACTOR, ENERGY_DISTRIBUTION, min_energy, max_energy,
             ANGLE_DISTRIBUTION, isCheck_WF, isCheck_ED, isCheck_AD, notInclude1, notInclude2,
             include1, include2, Emitter,isEmit, isExclude1, isExclude2, isInclude1, isInclude2]




def getGasgasParameter(str):
    '''
    传入一组Gasgas命令
    '''
    name = ""
    types= "ARGON"
    pre= ""
    temp= ""

    gasgasOption = Gasgas().getGasgasObject(str)

    name = gasgasOption.name
    types = gasgasOption.types
    pre = gasgasOption.pre
    temp = gasgasOption.temp

    return [name,types,pre,temp]

def getPopulateParameter(str):
    '''
    传入一组Populate命令
    '''
    # strs = str.split("\n")

    name = ""
    types = "未指定"
    volume = "未指定"
    X1 = ""
    Y1 = ""
    Z1 = ""
    X2 = ""
    Y2 = ""
    Z2 = ""
    density = ""
    temp = ""
    # emissionOption = EmissionOption().getEmissionExplosiveObject(optionStr)
    populateOption = Populate().getPopulateObject(str)
    name = populateOption.name
    types = populateOption.types
    volume = populateOption.volume
    X1 = populateOption.X1
    Y1 = populateOption.Y1
    Z1 = populateOption.Z1
    X2 = populateOption.X2
    Y2 = populateOption.Y2
    Z2 = populateOption.Z2
    density = populateOption.density
    temp = populateOption.temp
    return [name, types, volume, X1, Y1, Z1, X2, Y2, Z2, density, temp]

def getEmTParameter(str):
    """传入一组EmT命令"""
    strs = str.split("\n")

    # 初始化
    emitName = WF = TP = "error"
    isSpecies = species = isNumber = creationRate = isTiming = timingType = stepMultiple = isSurfaceSpacing = \
        surfaceSpacing = isOutwardSpacing = outwardSpacing =  "error"
    mobject = "未指定"
    dn = "0.001"
    excludeVolume1 = excludeVolume2 = includeVolume1 = includeVolume2 = "不指定"
    isEmit = isExclude1 = isExclude2 = isInclude1 = isInclude2 = False

    # 逐行分析
    optionStr = ""
    for line in strs:
        if line.startswith("FUNCTION") and "Dn(" in line:
            fun = Function().getFunctionObject(line)
            dn = fun.functionExpression

        if line.startswith("FUNCTION") and "WF(" in line:
            fun = Function().getFunctionObject(line)
            WF = fun.functionExpression

        if line.startswith("FUNCTION") and "TP(" in line:
            fun = Function().getFunctionObject(line)
            TP = fun.functionExpression

        if line.startswith("\t"):
            if ";" not in line:
                optionStr = optionStr + line + "\n"
            else:
                optionStr = optionStr + line + "\n"
                emissionOption = EmissionOption().getEmissionExplosiveObject(optionStr)
                emitName = emissionOption.emitName
                isSpecies = emissionOption.isSpecies
                species = emissionOption.species
                isNumber = emissionOption.isNumber
                creationRate = emissionOption.creationRate
                isTiming = emissionOption.isTiming
                timingType = emissionOption.timingType
                stepMultiple = emissionOption.stepMultiple
                isSurfaceSpacing = emissionOption.isSurfaceSpacing
                surfaceSpacing = emissionOption.surfaceSpacing
                isOutwardSpacing = emissionOption.isOutwardSpacing
                outwardSpacing = emissionOption.outwardSpacing

        if line.startswith("EMIT"):
            isEmit = True
            emit = Emit().getEmitObject(line)
            mobject = emit.mobject
            isExclude1 = emit.isExclude1
            excludeVolume1 = emit.excludeVolume1
            isExclude2 = emit.isExclude2
            excludeVolume2 = emit.excludeVolume2
            isInclude1 = emit.isInclude1
            includeVolume1 = emit.includeVolume1
            isInclude2 = emit.isInclude2
            includeVolume2 = emit.includeVolume2

    return [emitName, WF, TP,
            isSpecies, species, isNumber, creationRate, isTiming, timingType, stepMultiple, isSurfaceSpacing,
            surfaceSpacing, isOutwardSpacing, outwardSpacing, dn,
            isEmit, mobject, isExclude1, excludeVolume1, isExclude2, excludeVolume2, isInclude1,
            includeVolume1, isInclude2, includeVolume2]

#########常用边界###########
def getPortParameter(str):
    """传入一组Port命令"""
    # 分割命令组
    strs = str.split(";\n")
    # 去掉第一行的!!开头
    strs[0] = strs[0].split("\n")[1]

    # 初始化
    isFt = False
    ft = "0.0"
    isGeFirst = False
    geFirstName = "GE2"
    geFirstVal = "0.0"
    isGeSecond = False
    geSecondName = "GE3"
    geSecondVal = "0.0"

    GEFunNum = 0
    for line in strs:
        if line.startswith("FUNCTION") and ".F" in line:
            isFt = True
            funF = Function().getFunctionObject(line)
            ft = funF.functionExpression
        elif line.startswith("FUNCTION") and ".GE" in line:
            funGE = Function().getFunctionObject(line)
            if GEFunNum == 0:
                isGeFirst = True
                geFirstName = funGE.functionName.split(".")[1][0:3]
                geFirstVal = funGE.functionExpression
            if GEFunNum == 1:
                isGeSecond = True
                geSecondName = funGE.functionName.split(".")[1][0:3]
                geSecondVal = funGE.functionExpression
            GEFunNum = GEFunNum + 1

        elif line.startswith("PORT"):
            port = Port().getPortObject(line)
            # FreeCAD.Console.PrintError('\n\n\n'+str(port.laplacenum3)+'  '+str(port.laplacianThird)+'\n\n\n')

    return [port.areaName,
            port.directionType,
            port.isPhaseVelocity, port.phaseVelocity,
            port.isScale, port.scale,
            isFt, ft,
            isGeFirst, geFirstName, geFirstVal,
            isGeSecond, geSecondName, geSecondVal,
            port.isNormalization, port.normalizationLine,
            port.isLaplacian, port.laplacianFirst, port.laplacianSecond,
            port.laplacenum1,port.laplacenum2,
            port.laplacenum3,port.laplacenum4,port.laplacenum5,
            port.laplacianThird,port.laplacianFourth,port.laplacianFifth,
            port.laplace_num,
            port.circuit_Checked,port.circuit,port.observe_name]


def getFreeParameter(str):
    """传入一行Free命令"""
    lines = str.split("\n")

    # 初始化
    funExpression = "1.0*Xn*Xn"

    for line in lines:
        if line.startswith("FUNCTION"):
            fun = Function().getFunctionObject(line)
            funExpression = fun.functionExpression
        if line.startswith("FREESPACE"):
            freespace = Freespace().getFreespaceObject(line)
            if freespace.xType == Freespace.XType.x1:
                xType = "R"
            elif freespace.xType == Freespace.XType.x2:
                xType = "theta"
            elif freespace.xType == Freespace.XType.x3:
                xType = "Z"
            else:
                xType = "error"

    return [freespace.freeSpaceName,
            xType,
            freespace.trendType,
            freespace.component,
            [freespace.isConductivity, funExpression]]


def getSymParameter(str):
    """传入一行Sym命令"""
    lines = str.split("\n")
    for line in lines:
        if line.startswith("SYMMETRY"):
            symmetry = Symmetry().getSymmetryObject(line)

            if symmetry.type == Symmetry.Type.periodic:
                type = u"周期对称"
            elif symmetry.type == Symmetry.Type.axial:
                type = u"轴对称"
            elif symmetry.type == Symmetry.Type.mirror:
                type = u"镜像对称"
            else:
                type = "error"

            if symmetry.trendType == Symmetry.TrendType.positive:
                isPositive = True
                isNegative = False
            if symmetry.trendType == Symmetry.TrendType.negative:
                isPositive = False
                isNegative = True

    return [type, [isNegative, isPositive], symmetry.lineOrArea1, symmetry.lineOrArea2]

#########工程信息###########
def getHeaderParameter(str):
    """传入一组Header命令"""
    strs = str.split("\n")

    modeling = author = company = remarks = ""
    for line in strs:
        if "DEVICE" in line:
            modeling = Header().getHeaderObject(line).val
        if "AUTHOR" in line:
            author = Header().getHeaderObject(line).val
        if "ORGANIZATION" in line:
            company = Header().getHeaderObject(line).val
        if "REMARKS" in line:
            remarks = Header().getHeaderObject(line).val

    return [modeling, author, company, remarks]


def getWorkSpaceSettingParameter(str):
    """传入一组工作区域命令"""
    strs = str.split("\n")

    name=x1Start=x1Stop=x2Start=x2Stop=x3Start=x3Stop=""
    for line in strs:
        if line.startswith("POINT"):
            [ponitName, coordinates] = getPointParameter(line)
            if ".LO" in ponitName:
                [x1Start, x2Start, x3Start] = coordinates
            if ".HI" in ponitName:
                [x1Stop, x2Stop, x3Stop] = coordinates
                name = ponitName.split(".HI")[0]
    return [name, x1Start, x1Stop, x2Start,x2Stop,x3Start,x3Stop]


def getMatericalParameter(str):
    """传入一组材料定义命令"""
    strs = str.split("\n")

    name = atomicNumber = atomicMass = massDensity  =conductivity = permittivity = ""
    isConductivity = isPermittivity = False
    for line in strs:
        if line.startswith("MATERIAL"):
            material = Material()
            material.getMaterial(line)
            name = material.name
            atomicNumber = material.atomicNumber
            atomicMass = material.atomicMass
            massDensity = material.massDensity
            isConductivity = material.isConductivity
            conductivity = material.conductivity
            isPermittivity = material.isPermittivity
            permittivity = material.permittivity

    return [name, atomicNumber, atomicMass, massDensity,
    [isConductivity, conductivity],
    [isPermittivity, permittivity]]

#fubiao 
def getSpeciesParameter(str):
    '''传入新粒子命令'''
    strs = str.split("\n")

    name = powerUnitl = quality = massUnit= ""

    for line in strs:
        if line.startswith("SPECIES"):
            species = Species()
            species.getSpecies(line)
            name = species.name
            powerUnitl = species.powerUnitl
            quality = species.quality
            massUnit = species.massUnit
            

    return [name, powerUnitl, quality, massUnit]

def getFiledSettingParameter(str):
    """传入一组场设置命令"""
    strs = str.split("\n")

    isSetB1 = isSetB2 = isSetB3 = isSetE1 = isSetE2 = isSetE3 = False
    setB1 = setB2 = setB3 = setE1 = setE2 = setE3 = "0.0"
    diySet = ""

    # 自定义设置为第二行
    # if len(strs) > 1:
    #     diySet = strs[2]
    for line in strs[2:]:
        if line.startswith("FUNCTION"):
            function = Function()
            function.getFunctionObject(line)
            functionName = function.functionName

            if functionName in Preset.Type.B1ST:
                isSetB1 = True
                setB1 = function.functionExpression
            elif functionName in Preset.Type.B2ST:
                isSetB2 = True
                setB2 = function.functionExpression
            elif functionName in Preset.Type.B3ST:
                isSetB3 = True
                setB3 = function.functionExpression
            elif functionName in Preset.Type.E1ST:
                isSetE1 = True
                setE1 = function.functionExpression
            elif functionName in Preset.Type.E2ST:
                isSetE2 = True
                setE2 = function.functionExpression
            elif functionName in Preset.Type.E3ST:
                isSetE3 = True
                setE3 = function.functionExpression
            else:
                #自定义
                if diySet !="":
                    diySet=diySet+"\n"
                diySet=diySet+line

    return [[isSetB1, setB1], [isSetB2, setB2], [isSetB3, setB3],
                      [isSetE1, setE1], [isSetE2, setE2], [isSetE3, setE3],
                      diySet]


def getTimeDomainComputingParameter(str):
    """传入一组时域计算设置命令"""
    strs = str.split("\n")

    time = "20"
    step = "0.01"
    algorithm = "error"
    isChargeAlgorithm = isStep = isPattern = isEM = isTE = isTM = False
    types = "ALL"
    everyNum = '1'
    maxNum = '50000'
    isChecked = False
    checkBoxStep = False
    computeTimeInterval = "1"
    is_re = False
    is_nonre = True

    for line in strs:
        if line.startswith("MAXWELL"):
            maxwell = Maxwell().getMaxwellObject(line)
            if maxwell.type == Maxwell.Type.biased:
                algorithm = u"时偏FDTD"
            elif maxwell.type == Maxwell.Type.centered:
                algorithm = u"中心差分FDTD"
            elif maxwell.type == Maxwell.Type.high_q:
                algorithm = u"高Q值FDTD"

        if line.startswith("MODE"):
            mode = Mode().getModeObject(line)
            if mode.type == Mode.Type.BOTH:
                isPattern = True
                isEM = True
            if mode.type == Mode.Type.TE:
                isPattern = True
                isTE = True
            if mode.type == Mode.Type.TM:
                isPattern = True
                isTM = True

        if line.startswith("TIME_STEP"):
            timeStep = TimeStep().getTimeStepObject(line)
            isStep = True
            step = timeStep.step

        if line.startswith("CONTINUITY"):
            isChargeAlgorithm = True

        if line.startswith("DURATION"):
            duration = Duration().getDuration(line)
            time = duration.timeSpan
        if line.startswith("MERGE"):
            merge_instance = Merge().getMergeObject(line)
            types = merge_instance.types
            everyNum = merge_instance.everyNum
            maxNum = merge_instance.maxNum
            isChecked = True
        if line.startswith("KINEMATICS"):
            kine = Kinematics().getKinematicsObject(line)
            checkBoxStep = True
            computeTimeInterval = kine.computeTimeInterval
            is_re = kine.is_re
            is_nonre = kine.is_nonre


    return [time, algorithm, [isPattern, isEM, isTE, isTM], [isStep, step], isChargeAlgorithm,types,everyNum,maxNum,isChecked,checkBoxStep,computeTimeInterval,is_re,is_nonre]


def getDataProcessingSettingParameter(str):
    """传入一组数据处理命令"""
    strs = str.split("\n")

    fileName = prefix = suffix = ""
    isObs = isRan = isCntr = isVec = isPha = isASCII = isBinary = isPrefix = isSuffix = False

    for line in strs:
        if line.startswith("DUMP"):
            dump = Dump().getDumpObject(line)
            if dump.type ==Dump.Type.type:
                if dump.val == Dump.DataType.contour:
                    isCntr = True
                elif dump.val == Dump.DataType.observe:
                    isObs = True
                elif dump.val == Dump.DataType.phasespace:
                    isPha = True
                elif dump.val == Dump.DataType.range:
                    isRan = True
                elif dump.val == Dump.DataType.vector:
                    isVec = True
            elif dump.type == Dump.Type.prefix:
                isPrefix = True
                prefix = dump.val.split("\"")[1]
            elif dump.type == Dump.Type.suffix:
                isSuffix = True
                suffix = dump.val.split("\"")[1]
            elif dump.type == Dump.Type.format:
                if dump.val == Dump.FormatType.ascii:
                    isASCII = True
                else:
                    isBinary = True
            elif dump.type == Dump.Type.name:
                fileName = dump.val

    return [isObs, isRan, isCntr, isVec, isPha,
                          [isPrefix, prefix],
                          [isSuffix, suffix],
                          [isASCII, isBinary]]


def getRunOptionsParameter(str):
    """传入运行选项设置命令"""
    strs = str.split("\n")
    isDisplay = isPause = False
    for line in strs:
        if "DISPLAY" in line:
            isDisplay = True
        if "GRAPHICS" in line:
            isPause = True

    return [isDisplay, isPause]


#########其他模型信息###########

def getDriverParameter(str):
    """
        传入一组空间电流源命令
        :param name: 名称
        :param currentDensity: 指定电流密度
        :param funExpression: 函数表达式
        :return:
        """

    strs = str.split("\n")

    # 初始化
    name=currentDensity=funExpression="error"

    for line in strs:
        if line.startswith("FUNCTION"):
            fun = Function(type=Function.Type.expression).getFunctionObject(line)
            funExpression = fun.functionExpression
        elif line.startswith("INDUCTOR"):
            drive = Driver().getDriverObject(line)
            currentDensity = drive.currentDensity
            name = drive.name
    return [name, currentDensity, funExpression]


def getFoilParameter(str):
    """"传入Foil一行命令"""
    str = str.split("\n")[0]

    foil = Foil().getFoilObject(str)
    # isDIY = DITMaterial = isDefault = defaultMaterial = "error"
    # 完善Foil的逆反转 @ lizhenguang
    if foil.material == "GOLD":
        isDefault = True
        defaultMaterial = "GOLD"
        isDIY = False
        DITMaterial = u"未指定"
    else:
        isDefault = False
        defaultMaterial = "GOLD"
        isDIY = True
        DITMaterial = foil.material
    return [foil.name, foil.thick, isDIY, DITMaterial, isDefault, defaultMaterial]


def getInductorParameter(str):
    """"传入Inductor一行命令"""
    str = str.split("\n")[0]

    inductor = Inductor().getInductorObject(str)

    return [inductor.name, inductor.diameter, inductor.isInductance, inductor.inductance]