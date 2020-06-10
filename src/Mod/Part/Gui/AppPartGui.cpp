/***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU Library General Public License as       *
*   published by the Free Software Foundation; either version 2 of the    *
*   License, or (at your option) any later version.                       *
*   for detail see the LICENCE text file.                                 *
*   Juergen Riegel 2002                                                   *
*                                                                         *
***************************************************************************/


#include "PreCompiled.h"
#ifndef _PreComp_
# include <Standard_math.hxx>
# include <Inventor/system/inttypes.h>
#endif

#include <CXX/Extensions.hxx>
#include <CXX/Objects.hxx>

#include <Base/Console.h>
#include <Base/Interpreter.h>

#include <Gui/Application.h>
#include <Gui/BitmapFactory.h>
#include <Gui/WidgetFactory.h>
///
#include<Gui/Document.h>
#include<Gui/Application.h>
#include <Mod/Part/App/FeaturePartCut.h>
#include<Mod/Part/App/TopoShapePy.h>
#include <Mod/Part/App/FeaturePartFuse.h>
#include<Mod/Part/App/PropertyTopoShape.h>
#include<Mod/Part/App/PartFeature.h>
#include<Mod/Part/App/TopoShape.h>
//#include<Mod/Part/App/DocumentObjectPy.h>
#include<Mod/Part/App/modelRefine.h>
# include <BRepExtrema_DistShapeShape.hxx>
# include <BRepAlgoAPI_Cut.hxx>
# include <BRepAlgoAPI_Fuse.hxx>
# include <BRep_Builder.hxx>
#include<TopTools_IndexedMapOfShape.hxx>
# include <TopExp.hxx>
# include <TopoDS.hxx>
#include<Gui/ViewProviderDocumentObject.h>
///
#include<App/DocumentObjectPy.h>
# include <BRepLib_FindSurface.hxx>
# include <BRepAdaptor_Surface.hxx>
# include <TopExp_Explorer.hxx>
# include <gp_Pln.hxx>

#include "AttacherTexts.h"
#include "PropertyEnumAttacherItem.h"
#include "SoBrepFaceSet.h"
#include "SoBrepEdgeSet.h"
#include "SoBrepPointSet.h"
#include "SoFCShapeObject.h"
#include "ViewProvider.h"
#include "ViewProviderExt.h"
#include "ViewProviderPython.h"
#include "ViewProviderBox.h"
#include "ViewProviderCurveNet.h"
#include "ViewProviderImport.h"
#include "ViewProviderExtrusion.h"
#include "ViewProvider2DObject.h"
#include "ViewProviderMirror.h"
#include "ViewProviderBoolean.h"
#include "ViewProviderCompound.h"
#include "ViewProviderCircleParametric.h"
#include "ViewProviderLineParametric.h"
#include "ViewProviderPointParametric.h"
#include "ViewProviderEllipseParametric.h"
#include "ViewProviderHelixParametric.h"
#include "ViewProviderPlaneParametric.h"
#include "ViewProviderSphereParametric.h"
#include "ViewProviderCylinderParametric.h"
#include "ViewProviderConeParametric.h"
#include "ViewProviderTorusParametric.h"
#include "ViewProviderRuledSurface.h"
#include "ViewProviderPrism.h"
#include "ViewProviderSpline.h"
#include "ViewProviderRegularPolygon.h"
#include "TaskDimension.h"
#include "DlgSettingsGeneral.h"
#include "DlgSettingsObjectColor.h"
#include "DlgSettings3DViewPartImp.h"
#include "Workbench.h"



#include <Gui/Language/Translator.h>
#include<time.h>
#include "Resources/icons/PartFeature.xpm"
#include "Resources/icons/PartFeatureImport.xpm"

// use a different name to CreateCommand()
void CreatePartCommands(void);
void CreateSimplePartCommands(void);
void CreateParamPartCommands(void);

void loadPartResource()
{
	// add resources and reloads the translators
	Q_INIT_RESOURCE(Part);
	Gui::Translator::instance()->refresh();
}

namespace PartGui {
	class Module : public Py::ExtensionModule<Module>
	{
	public:
		Module() : Py::ExtensionModule<Module>("PartGui")
		{
			/*add_varargs_method("updateBoolean", &Module::updateBoolean,
				"updateBoolean(int order) -- refresh the boolean from order"
				);*/
			add_varargs_method("updateBoolean", &Module::updateBooleanLast,
				"updateBoolean(int order) -- refresh the boolean from order"
				);
			add_varargs_method("customBoolean", &Module::customBoolean,
				"customBoolean([list]) -- refresh the boolean from order"
				);
			add_varargs_method("getPointsOfObj", &Module::getPointsOfObj,
				"getPointsOfObj -- Helper method to convert a pythonocc shape to an internal shape"
				);

			initialize("This module is the PartGui module."); // register with Python
		}
		virtual ~Module() {}

	private:
		/*布尔sub*/
		//void booleanSub(TopoDS_Shape &resultShape, TopoDS_Shape theFirstShap, TopoDS_Shape theSecondShape){

