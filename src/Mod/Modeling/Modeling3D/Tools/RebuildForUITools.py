# -*- coding: UTF-8 -*-
from Modeling.Common.Tools import CoordinateSystemTools,ObjectsTools
def fillUniformGridByObj(ui,obj):
    '''
    @ brief 根据obj对象填入非均匀网格数据
    @ param :ui填入的ui界面
    @ param :obj对象
    @ return None
    '''
    currentCoordinate=obj.Document.CoordinateSystem

    if currentCoordinate==CoordinateSystemTools.CoordinateType.Rectangular:
        #填入非均匀网格属性
        ui.checkBox_UniformX.setChecked(obj.X)
        ui.checkBox_UniformY.setChecked(obj.Y)
        ui.checkBox_UniformZ.setChecked(obj.Z)

        ui.lineEdit_UniformX.setText(ObjectsTools.turnPropertyToExpression(obj,"X_Value"))
        ui.lineEdit_UniformY.setText(ObjectsTools.turnPropertyToExpression(obj,"Y_Value"))
        ui.lineEdit_UniformZ.setText(ObjectsTools.turnPropertyToExpression(obj,"Z_Value"))
    elif currentCoordinate==CoordinateSystemTools.CoordinateType.Polar:
        #填入非均匀网格属性
        ui.checkBox_UniformX.setChecked(obj.R)
        ui.checkBox_UniformY.setChecked(obj.Theta)
        ui.checkBox_UniformZ.setChecked(obj.Z)

        ui.lineEdit_UniformX.setText(ObjectsTools.turnPropertyToExpression(obj,"R_Value"))
        ui.lineEdit_UniformY.setText(ObjectsTools.turnPropertyToExpression(obj,"Theta_Value"))
        ui.lineEdit_UniformZ.setText(ObjectsTools.turnPropertyToExpression(obj,"Z_Value"))                
    elif currentCoordinate==CoordinateSystemTools.CoordinateType.Cylindrical:
        #填入非均匀网格属性
        ui.checkBox_UniformX.setChecked(obj.Z)
        ui.checkBox_UniformY.setChecked(obj.R)
        ui.checkBox_UniformZ.setChecked(obj.Theta)

        ui.lineEdit_UniformX.setText(ObjectsTools.turnPropertyToExpression(obj,"Z_Value"))
        ui.lineEdit_UniformY.setText(ObjectsTools.turnPropertyToExpression(obj,"R_Value"))
        ui.lineEdit_UniformZ.setText(ObjectsTools.turnPropertyToExpression(obj,"Theta_Value"))

def getCoordinateName(coordinate):
    '''
    :param coordinate: 输入当前界面的坐标
    :return:返回一个含有三个元素的坐标列表
    '''
    Coordi_Name=[]
    if coordinate == CoordinateSystemTools.CoordinateType.Rectangular:
        Coordi_Name=["X","Y","Z"]
    elif coordinate == CoordinateSystemTools.CoordinateType.Polar:
        Coordi_Name=["R","Theta","Z"]
    elif coordinate == CoordinateSystemTools.CoordinateType.Cylindrical:
        Coordi_Name=["Z","R","Theta"]

    return Coordi_Name