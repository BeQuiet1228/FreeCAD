# -*- coding: utf-8 -*-
#json格式数据需要保持原有顺序输出
from collections import OrderedDict

'''
根据物理设置，判断模型是否需要被隐藏
'''
from Modeling.Common.Tools import ObjectsTools
import FreeCAD
import json
def setVisibility(transparency=0):
    '''
    @ param :transparency 默认透明度为0
    @ return :返回所有被这些名引用的模型
    '''
    resObjsBeUsed=[]
    needCheckType=["Foil_Type","Ind_Type","Port_Type","Free_Type","Sym_Type"]
    #注意getAllObjectszofThisDocWithoutOrder是有序的
    orderedObjsWithoutOrderList=ObjectsTools.getAllObjectszofThisDocWithoutOrder(FreeCAD.ActiveDocument.Name)
    referedObjLabelWhitoutOrder=""
    JSON_CADComment = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict)
    items=JSON_CADComment.items()
    for key,value in items:
        referedObjLabelWhitoutOrder=""
        if "Dlg_Type" in value:
            if value["Dlg_Type"] in needCheckType:
                
                if value["Orthogonal_projection_surface"] in orderedObjsWithoutOrderList:
                    referedObjLabelWhitoutOrder=value["Orthogonal_projection_surface"]
                    # 
                    realLabelName="["+str(orderedObjsWithoutOrderList.index(value["Orthogonal_projection_surface"]))+"]_"+str(referedObjLabelWhitoutOrder)

                    objs=FreeCAD.ActiveDocument.getObjectsByLabel(realLabelName)
                    if len(objs)==1:
                        obj=objs[0]
                        obj.ViewObject.DisplayMode = u'Flat Lines'
                        obj.ViewObject.Visibility = True
                        obj.ViewObject.Transparency=transparency
                        resObjsBeUsed.append(obj)
                        
                    elif len(objs)<=0:
                        pass
                #对称面
                # 由于只有sym有该成员所以此处加个判断@lzg
                if value["Dlg_Type"] == "Sym_Type":
                    if value["Symmetric_projection_surface"] in orderedObjsWithoutOrderList:
                        referedObjLabelWhitoutOrder=value["Symmetric_projection_surface"]
                    # 
                        realLabelName="["+str(orderedObjsWithoutOrderList.index(value["Symmetric_projection_surface"]))+"]_"+str(referedObjLabelWhitoutOrder)

                        objs=FreeCAD.ActiveDocument.getObjectsByLabel(realLabelName)
                        if len(objs)==1:
                            obj=objs[0]
                            obj.ViewObject.DisplayMode = u'Flat Lines'
                            obj.ViewObject.Visibility = True
                            obj.ViewObject.Transparency=transparency
                            resObjsBeUsed.append(obj)
                        
                        elif len(objs)<=0:
                            pass
    return resObjsBeUsed