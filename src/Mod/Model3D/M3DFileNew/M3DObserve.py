# encoding:utf-8
# 此文件存放等位图、矢量图、空间图、相空间图、时间图的m3d
import M3DShare

blankSpace = " "
semicolon = ";"
newLine = "\n"
tab = "\t"
comma = ","


def CustomTimer(obj):
    """
        新建定时器
        返回值：temp_m3d_ap
    """
    temp_m3d_ap = ""

    if obj.CustomTimerType == "周期型":
        if obj.isTimerStep:
            temp_m3d_ap += "TIMER" + blankSpace + obj.Label + blankSpace + "PERIODIC" + blankSpace + "INTEGER" + \
                           blankSpace + obj.startTime + blankSpace + obj.endTime + blankSpace + obj.period + \
                           semicolon + newLine
        if obj.isTimerSimulate:
            temp_m3d_ap += "TIMER" + blankSpace + obj.Label + blankSpace + "PERIODIC" + blankSpace + "REAL" + \
                           blankSpace + obj.startTime + blankSpace + obj.endTime + blankSpace + obj.period + \
                           semicolon + newLine

    if obj.CustomTimerType == "离散型":
        if obj.isTimerStep:
            temp_m3d_ap += "TIMER" + blankSpace + obj.Label + blankSpace + "DISCRETE" + blankSpace + "INTEGER" + \
                           blankSpace + obj.DiscreteTime + semicolon + newLine
        if obj.isTimerSimulate:
            temp_m3d_ap += "TIMER" + blankSpace + obj.Label + blankSpace + "DISCRETE" + blankSpace + "REAL" + \
                           blankSpace + obj.DiscreteTime + semicolon + newLine
    return temp_m3d_ap


def DefaultTimer(obj):
    """
        默认定时器
        返回值：temp_m3d_ap
    """
    temp_m3d_ap = ""

    if obj.defTimerType == "周期型":
        if obj.isTimeSteps:
            temp_m3d_ap += "TIMER" + blankSpace + obj.Label + blankSpace + "PERIODIC" + blankSpace + "INTEGER" + \
                           blankSpace + obj.startTime + blankSpace + obj.endTime + blankSpace + obj.timeCycle + \
                           semicolon + newLine
        if obj.isSimulationSteps:
            temp_m3d_ap += "TIMER" + blankSpace + obj.Label + blankSpace + "PERIODIC" + blankSpace + "REAL" + \
                           blankSpace + obj.startTime + blankSpace + obj.endTime + blankSpace + obj.timeCycle + \
                           semicolon + newLine

    if obj.defTimerType == "离散型":
        if obj.isTimeSteps:
            temp_m3d_ap += "TIMER" + blankSpace + obj.Label + blankSpace + "DISCRETE" + blankSpace + "INTEGER" + \
                           blankSpace + obj.discreteTime + semicolon + newLine
        if obj.isSimulationSteps:
            temp_m3d_ap += "TIMER" + blankSpace + obj.Label + blankSpace + "DISCRETE" + blankSpace + "REAL" + \
                           blankSpace + obj.discreteTime + semicolon + newLine
    return temp_m3d_ap


def Cntr(obj):
    """
        Cntr
        返回值：
            temp_m3d
            temp_m3d_ap
    """
    temp_m3d = ""
    temp_m3d_ap = ""
    Oline_temp = ""
    Timer_name = M3DShare.getTimerM3D(obj)

    # 是否指定正交投影面
    if obj.orthogonalProjectionPlane == "未指定":
        temp_m3d += "AREA" + blankSpace + obj.Label + blankSpace + "CONFORMAL"
        temp_m3d += M3DShare.PointCoordinates().point1(obj)
        temp_m3d += M3DShare.PointCoordinates().point2(obj) + semicolon + newLine
        ProjectionLine_temp = "CONTOUR" + blankSpace + "FIELD" + blankSpace + obj.observationField + \
                              blankSpace + obj.Label
    else:
        ProjectionLine_temp = "CONTOUR" + blankSpace + "FIELD" + blankSpace + obj.observationField + blankSpace + \
                              obj.orthogonalProjectionPlane
    # 是否选中等值线填充
    if obj.isoline:
        Oline_temp = blankSpace + "SHADE"

    temp_m3d_ap += '%s %s%s' % (ProjectionLine_temp, Timer_name, Oline_temp) + semicolon + newLine
    return temp_m3d, temp_m3d_ap


