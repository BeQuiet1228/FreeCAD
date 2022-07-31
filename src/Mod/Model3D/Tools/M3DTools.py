# -*- coding: utf-8 -*-
from Model3D.Tools.ObjectTools import ObjectType
from Model3D.Tools import ObjectTools


def getAllModelObjDict():
    """
    获取所有的点线面的obj
    """
    res_dict = {
        ObjectType.Point: [],
        ObjectType.Line_Conformal: [],
        ObjectType.Line_Oblique: [],
        ObjectType.Area_Conformal: [],
        ObjectType.Area_Rectangular: [],
        ObjectType.Area_Polygonal: [],
        ObjectType.Area_Function: [],
        ObjectType.Vol_Conformal: [],
        ObjectType.Vol_SpecialCone: [],
        ObjectType.Vol_Cylinder: [],
        ObjectType.Vol_Parallelepipedal: [],
        ObjectType.Vol_Annular: [],
        ObjectType.Vol_Pyramid: [],
        ObjectType.Vol_Rhombus: [],
        ObjectType.Vol_Spherical: [],
        ObjectType.Vol_Wedge: [],
        ObjectType.Vol_Tetrahedron: [],
        ObjectType.Vol_Toroidal_Section: [],
        ObjectType.Vol_Annular_Section: [],
        ObjectType.Vol_Function: [],
        ObjectType.Vol_Extruded: [],
        ObjectType.Vol_Helical: [],
        ObjectType.Vol_Array: [],
        ObjectType.Vol_Draft_Revolution: [],
        ObjectType.Vol_Revolution: [],
        ObjectType.Vol_ParamArray: [],
        ObjectType.Vol_Draft_Extrude: [],
        ObjectType.MARK: []
    }
    obj_List = ObjectTools.getAllObjects()
    for i in obj_List:
        if not hasattr(i, "Type"):
            continue
        if i.Type == ObjectType.Point:
            res_dict[ObjectType.Point].append(i)

        elif i.Type == ObjectType.Line_Conformal:
            res_dict[ObjectType.Line_Conformal].append(i)

        elif i.Type == ObjectType.Line_Oblique:
            res_dict[ObjectType.Line_Oblique].append(i)

        elif i.Type == ObjectType.Area_Conformal:
            res_dict[ObjectType.Area_Conformal].append(i)

        elif i.Type == ObjectType.Area_Rectangular:
            res_dict[ObjectType.Area_Rectangular].append(i)

        elif i.Type == ObjectType.Area_Polygonal:
            res_dict[ObjectType.Area_Polygonal].append(i)

        elif i.Type == ObjectType.Area_Function:
            res_dict[ObjectType.Area_Function].append(i)

        elif i.Type == ObjectType.Vol_Conformal:
            res_dict[ObjectType.Vol_Conformal].append(i)

        elif i.Type == ObjectType.Vol_SpecialCone:
            res_dict[ObjectType.Vol_SpecialCone].append(i)

        if i.Type == ObjectType.Vol_Cylinder:
            res_dict[ObjectType.Vol_Cylinder].append(i)

        elif i.Type == ObjectType.Vol_Parallelepipedal:
            res_dict[ObjectType.Vol_Parallelepipedal].append(i)

        elif i.Type == ObjectType.Vol_Annular:
            res_dict[ObjectType.Vol_Annular].append(i)

        elif i.Type == ObjectType.Vol_Pyramid:
            res_dict[ObjectType.Vol_Pyramid].append(i)

        elif i.Type == ObjectType.Vol_Rhombus:
            res_dict[ObjectType.Vol_Rhombus].append(i)

        elif i.Type == ObjectType.Vol_Spherical:
            res_dict[ObjectType.Vol_Spherical].append(i)

        elif i.Type == ObjectType.Vol_Wedge:
            res_dict[ObjectType.Vol_Wedge].append(i)

        elif i.Type == ObjectType.Vol_Tetrahedron:
            res_dict[ObjectType.Vol_Tetrahedron].append(i)

        elif i.Type == ObjectType.Vol_Toroidal_Section:
            res_dict[ObjectType.Vol_Toroidal_Section].append(i)

        elif i.Type == ObjectType.Vol_Annular_Section:
            res_dict[ObjectType.Vol_Annular_Section].append(i)

        elif i.Type == ObjectType.Vol_Function:
            res_dict[ObjectType.Vol_Function].append(i)

        elif i.Type == ObjectType.Vol_Extruded:
            res_dict[ObjectType.Vol_Extruded].append(i)

        elif i.Type == ObjectType.Vol_Helical:
            res_dict[ObjectType.Vol_Helical].append(i)

        elif i.Type == ObjectType.Vol_Array:
            res_dict[ObjectType.Vol_Array].append(i)

        elif i.Type == ObjectType.Vol_Draft_Revolution:
            res_dict[ObjectType.Vol_Draft_Revolution].append(i)

        elif i.Type == ObjectType.Vol_Revolution:
            res_dict[ObjectType.Vol_Revolution].append(i)

        elif i.Type == ObjectType.Vol_ParamArray:
            res_dict[ObjectType.Vol_ParamArray].append(i)

        elif i.Type == ObjectType.Vol_Draft_Extrude:
            res_dict[ObjectType.Vol_Draft_Extrude].append(i)


    # 为Mark单独写一个
    obj_mark_list = ObjectTools.getAllPhyAndProObjects()
    for j in obj_mark_list:
        if j.Type == ObjectType.MARK:
            res_dict[ObjectType.MARK].append(j)

    return res_dict


