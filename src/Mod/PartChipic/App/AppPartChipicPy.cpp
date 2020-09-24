/***************************************************************************
*   Copyright (c) Jürgen Riegel          (juergen.riegel@web.de) 2002     *
*                                                                         *
*   This file is part of the FreeCAD CAx development system.              *
*                                                                         *
*   This library is free software; you can redistribute it and/or         *
*   modify it under the terms of the GNU Library General Public           *
*   License as published by the Free Software Foundation; either          *
*   version 2 of the License, or (at your option) any later version.      *
*                                                                         *
*   This library  is distributed in the hope that it will be useful,      *
*   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
*   GNU Library General Public License for more details.                  *
*                                                                         *
*   You should have received a copy of the GNU Library General Public     *
*   License along with this library; see the file COPYING.LIB. If not,    *
*   write to the Free Software Foundation, Inc., 59 Temple Place,         *
*   Suite 330, Boston, MA  02111-1307, USA                                *
*                                                                         *
***************************************************************************/

#include "PreCompiled.h"
#include "ChipicConst.h"
#ifndef _PreComp_
# include <Python.h>
# include <BRepAdaptor_Curve.hxx>
# include <BRepCheck_Analyzer.hxx>
# include <BRepFeat_SplitShape.hxx>
# include <BRepPrimAPI_MakeBox.hxx>
# include <BRepPrimAPI_MakeCone.hxx>
# include <BRepPrimAPI_MakeTorus.hxx>
# include <BRepPrimAPI_MakeCylinder.hxx>
# include <BRepPrimAPI_MakeSphere.hxx>
# include <BRepPrimAPI_MakeRevolution.hxx>
# include <BRepPrim_Wedge.hxx>
# include <BRep_Builder.hxx>
# include <BRep_Tool.hxx>
# include <BRepLib.hxx>
# include <BRepBuilderAPI_MakeFace.hxx>
# include <BRepBuilderAPI_MakeEdge.hxx>
# include <BRepBuilderAPI_MakeVertex.hxx>
# include <BRepBuilderAPI_MakeWire.hxx>
# include <BRepBuilderAPI_MakePolygon.hxx>
# include <BRepBuilderAPI_MakeShell.hxx>
# include <BRepBuilderAPI_MakeSolid.hxx>
# include <BRepOffsetAPI_Sewing.hxx>
# include <BRepExtrema_DistShapeShape.hxx>
# include <BRepFill.hxx>
# include <BRepLib.hxx>
# include <gp_Circ.hxx>
# include <gp_Ax3.hxx>
# include <gp_Pnt.hxx>
# include <gp_Lin.hxx>
# include <gp_Pln.hxx>
# include <GCE2d_MakeSegment.hxx>
# include <Geom2d_Line.hxx>
# include <Geom_Circle.hxx>
# include <Geom_Line.hxx>
# include <Geom_Plane.hxx>
# include <Geom_BSplineSurface.hxx>
# include <Geom_ConicalSurface.hxx>
# include <Geom_CylindricalSurface.hxx>
# include <Geom_OffsetSurface.hxx>
# include <GeomAPI_PointsToBSplineSurface.hxx>
# include <Geom_Circle.hxx>
# include <Geom_Plane.hxx>
# include <Geom2d_TrimmedCurve.hxx>
# include <Interface_Static.hxx>
# include <ShapeUpgrade_ShellSewing.hxx>
# include <Standard_ConstructionError.hxx>
# include <Standard_DomainError.hxx>
# include <TopoDS.hxx>
# include <TopoDS_Edge.hxx>
# include <TopoDS_Face.hxx>
# include <TopoDS_Wire.hxx>
# include <TopoDS_Shell.hxx>
# include <TopoDS_Solid.hxx>
# include <TopoDS_Compound.hxx>
# include <TopExp_Explorer.hxx>
# include <TColgp_HArray2OfPnt.hxx>
# include <TColStd_Array1OfReal.hxx>
# include <TColStd_Array1OfInteger.hxx>
# include <TopTools_ListIteratorOfListOfShape.hxx>
# include <Precision.hxx>
# include <Standard_Version.hxx>
# include <ShapeConstruct_MakeTriangulation.hxx>
# include <BRepLib_FindSurface.hxx>
# include <BRepAdaptor_Surface.hxx>
# include <BRepAlgoAPI_Cut.hxx>
# include <BRepAlgoAPI_Fuse.hxx>
# include <BRepPrimAPI_MakePrism.hxx>
#include <TopoDS_FrozenShape.hxx>
#include <TopoDS_UnCompatibleShapes.hxx>
#endif

#include <CXX/Extensions.hxx>
#include <CXX/Objects.hxx>

#include <BRepOffsetAPI_ThruSections.hxx>
#include <BSplCLib.hxx>
#include <GeomFill_AppSurf.hxx>
#include <GeomFill_Line.hxx>
#include <GeomFill_Pipe.hxx>
#include <GeomFill_SectionGenerator.hxx>
#include <NCollection_List.hxx>
#include <BRepFill_Filling.hxx>
# include <BRepBuilderAPI_Copy.hxx>
#include <Base/Console.h>
#include <Base/PyObjectBase.h>
#include <Base/Interpreter.h>
#include <Base/Exception.h>
#include <Base/FileInfo.h>
#include <Base/GeometryPyCXX.h>
#include <Base/VectorPy.h>
#include <App/Application.h>
#include <App/Document.h>
#include <App/DocumentObjectPy.h>
#include <Mod/Part/App/TopoShapePy.h>
#include <Mod/Part/App/PartFeature.h>
#include <Mod/Part/App/FaceMaker.h>
#include <Mod/Part/App/TopoShapeEdgePy.h>
#include <Mod/Part/App/TopoShapeSolidPy.h>

#include<App/DocumentPy.h>
//#include<Gui/Document.h>
//#include<Gui/Application.h>
#include<time.h>


#include <Mod/Part/App/OCCError.h>
#include <Mod/Part/App/TopoShape.h>

#include <Mod/Mesh/App/Mesh.h>
#include <Mod/Mesh/App/MeshPy.h>
#include <Mod/Part/App/TopoShapePy.h>
#include <Mod/Part/App/TopoShapeWirePy.h>
#include <Mod/Mesh/App/Core/Algorithm.h>
#include <Mod/Mesh/App/Core/MeshKernel.h>

#include <boost/regex.hpp>
#include <boost/algorithm/string.hpp>
#include <boost/lexical_cast.hpp>
#include <boost/format.hpp>
#include <algorithm>
#include <tchar.h>

#include <windows.h>
#include <string>
#include <cstring>

#include "PM3VFunctional.h"
#include "MathMod.h"
#include "mathmod/ui_modules/parametersoptions.h"

////
#include <CXX/Extensions.hxx>
#include <CXX/Objects.hxx>

#include <Base/PyObjectBase.h>
#include <Base/Console.h>
#include <App/Application.h>
#include <App/Document.h>
#include <App/DocumentObjectPy.h>
#include <Gui/Application.h>
#include <Gui/MainWindow.h>
#include <Mod/Part/Gui/ViewProvider.h>
#include <Mod/Part/App/PartFeature.h>
#include<Gui/Document.h>
#include<Gui/Application.h>
#include <Mod/Part/App/FeaturePartCut.h>

#include <Mod/Part/App/FeaturePartFuse.h>
#include<Mod/Part/App/PropertyTopoShape.h>

#include<Mod/Part/App/TopoShape.h>

#include<Mod/Part/App/modelRefine.h>

# include <BRepAlgoAPI_Cut.hxx>
# include <BRepAlgoAPI_Fuse.hxx>
# include <BRep_Builder.hxx>
#include<TopTools_IndexedMapOfShape.hxx>
# include <TopExp.hxx>
#include<Gui/ViewProviderDocumentObject.h>

# include <BRepAlgoAPI_Common.hxx>

#ifndef M_PI
#define M_PI    3.14159265358979323846 /* pi */
#endif

#ifndef M_PI_2
#define M_PI_2  1.57079632679489661923 /* pi/2 */
#endif

DWORD start, stop;
#define TEST_OUTPUT 1
namespace PartChipic {
	class Module : public Py::ExtensionModule<Module>
	{
	public:
		Module() : Py::ExtensionModule<Module>("PartChipic")
		{
			add_varargs_method("customBoolean", &Module::customBoolean,
				"customBoolean([list]) -- refresh the boolean from order"
				);
			add_varargs_method("updateBoolean0", &Module::updateBoolean0,
				"updateBoolean() -- update the boolean of Document."
				);
			add_varargs_method("updateBoolean", &Module::updateBoolean,
				"updateBoolean() -- update the boolean of Document."
				);
			add_varargs_method("makeFuncMesh", &Module::makeFuncMesh,
				"makeFuncMesh(func,xmin,xmax,ymin,ymax,zmim,zmax,tempFilePath) -- Create a function mesh."
				);
			add_varargs_method("makeObjFileMesh", &Module::makeObjFileMesh,
				"makeObjFileMesh(path) -- Create a obj mesh."
				);

			add_varargs_method("makeExtrude", &Module::makeExtrude,
				"makeExtrude(baseObjName,length,[dir]) -- Make a extrude located\n"
				"in pnt with the dimensions (length)\n"
				"By default lenght=10mm"
				);
			add_varargs_method("makePicRevolution", &Module::makePicRevolution,
				"makePicRevolution(baseAreaName,Point1,Point2,Angle) -- Make a revolution located\n"
				"make a revolution obj with baseAreaName ,and get Axis by Point1 and Point2,with angle "
				);

			/*fubiao*/
			/*add_varargs_method("makePoint", &Module::makePoint,
			"makePoint(vector) -- Make a Point with given point\n"
			"By default pnt=Vector(1,1,1)"
			);*/
			add_varargs_method("makeMyCirc", &Module::makeMyCirc,
				"makeMyCirc(radius1,radius2,height,[pnt,dir,angle]) -- Make a cone with given radii and height\n"
				"By default pnt=Vector(0,0,0), dir=Vector(0,0,1) and angle=360"
				);
			/*end*/

			initialize("This is a module working with shapes."); // register with Python
		}

		virtual ~Module() {}

