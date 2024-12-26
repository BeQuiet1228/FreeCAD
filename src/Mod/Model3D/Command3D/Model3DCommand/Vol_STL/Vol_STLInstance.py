# -*- coding: utf8 -*-
import FreeCAD
import Part
from Model3D.Tools import Tools3D, ObjectTools, InitDoc3D
import Mesh
import Part
import os


class Vol_STL:
    def __init__(self, obj):
        obj.Proxy = self

    def onChanged(self, fp, prop):
        pass

    def execute(self, fp):
        try:
            mesh = Mesh.Mesh(fp.FilePath)
            shape = Part.Shape()
            # shape.read(fp.FilePath)
            # if shape.isNull(): # 检查是否成功导入
            #     Tools3D.sayz(f"Error: Failed to import STEP file from {fp.FilePath}. The shape is null.")
            #     return None
            shape.makeShapeFromMesh(mesh.Topology, 1)
            solid = Part.Solid(shape)
            fp.Shape = solid
            base_name, _ = os.path.splitext(fp.FilePath) # 分离文件名和扩展名
            brep_filepath = base_name + ".brep" # 构建新的文件名
            shape.exportBrep(brep_filepath)
        except:
            Tools3D.sayz("Redraw Point Failed!")


class GetProperty:
    def __init__(self):
        #FreeCAD.ActiveDocument.openTransaction('CreatePoint_3D')
        self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", ObjectTools.ObjectType.Vol_STL)
        self.__setProperty(self.obj)
        InitDoc3D.addObjectToGroup_helper(self.obj, 'PointG', '点')
        FreeCAD.ActiveDocument.commitTransaction()

    def __setProperty(self, obj):
        obj.addProperty("App::PropertyString", "Type").Type = ObjectTools.ObjectType.Vol_STL
        obj.addProperty("App::PropertyString", "FilePath").FilePath = "C:/PICGUIC_L/Example/3d/MILO-C/123_CC.stl"
        Tools3D.addCommonProperty(obj)
        Tools3D.addAttributeToObject(obj)


def getObject():
    PointObj = GetProperty()
    Vol_STL(PointObj.obj)
    Tools3D.ViewProvider(PointObj.obj.ViewObject)
    return PointObj.obj