		//	if (theFirstShap.IsNull() || theSecondShape.IsNull()){
		//		std::cerr << "baseShape or toolShape is Null!" << std::endl;
		//	}
		//	BRepAlgoAPI_Cut mkCut(theFirstShap, theSecondShape);
		//	if (!mkCut.IsDone())
		//		std::cerr << "Cut out failed!" << std::endl;
		//	//return new App::DocumentObjectExecReturn("Cut out failed");
		//	TopoDS_Shape shap = mkCut.Shape();
		//	resultShape = shap;
		//}
		/*布尔add one: resultShape=resultShape+shape*/
		void booleanAddOne(TopoDS_Shape &resultShape, TopoDS_Shape addShape){
			if (resultShape.IsNull()){
				resultShape = addShape;
				return;
			}
			if (addShape.IsNull()){
				return;
			}
			TopoDS_Shape temp = resultShape;

			BRepAlgoAPI_Fuse mkFuse;
			TopTools_ListOfShape shapeArguments, shapeTools;
			const TopoDS_Shape& shape = temp;
			if (shape.IsNull())
				std::cerr << "input shap is null" << std::endl;
			//throw Base::RuntimeError("Input shape is null");
			shapeArguments.Append(shape);


			shapeTools.Append(addShape);

			mkFuse.SetArguments(shapeArguments);
			mkFuse.SetTools(shapeTools);
			mkFuse.Build();
			if (!mkFuse.IsDone())
				throw Base::RuntimeError("MultiFusion failed");
			// 所有真空的联合体
			temp = mkFuse.Shape();
			resultShape = temp;
		}
		/*布尔add resultShape=resultShape+add(shapeList)*/
		void booleanAddShapes(TopoDS_Shape &resultShape, std::vector<TopoDS_Shape> shapeList){
			TopoDS_Shape temp = resultShape;
			if (shapeList.size() == 0)
				return;
			else if (shapeList.size() == 1){
				resultShape = shapeList[0];
				return;
				//booleanAddOne(resultShape, shapeList[0]);
			}
			else{
				BRepAlgoAPI_Fuse mkFuse;
				TopTools_ListOfShape shapeArguments, shapeTools;
				const TopoDS_Shape& shape = shapeList[0];
				if (shape.IsNull())
					std::cerr << "input shap is null" << std::endl;
				//throw Base::RuntimeError("Input shape is null");
				shapeArguments.Append(shape);

				for (std::vector<TopoDS_Shape>::iterator it = shapeList.begin() + 1; it != shapeList.end(); ++it) {
					if (it->IsNull())
					{
						std::cerr << "input shape is null" << std::endl;
						//throw Base::RuntimeError("Input shape is null");
					}
					shapeTools.Append(*it);
				}

				mkFuse.SetArguments(shapeArguments);
				mkFuse.SetTools(shapeTools);
				mkFuse.Build();
				if (!mkFuse.IsDone())
					throw Base::RuntimeError("MultiFusion failed");
				// 所有真空的联合体
				resultShape = mkFuse.Shape();
			}
		}
		Part::ShapeHistory buildHistory(BRepBuilderAPI_MakeShape& mkShape, TopAbs_ShapeEnum type,
			const TopoDS_Shape& newS, const TopoDS_Shape& oldS)
		{
			Part::ShapeHistory history;
			history.type = type;

			TopTools_IndexedMapOfShape newM, oldM;
			TopExp::MapShapes(newS, type, newM); // map containing all old objects of type "type"
			TopExp::MapShapes(oldS, type, oldM); // map containing all new objects of type "type"

			// Look at all objects in the old shape and try to find the modified object in the new shape
			for (int i = 1; i <= oldM.Extent(); i++) {
				bool found = false;
				TopTools_ListIteratorOfListOfShape it;
				// Find all new objects that are a modification of the old object (e.g. a face was resized)
				for (it.Initialize(mkShape.Modified(oldM(i))); it.More(); it.Next()) {
					found = true;
					for (int j = 1; j <= newM.Extent(); j++) { // one old object might create several new ones!
						if (newM(j).IsPartner(it.Value())) {
							history.shapeMap[i - 1].push_back(j - 1); // adjust indices to start at zero
							break;
						}
					}
				}

				// Find all new objects that were generated from an old object (e.g. a face generated from an edge)
				for (it.Initialize(mkShape.Generated(oldM(i))); it.More(); it.Next()) {
					found = true;
					for (int j = 1; j <= newM.Extent(); j++) {
						if (newM(j).IsPartner(it.Value())) {
							history.shapeMap[i - 1].push_back(j - 1);
							break;
						}
					}
				}

				if (!found) {
					// Find all old objects that don't exist any more (e.g. a face was completely cut away)
					if (mkShape.IsDeleted(oldM(i))) {
						history.shapeMap[i - 1] = std::vector<int>();
					}
					else {
						// Mop up the rest (will this ever be reached?)
						for (int j = 1; j <= newM.Extent(); j++) {
							if (newM(j).IsPartner(oldM(i))) {
								history.shapeMap[i - 1].push_back(j - 1);
								break;
							}
						}
					}
				}
			}

			return history;
		}
		Part::ShapeHistory joinHistory(const Part::ShapeHistory& oldH, const Part::ShapeHistory& newH)
		{
			Part::ShapeHistory join;
			join.type = oldH.type;

			for (Part::ShapeHistory::MapList::const_iterator it = oldH.shapeMap.begin(); it != oldH.shapeMap.end(); ++it) {
				int old_shape_index = it->first;
				if (it->second.empty())
					join.shapeMap[old_shape_index] = Part::ShapeHistory::List();
				for (Part::ShapeHistory::List::const_iterator jt = it->second.begin(); jt != it->second.end(); ++jt) {
					Part::ShapeHistory::MapList::const_iterator kt = newH.shapeMap.find(*jt);
					if (kt != newH.shapeMap.end()) {
						Part::ShapeHistory::List& ary = join.shapeMap[old_shape_index];
						ary.insert(ary.end(), kt->second.begin(), kt->second.end());
					}
				}
			}
			return join;
		}
		void applyTransparency(const float& transparency,
			std::vector<App::Color>& colors)
		{
			if (transparency != 0.0) {
				// transparency has been set object-wide
				std::vector<App::Color>::iterator j;
				for (j = colors.begin(); j != colors.end(); ++j) {
					// transparency hasn't been set for this face
					if (j->a == 0.0)
						j->a = transparency / 100.0; // transparency comes in percent
				}
			}
		}
		void applyColor(const Part::ShapeHistory& hist,
			const std::vector<App::Color>& colBase,
			std::vector<App::Color>& colBool)
		{
			std::map<int, std::vector<int> >::const_iterator jt;
			// apply color from modified faces
			for (jt = hist.shapeMap.begin(); jt != hist.shapeMap.end(); ++jt) {
				std::vector<int>::const_iterator kt;
				for (kt = jt->second.begin(); kt != jt->second.end(); ++kt) {
					if (*kt >= colBool.size() || jt->first >= colBase.size())
					{
						std::cerr << "out of size()" << std::endl;
						continue;
					}
					colBool[*kt] = colBase[jt->first];
				}
			}
		}
		void booleanSub(App::DocumentObject &resultObj, App::DocumentObject* obj1, App::DocumentObject* obj2)
		{
			if (!obj1 || !obj2){
				return;
			}
			Part::PropertyShapeHistory* resultHistory = (Part::PropertyShapeHistory*)(&resultObj)->getPropertyByName("History");
			TopoDS_Shape resultShape;
			TopoDS_Shape shape1 = static_cast<Part::Feature*>(obj1)->Shape.getValue();
			TopoDS_Shape shape2 = static_cast<Part::Feature*>(obj2)->Shape.getValue();

			if (shape1.IsNull() || shape2.IsNull()){
				return;
				//throw Base::RuntimeError("baseShape or toolShape is Null!");
			}
			else if (shape1.IsNull()){
				obj1 = obj2;
			}
			else if (shape2.IsNull()){
				obj2 = obj1;
			}
			else if (shape1.IsEqual(shape2)){
				cerr << "equal" << std::endl;
			}
			else if (shape1.IsSame(shape2)){
				cerr << "same" << std::endl;
			}
			shape1 = static_cast<Part::Feature*>(obj1)->Shape.getValue();
			shape2 = static_cast<Part::Feature*>(obj2)->Shape.getValue();
			std::unique_ptr<BRepAlgoAPI_BooleanOperation> mkBool((BRepAlgoAPI_BooleanOperation*)new BRepAlgoAPI_Cut(shape1, shape2));
			//BRepAlgoAPI_Cut mkCut(shape1, shape2);
			if (!mkBool->IsDone())
				throw Base::RuntimeError("Cut out failed!");
			//return new App::DocumentObjectExecReturn("Cut out failed");
			resultShape = mkBool->Shape();
			//resultShape = shap;

			///
			

			std::vector<Part::ShapeHistory> history;
			history.push_back(buildHistory(*mkBool.get(), TopAbs_FACE, resultShape, shape1));
			history.push_back(buildHistory(*mkBool.get(), TopAbs_FACE, resultShape, shape2));
			///refine
			if (true) {
				try {
					TopoDS_Shape oldShape = resultShape;
					Part::BRepBuilderAPI_RefineModel mkRefine(oldShape);
					resultShape = mkRefine.Shape();
					Part::ShapeHistory hist = buildHistory(mkRefine, TopAbs_FACE, resultShape, oldShape);
					history[0] = joinHistory(history[0], hist);
					history[1] = joinHistory(history[1], hist);
				}
				catch (Standard_Failure) {
					// do nothing
				}
			}
			///
			static_cast<Part::Feature*>(&resultObj)->Shape.setValue(resultShape);
			resultHistory->setValues(history);

			const std::vector<Part::ShapeHistory>& hist = resultHistory->getValues();
			if (hist.size() != 2)
				return;

			Part::Feature* objBool = dynamic_cast<Part::Feature*>(&resultObj);
			Part::Feature* objBase = dynamic_cast<Part::Feature*>(obj1);
			Part::Feature* objTool = dynamic_cast<Part::Feature*>(obj2);
			if (objBase && objTool) {
				const TopoDS_Shape& baseShape = objBase->Shape.getValue();
				const TopoDS_Shape& toolShape = objTool->Shape.getValue();
				const TopoDS_Shape& boolShape = objBool->Shape.getValue();

				TopTools_IndexedMapOfShape baseMap, toolMap, boolMap;
				TopExp::MapShapes(baseShape, TopAbs_FACE, baseMap);
				TopExp::MapShapes(toolShape, TopAbs_FACE, toolMap);
				TopExp::MapShapes(boolShape, TopAbs_FACE, boolMap);

				Gui::ViewProvider* vpBase = Gui::Application::Instance->getViewProvider(objBase);
				Gui::ViewProvider* vpTool = Gui::Application::Instance->getViewProvider(objTool);
				Gui::ViewProviderGeometryObject* vpg = static_cast<Gui::ViewProviderGeometryObject*>(Gui::Application::Instance->getViewProvider(&resultObj));
				if (vpBase && vpTool) {
					std::vector<App::Color> colBase = static_cast<PartGui::ViewProviderPart*>(vpBase)->DiffuseColor.getValues();
					std::vector<App::Color> colTool = static_cast<PartGui::ViewProviderPart*>(vpTool)->DiffuseColor.getValues();
					std::vector<App::Color> colBool;
					colBool.resize(boolMap.Extent(), vpg->ShapeColor.getValue());
					applyTransparency(static_cast<PartGui::ViewProviderPart*>(vpBase)->Transparency.getValue(), colBase);
					applyTransparency(static_cast<PartGui::ViewProviderPart*>(vpTool)->Transparency.getValue(), colTool);

					if (static_cast<int>(colBase.size()) == baseMap.Extent()) {
						applyColor(hist[0], colBase, colBool);
					}
					else if (!colBase.empty() && colBase[0] != vpg->ShapeColor.getValue()) {
						colBase.resize(baseMap.Extent(), colBase[0]);
						applyColor(hist[0], colBase, colBool);
					}

					if (static_cast<int>(colTool.size()) == toolMap.Extent()) {
						applyColor(hist[1], colTool, colBool);
					}
					else if (!colTool.empty() && colTool[0] != vpg->ShapeColor.getValue()) {
						colTool.resize(toolMap.Extent(), colTool[0]);
						applyColor(hist[1], colTool, colBool);
					}
					Gui::ViewProvider* vp = Gui::Application::Instance->getViewProvider(&resultObj);
					static_cast<PartGui::ViewProviderPart*>(vp)->DiffuseColor.setValues(colBool);
				}
			}
			///
		}
		void booleanAdd(App::DocumentObject &resultObj, App::DocumentObject* obj1, App::DocumentObject* obj2)
		{
			TopoDS_Shape shape1 = static_cast<Part::Feature*>(obj1)->Shape.getValue();
			TopoDS_Shape shape2 = static_cast<Part::Feature*>(obj2)->Shape.getValue();
			//两者都为空
			if ((!obj1&&!obj2) || (shape1.IsNull() && shape2.IsNull())){
				return;
			}
			else if ((!obj1&&obj2) || (shape1.IsNull() && !shape2.IsNull())){
				obj1 = obj2;
				//static_cast<Part::Feature*>(&resultObj)->Shape.setValue(static_cast<Part::Feature*>(obj2)->Shape.getValue());

			}
			else if ((obj1&&!obj2) || (!shape1.IsNull() && shape2.IsNull()))
			{
				obj2 = obj1;
			}
			Part::PropertyShapeHistory* resultHistory = (Part::PropertyShapeHistory*)(&resultObj)->getPropertyByName("History");
			shape1 = static_cast<Part::Feature*>(obj1)->Shape.getValue();
			shape2 = static_cast<Part::Feature*>(obj2)->Shape.getValue();

			TopoDS_Shape resultShape;
			BRepAlgoAPI_Fuse mkFuse;
			TopTools_ListOfShape shapeArguments, shapeTools;
			const TopoDS_Shape& shape = shape1;
			if (shape.IsNull())
				throw Base::RuntimeError("input shap is null");
			//throw Base::RuntimeError("Input shape is null");
			shapeArguments.Append(shape);

			shapeTools.Append(shape2);

			mkFuse.SetArguments(shapeArguments);
			mkFuse.SetTools(shapeTools);
			mkFuse.Build();
			if (!mkFuse.IsDone())
				throw Base::RuntimeError("MultiFusion failed");
			resultShape = mkFuse.Shape();
			
			///
			std::vector<Part::ShapeHistory> history;
			history.push_back(buildHistory(mkFuse, TopAbs_FACE, resultShape, shape1));
			history.push_back(buildHistory(mkFuse, TopAbs_FACE, resultShape, shape2));
			///refine
			if (true) {
				try {
					TopoDS_Shape oldShape = resultShape;
					
					Part::BRepBuilderAPI_RefineModel mkRefine(oldShape);
					resultShape = mkRefine.Shape();
					Part::ShapeHistory hist = buildHistory(mkRefine, TopAbs_FACE, resultShape, oldShape);
					for (std::vector<Part::ShapeHistory>::iterator jt = history.begin(); jt != history.end(); ++jt)
						*jt = joinHistory(*jt, hist);
				}
				catch (Standard_Failure) {
					// do nothing
				}
			}
			///
			static_cast<Part::Feature*>(&resultObj)->Shape.setValue(resultShape);
			resultHistory->setValues(history);
			///
			const std::vector<Part::ShapeHistory>& hist = history;
			const TopoDS_Shape& boolShape = static_cast<Part::MultiFuse*>(&resultObj)->Shape.getValue();
			TopTools_IndexedMapOfShape boolMap;
			TopExp::MapShapes(boolShape, TopAbs_FACE, boolMap);

			Gui::ViewProviderGeometryObject* vpg = dynamic_cast<Gui::ViewProviderGeometryObject*>(Gui::Application::Instance->getViewProvider(&resultObj));
			std::vector<App::Color> colBool;
			colBool.resize(boolMap.Extent(), vpg->ShapeColor.getValue());

			std::vector<App::DocumentObject*> sources;
			sources.push_back(obj1);
			sources.push_back(obj2);
			int index = 0;
			for (std::vector<App::DocumentObject*>::iterator it = sources.begin(); it != sources.end(); ++it, ++index) {
				Part::Feature* objBase = static_cast<Part::Feature*>(*it);
				if (!objBase)
					continue;
				const TopoDS_Shape& baseShape = objBase->Shape.getValue();

				TopTools_IndexedMapOfShape baseMap;
				TopExp::MapShapes(baseShape, TopAbs_FACE, baseMap);

				Gui::ViewProvider* vpBase = Gui::Application::Instance->getViewProvider(objBase);
				if (vpBase) {
					std::vector<App::Color> colBase = static_cast<PartGui::ViewProviderPart*>(vpBase)->DiffuseColor.getValues();
					applyTransparency(static_cast<PartGui::ViewProviderPart*>(vpBase)->Transparency.getValue(), colBase);
					if (static_cast<int>(colBase.size()) == baseMap.Extent()) {
						//colBase Shapes单个对应的<App::Color>
						//colBool 最终的<App::Color>
						applyColor(hist[index], colBase, colBool);
					}
					else if (!colBase.empty() && colBase[0] != vpg->ShapeColor.getValue()) {
						colBase.resize(baseMap.Extent(), colBase[0]);
						applyColor(hist[index], colBase, colBool);
					}
				}
			}
			Gui::ViewProvider* vp = Gui::Application::Instance->getViewProvider(&resultObj);
			static_cast<PartGui::ViewProviderPart*>(vp)->DiffuseColor.setValues(colBool);
			//////
		}
		void booleanAdd2(Part::MultiFuse &resultObj, App::DocumentObject* obj1, App::DocumentObject* obj2)
		{
			std::vector<App::DocumentObject*> objs;
			objs.push_back(obj1);
			objs.push_back(obj2);
			resultObj.Shapes.setValues(objs);
		}
		void booleanSub2(Part::Cut &resultObj, App::DocumentObject*obj1, App::DocumentObject*obj2){
			resultObj.Base.setValue(obj1);
			resultObj.Tool.setValue(obj2);
		}
		//复制Shape和DiffuseColor
		void copyDocumentObj(App::DocumentObject&finalObj, std::vector<App::Color>& color, float& transparency, App::DocumentObject* beCopyObj){
			static_cast<Part::Feature*>(&finalObj)->Shape.setValue(static_cast<Part::Feature*>(beCopyObj)->Shape.getValue());

			Gui::ViewProvider* vpBase = Gui::Application::Instance->getViewProvider(beCopyObj);
			color = static_cast<PartGui::ViewProviderPart*>(vpBase)->DiffuseColor.getValues();
			transparency = static_cast<PartGui::ViewProviderPart*>(vpBase)->Transparency.getValue();
			//vp =(Gui::Application::Instance->getViewProvider(beCopyObj));
		}
		Py::Object updateBoolean(const Py::Tuple& args)
		{
			DWORD start, stop;
			start = GetTickCount();
			std::cerr << "start boolean" << std::endl;
			int changedOrder = 0;
			if (!PyArg_ParseTuple(args.ptr(), "|i", &changedOrder))
				return Py::None();
			App::Document* pcDoc;
			pcDoc = App::GetApplication().getActiveDocument();
			Gui::Document *guiPcDoc = Gui::Application::Instance->activeDocument();
			//Gui::Document *guiPcDoc = Gui::Application::Instance->activeDocument();
			if (pcDoc == NULL){
				return Py::None();
			}
			App::DocumentObject* resultObj = NULL;
			std::vector<App::DocumentObject*> topoSortedObjects = pcDoc->topologicalSort();
			std::map<int, Gui::BooleanObjects> bObjsMap = (guiPcDoc->booleanObjectMap);
			std::map<int, Gui::BooleanObjects> tempMap = bObjsMap;
			for (std::map<int, Gui::BooleanObjects>::const_iterator it = tempMap.begin(); it != tempMap.end(); ++it){
				if ((it)->first>= changedOrder)
					bObjsMap.erase((it)->first);
			}
			//所有需要做布尔运算的模型，即有Attribute且不为未定义的模型
			//std::vector<std::pair<App::DocumentObject*,std::string>> objsList;
			std::map<int, App::DocumentObject*> objsMap;
			for (auto objIt = topoSortedObjects.rbegin(); objIt != topoSortedObjects.rend(); ++objIt){
				if (strcmp((*objIt)->getNameInDocument(), "ResultShape") == 0){
					resultObj = (*objIt);
				}
				std::vector<App::Property*>propList;
				std::vector<std::string>propNames;
				(*objIt)->getPropertyList(propList);
				propNames=(*objIt)->getDynamicPropertyNames();
				if (propList.size() < 20){
					continue;
				}
				
				std::vector<App::Property*>::iterator pt;
				for (auto pt = propList.begin(); pt != propList.end(); ++pt){
					const char* name = (*pt)->getName();
					if (strcmp((*pt)->getName(), "Attribute") == 0 && !((App::PropertyEnumeration*)*pt)->isValue("NotDefine")){
						//std::string objAttr = ((App::PropertyEnumeration*)*pt)->getValueAsString();
						std::vector<std::string>::iterator ret;
						ret = std::find(propNames.begin(), propNames.end(), "Order");
						//没有Order属性
						if (ret == propNames.end())
							continue;
						int orderOfObj = ((App::PropertyInteger*)(*objIt)->getPropertyByName("Order"))->getValue();
						objsMap[orderOfObj] = (*objIt);
						//objsList.push_back(std::make_pair((*objIt),objAttr));
						break;
					}
					//删除属性是未定义的模型的map
					else if (strcmp((*pt)->getName(), "Attribute") == 0 && ((App::PropertyEnumeration*)*pt)->isValue("NotDefine"))
					{
						std::vector<std::string>::iterator ret;
						ret = std::find(propNames.begin(), propNames.end(), "Order");
						//没有Order属性
						if (ret == propNames.end())
							continue;
						int orderOfObj = ((App::PropertyInteger*)(*objIt)->getPropertyByName("Order"))->getValue();
						if (bObjsMap.find(orderOfObj) != bObjsMap.end()){
							bObjsMap.erase(orderOfObj);
						}
					}
					if (strcmp((*pt)->getName(), "realShape") == 0)
					{
						TopoDS_Shape realShape = ((Part::PropertyPartShape*)(*objIt)->getPropertyByName("realShape"))->getValue();
					}
				}
			}
			//if (objsMap.size() == 0){
			//	return Py::None();
			//}
			if (!resultObj){
				resultObj = pcDoc->addObject("Part::FeaturePython", "ResultShape");
				//App::PropertyPythonObject* Proxy  = static_cast<App::PropertyPythonObject*>(resultObj->getPropertyByName("Proxy"));
				//Proxy->setValue(0);
				////Gui::ViewProviderDocumentObject*vpDocObj = new Gui::ViewProviderDocumentObject();
				////Gui::ViewProviderPythonFeatureImp* vp = new Gui::ViewProviderPythonFeatureImp(vpDocObj);
				////vp->attach(resultObj);
				//return Py::None();
			}
			//guiPcDoc->setHide("ResultShape");
			static_cast<Part::Feature*>(resultObj)->Shape.setValue(*(new TopoDS_Shape()));


			App::DocumentObject *pcLastConductorObj = NULL;
			std::vector<App::DocumentObject*> vacuoList;
			std::vector<App::DocumentObject*> conductorList;
			//Part::MultiFuse resultMultiFuse;
			//lastOne 0:初始；1:上一个是导体；2:上一个是真空
			int lastOne = 0;
			
			int startOrder = -1;
			if (bObjsMap.size() > 0 && changedOrder != 0)
			{
				if (changedOrder != bObjsMap.begin()->first){
					std::map<int, Gui::BooleanObjects>::iterator itfinal = bObjsMap.begin();
					std::map<int, Gui::BooleanObjects>::iterator it = bObjsMap.begin();
					while (it != bObjsMap.end() && it->first < changedOrder){
						startOrder = it->first;
						itfinal = it;
						++it;
					}

					static_cast<Part::Feature*>(resultObj)->Shape.setValue(static_cast<Part::Feature*>(itfinal->second.curResultObj)->Shape.getValue());
					Gui::ViewProvider* vpBase = Gui::Application::Instance->getViewProvider(resultObj);
					static_cast<PartGui::ViewProviderPart*>(vpBase)->DiffuseColor.setValues(itfinal->second.curDiffuseCol);
					static_cast<PartGui::ViewProviderPart*>(vpBase)->Transparency.setValue(itfinal->second.curTransparency);
				}
			}
			else if (bObjsMap.size() == 0){
				static_cast<Part::Feature*>(resultObj)->Shape.setValue(*(new TopoDS_Shape()));
			}
			for (std::map<int, App::DocumentObject*>::const_iterator it = objsMap.begin(); it != objsMap.end(); ++it){
				guiPcDoc->setHide(it->second->getNameInDocument());
				int objOrder = ((App::PropertyInteger*)(it->second->getPropertyByName("Order")))->getValue();
				if (objOrder <= startOrder){
					continue;
				}
				Part::Feature *lastResultObj = new Part::Feature();
				std::vector<App::Color> lastColor;
				float lastTransparency = 0.0;

				copyDocumentObj(*lastResultObj, lastColor, lastTransparency, resultObj);

				std::string attrOfObj = ((App::PropertyEnumeration*)(it->second->getPropertyByName("Attribute")))->getValueAsString();
				if ((strcmp(attrOfObj.c_str(), "Conductor") == 0) || (strcmp(attrOfObj.c_str(), "Custom") == 0)){
					booleanAdd(*resultObj, resultObj, it->second);

					Part::Feature *curResultObj = new Part::Feature();
					std::vector<App::Color> curColor;
					float curTransparency = 0.0;

					copyDocumentObj(*curResultObj, curColor, curTransparency, resultObj);

					Gui::BooleanObjects bo = { objOrder, lastResultObj, lastColor, lastTransparency, curResultObj, curColor, curTransparency };
					bObjsMap[objOrder] = bo;
				}
				else{
					booleanSub(*resultObj, resultObj, it->second);

					Part::Feature *curResultObj = new Part::Feature();
					std::vector<App::Color> curColor;
					float curTransparency = 0.0;

					copyDocumentObj(*curResultObj, curColor, curTransparency, resultObj);

					Gui::BooleanObjects bo = { objOrder, lastResultObj, lastColor, lastTransparency, curResultObj, curColor, curTransparency };
					bObjsMap[objOrder] = bo;
				}
			}
			guiPcDoc->setShow(resultObj->getNameInDocument());
			guiPcDoc->booleanObjectMap = bObjsMap;
			pcDoc->recompute();
			pcDoc->flagNeedUpdateBoolean.setValue(-1);
			std::cerr << "start end" << std::endl;

			stop = GetTickCount();
			cerr << "bool time:" << (stop - start)*1.0 / 1000 << endl;
			return Py::None();
		}
		/*关于PropertyShapeHistory:它主要用于存储参与运算的模型的面片对应关系，首先它是一个vector容器，假设变量名为shapeHistory。
		一般来说，有几个模型与这个最终的有关，它的size就有几个，它的每一个子元素shapeHistory[i]表示最终的面片与第i个模型之间的
		面片对应关系。例如：
		shapeHistory[0]={<0,<0>>,<1,<1>>,<2,<3>>},表示第一个模型与最终模型的面片对应关系,
		最终模型的第0个面片与该模型的第0个面片重合（颜色要一样）；
		            1                  1                        ；
					3                  2                        ；*/
		//设置联合体的形状
		void setCompoundShape(App::DocumentObject *compoundObj, const std::vector<App::DocumentObject*> &objs, const std::vector<TopoDS_Shape>&finalShapes)
		{
			try {
				std::vector<Part::ShapeHistory> history;
				int countFaces = 0;

				BRep_Builder builder;
				TopoDS_Compound comp;
				builder.MakeCompound(comp);

				const std::vector<App::DocumentObject*>& links = objs;
				//for (std::vector<App::DocumentObject*>::const_iterator it = links.begin(); it != links.end(); ++it) {
				for (std::vector<TopoDS_Shape>::const_iterator it = finalShapes.begin(); it != finalShapes.end(); ++it) {

					//if (*it && (*it)->getTypeId().isDerivedFrom(Part::Feature::getClassTypeId())) {
						//Part::Feature* fea = static_cast<Part::Feature*>(*it);
						const TopoDS_Shape& sh = *it;
						if (!sh.IsNull()) {
							builder.Add(comp, sh);
							TopTools_IndexedMapOfShape faceMap;
							TopExp::MapShapes(sh, TopAbs_FACE, faceMap);
							Part::ShapeHistory hist;
							hist.type = TopAbs_FACE;
							for (int i = 1; i <= faceMap.Extent(); i++) {
								hist.shapeMap[i - 1].push_back(countFaces++);
							}
							history.push_back(hist);
						}
					//}
				}
				static_cast<Part::Feature*>(compoundObj)->Shape.setValue(comp);


				Part::PropertyShapeHistory* resultHistory = (Part::PropertyShapeHistory*)(compoundObj)->getPropertyByName("History");
				resultHistory->setValues(history);
				if (resultHistory)
					std::cout << "Yse" << std::endl;
				else
					std::cout << "No" << std::endl;
			}
			catch (Standard_Failure& e) {
				std::cerr << "makeCompound wrong" << endl;
				//return new App::DocumentObjectExecReturn(e.GetMessageString());
			}
		}
		//设置联合体的颜色
		void setCompoundColor(App::DocumentObject *compoundObj, 
							 const std::vector<App::DocumentObject*> &objs,
							 const std::vector<TopoDS_Shape> &shapeOfCon,
							 const std::vector<App::Color> &colorOfCon){
			if (objs.size() == 0){
				return;
			}
			Part::PropertyShapeHistory* resultHistory = (Part::PropertyShapeHistory*)(compoundObj)->getPropertyByName("History");
			const std::vector<Part::ShapeHistory>& hist = resultHistory->getValues();

			Part::Feature*compoundFeaure=static_cast<Part::Feature*>(compoundObj);
			const TopoDS_Shape& compShape = compoundFeaure->Shape.getValue();
			TopTools_IndexedMapOfShape compMap;
			TopExp::MapShapes(compShape, TopAbs_FACE, compMap);

			std::vector<App::Color> compCol;
			Gui::ViewProviderGeometryObject* vpg = static_cast<Gui::ViewProviderGeometryObject*>(Gui::Application::Instance->getViewProvider(compoundObj));
			compCol.resize(compMap.Extent(), vpg->ShapeColor.getValue());
			Gui::ViewProvider* vp = Gui::Application::Instance->getViewProvider(compoundObj);
			//int index = 0;
			/*for (std::vector<App::DocumentObject*>::const_iterator it = objs.begin(); it != objs.end(); ++it, ++index) {
				Part::Feature* objBase = dynamic_cast<Part::Feature*>(*it);
				if (!objBase)
					continue;

				const TopoDS_Shape& baseShape = objBase->Shape.getValue();

				TopTools_IndexedMapOfShape baseMap;
				TopExp::MapShapes(baseShape, TopAbs_FACE, baseMap);

				Gui::ViewProvider* vpBase = Gui::Application::Instance->getViewProvider(objBase);
				std::vector<App::Color> baseCol = static_cast<PartGui::ViewProviderPart*>(vpBase)->DiffuseColor.getValues();
				applyTransparency(static_cast<PartGui::ViewProviderPart*>(vpBase)->Transparency.getValue(), baseCol);
				if (static_cast<int>(baseCol.size()) == baseMap.Extent()) {
					applyColor(hist[index], baseCol, compCol);
				}
				else if (!baseCol.empty() && baseCol[0] != vpg->ShapeColor.getValue()) {
					baseCol.resize(baseMap.Extent(), baseCol[0]);
					applyColor(hist[index], baseCol, compCol);
				}
			}*/
			int index = 0;
			std::vector<TopoDS_Shape>::const_iterator shIt = shapeOfCon.begin();
			std::vector<App::Color>::const_iterator colIt = colorOfCon.begin();
			for (; shIt != shapeOfCon.end() || colIt != colorOfCon.end(); ++shIt, ++colIt,++index)
			{
				if ((*shIt).IsNull())
					continue;

				TopTools_IndexedMapOfShape baseMap;
				TopExp::MapShapes(*shIt, TopAbs_FACE, baseMap);
				std::vector<App::Color> baseCol;
				baseCol.push_back(*colIt);

				if (static_cast<int>(baseCol.size()) == baseMap.Extent()) {
					applyColor(hist[index], baseCol, compCol);
				}
				else if (!baseCol.empty() && baseCol[0] != vpg->ShapeColor.getValue()) {
					baseCol.resize(baseMap.Extent(), baseCol[0]);
					applyColor(hist[index], baseCol, compCol);
				}
			}
			static_cast<PartGui::ViewProviderPart*>(vp)->DiffuseColor.setValues(compCol);
			//vp->DiffuseColor.setValues(compCol);
		}
		//因为上面这个布尔以后会出现黑色错误模型，所以尝试在这里改变bool的方式
		Py::Object updateBooleanLast(const Py::Tuple& args)
		{
			DWORD start, stop;
			start = GetTickCount();
			std::cerr << "start boolean"<<start << std::endl;

			int changedOrder = 0,reshow=0;

			if (!PyArg_ParseTuple(args.ptr(), "|ii", &changedOrder, &reshow))
				return Py::None();
			/*if (changedOrder == -1)
			{
				std::cout << "changedOrder==-1 break" << std::endl;
				return Py::None();
			}
			else{
				std::cout << "changedOrder="<<changedOrder << std::endl;
			}*/
				
			App::Document* pcDoc;
			Gui::Document *guiPcDoc = Gui::Application::Instance->activeDocument();
			pcDoc = App::GetApplication().getActiveDocument();
			App::DocumentObject* resultObj = NULL;
			std::vector<App::DocumentObject*> topoSortedObjects = pcDoc->topologicalSort();
			//所有需要做布尔运算的模型，即有Attribute且不为未定义的模型
			//std::vector<std::pair<App::DocumentObject*,std::string>> objsList;
			std::map<int, App::DocumentObject*> objsMap;
			for (auto objIt = topoSortedObjects.rbegin(); objIt != topoSortedObjects.rend(); ++objIt){

				if (strcmp((*objIt)->getNameInDocument(), "ResultShape") == 0){
					resultObj = (*objIt);
				}

				std::vector<App::Property*>propList;
				std::vector<std::string>propNames;
				(*objIt)->getPropertyList(propList);
				propNames = (*objIt)->getDynamicPropertyNames();
				if (propList.size() < 20){
					continue;
				}

				std::vector<App::Property*>::iterator pt;
				for (auto pt = propList.begin(); pt != propList.end(); ++pt){
					const char* name = (*pt)->getName();
					if (strcmp((*pt)->getName(), "Attribute") == 0 && !((App::PropertyEnumeration*)*pt)->isValue("NotDefine")){
						//std::string objAttr = ((App::PropertyEnumeration*)*pt)->getValueAsString();
						std::vector<std::string>::iterator ret;
						ret = std::find(propNames.begin(), propNames.end(), "Order");
						//没有Order属性
						if (ret == propNames.end())
							continue;
						int orderOfObj = ((App::PropertyInteger*)(*objIt)->getPropertyByName("Order"))->getValue();
						objsMap[orderOfObj] = (*objIt);
						//objsList.push_back(std::make_pair((*objIt),objAttr));
						break;
					}	
				}
			}
			static_cast<Part::Feature*>(resultObj)->Shape.setValue(*(new TopoDS_Shape()));
			//objsMap倒着查找，如果是真空，就加入vacuoShape列表，遇到实体，就用实体减去vacuoShape列表,最后用makeCompound组合最后的体
			std::vector<TopoDS_Shape> vacuoShapes;
			std::vector<TopoDS_Shape> finalShapes;

			std::vector<App::DocumentObject*> vacuoObjs;
			std::vector<App::DocumentObject*> finalObjs;
			std::vector<Part::ShapeHistory> historyOfCon;
			//存放导体属性的颜色
			std::vector<App::Color> ColorOfCon;
			for (std::map<int, App::DocumentObject*>::reverse_iterator it = objsMap.rbegin(); it != objsMap.rend(); ++it){
				guiPcDoc->setHide(it->second->getNameInDocument());
				TopoDS_Shape itShape = static_cast<Part::Feature*>(it->second)->Shape.getValue();
				if (itShape.IsNull())
					continue;
				//这个模型的属性string是什么
				std::string attrOfObj = ((App::PropertyEnumeration*)(it->second->getPropertyByName("Attribute")))->getValueAsString();
				if (strcmp(attrOfObj.c_str(), "Vacuo") == 0){
					vacuoShapes.push_back(itShape);
					vacuoObjs.push_back(it->second);
				}
				else if ((strcmp(attrOfObj.c_str(), "Conductor") == 0) || (strcmp(attrOfObj.c_str(), "Custom") == 0)){
					TopoDS_Shape finalShape;
					//测试
					clock_t t1, t2;
					if (vacuoShapes.size() != 0)
					{
						t1 = clock();
						std::cout << "t1:" << t1 << std::endl;
						std::cout << "order:" << it->first << "size of vocau:" << vacuoShapes.size() << endl;
						finalShape = Part::TopoShape(itShape).cut(vacuoShapes);
						t2 = clock();
						std::cout << "t2:" << t1 << std::endl;
						std::cout << "this cut: " << (t2 - t1) << std::endl;
					}
					else{
						finalShape = itShape;
					}
					
					finalShapes.push_back(finalShape);
					finalObjs.push_back(it->second);
					//加入颜色
					Part::Feature* objBase = dynamic_cast<Part::Feature*>(it->second);
					Gui::ViewProvider* vpBase = Gui::Application::Instance->getViewProvider(objBase);
					std::vector<App::Color> baseCol = static_cast<PartGui::ViewProviderPart*>(vpBase)->DiffuseColor.getValues();
					//因为每一个所有的形状只能是一种颜色
					if (baseCol.size() != 0)
						ColorOfCon.push_back(baseCol[0]);
					else
						//默认
						ColorOfCon.push_back(App::Color(0.80, 0.80, 0.80, 0.5));
				}
			}
			//测试
			clock_t t1, t2;
			
			//makeCompound
			BRep_Builder builder;
			TopoDS_Compound comp;
			builder.MakeCompound(comp);
			t1 = clock();
			std::cout << "compound start: " << t1 << std::endl;
			for (std::vector<TopoDS_Shape>::iterator it = finalShapes.begin(); it != finalShapes.end(); ++it){
				if (!(*it).IsNull())
					builder.Add(comp, *it);
			}
			/*TopoDS_Shape finalShape;
			if (finalShapes.size() != 0){
				if (finalShapes.size() == 1){
					finalShape = finalShapes[0];
				}
				else{
					Part::TopoShape *baseShape = new Part::TopoShape(finalShapes[finalShapes.size() - 1]);
					finalShapes.pop_back();
					finalShape = baseShape->fuse(finalShapes);
				}		
			}*/
			t2 = clock();
			std::cout << "compound end: " << t2 << std::endl;
			std::cout << "compound adll: " << (t2 - t1) << std::endl;
			//Part::TopoShape shape(comp);
			//将comp的shape给resultShape
			if (!resultObj){
				resultObj = pcDoc->addObject("Part::FeaturePython", "ResultShape");
			}

			if (finalShapes.size() != 0)
			{
				//static_cast<Part::Feature*>(resultObj)->Shape.setValue(comp);
				setCompoundShape(resultObj, finalObjs,finalShapes);
				//static_cast<Part::Feature*>(resultObj)->Shape.setValue(comp);
				setCompoundColor(resultObj, finalObjs,finalShapes, ColorOfCon);
			}
				
			


			//guiPcDoc->setShow(resultObj->getNameInDocument());
			//guiPcDoc->booleanObjectMap = bObjsMap;
			pcDoc->recompute();
			pcDoc->flagNeedUpdateBoolean.setValue(-1);

			

			stop = GetTickCount();
			std::cerr << "start end" << stop << std::endl;
			//cerr << "bool time:" << (stop - start)*1.0 / 1000 << endl;

			//stop = GetTickCount();
			//cerr << "bool time:" << (stop - start)*1.0 / 1000 << endl;
			return Py::None();
			;
		}
		////自定义Boolean
		Py::Object customBoolean(const Py::Tuple& args)
		{
			DWORD start, stop;
			start = GetTickCount();
			PyObject *pcObjsPy;
			PyObject *toolShapePy;
			PyObject *resultObjPy;
			int showCutFace;
			if (!PyArg_ParseTuple(args.ptr(), "OOOi", &pcObjsPy, &toolShapePy, &resultObjPy, &showCutFace))
				throw Py::Exception();
			const TopoDS_Shape& toolShape = static_cast<Part::TopoShapePy*>(toolShapePy)->getTopoShapePtr()->getShape();

			App::DocumentObject* resultObj = static_cast<App::DocumentObjectPy*>(resultObjPy)->getDocumentObjectPtr();

			App::Document* pcDoc = App::GetApplication().getActiveDocument();
			Gui::Document *guiPcDoc = Gui::Application::Instance->activeDocument();

			std::map<int, App::DocumentObject*> objsMap;

			DWORD s3, s4;
			s3 = GetTickCount();
			Py::Sequence list(pcObjsPy);
			App::DocumentObject* objItem;
			for (Py::Sequence::iterator it = list.begin(); it != list.end(); ++it) {
				PyObject* item = (*it).ptr();
				if (PyObject_TypeCheck(item, &(App::DocumentObjectPy::Type))) {
					App::DocumentObject* objItem = static_cast<App::DocumentObjectPy*>(item)->getDocumentObjectPtr();

					if (strcmp(objItem->getNameInDocument(), "Generated__cross_section") == 0){
						resultObj = objItem;
					}

					std::vector<App::Property*>propList;
					std::vector<std::string>propNames;
					objItem->getPropertyList(propList);
					propNames = objItem->getDynamicPropertyNames();
					if (propList.size() < 20){
						continue;
					}
					//判断模型可见性
					Part::Feature* objBase = dynamic_cast<Part::Feature*>(objItem);
					Gui::ViewProvider* vpBase = Gui::Application::Instance->getViewProvider(objBase);
					Gui::ViewProviderDocumentObject* vpObj = static_cast<Gui::ViewProviderDocumentObject*> (vpBase);
					//bool isVisible = false;
					//if (vpObj)
					//{
					//	isVisible = vpObj->Visibility.getValue();
					//}

					std::vector<App::Property*>::iterator pt;
					for (auto pt = propList.begin(); pt != propList.end(); ++pt){

						const char* name = (*pt)->getName();
						//要么是非未定义，要么是未定义但是，是可见的模型
						if (strcmp((*pt)->getName(), "Attribute") == 0){
							//std::string objAttr = ((App::PropertyEnumeration*)*pt)->getValueAsString();
							std::vector<std::string>::iterator ret;
							ret = std::find(propNames.begin(), propNames.end(), "Order");
							//没有Order属性
							if (ret == propNames.end())
								continue;
							int orderOfObj = ((App::PropertyInteger*)(objItem)->getPropertyByName("Order"))->getValue();
							objsMap[orderOfObj] = (objItem);
							//objsList.push_back(std::make_pair((*objIt),objAttr));
							break;
						}
					}
				}
			}

			//std::vector<App::DocumentObject*> topoSortedObjects = pcDoc->topologicalSort();
			////所有需要做布尔运算的模型，即有Attribute且不为未定义的模型
			////std::vector<std::pair<App::DocumentObject*,std::string>> objsList;
			//
			//for (auto objIt = topoSortedObjects.rbegin(); objIt != topoSortedObjects.rend(); ++objIt){

			//	if (strcmp((*objIt)->getNameInDocument(), "Generated__cross_section") == 0){
			//		resultObj = (*objIt);
			//	}

			//	std::vector<App::Property*>propList;
			//	std::vector<std::string>propNames;
			//	(*objIt)->getPropertyList(propList);
			//	propNames = (*objIt)->getDynamicPropertyNames();
			//	if (propList.size() < 20){
			//		continue;
			//	}
			//	//判断模型可见性
			//	Part::Feature* objBase = dynamic_cast<Part::Feature*>(*objIt);
			//	Gui::ViewProvider* vpBase = Gui::Application::Instance->getViewProvider(objBase);
			//	Gui::ViewProviderDocumentObject* vpObj = static_cast<Gui::ViewProviderDocumentObject*> (vpBase);
			//	bool isVisible = false;
			//	if (vpObj)
			//	{
			//		isVisible=vpObj->Visibility.getValue();
			//	}
			//	

			//	std::vector<App::Property*>::iterator pt;
			//	for (auto pt = propList.begin(); pt != propList.end(); ++pt){

			//		const char* name = (*pt)->getName();
			//		//要么是非未定义，要么是未定义但是，是可见的模型
			//		if (strcmp((*pt)->getName(), "Attribute") == 0 && 
			//			(!((App::PropertyEnumeration*)*pt)->isValue("NotDefine")||
			//			(((App::PropertyEnumeration*)*pt)->isValue("NotDefine")) && isVisible)){
			//			//std::string objAttr = ((App::PropertyEnumeration*)*pt)->getValueAsString();
			//			std::vector<std::string>::iterator ret;
			//			ret = std::find(propNames.begin(), propNames.end(), "Order");
			//			//没有Order属性
			//			if (ret == propNames.end())
			//				continue;
			//			int orderOfObj = ((App::PropertyInteger*)(*objIt)->getPropertyByName("Order"))->getValue();
			//			objsMap[orderOfObj] = (*objIt);
			//			//objsList.push_back(std::make_pair((*objIt),objAttr));
			//			break;
			//		}
			//	}
			//}
			s4 = GetTickCount();
			std::cerr << "getObjMap time " << (s4 - s3)*1.0 / 1000 << std::endl;
			static_cast<Part::Feature*>(resultObj)->Shape.setValue(*(new TopoDS_Shape()));

			//objsMap倒着查找，如果是真空，就加入vacuoShape列表，遇到实体，就用实体减去vacuoShape列表,最后用makeCompound组合最后的体
			std::vector<TopoDS_Shape> vacuoShapes;
			//首先将最后的shape加入到容器
			vacuoShapes.push_back(toolShape);

			std::vector<TopoDS_Shape> finalShapes;

			std::vector<App::DocumentObject*> vacuoObjs;
			std::vector<App::DocumentObject*> finalObjs;
			std::vector<Part::ShapeHistory> historyOfCon;
			//存放导体属性的颜色
			std::vector<App::Color> ColorOfCon;
			for (std::map<int, App::DocumentObject*>::reverse_iterator it = objsMap.rbegin(); it != objsMap.rend(); ++it){
				guiPcDoc->setHide(it->second->getNameInDocument());
				TopoDS_Shape itShape = static_cast<Part::Feature*>(it->second)->Shape.getValue();
				if (itShape.IsNull())
					continue;
				//这个模型的属性string是什么
				std::string attrOfObj = ((App::PropertyEnumeration*)(it->second->getPropertyByName("Attribute")))->getValueAsString();
				if (strcmp(attrOfObj.c_str(), "Vacuo") == 0){
					vacuoShapes.push_back(itShape);
					vacuoObjs.push_back(it->second);
				}
				else{
					TopoDS_Shape finalShape;
					if ((strcmp(attrOfObj.c_str(), "Conductor") == 0) || (strcmp(attrOfObj.c_str(), "Custom") == 0)){
						
						//测试
						clock_t t1, t2;
						if (vacuoShapes.size() != 0)
						{
							t1 = clock();
							std::cout << "t1:" << t1 << std::endl;
							finalShape = Part::TopoShape(itShape).cut(vacuoShapes);
							t2 = clock();
							std::cout << "t2:" << t1 << std::endl;
							std::cout << "this cut: " << (t2 - t1) << std::endl;
						}
						else{
							finalShape = itShape;
						}
					}
					else if ((strcmp(attrOfObj.c_str(), "NotDefine") == 0))
					{
						//TopoDS_Shape finalShape;
						finalShape = Part::TopoShape(itShape).cut(toolShape);

					}
					finalShapes.push_back(finalShape);
					finalObjs.push_back(it->second);
					//加入颜色
					Part::Feature* objBase = dynamic_cast<Part::Feature*>(it->second);
					Gui::ViewProvider* vpBase = Gui::Application::Instance->getViewProvider(objBase);
					std::vector<App::Color> baseCol = static_cast<PartGui::ViewProviderPart*>(vpBase)->DiffuseColor.getValues();
					//因为每一个所有的形状只能是一种颜色
					if (baseCol.size() != 0)
						ColorOfCon.push_back(baseCol[0]);
					else
						//默认
						ColorOfCon.push_back(App::Color(0.80, 0.80, 0.80, 0.5));
					
					
				}
				
			}
			//测试
			clock_t t1, t2;

			//makeCompound
			BRep_Builder builder;
			TopoDS_Compound comp;
			builder.MakeCompound(comp);
			t1 = clock();
			std::cout << "compound start: " << t1 << std::endl;
			for (std::vector<TopoDS_Shape>::iterator it = finalShapes.begin(); it != finalShapes.end(); ++it){
				if (!(*it).IsNull())
					builder.Add(comp, *it);
			}
			/*TopoDS_Shape finalShape;
			if (finalShapes.size() != 0){
			if (finalShapes.size() == 1){
			finalShape = finalShapes[0];
			}
			else{
			Part::TopoShape *baseShape = new Part::TopoShape(finalShapes[finalShapes.size() - 1]);
			finalShapes.pop_back();
			finalShape = baseShape->fuse(finalShapes);
			}
			}*/
			t2 = clock();
			std::cout << "compound end: " << t2 << std::endl;
			std::cout << "compound adll: " << (t2 - t1) << std::endl;
			//Part::TopoShape shape(comp);
			//将comp的shape给resultShape
			if (!resultObj){
				resultObj = pcDoc->addObject("Part::FeaturePython", "Generated__cross_section");
			}

			if (finalShapes.size() != 0)
			{
				//static_cast<Part::Feature*>(resultObj)->Shape.setValue(comp);
				setCompoundShape(resultObj, finalObjs, finalShapes);
				//static_cast<Part::Feature*>(resultObj)->Shape.setValue(comp);
				setCompoundColor(resultObj, finalObjs, finalShapes, ColorOfCon);

				if (showCutFace)
				{
					//设置相切处颜色
					DWORD s1, s2;
					s1 = GetTickCount();
					Part::Feature*compoundFeaure = static_cast<Part::Feature*>(resultObj);
					const TopoDS_Shape& compShape = compoundFeaure->Shape.getValue();

					Gui::ViewProvider* vpBase = Gui::Application::Instance->getViewProvider(compoundFeaure);
					std::vector<App::Color> baseCol = static_cast<PartGui::ViewProviderPart*>(vpBase)->DiffuseColor.getValues();

					showCoinsideFace(compShape, toolShape, App::Color(0.8, 0.8, 0.8), baseCol);

					static_cast<PartGui::ViewProviderPart*>(vpBase)->DiffuseColor.setValues(baseCol);
					s2 = GetTickCount();
					std::cerr << "set cut color time:" << (s2 - s1)*1.0 / 1000 << endl;
				}
				
			}




			//guiPcDoc->setShow(resultObj->getNameInDocument());
			//guiPcDoc->booleanObjectMap = bObjsMap;
			pcDoc->recompute();
			pcDoc->flagNeedUpdateBoolean.setValue(-1);



			stop = GetTickCount();
			std::cerr << "start end" << stop << std::endl;
			//cerr << "bool time:" << (stop - start)*1.0 / 1000 << endl;
			
			//stop = GetTickCount();
			//cerr << "bool time:" << (stop - start)*1.0 / 1000 << endl;
			return Py::None();
			;
		}
		/*将shapeTool与shapeBase相重合的面片改变颜色*/
		void showCoinsideFace(const TopoDS_Shape &shapeBase,
			const TopoDS_Shape &shapeTool,
			App::Color color,
			std::vector<App::Color> &baseCols)
		{
			//先得到shapeBase 和shapeTool的所有面片
			TopTools_IndexedMapOfShape faceBaseMap, faceToolMap;
			TopExp::MapShapes(shapeBase, TopAbs_FACE, faceBaseMap);
			TopExp::MapShapes(shapeTool, TopAbs_FACE, faceToolMap);

			std::cout << "baseCols Size:" << baseCols.size() << " faces Size:" << faceBaseMap.Extent() << std::endl;
			if (baseCols.size() != faceBaseMap.Extent())
			{
				std::cerr << "showCoinsideFace wrong" << std::endl;
			}

			std::vector<TopoDS_Shape> facesBaseVec(faceBaseMap.Extent()), facesToolVec(faceToolMap.Extent());
			std::vector<Base::Vector3d> toolVectors(faceToolMap.Extent(),Base::Vector3d(0.0,0.0,0.0));

			int i = 1;
			for (; i <= faceBaseMap.Extent() && i <= faceToolMap.Extent(); i++)
			{
				facesBaseVec[i-1]=(faceBaseMap.FindKey(i));
				facesToolVec[i-1]=(faceToolMap.FindKey(i));
			}
			//
			while (i <= faceBaseMap.Extent())
			{
				facesBaseVec[i-1]=(faceBaseMap.FindKey(i));
				i++;
			}
			while (i <= faceToolMap.Extent())
			{
				facesToolVec[i-1]=(faceToolMap.FindKey(i));
				i++;
			}
			//计算每个baseFace和ToolFace之间的距离
			std::vector<TopoDS_Shape>::iterator baseIt = facesBaseVec.begin();
			std::vector<TopoDS_Shape>::iterator toolIt = facesToolVec.begin();
			
			int baseFaceIndex = -1;
			for (; baseIt != facesBaseVec.end(); baseIt++)
			{
				Base::Vector3d baseNormal(0.0, 0.0, 0.0);
				baseFaceIndex++;
				toolIt = facesToolVec.begin();
				int toolFaceIndex = -1;
				//遍历toolFaces
				for (; toolIt != facesToolVec.end(); ++toolIt)
				{
					toolFaceIndex++;
					//计算距离
					BRepExtrema_DistShapeShape extss(*baseIt, *toolIt);
					//extss(*toolIt,*baseIt);
					//extss.LoadS1(*baseIt);
					//extss.LoadS2(*baseIt);

					if (!extss.IsDone()) {
						PyErr_SetString(PyExc_TypeError, "BRepExtrema_DistShapeShape failed");
						continue;
						//return 0;
					}
					else
					{
						int count = extss.NbSolution();
						if (count != 0)
						{
							Standard_Real minDist = extss.Value();
							//距离为0
							if (minDist == 0.0)
							{
								//看看法相是不是相同
								if (toolVectors[toolFaceIndex] == Base::Vector3d(0.0, 0.0, 0.0))
									toolVectors[toolFaceIndex] = calculateShapeNormal(*toolIt);
								if (baseNormal == Base::Vector3d(0.0, 0.0, 0.0))
									baseNormal = calculateShapeNormal(*baseIt);
								if ((toolVectors[toolFaceIndex] == baseNormal || toolVectors[toolFaceIndex] == (-baseNormal)) && baseNormal!=Base::Vector3d(0.0,0.0,0.0))
								{
									//
									baseCols[baseFaceIndex] = color;
									//退出这重循环，到下一个面片
									break;
								}
								
							}
						}
					}

				}
			}
		}