	private:
		virtual Py::Object invoke_method_varargs(void *method_def, const Py::Tuple &args)
		{
			try {
				return Py::ExtensionModule<Module>::invoke_method_varargs(method_def, args);
			}
			catch (const Standard_Failure &e) {
				std::string str;
				Standard_CString msg = e.GetMessageString();
				str += typeid(e).name();
				str += " ";
				if (msg) { str += msg; }
				else     { str += "No OCCT Exception Message"; }
				Base::Console().Error("%s\n", str.c_str());
				throw Py::Exception(Part::PartExceptionOCCError, str);
			}
			catch (const Base::Exception &e) {
				std::string str;
				str += "FreeCAD exception thrown (";
				str += e.what();
				str += ")";
				e.ReportException();
				throw Py::RuntimeError(str);
			}
			catch (const std::exception &e) {
				std::string str;
				str += "C++ exception thrown (";
				str += e.what();
				str += ")";
				Base::Console().Error("%s\n", str.c_str());
				throw Py::RuntimeError(str);
			}
		}
		/*布尔sub*/
		void booleanSub2(TopoDS_Shape &resultShape, TopoDS_Shape theFirstShap, TopoDS_Shape theSecondShape){

			if (theSecondShape.IsNull()){
				resultShape = theFirstShap;
				return;
			}

			BRepAlgoAPI_Cut mkCut(theFirstShap, theSecondShape);
			if (!mkCut.IsDone())
				std::cerr << "Cut out failed!" << std::endl;
			//return new App::DocumentObjectExecReturn("Cut out failed");
			TopoDS_Shape shap = mkCut.Shape();
			resultShape = shap;
		}
		/*布尔add one: resultShape=resultShape+shape*/
		void booleanAddOne2(TopoDS_Shape &resultShape, TopoDS_Shape addShape){
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
		void booleanAdd2(TopoDS_Shape &resultShape, std::vector<TopoDS_Shape> shapeList){
			int n = 0;
			TopoDS_Shape temp = resultShape;
			if (shapeList.size() == 0)
				return;
			if (resultShape.IsNull()){
				resultShape = shapeList[0];
				n = 1;
				//booleanAddOne(resultShape, shapeList[0]);
			}
			if (shapeList.size() > n){
				BRepAlgoAPI_Fuse mkFuse;
				mkFuse.SetRunParallel(true);
				TopTools_ListOfShape shapeArguments, shapeTools;
				const TopoDS_Shape& shape = resultShape;
				if (shape.IsNull())
					std::cerr << "input shap is null" << std::endl;
				//throw Base::RuntimeError("Input shape is null");
				shapeArguments.Append(shape);

				for (std::vector<TopoDS_Shape>::iterator it = shapeList.begin() + n; it != shapeList.end(); ++it) {
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
		Py::Object updateBoolean00(const Py::Tuple& args)
		{
			DWORD start, stop;
			start = GetTickCount();
			std::cerr << "start boolean" << start << std::endl;

			int changedOrder = 0, beforeOrder = 0;

			if (!PyArg_ParseTuple(args.ptr(), "|ii", &changedOrder, &beforeOrder))
				return Py::None();
			/*if (changedOrder == -1)
			{
			std::cout << "changedOrder==-1 break" << std::endl;
			return Py::None();
			}
			else{
			std::cout << "changedOrder=" << changedOrder << std::endl;
			}*/

			App::Document* pcDoc;
			Gui::Document *guiPcDoc = Gui::Application::Instance->activeDocument();
			pcDoc = App::GetApplication().getActiveDocument();
			App::DocumentObject* resultObj = NULL;
			std::vector<App::DocumentObject*> topoSortedObjects = pcDoc->topologicalSort();
			//所有需要做布尔运算的模型，即有Attribute且不为未定义的模型
			//std::vector<std::pair<App::DocumentObject*,std::string>> objsList;
			std::vector<int> indexVec;
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
						indexVec.push_back(orderOfObj);
						//objsList.push_back(std::make_pair((*objIt),objAttr));
						break;
					}
				}
			}
			//			static_cast<Part::Feature*>(resultObj)->Shape.setValue(*(new TopoDS_Shape()));
			//objsMap倒着查找，如果是真空，就加入vacuoShape列表，遇到实体，就用实体减去vacuoShape列表,最后用makeCompound组合最后的体
			std::vector<TopoDS_Shape> vacuoShapes;
			std::vector<TopoDS_Shape> finalShapes;
			int flag = -1;//上一个体的属性0：void,-1:未确定
			BRep_Builder builder0;
			TopoDS_Compound comp0;
			builder0.MakeCompound(comp0);
			std::sort(indexVec.begin(), indexVec.end());
			//for (std::map<int, App::DocumentObject*>::reverse_iterator it = objsMap.rbegin(); it != objsMap.rend(); ++it)
			for (int ii = 0; ii < indexVec.size(); ii++)
			{
				App::DocumentObject* second = objsMap[indexVec[ii]];
				guiPcDoc->setHide(second->getNameInDocument());
				TopoDS_Shape itShape = static_cast<Part::Feature*>(second)->Shape.getValue();
				//这个模型的属性string是什么
				std::string attrOfObj = ((App::PropertyEnumeration*)(second->getPropertyByName("Attribute")))->getValueAsString();
				if (strcmp(attrOfObj.c_str(), "Vacuo") == 0){
					if (!itShape.IsNull())
						vacuoShapes.push_back(itShape);
				}
				else if ((strcmp(attrOfObj.c_str(), "Conductor") == 0) || (strcmp(attrOfObj.c_str(), "Custom") == 0)){
					//测试
					clock_t t1, t2;
					if (vacuoShapes.size() != 0)
					{
						//t1 = clock();
						//std::cout << "t1:" << t1 << std::endl;
						TopoDS_Shape finalShape = Part::TopoShape(comp0).cut(vacuoShapes);
						//t2 = clock();
						//std::cout << "t2:" << t1 << std::endl;
						//std::cout << "this cut: " << (t2 - t1) << std::endl;
						//BRep_Builder builderx;
						//TopoDS_Compound compx;
						builder0.MakeCompound(comp0);
						builder0.Add(comp0, finalShape);
						//comp0 = compx;
						vacuoShapes.clear();
						if (!itShape.IsNull())
							builder0.Add(comp0, itShape);
					}
					else{
						if (!itShape.IsNull())
							builder0.Add(comp0, itShape);
					}

				}
			}
			if (vacuoShapes.size() != 0)
			{
				//t1 = clock();
				//std::cout << "t1:" << t1 << std::endl;
				TopoDS_Shape finalShape = Part::TopoShape(comp0).cut(vacuoShapes);
				//t2 = clock();
				//std::cout << "t2:" << t1 << std::endl;
				//std::cout << "this cut: " << (t2 - t1) << std::endl;
				//BRep_Builder builderx;
				//TopoDS_Compound compx;
				builder0.MakeCompound(comp0);
				builder0.Add(comp0, finalShape);
				//comp0 = compx;
				vacuoShapes.clear();
			}
			//测试
			//			clock_t t1, t2;

			//makeCompound
			/*		BRep_Builder builder;
			TopoDS_Compound comp;
			builder.MakeCompound(comp);
			//			t1 = clock();
			//			std::cout << "compound start: " << t1 << std::endl;
			for (std::vector<TopoDS_Shape>::iterator it = finalShapes.begin(); it != finalShapes.end(); ++it){
			if (!(*it).IsNull())
			builder.Add(comp, *it);
			}*/
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
			//			t2 = clock();
			//			std::cout << "compound end: " << t2 << std::endl;
			//			std::cout << "compound adll: " << (t2 - t1) << std::endl;
			//Part::TopoShape shape(comp);
			//将comp的shape给resultShape
			if (!resultObj){
				resultObj = pcDoc->addObject("Part::FeaturePython", "ResultShape");
			}

			//if (finalShapes.size() != 0)
			static_cast<Part::Feature*>(resultObj)->Shape.setValue(comp0);



			//guiPcDoc->setShow(resultObj->getNameInDocument());
			//guiPcDoc->booleanObjectMap = bObjsMap;
			//			pcDoc->recompute();
			pcDoc->flagNeedUpdateBoolean.setValue(-1);



			stop = GetTickCount();
			std::cerr << "end boolean" << stop << std::endl;
			cerr << "bool time:" << (stop - start)*1.0 / 1000 << endl;

			//stop = GetTickCount();
			//cerr << "bool time:" << (stop - start)*1.0 / 1000 << endl;
			return Py::None();
			;
		}
		/*
		调用函数前先判断是否需要bool运算
		*/
		Py::Object updateBoolean(const Py::Tuple& args)
		{
			DWORD start, stop, mid;
			start = GetTickCount();
			std::cerr << "start boolean" << start << std::endl;

			int curOrder = 0,//更改或新建模型的顺序号 
				reshow = 0, //不是新建模型
				maxOrder = 0;
			if (!PyArg_ParseTuple(args.ptr(), "|ii", &curOrder, &reshow))
				return Py::None();
			//std::cerr << "reshow:" << reshow << std::endl;
			App::Document* pcDoc;
			Gui::Document *guiPcDoc = Gui::Application::Instance->activeDocument();
			pcDoc = App::GetApplication().getActiveDocument();
			App::DocumentObject* resultObj = NULL;
			std::vector<App::DocumentObject*> topoSortedObjects = pcDoc->topologicalSort();
			//所有需要做布尔运算的模型，即有Attribute且不为未定义的模型
			std::map<int, App::DocumentObject*> objsMap;
			std::vector<int> orderAry;
			for (auto objIt = topoSortedObjects.rbegin(); objIt != topoSortedObjects.rend(); ++objIt){

				if (strcmp((*objIt)->getNameInDocument(), S_RESULTSHAPE) == 0){
					resultObj = (*objIt);
					continue;
				}

				std::vector<App::Property*>propList;
				std::vector<std::string>propNames;
				(*objIt)->getPropertyList(propList);
				propNames = (*objIt)->getDynamicPropertyNames();
				if (propList.size() < 20){
					continue;
				}

				//std::vector<App::Property*>::iterator pt;
				//for (auto pt = propList.begin(); pt != propList.end(); ++pt)
				{
					std::string jattrOfObj = ((App::PropertyEnumeration*)((*objIt)->getPropertyByName(S_ATTRIBUTE)))->getValueAsString();
					//const char* name = (*pt)->getName();
					//if (strcmp((*pt)->getName(), S_ATTRIBUTE) == 0 && !((App::PropertyEnumeration*)*pt)->isValue(S_NOTDEFINE))
					if (!(strcmp(jattrOfObj.c_str(), S_NOTDEFINE) == 0))
					{
						//std::string objAttr = ((App::PropertyEnumeration*)*pt)->getValueAsString();
						std::vector<std::string>::iterator ret;
						ret = std::find(propNames.begin(), propNames.end(), S_ORDER);
						//没有Order属性
						if (!(ret == propNames.end())) {
							int orderOfObj = ((App::PropertyInteger*)(*objIt)->getPropertyByName(S_ORDER))->getValue();
							objsMap[orderOfObj] = (*objIt);
						}
						/*	continue;
						int orderOfObj = ((App::PropertyInteger*)(*objIt)->getPropertyByName(S_ORDER))->getValue();
						objsMap[orderOfObj] = (*objIt);
						//objsList.push_back(std::make_pair((*objIt),objAttr));
						break;*/
					}
				}
			}
			if (!resultObj){
				resultObj = pcDoc->addObject("Part::FeaturePython", S_RESULTSHAPE);
			}
			//新建的是S_NOTDEFINE
			//if (reshow == 0 && objsMap[curOrder] == NULL)
			//	return Py::None();

			//倒序记录order
			for (std::map<int, App::DocumentObject*>::reverse_iterator it = objsMap.rbegin(); it != objsMap.rend(); ++it) {
				orderAry.push_back((*it).first);
			}
			int bcon = 1;
			//新建的是最后一个
			if (reshow == 0 && orderAry.size() > 0 && orderAry[0] == curOrder) {
				{
					TopoDS_Shape sh = static_cast<Part::Feature*>(resultObj)->Shape.getValue();
					BRep_Builder builder;
					TopoDS_Compound comp;
					builder.MakeCompound(comp);
					if (!sh.IsNull()) {
						//std::cerr << "resultObj:" << reshow << std::endl;
						builder.Add(comp, sh);
					}

					std::string jattrOfObj = ((App::PropertyEnumeration*)(objsMap[orderAry[0]]->getPropertyByName(S_ATTRIBUTE)))->getValueAsString();
					if (strcmp(jattrOfObj.c_str(), S_VACUO) == 0) {//todo
						//TopoDS_Shape finalShape = Part::TopoShape(comp).cut(static_cast<Part::Feature*>(objsMap[orderAry[0]])->Shape.getValue());
						//static_cast<Part::Feature*>(resultObj)->Shape.setValue(finalShape);
						;
					}
					else {
						builder.Add(comp, static_cast<Part::Feature*>(objsMap[orderAry[0]])->Shape.getValue());
						static_cast<Part::Feature*>(resultObj)->Shape.setValue(comp);
						bcon = 0;
					}
				}
			}
			if (bcon) {
				std::vector < std::vector<int> > shapsGroup;
				//std::vector < std::vector<TopoDS_Shape> > vacuosShapsGroup;
				std::vector < TopoDS_Shape > vacuosShapsGroup;
				std::vector<TopoDS_Shape> vacuoGroup;
				TopoDS_Shape vacuoShape;
				for (int j = 0; j < orderAry.size(); j++) {
					std::string jattrOfObj = ((App::PropertyEnumeration*)(objsMap[orderAry[j]]->getPropertyByName(S_ATTRIBUTE)))->getValueAsString();
					int befor_vacuo = 0;
					if (strcmp(jattrOfObj.c_str(), S_VACUO) == 0){
						befor_vacuo = 1;
						TopoDS_Shape sh = static_cast<Part::Feature*>(objsMap[orderAry[j]])->Shape.getValue();
						if (vacuoShape.IsNull()) {
							vacuoShape = sh;
							continue;
						}
						if (!sh.IsNull())
							vacuoGroup.push_back(sh);
						continue;
					}
					std::vector<int> tmpShapsAry;
					tmpShapsAry.push_back(orderAry[j]);

					int i = j + 1;
					for (; i < orderAry.size(); i++, j++) {
						std::string iattrOfObj = ((App::PropertyEnumeration*)(objsMap[orderAry[i]]->getPropertyByName(S_ATTRIBUTE)))->getValueAsString();
						if (strcmp(iattrOfObj.c_str(), S_VACUO) == 0){//当前是真空
							j = i - 1;
							break;
						}
						else {
							tmpShapsAry.push_back(orderAry[i]);
						}
					}
					if (vacuoGroup.size() > 0)
						vacuoShape = Part::TopoShape(vacuoShape).fuse(vacuoGroup);//将S_VACUO融合
					vacuosShapsGroup.push_back(vacuoShape);
					shapsGroup.push_back(tmpShapsAry);
					vacuoGroup.clear();
				}
				//			static_cast<Part::Feature*>(resultObj)->Shape.setValue(*(new TopoDS_Shape()));
				//objsMap倒着查找，如果是真空，就加入vacuoShape列表，遇到实体，就用实体减去vacuoShape列表,最后用makeCompound组合最后的体
				int gsize = shapsGroup.size();
				std::cerr << "gsize = " << gsize << std::endl;
				std::vector<TopoDS_Shape> finalShapes;
				if (gsize > 0) {

					finalShapes.resize(gsize);

					//Base::Console().Log("gsize:");
					mid = GetTickCount();
					//std::cerr << "mid boolean" << mid << std::endl;
					//std::cerr << "mid boolean" << mid - start << std::endl;
#pragma omp parallel for
					for (int j = 0; j < gsize; j++){
						//std::cerr << "#pragma omp parallel for j:" << j << std::endl;
						if (shapsGroup[j].size() > 0) {
							/*BRep_Builder builder;
							TopoDS_Compound comp;
							builder.MakeCompound(comp);

							for (int i = 0; i < shapsGroup[j].size(); i++) {
							TopoDS_Shape sh = static_cast<Part::Feature*>(objsMap[shapsGroup[j][i]])->Shape.getValue();
							if (!sh.IsNull())
							builder.Add(comp, sh);
							}
							if (!comp.IsNull() && vacuosShapsGroup[j].size() > 0){
							finalShapes[j] = Part::TopoShape(comp).cut(vacuosShapsGroup[j]);
							}
							else
							finalShapes[j] = comp;*/

							int k = 0;
							TopoDS_Shape finalShape;
							for (int i = 0; i < shapsGroup[j].size(); i++) {
								TopoDS_Shape sh = static_cast<Part::Feature*>(objsMap[shapsGroup[j][i]])->Shape.getValue();
								if (!sh.IsNull()) {
									finalShape = sh;
									k = i;
									break;
								}
							}
							std::vector<TopoDS_Shape> tmp;
							for (int i = k + 1; i < shapsGroup[j].size(); i++) {
								TopoDS_Shape sh = static_cast<Part::Feature*>(objsMap[shapsGroup[j][i]])->Shape.getValue();
								if (!sh.IsNull()) {
									tmp.push_back(sh);
								}
							}
							if ((!finalShape.IsNull()) && tmp.size() > 0)
								finalShape = Part::TopoShape(finalShape).fuse(tmp);
							if (!finalShape.IsNull() && !vacuosShapsGroup[j].IsNull()){//.size() > 0
								finalShapes[j] = Part::TopoShape(finalShape).cut(vacuosShapsGroup[j]);
							}
							else
								finalShapes[j] = finalShape;
							/*
							for (int i = 0; i < shapsGroup[j].size(); i++) {
							TopoDS_Shape tmp = static_cast<Part::Feature*>(objsMap[shapsGroup[j][i]])->Shape.getValue();
							if (!tmp.IsNull())
							if (vacuosShapsGroup[j].size() > 0) {
							TopoDS_Shape finalShape = Part::TopoShape(tmp).cut(vacuosShapsGroup[j]);
							finalShapes[shapsGroup[j][i]] = (finalShape);
							}
							else
							finalShapes[shapsGroup[j][i]] = tmp;
							}*/
						}
					}
					Base::Console().Log("\n");
				}
				//测试
				//			clock_t t1, t2;			
				//			t1 = clock();
				//			std::cout << "compound start: " << t1 << std::endl;
				/*for (std::vector<TopoDS_Shape>::iterator it = finalShapes.begin(); it != finalShapes.end(); ++it){
				if (!(*it).IsNull())
				builder.Add(comp, *it);
				}*/
				BRep_Builder builder;
				TopoDS_Compound comp;
				builder.MakeCompound(comp);
				for (int i = 0; i < finalShapes.size(); i++){
					if (!(finalShapes[i]).IsNull())
						builder.Add(comp, finalShapes[i]);
				}
				if (comp.IsNull())
					std::cerr << "TopoDS_Shape:" << 0 << std::endl;
				else
					std::cerr << "TopoDS_Shape:" << 1 << std::endl;
				//if (finalShapes.size() != 0)
				static_cast<Part::Feature*>(resultObj)->Shape.setValue(comp);
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
			//			t2 = clock();
			//			std::cout << "compound end: " << t2 << std::endl;
			//			std::cout << "compound adll: " << (t2 - t1) << std::endl;
			//Part::TopoShape shape(comp);
			//将comp的shape给resultShape


			/*TopoDS_Shape sh = static_cast<Part::Feature*>(resultObj)->Shape.getValue();
			if (sh.IsNull())
			std::cerr << "TopoDS_Shape:" << 0 << std::endl;
			else
			std::cerr << "TopoDS_Shape:" << 1 << std::endl;*/

			//guiPcDoc->setShow(resultObj->getNameInDocument());
			//guiPcDoc->booleanObjectMap = bObjsMap;
			//			pcDoc->recompute();
			pcDoc->flagNeedUpdateBoolean.setValue(-1);



			stop = GetTickCount();
			std::cerr << "end boolean" << stop << std::endl;
			cerr << "bool time:" << (stop - start)*1.0 / 1000 << endl;

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
			PyObject *pcObjsPy;//需要裁减的体数组
			PyObject *toolShapePy;//用于裁减的圆柱体
			PyObject *resultObjPy;//结果
			int showCutFace;//是否显示轮廓0：是
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
						//resultObj = objItem;
						continue;
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

			/*s4 = GetTickCount();
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

			}*/

			//if (bcon) 
			{
				std::vector<int> orderAry;
				//倒序记录order
				for (std::map<int, App::DocumentObject*>::reverse_iterator it = objsMap.rbegin(); it != objsMap.rend(); ++it) {
					orderAry.push_back((*it).first);
				}
				std::vector < std::vector<int> > shapsGroup;
				//std::vector < std::vector<TopoDS_Shape> > vacuosShapsGroup;
				std::vector < TopoDS_Shape > vacuosShapsGroup;
				std::vector<TopoDS_Shape> vacuoGroup;
				TopoDS_Shape vacuoShape = toolShape;
				for (int j = 0; j < orderAry.size(); j++) {
					std::string jattrOfObj = ((App::PropertyEnumeration*)(objsMap[orderAry[j]]->getPropertyByName(S_ATTRIBUTE)))->getValueAsString();
					int befor_vacuo = 0;
					if (strcmp(jattrOfObj.c_str(), S_VACUO) == 0){
						befor_vacuo = 1;
						TopoDS_Shape sh = static_cast<Part::Feature*>(objsMap[orderAry[j]])->Shape.getValue();
						/*if (vacuoShape.IsNull()) {
						vacuoShape = sh;
						continue;
						}*/
						if (!sh.IsNull())
							vacuoGroup.push_back(sh);
						continue;
					}
					std::vector<int> tmpShapsAry;
					tmpShapsAry.push_back(orderAry[j]);

					int i = j + 1;
					for (; i < orderAry.size(); i++, j++) {
						std::string iattrOfObj = ((App::PropertyEnumeration*)(objsMap[orderAry[i]]->getPropertyByName(S_ATTRIBUTE)))->getValueAsString();
						if (strcmp(iattrOfObj.c_str(), S_VACUO) == 0){//当前是真空
							j = i - 1;
							break;
						}
						else {
							tmpShapsAry.push_back(orderAry[i]);
						}
					}
					if (vacuoGroup.size() > 0)
						vacuoShape = Part::TopoShape(vacuoShape).fuse(vacuoGroup);//将S_VACUO融合
					vacuosShapsGroup.push_back(vacuoShape);
					shapsGroup.push_back(tmpShapsAry);
					vacuoGroup.clear();
				}
				//			static_cast<Part::Feature*>(resultObj)->Shape.setValue(*(new TopoDS_Shape()));
				//objsMap倒着查找，如果是真空，就加入vacuoShape列表，遇到实体，就用实体减去vacuoShape列表,最后用makeCompound组合最后的体
				int gsize = shapsGroup.size();
				std::cerr << "gsize = " << gsize << std::endl;
				std::vector<TopoDS_Shape> finalShapes;
				if (gsize > 0) {

					finalShapes.resize(gsize);

					//Base::Console().Log("gsize:");
					//mid = GetTickCount();
					//std::cerr << "mid boolean" << mid << std::endl;
					//std::cerr << "mid boolean" << mid - start << std::endl;
#pragma omp parallel for
					for (int j = 0; j < gsize; j++){
						//std::cerr << "#pragma omp parallel for j:" << j << std::endl;
						if (shapsGroup[j].size() > 0) {
							/*BRep_Builder builder;
							TopoDS_Compound comp;
							builder.MakeCompound(comp);

							for (int i = 0; i < shapsGroup[j].size(); i++) {
							TopoDS_Shape sh = static_cast<Part::Feature*>(objsMap[shapsGroup[j][i]])->Shape.getValue();
							if (!sh.IsNull())
							builder.Add(comp, sh);
							}
							if (!comp.IsNull() && vacuosShapsGroup[j].size() > 0){
							finalShapes[j] = Part::TopoShape(comp).cut(vacuosShapsGroup[j]);
							}
							else
							finalShapes[j] = comp;*/

							int k = 0;
							TopoDS_Shape finalShape;
							for (int i = 0; i < shapsGroup[j].size(); i++) {
								TopoDS_Shape sh = static_cast<Part::Feature*>(objsMap[shapsGroup[j][i]])->Shape.getValue();
								if (!sh.IsNull()) {
									finalShape = sh;
									k = i;
									break;
								}
							}
							std::vector<TopoDS_Shape> tmp;
							for (int i = k + 1; i < shapsGroup[j].size(); i++) {
								TopoDS_Shape sh = static_cast<Part::Feature*>(objsMap[shapsGroup[j][i]])->Shape.getValue();
								if (!sh.IsNull()) {
									tmp.push_back(sh);
								}
							}
							if ((!finalShape.IsNull()) && tmp.size() > 0)
								finalShape = Part::TopoShape(finalShape).fuse(tmp);
							if (!finalShape.IsNull() && !vacuosShapsGroup[j].IsNull()){//.size() > 0
								finalShapes[j] = Part::TopoShape(finalShape).cut(vacuosShapsGroup[j]);
							}
							else
								finalShapes[j] = finalShape;
							/*
							for (int i = 0; i < shapsGroup[j].size(); i++) {
							TopoDS_Shape tmp = static_cast<Part::Feature*>(objsMap[shapsGroup[j][i]])->Shape.getValue();
							if (!tmp.IsNull())
							if (vacuosShapsGroup[j].size() > 0) {
							TopoDS_Shape finalShape = Part::TopoShape(tmp).cut(vacuosShapsGroup[j]);
							finalShapes[shapsGroup[j][i]] = (finalShape);
							}
							else
							finalShapes[shapsGroup[j][i]] = tmp;
							}*/
						}
					}
					Base::Console().Log("\n");
				}
				//测试
				//			clock_t t1, t2;			
				//			t1 = clock();
				//			std::cout << "compound start: " << t1 << std::endl;
				/*for (std::vector<TopoDS_Shape>::iterator it = finalShapes.begin(); it != finalShapes.end(); ++it){
				if (!(*it).IsNull())
				builder.Add(comp, *it);
				}*/
				BRep_Builder builder;
				TopoDS_Compound comp;
				builder.MakeCompound(comp);
				for (int i = 0; i < finalShapes.size(); i++){
					if (!(finalShapes[i]).IsNull())
						builder.Add(comp, finalShapes[i]);
				}
				if (comp.IsNull())
					std::cerr << "TopoDS_Shape:" << 0 << std::endl;
				else
					std::cerr << "TopoDS_Shape:" << 1 << std::endl;
				//if (finalShapes.size() != 0)
				static_cast<Part::Feature*>(resultObj)->Shape.setValue(comp);
			}


			//guiPcDoc->setShow(resultObj->getNameInDocument());
			//guiPcDoc->booleanObjectMap = bObjsMap;
			pcDoc->recompute();
			pcDoc->flagNeedUpdateBoolean.setValue(-1);



			stop = GetTickCount();
			std::cerr << "start end" << (stop - start) / 1000. << std::endl;
			//cerr << "bool time:" << (stop - start)*1.0 / 1000 << endl;

			//stop = GetTickCount();
			//cerr << "bool time:" << (stop - start)*1.0 / 1000 << endl;
			return Py::None();
			;
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
			std::vector<Base::Vector3d> toolVectors(faceToolMap.Extent(), Base::Vector3d(0.0, 0.0, 0.0));

			int i = 1;
			for (; i <= faceBaseMap.Extent() && i <= faceToolMap.Extent(); i++)
			{
				facesBaseVec[i - 1] = (faceBaseMap.FindKey(i));
				facesToolVec[i - 1] = (faceToolMap.FindKey(i));
			}
			//
			while (i <= faceBaseMap.Extent())
			{
				facesBaseVec[i - 1] = (faceBaseMap.FindKey(i));
				i++;
			}
			while (i <= faceToolMap.Extent())
			{
				facesToolVec[i - 1] = (faceToolMap.FindKey(i));
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
									toolVectors[toolFaceIndex] = calculateShapeNormal2(*toolIt);
								if (baseNormal == Base::Vector3d(0.0, 0.0, 0.0))
									baseNormal = calculateShapeNormal2(*baseIt);
								if ((toolVectors[toolFaceIndex] == baseNormal || toolVectors[toolFaceIndex] == (-baseNormal)) && baseNormal != Base::Vector3d(0.0, 0.0, 0.0))
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

			Part::Feature*compoundFeaure = static_cast<Part::Feature*>(compoundObj);
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
			for (; shIt != shapeOfCon.end() || colIt != colorOfCon.end(); ++shIt, ++colIt, ++index)
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
		Py::Object updateBoolean0(const Py::Tuple& args)
		{
			start = GetTickCount();
			int curOrder = 0, beforeOrder = 0, maxOrder = 0;
			if (!PyArg_ParseTuple(args.ptr(), "|ii", &curOrder, &beforeOrder))
				return Py::None();
			App::Document* pcDoc;
			pcDoc = App::GetApplication().getActiveDocument();
			//Gui::Document *guiPcDoc = Gui::Application::Instance->activeDocument();
			if (pcDoc == NULL){
				return Py::None();
			}
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
				(*objIt)->getPropertyList(propList);
				if (propList.size() < 21){
					continue;
				}
				std::vector<App::Property*>::iterator pt;
				for (auto pt = propList.begin(); pt != propList.end(); ++pt){
					const char* name = (*pt)->getName();
					if (strcmp((*pt)->getName(), "Attribute") == 0 && !((App::PropertyEnumeration*)*pt)->isValue("NotDefine")){
						//std::string objAttr = ((App::PropertyEnumeration*)*pt)->getValueAsString();
						App::Property *ret = (*objIt)->getPropertyByName("Order");
						if (ret == 0)
							continue;
						int orderOfObj = ((App::PropertyInteger*)ret)->getValue();
						if (maxOrder < orderOfObj) maxOrder = orderOfObj;
						objsMap[orderOfObj] = (*objIt);
						//objsList.push_back(std::make_pair((*objIt),objAttr));
						break;
					}
				}
			}
			if (objsMap.size() == 0){
				return Py::None();
			}

			if (!resultObj){
				resultObj = pcDoc->addObject("Part::FeaturePython", "ResultShape");
			}

			App::DocumentObject *pcLastConductorObj = NULL;
			std::vector<TopoDS_Shape> vacuoList;
			std::vector<TopoDS_Shape> conductorList;
			TopoDS_Shape resultShape;

			/*if (maxOrder == curOrder && maxOrder == beforeOrder) {
			TopoDS_Shape resultShape = static_cast<Part::Feature*>(resultObj)->Shape.getValue();
			std::string attrOfObj = ((App::PropertyEnumeration*)(objsMap[maxOrder]->getPropertyByName("Attribute")))->getValueAsString();
			if ((strcmp(attrOfObj.c_str(), "Conductor") == 0) || (strcmp(attrOfObj.c_str(), "Custom") == 0)) {
			conductorList.push_back(static_cast<Part::Feature*>(objsMap[maxOrder])->Shape.getValue());
			booleanAdd(resultShape, conductorList);
			}
			else {
			booleanSub(resultShape, resultShape, static_cast<Part::Feature*>(objsMap[maxOrder])->Shape.getValue());
			}
			static_cast<Part::Feature*>(resultObj)->Shape.setValue(resultShape);
			return Py::None();
			}*/

			for (std::map<int, App::DocumentObject*>::const_iterator it = objsMap.begin(); it != objsMap.end(); ++it){
				//guiPcDoc->setHide(it->second->getNameInDocument());
				std::string attrOfObj = ((App::PropertyEnumeration*)(it->second->getPropertyByName("Attribute")))->getValueAsString();
				if ((strcmp(attrOfObj.c_str(), "Conductor") == 0) || (strcmp(attrOfObj.c_str(), "Custom") == 0)){
					if (vacuoList.size() == 0){

						TopoDS_Shape itShape = static_cast<Part::Feature*>(it->second)->Shape.getValue();
						//booleanAddOne(resultShape, itShape);
						conductorList.push_back(itShape);

					}
					else{
						//先将空对象联合
						//std::vector<TopoDS_Shape> s;

						//std::vector<App::DocumentObject*>::iterator itVacuo;
						//for (itVacuo = vacuoList.begin(); itVacuo != vacuoList.end(); ++itVacuo) {
						//	if ((*itVacuo)->getTypeId().isDerivedFrom(Part::Feature::getClassTypeId())) {
						//		s.push_back(static_cast<Part::Feature*>(*itVacuo)->Shape.getValue());
						//	}
						//}
						TopoDS_Shape tempResult;
#pragma omp sections
						{
#pragma omp section
							{
								//所有真空相加
								booleanAdd2(tempResult, vacuoList);
							}
#pragma omp section
							{
								//导体相加
								booleanAdd2(resultShape, conductorList);
							}
						}

						//resultShape=resultShape-tempResult
						booleanSub2(resultShape, resultShape, tempResult);
						vacuoList.clear();
						conductorList.clear();
						//booleanAddOne(resultShape, tempResult);
						//再将这个导体与resultShape 相加
						TopoDS_Shape itShape = static_cast<Part::Feature*>(it->second)->Shape.getValue();
						//booleanAddOne(resultShape, itShape);						
						conductorList.push_back(itShape);
					}

				}
				else{
					//真空
					TopoDS_Shape itShape = static_cast<Part::Feature*>(it->second)->Shape.getValue();
					vacuoList.push_back(itShape);
					//隐藏
					//Gui::Document *guiPcDoc = Gui::Application::Instance->activeDocument();
				}
			}
			if (vacuoList.size() != 0 || conductorList.size() != 0){
				//先将空对象联合
				//std::vector<TopoDS_Shape> s;

				//std::vector<App::DocumentObject*>::iterator it;
				//for (it = vacuoList.begin(); it != vacuoList.end(); ++it) {
				//	if ((*it)->getTypeId().isDerivedFrom(Part::Feature::getClassTypeId())) {
				//		s.push_back(static_cast<Part::Feature*>(*it)->Shape.getValue());
				//	}
				//}
				TopoDS_Shape tempResult;
#pragma omp sections
				{
#pragma omp section
							{
								//所有真空相加
								booleanAdd2(tempResult, vacuoList);
							}
#pragma omp section
							{
								//导体相加
								booleanAdd2(resultShape, conductorList);
							}
				}
				//resultShape=resultShape-tempResult
				booleanSub2(resultShape, resultShape, tempResult);
			}
			//将最终的形状赋给模型
			static_cast<Part::Feature*>(resultObj)->Shape.setValue(resultShape);

			stop = GetTickCount();
			cerr << "tunning time:" << (stop - start)*1.0 / 1000 << endl;
			//pcDoc->updateBoolean();
			return Py::None();
		}

		///Start 草图建模的拉伸
		Py::Object makeExtrude(const Py::Tuple& args){
			const char* baseObjName = 0;
			double length;
			PyObject *pDir = 0;
			if (!PyArg_ParseTuple(args.ptr(), "sd|O!",
				&baseObjName,
				&length,
				&(Base::VectorPy::Type), &pDir))
				throw Py::Exception();

			if (baseObjName == ""){
				std::cerr << "none obj name" << std::endl;
			}
			if (length == 0){
				std::cerr << "none obj name" << std::endl;
			}

			try {
				gp_Dir d(0, 0, 1);
				if (pDir) {
					Base::Vector3d vec = static_cast<Base::VectorPy*>(pDir)->value();
					d.SetCoord(vec.x, vec.y, vec.z);
				}
				App::Document *pcDoc = App::GetApplication().getActiveDocument();
				//先得到基础面
				App::DocumentObject* link = pcDoc->getObject(baseObjName);
				if (!link)
					std::cerr << "No object linked" << std::endl;
				if (!link->getTypeId().isDerivedFrom(Part::Feature::getClassTypeId()))
					std::cerr << "Linked object is not a Part object" << std::endl;
				Part::Feature *base = static_cast<Part::Feature*>(link);
				//先计算法向
				//Extrusion::ExtrusionParameters params = computeFinalParameters();
				//计算平面法向
				//Base::Vector3d dir = calculateShapeNormal(link);
				ExtrusionParameters params = computeFinalParameters(link, length);
				Part::TopoShape result = extrudeShape(base->Shape.getShape(), params);

				return Py::asObject(new Part::TopoShapeSolidPy(new Part::TopoShape(result)));


			}
			catch (...){
				std::cerr << "makeExtrude Error!" << std::endl;
			}
		}

		struct ExtrusionParameters {
			gp_Dir dir;
			double lengthFwd;
			double lengthRev;
			bool solid;
			double taperAngleFwd; //in radians
			double taperAngleRev;
			std::string faceMakerClass;
			ExtrusionParameters() : lengthFwd(0), lengthRev(0), solid(false), taperAngleFwd(0), taperAngleRev(0) {}// constructor to keep garbage out
		};

		ExtrusionParameters computeFinalParameters(App::DocumentObject* obj,
			double length,
			bool isReverse = false,
			bool isSymmetric = false,
			bool isSolid = true,
			double TaperAngle = 0.0,
			double TaperAngleRev = 0.0)
		{
			ExtrusionParameters result;
			Base::Vector3d dir;

			dir = calculateShapeNormal(obj);

			//this->Dir.setValue(dir);
			if (dir.Length() < Precision::Confusion())
				throw Base::ValueError("Direction is zero-length");
			result.dir = gp_Dir(dir.x, dir.y, dir.z);

			if (dir.Length() < Precision::Confusion())
				throw Base::ValueError("Direction is zero-length");
			result.dir = gp_Dir(dir.x, dir.y, dir.z);
			if (isReverse)
				result.dir.Reverse();


			result.lengthFwd = length;
			result.lengthRev = 0.0;
			if (fabs(result.lengthFwd) < Precision::Confusion()
				&& fabs(result.lengthRev) < Precision::Confusion()){
				result.lengthFwd = dir.Length();
			}

			if (isSymmetric){
				result.lengthRev = result.lengthFwd * 0.5;
				result.lengthFwd = result.lengthFwd * 0.5;
			}

			if (fabs(result.lengthFwd + result.lengthRev) < Precision::Confusion())
				throw Base::ValueError("Total length of extrusion is zero.");

			result.solid = isSolid;

			result.taperAngleFwd = TaperAngle * M_PI / 180.0;
			if (fabs(result.taperAngleFwd) > M_PI * 0.5 - Precision::Angular())
				throw Base::ValueError("Magnitude of taper angle matches or exceeds 90 degrees. That is too much.");
			result.taperAngleRev = TaperAngleRev * M_PI / 180.0;
			if (fabs(result.taperAngleRev) > M_PI * 0.5 - Precision::Angular())
				throw Base::ValueError("Magnitude of taper angle matches or exceeds 90 degrees. That is too much.");

			result.faceMakerClass = "";

			return result;
		}



		Part::TopoShape extrudeShape(const Part::TopoShape source, ExtrusionParameters params)
		{
			TopoDS_Shape result;
			gp_Vec vec = gp_Vec(params.dir).Multiplied(params.lengthFwd + params.lengthRev);//total vector of extrusion

			//Regular (non-tapered) extrusion!
			TopoDS_Shape myShape = source.getShape();
			if (myShape.IsNull())
				Standard_Failure::Raise("Cannot extrude empty shape");

			// #0000910: Circles Extrude Only Surfaces, thus use BRepBuilderAPI_Copy
			myShape = BRepBuilderAPI_Copy(myShape).Shape();

			//apply reverse part of extrusion by shifting the source shape
			if (fabs(params.lengthRev) > Precision::Confusion()){
				gp_Trsf mov;
				mov.SetTranslation(gp_Vec(params.dir)*(-params.lengthRev));
				TopLoc_Location loc(mov);
				myShape.Move(loc);
			}

			//make faces from wires
			if (params.solid) {
				//test if we need to make faces from wires. If there are faces - we don't.
				TopExp_Explorer xp(myShape, TopAbs_FACE);
				if (xp.More()){
					//source shape has faces. Just extrude as-is.
				}
				else {
					std::unique_ptr<Part::FaceMaker> mkFace = Part::FaceMaker::ConstructFromType(params.faceMakerClass.c_str());

					if (myShape.ShapeType() == TopAbs_COMPOUND)
						mkFace->useCompound(TopoDS::Compound(myShape));
					else
						mkFace->addShape(myShape);
					mkFace->Build();
					myShape = mkFace->Shape();
				}
			}

			//extrude!
			BRepPrimAPI_MakePrism mkPrism(myShape, vec);
			result = mkPrism.Shape();

			if (result.IsNull())
				throw Base::Exception("Result of extrusion is null shape.");
			return Part::TopoShape(result);
		}

		Base::Vector3d calculateShapeNormal(const App::DocumentObject* shapeLink){
			if (!shapeLink){
				std::cerr << "no resource obj" << std::endl;
			}
			const Part::TopoShape &tsh = static_cast<const Part::Feature*>(shapeLink)->Shape.getShape();
			TopoDS_Shape sh = tsh.getShape();
			if (sh.IsNull())
				throw Base::Exception("calculateShapeNormal: link points to a valid object, but its shape is null.");
			//find plane
			BRepLib_FindSurface planeFinder(sh, -1, /*OnlyPlane=*/true);
			if (!planeFinder.Found())
				throw Base::ValueError("Can't find normal direction, because the shape is not on a plane.");

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

			}
			return Base::Vector3d(normal.X(), normal.Y(), normal.Z());
		}
		///End 草图建模的拉伸
		/// start 旋转体
		TopoDS_Shape revolutionShape(App::DocumentObject *pAreaObj, Base::Vector3d base, Base::Vector3d axis, double angle)
		{
			App::DocumentObject* link = pAreaObj;
			if (!link)
			{
				std::cerr << "base Area is None" << std::endl;
				throw Py::Exception(Part::PartExceptionOCCDomainError, "revolutionShape error");
				//return NULL;
			}
			if (!link->getTypeId().isDerivedFrom(Part::Feature::getClassTypeId()))
			{
				std::cerr << "base Area is not a part shape" << std::endl;
				throw Py::Exception(Part::PartExceptionOCCDomainError, "revolutionShape error");
				//return NULL;
			}
			//return new App::DocumentObjectExecReturn("Linked object is not a Part object");
			Part::Feature *baseObj = static_cast<Part::Feature*>(pAreaObj);

			try {
				//read out axis link
				double angle_edge = 0;
				Base::Vector3d b = base;
				Base::Vector3d v = axis;
				/*bool linkFetched = this->fetchAxisLink(this->AxisLink, b, v, angle_edge);
				if (linkFetched){
				this->Base.setValue(b);
				this->Axis.setValue(v);
				}*/

				gp_Pnt pnt(b.x, b.y, b.z);
				gp_Dir dir(v.x, v.y, v.z);
				gp_Ax1 revAx(pnt, dir);

				//read out revolution angle
				double thisAngle = angle / 180.0f*M_PI;
				if (fabs(thisAngle) < Precision::Angular())
					thisAngle = angle_edge;

				//apply "midplane" symmetry
				Part::TopoShape sourceShape = baseObj->Shape.getShape();
				/*if (Symmetric.getValue()) {
				//rotate source shape backwards by half thisAngle, to make resulting revolution symmetric to the profile
				gp_Trsf mov;
				mov.SetRotation(revAx, thisAngle * (-0.5));
				TopLoc_Location loc(mov);
				sourceShape.setShape(sourceShape.getShape().Moved(loc));
				}*/

				//"make solid" processing: make faces from wires.
				Standard_Boolean makeSolid = Standard_True;
				if (makeSolid){
					//test if we need to make faces from wires. If there are faces - we don't.
					TopExp_Explorer xp(sourceShape.getShape(), TopAbs_FACE);
					if (xp.More())
						//source shape has faces. Just revolve as-is.
						makeSolid = Standard_False;
				}
				std::string faceMakerClass = "Part::FaceMakerBullseye";
				if (makeSolid && strlen(faceMakerClass.c_str()) > 0){
					//new facemaking behavior: use facemaker class
					std::unique_ptr<Part::FaceMaker> mkFace = Part::FaceMaker::ConstructFromType(faceMakerClass.c_str());

					TopoDS_Shape myShape = sourceShape.getShape();
					if (myShape.ShapeType() == TopAbs_COMPOUND)
						mkFace->useCompound(TopoDS::Compound(myShape));
					else
						mkFace->addShape(myShape);
					mkFace->Build();
					myShape = mkFace->Shape();
					sourceShape = Part::TopoShape(myShape);

					makeSolid = Standard_False;//don't ask TopoShape::revolve to make solid, as we've made faces...
				}

				// actual revolution!
				TopoDS_Shape revolve = sourceShape.revolve(revAx, thisAngle, makeSolid);

				return revolve;
			}
			catch (Standard_Failure& e) {
				std::cerr << "make revolution error" << std::endl;
				throw Py::Exception(Part::PartExceptionOCCDomainError, "revolutionShape error");
				//return new App::DocumentObjectExecReturn(e.GetMessageString());
			}
		}
		Py::Object makePicRevolution(const Py::Tuple& args)
		{
			const char* baseAreaName = 0;
			PyObject *pBase = 0;
			PyObject *pAxis = 0;
			double angle = 360;

			if (!PyArg_ParseTuple(args.ptr(), "sd|O!O!",
				&baseAreaName,
				&angle,
				&(Base::VectorPy::Type), &pBase,
				&(Base::VectorPy::Type), &pAxis))
				throw Py::Exception();
			try{
				Base::Vector3d p1(0, 0, 0);
				Base::Vector3d p2(0, 0, 1);

				if (pBase) {
					p1 = static_cast<Base::VectorPy*>(pBase)->value();
				}
				if (pAxis) {
					p2 = static_cast<Base::VectorPy*>(pAxis)->value();
				}
				//基点
				Base::Vector3d base = p1;
				//方向
				Base::Vector3d axis = p2 - p1;
				//基础面对象
				App::Document* pcDoc = App::GetApplication().getActiveDocument();
				App::DocumentObject *pAreaObj = pcDoc->getObject(baseAreaName);

				TopoDS_Shape resultShape = revolutionShape(pAreaObj, base, axis, angle);
				if (resultShape.IsNull()){
					throw Py::Exception(Part::PartExceptionOCCDomainError, "revolution shape is null");
				}
				//if (resultShape->IsNull()){
				//	throw Py::Exception(PartExceptionOCCDomainError, "revolution shape is null");
				//}
				return Py::asObject(new Part::TopoShapeSolidPy(new Part::TopoShape(resultShape)));

			}
			catch (Standard_DomainError) {
				throw Py::Exception(Part::PartExceptionOCCDomainError, "creation of revolution failed");
			}

		}

		void testTime(std::string mark, clock_t &t0, clock_t t1){
			t1 = clock();
			std::cerr << mark << " " << double(t1 - t0) << std::endl;
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
		//复制Shape和DiffuseColor
		void copyDocumentObj(App::DocumentObject&finalObj, std::vector<App::Color>& color, float& transparency, App::DocumentObject* beCopyObj){
			static_cast<Part::Feature*>(&finalObj)->Shape.setValue(static_cast<Part::Feature*>(beCopyObj)->Shape.getValue());

			Gui::ViewProvider* vpBase = Gui::Application::Instance->getViewProvider(beCopyObj);
			color = static_cast<PartGui::ViewProviderPart*>(vpBase)->DiffuseColor.getValues();
			transparency = static_cast<PartGui::ViewProviderPart*>(vpBase)->Transparency.getValue();
			//vp =(Gui::Application::Instance->getViewProvider(beCopyObj));
		}
		Py::Object updateBoolean2(const Py::Tuple& args)
		{
			DWORD start, stop;
			start = GetTickCount();
			std::cerr << "start boolean" << std::endl;
			int changedOrder = 0, beforeOrder = 0;
			if (!PyArg_ParseTuple(args.ptr(), "|ii", &changedOrder, &beforeOrder))
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
				if ((it)->first >= changedOrder)
					bObjsMap.erase((it)->first);
			}
			//所有需要做布尔运算的模型，即有Attribute且不为未定义的模型
			//std::vector<std::pair<App::DocumentObject*,std::string>> objsList;
			std::map<int, App::DocumentObject*> objsMap;
			std::vector<int> objsOrderVec;
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
						objsOrderVec.push_back(orderOfObj);
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

			if (objsOrderVec.size() < 1)
				return Py::None();

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
			//按Order排序
			//默认为升序
			std::sort(objsOrderVec.begin(), objsOrderVec.end());
			std::vector<int> voidOrderVec;
			std::vector<std::vector<App::DocumentObject*>> objVecVec;
			std::vector<int> attVec;
			for (int ii = 0; ii < objsOrderVec.size(); ii++) {
				std::vector<App::DocumentObject*> condMap;
				int flag = 0;
				std::string attrOfObj = ((App::PropertyEnumeration*)(objsMap[ii]->getPropertyByName("Attribute")))->getValueAsString();
				if (!((strcmp(attrOfObj.c_str(), "Conductor") == 0) || (strcmp(attrOfObj.c_str(), "Custom") == 0))){
					flag = 1;
				}
				attVec.push_back(flag);
				int flagJJ = 0;
				for (int jj = ii; jj < objsOrderVec.size(); jj++) {
					std::string attrOfObjJJ = ((App::PropertyEnumeration*)(objsMap[jj]->getPropertyByName("Attribute")))->getValueAsString();
					if (!((strcmp(attrOfObjJJ.c_str(), "Conductor") == 0) || (strcmp(attrOfObjJJ.c_str(), "Custom") == 0))){
						flagJJ = 1;
					}
					else flagJJ = 0;
					if (flag != flagJJ) {
						ii = jj - 1;
						break;
					}
					condMap.push_back(objsMap[jj]);
				}
				objVecVec.push_back(condMap);
			}
			std::vector<TopoDS_Shape> tempResults;
			tempResults.resize(attVec.size());
			for (int ii = 0; ii < attVec.size(); ii++) {
				;
			}
			for (std::map<int, App::DocumentObject*>::const_iterator it = objsMap.begin(); it != objsMap.end(); ++it){
				guiPcDoc->setHide(it->second->getNameInDocument());
				int objOrder = ((App::PropertyInteger*)(it->second->getPropertyByName("Order")))->getValue();
				/*if (objOrder <= startOrder){
				continue;
				}
				Part::Feature *lastResultObj = new Part::Feature();
				std::vector<App::Color> lastColor;
				float lastTransparency = 0.0;

				copyDocumentObj(*lastResultObj, lastColor, lastTransparency, resultObj);*/

				std::string attrOfObj = ((App::PropertyEnumeration*)(it->second->getPropertyByName("Attribute")))->getValueAsString();
				if ((strcmp(attrOfObj.c_str(), "Conductor") == 0) || (strcmp(attrOfObj.c_str(), "Custom") == 0)){
					booleanAdd(*resultObj, resultObj, it->second);

					/*Part::Feature *curResultObj = new Part::Feature();
					std::vector<App::Color> curColor;
					float curTransparency = 0.0;

					copyDocumentObj(*curResultObj, curColor, curTransparency, resultObj);

					Gui::BooleanObjects bo = { objOrder, lastResultObj, lastColor, lastTransparency, curResultObj, curColor, curTransparency };
					bObjsMap[objOrder] = bo;*/
				}
				else{
					booleanSub(*resultObj, resultObj, it->second);

					/*Part::Feature *curResultObj = new Part::Feature();
					std::vector<App::Color> curColor;
					float curTransparency = 0.0;

					copyDocumentObj(*curResultObj, curColor, curTransparency, resultObj);

					Gui::BooleanObjects bo = { objOrder, lastResultObj, lastColor, lastTransparency, curResultObj, curColor, curTransparency };
					bObjsMap[objOrder] = bo;*/
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
		Py::Object makeFuncMesh(const Py::Tuple& args)
		{
			//clock_t t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10;
			//由面形成实体的精确度 如果函数体的范围是1-10  将精确度设置为0.001（否则会很慢），一般情况下设置为0.01，
			Standard_Real facePrecision = 0.01;
			//type=0表示面，1表示体
			int type = 0;
			double angle = 360;
			char* func;
			double xmax, xmin, ymax, ymin, zmax, zmin = 0;
			double xmaxo, xmino, ymaxo, ymino, zmaxo, zmino = 0;
			char* coor;
			//精度
			char* precision;
			char* attribute;
			PyObject *pPnt = 0, *pDir = 0;
			if (!PyArg_ParseTuple(args.ptr(), "isddddddsss",
				&type, &func, &xmin, &xmax, &ymin, &ymax, &zmin, &zmax, &coor, &precision, &attribute
				))
				throw Py::Exception();

			try {

				/*//t0 = clock();
				//输出文件
				//std::string filePath(path);
				//生成文件，如果存在删除重来
				//std::ofstream file(path, std::ios::trunc);
				std::string jsonTemp = "";
				//面
				if (type == 0){
				jsonTemp = "{\n"
				"    \"MathModels\": [\n"
				"        {\n"
				"            \"Iso3D\": {\n"
				"                \"Cnd\": [\n"
				"                    \"\"\n"
				"                ],\n"
				"                \"Component\": [\n"
				"                    \"Model\"\n"
				"                ],\n"
				"                \"Fxyz\": [\n"
				"                    \"%1%\"\n"
				"                ],\n"
				"                \"Name\": [\n"
				"                    \"Model\"\n"
				"                ],\n"
				"                \"Xmax\": [\n"
				"                    \"%3%\"\n"
				"                ],\n"
				"                \"Xmin\": [\n"
				"                    \"%2%\"\n"
				"                ],\n"
				"                \"Ymax\": [\n"
				"                    \"%5%\"\n"
				"                ],\n"
				"                \"Ymin\": [\n"
				"                    \"%4%\"\n"
				"                ],\n"
				"                \"Zmax\": [\n"
				"                    \"%7%\"\n"
				"                ],\n"
				"                \"Zmin\": [\n"
				"                    \"%6%\"\n"
				"                ]\n"
				"            }\n"
				"        }\n"
				"    ]\n"
				"}\n"
				;
				//求六个边界点中绝对值较大的点
				double  absXmin = abs(xmin);
				double  absYmin = abs(ymin);
				double  absZmin = abs(zmin);
				double  absXmax = abs(xmax);
				double  absYmax = abs(ymax);
				double  absZmax = abs(zmax);
				//
				double absmax = absXmin;
				if (absmax < absYmin)
				{
				absmax = absYmin;

				}
				if (absmax < absZmin)
				absmax = absZmin;
				if (absmax < absXmax)
				absmax = absXmax;
				if (absmax < absYmax)
				absmax = absYmax;
				if (absmax < absZmax)
				absmax = absZmax;
				//这里确定面的精确度
				if (1.0 < absmax && absmax < 10.0)
				facePrecision = 0.001;
				}
				//体
				else{
				jsonTemp = "{\n"
				"    \"MathModels\": [\n"
				"        {\n"
				"            \"Iso3D\": {\n"
				"                \"Cnd\": [\n"
				"                    \"\"\n"
				"                ],\n"
				"                \"Component\": [\n"
				"                    \"Model\"\n"
				"                ],\n"
				"                \"Fxyz\": [\n"
				"                    \"if(x=%2%,1,if(x=%3%,1,if(y=%4%,1,if(y=%5%,1,if(z=%6%,1,if(z=%7%,1,%1%))))))\"\n"
				"                ],\n"
				"                \"Name\": [\n"
				"                    \"Model\"\n"
				"                ],\n"
				"                \"Xmax\": [\n"
				"                    \"%3%\"\n"
				"                ],\n"
				"                \"Xmin\": [\n"
				"                    \"%2%\"\n"
				"                ],\n"
				"                \"Ymax\": [\n"
				"                    \"%5%\"\n"
				"                ],\n"
				"                \"Ymin\": [\n"
				"                    \"%4%\"\n"
				"                ],\n"
				"                \"Zmax\": [\n"
				"                    \"%7%\"\n"
				"                ],\n"
				"                \"Zmin\": [\n"
				"                    \"%6%\"\n"
				"                ]\n"
				"            }\n"
				"        }\n"
				"    ]\n"
				"}\n"
				;
				//求六个边界点中绝对值较大的点

				double deltax = (xmax - xmin) / 20;
				double deltay = (ymax - ymin) / 20;
				double deltaz = (zmax - zmin) / 20;
				xmin -= 2*deltax;
				xmax += 2 * deltax;
				ymin -= 2 * deltay;
				ymax += 2 * deltay;
				zmin -= 2 * deltaz;
				zmax += 2 * deltaz;
				}
				facePrecision = 0.00001;*/
				/*boost::format fmt(jsonTemp);
				fmt%func% xmin % xmax % ymin %ymax%zmin%zmax;
				file << fmt.str();
				file.close();
				//获取当前应用程序路径
				//t1 = clock();
				//std::cerr << "makeFunc Mesh 1" << double(t1 - t0) << std::endl;

				char exeFullPath[MAX_PATH]; // Full path

				std::string strPath = "";

				GetModuleFileName(NULL, exeFullPath, MAX_PATH);

				strPath = (std::string)exeFullPath;    // Get full path of the file

				int pos = strPath.find_last_of('\\', strPath.length());

				std::string exePath = strPath.substr(0, pos);  // Return the directory without the file name
				exePath = exePath + "\\..\\Mod\\Modeling\\MathMod\\MathMod.exe";
				std::string objPath = filePath.substr(0, filePath.length() - 5) + ".obj";
				//如果是带引号的路径，则替换包括最末位的引号
				if (filePath[filePath.length() - 1] == '\"')
				{
				objPath = filePath.substr(0, filePath.length() - 6) + ".obj\"";
				}

				//运行程序--
				STARTUPINFO stStartUpInfo;
				::memset(&stStartUpInfo, 0, sizeof(stStartUpInfo));
				stStartUpInfo.lpReserved = NULL;
				stStartUpInfo.lpDesktop = NULL;
				stStartUpInfo.lpTitle = NULL;
				stStartUpInfo.cbReserved2 = NULL;
				stStartUpInfo.lpReserved2 = NULL;
				stStartUpInfo.cb = sizeof(stStartUpInfo);
				stStartUpInfo.dwFlags = STARTF_USESHOWWINDOW;
				stStartUpInfo.wShowWindow = 0;// SW_HIDE;
				PROCESS_INFORMATION stProcessInfo;
				::memset(&stProcessInfo, 0, sizeof(stProcessInfo));

				LPSTR szCmd = (LPSTR)(exePath.c_str());
				std::string precisionS = precision;
				//参数加上精度信息
				filePath = " " + filePath + " " + precisionS;
				LPSTR fileCmd = (LPSTR)(filePath.c_str());

				//先把已占文件删除
				Base::FileInfo fi(objPath);
				if (fi.exists() && fi.isFile())
				{
				fi.deleteFile();
				}

				try
				{
				bool bRet = ::CreateProcess(
				szCmd,
				fileCmd,
				NULL,
				NULL,
				false,
				CREATE_NEW_CONSOLE,
				NULL,
				NULL,
				&stStartUpInfo,
				&stProcessInfo);
				//testTime("t2 ", t0, t1);
				if (bRet)
				{
				//等待后关闭进程

				bool noexist = true;

				//等10秒，超时文件还不存在就是生成失败
				Sleep(1000);
				for (size_t i = 0; i < 100; i++)
				{
				Sleep(100);
				Base::FileInfo fi(objPath);
				if (fi.exists() && fi.isFile())
				{
				noexist = false;
				break;
				}

				}
				//testTime("t3 ", t0, t1);


				DWORD dwEC = 0;
				BOOL b = GetExitCodeProcess(
				stProcessInfo.hProcess,
				&dwEC
				);



				if (b)
				{
				TerminateProcess(stProcessInfo.hProcess, dwEC);
				}


				::CloseHandle(stProcessInfo.hProcess);
				::CloseHandle(stProcessInfo.hThread);
				stProcessInfo.hProcess = NULL;
				stProcessInfo.hThread = NULL;
				stProcessInfo.dwProcessId = 0;
				stProcessInfo.dwThreadId = 0;

				if (noexist)
				{
				throw Py::Exception(Part::PartExceptionOCCError, " Cant make Function Mesh");
				}
				}
				else
				{
				//如果创建进程失败，查看错误码
				DWORD dwErrCode = GetLastError();
				printf_s("ErrCode : %d\n", dwErrCode);

				}
				}
				catch (...)
				{
				}

				*/
				//划分为6个象限
				boost::format fmt("if(x=%2%,1,if(x=%3%,1,if(y=%4%,1,if(y=%5%,1,if(z=%6%,1,if(z=%7%,1,%1%))))))");
				fmt%func% xmin % xmax % ymin %ymax%zmin%zmax;
				Base::Console().Log("fmt: ");
				Base::Console().Log(fmt.str().c_str());
				xmino = xmin;
				xmaxo = xmax;
				ymino = ymin;
				ymaxo = ymax;
				zmino = zmin;
				zmaxo = zmax;
				PM3::ExpParser exparser;
				vcg::Point3d Start, End;
				std::string er;
				PM3::DefValue3D far_ori, near_ori;
				double yreso = (ymax - ymin) * 3.1415926 / 20. / 180;
				if (std::string(attribute) == "Void")
				{
					if (std::string(coor) == S_COOR_RECTANGULAR) {
						far_ori.X() = PM3::convertToStringd(xmax + 0.0001);
						far_ori.Y() = PM3::convertToStringd(ymax + 0.0001);
						far_ori.Z() = PM3::convertToStringd(zmax + 0.0001);
						near_ori.X() = PM3::convertToStringd(xmin - 0.0001);
						near_ori.Y() = PM3::convertToStringd(ymin - 0.0001);
						near_ori.Z() = PM3::convertToStringd(zmin - 0.0001);
						far_ori.Parser(&exparser, End, er);
						near_ori.Parser(&exparser, Start, er);
					}
					else {
						far_ori.X() = PM3::convertToStringd(xmax + 0.0001);
						far_ori.Y() = PM3::convertToStringd(ymax + 0.01);
						far_ori.Z() = PM3::convertToStringd(zmax + 0.0001);
						near_ori.X() = PM3::convertToStringd(xmin - 0.0001);
						near_ori.Y() = PM3::convertToStringd(ymin - 0.01);
						near_ori.Z() = PM3::convertToStringd(zmin - 0.0001);
						far_ori.Parser(&exparser, End, er);
						near_ori.Parser(&exparser, Start, er);
					}
				}
				else
				{
					far_ori.X() = PM3::convertToStringd(xmax);
					far_ori.Y() = PM3::convertToStringd(ymax);
					far_ori.Z() = PM3::convertToStringd(zmax);
					near_ori.X() = PM3::convertToStringd(xmin);
					near_ori.Y() = PM3::convertToStringd(ymin);
					near_ori.Z() = PM3::convertToStringd(zmin);
					far_ori.Parser(&exparser, End, er);
					near_ori.Parser(&exparser, Start, er);
				}

				{//计算边界
					//存放点
					std::vector<Base::Vector3d> Points;
					//存放面
					std::vector<Data::ComplexGeoData::Facet> Facets;
					double maxf = -1;
					Mesh::MeshObject mesh;
					PM3::VFunctional vfunc;
					vfunc.yreso = -1;// yreso;
					if (std::string(coor) == S_COOR_RECTANGULAR)
						vfunc.setSystem(PM3::SYSCARTESIAN);
					else
						vfunc.setSystem(PM3::SYSCYLINDRICAL);
					vfunc.f = func;
					vfunc.name = "bbox";
					PM3::DefValue3D far_pointV, near_pointV;
					if (std::string(coor) == S_COOR_RECTANGULAR) {
						//vfunc.setSystem(PM3::SYSCARTESIAN);
						PM3::DefValue3D far_point, near_point;
						far_point.X() = PM3::convertToStringd(End[0]) + "m";
						far_point.Y() = PM3::convertToStringd(End[1]) + "m";
						far_point.Z() = PM3::convertToStringd(End[2]) + "m";
						near_point.X() = PM3::convertToStringd(Start[0]) + "m";
						near_point.Y() = PM3::convertToStringd(Start[1]) + "m";
						near_point.Z() = PM3::convertToStringd(Start[2]) + "m";
						far_pointV = (far_point);
						near_pointV = (near_point);
					}
					else {
						PM3::DefValue3D far_point, near_point;
						far_point.X() = PM3::convertToStringd(xmax) + "m";
						far_point.Y() = PM3::convertToStringd(ymax) + "deg";
						far_point.Z() = PM3::convertToStringd(zmax) + "m";
						near_point.X() = PM3::convertToStringd(xmin) + "m";
						near_point.Y() = PM3::convertToStringd(ymin) + "deg";
						near_point.Z() = PM3::convertToStringd(zmin) + "m";
						far_pointV = (far_point);
						near_pointV = (near_point);
					}
					vfunc.far_point = far_pointV;// .setValue(PM3::convertToStringd(xmax) + "," + PM3::convertToStringd(ymax) + "," + PM3::convertToStringd(zmax));
					vfunc.near_point = near_pointV;// .setValue(PM3::convertToStringd(xmin) + "," + PM3::convertToStringd(ymin) + "," + PM3::convertToStringd(zmin));
					PM3::ExpParser exparser;
					vfunc.pexparser = &exparser;

					vfunc.update_mesh_topology(Points, Facets, maxf);
					vcg::Point3d nStart = Start, nEnd = End;
					if (Facets.size() > 0)
					{
						mesh.setFacets(Facets, Points);
						Base::BoundBox3d bbox = mesh.getBoundBox();
						Start = vcg::Point3d(bbox.MinX, bbox.MinY, bbox.MinZ);
						End = vcg::Point3d(bbox.MaxX, bbox.MaxY, bbox.MaxZ);
						if (std::string(coor) == S_COOR_RECTANGULAR)
						{
							xmin = Start[0] - 1 * vfunc.iso->Step[0];
							//if (xmin < xmino) xmin = xmino;
							xmax = End[0] + 1 * vfunc.iso->Step[0];
							//if (xmax > xmaxo) xmax = xmaxo;
							ymin = Start[1] - 1 * vfunc.iso->Step[1];
							ymax = End[1] + 1 * vfunc.iso->Step[1];
							zmin = Start[2] - 1 * vfunc.iso->Step[2];
							//if (zmin < zmino) zmin = zmino;
							zmax = End[2] + 1 * vfunc.iso->Step[2];
							//if (zmax > zmaxo) zmax = zmaxo;
						}
						else //if (std::string(coor) != "Rectangular")
						{
							xmin = Start[0] - 1 * vfunc.iso->Step[0];
							if (xmin < 0) xmin = 0;
							//if (xmin < xmino) xmin = xmino;
							xmax = End[0] + 1 * vfunc.iso->Step[0];
							//if (xmax > xmaxo) xmax = xmaxo;
							ymin = Start[1] * 180. / PM3::pi() - 1 * (ymaxo - ymino) / 20.;
							if (ymin < ymino) ymin = ymino;
							ymax = End[1] * 180. / PM3::pi() + 1 * (ymaxo - ymino) / 20.;
							if (ymax > ymaxo) ymax = ymaxo;
							zmin = Start[2] - 1 * vfunc.iso->Step[2];
							//if (zmin < zmino) zmin = zmino;
							zmax = End[2] + 1 * vfunc.iso->Step[2];
							//if (zmax > zmaxo) zmax = zmaxo;
						}
					}
				}
				int nb_ligne = 10, nb_colon = 10, nb_depth = 10;

				yreso = (ymax - ymin) * 3.1415926 / (8) / 180;
				if (std::string(attribute) == "Void")
				{
					if (std::string(coor) == S_COOR_RECTANGULAR) {
						far_ori.X() = PM3::convertToStringd(xmax + 0.0001);
						far_ori.Y() = PM3::convertToStringd(ymax + 0.0001);
						far_ori.Z() = PM3::convertToStringd(zmax + 0.0001);
						near_ori.X() = PM3::convertToStringd(xmin - 0.0001);
						near_ori.Y() = PM3::convertToStringd(ymin - 0.0001);
						near_ori.Z() = PM3::convertToStringd(zmin - 0.0001);
						far_ori.Parser(&exparser, End, er);
						near_ori.Parser(&exparser, Start, er);
					}
					else {
						far_ori.X() = PM3::convertToStringd(xmax + 0.0001);
						far_ori.Y() = PM3::convertToStringd(ymax + 0.01);
						far_ori.Z() = PM3::convertToStringd(zmax + 0.0001);
						near_ori.X() = PM3::convertToStringd(xmin - 0.0001);
						near_ori.Y() = PM3::convertToStringd(ymin - 0.01);
						near_ori.Z() = PM3::convertToStringd(zmin - 0.0001);
						far_ori.Parser(&exparser, End, er);
						near_ori.Parser(&exparser, Start, er);
					}
				}
				else
				{
					far_ori.X() = PM3::convertToStringd(xmax);
					far_ori.Y() = PM3::convertToStringd(ymax);
					far_ori.Z() = PM3::convertToStringd(zmax);
					near_ori.X() = PM3::convertToStringd(xmin);
					near_ori.Y() = PM3::convertToStringd(ymin);
					near_ori.Z() = PM3::convertToStringd(zmin);
					far_ori.Parser(&exparser, End, er);
					near_ori.Parser(&exparser, Start, er);
				}
				{
					xmax = End.X();
					ymax = End.Y();
					zmax = End.Z();
					xmin = Start.X();
					ymin = Start.Y();
					zmin = Start.Z();
				}
				std::vector<PM3::DefValue3D> far_pointV, near_pointV, far_pointVo, near_pointVo;
				if (std::string(coor) == S_COOR_RECTANGULAR) {
					nb_ligne = 20, nb_colon = 20, nb_depth = 20;

					yreso = (ymax - ymin) / (20 - 4) / 180;
					//vfunc.setSystem(PM3::SYSCARTESIAN);
					PM3::DefValue3D far_point, near_point;
					far_point.X() = PM3::convertToStringd(xmax) + "m";
					far_point.Y() = PM3::convertToStringd(ymax) + "m";
					far_point.Z() = PM3::convertToStringd(zmax) + "m";
					near_point.X() = PM3::convertToStringd(xmin) + "m";
					near_point.Y() = PM3::convertToStringd(ymin) + "m";
					near_point.Z() = PM3::convertToStringd(zmin) + "m";
					far_pointV.push_back(far_point);
					near_pointV.push_back(near_point);
					far_point.X() = PM3::convertToStringd(xmaxo) + "m";
					far_point.Y() = PM3::convertToStringd(ymaxo) + "m";
					far_point.Z() = PM3::convertToStringd(zmaxo) + "m";
					near_point.X() = PM3::convertToStringd(xmino) + "m";
					near_point.Y() = PM3::convertToStringd(ymino) + "m";
					near_point.Z() = PM3::convertToStringd(zmino) + "m";
					far_pointVo.push_back(far_point);
					near_pointVo.push_back(near_point);
				}
				else {
					nb_ligne = 20, nb_colon = 8, nb_depth = 20;
					yreso = 90 * 3.1415926 / (nb_colon) / 180;
					if (ymax > 270) {
						if (ymin > 270) {
							PM3::DefValue3D far_point, near_point;
							far_point.X() = PM3::convertToStringd(xmax) + "m";
							far_point.Y() = PM3::convertToStringd(ymax) + "deg";
							far_point.Z() = PM3::convertToStringd(zmax) + "m";
							near_point.X() = PM3::convertToStringd(xmin) + "m";
							near_point.Y() = PM3::convertToStringd(ymin) + "deg";
							near_point.Z() = PM3::convertToStringd(zmin) + "m";
							far_pointV.push_back(far_point);
							near_pointV.push_back(near_point);

							far_point.X() = PM3::convertToStringd(xmaxo) + "m";
							far_point.Y() = PM3::convertToStringd(ymaxo) + "deg";
							far_point.Z() = PM3::convertToStringd(zmaxo) + "m";
							near_point.X() = PM3::convertToStringd(xmino) + "m";
							near_point.Y() = PM3::convertToStringd(ymino) + "deg";
							near_point.Z() = PM3::convertToStringd(zmino) + "m";
							far_pointVo.push_back(far_point);
							near_pointVo.push_back(near_point);
						}
						else if (ymin > 180) {
							PM3::DefValue3D far_point, near_point;
							far_point.X() = PM3::convertToStringd(xmax) + "m";
							far_point.Y() = PM3::convertToStringd(ymax) + "deg";
							far_point.Z() = PM3::convertToStringd(zmax) + "m";
							near_point.X() = PM3::convertToStringd(xmin) + "m";
							near_point.Y() = PM3::convertToStringd(270) + "deg";
							near_point.Z() = PM3::convertToStringd(zmin) + "m";
							far_pointV.push_back(far_point);
							near_pointV.push_back(near_point);
							far_point.X() = PM3::convertToStringd(xmaxo) + "m";
							far_point.Y() = PM3::convertToStringd(ymaxo) + "deg";
							far_point.Z() = PM3::convertToStringd(zmaxo) + "m";
							near_point.X() = PM3::convertToStringd(xmino) + "m";
							near_point.Y() = PM3::convertToStringd(270) + "deg";
							near_point.Z() = PM3::convertToStringd(zmino) + "m";
							far_pointVo.push_back(far_point);
							near_pointVo.push_back(near_point);
							far_point.X() = PM3::convertToStringd(xmax) + "m";
							far_point.Y() = PM3::convertToStringd(270) + "deg";
							far_point.Z() = PM3::convertToStringd(zmax) + "m";
							near_point.X() = PM3::convertToStringd(xmin) + "m";
							near_point.Y() = PM3::convertToStringd(ymin) + "deg";
							near_point.Z() = PM3::convertToStringd(zmin) + "m";
							far_pointV.push_back(far_point);
							near_pointV.push_back(near_point);
							far_point.X() = PM3::convertToStringd(xmaxo) + "m";
							far_point.Y() = PM3::convertToStringd(270) + "deg";
							far_point.Z() = PM3::convertToStringd(zmaxo) + "m";
							near_point.X() = PM3::convertToStringd(xmino) + "m";
							near_point.Y() = PM3::convertToStringd(ymino) + "deg";
							near_point.Z() = PM3::convertToStringd(zmino) + "m";
							far_pointVo.push_back(far_point);
							near_pointVo.push_back(near_point);
						}
						else if (ymin > 90) {
							PM3::DefValue3D far_point, near_point;
							far_point.X() = PM3::convertToStringd(xmax) + "m";
							far_point.Y() = PM3::convertToStringd(ymax) + "deg";
							far_point.Z() = PM3::convertToStringd(zmax) + "m";
							near_point.X() = PM3::convertToStringd(xmin) + "m";
							near_point.Y() = PM3::convertToStringd(270) + "deg";
							near_point.Z() = PM3::convertToStringd(zmin) + "m";
							far_pointV.push_back(far_point);
							near_pointV.push_back(near_point);
							far_point.X() = PM3::convertToStringd(xmaxo) + "m";
							far_point.Y() = PM3::convertToStringd(ymaxo) + "deg";
							far_point.Z() = PM3::convertToStringd(zmaxo) + "m";
							near_point.X() = PM3::convertToStringd(xmino) + "m";
							near_point.Y() = PM3::convertToStringd(270) + "deg";
							near_point.Z() = PM3::convertToStringd(zmino) + "m";
							far_pointVo.push_back(far_point);
							near_pointVo.push_back(near_point);
							far_point.X() = PM3::convertToStringd(xmax) + "m";
							far_point.Y() = PM3::convertToStringd(270) + "deg";
							far_point.Z() = PM3::convertToStringd(zmax) + "m";
							near_point.X() = PM3::convertToStringd(xmin) + "m";
							near_point.Y() = PM3::convertToStringd(180) + "deg";
							near_point.Z() = PM3::convertToStringd(zmin) + "m";
							far_pointV.push_back(far_point);
							near_pointV.push_back(near_point);
							far_point.X() = PM3::convertToStringd(xmaxo) + "m";
							far_point.Y() = PM3::convertToStringd(270) + "deg";
							far_point.Z() = PM3::convertToStringd(zmaxo) + "m";
							near_point.X() = PM3::convertToStringd(xmino) + "m";
							near_point.Y() = PM3::convertToStringd(180) + "deg";
							near_point.Z() = PM3::convertToStringd(zmino) + "m";
							far_pointVo.push_back(far_point);
							near_pointVo.push_back(near_point);
							far_point.X() = PM3::convertToStringd(xmax) + "m";
							far_point.Y() = PM3::convertToStringd(180) + "deg";
							far_point.Z() = PM3::convertToStringd(zmax) + "m";
							near_point.X() = PM3::convertToStringd(xmin) + "m";
							near_point.Y() = PM3::convertToStringd(ymin) + "deg";
							near_point.Z() = PM3::convertToStringd(zmin) + "m";
							far_pointV.push_back(far_point);
							near_pointV.push_back(near_point);
							far_point.X() = PM3::convertToStringd(xmaxo) + "m";
							far_point.Y() = PM3::convertToStringd(180) + "deg";
							far_point.Z() = PM3::convertToStringd(zmaxo) + "m";
							near_point.X() = PM3::convertToStringd(xmino) + "m";
							near_point.Y() = PM3::convertToStringd(ymino) + "deg";
							near_point.Z() = PM3::convertToStringd(zmino) + "m";
							far_pointVo.push_back(far_point);
							near_pointVo.push_back(near_point);
						}
						else {
							PM3::DefValue3D far_point, near_point;
							far_point.X() = PM3::convertToStringd(xmax) + "m";
							far_point.Y() = PM3::convertToStringd(ymax) + "deg";
							far_point.Z() = PM3::convertToStringd(zmax) + "m";
							near_point.X() = PM3::convertToStringd(xmin) + "m";
							near_point.Y() = PM3::convertToStringd(270) + "deg";
							near_point.Z() = PM3::convertToStringd(zmin) + "m";
							far_pointV.push_back(far_point);
							near_pointV.push_back(near_point);
							far_point.X() = PM3::convertToStringd(xmaxo) + "m";
							far_point.Y() = PM3::convertToStringd(ymaxo) + "deg";
							far_point.Z() = PM3::convertToStringd(zmaxo) + "m";
							near_point.X() = PM3::convertToStringd(xmino) + "m";
							near_point.Y() = PM3::convertToStringd(270) + "deg";
							near_point.Z() = PM3::convertToStringd(zmino) + "m";
							far_pointVo.push_back(far_point);
							near_pointVo.push_back(near_point);
							far_point.X() = PM3::convertToStringd(xmax) + "m";
							far_point.Y() = PM3::convertToStringd(270) + "deg";
							far_point.Z() = PM3::convertToStringd(zmax) + "m";
							near_point.X() = PM3::convertToStringd(xmin) + "m";
							near_point.Y() = PM3::convertToStringd(180) + "deg";
							near_point.Z() = PM3::convertToStringd(zmin) + "m";
							far_pointV.push_back(far_point);
							near_pointV.push_back(near_point);
							far_point.X() = PM3::convertToStringd(xmaxo) + "m";
							far_point.Y() = PM3::convertToStringd(270) + "deg";
							far_point.Z() = PM3::convertToStringd(zmaxo) + "m";
							near_point.X() = PM3::convertToStringd(xmino) + "m";
							near_point.Y() = PM3::convertToStringd(180) + "deg";
							near_point.Z() = PM3::convertToStringd(zmino) + "m";
							far_pointVo.push_back(far_point);
							near_pointVo.push_back(near_point);
							far_point.X() = PM3::convertToStringd(xmax) + "m";
							far_point.Y() = PM3::convertToStringd(180) + "deg";
							far_point.Z() = PM3::convertToStringd(zmax) + "m";
							near_point.X() = PM3::convertToStringd(xmin) + "m";
							near_point.Y() = PM3::convertToStringd(90) + "deg";
							near_point.Z() = PM3::convertToStringd(zmin) + "m";
							far_pointV.push_back(far_point);
							near_pointV.push_back(near_point);
							far_point.X() = PM3::convertToStringd(xmaxo) + "m";
							far_point.Y() = PM3::convertToStringd(180) + "deg";
							far_point.Z() = PM3::convertToStringd(zmaxo) + "m";
							near_point.X() = PM3::convertToStringd(xmino) + "m";
							near_point.Y() = PM3::convertToStringd(90) + "deg";
							near_point.Z() = PM3::convertToStringd(zmino) + "m";
							far_pointVo.push_back(far_point);
							near_pointVo.push_back(near_point);
							/*if (ymin < 0) {
							far_point.X() = PM3::convertToStringd(xmax) + "m";
							far_point.Y() = PM3::convertToStringd(90) + "deg";
							far_point.Z() = PM3::convertToStringd(zmax) + "m";
							near_point.X() = PM3::convertToStringd(xmin) + "m";
							near_point.Y() = PM3::convertToStringd(0) + "deg";
							near_point.Z() = PM3::convertToStringd(zmin) + "m";
							far_pointV.push_back(far_point);
							near_pointV.push_back(near_point);
							far_point.X() = PM3::convertToStringd(xmax) + "m";
							far_point.Y() = PM3::convertToStringd(0) + "deg";
							far_point.Z() = PM3::convertToStringd(zmax) + "m";
							near_point.X() = PM3::convertToStringd(xmin) + "m";
							near_point.Y() = PM3::convertToStringd(ymin) + "deg";
							near_point.Z() = PM3::convertToStringd(zmin) + "m";
							far_pointV.push_back(far_point);
							near_pointV.push_back(near_point);
							}
							else */
							{
								far_point.X() = PM3::convertToStringd(xmax) + "m";
								far_point.Y() = PM3::convertToStringd(90) + "deg";
								far_point.Z() = PM3::convertToStringd(zmax) + "m";
								near_point.X() = PM3::convertToStringd(xmin) + "m";
								near_point.Y() = PM3::convertToStringd(ymin) + "deg";
								near_point.Z() = PM3::convertToStringd(zmin) + "m";
								far_pointV.push_back(far_point);
								near_pointV.push_back(near_point);
								far_point.X() = PM3::convertToStringd(xmaxo) + "m";
								far_point.Y() = PM3::convertToStringd(90) + "deg";
								far_point.Z() = PM3::convertToStringd(zmaxo) + "m";
								near_point.X() = PM3::convertToStringd(xmino) + "m";
								near_point.Y() = PM3::convertToStringd(ymino) + "deg";
								near_point.Z() = PM3::convertToStringd(zmino) + "m";
								far_pointVo.push_back(far_point);
								near_pointVo.push_back(near_point);
							}
						}

					}
					else if (ymax > 180) {
						if (ymin > 180) {
							PM3::DefValue3D far_point, near_point;
							far_point.X() = PM3::convertToStringd(xmax) + "m";
							far_point.Y() = PM3::convertToStringd(ymax) + "deg";
							far_point.Z() = PM3::convertToStringd(zmax) + "m";
							near_point.X() = PM3::convertToStringd(xmin) + "m";
							near_point.Y() = PM3::convertToStringd(ymin) + "deg";
							near_point.Z() = PM3::convertToStringd(zmin) + "m";
							far_pointV.push_back(far_point);
							near_pointV.push_back(near_point);
							far_point.X() = PM3::convertToStringd(xmaxo) + "m";
							far_point.Y() = PM3::convertToStringd(ymaxo) + "deg";
							far_point.Z() = PM3::convertToStringd(zmaxo) + "m";
							near_point.X() = PM3::convertToStringd(xmino) + "m";
							near_point.Y() = PM3::convertToStringd(ymino) + "deg";
							near_point.Z() = PM3::convertToStringd(zmino) + "m";
							far_pointVo.push_back(far_point);
							near_pointVo.push_back(near_point);
						}
						else if (ymin > 90) {
							PM3::DefValue3D far_point, near_point;
							far_point.X() = PM3::convertToStringd(xmax) + "m";
							far_point.Y() = PM3::convertToStringd(ymax) + "deg";
							far_point.Z() = PM3::convertToStringd(zmax) + "m";
							near_point.X() = PM3::convertToStringd(xmin) + "m";
							near_point.Y() = PM3::convertToStringd(180) + "deg";
							near_point.Z() = PM3::convertToStringd(zmin) + "m";
							far_pointV.push_back(far_point);
							near_pointV.push_back(near_point);
							far_point.X() = PM3::convertToStringd(xmaxo) + "m";
							far_point.Y() = PM3::convertToStringd(ymaxo) + "deg";
							far_point.Z() = PM3::convertToStringd(zmaxo) + "m";
							near_point.X() = PM3::convertToStringd(xmino) + "m";
							near_point.Y() = PM3::convertToStringd(180) + "deg";
							near_point.Z() = PM3::convertToStringd(zmino) + "m";
							far_pointVo.push_back(far_point);
							near_pointVo.push_back(near_point);
							far_point.X() = PM3::convertToStringd(xmax) + "m";
							far_point.Y() = PM3::convertToStringd(180) + "deg";
							far_point.Z() = PM3::convertToStringd(zmax) + "m";
							near_point.X() = PM3::convertToStringd(xmin) + "m";
							near_point.Y() = PM3::convertToStringd(ymin) + "deg";
							near_point.Z() = PM3::convertToStringd(zmin) + "m";
							far_pointV.push_back(far_point);
							near_pointV.push_back(near_point);
							far_point.X() = PM3::convertToStringd(xmaxo) + "m";
							far_point.Y() = PM3::convertToStringd(180) + "deg";
							far_point.Z() = PM3::convertToStringd(zmaxo) + "m";
							near_point.X() = PM3::convertToStringd(xmino) + "m";
							near_point.Y() = PM3::convertToStringd(ymino) + "deg";
							near_point.Z() = PM3::convertToStringd(zmino) + "m";
							far_pointVo.push_back(far_point);
							near_pointVo.push_back(near_point);
						}
						else {
							PM3::DefValue3D far_point, near_point;
							far_point.X() = PM3::convertToStringd(xmax) + "m";
							far_point.Y() = PM3::convertToStringd(ymax) + "deg";
							far_point.Z() = PM3::convertToStringd(zmax) + "m";
							near_point.X() = PM3::convertToStringd(xmin) + "m";
							near_point.Y() = PM3::convertToStringd(180) + "deg";
							near_point.Z() = PM3::convertToStringd(zmin) + "m";
							far_pointV.push_back(far_point);
							near_pointV.push_back(near_point);
							far_point.X() = PM3::convertToStringd(xmaxo) + "m";
							far_point.Y() = PM3::convertToStringd(ymaxo) + "deg";
							far_point.Z() = PM3::convertToStringd(zmaxo) + "m";
							near_point.X() = PM3::convertToStringd(xmino) + "m";
							near_point.Y() = PM3::convertToStringd(180) + "deg";
							near_point.Z() = PM3::convertToStringd(zmino) + "m";
							far_pointVo.push_back(far_point);
							near_pointVo.push_back(near_point);
							far_point.X() = PM3::convertToStringd(xmax) + "m";
							far_point.Y() = PM3::convertToStringd(180) + "deg";
							far_point.Z() = PM3::convertToStringd(zmax) + "m";
							near_point.X() = PM3::convertToStringd(xmin) + "m";
							near_point.Y() = PM3::convertToStringd(90) + "deg";
							near_point.Z() = PM3::convertToStringd(zmin) + "m";
							far_pointV.push_back(far_point);
							near_pointV.push_back(near_point);
							far_point.X() = PM3::convertToStringd(xmaxo) + "m";
							far_point.Y() = PM3::convertToStringd(180) + "deg";
							far_point.Z() = PM3::convertToStringd(zmaxo) + "m";
							near_point.X() = PM3::convertToStringd(xmino) + "m";
							near_point.Y() = PM3::convertToStringd(90) + "deg";
							near_point.Z() = PM3::convertToStringd(zmino) + "m";
							far_pointVo.push_back(far_point);
							near_pointVo.push_back(near_point);
							/*if (ymin < 0) {
							far_point.X() = PM3::convertToStringd(xmax) + "m";
							far_point.Y() = PM3::convertToStringd(90) + "deg";
							far_point.Z() = PM3::convertToStringd(zmax) + "m";
							near_point.X() = PM3::convertToStringd(xmin) + "m";
							near_point.Y() = PM3::convertToStringd(0) + "deg";
							near_point.Z() = PM3::convertToStringd(zmin) + "m";
							far_pointV.push_back(far_point);
							near_pointV.push_back(near_point);
							far_point.X() = PM3::convertToStringd(xmax) + "m";
							far_point.Y() = PM3::convertToStringd(0) + "deg";
							far_point.Z() = PM3::convertToStringd(zmax) + "m";
							near_point.X() = PM3::convertToStringd(xmin) + "m";
							near_point.Y() = PM3::convertToStringd(ymin) + "deg";
							near_point.Z() = PM3::convertToStringd(zmin) + "m";
							far_pointV.push_back(far_point);
							near_pointV.push_back(near_point);
							}
							else*/ {
								far_point.X() = PM3::convertToStringd(xmax) + "m";
								far_point.Y() = PM3::convertToStringd(90) + "deg";
								far_point.Z() = PM3::convertToStringd(zmax) + "m";
								near_point.X() = PM3::convertToStringd(xmin) + "m";
								near_point.Y() = PM3::convertToStringd(ymin) + "deg";
								near_point.Z() = PM3::convertToStringd(zmin) + "m";
								far_pointV.push_back(far_point);
								near_pointV.push_back(near_point);
								far_point.X() = PM3::convertToStringd(xmaxo) + "m";
								far_point.Y() = PM3::convertToStringd(90) + "deg";
								far_point.Z() = PM3::convertToStringd(zmaxo) + "m";
								near_point.X() = PM3::convertToStringd(xmino) + "m";
								near_point.Y() = PM3::convertToStringd(ymino) + "deg";
								near_point.Z() = PM3::convertToStringd(zmino) + "m";
								far_pointVo.push_back(far_point);
								near_pointVo.push_back(near_point);
							}
						}
					}
					else if (ymax > 90) {
						if (ymin > 90) {
							PM3::DefValue3D far_point, near_point;
							far_point.X() = PM3::convertToStringd(xmax) + "m";
							far_point.Y() = PM3::convertToStringd(ymax) + "deg";
							far_point.Z() = PM3::convertToStringd(zmax) + "m";
							near_point.X() = PM3::convertToStringd(xmin) + "m";
							near_point.Y() = PM3::convertToStringd(ymin) + "deg";
							near_point.Z() = PM3::convertToStringd(zmin) + "m";
							far_pointV.push_back(far_point);
							near_pointV.push_back(near_point);
							far_point.X() = PM3::convertToStringd(xmaxo) + "m";
							far_point.Y() = PM3::convertToStringd(ymaxo) + "deg";
							far_point.Z() = PM3::convertToStringd(zmaxo) + "m";
							near_point.X() = PM3::convertToStringd(xmino) + "m";
							near_point.Y() = PM3::convertToStringd(ymino) + "deg";
							near_point.Z() = PM3::convertToStringd(zmino) + "m";
							far_pointVo.push_back(far_point);
							near_pointVo.push_back(near_point);
						}
						else {
							PM3::DefValue3D far_point, near_point;
							far_point.X() = PM3::convertToStringd(xmax) + "m";
							far_point.Y() = PM3::convertToStringd(ymax) + "deg";
							far_point.Z() = PM3::convertToStringd(zmax) + "m";
							near_point.X() = PM3::convertToStringd(xmin) + "m";
							near_point.Y() = PM3::convertToStringd(90) + "deg";
							near_point.Z() = PM3::convertToStringd(zmin) + "m";
							far_pointV.push_back(far_point);
							near_pointV.push_back(near_point);
							far_point.X() = PM3::convertToStringd(xmaxo) + "m";
							far_point.Y() = PM3::convertToStringd(ymaxo) + "deg";
							far_point.Z() = PM3::convertToStringd(zmaxo) + "m";
							near_point.X() = PM3::convertToStringd(xmino) + "m";
							near_point.Y() = PM3::convertToStringd(90) + "deg";
							near_point.Z() = PM3::convertToStringd(zmino) + "m";
							far_pointVo.push_back(far_point);
							near_pointVo.push_back(near_point);
							far_point.X() = PM3::convertToStringd(xmax) + "m";
							far_point.Y() = PM3::convertToStringd(90) + "deg";
							far_point.Z() = PM3::convertToStringd(zmax) + "m";
							near_point.X() = PM3::convertToStringd(xmin) + "m";
							near_point.Y() = PM3::convertToStringd(ymin) + "deg";
							near_point.Z() = PM3::convertToStringd(zmin) + "m";
							far_pointV.push_back(far_point);
							near_pointV.push_back(near_point);
							far_point.X() = PM3::convertToStringd(xmaxo) + "m";
							far_point.Y() = PM3::convertToStringd(90) + "deg";
							far_point.Z() = PM3::convertToStringd(zmaxo) + "m";
							near_point.X() = PM3::convertToStringd(xmino) + "m";
							near_point.Y() = PM3::convertToStringd(ymino) + "deg";
							near_point.Z() = PM3::convertToStringd(zmino) + "m";
							far_pointVo.push_back(far_point);
							near_pointVo.push_back(near_point);

						}
					}
					else {//>0
						PM3::DefValue3D far_point, near_point;
						far_point.X() = PM3::convertToStringd(xmax) + "m";
						far_point.Y() = PM3::convertToStringd(ymax) + "deg";
						far_point.Z() = PM3::convertToStringd(zmax) + "m";
						near_point.X() = PM3::convertToStringd(xmin) + "m";
						near_point.Y() = PM3::convertToStringd(ymin) + "deg";
						near_point.Z() = PM3::convertToStringd(zmin) + "m";
						far_pointV.push_back(far_point);
						near_pointV.push_back(near_point);
						far_point.X() = PM3::convertToStringd(xmaxo) + "m";
						far_point.Y() = PM3::convertToStringd(ymaxo) + "deg";
						far_point.Z() = PM3::convertToStringd(zmaxo) + "m";
						near_point.X() = PM3::convertToStringd(xmino) + "m";
						near_point.Y() = PM3::convertToStringd(ymino) + "deg";
						near_point.Z() = PM3::convertToStringd(zmino) + "m";
						far_pointVo.push_back(far_point);
						near_pointVo.push_back(near_point);
						/*if (ymin < 0) {
						far_point.X() = PM3::convertToStringd(xmax) + "m";
						far_point.Y() = PM3::convertToStringd(ymax) + "deg";
						far_point.Z() = PM3::convertToStringd(zmax) + "m";
						near_point.X() = PM3::convertToStringd(xmin) + "m";
						near_point.Y() = PM3::convertToStringd(0) + "deg";
						near_point.Z() = PM3::convertToStringd(zmin) + "m";
						far_pointV.push_back(far_point);
						near_pointV.push_back(near_point);
						far_point.X() = PM3::convertToStringd(xmax) + "m";
						far_point.Y() = PM3::convertToStringd(0) + "deg";
						far_point.Z() = PM3::convertToStringd(zmax) + "m";
						near_point.X() = PM3::convertToStringd(xmin) + "m";
						near_point.Y() = PM3::convertToStringd(ymin) + "deg";
						near_point.Z() = PM3::convertToStringd(zmin) + "m";
						far_pointV.push_back(far_point);
						near_pointV.push_back(near_point);
						}
						else {
						far_point.X() = PM3::convertToStringd(xmax) + "m";
						far_point.Y() = PM3::convertToStringd(ymax) + "deg";
						far_point.Z() = PM3::convertToStringd(zmax) + "m";
						near_point.X() = PM3::convertToStringd(xmin) + "m";
						near_point.Y() = PM3::convertToStringd(ymin) + "deg";
						near_point.Z() = PM3::convertToStringd(zmin) + "m";
						far_pointV.push_back(far_point);
						near_pointV.push_back(near_point);
						}*/
					}
				}
				/*else {
				vfunc.setSystem(PM3::SYSMYCC);
				vfunc.far_point.X() = PM3::convertToStringd(xmax) + "m";
				vfunc.far_point.Y() = PM3::convertToStringd(ymax) + "m";
				vfunc.far_point.Z() = PM3::convertToStringd(zmax) + "deg";
				vfunc.near_point.X() = PM3::convertToStringd(xmin) + "m";
				vfunc.near_point.Y() = PM3::convertToStringd(ymin) + "m";
				vfunc.near_point.Z() = PM3::convertToStringd(zmin) + "deg";
				}*/
				Part::TopoShape* topoShapeV[5] = { 0 };
				if (far_pointV.size() > 0)
				{
					clock_t t0, t1;
					t0 = clock();
					//	std::cout << "start" << double(t0) << std::endl;
#pragma omp parallel for
					for (int nn = 0; nn < far_pointV.size(); nn++) {
						char s[256];
						std::string tempstr;
						//存放点
						std::vector<Base::Vector3d> Points;
						//存放面
						std::vector<Data::ComplexGeoData::Facet> Facets;
						double maxf = -1;
						Mesh::MeshObject mesh;
						PM3::VFunctional vfunc;
						vfunc.yreso = yreso;
						vfunc.iso->type = type;
						vfunc.iso->nb_ligne = nb_ligne;
						vfunc.iso->nb_colon = nb_colon;
						vfunc.iso->nb_depth = nb_depth;

						yreso = (ymax - ymin) * 3.1415926 / (8) / 180;
						if (std::string(coor) == S_COOR_RECTANGULAR)
							vfunc.setSystem(PM3::SYSCARTESIAN);
						else
							vfunc.setSystem(PM3::SYSCYLINDRICAL);
						vfunc.f = func;
						_itoa(nn, s, 10);
						vfunc.name = s;
						vfunc.far_point = far_pointV[nn];// .setValue(PM3::convertToStringd(xmax) + "," + PM3::convertToStringd(ymax) + "," + PM3::convertToStringd(zmax));
						tempstr = far_pointV[nn][0] + " " + far_pointV[nn][1] + " " + far_pointV[nn][2] + "/n";
						Base::Console().Log(tempstr.c_str());
						vfunc.near_point = near_pointV[nn];// .setValue(PM3::convertToStringd(xmin) + "," + PM3::convertToStringd(ymin) + "," + PM3::convertToStringd(zmin));
						tempstr = near_pointV[nn][0] + " " + near_pointV[nn][1] + " " + near_pointV[nn][2] + "/n";
						Base::Console().Log(tempstr.c_str());
						PM3::ExpParser exparser;
						vfunc.pexparser = &exparser;

						vfunc.update_mesh_topology(Points, Facets, maxf);

						if (Facets.size() > 0)
						{
							mesh.setFacets(Facets, Points);
							std::string filename;
							if (TEST_OUTPUT == 1) {								
								filename = "d://mesh";
								_itoa(nn, s, 10);
								filename = filename + s;
								filename = filename + ".stl";
								mesh.save(filename.c_str());
								_itoa(Facets.size(), s, 10);
								Base::Console().Log(s);
								Base::Console().Log("facets\n");
								_itoa(Points.size(), s, 10);
								Base::Console().Log(s);
								Base::Console().Log("points\n");
							}
							//if (false) 
							{
								try {


									//TopoDS_Shell mkPoly;

									//LoadOBJ(str, mkPoly);
									//TopoDS_Shell resultShape;
									//					Part::TopoShape resultShape;
									//std::shared_ptr<TopoShape> resultShapePtr(new TopoShape());
									//testTime("t4 ", t0, t1);
									//					LoadOBJ2_2(resultShape, facePrecision, Points, Facets);
									//testTime("t5 ", t0, t1);
									//	if (!mkPoly.IsDone())
									//		Standard_Failure::Raise("Cannot create polygon because less than two vertices are given");
									//ZD
									//Py::Object result = Py::asObject(new Part::TopoShapePy(new Part::TopoShape(resultShape)));
									//					Py::Object result = Py::asObject(new Part::TopoShapePy(new Part::TopoShape(resultShape)));
									//testTime("t6 ", t0, t1);
									//					return result;
									//Mesh::MeshObject *mesh_copy = new Mesh::MeshObject(mesh->getKernel());
									float dev = 0.000001;
									unsigned long minFacets = 0;
									std::vector<Mesh::Segment> segments = mesh.getSegmentsFromType
										(Mesh::MeshObject::PLANE, dev, minFacets);
									std::list < Part::TopoShape*> faces;
									//std::vector<unsigned long> remove;
									std::vector<unsigned long> all;
									//std::vector<unsigned long> invalid;
									std::string str("Py::Object makeFuncMesh: ");
									if (TEST_OUTPUT == 1) {										
										_itoa(mesh.countFacets(), s, 10);
										str = str + s;
										str = str + "\n";
										Base::Console().Log(str.c_str());
									}
									for (std::vector<Mesh::Segment>::iterator it = segments.begin(); it != segments.end(); ++it) {
										const std::vector<unsigned long>& segm = it->getIndices();
										for (int i = 0; i < segm.size(); i++)
											all.push_back(segm[i]);
									}
									if (TEST_OUTPUT == 1) {
										str = ("Py::Object makeFuncMesh all: ");
										_itoa(all.size(), s, 10);
										str = str + s;
										str = str + "\n";
										Base::Console().Log(str.c_str());
									}
									int n = 0, sum = 0;
									for (std::vector<Mesh::Segment>::iterator it = segments.begin(); it != segments.end(); ++it) {
										const std::vector<unsigned long>& segm = it->getIndices();
										if (segm.size() > 0) {
											std::list<Part::TopoShape *> wires = wireFromSegment(&mesh, segm);
											if (wires.size() > 0) {
												Part::TopoShape *ext = 0;
												int max_length = 0;
												for (list<Part::TopoShape *>::iterator it = wires.begin(); it != wires.end(); ++it){
													Part::TopoShape *sh = *it;
													if (sh->getBoundBox().CalcDiagonalLength() > max_length) {
														max_length = sh->getBoundBox().CalcDiagonalLength();
														ext = *it;
													}
												}
												wires.remove(ext);
												for (list<Part::TopoShape *>::iterator it = wires.begin(); it != wires.end(); ++it){
													Part::TopoShape *sh = *it;
													TopoDS_Shape _sh = sh->getShape();
													_sh.Reverse();
												}
												wires.push_front(ext);
												Part::TopoShape* t = wireToFace(wires);
												_itoa(n, s, 10);
												str = "d://segm";
												str = str + s;
												str = str + ".stl";
												//t->write(str.c_str());
												if (t == 0) {
													Mesh::MeshObject* temp = mesh.meshFromSegment(segm);
													Part::TopoShape *shape = new Part::TopoShape();
													Points.clear(), Facets.clear();
													temp->getFaces(Points, Facets, 0, 0);
													shape->setFaces(Points, Facets);
													if (shape->getShape().ShapeType() != TopAbs_FACE)
														getFaces(shape, faces);
													else
														faces.push_back(shape);
													//temp->save("d://segm.stl");
													//for (int i = 0; i < segm.size(); i++)
													//	invalid.push_back(segm[i]);
													delete temp;
												}
												else {
													faces.push_back(t);
													//for (int i = 0; i < segm.size(); i++)
													//	remove.push_back(segm[i]);
												}
											}
										}
										n++;
									}
									//not in seg
									if (all.size() < mesh.countFacets()) {
										mesh.deleteFacets(all);
										if (TEST_OUTPUT == 1) {
											str = ("Py::Object makeFuncMesh not in seg: ");
											_itoa(mesh.countFacets(), s, 10);
											str = str + s;
											str = str + "\n";
											Base::Console().Log(str.c_str());
										}
										std::vector<std::vector<unsigned long> > vvec = mesh.getComponents();
										if (TEST_OUTPUT == 1) {
											_itoa(vvec.size(), s, 10);
											str = "mesh->getComponents(): ";
											str = str + s;
											str = str + "\n";
											Base::Console().Log(str.c_str());
										}
										for (int i = 0; i < vvec.size(); i++) {
											Part::TopoShape *shape = new Part::TopoShape();
											Mesh::MeshObject* temp = mesh.meshFromSegment(vvec[i]);
											if (TEST_OUTPUT == 1) {
												_itoa(i, s, 10);
												str = "d://seg";
												str = str + s;
												str = str + ".stl";
												//temp->save(str.c_str());
											}
											Points.clear(), Facets.clear();
											temp->getFaces(Points, Facets, 0, 0);
											shape->setFaces(Points, Facets);
											if (shape->getShape().ShapeType() != TopAbs_FACE)
												getFaces(shape, faces);
											else
												faces.push_back(shape);
											delete temp;
										}

									}
									Part::TopoShape* shell = Shell(faces);
									if (TEST_OUTPUT == 1) {
										filename = "d://shell";
										_itoa(nn, s, 10);
										filename = filename + s;
										filename = filename + ".stl";
										shell->write(filename.c_str());
									}
									Part::TopoShape* funcShape = Solid(shell);
									if (TEST_OUTPUT == 1) {
										filename = "d://solid";
										_itoa(nn, s, 10);
										filename = filename + s;
										filename = filename + ".stl";
										funcShape->write(filename.c_str());
									}
									if (type == 1) {

										vcg::Point3d Start, End;
										std::string er;
										far_pointVo[nn].Parser(&exparser, End, er);
										near_pointVo[nn].Parser(&exparser, Start, er);
										Part::TopoShape* com = getShapeOfComformal(coor,
											Base::Vector3f(Start[0], Start[1], Start[2]),
											Vector3f(End[0], End[1], End[2]));
										if (TEST_OUTPUT == 1) {
											filename = "d://com";
											_itoa(nn, s, 10);
											filename = filename + s;
											filename = filename + ".stl";
											//com->write(filename.c_str());
										}
										BRepAlgoAPI_Common mkCommon(com->getShape(), funcShape->getShape());
										if (!mkCommon.IsDone()) {
											Base::Console().Log("makeFuncMesh - mkCommon not done\n");
											;// return new App::DocumentObjectExecReturn("DVD::execute - mkCommon not done");
										}
										if (mkCommon.Shape().IsNull()) {
											Base::Console().Log("makeFuncMesh - mkCommon.Shape is Null\n");
											;// return new App::DocumentObjectExecReturn("DVD::execute - mkCommon.Shape is Null");
										}

										funcShape->setShape(mkCommon.Shape());
										delete com;
										if (TEST_OUTPUT == 1) {
											filename = "d://common";
											_itoa(nn, s, 10);
											filename = filename + s;
											filename = filename + ".stl";
											funcShape->write(filename.c_str());
											Base::Console().Log("topoShapeV.push_back(funcShape)\n");
										}
										topoShapeV[nn] = funcShape;
									}
									else {
										topoShapeV[nn] = funcShape;
										//topoShapeV[nn] = Shell(faces);//Compound(faces);//
										//topoShapeV[nn] = makeFace(faces, "Part::FaceMakerBullseye"); //shell;
									}
									delete shell;
									for (std::list<Part::TopoShape *>::iterator it = faces.begin(); it != faces.end(); ++it)
										delete *it;
								}
								catch (Standard_Failure& e) {
									throw Py::Exception(Part::PartExceptionOCCError, e.GetMessageString());
								}
							}
						}
					}
					t1 = clock();
					std::cout << "#pragma: " << (t1 - t0) << std::endl;
				}

				try{
					Part::TopoShape* funcShape = 0;
					{
						int k = 0;
						for (k = 0; k < 5; k++)
							if (topoShapeV[k] != 0) {
								funcShape = topoShapeV[k];
								break;
							}
						std::vector<TopoDS_Shape> tmpv;
						for (k = k + 1; k < 5; k++) {
							if (topoShapeV[k] == 0)
								continue;
							tmpv.push_back(topoShapeV[k]->getShape());
							/*funcShape->setShape(funcShape->fuse(topoShapeV[k]->getShape()));
							std::string filename = "d://fuse";
							char s[256];
							_itoa(k, s, 10);
							filename = filename + s;
							filename = filename + ".stl";
							//funcShape->write(filename.c_str());*/
						}
						if (funcShape != 0 && tmpv.size() > 0)
							funcShape->setShape(funcShape->fuse(tmpv));
					}
					if (funcShape != 0)
						return Py::asObject(new Part::TopoShapePy(funcShape));
					else
						return Py::asObject(new Part::TopoShapePy(new Part::TopoShape()));

					//3
					//return Py::asObject(new Mesh::MeshPy(mesh));
				}
				catch (Standard_Failure& e) {
					throw Py::Exception(Part::PartExceptionOCCError, e.GetMessageString());
				}
			}
			catch (Standard_DomainError) {
				throw Py::Exception(Part::PartExceptionOCCDomainError, "creation of funcmesh failed");
			}
		}
		//#将单个坐标点转化为直角坐标系下的点
		//def otherToRecOne(coordinateType, point) :
		Base::Vector3f otherToRecOne(std::string curCoordinateSys, Base::Vector3f point)
		{
			Base::Vector3f resultPoint = point;
			//if (curCoordinateSys == "Rectangular")

			//	#极坐标系下：
			//	#极坐标系下，R与直角坐标系的X相同；根据R与θ求得直角坐标系下的y；z与直角坐标系z相同
			if (curCoordinateSys == S_COOR_POLAR || curCoordinateSys == S_COOR_CYLINDICAL) {
				float radian = point.y;// *PM3::pi() / 180.0;
				float pointY = point.x*sin(radian);
				float pointX = point.x*cos(radian);
				resultPoint = Base::Vector3f(pointX, pointY, point.z);
				//	#圆柱坐标系下的转换
			}
			//	#转换完成
			return resultPoint;
		}
		Base::Vector3f otherToRecOneDegree(std::string curCoordinateSys, Base::Vector3f point)
		{
			Base::Vector3f resultPoint = point;
			//if (curCoordinateSys == "Rectangular")

			//	#极坐标系下：
			//	#极坐标系下，R与直角坐标系的X相同；根据R与θ求得直角坐标系下的y；z与直角坐标系z相同
			if (curCoordinateSys == S_COOR_POLAR || curCoordinateSys == S_COOR_CYLINDICAL) {
				float radian = point.y*M_PI / 180.0;
				float pointY = point.x*sin(radian);
				float pointX = point.x*cos(radian);
				resultPoint = Base::Vector3f(pointX, pointY, point.z);
				//	#圆柱坐标系下的转换
			}
			//	#转换完成
			return resultPoint;
		}
		Part::TopoShape* makeLine(Base::Vector3f tempP1, Base::Vector3f tempP2)
		{
			BRepBuilderAPI_MakeEdge makeEdge(gp_Pnt(tempP1.x, tempP1.y, tempP1.z),
				gp_Pnt(tempP2.x, tempP2.y, tempP2.z));
			TopoDS_Edge edge = makeEdge.Edge();
			return new Part::TopoShape(edge);
		}
		Part::TopoShape* makeCircle(double radius, Base::Vector3f pnt, Base::Vector3f vec, double angle1, double angle2)
		{
			try {
				gp_Pnt loc(0, 0, 0);
				gp_Dir dir(0, 0, 1);
				loc.SetCoord(pnt.x, pnt.y, pnt.z);
				dir.SetCoord(vec.x, vec.y, vec.z);

				gp_Ax1 axis(loc, dir);
				gp_Circ circle;
				circle.SetAxis(axis);
				circle.SetRadius(radius);

				Handle(Geom_Circle) hCircle = new Geom_Circle(circle);
				BRepBuilderAPI_MakeEdge aMakeEdge(hCircle, angle1, angle2);
				TopoDS_Edge edge = aMakeEdge.Edge();
				return new Part::TopoShape(edge);
			}
			catch (Standard_Failure) {
				throw Py::Exception(Part::PartExceptionOCCError, "creation of circle failed");
			}
		}
		Part::TopoShape* makeSphere(double radius, Base::Vector3f pnt = Base::Vector3f(0, 0, 0), Base::Vector3f vec = Base::Vector3f(0, 0, 1), double angle1 = -90, double angle2 = 90, double angle3 = 360)
		{
			try {
				gp_Pnt p(0, 0, 0);
				gp_Dir d(0, 0, 1);

				p.SetCoord(pnt.x, pnt.y, pnt.z);
				d.SetCoord(vec.x, vec.y, vec.z);

				BRepPrimAPI_MakeSphere mkSphere(gp_Ax2(p, d), radius, angle1, angle2, angle3);
				TopoDS_Shape shape = mkSphere.Shape();
				return new Part::TopoShape(shape);
			}
			catch (Standard_DomainError) {
				throw Py::Exception(Part::PartExceptionOCCDomainError, "creation of sphere failed");
			}
		}
		Part::TopoShape* makeFace(std::vector<Part::TopoShape*> list, char *className)
		{
			try {
				std::unique_ptr<Part::FaceMaker> fm = Part::FaceMaker::ConstructFromType(className);
				for (int i = 0; i < list.size(); i++) {
					fm->addShape(list[i]->getShape());
				}
				fm->Build();

				if (fm->Shape().IsNull())
					return new Part::TopoShape(fm->Shape());


				return new Part::TopoShape(fm->Shape());

			}
			catch (Standard_Failure& e) {
				throw Py::Exception(Part::PartExceptionOCCError, e.GetMessageString());
			}
			catch (Base::Exception &e){
				throw Py::Exception(Base::BaseExceptionFreeCADError, e.what());
			}
		}

		Part::TopoShape* makeFace(std::list<Part::TopoShape*> list, char *className)
		{
			try {
				std::unique_ptr<Part::FaceMaker> fm = Part::FaceMaker::ConstructFromType(className);
				for (auto it = list.begin(); it != list.end(); ++it)
				{
					fm->addShape((*it)->getShape());
				}
				fm->Build();

				if (fm->Shape().IsNull())
					return new Part::TopoShape(fm->Shape());


				return new Part::TopoShape(fm->Shape());

			}
			catch (Standard_Failure& e) {
				throw Py::Exception(Part::PartExceptionOCCError, e.GetMessageString());
			}
			catch (Base::Exception &e){
				throw Py::Exception(Base::BaseExceptionFreeCADError, e.what());
			}

		}
		Part::TopoShape* Wire(Part::TopoShape* linePath){
			BRepBuilderAPI_MakeWire mkWire;
			const TopoDS_Shape& sh = linePath->getShape();
			if (sh.ShapeType() == TopAbs_EDGE)
				mkWire.Add(TopoDS::Edge(sh));
			else if (sh.ShapeType() == TopAbs_WIRE)
				mkWire.Add(TopoDS::Wire(sh));
			return new Part::TopoShape(mkWire.Wire());
		}
		//# 已知两个极坐标点，求两个点形成的薄管形
		//def getPipeObj(polarPoint1, polarPoint2) :
		Part::TopoShape* getPipeObj(Base::Vector3f polarPoint1, Base::Vector3f polarPoint2)
		{
			Base::Vector3f tempP1 = otherToRecOne("Polar", polarPoint1);
			Base::Vector3f tempP2 = otherToRecOne("Polar", Base::Vector3f(polarPoint1.x, polarPoint1.y, polarPoint2.z));
			Part::TopoShape* resultShape = 0;
			float starAngle = polarPoint1.y;
			float endAngle = polarPoint2.y;
			Base::Vector3f dir = Base::Vector3f(0, 0, 2);
			//#这样设置可以生成面片
			if (starAngle == endAngle)
				endAngle = starAngle + 0.01;
			Part::TopoShape* line = makeLine(tempP1, tempP2);
			if (tempP1 == tempP2)
				resultShape = makeCircle(polarPoint1.x, Base::Vector3f(0, 0, tempP1.z), dir, starAngle, endAngle);
			else {
				Part::TopoShape* linePath = makeCircle((polarPoint1.x + polarPoint2.x) / 2, Base::Vector3f(0, 0, tempP1.z), dir, starAngle, endAngle);
				Part::TopoShape* path = Wire(linePath);
				resultShape = new Part::TopoShape(path->makePipe(line->getShape()));
			}
			return resultShape;
		}
		//		#极坐标系下两个点得到扇形
		//		def getArcObj(polarPoint1, polarPoint2) :
		Part::TopoShape* getArcObj(Base::Vector3f polarPoint1, Base::Vector3f polarPoint2)
		{
			Base::Vector3f tempP1 = otherToRecOne("Polar", polarPoint1);
			Base::Vector3f tempP2 = otherToRecOne("Polar", Base::Vector3f(polarPoint2.x, polarPoint1.y, polarPoint2.z));
			Part::TopoShape* resultShape = 0;
			double startAngle = polarPoint1.y;
			double endAngle = polarPoint2.y;
			Base::Vector3f dir = Base::Vector3f(0, 0, 2);
			//#这样设置可以生成面片
			if (startAngle == endAngle)
				endAngle = startAngle + 0.01;
			if (tempP1 == tempP2) {
				//# 排除polarPoint.x为0
				if (polarPoint2.x != 0.0)
					resultShape = makeCircle(fabs((polarPoint2.x)), Base::Vector3f(0, 0, tempP1.z), dir, startAngle, endAngle);
				else
					resultShape = makeSphere(0.0001, tempP1);
			}
			else {
				if (fabs(startAngle - endAngle) == 2 * M_PI){
					//wires = []
					std::vector<Part::TopoShape*> wires;
					if (polarPoint1.x != 0.0) {
						Part::TopoShape* arcLine1 = makeCircle(fabs(polarPoint1.x), Base::Vector3f(0, 0, tempP1.z), dir, polarPoint1.y, polarPoint2.y);
						wires.push_back(arcLine1);
					}
					if (polarPoint2.x != 0.0) {
						Part::TopoShape*arcLine2 = makeCircle(fabs(polarPoint2.x), Base::Vector3f(0, 0, tempP2.z), dir, polarPoint1.y, polarPoint2.y);
						wires.push_back(arcLine2);
					}
					resultShape = makeFace(wires, "Part::FaceMakerBullseye");
				}
				else {
					Part::TopoShape* line = makeLine(tempP1, tempP2);
					//#linePath = Part.makeCircle(math.fabs((polarPoint1.x + polarPoint2.x) / 2), FreeCAD.Vector(0, 0, tempP1.z), dir, startAngle, endAngle)
					Part::TopoShape* linePath = makeCircle(fabs(polarPoint2.x), Base::Vector3f(0, 0, tempP1.z), dir, startAngle, endAngle);
					Part::TopoShape* path = Wire(linePath);
					//	resultShape = path.makePipe(line)
					resultShape = new Part::TopoShape(path->makePipe(line->getShape()));
				}
			}

			return resultShape;
		}
		//#通过两个点得到一个conformal的shape(借鉴comformal体)
		//def getShapeOfComformal(curCoordinateSys, pointmin, pointmax) :
		Part::TopoShape* getShapeOfComformal(std::string curCoordinateSys, Base::Vector3f pointmin, Base::Vector3f pointmax)
		{
			Part::TopoShape* resultShape = 0;
			Base::Vector3f Point1 = pointmin;
			Base::Vector3f Point2 = pointmax;
			if (curCoordinateSys == "Rectangular") {
				double length = abs(Point1.x - Point2.x);
				double width = abs(Point1.y - Point2.y);
				double height = abs(Point1.z - Point2.z);
				Base::Vector3f dir = Base::Vector3f(0, 0, 1);
				try {
					gp_Pnt p(0, 0, 0);
					gp_Dir d(0, 0, 1);
					p.SetCoord(Point1.x, Point1.y, Point1.z);
					BRepPrimAPI_MakeBox mkBox(gp_Ax2(p, d), length, width, height);
					TopoDS_Shape ResultShape = mkBox.Shape();
					//return Py::asObject(new TopoShapeSolidPy(new TopoShape(ResultShape)));
					resultShape = new Part::TopoShape(ResultShape);// = Part.makeBox(length, width, height, Point1, dir);
				}
				catch (Standard_Failure& e){
					//DocumentTools.printErrorMessage("Redraw Conformal Failed!")
					//	return
					//	pass
					//	# Shape = Part.makeBox(length, width, height, Point1, dir)
					//	pass
					;
				}
			}
			else {//				   elif curCoordinateSys == 'Polar' or curCoordinateSys == 'Cylindrical':
				Base::Vector3f tempP1 = otherToRecOne(curCoordinateSys, Point1);
				Base::Vector3f tempP11 = otherToRecOne(curCoordinateSys, Point2);
				Base::Vector3f tempP2 = otherToRecOne(curCoordinateSys, Base::Vector3f(Point2.x, Point1.y, Point1.z));
				Base::Vector3f tempP3 = otherToRecOne(curCoordinateSys, Base::Vector3f(Point2.x, Point1.y, Point2.z));
				Base::Vector3f tempP4 = otherToRecOne(curCoordinateSys, Base::Vector3f(Point1.x, Point1.y, Point2.z));

				//	#只有一个点的情况
				if (tempP1 == tempP2 && tempP2 == tempP4) {
					//# Shape = Part.Vertex(FreeCAD.Vector(tempP1.x, tempP1.y, tempP1.z))
					//# Shape = Part.makeBox(0.001, 0.001, 0.001, tempP1)
					//# return
					//resultShape = makePoint(tempP1);
					resultShape = makeSphere(0.00001, tempP1);
				}
				//	#防止两个点重合出现错误的情况
				else if (tempP1 == tempP2)
				{
					//# tempP2 = tempP2.add(FreeCAD.Vector(0.001*math.cos(tempP2.y), 0.001*math.sin(tempP2.y), 0))				
					if (tempP3 == tempP4){
						resultShape = makeLine(tempP1, tempP3);
					}
					else
						resultShape = getPipeObj(Point1, Point2);
				}
				else if (tempP1 == tempP4)
					//# tempP4 = tempP4.add(FreeCAD.Vector(0, 0, 0.01))
					resultShape = getArcObj(Point1, Point2);

				else {
					//# line1 = Part.makeLine(tempP1, tempP2)
					Part::TopoShape* line2 = makeLine(tempP1, tempP4);
					Part::TopoShape* shapeCir = getArcObj(Base::Vector3f(Point1.x, Point1.y, Point2.z), Point2);
					Part::TopoShape* path = Wire(line2);
					//resultShape = path.makePipe(shapeCir);
					resultShape = new Part::TopoShape(path->makePipe(shapeCir->getShape()));
				}
			}
			if (resultShape != 0)
				return Solid(resultShape);
			else
				Base::Console().Log("getShapeOfComformal error!");
			return 0;
		}
		Part::TopoShape* Solid(Part::TopoShape* shell)
		{
			if (shell == 0)
				return 0;
			try {
				const TopoDS_Shape& shape = shell->getShape();
				//first, if we were given a compsolid, try making a solid out of it
				TopExp_Explorer CSExp(shape, TopAbs_COMPSOLID);
				TopoDS_CompSolid compsolid;
				int count = 0;
				for (; CSExp.More(); CSExp.Next()) {
					++count;
					compsolid = TopoDS::CompSolid(CSExp.Current());
					if (count > 1)
						break;
				}
				if (count == 0) {
					//no compsolids. Get shells...
					BRepBuilderAPI_MakeSolid mkSolid;
					TopExp_Explorer anExp(shape, TopAbs_SHELL);
					count = 0;
					for (; anExp.More(); anExp.Next()) {
						++count;
						mkSolid.Add(TopoDS::Shell(anExp.Current()));
					}

					if (count == 0)//no shells?
						Standard_Failure::Raise("No shells or compsolids found in shape");

					TopoDS_Solid solid = mkSolid.Solid();
					BRepLib::OrientClosedSolid(solid);
					return new Part::TopoShape(solid);
				}
				else if (count == 1) {
					BRepBuilderAPI_MakeSolid mkSolid(compsolid);
					TopoDS_Solid solid = mkSolid.Solid();
					return new Part::TopoShape(solid);
				}
				else if (count > 1) {
					Standard_Failure::Raise("Only one compsolid can be accepted. Provided shape has more than one compsolid.");
				}

			}
			catch (Standard_Failure err) {
				std::stringstream errmsg;
				errmsg << "Creation of solid failed: " << err.GetMessageString();
			}

			return 0;
		}
		Part::TopoShape* SolidCompound(Part::TopoShape* compound)
		{
			if (compound == 0)
				return 0;
			try {
				const TopoDS_Shape& shape = compound->getShape();
				//first, if we were given a compsolid, try making a solid out of it
				TopExp_Explorer CSExp(shape, TopAbs_COMPSOLID);
				TopoDS_CompSolid compsolid;
				int count = 0;
				for (; CSExp.More(); CSExp.Next()) {
					++count;
					compsolid = TopoDS::CompSolid(CSExp.Current());
					if (count > 1)
						break;
				}
				if (count == 0) {
					//no compsolids. Get shells...
					BRepBuilderAPI_MakeSolid mkSolid;
					TopExp_Explorer anExp(shape, TopAbs_SHELL);
					count = 0;
					for (; anExp.More(); anExp.Next()) {
						++count;
						mkSolid.Add(TopoDS::Shell(anExp.Current()));
					}

					if (count == 0)//no shells?
						Standard_Failure::Raise("No shells or compsolids found in shape");

					TopoDS_Solid solid = mkSolid.Solid();
					BRepLib::OrientClosedSolid(solid);
					return new Part::TopoShape(solid);
				}
				else if (count == 1) {
					BRepBuilderAPI_MakeSolid mkSolid(compsolid);
					TopoDS_Solid solid = mkSolid.Solid();
					return new Part::TopoShape(solid);
				}
				else { // if (count > 1)
					Standard_Failure::Raise("Only one compsolid can be accepted. Provided shape has more than one compsolid.");
					return 0; //prevents compiler warning
				}
			}
			catch (Standard_Failure err) {
				std::stringstream errmsg;
				errmsg << "Creation of solid failed: " << err.GetMessageString();
				Base::Console().Log(errmsg.str().c_str());
			}

			return 0;
		}
		void getFaces(Part::TopoShape *sh, std::list < Part::TopoShape*> &faces)
		{
			Py::List ret;
			TopTools_IndexedMapOfShape M;

			TopExp_Explorer Ex(sh->getShape(), TopAbs_FACE);
			while (Ex.More())
			{
				M.Add(Ex.Current());
				Ex.Next();
			}

			for (Standard_Integer k = 1; k <= M.Extent(); k++)
			{
				const TopoDS_Shape& shape = M(k);
				faces.push_back(new Part::TopoShape(shape));
			}
		}
		Part::TopoShape* Compound(std::list < Part::TopoShape*> list)
		{
			BRep_Builder builder;
			TopoDS_CompSolid Comp;
			builder.MakeCompSolid(Comp);

			try {
				for (std::list<Part::TopoShape *>::iterator it = list.begin(); it != list.end(); ++it) {
					{
						const TopoDS_Shape& sh = (*it)->getShape();
						if (!sh.IsNull())
							builder.Add(Comp, sh);
					}
				}
			}
			catch (Standard_Failure& e) {
				Base::Console().Error("Compound: sh.IsNull()!!!!!!!!!!!!!!!!!!!!!!!!!!");;
			}

			return new Part::TopoShape(Comp);
		}
		Part::TopoShape* Shell(std::list < Part::TopoShape*> list)
		{
			BRep_Builder builder;
			TopoDS_Shape shape;
			TopoDS_Shell shell;
			//BRepOffsetAPI_Sewing mkShell;
			builder.MakeShell(shell);

			try {
				for (std::list<Part::TopoShape *>::iterator it = list.begin(); it != list.end(); ++it) {
					{
						const TopoDS_Shape& sh = (*it)->getShape();
						if (!sh.IsNull())
							builder.Add(shell, sh);
						else Base::Console().Error("Shell sh.IsNull() For!!!!!!!!!!!!!!!!!!!!!!!!!!");
					}
				}

				shape = shell;
				BRepCheck_Analyzer check(shell, Standard_False);
				if (!check.IsValid()) {
					ShapeUpgrade_ShellSewing sewShell;
					shape = sewShell.ApplySewing(shell);
				}
			}
			catch (Standard_Failure& e) {
				Base::Console().Error("Shell sh.IsNull()!!!!!!!!!!!!!!!!!!!!!!!!!!");
			}

			return new Part::TopoShape(shape);
		}
		Part::TopoShape* Shell2(std::list < Part::TopoShape*> list){
			BRep_Builder builder;
			TopoDS_Shape shape;
			TopoDS_Shell shell;
			//BRepOffsetAPI_Sewing mkShell;
			builder.MakeShell(shell);

			try {
				for (std::list<Part::TopoShape *>::iterator it = list.begin(); it != list.end(); ++it) {
					Part::TopoShape *ptr = *it;
					const TopoDS_Shape& sh = ptr->getShape();

					if (!sh.IsNull()) {
						try {
							builder.Add(shell, TopoDS::Face(sh));
						}
						catch (TopoDS_UnCompatibleShapes &e1) {
							Base::Console().Error("ERR Part::TopoShape* Shell(std::list < Part::TopoShape*> list) TopoDS_UnCompatibleShapes1\n");
						}
						catch (TopoDS_FrozenShape &e2) {
							Base::Console().Error("ERR Part::TopoShape* Shell(std::list < Part::TopoShape*> list) TopoDS_FrozenShape1\n");
						}
						catch (Standard_Failure& e) {

							Base::Console().Error("ERR Part::TopoShape* Shell(std::list < Part::TopoShape*> list)1\n");
						}
					}
					else {
						Base::Console().Error("sh.IsNull()!!!!!!!!!!!!!!!!!!!!!!!!!!");
					}
				}

				shape = shell;
				BRepCheck_Analyzer check(shell);
				if (!check.IsValid()) {
					ShapeUpgrade_ShellSewing sewShell;
					shape = sewShell.ApplySewing(shell);
					return new Part::TopoShape(shape);
				}

				if (shape.IsNull())
					Base::Console().Error("ERR Part::TopoShape* Shell(std::list < Part::TopoShape*>: Shape is null2\n"); //Standard_Failure::Raise("Shape is null");

				if (shape.ShapeType() != TopAbs_SHELL)
					Base::Console().Error("ERR Part::TopoShape* Shell(std::list < Part::TopoShape*>: Shape is not a shell3\n"); //Standard_Failure::Raise("Shape is not a shell");
			}
			catch (Standard_Failure& e) {
				;
			}

			return 0;
		}
		Part::TopoShape* wireToFace(std::list<Part::TopoShape *> list) {
			{
				try {
					std::vector<TopoDS_Wire> wires;
					for (std::list<Part::TopoShape *>::iterator it = list.begin(); it != list.end(); ++it){
						//for (Py::List::iterator it = list.begin(); it != list.end(); ++it) {
						Part::TopoShape *sh = *it;
						{
							const TopoDS_Shape& _sh = sh->getShape();
							if (_sh.ShapeType() == TopAbs_WIRE)
								wires.push_back(TopoDS::Wire(_sh));
							else
								Base::Console().Error("ERR Part::TopoShape* wireToFace: shape is not a wire1\n");// Standard_Failure::Raise("shape is not a wire");
						}
					}

					if (!wires.empty()) {
						BRepBuilderAPI_MakeFace mkFace(wires.front(), Standard_False);
						if (!mkFace.IsDone()) {
							switch (mkFace.Error()) {
							case BRepBuilderAPI_NoFace:
								Base::Console().Error("Part::TopoShape* wireToFace: No face2\n");
								break;
							case BRepBuilderAPI_NotPlanar:
								Base::Console().Error("Part::TopoShape* wireToFace: Not planar3\n");// Standard_Failure::Raise("Not planar");
								break;
							case BRepBuilderAPI_CurveProjectionFailed:
								Base::Console().Error("Part::TopoShape* wireToFace: Curve projection failed4\n"); //Standard_Failure::Raise("Curve projection failed");
								break;
							case BRepBuilderAPI_ParametersOutOfRange:
								Base::Console().Error("Part::TopoShape* wireToFace: Parameters out of range5\n"); //Standard_Failure::Raise("Parameters out of range");
								break;
#if OCC_VERSION_HEX < 0x060500
							case BRepBuilderAPI_SurfaceNotC2:
								Standard_Failure::Raise("Surface not C2");
								break;
#endif
							default:
								Base::Console().Error("Part::TopoShape* wireToFace: Unknown failure6\n"); //Standard_Failure::Raise("Unknown failure");
								break;
							}
							return 0;
						}
						for (std::vector<TopoDS_Wire>::iterator it = wires.begin() + 1; it != wires.end(); ++it)
							mkFace.Add(*it);
						return new Part::TopoShape(mkFace.Face());
					}
					else {
						Base::Console().Error("Part::TopoShape* wireToFace: no wires in list7\n"); //Standard_Failure::Raise("no wires in list");
					}
				}
				catch (Standard_Failure& e) {

					;
				}
			}
			return 0;
		}
		std::list<Part::TopoShape *> wireFromSegment(Mesh::MeshObject* mesh, std::vector<unsigned long> list)
		{
			std::list<std::vector<Base::Vector3f> > bounds;
			MeshCore::MeshAlgorithm algo(mesh->getKernel());
			algo.GetFacetBorders(list, bounds);

			std::list<Part::TopoShape *> wires;
			std::list<std::vector<Base::Vector3f> >::iterator bt;

			for (bt = bounds.begin(); bt != bounds.end(); ++bt) {
				BRepBuilderAPI_MakePolygon mkPoly;
				for (std::vector<Base::Vector3f>::reverse_iterator it = bt->rbegin(); it != bt->rend(); ++it) {
					mkPoly.Add(gp_Pnt(it->x, it->y, it->z));
				}
				if (mkPoly.IsDone()) {
					//PyObject* wire = new Part::TopoShapeWirePy(new Part::TopoShape(mkPoly.Wire()));
					TopoDS_Wire wire = mkPoly.Wire();
					Part::TopoShape *sh = new Part::TopoShape(wire);
					sh->getBoundBox().CalcDiagonalLength();

					wires.push_back(new Part::TopoShape(wire));
				}
			}

			return wires;
		}
		Py::Object makeObjFileMesh(const Py::Tuple& args)
		{
			char* path;

			PyObject *pPnt = 0, *pDir = 0;
			if (!PyArg_ParseTuple(args.ptr(), "s",
				&path
				))
				throw Py::Exception();

			try {
				// ask for read permission
				Base::FileInfo fi(path);
				if (!fi.exists() || !fi.isFile())
					throw Base::FileException("File does not exist", path);
				if (!fi.isReadable())
					throw Base::FileException("No permission on the file", path);

				Base::ifstream str(fi, std::ios::in | std::ios::binary);


				TopoDS_Shell mkPoly;

				try {
					LoadOBJ(str, mkPoly);


					//	if (!mkPoly.IsDone())
					//		Standard_Failure::Raise("Cannot create polygon because less than two vertices are given");

					return Py::asObject(new Part::TopoShapePy(new Part::TopoShape(mkPoly)));
				}
				catch (Standard_Failure& e) {
					throw Py::Exception(Part::PartExceptionOCCError, e.GetMessageString());
				}
			}
			catch (Standard_DomainError) {
				throw Py::Exception(Part::PartExceptionOCCDomainError, "creation of objFileMesh failed");
			}
		}

		/*fubiao 创建一个点*/
		/*py::Object makePoint(const Py::Tuple& args)
		{
		PyObject *pPnt = 0;
		if (!PyArg_ParseTuple(args.ptr(), "O!",
		&(Base::VectorPy::Type), &pPnt))
		throw Py::Exception();

		try {
		gp_Pnt loc(0, 0, 0);
		if (pPnt) {
		Base::Vector3d pnt = static_cast<Base::VectorPy*>(pPnt)->value();
		loc.SetCoord(pnt.x, pnt.y, pnt.z);
		}
		gp_Pnt point;
		point.SetX(pnt.x);
		point.SetY(pnt.y);
		point.SetZ(pnt.z);

		TopoDS_Shape shape = point.Shape();
		return Py::asObject(new TopoShapeEdgePy(new TopoShape(shape)));
		}
		catch (Standard_Failure) {
		throw Py::Exception(PartExceptionOCCError, "creation of circle failed");
		}

		}*/
		/*fubiao创建一个挖空的圆柱*/
		Py::Object makeMyCirc(const Py::Tuple& args)
		{
			double radius, angle1 = 0.0, angle2 = 360;
			PyObject *pPnt = 0, *pDir = 0;
			if (!PyArg_ParseTuple(args.ptr(), "d|O!O!dd",
				&radius,
				&(Base::VectorPy::Type), &pPnt,
				&(Base::VectorPy::Type), &pDir,
				&angle1, &angle2))
				throw Py::Exception();

			try {
				gp_Pnt loc(0, 0, 0);
				gp_Dir dir(0, 0, 1);
				if (pPnt) {
					Base::Vector3d pnt = static_cast<Base::VectorPy*>(pPnt)->value();
					loc.SetCoord(pnt.x, pnt.y, pnt.z);
				}
				if (pDir) {
					Base::Vector3d vec = static_cast<Base::VectorPy*>(pDir)->value();
					dir.SetCoord(vec.x, vec.y, vec.z);
				}
				gp_Ax1 axis(loc, dir);
				gp_Circ circle;
				circle.SetAxis(axis);
				circle.SetRadius(radius);

				Handle(Geom_Circle) hCircle = new Geom_Circle(circle);
				BRepBuilderAPI_MakeEdge aMakeEdge(hCircle, angle1*(M_PI / 180), angle2*(M_PI / 180));
				TopoDS_Edge edge = aMakeEdge.Edge();
				return Py::asObject(new Part::TopoShapeEdgePy(new Part::TopoShape(edge)));
			}
			catch (Standard_Failure) {
				throw Py::Exception(Part::PartExceptionOCCError, "creation of circle failed");
			}
		}

		/*loads an obj File get topo_shape*/
		bool LoadOBJ2_2(Part::TopoShape &resultShape,
			const Standard_Real facePrecision, std::vector<Base::Vector3d> Points,
			std::vector<Data::ComplexGeoData::Facet> Facets){

			float fX, fY, fZ;
			int  i1 = 1, i2 = 1, i3 = 1, i4 = 1;
			std::string line;
			boost::cmatch what;
			try{

				//t4 = clock();
				//cerr << "read obj time:" << (double)(t4 - t3) << endl;
				//有效点的索引
				std::set<int> validPointIndex;


				//int* inValidPointIndex = new int[validPointIndex.size()+1];
				std::map<int, int> numsOfInvalidthisIndex;
				std::vector<Base::Vector3d> validPoints;
				//去除无效的点
				std::vector<Data::ComplexGeoData::Facet>::iterator itFace = Facets.begin();
				//clock_t  t7, t8;
				//t7 = clock();
				//遍历所有面的点，剩下的就是无效的点
				for (; itFace != Facets.end(); ++itFace){
					validPointIndex.insert(itFace->I1);
					validPointIndex.insert(itFace->I2);
					validPointIndex.insert(itFace->I3);

				}
				//t8 = clock();
				//cerr << "time1:" << (double)(t8 - t7) << endl;
				//删除多余的点的索引
				std::set<int>::iterator itValidP = validPointIndex.begin();
				//定义一个和点数一样的多数组，初始化为-1，值表示该索引之前无效点的个数
				int numOdInvalidPoints = { 0 };

				int indexPoint = 0;
				int inValidPoints = 0;
				//clock_t  t9, t10;
				//t9 = clock();
				for (; itValidP != validPointIndex.end();){
					//set是有序的,无效的
					if (*itValidP != indexPoint){
						inValidPoints++;
						//inValidPointIndex[indexPoint] = inValidPoints;
					}
					//有效的
					else{
						validPoints.push_back(*(Points.begin() + indexPoint));
						++itValidP;
					}
					//indexPoint处无效点的个数
					numsOfInvalidthisIndex[indexPoint] = inValidPoints;
					indexPoint++;
				}
				//t10 = clock();
				//cerr << "time2:" << (double)(t10 - t9) << endl;
				//size_t numofValid = validPointIndex.size();
				//size_t numofInValid = inValidPoints;
				//重新计算面，去掉无用的点
				std::vector<Data::ComplexGeoData::Facet> validFacets;
				itFace = Facets.begin();
				//clock_t  t11, t12;
				//t11 = clock();
				for (; itFace != Facets.end(); ++itFace){
					Data::ComplexGeoData::Facet face;
					face.I1 = itFace->I1 - numsOfInvalidthisIndex[itFace->I1];
					face.I2 = itFace->I2 - numsOfInvalidthisIndex[itFace->I2];
					face.I3 = itFace->I3 - numsOfInvalidthisIndex[itFace->I3];
					validFacets.push_back(face);
				}
				//t12 = clock();
				//cerr << "time3:" << (double)(t12 - t11) << endl;
				/*
				for (int i = 0; i < validPoints.size(); ++i){
				Base::Console().Error("%lf %lf %lf\n", validPoints[i].x, validPoints[i].y, validPoints[i].z);
				}
				Base::Console().Error("=============================================================\n");
				for (int i = 0; i < validFacets.size(); ++i){
				Base::Console().Error("%d %d %d\n", validFacets[i].I1, validFacets[i].I3, validFacets[i].I2);
				}*/
				//clock_t  t5, t6;
				//t5 = clock();
				std::shared_ptr<Part::TopoShape> shapePtr(new Part::TopoShape());
				shapePtr->setFaces(validPoints, validFacets, facePrecision);// facePrecision);
				//t6 = clock();
				//cerr << "makeface obj time:" << (double)(t6 - t5) << endl;
				//TopoShape *pShape=
				resultShape = *shapePtr;
			}
			catch (...){
				std::cerr << "makeFace Wrong\n" << std::endl;
			}
			//t2 = clock();
			//cerr << "load obj time:" << (double)(t2 - t1) << endl;

			return 1;
		}

		/*loads an obj File get topo_shape*/
		bool LoadOBJ2(std::istream &rstrIn, Part::TopoShape &resultShape, const Standard_Real facePrecision){
			//clock_t  t1, t2;
			//t1 = clock();
			boost::regex rx_p("^v\\s+([-+]?[0-9]*)\\.?([0-9]+([eE][-+]?[0-9]+)?)"
				"\\s+([-+]?[0-9]*)\\.?([0-9]+([eE][-+]?[0-9]+)?)"
				"\\s+([-+]?[0-9]*)\\.?([0-9]+([eE][-+]?[0-9]+)?)\\s*$");
			boost::regex rx_f3("^f\\s+([-+]?[0-9]+)/?[-+]?[0-9]*/?[-+]?[0-9]*"
				"\\s+([-+]?[0-9]+)/?[-+]?[0-9]*/?[-+]?[0-9]*"
				"\\s+([-+]?[0-9]+)/?[-+]?[0-9]*/?[-+]?[0-9]*\\s*$");
			if (!rstrIn || rstrIn.bad() == true)
				return false;

			std::streambuf* buf = rstrIn.rdbuf();
			if (!buf)
				return false;
			float fX, fY, fZ, maxf;
			int  i1 = 1, i2 = 1, i3 = 1, i4 = 1;
			std::string line;
			boost::cmatch what;
			int flag = 0;
			try{
				//存放点
				std::vector<Base::Vector3d> Points;
				//存放面
				std::vector<Data::ComplexGeoData::Facet> Facets;
				//clock_t  t3, t4;
				//t3 = clock();
				//这里默认点遍历完点然后再遍历面
				while (std::getline(rstrIn, line)) {

					if (boost::regex_match(line.c_str(), what, rx_p)) {
						fX = (float)std::atof(what[1].first);
						fY = (float)std::atof(what[4].first);
						fZ = (float)std::atof(what[7].first);
						Points.push_back(Base::Vector3d(fX, fY, fZ));
						if (flag == 0) {
							maxf = fX;
							flag = 1;
						}
						maxf = fmax(maxf, fmax(fZ, fmax(fX, fY)));
					}
					else if (boost::regex_match(line.c_str(), what, rx_f3)) {
						// 3-vertex face
						i1 = std::atoi(what[1].first);
						i1 = i1 > 0 ? i1 - 1 : i1 + static_cast<int>(Points.size());
						i2 = std::atoi(what[2].first);
						i2 = i2 > 0 ? i2 - 1 : i2 + static_cast<int>(Points.size());
						i3 = std::atoi(what[3].first);
						i3 = i3 > 0 ? i3 - 1 : i3 + static_cast<int>(Points.size());

						//防止点溢出
						if (i1 <= static_cast<int>(Points.size())
							&& i2 <= static_cast<int>(Points.size())
							&& i3 <= static_cast<int>(Points.size())){
							Data::ComplexGeoData::Facet face;
							face.I1 = i1;
							face.I2 = i2;
							face.I3 = i3;
							Facets.push_back(face);
						}
					}
				}
				//t4 = clock();
				//cerr << "read obj time:" << (double)(t4 - t3) << endl;
				//有效点的索引
				std::set<int> validPointIndex;


				//int* inValidPointIndex = new int[validPointIndex.size()+1];
				std::map<int, int> numsOfInvalidthisIndex;
				std::vector<Base::Vector3d> validPoints;
				//去除无效的点
				std::vector<Data::ComplexGeoData::Facet>::iterator itFace = Facets.begin();
				//clock_t  t7, t8;
				//t7 = clock();
				//遍历所有面的点，剩下的就是无效的点
				for (; itFace != Facets.end(); ++itFace){
					validPointIndex.insert(itFace->I1);
					validPointIndex.insert(itFace->I2);
					validPointIndex.insert(itFace->I3);

				}
				//t8 = clock();
				//cerr << "time1:" << (double)(t8 - t7) << endl;
				//删除多余的点的索引
				std::set<int>::iterator itValidP = validPointIndex.begin();
				//定义一个和点数一样的多数组，初始化为-1，值表示该索引之前无效点的个数
				int numOdInvalidPoints = { 0 };

				int indexPoint = 0;
				int inValidPoints = 0;
				//clock_t  t9, t10;
				//t9 = clock();
				for (; itValidP != validPointIndex.end();){
					//set是有序的,无效的
					if (*itValidP != indexPoint){
						inValidPoints++;
						//inValidPointIndex[indexPoint] = inValidPoints;
					}
					//有效的
					else{
						validPoints.push_back(*(Points.begin() + indexPoint));
						++itValidP;
					}
					//indexPoint处无效点的个数
					numsOfInvalidthisIndex[indexPoint] = inValidPoints;
					indexPoint++;
				}
				//t10 = clock();
				//cerr << "time2:" << (double)(t10 - t9) << endl;
				//size_t numofValid = validPointIndex.size();
				//size_t numofInValid = inValidPoints;
				//重新计算面，去掉无用的点
				std::vector<Data::ComplexGeoData::Facet> validFacets;
				itFace = Facets.begin();
				//clock_t  t11, t12;
				//t11 = clock();
				for (; itFace != Facets.end(); ++itFace){
					Data::ComplexGeoData::Facet face;
					face.I1 = itFace->I1 - numsOfInvalidthisIndex[itFace->I1];
					face.I2 = itFace->I2 - numsOfInvalidthisIndex[itFace->I2];
					face.I3 = itFace->I3 - numsOfInvalidthisIndex[itFace->I3];
					validFacets.push_back(face);
				}
				//t12 = clock();
				//cerr << "time3:" << (double)(t12 - t11) << endl;
				/*
				for (int i = 0; i < validPoints.size(); ++i){
				Base::Console().Error("%lf %lf %lf\n", validPoints[i].x, validPoints[i].y, validPoints[i].z);
				}
				Base::Console().Error("=============================================================\n");
				for (int i = 0; i < validFacets.size(); ++i){
				Base::Console().Error("%d %d %d\n", validFacets[i].I1, validFacets[i].I3, validFacets[i].I2);
				}*/
				//clock_t  t5, t6;
				//t5 = clock();
				std::shared_ptr<Part::TopoShape> shapePtr(new Part::TopoShape());

				shapePtr->setFaces(validPoints, validFacets, maxf / 100);// facePrecision);
				//t6 = clock();
				//cerr << "makeface obj time:" << (double)(t6 - t5) << endl;
				//TopoShape *pShape=
				resultShape = *shapePtr;
			}
			catch (...){
				std::cerr << "makeFace Wrong\n" << std::endl;
			}
			//t2 = clock();
			//cerr << "load obj time:" << (double)(t2 - t1) << endl;
			return 1;
		}

		bool LoadOBJ3(std::istream &rstrIn, TopoDS_Shell &resultShape, const Standard_Real facePrecision){
			//clock_t  t1, t2;
			//t1 = clock();
			boost::regex rx_p("^v\\s+([-+]?[0-9]*)\\.?([0-9]+([eE][-+]?[0-9]+)?)"
				"\\s+([-+]?[0-9]*)\\.?([0-9]+([eE][-+]?[0-9]+)?)"
				"\\s+([-+]?[0-9]*)\\.?([0-9]+([eE][-+]?[0-9]+)?)\\s*$");
			boost::regex rx_f3("^f\\s+([-+]?[0-9]+)/?[-+]?[0-9]*/?[-+]?[0-9]*"
				"\\s+([-+]?[0-9]+)/?[-+]?[0-9]*/?[-+]?[0-9]*"
				"\\s+([-+]?[0-9]+)/?[-+]?[0-9]*/?[-+]?[0-9]*\\s*$");
			if (!rstrIn || rstrIn.bad() == true)
				return false;

			std::streambuf* buf = rstrIn.rdbuf();
			if (!buf)
				return false;
			float fX, fY, fZ;
			int  i1 = 1, i2 = 1, i3 = 1, i4 = 1;
			std::string line;
			boost::cmatch what;

			try{
				//存放点
				std::vector<Base::Vector3d> Points;
				//存放面
				std::vector<Data::ComplexGeoData::Facet> Facets;
				//clock_t  t3, t4;
				//t3 = clock();
				//这里默认点遍历完点然后再遍历面
				while (std::getline(rstrIn, line)) {

					if (boost::regex_match(line.c_str(), what, rx_p)) {
						fX = (float)std::atof(what[1].first);
						fY = (float)std::atof(what[4].first);
						fZ = (float)std::atof(what[7].first);
						Points.push_back(Base::Vector3d(fX, fY, fZ));
					}
					else if (boost::regex_match(line.c_str(), what, rx_f3)) {
						// 3-vertex face
						i1 = std::atoi(what[1].first);
						i1 = i1 > 0 ? i1 - 1 : i1 + static_cast<int>(Points.size());
						i2 = std::atoi(what[2].first);
						i2 = i2 > 0 ? i2 - 1 : i2 + static_cast<int>(Points.size());
						i3 = std::atoi(what[3].first);
						i3 = i3 > 0 ? i3 - 1 : i3 + static_cast<int>(Points.size());

						//防止点溢出
						if (i1 <= static_cast<int>(Points.size())
							&& i2 <= static_cast<int>(Points.size())
							&& i3 <= static_cast<int>(Points.size())){
							Data::ComplexGeoData::Facet face;
							face.I1 = i1;
							face.I2 = i2;
							face.I3 = i3;
							Facets.push_back(face);
						}
					}
				}
				//t4 = clock();
				//cerr << "read obj time:" << (double)(t4 - t3) << endl;
				//有效点的索引
				std::set<int> validPointIndex;


				//int* inValidPointIndex = new int[validPointIndex.size()+1];
				std::map<int, int> numsOfInvalidthisIndex;
				std::vector<Base::Vector3d> validPoints;
				//去除无效的点
				std::vector<Data::ComplexGeoData::Facet>::iterator itFace = Facets.begin();
				//clock_t  t7, t8;
				//t7 = clock();
				//遍历所有面的点，剩下的就是无效的点
				for (; itFace != Facets.end(); ++itFace){
					validPointIndex.insert(itFace->I1);
					validPointIndex.insert(itFace->I2);
					validPointIndex.insert(itFace->I3);

				}
				//t8 = clock();
				//cerr << "time1:" << (double)(t8 - t7) << endl;
				//删除多余的点的索引
				std::set<int>::iterator itValidP = validPointIndex.begin();
				//定义一个和点数一样的多数组，初始化为-1，值表示该索引之前无效点的个数
				int numOdInvalidPoints = { 0 };

				int indexPoint = 0;
				int inValidPoints = 0;
				//clock_t  t9, t10;
				//t9 = clock();
				for (; itValidP != validPointIndex.end();){
					//set是有序的,无效的
					if (*itValidP != indexPoint){
						inValidPoints++;
						//inValidPointIndex[indexPoint] = inValidPoints;
					}
					//有效的
					else{
						validPoints.push_back(*(Points.begin() + indexPoint));
						++itValidP;
					}
					//indexPoint处无效点的个数
					numsOfInvalidthisIndex[indexPoint] = inValidPoints;
					indexPoint++;
				}
				//t10 = clock();
				//cerr << "time2:" << (double)(t10 - t9) << endl;
				//size_t numofValid = validPointIndex.size();
				//size_t numofInValid = inValidPoints;
				//重新计算面，去掉无用的点
				std::vector<Data::ComplexGeoData::Facet> validFacets;
				itFace = Facets.begin();
				//clock_t  t11, t12;
				//t11 = clock();
				for (; itFace != Facets.end(); ++itFace){
					Data::ComplexGeoData::Facet face;
					face.I1 = itFace->I1 - numsOfInvalidthisIndex[itFace->I1];
					face.I2 = itFace->I2 - numsOfInvalidthisIndex[itFace->I2];
					face.I3 = itFace->I3 - numsOfInvalidthisIndex[itFace->I3];
					validFacets.push_back(face);
				}
				//t12 = clock();
				//cerr << "time3:" << (double)(t12 - t11) << endl;
				/*
				for (int i = 0; i < validPoints.size(); ++i){
				Base::Console().Error("%lf %lf %lf\n", validPoints[i].x, validPoints[i].y, validPoints[i].z);
				}
				Base::Console().Error("=============================================================\n");
				for (int i = 0; i < validFacets.size(); ++i){
				Base::Console().Error("%d %d %d\n", validFacets[i].I1, validFacets[i].I3, validFacets[i].I2);
				}*/
				//clock_t  t5, t6;
				//t5 = clock();

				resultShape = getTopoShapeByPointsAndFaces(validPoints, validFacets);
				//t6 = clock();
				//cerr << "makeface obj time:" << (double)(t6 - t5) << endl;
				//TopoShape *pShape=
			}
			catch (...){
				std::cerr << "makeFace Wrong\n" << std::endl;
			}
			//t2 = clock();
			//cerr << "load obj time:" << (double)(t2 - t1) << endl;
		}

		TopoDS_Shell getTopoShapeByPointsAndFaces(std::vector<Base::Vector3d>points, std::vector<Data::ComplexGeoData::Facet>faces){
			Standard_Real x1, y1, z1;
			Standard_Real x2, y2, z2;
			Standard_Real x3, y3, z3;

			gp_XYZ p1, p2, p3;
			TopoDS_Vertex Vertex1, Vertex2, Vertex3;
			TopoDS_Face newFace;
			TopoDS_Wire newWire;
			std::vector<TopoDS_Face> faceShapes;
			TopoDS_Shell shell;
			BRep_Builder builder;
			builder.MakeShell(shell);

			for (std::vector<Data::ComplexGeoData::Facet>::const_iterator it = faces.begin(); it != faces.end(); ++it) {
				if (it->I1 >= points.size() || it->I2 >= points.size() || it->I3 >= points.size())
					continue;
				x1 = points[it->I1].x; y1 = points[it->I1].y; z1 = points[it->I1].z;
				x2 = points[it->I2].x; y2 = points[it->I2].y; z2 = points[it->I2].z;
				x3 = points[it->I3].x; y3 = points[it->I3].y; z3 = points[it->I3].z;

				p1.SetCoord(x1, y1, z1);
				p2.SetCoord(x2, y2, z2);
				p3.SetCoord(x3, y3, z3);

				if ((!(p1.IsEqual(p2, 0.0))) && (!(p1.IsEqual(p3, 0.0)))) {
					Vertex1 = BRepBuilderAPI_MakeVertex(p1);
					Vertex2 = BRepBuilderAPI_MakeVertex(p2);
					Vertex3 = BRepBuilderAPI_MakeVertex(p3);

					newWire = BRepBuilderAPI_MakePolygon(Vertex1, Vertex2, Vertex3, Standard_True);
					if (!newWire.IsNull()) {
						newFace = BRepBuilderAPI_MakeFace(newWire);
						if (!newFace.IsNull())
							builder.Add(shell, newFace);
						//faceShapes.push_back(newFace);
					}
				}
			}
			return shell;
		}
		/*将面list变为shell*/
		TopoDS_Shape turnFaceListToShell(std::vector<TopoDS_Face> &faceShapes)
		{
			BRep_Builder builder;
			TopoDS_Shape shape;
			TopoDS_Shell shell;
			//BRepOffsetAPI_Sewing mkShell;
			builder.MakeShell(shell);

			try {
				for (std::vector<TopoDS_Face>::iterator it = faceShapes.begin(); it != faceShapes.end(); ++it) {
					const TopoDS_Shape& sh = static_cast<TopoDS_Face>(*it);
					if (!sh.IsNull())
						builder.Add(shell, sh);
				}

				shape = shell;
				BRepCheck_Analyzer check(shell);
				if (!check.IsValid()) {
					ShapeUpgrade_ShellSewing sewShell;
					shape = sewShell.ApplySewing(shell);
				}
			}
			catch (Standard_Failure& e) {
				throw Py::Exception(Part::PartExceptionOCCError, e.GetMessageString());
			}

			return shape;
		}
		/** Loads an OBJ file. */
		void LoadOBJ(std::istream &rstrIn, TopoDS_Shell& shell)
		{

			boost::regex rx_p("^v\\s+([-+]?[0-9]*)\\.?([0-9]+([eE][-+]?[0-9]+)?)"
				"\\s+([-+]?[0-9]*)\\.?([0-9]+([eE][-+]?[0-9]+)?)"
				"\\s+([-+]?[0-9]*)\\.?([0-9]+([eE][-+]?[0-9]+)?)\\s*$");


			//	boost::regex rx_f3("^f\\s+([-+]?[0-9]+)/?[-+]?[0-9]*/?[-+]?[0-9]*"
			//		"\\s+([-+]?[0-9]+)/?[-+]?[0-9]*/?[-+]?[0-9]*"
			//		"\\s+([-+]?[0-9]+)/?[-+]?[0-9]*/?[-+]?[0-9]*\\s*$");
			//	boost::regex rx_fint("[1-9]\d*|0");
			boost::cmatch what;

			unsigned long segment = 0;
			std::vector<Base::Vector3f> meshPoints;
			std::vector<Base::Vector3f> meshFacetPoints;
			//std::vector<int>  meshFacets;

			std::string line;
			float fX, fY, fZ;
			int  i1 = 1, i2 = 1, i3 = 1, i4 = 1;


			if (!rstrIn || rstrIn.bad() == true)
				return;

			std::streambuf* buf = rstrIn.rdbuf();
			if (!buf)
				return;


			bool new_segment = true;
			std::string groupName;

			BRep_Builder builder;
			//TopoDS_Shape shape;
			//TopoDS_Shell shell;
			//BRepOffsetAPI_Sewing mkShell;
			builder.MakeShell(shell);

			while (std::getline(rstrIn, line)) {
				// when a group name comes don't make it lower case
				if (!line.empty() && line[0] != 'g') {
					for (std::string::iterator it = line.begin(); it != line.end(); ++it)
						*it = tolower(*it);
				}
				if (line[0] == 'v' && boost::regex_match(line.c_str(), what, rx_p)) {
					fX = (float)std::atof(what[1].first);
					fY = (float)std::atof(what[4].first);
					fZ = (float)std::atof(what[7].first);
					meshPoints.push_back(Base::Vector3f(fX, fY, fZ));
				}

				else if (line[0] == 'f') {
					BRepBuilderAPI_MakePolygon poly;

					int start = std::atoi(&line[1]);
					start = start > 0 ? start - 1 : start + static_cast<int>(meshPoints.size());
					auto p = &line[1];
					// n-vertex face
					while (*p != '\n' && *p != '\0')
					{
						i1 = std::atoi(p);
						i1 = i1 > 0 ? i1 - 1 : i1 + static_cast<int>(meshPoints.size());
						poly.Add(gp_Pnt(meshPoints[i1].x, meshPoints[i1].y, meshPoints[i1].z));
						while ((*p != '\n' && *p != '\0') && (*p != ' '))
						{
							++p;
						}
						while ((*p != '\n' && *p != '\0') && (*p == ' '))
						{
							++p;
						}
					}

					poly.Add(gp_Pnt(meshPoints[start].x, meshPoints[start].y, meshPoints[start].z));
					//poly.Build();

					std::unique_ptr<Part::FaceMaker> fm
						= Part::FaceMaker::ConstructFromType("Part::FaceMakerExtrusion");
					///加一个try catch 当ploy的所有点是同一个点的时候会有问题，避免
					try{
						TopoDS_Shape s = poly.Shape();
						fm->addShape(/*poly.Shape()*/s);
						//fm->Build();
						auto fshape = fm->Shape();
						builder.Add(shell, fshape);
					}
					catch (...){
						std::cerr << "error!" << std::endl;
					}

				}

			}

			//shape = shell;
			//	BRepCheck_Analyzer check(shell);
			//if (!check.IsValid()) {
			//		ShapeUpgrade_ShellSewing sewShell;
			//shape = sewShell.ApplySewing(shell);
			//	}


			return;
		}


		/*求面的法线*/
		Base::Vector3d calculateShapeNormal2(const TopoDS_Shape& sh)
		{

			if (sh.IsNull())
				throw Base::Exception("calculateShapeNormal: link points to a valid object, but its shape is null.");
			//find plane
			BRepLib_FindSurface planeFinder(sh, -1, true);
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
	};

	PyObject* initModule()
	{
		return (new Module)->module().ptr();
	}


} // namespace PartChipic
