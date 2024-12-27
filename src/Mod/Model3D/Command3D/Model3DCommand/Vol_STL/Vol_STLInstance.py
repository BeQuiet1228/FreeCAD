# -*- coding: utf8 -*-
import FreeCAD
import Part
from Model3D.Tools import Tools3D, ObjectTools, InitDoc3D
import Mesh
import Part
import os
import gmsh

# 定义 Z88 文件写入函数
def write_z88_mesh_to_file(femnodes_mesh, femelement_table, z88_element_type, f):
    node_dimension = 3  # 2 for 2D not supported
    if (z88_element_type == 4 or
       z88_element_type == 17 or z88_element_type == 16 or
       z88_element_type == 1 or z88_element_type == 10):
        node_dof = 3
    elif z88_element_type == 23 or z88_element_type == 24:
        node_dof = 6  # schalenelemente
    else:
        Tools3D.sayz("Error: wrong z88_element_type")
        return
    node_count = len(femnodes_mesh)
    element_count = len(femelement_table)
    dofs = node_dof * node_count
    unknown_flag = 0
    written_by = "written by FreeCAD"

    # first line, some z88 specific stuff
    f.write("{0} {1} {2} {3} {4} {5}\n".format(node_dimension, node_count, element_count, dofs, unknown_flag, written_by))
    # nodes
    for node in femnodes_mesh:
        vec = femnodes_mesh[node]
        f.write("{0} {1} {2:.6f} {3:.6f} {4:.6f}\n".format(node, node_dof, vec['x'], vec['y'], vec['z'], node))
    # elements
    for element in femelement_table:
        # z88_element_type is checked for every element, but mixed elements are not supported up to date
        n = femelement_table[element]
        if z88_element_type == 2 or z88_element_type == 4 or z88_element_type == 5 or z88_element_type == 9 or z88_element_type == 13 or z88_element_type == 25:
            # seg2 FreeCAD --> stab4 Z88
            # N1, N2
            f.write("{0} {1}\n".format(element, z88_element_type, element))
            f.write("{0} {1}\n".format(
                    n[0], n[1]))
        elif z88_element_type == 3 or z88_element_type == 14 or z88_element_type == 24:
            # tria6 FreeCAD --> schale24 Z88
            # N1, N2, N3, N4, N5, N6
            f.write("{0} {1}\n".format(element, z88_element_type, element))
            f.write("{0} {1} {2} {3} {4} {5}\n".format(
                    n[0], n[1], n[2], n[3], n[4], n[5]))
        elif z88_element_type == 7 or z88_element_type == 20 or z88_element_type == 23:
            # quad8 FreeCAD --> schale23 Z88
            # N1, N2, N3, N4, N5, N6, N7, N8
            f.write("{0} {1}\n".format(element, z88_element_type, element))
            f.write("{0} {1} {2} {3} {4} {5} {6} {7}\n".format(
                    n[0], n[1], n[2], n[3], n[4], n[5], n[6], n[7]))
        elif z88_element_type == 17:
            # tetra4 FreeCAD --> volume17 Z88
            # N4, N2, N3, N1
            f.write("{0} {1}\n".format(element, z88_element_type, element))
            f.write("{0} {1} {2} {3}\n".format(
                    n[3], n[1], n[2], n[0]))
        elif z88_element_type == 16:
            # tetra10 FreeCAD --> volume16 Z88
            # N1, N2, N4, N3, N5, N9, N8, N6, N10, N7, FC to Z88 is differend as Z88 to FC
            f.write("{0} {1}\n".format(element, z88_element_type, element))
            f.write("{0} {1} {2} {3} {4} {5} {6} {7} {8} {9}\n".format(
                    n[0], n[1], n[3], n[2], n[4], n[8], n[7], n[5], n[9], n[6]))
        elif z88_element_type == 1:
            # hexa8 FreeCAD --> volume1 Z88
            # N1, N2, N3, N4, N5, N6, N7, N8
            f.write("{0} {1}\n".format(element, z88_element_type, element))
            f.write("{0} {1} {2} {3} {4} {5} {6} {7}\n".format(
                    n[0], n[1], n[2], n[3], n[4], n[5], n[6], n[7]))
        elif z88_element_type == 10:
            # hexa20 FreeCAD --> volume10 Z88
            # N2, N3, N4, N1, N6, N7, N8, N5, N10, N11, N12, N9,  N14, N15, N16, N13, N18, N19, N20, N17
            # or turn by 90 degree and they match !
            # N1, N2, N3, N4, N5, N6, N7, N8, N9, N10, N11, N12, N13, N14, N15, N16, N17, N18, N19, N20
            f.write("{0} {1}\n".format(element, z88_element_type, element))
            f.write("{0} {1} {2} {3} {4} {5} {6} {7} {8} {9} {10} {11} {12} {13} {14} {15} {16} {17} {18} {19}\n".format(
                    n[0], n[1], n[2], n[3], n[4], n[5], n[6], n[7], n[8], n[9], n[10], n[11], n[12], n[13], n[14], n[15], n[16], n[17], n[18], n[19]))
        else:
            Tools3D.sayz("Writing of Z88 elementtype {0} not supported.\n".format(z88_element_type))
            # TODO support schale12 (made from prism15) and schale16 (made from hexa20)
            return