		/*求面的法线*/
		Base::Vector3d calculateShapeNormal(const TopoDS_Shape& sh){

			if (sh.IsNull())
				throw Base::Exception("calculateShapeNormal: link points to a valid object, but its shape is null.");
			//find plane
			BRepLib_FindSurface planeFinder(sh, -1, /*OnlyPlane=*/true);
			if (!planeFinder.Found())
			{
				//throw Base::ValueError("Can't find normal direction, because the shape is not on a plane.");
				return Base::Vector3d(0.0, 0.0, 0.0);
			}
				

			//find plane normal and return result.
			GeomAdaptor_Surface surf(planeFinder.Surface());
			gp_Dir normal = surf.Plane().Axis().Direction();

			//now se know the plane. But if there are faces, the
			//plane normal direction is not dependent on face orientation (because findPlane only uses edges).
			//let's fix that.
			try{
				TopExp_Explorer ex(sh, TopAbs_FACE);
				if (ex.More()) {
					BRepAdaptor_Surface surf(TopoDS::Face(ex.Current()));
					///
					//gp_Pln p = surf.Plane();//报错
					//const gp_Ax1 a = p.Axis();
					//const gp_Dir d = a.Direction();
					///
					normal = surf.Plane().Axis().Direction();
					if (ex.Current().Orientation() == TopAbs_REVERSED){
						normal.Reverse();
					}
				}
			}
			catch (...){
				std::cerr << "fix faces wrong\n";
				return Base::Vector3d(0.0, 0.0, 0.0);

			}
			return Base::Vector3d(normal.X(), normal.Y(), normal.Z());
		}
		//求点(x,y)与原点连成的直线与x轴正方向的夹角
		double getTheta(double x,double y){
			double theta;
			if (y == 0 && x >= 0){
				theta = 0;
			}
			else if ((y == 0 && x < 0)){
				theta = 180;
			}
			else if (y <0){
				theta = 360 + (180 / acos(-1))*(atan2(y, x));
			}

			else{
				theta = (180 / acos(-1))*(atan2(y, x));
			}
			return theta;
			
		}
		
