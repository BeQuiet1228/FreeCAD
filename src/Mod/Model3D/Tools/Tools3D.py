# -*- coding: utf8 -*-
import math
import FreeCAD
import ObjectTools
import ExpressionTools3D
import traceback
import Completer


def addCommonProperty(obj):
    """
    点线面相关的属性
    """
    obj.addProperty("App::PropertyInteger", "Order").Order = 999
    obj.addProperty("App::PropertyString", "MarkX", "NonUniformGrid", "").MarkX = "DX1"
    obj.addProperty("App::PropertyString", "MarkY", "NonUniformGrid", "").MarkY = "DX2"
    obj.addProperty("App::PropertyString", "MarkZ", "NonUniformGrid", "").MarkZ = "DX3"
    obj.addProperty("App::PropertyBool", "isMarkX", "NonUniformGrid", "").isMarkX = False
    obj.addProperty("App::PropertyBool", "isMarkY", "NonUniformGrid", "").isMarkY = False
    obj.addProperty("App::PropertyBool", "isMarkZ", "NonUniformGrid", "").isMarkZ = False
    obj.addProperty("App::PropertyBool", "isCheckMinX", "NonUniformGrid", "").isCheckMinX = False
    obj.addProperty("App::PropertyBool", "isCheckMidX", "NonUniformGrid", "").isCheckMidX = False
    obj.addProperty("App::PropertyBool", "isCheckMaxX", "NonUniformGrid", "").isCheckMaxX = False
    obj.addProperty("App::PropertyBool", "isCheckMinY", "NonUniformGrid", "").isCheckMinY = False
    obj.addProperty("App::PropertyBool", "isCheckMidY", "NonUniformGrid", "").isCheckMidY = False
    obj.addProperty("App::PropertyBool", "isCheckMaxY", "NonUniformGrid", "").isCheckMaxY = False
    obj.addProperty("App::PropertyBool", "isCheckMinZ", "NonUniformGrid", "").isCheckMinZ = False
    obj.addProperty("App::PropertyBool", "isCheckMidZ", "NonUniformGrid", "").isCheckMidZ = False
    obj.addProperty("App::PropertyBool", "isCheckMaxZ", "NonUniformGrid", "").isCheckMaxZ = False


def addCommonPropertyToObject(obj):
    """
    体相关的公共属性
    """
    obj.addProperty("App::PropertyInteger", "Order").Order = 999
    obj.addProperty("App::PropertyString", "MarkX", "NonUniformGrid", "").MarkX = "DX1"
    obj.addProperty("App::PropertyString", "MarkY", "NonUniformGrid", "").MarkY = "DX2"
    obj.addProperty("App::PropertyString", "MarkZ", "NonUniformGrid", "").MarkZ = "DX3"
    obj.addProperty("App::PropertyBool", "isMarkX", "NonUniformGrid", "").isMarkX = True
    obj.addProperty("App::PropertyBool", "isMarkY", "NonUniformGrid", "").isMarkY = True
    obj.addProperty("App::PropertyBool", "isMarkZ", "NonUniformGrid", "").isMarkZ = True
    obj.addProperty("App::PropertyBool", "isCheckMinX", "NonUniformGrid", "").isCheckMinX = False
    obj.addProperty("App::PropertyBool", "isCheckMidX", "NonUniformGrid", "").isCheckMidX = False
    obj.addProperty("App::PropertyBool", "isCheckMaxX", "NonUniformGrid", "").isCheckMaxX = False
    obj.addProperty("App::PropertyBool", "isCheckMinY", "NonUniformGrid", "").isCheckMinY = False
    obj.addProperty("App::PropertyBool", "isCheckMidY", "NonUniformGrid", "").isCheckMidY = False
    obj.addProperty("App::PropertyBool", "isCheckMaxY", "NonUniformGrid", "").isCheckMaxY = False
    obj.addProperty("App::PropertyBool", "isCheckMinZ", "NonUniformGrid", "").isCheckMinZ = False
    obj.addProperty("App::PropertyBool", "isCheckMidZ", "NonUniformGrid", "").isCheckMidZ = False
    obj.addProperty("App::PropertyBool", "isCheckMaxZ", "NonUniformGrid", "").isCheckMaxZ = False


def addAttributeToObject(obj):
    """
    为模型添加Attribute属性
    """
    # 属性
    obj.addProperty("App::PropertyString", "Attribute", "Attribute", "Conformal of Object").Attribute = "NotDefine"
    obj.addProperty("App::PropertyString", "C_SIGMA", "Attribute", "").C_SIGMA = "Isotropy"
    obj.addProperty("App::PropertyString", "RDC", "Attribute", "").RDC = "Isotropy"
    obj.addProperty("App::PropertyString", "SIGMA1", "Attribute", "").SIGMA1 = "0.05"
    obj.addProperty("App::PropertyString", "SIGMA2", "Attribute", "").SIGMA2 = "1.0"
    obj.addProperty("App::PropertyString", "SIGMA3", "Attribute", "").SIGMA3 = "1.0"
    obj.addProperty("App::PropertyString", "EPS1", "Attribute", "").EPS1 = "1.0"
    obj.addProperty("App::PropertyString", "EPS2", "Attribute", "").EPS2 = "0.0"
    obj.addProperty("App::PropertyString", "EPS3", "Attribute", "").EPS3 = "0.0"


