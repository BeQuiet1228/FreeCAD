# -*- coding: UTF-8 -*-
from Modeling.Common.Tools import CoordinateSystemTools,ObjectsTools
import FreeCAD
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
def fillUniformGridToObj(ui, obj):
    '''
    @ brief 根据非均匀网格数据填入obj对象
    @ param :ui填入的ui界面
    @ param :obj对象
    @ return None
    '''
    from Modeling.Common.Tools import InputTools
    mark_x_bool = ui.checkBox_UniformX.isChecked()
    mark_y_bool = ui.checkBox_UniformY.isChecked()
    mark_z_bool = ui.checkBox_UniformZ.isChecked()

    Fx = ui.lineEdit_UniformX.text()
    Fy = ui.lineEdit_UniformY.text()
    Fz = ui.lineEdit_UniformZ.text()
    if FreeCAD.ActiveDocument.CoordinateSystem == "Rectangular":
        if mark_x_bool:
            Fx_1 = InputTools.Stringfunctions(Fx)
            try:
                obj.setExpression('X_Value',None)
                obj.setExpression('X_Value', str(Fx_1[0]))
            except:
                error=error+'Mark.X'+'  '+str(Fx)+'\n'
        if mark_y_bool:
            Fy_1 = InputTools.Stringfunctions(Fy)
            try:
                obj.setExpression('Y_Value', None)
                obj.setExpression('Y_Value', str(Fy_1[0]))
            except:
                error=error+'Mark.Y'+'  '+str(Fy)+'\n'
        if mark_z_bool:
            Fz_1 = InputTools.Stringfunctions(Fz)
            try:
                obj.setExpression('Z_Value', None)
                obj.setExpression('Z_Value', str(Fz_1[0]))
            except:
                error=error+'Mark.Z'+'  '+str(Fz)+'\n'
    elif FreeCAD.ActiveDocument.CoordinateSystem=="Polar":
        if mark_x_bool:
            Fx_1 = InputTools.Stringfunctions(Fx)
            try:
                obj.setExpression('R_Value', None)
                obj.setExpression('R_Value', str(Fx_1[0]))
            except:
                error=error+'Mark.R'+'  '+str(Fx)+'\n'
        if mark_y_bool:
            Fy_1 = InputTools.anglefunctions(Fy)
            try:
                obj.setExpression('Theta_Value', None)
                obj.setExpression('Theta_Value', str(Fy_1[0]))
            except:
                error=error+'Mark.Theta'+'  '+str(Fy)+'\n'
        if mark_z_bool:
            Fz_1 = InputTools.Stringfunctions(Fz)
            try:
                obj.setExpression('Z_Value', None)
                obj.setExpression('Z_Value', str(Fz_1[0]))
            except:
                error=error+'Mark.Z'+'  '+str(Fz)+'\n'
    else:
        if mark_x_bool:
            Fx_1 = InputTools.Stringfunctions(Fx)
            try:
                obj.setExpression('Z_Value', None)
                obj.setExpression('Z_Value', str(Fx_1[0]))
            except:
                error=error+'Mark.Z'+'  '+str(Fx)+'\n'
        if mark_y_bool:
            Fy_1 = InputTools.Stringfunctions(Fy)
            try:
                obj.setExpression('R_Value', None)
                obj.setExpression('R_Value', str(Fy_1[0]))
            except:
                error=error+'Mark.R'+'  '+str(Fy)+'\n'
        if mark_z_bool:
            Fz_1 = InputTools.anglefunctions(Fz)
            try:
                obj.setExpression('Theta_Value', None)
                obj.setExpression('Theta_Value', str(Fz_1[0]))
            except:
                error=error+'Mark.Theta'+'  '+str(Fz)+'\n'

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