def getAllPlotsDict():
    """
    获取观测设置相关的字典,放进ALL PLOTS
    """
    res_dict = {
        ObjectType.DefaultTimer:[],
        ObjectType.CustomTimer: [],
        ObjectType.CNTR: [],
        ObjectType.Vector: [],
        ObjectType.PhasSpace: [],
        ObjectType.AreaRan: [],
        ObjectType.Observe: []
    }

    ap_list = ObjectTools.getAllPhyAndProObjects()
    for i in ap_list:

        if i.Type == ObjectType.DefaultTimer:
            res_dict[ObjectType.DefaultTimer].append(i)

        if i.Type == ObjectType.CustomTimer:
            res_dict[ObjectType.CustomTimer].append(i)

        if i.Type == ObjectType.CNTR:
            res_dict[ObjectType.CNTR].append(i)

        elif i.Type == ObjectType.Vector:
            res_dict[ObjectType.Vector].append(i)

        elif i.Type == ObjectType.PhasSpace:
            res_dict[ObjectType.PhasSpace].append(i)

        elif i.Type == ObjectType.AreaRan:
            res_dict[ObjectType.AreaRan].append(i)

        elif i.Type == ObjectType.Observe or i.Type == "Observe":
            res_dict[ObjectType.Observe].append(i)

    return res_dict


def getHeaderDict():
    """
    获取模型输入信息
    """
    res_dict = {ObjectType.Info: []}
    h_list = ObjectTools.getAllPhyAndProObjects()
    for i in h_list:
        if i.Type == ObjectType.Info:
            res_dict[ObjectType.Info].append(i)

    return res_dict


def getGridDict():
    """
    获取网格信息
    """
    res_dict = {ObjectType.Simu: []}
    grid_list = ObjectTools.getAllPhyAndProObjects()
    for i in grid_list:
        if i.Type == ObjectType.Simu:
            res_dict[ObjectType.Simu].append(i)

    return res_dict


def getCommonPresets():
    """
    获取 CommonPresets 有关的m3d
    """
    res_dict = {ObjectType.NewParticle: [],
                ObjectType.NewMaterial: [],
                ObjectType.FieldSetting: []
                }
    cp_list = ObjectTools.getAllPhyAndProObjects()
    for i in cp_list:
        if i.Type == ObjectType.NewParticle:
            res_dict[ObjectType.NewParticle].append(i)

        if i.Type == ObjectType.NewMaterial:
            res_dict[ObjectType.NewMaterial].append(i)

        if i.Type == ObjectType.FieldSetting:
            res_dict[ObjectType.FieldSetting].append(i)
    return res_dict