class ViewProvider:
    def __init__(self, obj):
        ''' Set this object to the proxy object of the actual view provider '''
        # 将此对象设置为实际视图提供程序的代理对象
        obj.Proxy = self
        # obj.Transparency=0
        obj.DisplayMode = u"Flat Lines"

    def attach(self, obj):
        ''' Setup the scene sub-graph of the view provider, this method is mandatory '''
        # 设置视图提供程序的场景子图，此方法是强制性的
        return

    def updateData(self, fp, prop):
        ''' If a property of the handled feature has changed we have the chance to handle this here '''
        # 如果已处理特性的一个属性发生了改变，我们有机会在这里处理它
        return

    def getDisplayModes(self, obj):
        ''' Return a list of display modes. '''
        # 返回显示模式列表
        modes = []
        return modes

    def getDefaultDisplayMode(self):
        ''' Return the name of the default display mode. It must be defined in getDisplayModes. '''
        # 返回默认显示模式的名称。它必须在getDisplayModes中定义
        return "Flat Lines"

    def setDisplayMode(self, mode):
        ''' Map the display mode defined in attach with those defined in getDisplayModes.
        Since they have the same names nothing needs to be done. This method is optinal.
        '''
        # 将attach中定义的显示模式映射到getDisplayModes中定义的显示模式。因为它们有相同的名称，所以不需要做任何事情。此方法是可选的
        return mode

    def onChanged(self, vp, prop):
        ''' Print the name of the property that has changed '''
        # 打印已更改的属性的名称
        pass

    def getIcon(self):
        ''' Return the icon in XMP format which will appear in the tree view. This method is optional
        and if not defined a default icon is shown.
        '''
        # 返回将出现在树视图中的XMP格式图标。这个方法是可选的.如果没有定义，则显示一个默认图标
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
        # 在保存文档时，使用Python的cPickle模块存储这个对象。因为这里有一些不可选的东西——硬币之类的东西——我们必须定义这个方法
        # 返回一个包含所有可选对象或None的元组
        return

    def __setstate__(self, state):
        ''' When restoring the pickled object from document we have the chance to set some
        internals here. Since no data were pickled nothing needs to be done here.
        '''
        # 当从文档中恢复被pickle的对象时，我们有机会设置一些内部。由于没有对数据进行pickle，所以这里不需要进行任何操作
        return


def setOrderToObj(obj, ui):
    """
    将order设置到obj，如果order的顺序是不正确的，则会根据规则自动修正
    """
    curOrder = ui.spinBox_order.value()
    ObjectTools.updateWhenOrderChanged(obj, obj.Order, curOrder)


def getOrderFromObj(obj, ui):
    """
    从obj获取order属性，并将属性设置到ui上，如果obj的order远大于当前所有obj数量，则自动调整
    """
    objNumbers = len(ObjectTools.getAllObjects())
    if obj.Order > objNumbers - 1:
        ui.spinBox_order.setValue(objNumbers - 1)
    else:
        ui.spinBox_order.setValue(obj.Order)


def sayz(message):
    FreeCAD.Console.PrintError(message)
    FreeCAD.Console.PrintError("\n")


def QT_TRANSLATE_NOOP(txt, text):
    return text


def addLaunchOptionsCommonProperty(obj):
    """
    发射处理的公共属性
    """
    obj.addProperty("App::PropertyBool", "isParticleType").isParticleType = False
    obj.addProperty("App::PropertyString", "particleType").particleType = "电子"
    obj.addProperty("App::PropertyBool", "isGenerationRate").isGenerationRate = False
    obj.addProperty("App::PropertyInteger", "generationRate").generationRate = 1

    obj.addProperty("App::PropertyBool", "isFiringInterval").isFiringInterval = False
    obj.addProperty("App::PropertyBool", "isRandomDistribution").isRandomDistribution = True
    obj.addProperty("App::PropertyBool", "isStrictTiming").isStrictTiming = False
    obj.addProperty("App::PropertyInteger", "firingInterval").firingInterval = 0

    obj.addProperty("App::PropertyBool", "isSurfaceDistribution").isSurfaceDistribution = False
    obj.addProperty("App::PropertyBool", "isRandom1").isRandom1 = True
    obj.addProperty("App::PropertyBool", "isBalance1").isBalance1 = False
    obj.addProperty("App::PropertyBool", "isImmobilization1").isImmobilization1 = False

    obj.addProperty("App::PropertyBool", "isOuterSurfaceDistribution").isOuterSurfaceDistribution = False
    obj.addProperty("App::PropertyBool", "isRandom2").isRandom2 = True
    obj.addProperty("App::PropertyBool", "isImmobilization2").isImmobilization2 = False
    obj.addProperty("App::PropertyString", "excursion").excursion = "0.001"

    obj.addProperty("App::PropertyString", "launchArea1").launchArea1 = "不指定"
    obj.addProperty("App::PropertyString", "launchArea2").launchArea2 = "不指定"
    obj.addProperty("App::PropertyString", "launchOrthogonalProjectionRegin1").launchOrthogonalProjectionRegin1 = "不指定"
    obj.addProperty("App::PropertyString", "launchOrthogonalProjectionRegin2").launchOrthogonalProjectionRegin2 = "不指定"


def addCommonStartEndCoordinate(obj):
    """
    物理设置中的公共坐标属性
    """
    if FreeCAD.ActiveDocument.CoordinateSystem == "Rectangular":
        obj.addProperty("App::PropertyString", "point1_X", ).point1_X = "0mm"
        obj.addProperty("App::PropertyString", "point1_Y", ).point1_Y = "0mm"
        obj.addProperty("App::PropertyString", "point1_Z", ).point1_Z = "0mm"
        obj.addProperty("App::PropertyString", "point1_name", ).point1_name = "NULL"
        obj.addProperty("App::PropertyString", "point2_X", ).point2_X = "0mm"
        obj.addProperty("App::PropertyString", "point2_Y", ).point2_Y = "0mm"
        obj.addProperty("App::PropertyString", "point2_Z", ).point2_Z = "0mm"
        obj.addProperty("App::PropertyString", "point2_name", ).point2_name = "NULL"
    elif FreeCAD.ActiveDocument.CoordinateSystem == "Polar":
        obj.addProperty("App::PropertyString", "point1_X", ).point1_X = "0mm"
        obj.addProperty("App::PropertyString", "point1_Y", ).point1_Y = "0deg"
        obj.addProperty("App::PropertyString", "point1_Z", ).point1_Z = "0mm"
        obj.addProperty("App::PropertyString", "point1_name", ).point1_name = "NULL"
        obj.addProperty("App::PropertyString", "point2_X", ).point2_X = "0mm"
        obj.addProperty("App::PropertyString", "point2_Y", ).point2_Y = "0deg"
        obj.addProperty("App::PropertyString", "point2_Z", ).point2_Z = "0mm"
        obj.addProperty("App::PropertyString", "point2_name", ).point2_name = "NULL"
    else:
        obj.addProperty("App::PropertyString", "point1_X", ).point1_X = "0mm"
        obj.addProperty("App::PropertyString", "point1_Y", ).point1_Y = "0mm"
        obj.addProperty("App::PropertyString", "point1_Z", ).point1_Z = "0deg"
        obj.addProperty("App::PropertyString", "point1_name", ).point1_name = "NULL"
        obj.addProperty("App::PropertyString", "point2_X", ).point2_X = "0mm"
        obj.addProperty("App::PropertyString", "point2_Y", ).point2_Y = "0mm"
        obj.addProperty("App::PropertyString", "point2_Z", ).point2_Z = "0deg"
        obj.addProperty("App::PropertyString", "point2_name", ).point2_name = "NULL"

