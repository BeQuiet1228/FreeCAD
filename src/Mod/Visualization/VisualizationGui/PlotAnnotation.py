# -*- coding: UTF-8 -*-

import FreeCAD as App
import FreeCADGui as Gui

from PySide import QtGui, QtCore

import vPlot
import numpy as np

def annotate():
    plt = vPlot.getPlot()
    for item in range(len(vPlot.series())):
        serie = vPlot.series()[item]

        if serie.type in ['contour','vector']:
            # 获取图的横纵坐标范围
            data_x_min = plt.axleft.get_xlim()
            data_y_min = plt.axleft.get_ylim()
            # 获取x,y数据
            dataset = []
            for y in serie.y:
                for x in serie.x:
                    dataset.append([x, y])

            # 获取横纵坐标轴科学记数法倍数
            y_e = "%e" % data_y_min[1]
            x_e = "%e" % data_x_min[1]
            y_multiple = int(y_e.split('e', 2)[1])
            x_multiple = int(x_e.split('e', 2)[1])
            # 去除科学计数法单位只留一个整数位
            dataMat = np.vstack(
                (np.array(dataset)[:, 0] / pow(10, x_multiple), np.array(dataset)[:, 1] / pow(10, y_multiple)))
            dataMat = dataMat.T

            # 创建KD树
            tree = createKDTree(dataMat, 0)
            plt.axleft.figure.canvas.mpl_connect('button_press_event',
                                                 lambda event: button_press_event_slow(event, plt.axleft, tree,
                                                                                       x_multiple, y_multiple,
                                                                                       serie.x, serie.y, serie.z,
                                                                                       serie.type))

        elif serie.type == 'observe':
            serie = vPlot.series()[item]

            # 获取图的横纵坐标范围
            data_x_min = plt.axleft.get_xlim()
            data_y_min = plt.axleft.get_ylim()

            # 获取x,y数据
            dataset = np.array([serie.x,serie.y]).T

            # 获取横纵坐标轴科学记数法倍数
            y_e = "%e" % data_y_min[1]
            x_e = "%e" % data_x_min[1]
            y_multiple = int(y_e.split('e', 2)[1])
            x_multiple = int(x_e.split('e', 2)[1])
            # 去除科学计数法单位只留一个整数位
            dataMat = np.vstack(
                (np.array(dataset)[:, 0] / pow(10, x_multiple), np.array(dataset)[:, 1] / pow(10, y_multiple)))
            dataMat = dataMat.T

            # 创建KD树
            tree = createKDTree(dataMat, 0)
            plt.axleft.figure.canvas.mpl_connect('button_press_event',
                                                 lambda event: button_press_event_observe(event, plt.axleft, tree,
                                                                                          x_multiple, y_multiple,
                                                                                          serie.x, serie.y))


        else:
            plt.fig.canvas.mpl_connect('button_press_event',
                                           lambda event: button_press_event_fast(event,  plt.axleft))


#时间变化，空间变化，相空间图鼠标点击触发事件
def button_press_event_fast(event, axes):
    try:
        if event.inaxes ==axes and event.button == 3:
            #获取鼠标点击点的数据
            x = event.xdata
            y = event.ydata
            x_min, x_max = event.inaxes.get_xlim()
            y_min, y_max = event.inaxes.get_ylim()
            range_x = (x_max - x_min) / 30
            range_y = (y_max - y_min) / 30
            annotation = axes.annotate('x=' + str(x) + '\n ' + 'y=' + str(y), xy=(x, y), xycoords='data',
                                      xytext=(x + range_x, y + range_y),
                                      textcoords='data', horizontalalignment="left",
                                      arrowprops=dict(arrowstyle="simple", connectionstyle="arc3,rad=-0.1"),
                                      bbox=dict(boxstyle="round", facecolor="w", edgecolor="0.5", alpha=0.9)
                                      ,zorder=20)
            annotation.set_visible(True)
            axes.figure.canvas.draw()#刷新
            annotation.set_visible(False)
    except:
        pass

#等位图,矢量图鼠标点击触发事件
def button_press_event_observe(event, axes,tree,x_multiple,y_multiple,a,b):
    try:
        if event.inaxes ==axes and event.button == 3:
            x = event.xdata
            y = event.ydata
            x_min, x_max = axes.get_xlim()
            y_min, y_max = axes.get_ylim()
            range_x = (x_max - x_min) / 30
            range_y = (y_max - y_min) / 30
            point = [x / pow(10, x_multiple), y / pow(10, y_multiple)]
            nearpoint, neardis = searchTree(tree, point)
            real_nearpoint = [nearpoint[0] * pow(10, x_multiple), nearpoint[1] * pow(10, y_multiple)]
            #获取点的索引
            index_x = np.where(np.array(a) == real_nearpoint[0])[0][0]
            index_y = np.where(np.array(b) == real_nearpoint[1])[0][0]
            # FreeCAD.Console.PrintMessage(index_x)
            # FreeCAD.Console.PrintMessage('\n')
            # FreeCAD.Console.PrintMessage(index_y)
            # FreeCAD.Console.PrintMessage('\n')
            # FreeCAD.Console.PrintMessage(index)
            # FreeCAD.Console.PrintMessage('\n')
            #获取c的值

            text='x=' + str(real_nearpoint[0])+'\n'+'y=' + str(real_nearpoint[1])+'\n'

            annotation = axes.annotate((text),
                                      xy=(real_nearpoint[0], real_nearpoint[1]), xycoords='data', xytext=(real_nearpoint[0]+range_x, real_nearpoint[1]+range_y),
                                      textcoords='data', horizontalalignment="left",
                                      arrowprops=dict(arrowstyle="simple", connectionstyle="arc3,rad=-0.1"),
                                      bbox=dict(boxstyle="round", facecolor="w", edgecolor="0.5", alpha=0.9)
                                      ,zorder=20)
            annotation.set_visible(True)
            axes.figure.canvas.draw()
            annotation.set_visible(False)
    except:
        pass

