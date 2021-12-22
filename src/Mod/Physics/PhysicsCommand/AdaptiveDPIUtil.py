# -*- coding: UTF-8 -*-
import ctypes

def get_win_dpi():
    """ 
  In:
    none

  Out:
    x_dpi: dpi on x axis. [int]
    y_dpi: dpi on y axis. [int]
 
  """
    user32 = ctypes.windll.user32
    x_dpi, y_dpi = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

    return x_dpi, y_dpi


def get_new_dpi(x_old, y_old, height_scale = 0.6):
    """ 
    This function calculate the scale factor based on the current DPI setting.
    
    In:
    none
 
  Out:
    new_x: scale factor on x axis. [float]
    new_y: scale factor on y axis. [float]
 
  """
    x_dpi, y_dpi = get_win_dpi()

    if y_dpi * height_scale < y_old:
        new_y = y_dpi * height_scale
        new_x = x_old * new_y / y_old
        return new_x, new_y
    else:
        return x_old, y_old