def addCommonDirection(obj):
    """
    法向属性
    """
    obj.addProperty("App::PropertyBool", "isCheckNormal1", ).isCheckNormal1 = True
    obj.addProperty("App::PropertyBool", "isCheckNormal2", ).isCheckNormal2 = False
    obj.addProperty("App::PropertyBool", "isCheckNormal3", ).isCheckNormal3 = False


def addPhysicsProperty(obj):
    """
    设置网格的属性
    """
    # Mark
    obj.addProperty("App::PropertyBool", "isMarkX", "NonUniformGrid", "").isMarkX = False
    obj.addProperty("App::PropertyBool", "isMarkY", "NonUniformGrid", "").isMarkY = False
    obj.addProperty("App::PropertyBool", "isMarkZ", "NonUniformGrid", "").isMarkZ = False
    obj.addProperty("App::PropertyString", "MarkX", "NonUniformGrid", "").MarkX = "DX1"
    obj.addProperty("App::PropertyString", "MarkY", "NonUniformGrid", "").MarkY = "DX2"
    obj.addProperty("App::PropertyString", "MarkZ", "NonUniformGrid", "").MarkZ = "DX3"


def isNegativeOrPositive(obj):
    """
    设置正反向属性
    """
    obj.addProperty("App::PropertyBool", "isNegative").isNegative = False
    obj.addProperty("App::PropertyBool", "isPositive").isPositive = True


def addUserProperty(obj, num):
    """
    为obj添加user_xxx属性，该属性直接存储用户的输入信息
    :param obj: FreeCAD对象
    :param num: 添加属性的数量
    :return: None
    """
    if num > 0:
        # 从1开始命名
        for i in range(num):
            obj.addProperty("App::PropertyString", "user_point" + str(i+1) + "_x")
            obj.addProperty("App::PropertyString", "user_point" + str(i+1) + "_y")
            obj.addProperty("App::PropertyString", "user_point" + str(i+1) + "_z")


def getCoordinate():
    """
    获取坐标系的标签
    """
    coordinate = FreeCAD.ActiveDocument.CoordinateSystem
    if coordinate == u'Rectangular':
        unitList = ["X", "Y", "Z", "m", "m", "m"]
    elif coordinate == u"Polar":
        unitList = ["R", u"Theta", "Z", "m", "deg", "m"]
    else:
        unitList = ["Z", "R", u"Theta", "m", "m", "deg"]
    return unitList


def switchPointLabel(ui):
    """
    通过选择的坐标系转换点坐标的标签
    """
    coord = getCoordinate()
    x1 = coord[0]
    y1 = coord[1]
    z1 = coord[2]
    ui.label_X.setText(x1)
    ui.label_Y.setText(y1)
    ui.label_Z.setText(z1)


def switchPointLabel_BaseModel(ui):
    """
    BaseUI的点坐标标签名为label_x1, label_y1, label_z1
    通过选择的坐标系转换点坐标的标签
    """
    coord = getCoordinate()
    x1 = coord[0]
    y1 = coord[1]
    z1 = coord[2]
    ui.label_x1.setText(x1)
    ui.label_y1.setText(y1)
    ui.label_z1.setText(z1)


def switchPointLabel_Model(ui):
    """
    Model的坐标标签名为label_x2, label_y2, label_z2
    通过选择的坐标系转换点坐标的标签
    """
    coord = getCoordinate()
    x1 = coord[0]
    y1 = coord[1]
    z1 = coord[2]
    ui.label_x2.setText(x1)
    ui.label_y2.setText(y1)
    ui.label_z2.setText(z1)


def switchRadioButtonLabel(ui):
    """
    通过选择的坐标系转换法向按钮的标签
    """
    coord = getCoordinate()
    x1 = coord[0]
    y1 = coord[1]
    z1 = coord[2]
    ui.radioButton_x.setText(x1)
    ui.radioButton_y.setText(y1)
    ui.radioButton_z.setText(z1)


def switchCheckLabel(ui):
    """
    通过选择的坐标系转换网格的标签
    """
    coord = getCoordinate()
    x1 = coord[0]
    y1 = coord[1]
    z1 = coord[2]
    ui.checkBox_x.setText(x1)
    ui.checkBox_y.setText(y1)
    ui.checkBox_z.setText(z1)


