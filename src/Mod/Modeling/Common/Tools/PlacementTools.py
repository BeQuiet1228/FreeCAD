# -*- coding: utf-8 -*-
import FreeCAD, math
from FreeCAD import Base
from pivy import coin
from PySide import QtGui, QtCore

def moveAdd(pos,vectorList):
    resultList=[]
    for vector in vectorList:
        resultList.append(vector.add(pos))
    return resultList




def rotate(beforePlacement,curPlacement,vectorList):
    # r1表示本次旋转之前的旋转四元数，r2表示本次当前的旋转四元数，r1_1表示之前旋转四元数的逆，
    # r2*r1_1表示先将点回旋到初始位置，在初始位置上进行本次旋转。
    r2 = curPlacement.Rotation
    r1 = beforePlacement.Rotation
    r1_1 = r1.inverted()
    r = r2.multiply(r1_1)
    resultList=[]
    #先将局部坐标系与世界坐标系重合
    for vector in vectorList:        
        resultPoint=vector.sub(curPlacement.Base)
        # resultPoint2=resultPoint2.sub(fp.Placement.Base)
        resultPoint=r.multVec(resultPoint)
        # resultPoint2=r.multVec(resultPoint2)
        resultPoint=resultPoint.add(curPlacement.Base)
        # resultPoint2=resultPoint2.add(fp.Placement.Base)
        resultList.append(resultPoint)
    return resultList

