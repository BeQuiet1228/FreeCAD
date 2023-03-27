# encoding:utf-8
# 此文件包括：束发射，爆炸式发射，回旋发射，粒子设置，强场发射，热致发射，二次发射，气体电离
import M3DShare
from Model3D.Tools import Tools3D

blankSpace = " "
semicolon = ";"
newLine = "\n"
tab = "\t"
comma = ","


class EmissionFunction:
    # 发射选项和发射区域的公共m3d命令
    def LaunchOptions(self, obj):
        temp_m3d_pap = ""
        if obj.isParticleType:
            temp_m3d_pap += newLine + tab
            if obj.particleType == "电子":
                temp_m3d_pap += "SPECIES" + blankSpace + "ELECTRON"
            elif obj.particleType == "质子":
                temp_m3d_pap += "SPECIES" + blankSpace + "PROTON"
            else:
                Tools3D.sayz("请输入正确的粒子类型")
        if obj.isGenerationRate:
            temp_m3d_pap += newLine + tab
            temp_m3d_pap += "NUMBER" + blankSpace + str(obj.generationRate)
        if obj.isFiringInterval:
            temp_m3d_pap += newLine + tab
            if obj.isRandomDistribution:
                temp_m3d_pap += "RANDOM_TIMING" + blankSpace + str(obj.firingInterval)
            elif obj.isStrictTiming:
                temp_m3d_pap += "TIMING" + blankSpace + str(obj.firingInterval)
        if obj.isSurfaceDistribution:
            temp_m3d_pap += newLine + tab
            temp_m3d_pap += "SURFACE_SPACING" + blankSpace
            if obj.isRandom1:
                temp_m3d_pap += "RANDOM"
            elif obj.isBalance1:
                temp_m3d_pap += "UNIFORM"
            elif obj.isImmobilization1:
                temp_m3d_pap += "FIXED"

        if obj.isOuterSurfaceDistribution:
            temp_m3d_pap += newLine + tab
            temp_m3d_pap += "OUTWARD_SPACING" + blankSpace
            if obj.isRandom2:
                temp_m3d_pap += "RANDOM" + blankSpace
            elif obj.isImmobilization2:
                temp_m3d_pap += "FIXED" + blankSpace
            temp_m3d_pap += obj.Label + ".Dn"

        if hasattr(obj, "velocityDistribution"):
            if obj.isVelocityDistribution:
                temp_m3d_pap += newLine + tab
                temp_m3d_pap += "VELOCITY_SPREAD" + blankSpace + str(obj.velocityDistribution)

        temp_m3d_pap += semicolon + newLine

        if obj.emitter != "未指定":
            temp_m3d_pap += "EMIT" + blankSpace + obj.Label + blankSpace + obj.emitter
            if obj.launchArea1 != "不指定":
                temp_m3d_pap += blankSpace + "EXCLUDE" + blankSpace + obj.launchArea1
            if obj.launchArea2 != "不指定":
                temp_m3d_pap += blankSpace + "EXCLUDE" + blankSpace + obj.launchArea2
            if obj.launchOrthogonalProjectionRegin1 != "不指定":
                temp_m3d_pap += blankSpace + "INCLUDE" + blankSpace + obj.launchOrthogonalProjectionRegin1
            if obj.launchOrthogonalProjectionRegin2 != "不指定":
                temp_m3d_pap += blankSpace + "INCLUDE" + blankSpace + obj.launchOrthogonalProjectionRegin2
            temp_m3d_pap += semicolon + newLine

        return temp_m3d_pap

        # 此函数一条偏移Dn(T,X,Y,Z)的字符串命令

    def Excursion(self, obj):
        temp_m3d_pap = ""
        functionParameters = M3DShare.getCoodinatePara()
        if obj.isOuterSurfaceDistribution:
            temp_m3d_pap += "FUNCTION" + blankSpace + obj.Label + ".Dn" + functionParameters + \
                            obj.excursion + semicolon + newLine
        return temp_m3d_pap


# 束发射
def Beam(obj):
    temp_m3d_pap = ""
    temp_m3d_pap += EmissionFunction().Excursion(obj)
    functionParameters = M3DShare.getCoodinatePara()
    # 临时变量varF，便于字符串命令的拼接
    varF = "FUNCTION" + blankSpace + obj.Label
    temp_m3d_pap += varF + ".J" + functionParameters + obj.beamCurrentDensity + semicolon + newLine
    temp_m3d_pap += varF + ".V" + functionParameters + obj.beamVoltageDensity + semicolon + newLine
    temp_m3d_pap += "EMISSION" + blankSpace + "BEAM" + blankSpace + obj.Label + ".J" + blankSpace + obj.Label + \
                    ".V" + newLine + tab + "MODEL" + blankSpace + obj.Label
    temp_m3d_pap += EmissionFunction().LaunchOptions(obj)
    return temp_m3d_pap