def setCoordEnabled(ui, curType):
    """
    根据传入的点，线，面，体，设置控件的可编辑状态
    """
    ui.LineEdit_start_x.setEnabled(True)
    ui.LineEdit_start_y.setEnabled(True)
    ui.LineEdit_start_z.setEnabled(True)
    if curType == ObjectTools.ObjectType.Point:
        ui.LineEdit_end_x.setEnabled(False)
        ui.LineEdit_end_y.setEnabled(False)
        ui.LineEdit_end_z.setEnabled(False)
        ui.radioButton_x.setEnabled(False)
        ui.radioButton_y.setEnabled(False)
        ui.radioButton_z.setEnabled(False)
    elif curType == ObjectTools.ObjectType.Line_Conformal:
        ui.LineEdit_end_x.setEnabled(ui.radioButton_x.isChecked())
        ui.LineEdit_end_y.setEnabled(ui.radioButton_y.isChecked())
        ui.LineEdit_end_z.setEnabled(ui.radioButton_z.isChecked())
        ui.radioButton_x.setEnabled(True)
        ui.radioButton_y.setEnabled(True)
        ui.radioButton_z.setEnabled(True)
    elif curType == ObjectTools.ObjectType.Area_Conformal:
        ui.LineEdit_end_x.setEnabled(not ui.radioButton_x.isChecked())
        ui.LineEdit_end_y.setEnabled(not ui.radioButton_y.isChecked())
        ui.LineEdit_end_z.setEnabled(not ui.radioButton_z.isChecked())
        ui.radioButton_x.setEnabled(True)
        ui.radioButton_y.setEnabled(True)
        ui.radioButton_z.setEnabled(True)
    elif curType == ObjectTools.ObjectType.Vol_Conformal:
        ui.LineEdit_end_x.setEnabled(True)
        ui.LineEdit_end_y.setEnabled(True)
        ui.LineEdit_end_z.setEnabled(True)
        if hasattr(ui, "radioButton_z"):
            ui.radioButton_x.setEnabled(False)
            ui.radioButton_y.setEnabled(False)
            ui.radioButton_z.setEnabled(False)


def setIsEdit(ui, isEdit):
    """
    设置ui控件可编辑状态
    """
    ui.LineEdit_start_x.setEnabled(isEdit)
    ui.LineEdit_start_y.setEnabled(isEdit)
    ui.LineEdit_start_z.setEnabled(isEdit)
    ui.LineEdit_end_x.setEnabled(isEdit)
    ui.LineEdit_end_y.setEnabled(isEdit)
    ui.LineEdit_end_z.setEnabled(isEdit)
    if hasattr(ui, "radioButton_x"):
        ui.radioButton_x.setEnabled(isEdit)
        ui.radioButton_y.setEnabled(isEdit)
        ui.radioButton_z.setEnabled(isEdit)


def setModelCoordinate(ui, objName):
    """
    通过传入的名字，获取点，线，面，体的obj,并把obj的坐标设置到ui中
    """
    modelObj = ObjectTools.getObjByLabel(objName)
    ui.LineEdit_start_x.setText(str(modelObj.user_point1_x).replace(' ', ''))
    ui.LineEdit_start_y.setText(str(modelObj.user_point1_y).replace(' ', ''))
    ui.LineEdit_start_z.setText(str(modelObj.user_point1_z).replace(' ', ''))
    if hasattr(modelObj, "Point2X"):
        ui.LineEdit_end_x.setText(str(modelObj.user_point2_x).replace(' ', ''))
        ui.LineEdit_end_y.setText(str(modelObj.user_point2_y).replace(' ', ''))
        ui.LineEdit_end_z.setText(str(modelObj.user_point2_z).replace(' ', ''))
    # 获取当前坐标系及坐标系单位
    coord = getCoordinate()
    if hasattr(modelObj, "Normal"):
        if modelObj.Normal == coord[0]:
            ui.radioButton_x.setChecked(True)
        elif modelObj.Normal == coord[1]:
            ui.radioButton_y.setChecked(True)
        else:
            ui.radioButton_z.setChecked(True)


def setCoorToUI(ui, obj):
    """
    设置obj的坐标到ui
    """
    ui.LineEdit_start_x.setText(obj.point1_X)
    ui.LineEdit_start_y.setText(obj.point1_Y)
    ui.LineEdit_start_z.setText(obj.point1_Z)
    ui.LineEdit_end_x.setText(obj.point2_X)
    ui.LineEdit_end_y.setText(obj.point2_Y)
    ui.LineEdit_end_z.setText(obj.point2_Z)


def setGridToUI(ui, obj):
    """
    设置非均匀网格到ui中
    """
    ui.checkBox_x.setChecked(obj.isMarkX)
    ui.checkBox_y.setChecked(obj.isMarkY)
    ui.checkBox_z.setChecked(obj.isMarkZ)
    ui.LineEdit_DX1.setText(obj.MarkX)
    ui.LineEdit_DX2.setText(obj.MarkY)
    ui.LineEdit_DX3.setText(obj.MarkZ)


def getUICoordinate(obj, ui):
    """
    从ui中读取坐标到obj
    """
    obj.point1_X = ui.LineEdit_start_x.text()
    obj.point1_Y = ui.LineEdit_start_y.text()
    obj.point1_Z = ui.LineEdit_start_z.text()
    obj.point2_X = ui.LineEdit_end_x.text()
    obj.point2_Y = ui.LineEdit_end_y.text()
    obj.point2_Z = ui.LineEdit_end_z.text()


def getUIGrid(obj, ui):
    """
    获取ui的非均匀网格，设置到obj中
    """
    obj.isMarkX = ui.checkBox_x.isChecked()
    obj.isMarkY = ui.checkBox_y.isChecked()
    obj.isMarkZ = ui.checkBox_z.isChecked()
    obj.MarkX = ui.LineEdit_DX1.text()
    obj.MarkY = ui.LineEdit_DX2.text()
    obj.MarkZ = ui.LineEdit_DX3.text()


def getUIRadioButton(obj, ui):
    """
    获取ui的法向按钮，设置到obj中
    """
    obj.isCheckNormal1 = ui.radioButton_x.isChecked()
    obj.isCheckNormal2 = ui.radioButton_y.isChecked()
    obj.isCheckNormal3 = ui.radioButton_z.isChecked()


def setRadioButtonToUI(ui, obj):
    """
    设置法向按钮到ui中
    """
    ui.radioButton_x.setChecked(obj.isCheckNormal1)
    ui.radioButton_y.setChecked(obj.isCheckNormal2)
    ui.radioButton_z.setChecked(obj.isCheckNormal3)


