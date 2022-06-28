# -*- coding: utf-8 -*-
import FreeCAD, math
from FreeCAD import Base
from pivy import coin
from PySide import QtGui, QtCore

# 坐标系类
class CoordinateType:
    Rectangular="Rectangular"
    Polar="Polar"
    Cylindrical="Cylindrical"

#将极坐标点转化为直角坐标系点：
def testOtherToRec(coordinateType,point):
    #判断坐标系：实现数值转换
    result=point
    #直角坐标系下：
    if coordinateType=='Rectangular':
        pass
    #极坐标系下：
    #极坐标系下，R与直角坐标系的X相同；根据R与θ求得直角坐标系下的y；z与直角坐标系z相同
    elif coordinateType=='Polar' or coordinateType=='Cylindrical':
        radian=point.y*math.pi/180.0
        pointY=point.x*math.sin(radian)
        pointX=point.x*math.cos(radian)
        resultPoint=FreeCAD.Vector(pointX,pointY,point.z)
        result=resultPoint
        #test:
        points=[FreeCAD.Vector(1.0,45.0,1.0)]
        resultPoints=[]
        for point in points:
            resultPoints.append(point)

    #圆柱坐标系下的转换
    else:
        pass
    #转换完成
    return result


#将极坐标点转化为直角坐标系点：
def otherToRec(coordinateType,pointList):
    #判断坐标系：实现数值转换
    resultList=[]
    #直角坐标系下：
    if coordinateType=='Rectangular':
        resultList=pointList
        pass
    #极坐标系下：
    #极坐标系下，R与直角坐标系的X相同；根据R与θ求得直角坐标系下的y；z与直角坐标系z相同
    elif coordinateType=='Polar' or coordinateType=='Cylindrical':
        for point in pointList:
            radian=point.y*math.pi/180.0
            pointY=point.x*math.sin(radian)
            pointX=point.x*math.cos(radian)
            resultPoint=FreeCAD.Vector(pointX,pointY,point.z)
            resultList.append(resultPoint)

    #圆柱坐标系下的转换
    else:
        pass
    #转换完成
    return resultList

#将直角坐标系点转化为极坐标系点     ：
def recToOther(coordinateType,pointList):
    resultList=[]
    if coordinateType=='Rectangular':
        resultList=pointList
        pass
    elif coordinateType=='Polar' or coordinateType=='Cylindrical':
        for point in pointList:
            resultPoint=point
            if point.x==0:
                if point.y==0:
                    resultPoint=FreeCAD.Vector(0.0,0.0,point.z)
                elif point.y>0:
                    resultPoint=FreeCAD.Vector(point.y,90.0,point.z)
                elif point.y<0:
                    resultPoint=FreeCAD.Vector(-point.y,270.0,point.z)
                resultList.append(resultPoint)
            else:
                # theta 为弧度值，radian为角度
                theta=math.atan2(point.y,point.x)
                radian=theta*180.0/math.pi
                radian=radian%360.0
                #r
                r=math.sqrt(point.x**2+point.y**2)
                resultPoint=FreeCAD.Vector(r,radian,point.z)
                resultList.append(resultPoint)
    else:
        pass
    return resultList

    #将单个坐标点转化为直角坐标系下的点
def otherToRecOne(coordinateType,point):
    resultPoint=point
    if coordinateType=='Rectangular':
        resultPoint=point
        pass
    #极坐标系下：
    #极坐标系下，R与直角坐标系的X相同；根据R与θ求得直角坐标系下的y；z与直角坐标系z相同
    elif coordinateType=='Polar' or coordinateType=='Cylindrical':
        radian=point.y*math.pi/180.0
        pointY=point.x*math.sin(radian)
        pointX=point.x*math.cos(radian)
        resultPoint=FreeCAD.Vector(pointX,pointY,point.z)
    #圆柱坐标系下的转换
    else:
        pass
    #转换完成
    return resultPoint

def recToOtherOne(coordinateType,point):
    resultPoint=point
    if coordinateType=='Rectangular':
        resultPoint=point
    elif coordinateType=='Polar' or coordinateType=='Cylindrical':
        if point.x==0:
            if point.y==0:
                resultPoint=FreeCAD.Vector(0.0,0.0,point.z)
            elif point.y>0:
                resultPoint=FreeCAD.Vector(point.y,90.0,point.z)
            elif point.y<0:
                resultPoint=FreeCAD.Vector(-point.y,270.0,point.z)
            # resultList.append(resultPoint)
        else:
            # theta 为弧度值，radian为角度
            theta=math.atan2(point.y,point.x)
            radian=theta*180.0/math.pi
            radian=radian%360.0
            #r
            r=math.sqrt(point.x**2+point.y**2)
            resultPoint=FreeCAD.Vector(r,radian,point.z)
            # resultList.append(resultPoint)
    return resultPoint

#将直角坐标系点转化为极坐标系点 ：
def recToOtherNotPoints(coordinateType,pointList):
    '''
    与上面函数的唯一区别是，这里的点没有x,y,z属性
    '''
    resultList=[]
    if coordinateType=='Rectangular':
        resultList=pointList
        pass
    elif coordinateType=='Polar' or coordinateType=='Cylindrical':
        for point in pointList:
            resultPoint=point
            if point[0]==0:
                if point[1]==0:
                    resultPoint=FreeCAD.Vector(0.0,0.0,point[2])
                elif point[1]>0:
                    resultPoint=FreeCAD.Vector(point[1],90.0,point[2])
                elif point[1]<0:
                    resultPoint=FreeCAD.Vector(-point[1],270.0,point[2])
                resultList.append(resultPoint)
            else:
                # theta 为弧度值，radian为角度
                theta=math.atan2(point[1],point[0])
                radian=theta*180.0/math.pi
                radian=radian%360.0
                #r
                r=math.sqrt(point[0]**2+point[1]**2)
                resultPoint=FreeCAD.Vector(r,radian,point[2])
                resultList.append(resultPoint)
    else:
        pass
    return resultList