		Py::Object getPointsOfObj(const Py::Tuple& args){
			//const char* objName = 0;
			if (!PyArg_ParseTuple(args.ptr(), ""))
				return Py::None();
			App::Document *pcDoc = App::GetApplication().getActiveDocument();
			std::vector<App::DocumentObject*> topoSortedObjects = pcDoc->topologicalSort();
			std::vector<TopoDS_Shape> shapeList;
			std::vector<App::DocumentObject*>::iterator objIt = topoSortedObjects.begin();
			TopoDS_Shape *resultShape = new TopoDS_Shape();
			for (; objIt != topoSortedObjects.end(); ++objIt){
				if ((*objIt)->getTypeId().isDerivedFrom(Part::Feature::getClassTypeId())) {
					std::vector<App::Property*>propList;
					(*objIt)->getPropertyList(propList);
					std::vector<App::Property*>::iterator pt;
					//判断该模型是不是体
					bool flag = false;
					for (auto pt = propList.begin(); pt != propList.end(); ++pt){
						if (strcmp((*pt)->getName(), "Attribute") == 0){
							flag = true;
							break;
						}
					}
					TopoDS_Shape s = static_cast<Part::Feature*>(*objIt)->Shape.getValue();
					if (!s.IsNull() && flag){
						
						shapeList.push_back(s);
						
					}
					
				}
			}

			try{
				booleanAddShapes(*resultShape, shapeList);
			}
			catch(...){
				return Py::None();
			}
			

			double MinZ =0;
 			double MaxZ = 0;
			std::vector<Base::Vector3d> Points;
			if (!resultShape->IsNull()){
				Part::TopoShape *topoShape = new Part::TopoShape(*resultShape);
				Base::BoundBox3d box = topoShape->getBoundBox();

				MinZ = box.MinZ;
				MaxZ = box.MaxZ;
				double box_R = std::max<double>(sqrt((box.MaxX)*(box.MaxX) + (box.MaxY)*(box.MaxY)),
					sqrt((box.MinX)*(box.MinX) + (box.MinY)*(box.MinY)));
				double accuary = 1.0e-02;
				//0-10
				if (box_R < 1e-2){
					accuary =1.0e-03;
				}
				//10-100
				else if (box_R >= 1e-2 && box_R < 1e-1){
					accuary = 1.0e-02;
				}
				//100-200
				else if (box_R >= 1e-1 && box_R < 2e-1){
					accuary = 2.0e-02;
				}
				//200-700
				else if (box_R >= 2e-2 && box_R < 7e-1){
					accuary = 5.0e-02;
				}
				//700-1500
				else if (box_R >= 7e-1 && box_R < 1.5){
					accuary = 1.0e-01;
				}
				else{
					accuary = 5.0e-01;
				}
				
				std::vector<Base::Vector3d> Normals;
				topoShape->getPoints(Points, Normals, accuary);
				
				/*while (Points.size()>1e5 || Points.size()<1e4){
					if (Points.size() < 1e4){
						accuary = accuary * 10;
					}
					else{
						accuary = accuary / 10;
					}
					topoShape->getPoints(Points, Normals, accuary);
				}*/
			}
			
			if (Points.size()){

				
				std::vector<Base::Vector3d>::iterator vecIt;

				vecIt = Points.begin();
				double MinR = sqrt((vecIt->x)*(vecIt->x) + (vecIt->y)*(vecIt->y));
				double MaxR = MinR;
				double MinTheta = getTheta((vecIt->x), (vecIt->y));
				double MaxTheta = MinTheta;
				

				double MediumTheta = getTheta((vecIt + int(Points.size() / 2))->x, (vecIt + int(Points.size() / 2))->y);

				/*std::cerr << "minR1" << std::endl;
				std::cerr << MinR << std::endl;
				std::cerr << "maxR1" << std::endl;
				std::cerr << sqrt(((Points.end() - 1)->x)*(((Points.end() - 1))->x) + ((Points.end() - 1)->y)*((Points.end() - 1)->y)) << std::endl;
				std::cerr << "MinTheta1" << std::endl;
				std::cerr << getTheta((vecIt->x), (vecIt->y)) << std::endl;
				std::cerr << "MaxTheta1" << std::endl;
				std::cerr << getTheta(((Points.end() - 1)->x), ((Points.end() - 1)->y)) << std::endl;*/

				for (; vecIt != Points.end(); ++vecIt){
					double x = vecIt->x;
					double y = vecIt->y;
					double r = sqrt((vecIt->x)*(vecIt->x) + (vecIt->y)*(vecIt->y));
					MinR = std::min<double>(MinR, r);
					MaxR = std::max<double>(MaxR, r);
					double theta = getTheta(x, y);
					MinTheta = std::min<double>(MinTheta, theta);
					MaxTheta = std::max<double>(MaxTheta, theta);

				}
				std::cerr << "minR" << std::endl;
				std::cerr << MinR << std::endl;
				std::cerr << "maxR" << std::endl;
				std::cerr << MaxR << std::endl;
				std::cerr << "MinTheta" << std::endl;
				std::cerr << MinTheta << std::endl;
				std::cerr << "MaxTheta" << std::endl;
				std::cerr << MaxTheta << std::endl;
				std::cerr << "MediumTheta" << std::endl;
				std::cerr << MediumTheta << std::endl;
				std::cerr << Points.size() << std::endl;
				Py::List list;
				list.append(Py::Float(MinR));
				list.append(Py::Float(MaxR));
				list.append(Py::Float(MinZ));
				list.append(Py::Float(MaxZ));
				list.append(Py::Float(MinTheta));
				list.append(Py::Float(MaxTheta));
				list.append(Py::Float(MediumTheta));
				return list;
			}
			return Py::None();
		}

	};