def setPlaceToObj(obj, attr, place_str="0"):
    """
    获取UI信息，然后对字符串处理，并将处理后的值添加到obj
    """
    place = ExpressionTools3D.processingLengthExpression(place_str)
    # temp = ExpressionTools3D.parseExpressionStr(place_str)
    # place = ExpressionTools3D.processingLengthExpression(temp)
    try:
        # if True:

        obj.setExpression(attr, None)
        obj.setExpression(attr, place)
        obj.setExpression(attr, place)
    except:
        sayz(obj.Label + "--属性：  " + attr + "   坐标:   " + str(place))
        sayz(traceback.format_exc())
        return "error"
    else:
        return None


def addHelperProperty(obj, num):
    """
        为obj添加user_xxx属性，该属性直接存储用户的输入信息
        :param obj: FreeCAD对象
        :param num: 添加属性的数量
        :return: None
        """
    if num > 0:
        # 从1开始命名
        for i in range(num):
            obj.addProperty("App::PropertyString", "user_point" + str(i + 1) + "_x")
            obj.addProperty("App::PropertyString", "user_point" + str(i + 1) + "_y")
            obj.addProperty("App::PropertyString", "user_point" + str(i + 1) + "_z")
            if FreeCAD.ActiveDocument.CoordinateSystem == 'Rectangular':
                setattr(obj, "user_point" + str(i + 1) + "_x", "0mm")
                setattr(obj, "user_point" + str(i + 1) + "_y", "0mm")
                setattr(obj, "user_point" + str(i + 1) + "_z", "0mm")
            elif FreeCAD.ActiveDocument.CoordinateSystem == 'Polar':
                setattr(obj, "user_point" + str(i + 1) + "_x", "0mm")
                setattr(obj, "user_point" + str(i + 1) + "_y", "0deg")
                setattr(obj, "user_point" + str(i + 1) + "_z", "0mm")
            else:
                setattr(obj, "user_point" + str(i + 1) + "_x", "0mm")
                setattr(obj, "user_point" + str(i + 1) + "_y", "0mm")
                setattr(obj, "user_point" + str(i + 1) + "_z", "0deg")