# 爆炸发射
def Exps(obj):
    temp_m3d_pap = ""
    temp_m3d_pap += EmissionFunction().Excursion(obj)
    functionParameters = M3DShare.getCoodinatePara()
    # 临时变量var,varF便于字符串的命令的拼接
    var = ""
    varF = "FUNCTION" + blankSpace + obj.Label
    if obj.isLimitFieldValue:
        temp_m3d_pap += varF + ".TField" + functionParameters + obj.limitFieldValue + semicolon + newLine
        var += blankSpace + "THRESHOLD" + blankSpace + obj.Label + ".TField"
    if obj.isMoreThanSpacemoreThanSpace:
        temp_m3d_pap += varF + ".RField" + functionParameters + obj.moreThanSpace + semicolon + newLine
        var += blankSpace + "RESIDUAL" + blankSpace + obj.Label + ".RField"
    if obj.isPlasmaProductionRate:
        temp_m3d_pap += varF + ".FRate" + functionParameters + obj.plasmaProductionRate + semicolon + newLine
        var += blankSpace + "PLASMA" + blankSpace + obj.Label + ".FRate"
    if obj.isTheMinimumCharge:
        temp_m3d_pap += varF + ".Charge" + functionParameters + obj.theMinimumCharge + semicolon + newLine
        var += blankSpace + "MINIMUM_CHARGE" + blankSpace + obj.Label + ".Charge"
    temp_m3d_pap += "EMISSION" + blankSpace + "EXPLOSIVE" + var + newLine + tab + "MODEL" + blankSpace + obj.Label
    temp_m3d_pap += EmissionFunction().LaunchOptions(obj)
    return temp_m3d_pap


# 回旋发射
def Gyro(obj):
    temp_m3d_pap = ""
    temp_m3d_pap += EmissionFunction().Excursion(obj)
    temp_m3d_pap += "FUNCTION" + blankSpace + obj.Label + ".I(T) = " + obj.beamCurrent + semicolon + newLine
    temp_m3d_pap += "POINT" + blankSpace + obj.Label + ".CPT" + blankSpace + obj.launchCenterCoordinatesX + \
                    comma + blankSpace + obj.launchCenterCoordinatesY +comma + blankSpace + obj.launchCenterCoordinatesZ + \
                    semicolon + newLine
    # 临时变量axisDirection,轴线方向
    if obj.isCheckX:
        axisDirection = "X1"
    elif obj.isCheckY:
        axisDirection = "X2"
    elif obj.isCheckZ:
        axisDirection = "X3"
    else:
        print("轴线方向选取有误,请重新选择引导轴线方向")
        axisDirection = "请重新选择引导轴线方向"
    temp_m3d_pap += "EMISSION" + blankSpace + "GYRO" + blankSpace + obj.Label + ".I" + blankSpace + \
                    obj.guidingMagneticField + blankSpace + obj.longitudinalMomentum + blankSpace + \
                    obj.theHorizontalMomentum + blankSpace + obj.guideRadius + blankSpace + axisDirection + \
                    blankSpace + obj.Label + ".CPT" + newLine + tab + "MODEL" + blankSpace + obj.Label
    temp_m3d_pap += EmissionFunction().LaunchOptions(obj)
    return temp_m3d_pap


# 强场发射
def Feld(obj):
    temp_m3d_pap = ""
    temp_m3d_pap += EmissionFunction().Excursion(obj)
    functionParameters = M3DShare.getCoodinatePara()
    temp_m3d_pap += "FUNCTION" + blankSpace + obj.Label + ".B" + functionParameters + \
                    obj.constantB + semicolon + newLine
    temp_m3d_pap += "FUNCTION" + blankSpace + obj.Label + ".PHI" + functionParameters + \
                    obj.workingFunctionPHI + semicolon + newLine
    temp_m3d_pap += "EMISSION" + blankSpace + "HIGH_FIELD" + blankSpace + obj.constantA + blankSpace + obj.Label + ".B"\
                    + blankSpace + obj.Label + ".PHI" + newLine + tab + "MODEL" + blankSpace + obj.Label
    temp_m3d_pap += EmissionFunction().LaunchOptions(obj)
    return temp_m3d_pap


