import math
import Plot
import numpy as np

# -*- coding: UTF-8 -*-

fig1 = Plot.figure('test')

def call_back(event):
    axtemp = event.inaxes
    x_min, x_max = axtemp.get_xlim()
    y_min, y_max = axtemp.get_ylim()
    fanwei = (x_max - x_min) / 10
    fanwei_y = (y_max - y_min) / 10
    if event.button == 'up':
        axtemp.set(xlim=(x_min + fanwei, x_max - fanwei))
        axtemp.set(ylim=(y_min + fanwei_y, y_max - fanwei_y))
    elif event.button == 'down':
        axtemp.set(xlim=(x_min - fanwei, x_max + fanwei))
        axtemp.set(ylim=(y_min - fanwei_y, y_max + fanwei_y))
    fig1.canvas.draw_idle()

def plot():

    fig1.canvas.mpl_connect('scroll_event', call_back)


    p = range(0, 1001)
    x = [2.0 * xx / 1000.0 for xx in p]
    y = [xx ** 2.0 for xx in x]
    t = [tt / 1000.0 for tt in p]
    s = [math.sin(math.pi * 2.0 * tt) for tt in t]
    c = [math.cos(math.pi * 2.0 * tt) for tt in t]
    Plot.plot(t, s, r"$\sin\left( 2 \pi t \right)$")
    Plot.plot(t, c, r"$\cos\left( 2 \pi t \right)$")