def getHelperValue(obj):
    length = ExpressionTools3D.currentLengthUnits()
    angle = ExpressionTools3D.currentAngleUnits()
    if FreeCAD.ActiveDocument.CoordinateSystem == "Rectangular":
        obj.user_point1_x = str(obj.Point1X.getValueAs(length)) + length
        obj.user_point1_y = str(obj.Point1Y.getValueAs(length)) + length
        obj.user_point1_z = str(obj.Point1Z.getValueAs(length)) + length
        if hasattr(obj, "Point2X") and hasattr(obj, "user_point2_x"):
            obj.user_point2_x = str(obj.Point2X.getValueAs(length)) + length
            obj.user_point2_y = str(obj.Point2Y.getValueAs(length)) + length
            obj.user_point2_z = str(obj.Point2Z.getValueAs(length)) + length
        if hasattr(obj, "Point3X") and hasattr(obj, "user_point3_x"):
            obj.user_point3_x = str(obj.Point3X.getValueAs(length)) + length
            obj.user_point3_y = str(obj.Point3Y.getValueAs(length)) + length
            obj.user_point3_z = str(obj.Point3Z.getValueAs(length)) + length
        if hasattr(obj, "Point4X") and hasattr(obj, "user_point4_x"):
            obj.user_point4_x = str(obj.Point4X.getValueAs(length)) + length
            obj.user_point4_y = str(obj.Point4Y.getValueAs(length)) + length
            obj.user_point4_z = str(obj.Point4Z.getValueAs(length)) + length
        if hasattr(obj, "Point5X") and hasattr(obj, "user_point5_x"):
            obj.user_point5_x = str(obj.Point5X.getValueAs(length)) + length
            obj.user_point5_y = str(obj.Point5Y.getValueAs(length)) + length
            obj.user_point5_z = str(obj.Point5Z.getValueAs(length)) + length
        if hasattr(obj, "Point6X") and hasattr(obj, "user_point6_x"):
            obj.user_point6_x = str(obj.Point6X.getValueAs(length)) + length
            obj.user_point6_y = str(obj.Point6Y.getValueAs(length)) + length
            obj.user_point6_z = str(obj.Point6Z.getValueAs(length)) + length
        if hasattr(obj, "Point7X") and hasattr(obj, "user_point7_x"):
            obj.user_point7_x = str(obj.Point7X.getValueAs(length)) + length
            obj.user_point7_y = str(obj.Point7Y.getValueAs(length)) + length
            obj.user_point7_z = str(obj.Point7Z.getValueAs(length)) + length
        if hasattr(obj, "Point8X") and hasattr(obj, "user_point8_x"):
            obj.user_point8_x = str(obj.Point8X.getValueAs(length)) + length
            obj.user_point8_y = str(obj.Point8Y.getValueAs(length)) + length
            obj.user_point8_z = str(obj.Point8Z.getValueAs(length)) + length

    elif FreeCAD.ActiveDocument.CoordinateSystem == "Polar":
        obj.user_point1_x = str(obj.Point1X.getValueAs(length)) + length
        obj.user_point1_y = str(obj.Point1Y.getValueAs(angle)) + angle
        obj.user_point1_z = str(obj.Point1Z.getValueAs(length)) + length
        if hasattr(obj, "Point2X") and hasattr(obj, "user_point2_x"):
            obj.user_point2_x = str(obj.Point2X.getValueAs(length)) + length
            obj.user_point2_y = str(obj.Point2Y.getValueAs(angle)) + angle
            obj.user_point2_z = str(obj.Point2Z.getValueAs(length)) + length
        if hasattr(obj, "Point3X") and hasattr(obj, "user_point3_x"):
            obj.user_point3_x = str(obj.Point3X.getValueAs(length)) + length
            obj.user_point3_y = str(obj.Point3Y.getValueAs(angle)) + angle
            obj.user_point3_z = str(obj.Point3Z.getValueAs(length)) + length
        if hasattr(obj, "Point4X") and hasattr(obj, "user_point4_x"):
            obj.user_point4_x = str(obj.Point4X.getValueAs(length)) + length
            obj.user_point4_y = str(obj.Point4Y.getValueAs(angle)) + angle
            obj.user_point4_z = str(obj.Point4Z.getValueAs(length)) + length
        if hasattr(obj, "Point5X") and hasattr(obj, "user_point5_x"):
            obj.user_point5_x = str(obj.Point5X.getValueAs(length)) + length
            obj.user_point5_y = str(obj.Point5Y.getValueAs(angle)) + angle
            obj.user_point5_z = str(obj.Point5Z.getValueAs(length)) + length
        if hasattr(obj, "Point6X") and hasattr(obj, "user_point6_x"):
            obj.user_point6_x = str(obj.Point6X.getValueAs(length)) + length
            obj.user_point6_y = str(obj.Point6Y.getValueAs(angle)) + angle
            obj.user_point6_z = str(obj.Point6Z.getValueAs(length)) + length
        if hasattr(obj, "Point7X") and hasattr(obj, "user_point7_x"):
            obj.user_point7_x = str(obj.Point7X.getValueAs(length)) + length
            obj.user_point7_y = str(obj.Point7Y.getValueAs(angle)) + angle
            obj.user_point7_z = str(obj.Point7Z.getValueAs(length)) + length
        if hasattr(obj, "Point8X") and hasattr(obj, "user_point8_x"):
            obj.user_point8_x = str(obj.Point8X.getValueAs(length)) + length
            obj.user_point8_y = str(obj.Point8Y.getValueAs(angle)) + angle
            obj.user_point8_z = str(obj.Point8Z.getValueAs(length)) + length

    else:
        obj.user_point1_x = str(obj.Point1X.getValueAs(length)) + length
        obj.user_point1_y = str(obj.Point1Y.getValueAs(length)) + length
        obj.user_point1_z = str(obj.Point1Z.getValueAs(angle)) + angle
        if hasattr(obj, "Point2X") and hasattr(obj, "user_point2_x"):
            obj.user_point2_x = str(obj.Point2X.getValueAs(length)) + length
            obj.user_point2_y = str(obj.Point2Y.getValueAs(length)) + length
            obj.user_point2_z = str(obj.Point2Z.getValueAs(angle)) + angle
        if hasattr(obj, "Point3X") and hasattr(obj, "user_point3_x"):
            obj.user_point3_x = str(obj.Point3X.getValueAs(length)) + length
            obj.user_point3_y = str(obj.Point3Y.getValueAs(length)) + length
            obj.user_point3_z = str(obj.Point3Z.getValueAs(angle)) + angle
        if hasattr(obj, "Point4X") and hasattr(obj, "user_point4_x"):
            obj.user_point4_x = str(obj.Point4X.getValueAs(length)) + length
            obj.user_point4_y = str(obj.Point4Y.getValueAs(length)) + length
            obj.user_point4_z = str(obj.Point4Z.getValueAs(angle)) + angle
        if hasattr(obj, "Point5X") and hasattr(obj, "user_point5_x"):
            obj.user_point5_x = str(obj.Point5X.getValueAs(length)) + length
            obj.user_point5_y = str(obj.Point5Y.getValueAs(length)) + length
            obj.user_point5_z = str(obj.Point5Z.getValueAs(angle)) + angle
        if hasattr(obj, "Point6X") and hasattr(obj, "user_point6_x"):
            obj.user_point6_x = str(obj.Point6X.getValueAs(length)) + length
            obj.user_point6_y = str(obj.Point6Y.getValueAs(length)) + length
            obj.user_point6_z = str(obj.Point6Z.getValueAs(angle)) + angle
        if hasattr(obj, "Point7X") and hasattr(obj, "user_point7_x"):
            obj.user_point7_x = str(obj.Point7X.getValueAs(length)) + length
            obj.user_point7_y = str(obj.Point7Y.getValueAs(length)) + length
            obj.user_point7_z = str(obj.Point7Z.getValueAs(angle)) + angle
        if hasattr(obj, "Point8X") and hasattr(obj, "user_point8_x"):
            obj.user_point8_x = str(obj.Point8X.getValueAs(length)) + length
            obj.user_point8_y = str(obj.Point8Y.getValueAs(length)) + length
            obj.user_point8_z = str(obj.Point8Z.getValueAs(angle)) + angle


def addRadiusProperty(obj):
    """
    圆柱体，环形体，圆台体，球体，圆环区域体，环形区域体，螺旋体
    增加辅助半径属性
    """
    if obj.Type == ObjectTools.ObjectType.Vol_Cylinder:
        obj.addProperty("App::PropertyString", "user_radius1")
    elif obj.Type == ObjectTools.ObjectType.Vol_Annular:
        obj.addProperty("App::PropertyString", "user_radius1")
        obj.addProperty("App::PropertyString", "user_radius2")
    elif obj.Type == ObjectTools.ObjectType.Vol_SpecialCone:
        obj.addProperty("App::PropertyString", "user_radius1")
        obj.addProperty("App::PropertyString", "user_radius2")
    elif obj.Type == ObjectTools.ObjectType.Vol_Annular_Section:
        obj.addProperty("App::PropertyString", "user_radius1")
        obj.addProperty("App::PropertyString", "user_radius2")
    elif obj.Type == ObjectTools.ObjectType.Vol_Toroidal_Section:
        obj.addProperty("App::PropertyString", "user_radius1")
        obj.addProperty("App::PropertyString", "user_radius2")
    elif obj.Type == ObjectTools.ObjectType.Vol_Spherical:
        obj.addProperty("App::PropertyString", "user_radius1")