def Vector(obj):
    """
        Vector
        返回值：temp_m3d
              temp_m3d_ap

    """
    temp_m3d = ""
    temp_m3d_ap = ""
    VectorNumber_temp = ""
    Timer_name = M3DShare.getTimerM3D(obj)

    # 是否指定正交投影面
    if obj.orthogonalProjectionPlane == "未指定":
        temp_m3d += "AREA" + blankSpace + obj.Label + blankSpace + "CONFORMAL"
        temp_m3d += M3DShare.PointCoordinates().point1(obj)
        temp_m3d += M3DShare.PointCoordinates().point2(obj) + semicolon + newLine
        ProjectionLine_temp = "VECTOR" + blankSpace + "FIELD" + blankSpace + obj.observationField1 + comma + \
                              obj.observationField2 + blankSpace + obj.Label
    else:
        ProjectionLine_temp = "VECTOR" + blankSpace + "FIELD" + blankSpace + obj.observationField1 + comma + \
                              obj.observationField2 + blankSpace + obj.orthogonalProjectionPlane
    # 是否指定矢量个数
    if obj.isVectorNumber:
        VectorNumber_temp = blankSpace + "NUMBER" + blankSpace + obj.vectorNumber1 + blankSpace + obj.vectorNumber2

    temp_m3d_ap += '%s %s%s' % (ProjectionLine_temp, Timer_name, VectorNumber_temp) + semicolon + newLine
    return temp_m3d, temp_m3d_ap


def PhasSpace(obj):
    """
        PhasSpace
        返回值：temp_m3d_ap
    """
    temp_m3d_ap = ""
    temp_m3d_use = ""
    temp_m3d_use += "PHASESPACE" + blankSpace + "AXES" + blankSpace + obj.horizontalAxisShow + comma + \
                    obj.verticalAxisShow + blankSpace
    Thickness_temp = ""
    Suffix_temp = ""
    Timer_name = M3DShare.getTimerM3D(obj)

    if obj.observationParticle == u'全部':
        Particle_temp = ""
    elif obj.observationParticle == u'电子':
        Particle_temp = blankSpace + "SPECIES ELECTRON"
    elif obj.observationParticle == u'质子':
        Particle_temp = blankSpace + "SPECIES PROTON"
    else:
        Particle_temp = blankSpace + "SPECIES " + obj.observationParticle

    # 是否显示厚度
    if obj.isShowThickness:
        Thickness_temp = blankSpace + "WINDOW" + blankSpace + obj.showThick + blankSpace + obj.thickValue1 + \
                         blankSpace + obj.thickValue2

    # 是否选中后缀
    if obj.isSuffix:
        Suffix_temp = blankSpace + "SUFFIX" + blankSpace + obj.suffix

    temp_m3d_ap += temp_m3d_use + '%s%s%s%s' % (Timer_name, Particle_temp, Thickness_temp, Suffix_temp) +\
                   semicolon + newLine

    return temp_m3d_ap


