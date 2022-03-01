#-*- coding: utf-8 -*-

import Modeling3DGuiTest
import Vol_Cylinder           # a simple Cylinder
import Vol_Annular   # Cylinder with a hole
# import Area_TorusFace          # CircleFace with a hole
# import Area_Polygonal
# import Vol_Cone               # Cone with only one Radius
import Vol_SpecialCone        # Cone with two Radiuses
import Vol_Torus              # a Torus 
import Vol_OrthographicBody   # a CreateOrthographicBody
import Vol_Parallelepipedal     # 定义一个平行四边形
import Vol_Spherical             # 定义一个球体
import Vol_Wedge              # 定义一个楔形体
import Vol_Pyramid            # 金字塔形
import Vol_Rhombus            #菱形体
import Vol_Tetrahedron
import Point              
import Vol_Conformal          #投影
import Line_Conformal         # Line_Conformal
import Line_Oblique       # 线段
import Area_Conformal         #法向在坐标轴上的面
import Area_Rectangular
import Area_Polygonal
import _Operation_Clip
import _Operation_Copy
import Vol_Toroidal_Section
import Vol_Annular_Section
# import Vol_Functionimport Vol_Extruded
import Vol_Extruded
import Vol_Helical
import Vol_Boolean
import Object_Array
import Vol_Function
import DialogReShow
import ShowAllFunction

from Vol_Array.Command import Vol_Array_Dlg_Main
from _Operation_Clip.Command import ClipCommand

from DraftModeling_Extrude.Command import DraftModeling_ExtrudeDlgMain
from DraftModeling_Revolution.Command import DraftModeling_RevolutionDlgMain
# import Test
import Area_Function

from Vol_Revolution.Command import RevolutionCommand
import SingleClickObj



######################################工程设置######################################
# import TestFolder