def getRadiusProperty(obj):
    """
    圆柱体，环形体，圆台体，球体，圆环区域体，环形区域体，螺旋体
    获取辅助半径属性
    """
    length = ExpressionTools3D.currentLengthUnits()
    if obj.Type == ObjectTools.ObjectType.Vol_Cylinder:
        obj.user_radius1 = str(obj.Radius.getValueAs(length)) + length
    elif obj.Type == ObjectTools.ObjectType.Vol_Annular:
        obj.user_radius1 = str(obj.Radius1.getValueAs(length)) + length
        obj.user_radius2 = str(obj.Radius2.getValueAs(length)) + length
    elif obj.Type == ObjectTools.ObjectType.Vol_SpecialCone:
        obj.user_radius1 = str(obj.Radius_Bottom.getValueAs(length)) + length
        obj.user_radius2 = str(obj.Radius_Top.getValueAs(length)) + length
    elif obj.Type == ObjectTools.ObjectType.Vol_Annular_Section:
        obj.user_radius1 = str(obj.InnerRadius.getValueAs(length)) + length
        obj.user_radius2 = str(obj.OuterRadius.getValueAs(length)) + length
    elif obj.Type == ObjectTools.ObjectType.Vol_Toroidal_Section:
        obj.user_radius1 = str(obj.MajorRadius.getValueAs(length)) + length
        obj.user_radius2 = str(obj.MinorRadius.getValueAs(length)) + length
    elif obj.Type == ObjectTools.ObjectType.Vol_Spherical:
        obj.user_radius1 = str(obj.Radius.getValueAs(length)) + length


def addHeHelperProperty(obj):
    for i in range(3):
        obj.addProperty("App::PropertyString", "user_point" + str(i + 1) + "_x")
        obj.addProperty("App::PropertyString", "user_point" + str(i + 1) + "_y")
        obj.addProperty("App::PropertyString", "user_point" + str(i + 1) + "_z")
    obj.addProperty("App::PropertyString", "user_radius1")
    obj.addProperty("App::PropertyString", "user_radius2")
    obj.addProperty("App::PropertyString", "user_pitch")
    obj.addProperty("App::PropertyString", "user_width")


def getHeHelperValue(obj):
    length = ExpressionTools3D.currentLengthUnits()
    angle = ExpressionTools3D.currentAngleUnits()
    if FreeCAD.ActiveDocument.CoordinateSystem == "Rectangular":
        obj.user_point1_x = str(obj.PointBaseX.getValueAs(length)) + length
        obj.user_point1_y = str(obj.PointBaseY.getValueAs(length)) + length
        obj.user_point1_z = str(obj.PointBaseZ.getValueAs(length)) + length
        obj.user_point2_x = str(obj.PointTopX.getValueAs(length)) + length
        obj.user_point2_y = str(obj.PointTopY.getValueAs(length)) + length
        obj.user_point2_z = str(obj.PointTopZ.getValueAs(length)) + length
        obj.user_point3_x = str(obj.PointStartX.getValueAs(length)) + length
        obj.user_point3_y = str(obj.PointStartY.getValueAs(length)) + length
        obj.user_point3_z = str(obj.PointStartZ.getValueAs(length)) + length
    elif FreeCAD.ActiveDocument.CoordinateSystem == "Polar":
        obj.user_point1_x = str(obj.PointBaseX.getValueAs(length)) + length
        obj.user_point1_y = str(obj.PointBaseY.getValueAs(angle)) + angle
        obj.user_point1_z = str(obj.PointBaseZ.getValueAs(length)) + length
        obj.user_point2_x = str(obj.PointTopX.getValueAs(length)) + length
        obj.user_point2_y = str(obj.PointTopY.getValueAs(angle)) + angle
        obj.user_point2_z = str(obj.PointTopZ.getValueAs(length)) + length
        obj.user_point3_x = str(obj.PointStartX.getValueAs(length)) + length
        obj.user_point3_y = str(obj.PointStartY.getValueAs(angle)) + angle
        obj.user_point3_z = str(obj.PointStartZ.getValueAs(length)) + length
    else:
        obj.user_point1_x = str(obj.PointBaseX.getValueAs(length)) + length
        obj.user_point1_y = str(obj.PointBaseY.getValueAs(length)) + length
        obj.user_point1_z = str(obj.PointBaseZ.getValueAs(angle)) + angle
        obj.user_point2_x = str(obj.PointTopX.getValueAs(length)) + length
        obj.user_point2_y = str(obj.PointTopY.getValueAs(length)) + length
        obj.user_point2_z = str(obj.PointTopZ.getValueAs(angle)) + angle
        obj.user_point3_x = str(obj.PointStartX.getValueAs(length)) + length
        obj.user_point3_y = str(obj.PointStartY.getValueAs(length)) + length
        obj.user_point3_z = str(obj.PointStartZ.getValueAs(angle)) + angle

    obj.user_radius1 = str(obj.RadiusInside.getValueAs(length)) + length
    obj.user_radius2 = str(obj.RadiusOut.getValueAs(length)) + length
    obj.user_pitch = str(obj.Pitch.getValueAs(length)) + length
    obj.user_width = str(obj.Width.getValueAs(length)) + length


def defaultSettingForPolygonal(obj):
    """
    为多边形设置user_xxx的默认值
    :param obj:
    :return:
    """
    for i in range(obj.NumbersOfPoints):
        pos = getattr(obj, "Point" + str(i+1))
        setattr(obj, "user_point" + str(i + 1) + "_x", str(pos[0]) + "m")
        setattr(obj, "user_point" + str(i + 1) + "_y", str(pos[1]) + "m")
        setattr(obj, "user_point" + str(i + 1) + "_z", str(pos[2]) + "m")


def getHelperValueWithPoly(obj):
    length = ExpressionTools3D.currentLengthUnits()
    for i in range(obj.NumbersOfPoints):
        pos = getattr(obj, "Point" + str(i+1))
        setattr(obj, "user_point" + str(i + 1) + "_x", str(pos[0].getValueAs(length)) + length)
        setattr(obj, "user_point" + str(i + 1) + "_y", str(pos[1].getValueAs(length)) + length)
        setattr(obj, "user_point" + str(i + 1) + "_z", str(pos[2].getValueAs(length)) + length)