def AreaRan(obj):
    """
        AreaRan:空间观测
        返回值：temp_m3d
              temp_m3d_ap
    """
    temp_m3d = ""
    temp_m3d_ap = ""
    Field_temp = ""
    FieldIntegral_temp = ""
    FieldPower_temp = ""
    FieldEnergy_temp = ""
    FFT_temp = ""
    Timer_name = M3DShare.getTimerM3D(obj)

    # 场、场积分、场功率、场能量
    if obj.orthogonalProjectionLine == "未指定":
        temp_m3d += "LINE" + blankSpace + obj.Label + blankSpace + "CONFORMAL"
        temp_m3d += M3DShare.PointCoordinates().point1(obj)
        temp_m3d += M3DShare.PointCoordinates().point2(obj) + semicolon + newLine
        if obj.isField:
            Field_temp = "RANGE" + blankSpace + "FIELD" + blankSpace + obj.field + blankSpace + obj.Label
        if obj.isFieldIntegral:
            FieldIntegral_temp = "RANGE" + blankSpace + "FIELD_INTEGRAL" + blankSpace + obj.fieldIntegral + blankSpace + obj.Label
        if obj.isFieldPower:
            FieldPower_temp = "RANGE" + blankSpace + "FIELD_POWER" + blankSpace + obj.fieldPower + blankSpace + obj.Label
        if obj.isFieldEnergy:
            FieldEnergy_temp = "RANGE" + blankSpace + "FIELD_ENERGY" + blankSpace + obj.fieldEnergy + blankSpace + obj.Label

    else:
        if obj.isField:
            Field_temp = "RANGE" + blankSpace + "FIELD" + blankSpace + obj.field + blankSpace + obj.orthogonalProjectionLine
        if obj.isFieldIntegral:
            FieldIntegral_temp = "RANGE" + blankSpace + "FIELD_INTEGRAL" + blankSpace + obj.fieldIntegral + blankSpace + \
                                 obj.orthogonalProjectionLine
        if obj.isFieldPower:
            FieldPower_temp = "RANGE" + blankSpace + "FIELD_POWER" + blankSpace + obj.fieldPower + blankSpace + \
                              obj.orthogonalProjectionLine
        if obj.isFieldEnergy:
            FieldEnergy_temp = "RANGE" + blankSpace + "FIELD_ENERGY" + blankSpace + obj.fieldEnergy + blankSpace + \
                               obj.orthogonalProjectionLine

    # 是否选中傅里叶变换
    if obj.isFFT:
        if obj.isRealAnalysis:
            FFT_temp = blankSpace + "FFT" + blankSpace + "MAGNITUDE"
        if obj.isComplexAnalysis:
            FFT_temp = blankSpace + "FFT" + blankSpace + "COMPLEX"

    # 粒子
    if not obj.isParticle:
        temp_m3d_ap += '%s%s%s%s %s%s' % (Field_temp, FieldIntegral_temp, FieldPower_temp, FieldEnergy_temp,
                                          Timer_name, FFT_temp) + semicolon + newLine
    else:
        temp_m3d = ""
        temp_m3d_ap += "RANGE" + blankSpace + "PARTICLE" + blankSpace + obj.chooseParticle + blankSpace + \
                       obj.particleType + blankSpace + obj.particleAxis + blankSpace + Timer_name + semicolon + newLine

    return temp_m3d, temp_m3d_ap