	PyObject* initModule()
	{
		return (new Module)->module().ptr();
	}

} // namespace PartGui

PyMOD_INIT_FUNC(PartGui)
{
	if (!Gui::Application::Instance) {
		PyErr_SetString(PyExc_ImportError, "Cannot load Gui module in console application.");
		PyMOD_Return(0);
	}

	// load needed modules
	try {
		Base::Interpreter().runString("import Part");
	}
	catch (const Base::Exception& e) {
		PyErr_SetString(PyExc_ImportError, e.what());
		PyMOD_Return(0);
	}

	PyObject* partGuiModule = PartGui::initModule();

	Base::Console().Log("Loading GUI of Part module... done\n");

#if PY_MAJOR_VERSION >= 3
	static struct PyModuleDef pAttachEngineTextsModuleDef = {
		PyModuleDef_HEAD_INIT,
		"AttachEngineResources",
		"AttachEngineResources", -1,
		AttacherGui::AttacherGuiPy::Methods,
		NULL, NULL, NULL, NULL
	};
	PyObject* pAttachEngineTextsModule = PyModule_Create(&pAttachEngineTextsModuleDef);
#else
	PyObject* pAttachEngineTextsModule = Py_InitModule3("AttachEngineResources", AttacherGui::AttacherGuiPy::Methods,
		"AttachEngine Gui resources");
#endif

	Py_INCREF(pAttachEngineTextsModule);
	PyModule_AddObject(partGuiModule, "AttachEngineResources", pAttachEngineTextsModule);

	PartGui::PropertyEnumAttacherItem::init();
	PartGui::SoBrepFaceSet::initClass();
	PartGui::SoBrepEdgeSet::initClass();
	PartGui::SoBrepPointSet::initClass();
	PartGui::SoFCControlPoints::initClass();
	PartGui::ViewProviderPartExt::init();
	PartGui::ViewProviderPart::init();
	PartGui::ViewProviderEllipsoid::init();
	PartGui::ViewProviderPython::init();
	PartGui::ViewProviderBox::init();
	PartGui::ViewProviderPrism::init();
	PartGui::ViewProviderRegularPolygon::init();
	PartGui::ViewProviderWedge::init();
	PartGui::ViewProviderImport::init();
	PartGui::ViewProviderCurveNet::init();
	PartGui::ViewProviderExtrusion::init();
	PartGui::ViewProvider2DObject::init();
	PartGui::ViewProvider2DObjectPython::init();
	PartGui::ViewProviderMirror::init();
	PartGui::ViewProviderFillet::init();
	PartGui::ViewProviderChamfer::init();
	PartGui::ViewProviderRevolution::init();
	PartGui::ViewProviderLoft::init();
	PartGui::ViewProviderSweep::init();
	PartGui::ViewProviderOffset::init();
	PartGui::ViewProviderOffset2D::init();
	PartGui::ViewProviderThickness::init();
	PartGui::ViewProviderCustom::init();
	PartGui::ViewProviderCustomPython::init();
	PartGui::ViewProviderBoolean::init();
	PartGui::ViewProviderMultiFuse::init();
	PartGui::ViewProviderMultiCommon::init();
	PartGui::ViewProviderCompound::init();
	PartGui::ViewProviderSpline::init();
	PartGui::ViewProviderCircleParametric::init();
	PartGui::ViewProviderLineParametric::init();
	PartGui::ViewProviderPointParametric::init();
	PartGui::ViewProviderEllipseParametric::init();
	PartGui::ViewProviderHelixParametric::init();
	PartGui::ViewProviderSpiralParametric::init();
	PartGui::ViewProviderPlaneParametric::init();
	PartGui::ViewProviderSphereParametric::init();
	PartGui::ViewProviderCylinderParametric::init();
	PartGui::ViewProviderConeParametric::init();
	PartGui::ViewProviderTorusParametric::init();
	PartGui::ViewProviderRuledSurface::init();
	PartGui::ViewProviderFace::init();
	PartGui::DimensionLinear::initClass();
	PartGui::DimensionAngular::initClass();
	PartGui::ArcEngine::initClass();

	PartGui::Workbench::init();

	// instantiating the commands
	CreatePartCommands();
	CreateSimplePartCommands();
	CreateParamPartCommands();
	try{
		Py::Object ae = Base::Interpreter().runStringObject("__import__('AttachmentEditor.Commands').Commands");
		Py::Module(partGuiModule).setAttr(std::string("AttachmentEditor"), ae);
	}
	catch (Base::PyException &err){
		err.ReportException();
	}


	// register preferences pages
	(void)new Gui::PrefPageProducer<PartGui::DlgSettingsGeneral>(QT_TRANSLATE_NOOP("QObject", "Part design"));
	(void)new Gui::PrefPageProducer<PartGui::DlgSettings3DViewPart>(QT_TRANSLATE_NOOP("QObject", "Part design"));
	(void)new Gui::PrefPageProducer<PartGui::DlgImportExportIges>(QT_TRANSLATE_NOOP("QObject", "Import-Export"));
	(void)new Gui::PrefPageProducer<PartGui::DlgImportExportStep>(QT_TRANSLATE_NOOP("QObject", "Import-Export"));
	(void)new Gui::PrefPageProducer<PartGui::DlgSettingsObjectColor>(QT_TRANSLATE_NOOP("QObject", "Display"));
	Gui::ViewProviderBuilder::add(
		Part::PropertyPartShape::getClassTypeId(),
		PartGui::ViewProviderPart::getClassTypeId());

	// add resources and reloads the translators
	loadPartResource();

	// register bitmaps
	Gui::BitmapFactoryInst& rclBmpFactory = Gui::BitmapFactory();
	rclBmpFactory.addXPM("PartFeature", (const char**)PartFeature_xpm);
	rclBmpFactory.addXPM("PartFeatureImport", (const char**)PartFeatureImport_xpm);

	PyMOD_Return(partGuiModule);
}