def getHelperValueWith(obj):
        length = ExpressionTools3D.currentLengthUnits()
        angle = ExpressionTools3D.currentAngleUnits()
        if FreeCAD.ActiveDocument.CoordinateSystem == "Rectangular":
            obj.user_point1_x = str(obj.user_point1_x.getValueAs(length)) + length
            obj.user_point1_y = str(obj.user_point1_y.getValueAs(length)) + length
            obj.user_point1_z = str(obj.user_point1_z.getValueAs(length)) + length
            if hasattr(obj, "Point2X") and hasattr(obj, "user_point2_x"):
                obj.user_point2_x = str(obj.user_point2_x.getValueAs(length)) + length
                obj.user_point2_y = str(obj.user_point2_y.getValueAs(length)) + length
                obj.user_point2_z = str(obj.user_point2_z.getValueAs(length)) + length
            if hasattr(obj, "Point3X") and hasattr(obj, "user_point3_x"):
                obj.user_point3_x = str(obj.user_point3_x.getValueAs(length)) + length
                obj.user_point3_y = str(obj.user_point3_y.getValueAs(length)) + length
                obj.user_point3_z = str(obj.user_point3_z.getValueAs(length)) + length
            if hasattr(obj, "Point4X") and hasattr(obj, "user_point4_x"):
                obj.user_point4_x = str(obj.user_point4_x.getValueAs(length)) + length
                obj.user_point4_y = str(obj.user_point4_y.getValueAs(length)) + length
                obj.user_point4_z = str(obj.user_point4_z.getValueAs(length)) + length
            if hasattr(obj, "Point5X") and hasattr(obj, "user_point5_x"):
                obj.user_point5_x = str(obj.user_point5_x.getValueAs(length)) + length
                obj.user_point5_y = str(obj.user_point5_y.getValueAs(length)) + length
                obj.user_point5_z = str(obj.user_point5_z.getValueAs(length)) + length
            if hasattr(obj, "Point6X") and hasattr(obj, "user_point6_x"):
                obj.user_point6_x = str(obj.user_point6_x.getValueAs(length)) + length
                obj.user_point6_y = str(obj.user_point6_y.getValueAs(length)) + length
                obj.user_point6_z = str(obj.user_point6_z.getValueAs(length)) + length
            if hasattr(obj, "Point7X") and hasattr(obj, "user_point7_x"):
                obj.user_point7_x = str(obj.user_point7_x.getValueAs(length)) + length
                obj.user_point7_y = str(obj.user_point7_y.getValueAs(length)) + length
                obj.user_point7_z = str(obj.user_point7_z.getValueAs(length)) + length
            if hasattr(obj, "Point8X") and hasattr(obj, "user_point8_x"):
                obj.user_point8_x = str(obj.user_point8_x.getValueAs(length)) + length
                obj.user_point8_y = str(obj.user_point8_y.getValueAs(length)) + length
                obj.user_point8_z = str(obj.user_point8_z.getValueAs(length)) + length


def transToRecVector(x, y, z):
    """
    将点的坐标转化为直角坐标系下的坐标，返回直角坐标系下的Vector，用以FreeCAD建模
    :param x:
    :param y:
    :param z:
    :return: FreeCAD.Vector
    """
    coordinateType = FreeCAD.ActiveDocument.CoordinateSystem
    if coordinateType == 'Rectangular':
        # point格式：(X,Y,Z)
        return FreeCAD.Vector(x, y, z)
    elif coordinateType == 'Polar':
        # point格式：(R,θ,Z)
        pX = x * math.cos(y % 360 * math.pi / 180.0)
        pY = x * math.sin(y % 360 * math.pi / 180.0)
        pZ = z
        return FreeCAD.Vector(pX, pY, pZ)
    elif coordinateType == 'Cylindrical':
        # point格式：(Z,R,θ)
        pX = y * math.cos(z % 360 * math.pi / 180.0)
        pY = y * math.sin(z % 360 * math.pi / 180.0)
        pZ = x
        return FreeCAD.Vector(pX, pY, pZ)
    else:
        sayz("Coordinate switch wrong!")


def pointToRecVec(vec):
    """
    Vector转化为直角坐标系下Vector并返回
    :param vec:
    :return FreeCAD.Vector:
    """
    coordinateType = FreeCAD.ActiveDocument.CoordinateSystem
    if coordinateType == 'Rectangular':
        return vec
    elif coordinateType == 'Polar':
        pX = vec.x * math.cos(vec.y * math.pi / 180.0)
        pY = vec.x * math.sin(vec.y * math.pi / 180.0)
        pZ = vec.z
        return FreeCAD.Vector(pX, pY, pZ)
    elif coordinateType == 'Cylindrical':
        pX = vec.y * math.cos(vec.z * math.pi / 180.0)
        pY = vec.y * math.sin(vec.z * math.pi / 180.0)
        pZ = vec.x
        return FreeCAD.Vector(pX, pY, pZ)
    else:
        sayz("Coordinate switch wrong!")


def setLineEditsCompleter(lineEdits):
    '''
    @brief:为lineEdits列表里的LineEdit对象添加补全list
    '''
    for lineEdit in lineEdits:
        lineEdit.setcompleterlist(getParamsList())


def getParamsList():
    '''
    @brief:获得参数体的所有参数以及步长参数
    '''
    paramObj = FreeCAD.ActiveDocument.getObject("Param")
    if paramObj is None:
        return []
    params = paramObj.PropertiesList
    # paramsExtra = ["DX1", "DX2", "DX3"]
    # paramsList = params + paramsExtra
    paramsList = params
    return paramsList


def getAllLineEdits(ui):
    '''
    @brief:获得UI中的所有LineEdit控件对象list
    '''
    lineEdits=[]
    for attr in dir(ui):
        if isinstance(getattr(ui, attr), Completer.AutoCompleteEdit):
            lineEdits.append(getattr(ui,attr))
    return lineEdits


def setLabel(name):
    """
    名字只能以字母开头
    """
    while not name[0].isalpha():
        name = name[1:]
        if len(name) == 0:
            break
        setLabel(name)
    name = str(name).replace(' ', '')
    return name