def Observe(obj):
    """
        Observe :时间观测
        返回值：temp_m3d
              temp_m3d_ap
    """
    temp_m3d = ""
    temp_m3d_ap = ""
    # 模块临时变量
    Field_temp = ""
    ParticleStatistics_temp = ""
    CollectedParticles_temp = ""
    EmittedParticle_temp = ""
    AnnihilatingParticle_temp = ""
    FFT_temp = ""
    DataDisplay_temp = ""
    Alias_temp = ""
    FieldIntegral_temp = ""
    FieldPower_temp = ""
    FieldEnergy_temp = ""

    # 别名
    if obj.alias:
        Alias_temp = blankSpace + "suffix" + blankSpace + obj.alias

    # 分类项
    if obj.orthogonalProjectionPlane == "未指定":
        if obj.ObservationType == "时间观测点":
            temp_m3d += "POINT" + blankSpace + obj.Label + blankSpace + obj.point1_X + blankSpace + \
                        obj.point1_Y + blankSpace + obj.point1_Z + semicolon + newLine
            if obj.isField:
                Field_temp = "OBSERVE" + blankSpace + "FIELD" + blankSpace + obj.field + blankSpace + obj.Label

        elif obj.ObservationType == "时间观测线":
            temp_m3d += "LINE" + blankSpace + obj.Label + blankSpace + "CONFORMAL"
            temp_m3d += M3DShare.PointCoordinates().point1(obj)
            temp_m3d += M3DShare.PointCoordinates().point2(obj) + semicolon + newLine
            if obj.isField:
                Field_temp = "OBSERVE" + blankSpace + "FIELD" + blankSpace + \
                             obj.field + blankSpace + obj.Label
            if obj.isFieldIntegral:
                FieldIntegral_temp = "OBSERVE" + blankSpace + "FIELD_INTEGRAL" + blankSpace + \
                                     obj.fieldIntegral + blankSpace + obj.Label

        elif obj.ObservationType == "时间观测面":
            temp_m3d += "AREA" + blankSpace + obj.Label + blankSpace + "CONFORMAL"
            temp_m3d += M3DShare.PointCoordinates().point1(obj)
            temp_m3d += M3DShare.PointCoordinates().point2(obj) + semicolon + newLine
            if obj.isField:
                Field_temp = "OBSERVE" + blankSpace + "FIELD" + blankSpace + obj.field + \
                             blankSpace + obj.Label
            if obj.isFieldIntegral:
                FieldIntegral_temp = "OBSERVE" + blankSpace + "FIELD_INTEGRAL" + blankSpace + \
                                     obj.fieldIntegral + blankSpace + obj.Label
            if obj.isFieldPower:
                FieldPower_temp = "OBSERVE" + blankSpace + "FIELD_POWER" + blankSpace + obj.fieldPower + \
                                  blankSpace + obj.Label

            if obj.isCollectedParticles:
                #m3d运行有问题，lable和particles3对调
                CollectedParticles_temp = "OBSERVE" + blankSpace + "COLLECTED" + blankSpace + \
                                          obj.Label + blankSpace + obj.particles4 + blankSpace + obj.particles3
            if obj.isEmittedParticle:
                EmittedParticle_temp = "OBSERVE" + blankSpace + "EMITTED" + blankSpace + obj.particles3 + \
                                       blankSpace + obj.particles4 + blankSpace + obj.Label
            if obj.isAnnihilatingParticle:
                AnnihilatingParticle_temp = "OBSERVE" + blankSpace + "DESTROYED" + blankSpace + \
                                            obj.particles3 + blankSpace + obj.particles4 + blankSpace + obj.Label

        elif obj.ObservationType == "时间观测体":
            temp_m3d += "VOLUME" + blankSpace + obj.Label + blankSpace + "CONFORMAL"
            temp_m3d += M3DShare.PointCoordinates().point1(obj)
            temp_m3d += M3DShare.PointCoordinates().point2(obj) + semicolon + newLine
            if obj.isFieldEnergy:
                FieldEnergy_temp = "OBSERVE" + blankSpace + "FIELD_ENERGY" + blankSpace + obj.fieldEnergy + \
                                   blankSpace + obj.Label
            if obj.isParticleStatistics:
                if obj.particles2 == "EMIT_EPS":
                    ParticleStatistics_temp = "OBSERVE" + blankSpace + "PARTICLE_STATISTICS" + blankSpace \
                                              + obj.particles2 + blankSpace + obj.particles1 + blankSpace + obj.Label
                else:
                    ParticleStatistics_temp = "OBSERVE" + blankSpace + "PARTICLE_STATISTICS" + blankSpace \
                                              + obj.particles2 + blankSpace + obj.particles4 + blankSpace + obj.Label
            if obj.isCollectedParticles:
                # 收集粒子做特殊处理（腊群老师需要），原版本暂时保存
                #CollectedParticles_temp = "OBSERVE" + blankSpace + "COLLECTED" + blankSpace + \
                                          #obj.particles3 + blankSpace + obj.particles4 + blankSpace + obj.Label
                CollectedParticles_temp = "OBSERVE" + blankSpace + "COLLECTED" + blankSpace + \
                                          obj.Label + blankSpace + obj.particles4 + blankSpace + obj.particles3
                # if obj.particles3 == "CURRENT":
                #     CollectedParticles_temp += ";" + newLine + "OBSERVE" + blankSpace + "COLLECTED" + blankSpace + \
                #                             obj.Label + blankSpace + obj.particles4 + blankSpace + "DUMP"
            if obj.isEmittedParticle:
                EmittedParticle_temp = "OBSERVE" + blankSpace + "EMITTED" + blankSpace + obj.particles3 + \
                                       blankSpace + obj.particles4 + blankSpace + obj.Label
            if obj.isAnnihilatingParticle:
                AnnihilatingParticle_temp = "OBSERVE" + blankSpace + "DESTROYED" + blankSpace + \
                                            obj.particles3 + blankSpace + obj.particles4 + blankSpace + obj.Label

    else:
        if obj.ObservationType == "时间观测点":
            if obj.isField:
                Field_temp = "OBSERVE" + blankSpace + "FIELD" + blankSpace + obj.field + \
                             blankSpace + obj.orthogonalProjectionPlane

        elif obj.ObservationType == "时间观测线":
            if obj.isField:
                Field_temp = "OBSERVE" + blankSpace + "FIELD" + blankSpace + obj.field + \
                             blankSpace + obj.orthogonalProjectionPlane
            if obj.isFieldIntegral:
                FieldIntegral_temp = "OBSERVE" + blankSpace + "FIELD_INTEGRAL" + blankSpace + \
                                     obj.fieldIntegral + blankSpace + obj.orthogonalProjectionPlane

        elif obj.ObservationType == "时间观测面":
            if obj.isField:
                Field_temp = "OBSERVE" + blankSpace + "FIELD" + blankSpace + obj.field + \
                             blankSpace + obj.orthogonalProjectionPlane
            if obj.isFieldIntegral:
                FieldIntegral_temp = "OBSERVE" + blankSpace + "FIELD_INTEGRAL" + blankSpace + \
                                     obj.fieldIntegral + blankSpace + obj.orthogonalProjectionPlane
            if obj.isFieldPower:
                FieldPower_temp = "OBSERVE" + blankSpace + "FIELD_POWER" + blankSpace + obj.fieldPower + \
                                  blankSpace + obj.orthogonalProjectionPlane
            if obj.isCollectedParticles:
                CollectedParticles_temp = "OBSERVE" + blankSpace + "COLLECTED" + blankSpace + \
                                          obj.orthogonalProjectionPlane + blankSpace + obj.particles4 + blankSpace + obj.particles3
            if obj.isEmittedParticle:
                EmittedParticle_temp = "OBSERVE" + blankSpace + "EMITTED" + blankSpace + obj.particles3 + \
                                       blankSpace + obj.particles4 + blankSpace + obj.orthogonalProjectionPlane
            if obj.isAnnihilatingParticle:
                AnnihilatingParticle_temp = "OBSERVE" + blankSpace + "DESTROYED" + blankSpace + \
                                            obj.particles3 + blankSpace + obj.particles4 + blankSpace + obj.orthogonalProjectionPlane

        elif obj.ObservationType == "时间观测体":
            if obj.isFieldEnergy:
                FieldEnergy_temp = "OBSERVE" + blankSpace + "FIELD_ENERGY" + blankSpace + obj.fieldEnergy + \
                                   blankSpace + obj.orthogonalProjectionPlane
            if obj.isParticleStatistics:
                if obj.particles2 == "EMIT_EPS":
                    ParticleStatistics_temp = "OBSERVE" + blankSpace + "PARTICLE_STATISTICS" + blankSpace \
                                              + obj.particles2 + blankSpace + obj.particles1 + blankSpace + obj.orthogonalProjectionPlane
                else:
                    ParticleStatistics_temp = "OBSERVE" + blankSpace + "PARTICLE_STATISTICS" + blankSpace \
                                              + obj.particles2 + blankSpace + obj.particles4 + blankSpace + obj.orthogonalProjectionPlane
            if obj.isCollectedParticles:
                #收集粒子做特殊处理（腊群老师需要），原版本暂时保存
                #CollectedParticles_temp = "OBSERVE" + blankSpace + "COLLECTED" + blankSpace + \
                                          #obj.particles3 + blankSpace + obj.particles4 + blankSpace + obj.orthogonalProjectionPlane
                CollectedParticles_temp = "OBSERVE" + blankSpace + "COLLECTED" + blankSpace + \
                                          obj.orthogonalProjectionPlane + blankSpace + obj.particles4 + blankSpace + obj.particles3
                # if obj.particles3 == "CURRENT":
                #     CollectedParticles_temp += ";" + newLine + "OBSERVE" + blankSpace + "COLLECTED" + blankSpace + \
                #                             obj.orthogonalProjectionPlane + blankSpace + obj.particles4 + blankSpace + "DUMP"
            if obj.isEmittedParticle:
                EmittedParticle_temp = "OBSERVE" + blankSpace + "EMITTED" + blankSpace + obj.particles3 + \
                                       blankSpace + obj.particles4 + blankSpace + obj.orthogonalProjectionPlane
            if obj.isAnnihilatingParticle:
                AnnihilatingParticle_temp = "OBSERVE" + blankSpace + "DESTROYED" + blankSpace + \
                                            obj.particles3 + blankSpace + obj.particles4 + blankSpace + obj.orthogonalProjectionPlane

    temp_m3d_ap += '%s%s%s%s%s%s%s%s%s' % (Field_temp, FieldIntegral_temp, FieldPower_temp, FieldEnergy_temp,
                                           ParticleStatistics_temp, CollectedParticles_temp, EmittedParticle_temp,
                                           AnnihilatingParticle_temp, Alias_temp) + semicolon + newLine

    # 是否选中数据显示平滑处理
    if obj.isDataDisplay:
        # 如果是变量，不加"NANOSECOND"
        temp = obj.filteringTimeParameter
        if str(temp).replace('.', '').replace('-', '').replace('e', '').replace('E', '').isdigit():
            temp = obj.filteringTimeParameter + "NANOSECOND"
        if obj.isTimeAverage:
            DataDisplay_temp = blankSpace + "FILTER STEP" + blankSpace + temp
        if obj.isRcAnalyze:
            DataDisplay_temp = blankSpace + "FILTER LO_PASS" + blankSpace + temp

        temp_m3d_ap += '%s%s%s%s%s%s%s%s%s%s' % (Field_temp, FieldIntegral_temp, FieldPower_temp, FieldEnergy_temp,
                                                 ParticleStatistics_temp, CollectedParticles_temp, EmittedParticle_temp,
                                                 AnnihilatingParticle_temp,Alias_temp, DataDisplay_temp) + semicolon + newLine

    # 是否进行傅里叶变换
    if obj.isFFT:
        temp_frequencyRange1 = obj.frequencyRange1
        temp_frequencyRange2 = obj.frequencyRange2
        if obj.frequencyRange1.isdigit():
            temp_frequencyRange1 += "GHZ"
        if obj.frequencyRange2.isdigit():
            temp_frequencyRange2 += "GHZ"

        if obj.isRealAnalysis:
            FFT_temp = blankSpace + "FFT" + blankSpace + "MAGNITUDE"
            if obj.isFrequencyRange:
                FFT_temp = blankSpace + "FFT" + blankSpace + "MAGNITUDE" + blankSpace + "WINDOW FREQUENCY" + blankSpace + \
                           temp_frequencyRange1 + blankSpace + temp_frequencyRange2
        if obj.isComplexAnalysis:
            FFT_temp = blankSpace + "FFT" + blankSpace + "COMPLEX"
            if obj.isFrequencyRange:
                FFT_temp = blankSpace + "FFT" + blankSpace + "COMPLEX" + blankSpace + "WINDOW FREQUENCY" + blankSpace + \
                           temp_frequencyRange1 + blankSpace + temp_frequencyRange2
        temp_m3d_ap += '%s%s%s%s%s%s%s%s%s%s' % (Field_temp, FieldIntegral_temp, FieldPower_temp, FieldEnergy_temp,
                                                 ParticleStatistics_temp, CollectedParticles_temp, EmittedParticle_temp,
                                                 AnnihilatingParticle_temp, Alias_temp, FFT_temp) + semicolon + newLine

    # 是否选中时间范围
    if obj.isTimeRange:
        TimeRange_temp = blankSpace + "WINDOW TIME" + blankSpace + obj.timeRange1 + "NANOSECOND" + blankSpace + \
                         obj.timeRange2 + "NANOSECOND"

        temp_m3d_ap += '%s%s%s%s%s%s%s%s%s%s' % (Field_temp, FieldIntegral_temp, FieldPower_temp,FieldEnergy_temp,
                                                 ParticleStatistics_temp, CollectedParticles_temp, EmittedParticle_temp,
                                                 AnnihilatingParticle_temp, Alias_temp, TimeRange_temp) + semicolon + newLine
    # 是否选中观察间隔
    if obj.isObservationInterval:
        ObservationInterval_temp = blankSpace + "interval" + blankSpace + obj.observationInterval
        temp_m3d_ap += '%s%s%s%s%s%s%s%s%s%s' % (Field_temp, FieldIntegral_temp, FieldPower_temp,FieldEnergy_temp,
                                                 ParticleStatistics_temp, CollectedParticles_temp, EmittedParticle_temp,
                                                 AnnihilatingParticle_temp, Alias_temp, ObservationInterval_temp) + semicolon + newLine

    return temp_m3d, temp_m3d_ap