def getSimulationSetting():
    """
    获取 Simulation Setting 有关的字典
    """
    res_dict = {ObjectType.TimeDomain: []}
    ss_list = ObjectTools.getAllPhyAndProObjects()
    for i in ss_list:
        if i.Type == ObjectType.TimeDomain:
            res_dict[ObjectType.TimeDomain].append(i)
    return res_dict


def getDumpOptions():
    """
    获取 Dump Options 有关的字典
    """
    res_dict = {ObjectType.DataProcess: []}
    do_list = ObjectTools.getAllPhyAndProObjects()
    for i in do_list:
        if i.Type == ObjectType.DataProcess:
            res_dict[ObjectType.DataProcess].append(i)
    return res_dict

def getCollectionOutput():
    """
    获取Collection Output有关的的字典
    """
    res_dict = {ObjectType.CollectionOutput: []}
    ro_list = ObjectTools.getAllPhyAndProObjects()
    for i in ro_list:
        if i.Type == ObjectType.CollectionOutput:
            res_dict[ObjectType.CollectionOutput].append(i)
    return res_dict

def getRunOptions():
    """
    获取Run Options有关的的字典
    """
    res_dict = {ObjectType.RunOptions: []}
    ro_list = ObjectTools.getAllPhyAndProObjects()
    for i in ro_list:
        if i.Type == ObjectType.RunOptions:
            res_dict[ObjectType.RunOptions].append(i)
    return res_dict


def getAllPropertiesAndProcessesObj():
    """
    获取所有与 Properties And Processes 相关的obj
    return type -> dict
    """
    res_dict = {ObjectType.SOLE: [],
                ObjectType.DRIV: [],
                ObjectType.FOIL: [],
                ObjectType.IND:  [],
                ObjectType.PORT: [],
                ObjectType.FREE: [],
                ObjectType.SYMT: [],
                ObjectType.BEAM: [],
                ObjectType.EXPS: [],
                ObjectType.GYRO: [],
                ObjectType.POPU: [],
                ObjectType.FELD: [],
                ObjectType.THER: [],
                ObjectType.SECD: [],
                ObjectType.IONI: [],
                ObjectType.MacroParticle: [],
                }

    pp_list = ObjectTools.getAllPhyAndProObjects()  # physics and project list , 请不要混淆
    # 挑选与Properties And Processes相关的obj
    for i in pp_list:
        if i.Type == ObjectType.SOLE:
            res_dict[ObjectType.SOLE].append(i)
        elif i.Type == ObjectType.DRIV:
            res_dict[ObjectType.DRIV].append(i)
        elif i.Type == ObjectType.FOIL:
            res_dict[ObjectType.FOIL].append(i)
        elif i.Type == ObjectType.IND:
            res_dict[ObjectType.IND].append(i)
        elif i.Type == ObjectType.PORT:
            res_dict[ObjectType.PORT].append(i)
        elif i.Type == ObjectType.FREE:
            res_dict[ObjectType.FREE].append(i)
        elif i.Type == ObjectType.SYMT:
            res_dict[ObjectType.SYMT].append(i)
        # 发射处理
        elif i.Type == ObjectType.BEAM:
            res_dict[ObjectType.BEAM].append(i)
        elif i.Type == ObjectType.EXPS:
            res_dict[ObjectType.EXPS].append(i)
        elif i.Type == ObjectType.GYRO:
            res_dict[ObjectType.GYRO].append(i)
        elif i.Type == ObjectType.POPU:
            res_dict[ObjectType.POPU].append(i)
        elif i.Type == ObjectType.FELD:
            res_dict[ObjectType.FELD].append(i)
        elif i.Type == ObjectType.THER:
            res_dict[ObjectType.THER].append(i)
        elif i.Type == ObjectType.SECD:
            res_dict[ObjectType.SECD].append(i)
        elif i.Type == ObjectType.IONI:
            res_dict[ObjectType.IONI].append(i)
        elif i.Type == ObjectType.MacroParticle:
            res_dict[ObjectType.MacroParticle].append(i)

    return res_dict