class Vol_STL:
    def __init__(self, obj):
        obj.Proxy = self

    def onChanged(self, fp, prop):
        pass

    def execute(self, fp):
        #try:
        mesh = Mesh.Mesh(fp.FilePath)
        shape = Part.Shape()
        shape.makeShapeFromMesh(mesh.Topology, 1)
        solid = Part.Solid(shape)
        fp.Shape = solid
        # base_name, _ = os.path.splitext(fp.FilePath) # 分离文件名和扩展名
        # brep_filepath = base_name + ".brep" # 构建新的文件名
        # shape.exportBrep(brep_filepath)
        
        gmsh.initialize()
        gmsh.open(fp.FilePath) # 3D STL file of a cylinder
        surfaces = gmsh.model.getEntities(2)
        for dim, tag in surfaces:
            sloop = gmsh.model.geo.addSurfaceLoop([tag])  # 使用表面循环生成体数据
            volume = gmsh.model.geo.addVolume([sloop])
        gmsh.model.geo.synchronize()#等待生成完成
        # gmsh.model.mesh.classifySurfaces(gmsh.pi, True, True, gmsh.pi)
        # gmsh.model.mesh.createGeometry()
        # s = gmsh.model.getEntities(2)
        # surf = gmsh.model.geo.addSurfaceLoop([e[1] for e in s])
        # vol = gmsh.model.geo.addVolume([surf])
        # gmsh.model.geo.synchronize()

        # gmsh.option.setNumber('Mesh.Algorithm',1)
        # gmsh.option.setNumber('Mesh.MeshSizeMax', 0.05)
        # gmsh.option.setNumber('Mesh.MeshSizeMin', 0.05)
        # gmsh.option.setNumber("Mesh.Algorithm3D", 4)  # 使用 Delaunay 算法
        # gmsh.option.setNumber("Mesh.ElementOrder", 1) # 设置网格的阶数，1 表示线性网格
        # gmsh.option.setNumber("Mesh.Optimize", 1)    # 优化网格质量（可选）
        gmsh.model.mesh.generate(3)
        Tools3D.sayz('Model ' + gmsh.model.getCurrent() + ' (' +
            str(gmsh.model.getDimension()) + 'D)')

          # 节点数据
        femnodes_mesh = {}
        node_tags, node_coords, _ = gmsh.model.mesh.getNodes()
        for i, tag in enumerate(node_tags):
            femnodes_mesh[tag] = {
                "x": node_coords[i * 3 + 0],
                "y": node_coords[i * 3 + 1],
                "z": node_coords[i * 3 + 2],
            }

        # 单元数据
        femelement_table = {}
        z88_element_type = None
        elem_types, elem_tags, node_tags_list = gmsh.model.mesh.getElements(3)
        for t in elem_types:
            name, dim, order, numv, parv, _ = gmsh.model.mesh.getElementProperties(
                t)
            Tools3D.sayz(" - Element type: " + name + ", order " + str(order) + " (" +
                str(numv) + " nodes in param coord: " + str(parv) + ")")

        
        for i, elem_type in enumerate(elem_types):
            elem_nodes = node_tags_list[i]
            elem_tags_per_type = elem_tags[i]

            # 映射 Gmsh 单元类型到 Z88 单元类型
            if elem_type == 4:  # Tetrahedron (4-node)
                z88_element_type = 17
            elif elem_type == 11:  # Hexahedron (8-node)
                z88_element_type = 1
            elif elem_type == 92:  # Tetrahedron (10-node)
                z88_element_type = 16
            elif elem_type == 29:  # Hexahedron (20-node)
                z88_element_type = 10
            else:
                Tools3D.sayz("Unsupported Gmsh element type:" + str(elem_type))
                continue

            # 构造 `femelement_table`
            num_nodes_per_element = len(elem_nodes) // len(elem_tags_per_type)
            for j, elem_tag in enumerate(elem_tags_per_type):
                start_idx = j * num_nodes_per_element
                end_idx = start_idx + num_nodes_per_element
                femelement_table[elem_tag] = elem_nodes[start_idx:end_idx]

        base_name, _ = os.path.splitext(fp.FilePath) # 分离文件名和扩展名
        output_file = base_name + ".txt" # 构建新的文件名
        with open(output_file, "w") as f:
            write_z88_mesh_to_file(femnodes_mesh, femelement_table, z88_element_type, f)

        gmsh.write('F:/PICGUIC_L/Example/3d/MILO-C/test.msh')

        # except:
        #     Tools3D.sayz("Redraw Point Failed!")


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