#等位图,矢量图鼠标点击触发事件
def button_press_event_slow(event, axes,tree,x_multiple,y_multiple,a,b,c,flag):
    try:
        if event.inaxes ==axes and event.button == 3:
            x = event.xdata
            y = event.ydata
            x_min, x_max = axes.get_xlim()
            y_min, y_max = axes.get_ylim()
            range_x = (x_max - x_min) / 30
            range_y = (y_max - y_min) / 30
            point = [x / pow(10, x_multiple), y / pow(10, y_multiple)]
            nearpoint, neardis = searchTree(tree, point)
            real_nearpoint = [nearpoint[0] * pow(10, x_multiple), nearpoint[1] * pow(10, y_multiple)]
            #获取点的索引
            index_x = np.where(np.array(a) == real_nearpoint[0])[0][0]
            index_y = np.where(np.array(b) == real_nearpoint[1])[0][0]
            # FreeCAD.Console.PrintMessage(index_x)
            # FreeCAD.Console.PrintMessage('\n')
            # FreeCAD.Console.PrintMessage(index_y)
            # FreeCAD.Console.PrintMessage('\n')
            if flag == 'contour':
                index = (index_x + 1) * (index_y + 1) - 1
                # FreeCAD.Console.PrintMessage(index)
                # FreeCAD.Console.PrintMessage('\n')
                #获取c的值
                value = np.array(c)[index]
                text='x=' + str(real_nearpoint[0])+'\n'+'y=' + str(real_nearpoint[1])+'\n'+u'等位值=' + str(value)
            else:
                index = (index_x + 1) * (index_y + 1) - 1
                # FreeCAD.Console.PrintMessage(index)
                # FreeCAD.Console.PrintMessage('\n')
                # FreeCAD.Console.PrintMessage(index + len(np.array(a)) * len(np.array(b)))
                # FreeCAD.Console.PrintMessage('\n')
                # 获取c的值
                value1 = np.array(c)[index]
                value2 = np.array(c)[index+len(np.array(a))*len(np.array(b))]
                text = 'x=' + str(real_nearpoint[0]) + '\n' + 'y=' + str(real_nearpoint[1]) + '\n' + u'矢量x=' + str(value1)+ '\n' + u'矢量y=' + str(value2)
            annotation = axes.annotate((text),
                                      xy=(real_nearpoint[0], real_nearpoint[1]), xycoords='data', xytext=(real_nearpoint[0]+range_x, real_nearpoint[1]+range_y),
                                      textcoords='data', horizontalalignment="left",
                                      arrowprops=dict(arrowstyle="simple", connectionstyle="arc3,rad=-0.1"),
                                      bbox=dict(boxstyle="round", facecolor="w", edgecolor="0.5", alpha=0.9)
                                      ,zorder=20)
            annotation.set_visible(True)
            axes.figure.canvas.draw()
            annotation.set_visible(False)
    except:
        pass


#创建KD树
def createKDTree(dataSet, depth):
    n = np.shape(dataSet)[0]
    treeNode = {}
    if n == 0:
        return None
    else:
        n, m = np.shape(dataSet)
        split_axis = depth % m
        depth += 1
        treeNode['split'] = split_axis
        dataSet = sorted(dataSet, key=lambda a: a[split_axis])
        num = n // 2
        treeNode['median'] = dataSet[num]
        treeNode['left'] = createKDTree(dataSet[:num], depth)
        treeNode['right'] = createKDTree(dataSet[num + 1:], depth)
        return treeNode

#查找KD树
def searchTree(tree, data):
    k = len(data)
    if tree is None:
        return [0] * k, float('inf')
    split_axis = tree['split']
    median_point = tree['median']
    if data[split_axis] <= median_point[split_axis]:
        nearestPoint, nearestDistance = searchTree(tree['left'], data)
    else:
        nearestPoint, nearestDistance = searchTree(tree['right'], data)
    nowDistance = np.linalg.norm(data - median_point)  # the distance between data to current point
    if nowDistance < nearestDistance:
        nearestDistance = nowDistance
        nearestPoint = median_point.copy()
    splitDistance = abs(data[split_axis] - median_point[split_axis])  # the distance between hyperplane
    if splitDistance > nearestDistance:
        return nearestPoint, nearestDistance
    else:
        if data[split_axis] <= median_point[split_axis]:
            nextTree = tree['right']
        else:
            nextTree = tree['left']
        nearPoint, nearDistanc = searchTree(nextTree, data)
        if nearDistanc < nearestDistance:
            nearestDistance = nearDistanc
            nearestPoint = nearPoint.copy()
        return nearestPoint, nearestDistance