# 热致发射
def Ther(obj):
    temp_m3d_pap = ""
    temp_m3d_pap += EmissionFunction().Excursion(obj)
    functionParameters = M3DShare.getCoodinatePara()
    temp_m3d_pap += "FUNCTION" + blankSpace + obj.Label + ".WF" + functionParameters + \
                    obj.workingFunctionWF + semicolon + newLine
    temp_m3d_pap += "FUNCTION" + blankSpace + obj.Label + ".TP" + functionParameters + \
                    obj.workingTemperatureTP + semicolon + newLine
    temp_m3d_pap += "EMISSION" + blankSpace + "THERMIONIC" + blankSpace + obj.Label + ".WF" + blankSpace + obj.Label + \
                    ".TP" + newLine + tab + "MODEL" + blankSpace + obj.Label
    temp_m3d_pap += EmissionFunction().LaunchOptions(obj)
    return temp_m3d_pap


# 二次发射
def Secd(obj):
    temp_m3d_pap = ""
    # 临时变量energy,angle,便于字符串命令的拼接
    energy = ""
    angle = ""
    if obj.isEnergyDistribution:
        temp_m3d_pap += "FUNCTION" + blankSpace + "FED_" + obj.Label + "(EN) = " + obj.energyDistribution + semicolon + newLine
        energy += newLine + tab + "ENERGY_DISTRIBUTION" + blankSpace + "FED_" + obj.Label + blankSpace + \
                  obj.minimumEnergy + blankSpace + obj.maximumEnergy
    if obj.isAngularDistribution:
        temp_m3d_pap += "FUNCTION" + blankSpace + "FAD_" + obj.Label + "(CT) = " + obj.angularDistribution + semicolon + newLine
        angle += newLine + tab + "ANGLE_DISTRIBUTION" + blankSpace + "FAD_" + obj.Label
    temp_m3d_pap += "EMISSION" + blankSpace + "SECONDARY" + blankSpace + obj.maximumEmissionFactor + blankSpace + \
                    obj.maximumEmissionFactorEnergy + newLine + tab + "MODEL" + blankSpace + obj.Label
    if obj.isWeightCoefficient:
        temp_m3d_pap += newLine + tab + "WEIGHT_FACTOR" + blankSpace + obj.weightCoefficient
    temp_m3d_pap += energy + angle
    temp_m3d_pap += EmissionFunction().LaunchOptions(obj)
    return temp_m3d_pap


# 粒子设置
def Popu(obj):
    temp_m3d_pap = ""
    temp_m3d_pap += "POPULATE" + blankSpace + obj.typesOfParticles
    temp_m3d_pap += blankSpace + obj.orthogonalProjectionArea + blankSpace + obj.gridMacroParticleNumberX + blankSpace + \
                    obj.gridMacroParticleNumberY + blankSpace + obj.gridMacroParticleNumberZ + blankSpace + "FUNCTION" + \
                    blankSpace + "DENSITY" + blankSpace + obj.electricDensity + blankSpace + obj.averagelectronVelocityX + \
                    blankSpace + obj.averagelectronVelocityY + blankSpace + obj.averagelectronVelocityZ + blankSpace + \
                    "TEMPERATURE" + blankSpace + obj.temperature
    temp_m3d_pap += semicolon + newLine
    return temp_m3d_pap


# 气体电离
def Ioni(obj):
    temp_m3d = ""
    temp_m3d_pap = ""
    ioni_m3d = ""

    vol_lable = obj.ioniType
    if obj.ioniType == "未指定":
        vol_lable = obj.Label
        temp_m3d += "VOLUME" + blankSpace + obj.Label + blankSpace + "CONFORMAL"
        temp_m3d += M3DShare.PointCoordinates().point1(obj)
        temp_m3d += M3DShare.PointCoordinates().point2(obj) + semicolon + newLine

    ioni_m3d += "FUNCTION" + blankSpace + obj.GPreTimeFunction + ".F(T) = " + obj.gasPressure + semicolon
    temp_m3d_pap += "GASGAS" + blankSpace + "GASKING" + blankSpace + obj.ionizationOfGas + blankSpace + "PRESSURETM" + \
                    blankSpace + obj.GPreTimeFunction + ".F" + blankSpace + "TEMPERATURE" + blankSpace + \
                    obj.gasTemperature + blankSpace + "ACTIONAREA" + blankSpace + vol_lable + semicolon + newLine
    ioni_m3d += newLine + temp_m3d_pap
    return temp_m3d, ioni_m3d


def GasOut(obj):
    temp_m3d = ""
    direction = ""

    if obj.isNegative:
        direction = "negative"
    else:
        direction = "positive"

    temp_m3d += "OUTGAS" + blankSpace + obj.absorbVol + blankSpace + obj.density + blankSpace + obj.area + \
                blankSpace + obj.threshold + blankSpace + obj.grid + blankSpace + obj.normal + blankSpace + \
                direction + semicolon + newLine

    return temp_m3d