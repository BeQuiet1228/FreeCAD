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
#ifndef _PreComp_
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

#include<App/DocumentPy.h>
//#include<Gui/Document.h>
//#include<Gui/Application.h>
#include<time.h>


#include "OCCError.h"
#include "TopoShape.h"
#include "TopoShapePy.h"
#include "TopoShapeEdgePy.h"
#include "TopoShapeWirePy.h"
#include "TopoShapeFacePy.h"
#include "TopoShapeCompoundPy.h"
#include "TopoShapeCompSolidPy.h"
#include "TopoShapeSolidPy.h"
#include "TopoShapeShellPy.h"
#include "TopoShapeVertexPy.h"
#include "GeometryPy.h"
#include "GeometryCurvePy.h"
#include "BSplineSurfacePy.h"
#include "FeaturePartBox.h"
#include "FeaturePartCut.h"

#include "FeaturePartFuse.h"

#include "FeaturePartImportStep.h"
#include "FeaturePartImportIges.h"
#include "FeaturePartImportBrep.h"
#include "ImportIges.h"
#include "ImportStep.h"
#include "edgecluster.h"
#include "FaceMaker.h"
#include "PartPyCXX.h"


#include <boost/regex.hpp>
#include <boost/algorithm/string.hpp>
#include <boost/lexical_cast.hpp>
#include <boost/format.hpp>
#include <algorithm>
#include <tchar.h>

#include <windows.h>
#include <string>
#include <cstring>

#ifdef FCUseFreeType
#  include "FT2FC.h"
#endif

extern const char* BRepBuilderAPI_FaceErrorText(BRepBuilderAPI_FaceError fe);

namespace Part {
	extern Py::Object shape2pyshape(const TopoDS_Shape &shape);
}

#ifndef M_PI
#define M_PI    3.14159265358979323846 /* pi */
#endif

#ifndef M_PI_2
#define M_PI_2  1.57079632679489661923 /* pi/2 */
#endif

DWORD start, stop;

namespace Part {
	struct EdgePoints {
		gp_Pnt v1, v2;
		std::list<TopoDS_Edge>::iterator it;
		TopoDS_Edge edge;
	};

	PartExport std::list<TopoDS_Edge> sort_Edges(double tol3d, std::list<TopoDS_Edge>& edges)
	{
		tol3d = tol3d * tol3d;
		std::list<EdgePoints>  edge_points;
		TopExp_Explorer xp;
		for (std::list<TopoDS_Edge>::iterator it = edges.begin(); it != edges.end(); ++it) {
			EdgePoints ep;
			xp.Init(*it, TopAbs_VERTEX);
			ep.v1 = BRep_Tool::Pnt(TopoDS::Vertex(xp.Current()));
			xp.Next();
			ep.v2 = BRep_Tool::Pnt(TopoDS::Vertex(xp.Current()));
			ep.it = it;
			ep.edge = *it;
			edge_points.push_back(ep);
		}

		if (edge_points.empty())
			return std::list<TopoDS_Edge>();

		std::list<TopoDS_Edge> sorted;
		gp_Pnt first, last;
		first = edge_points.front().v1;
		last = edge_points.front().v2;

		sorted.push_back(edge_points.front().edge);
		edges.erase(edge_points.front().it);
		edge_points.erase(edge_points.begin());

		while (!edge_points.empty()) {
			// search for adjacent edge
			std::list<EdgePoints>::iterator pEI;
			for (pEI = edge_points.begin(); pEI != edge_points.end(); ++pEI) {
				if (pEI->v1.SquareDistance(last) <= tol3d) {
					last = pEI->v2;
					sorted.push_back(pEI->edge);
					edges.erase(pEI->it);
					edge_points.erase(pEI);
					pEI = edge_points.begin();
					break;
				}
				else if (pEI->v2.SquareDistance(first) <= tol3d) {
					first = pEI->v1;
					sorted.push_front(pEI->edge);
					edges.erase(pEI->it);
					edge_points.erase(pEI);
					pEI = edge_points.begin();
					break;
				}
				else if (pEI->v2.SquareDistance(last) <= tol3d) {
					last = pEI->v1;
					Standard_Real first, last;
					const Handle(Geom_Curve) & curve = BRep_Tool::Curve(pEI->edge, first, last);
					first = curve->ReversedParameter(first);
					last = curve->ReversedParameter(last);
					TopoDS_Edge edgeReversed = BRepBuilderAPI_MakeEdge(curve->Reversed(), last, first);
					sorted.push_back(edgeReversed);
					edges.erase(pEI->it);
					edge_points.erase(pEI);
					pEI = edge_points.begin();
					break;
				}
				else if (pEI->v1.SquareDistance(first) <= tol3d) {
					first = pEI->v2;
					Standard_Real first, last;
					const Handle(Geom_Curve) & curve = BRep_Tool::Curve(pEI->edge, first, last);
					first = curve->ReversedParameter(first);
					last = curve->ReversedParameter(last);
					TopoDS_Edge edgeReversed = BRepBuilderAPI_MakeEdge(curve->Reversed(), last, first);
					sorted.push_front(edgeReversed);
					edges.erase(pEI->it);
					edge_points.erase(pEI);
					pEI = edge_points.begin();
					break;
				}
			}

			if ((pEI == edge_points.end()) || (last.SquareDistance(first) <= tol3d)) {
				// no adjacent edge found or polyline is closed
				return sorted;
			}
		}

		return sorted;
	}
}

namespace Part {
	class Module : public Py::ExtensionModule<Module>
	{
	public:
		Module() : Py::ExtensionModule<Module>("Part")
		{
			add_varargs_method("updateBoolean", &Module::updateBoolean,
				"updateBoolean() -- update the boolean of Document."
				);
			add_varargs_method("open", &Module::open,
				"open(string) -- Create a new document and load the file into the document."
				);
			add_varargs_method("insert", &Module::insert,
				"insert(string,string) -- Insert the file into the given document."
				);
			//add_varargs_method("customBoolean", &Module::customBoolean,
			//	"customBoolean([list]) -- Insert the file into the given document."
			//	);
			add_varargs_method("export", &Module::exporter,
				"export(list,string) -- Export a list of objects into a single file."
				);
			add_varargs_method("read", &Module::read,
				"read(string) -- Load the file and return the shape."
				);
			add_varargs_method("show", &Module::show,
				"show(shape,[string]) -- Add the shape to the active document or create one if no document exists."
				);
			add_varargs_method("makeCompound", &Module::makeCompound,
				"makeCompound(list) -- Create a compound out of a list of shapes."
				);
			add_varargs_method("makeShell", &Module::makeShell,
				"makeShell(list) -- Create a shell out of a list of faces."
				);
			add_varargs_method("makeFuncMesh", &Module::makeFuncMesh,
				"makeFuncMesh(func,xmin,xmax,ymin,ymax,zmim,zmax,tempFilePath) -- Create a function mesh."
				);
			add_varargs_method("makeObjFileMesh", &Module::makeObjFileMesh,
				"makeObjFileMesh(path) -- Create a obj mesh."
				);
			add_varargs_method("makeFace", &Module::makeFace,
				"makeFace(list_of_shapes_or_compound, maker_class_name) -- Create a face (faces) using facemaker class.\n"
				"maker_class_name is a string like 'Part::FaceMakerSimple'."
				);
			add_varargs_method("makeFilledFace", &Module::makeFilledFace,
				"makeFilledFace(list) -- Create a face out of a list of edges."
				);
			add_varargs_method("makeSolid", &Module::makeSolid,
				"makeSolid(shape): Create a solid out of shells of shape. If shape is a compsolid, the overall volume solid is created."
				);
			add_varargs_method("makePlane", &Module::makePlane,
				"makePlane(length,width,[pnt,dirZ,dirX]) -- Make a plane\n"
				"By default pnt=Vector(0,0,0) and dirZ=Vector(0,0,1), dirX is ignored in this case"
				);
			add_varargs_method("makeBox", &Module::makeBox,
				"makeBox(length,width,height,[pnt,dir]) -- Make a box located\n"
				"in pnt with the dimensions (length,width,height)\n"
				"By default pnt=Vector(0,0,0) and dir=Vector(0,0,1)"
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
			add_varargs_method("makeWedge", &Module::makeWedge,
				"makeWedge(xmin, ymin, zmin, z2min, x2min,\n"
				"xmax, ymax, zmax, z2max, x2max,[pnt,dir])\n"
				" -- Make a wedge located in pnt\n"
				"By default pnt=Vector(0,0,0) and dir=Vector(0,0,1)"
				);
			add_varargs_method("makeLine", &Module::makeLine,
				"makeLine(startpnt,endpnt) -- Make a line between two points\n"
				"\n"
				"Args:\n"
				"    startpnt (Vector or tuple): Vector or 3 element tuple \n"
				"        containing the x,y and z coordinates of the start point,\n"
				"        i.e. (x1,y1,z1).\n"
				"    endpnt (Vector or tuple): Vector or 3 element tuple \n"
				"        containing the x,y and z coordinates of the start point,\n"
				"        i.e. (x1,y1,z1).\n"
				"\n"
				"Returns:\n"
				"    Edge: Part.Edge object\n"
				);
			add_varargs_method("makePolygon", &Module::makePolygon,
				"makePolygon(pntslist) -- Make a polygon from a list of points\n"
				"\n"
				"Args:\n"
				"    pntslist (list(Vector)): list of Vectors representing the \n"
				"        points of the polygon.\n"
				"\n"
				"Returns:\n"
				"    Wire: Part.Wire object. If the last point in the list is \n"
				"        not the same as the first point, the Wire will not be \n"
				"        closed and cannot be used to create a face.\n"
				);
			add_varargs_method("makeCircle", &Module::makeCircle,
				"makeCircle(radius,[pnt,dir,angle1,angle2]) -- Make a circle with a given radius\n"
				"By default pnt=Vector(0,0,0), dir=Vector(0,0,1), angle1=0 and angle2=360"
				);
			add_varargs_method("makeSphere", &Module::makeSphere,
				"makeSphere(radius,[pnt, dir, angle1,angle2,angle3]) -- Make a sphere with a given radius\n"
				"By default pnt=Vector(0,0,0), dir=Vector(0,0,1), angle1=0, angle2=90 and angle3=360"
				);
			add_varargs_method("makeCylinder", &Module::makeCylinder,
				"makeCylinder(radius,height,[pnt,dir,angle]) -- Make a cylinder with a given radius and height\n"
				"By default pnt=Vector(0,0,0),dir=Vector(0,0,1) and angle=360"
				);
			add_varargs_method("makeCone", &Module::makeCone,
				"makeCone(radius1,radius2,height,[pnt,dir,angle]) -- Make a cone with given radii and height\n"
				"By default pnt=Vector(0,0,0), dir=Vector(0,0,1) and angle=360"
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
			add_varargs_method("makeTorus", &Module::makeTorus,
				"makeTorus(radius1,radius2,[pnt,dir,angle1,angle2,angle]) -- Make a torus with a given radii and angles\n"
				"By default pnt=Vector(0,0,0),dir=Vector(0,0,1),angle1=0,angle1=360 and angle=360"
				);
			add_varargs_method("makeHelix", &Module::makeHelix,
				"makeHelix(pitch,height,radius,[angle]) -- Make a helix with a given pitch, height and radius\n"
				"By default a cylindrical surface is used to create the helix. If the fourth parameter is set\n"
				"(the apex given in degree) a conical surface is used instead"
				);
			add_varargs_method("makeLongHelix", &Module::makeLongHelix,
				"makeLongHelix(pitch,height,radius,[angle],[hand]) -- Make a (multi-edge) helix with a given pitch, height and radius\n"
				"By default a cylindrical surface is used to create the helix. If the fourth parameter is set\n"
				"(the apex given in degree) a conical surface is used instead."
				);
			add_varargs_method("makeThread", &Module::makeThread,
				"makeThread(pitch,depth,height,radius) -- Make a thread with a given pitch, depth, height and radius"
				);
			add_varargs_method("makeRevolution", &Module::makeRevolution,
				"makeRevolution(Curve,[vmin,vmax,angle,pnt,dir,shapetype]) -- Make a revolved shape\n"
				"by rotating the curve or a portion of it around an axis given by (pnt,dir).\n"
				"By default vmin/vmax=bounds of the curve,angle=360,pnt=Vector(0,0,0) and\n"
				"dir=Vector(0,0,1) and shapetype=Part.Solid"
				);
			add_varargs_method("makeRuledSurface", &Module::makeRuledSurface,
				"makeRuledSurface(Edge|Wire,Edge|Wire) -- Make a ruled surface\n"
				"Create a ruled surface out of two edges or wires. If wires are used then"
				"these must have the same number of edges."
				);
			add_varargs_method("makeTube", &Module::makeTube,
				"makeTube(edge,radius,[continuity,max degree,max segments]) -- Create a tube.\n"
				"continuity is a string which must be 'C0','C1','C2','C3','CN','G1' or 'G1',"
				);
			add_varargs_method("makeSweepSurface", &Module::makeSweepSurface,
				"makeSweepSurface(edge(path),edge(profile),[float]) -- Create a profile along a path."
				);
			add_varargs_method("makeLoft", &Module::makeLoft,
				"makeLoft(list of wires,[solid=False,ruled=False,closed=False,maxDegree=5]) -- Create a loft shape."
				);
			add_varargs_method("makeWireString", &Module::makeWireString,
				"makeWireString(string,fontdir,fontfile,height,[track]) -- Make list of wires in the form of a string's characters."
				);
			add_varargs_method("makeSplitShape", &Module::makeSplitShape,
				"makeSplitShape(shape, list of shape pairs,[check Interior=True]) -> two lists of shapes.\n"
				"The following shape pairs are supported:\n"
				"* Wire, Face\n"
				"* Edge, Face\n"
				"* Compound, Face\n"
				"* Edge, Edge\n"
				"* The face must be part of the specified shape and the edge, wire or compound must\n"
				"lie on the face.\n"
				"Output:\n"
				"The first list contains the faces that are the left of the projected wires.\n"
				"The second list contains the left part on the shape.\n\n"
				"Example:\n"
				"face = ...\n"
				"edges = ...\n"
				"split = [(edges[0],face),(edges[1],face)]\n"
				"r = Part.makeSplitShape(face, split)\n"
				"Part.show(r[0][0])\n"
				"Part.show(r[1][0])\n"
				);
			add_varargs_method("exportUnits", &Module::exportUnits,
				"exportUnits([string=MM|M|IN]) -- Set units for exporting STEP/IGES files and returns the units."
				);
			add_varargs_method("setStaticValue", &Module::setStaticValue,
				"setStaticValue(string,string|int|float) -- Set a name to a value The value can be a string, int or float."
				);
			add_varargs_method("cast_to_shape", &Module::cast_to_shape,
				"cast_to_shape(shape) -- Cast to the actual shape type"
				);
			add_varargs_method("getSortedClusters", &Module::getSortedClusters,
				"getSortedClusters(list of edges) -- Helper method to sort and cluster a variety of edges"
				);
			add_varargs_method("__sortEdges__", &Module::sortEdges,
				"__sortEdges__(list of edges) -- Helper method to sort an unsorted list of edges so that afterwards\n"
				"two adjacent edges share a common vertex"
				);
			add_varargs_method("sortEdges", &Module::sortEdges2,
				"sortEdges(list of edges) -- Helper method to sort a list of edges into a list of list of connected edges"
				);
			add_varargs_method("__toPythonOCC__", &Module::toPythonOCC,
				"__toPythonOCC__(shape) -- Helper method to convert an internal shape to pythonocc shape"
				);
			add_varargs_method("__fromPythonOCC__", &Module::fromPythonOCC,
				"__fromPythonOCC__(occ) -- Helper method to convert a pythonocc shape to an internal shape"
				);
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
		void booleanSub(TopoDS_Shape &resultShape, TopoDS_Shape theFirstShap, TopoDS_Shape theSecondShape){

			if (theFirstShap.IsNull() || theSecondShape.IsNull()){
				std::cerr << "baseShape or toolShape is Null!" << std::endl;
			}
			BRepAlgoAPI_Cut mkCut(theFirstShap, theSecondShape);
			if (!mkCut.IsDone())
				std::cerr << "Cut out failed!" << std::endl;
			//return new App::DocumentObjectExecReturn("Cut out failed");
			TopoDS_Shape shap = mkCut.Shape();
			resultShape = shap;
		}
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
		void booleanAdd(TopoDS_Shape &resultShape, std::vector<TopoDS_Shape> shapeList){
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
		/*fubiao*/
		Py::Object updateBoolean(const Py::Tuple& args)
		{
			start = GetTickCount();
			if (!PyArg_ParseTuple(args.ptr(), ""))
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
						int orderOfObj = ((App::PropertyInteger*)(*objIt)->getPropertyByName("Order"))->getValue();
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
			std::vector<App::DocumentObject*> vacuoList;
			std::vector<App::DocumentObject*> conductorList;
			TopoDS_Shape resultShape;
			for (std::map<int, App::DocumentObject*>::const_iterator it = objsMap.begin(); it != objsMap.end(); ++it){
				//guiPcDoc->setHide(it->second->getNameInDocument());
				std::string attrOfObj = ((App::PropertyEnumeration*)(it->second->getPropertyByName("Attribute")))->getValueAsString();
				if ((strcmp(attrOfObj.c_str(), "Conductor") == 0) || (strcmp(attrOfObj.c_str(), "Custom") == 0)){
					if (vacuoList.size() == 0){

						TopoDS_Shape itShape = static_cast<Part::Feature*>(it->second)->Shape.getValue();
						booleanAddOne(resultShape, itShape);
						//conductorList.push_back(pcLastConductorObj);

					}
					else{
						//先将空对象联合
						std::vector<TopoDS_Shape> s;

						std::vector<App::DocumentObject*>::iterator itVacuo;
						for (itVacuo = vacuoList.begin(); itVacuo != vacuoList.end(); ++itVacuo) {
							if ((*itVacuo)->getTypeId().isDerivedFrom(Part::Feature::getClassTypeId())) {
								s.push_back(static_cast<Part::Feature*>(*itVacuo)->Shape.getValue());
							}
						}
						TopoDS_Shape tempResult;
						//所有真空相加
						booleanAdd(tempResult, s);
						//resultShape=resultShape-tempResult
						booleanSub(resultShape, resultShape, tempResult);
						//booleanAddOne(resultShape, tempResult);
						//再将这个导体与resultShape 相加
						TopoDS_Shape itShape = static_cast<Part::Feature*>(it->second)->Shape.getValue();
						booleanAddOne(resultShape, itShape);

					}
					vacuoList.clear();
				}
				else{
					//真空
					vacuoList.push_back(it->second);
					//隐藏
					//Gui::Document *guiPcDoc = Gui::Application::Instance->activeDocument();
				}
			}
			if (vacuoList.size() != 0){
				//先将空对象联合
				std::vector<TopoDS_Shape> s;

				std::vector<App::DocumentObject*>::iterator it;
				for (it = vacuoList.begin(); it != vacuoList.end(); ++it) {
					if ((*it)->getTypeId().isDerivedFrom(Part::Feature::getClassTypeId())) {
						s.push_back(static_cast<Part::Feature*>(*it)->Shape.getValue());
					}
				}
				TopoDS_Shape tempResult;
				//所有真空相加
				booleanAdd(tempResult, s);
				//resultShape=resultShape-tempResult
				booleanSub(resultShape, resultShape, tempResult);
			}
			//将最终的形状赋给模型
			static_cast<Part::Feature*>(resultObj)->Shape.setValue(resultShape);

			stop = GetTickCount();
			cerr << "tunning time:" << (stop - start)*1.0 / 1000 << endl;
			//pcDoc->updateBoolean();
			return Py::None();
		}
		Py::Object open(const Py::Tuple& args)
		{
			char* Name;
			if (!PyArg_ParseTuple(args.ptr(), "et", "utf-8", &Name))
				throw Py::Exception();
			std::string EncodedName = std::string(Name);
			PyMem_Free(Name);

			//Base::Console().Log("Open in Part with %s",Name);
			Base::FileInfo file(EncodedName.c_str());

			// extract ending
			if (file.extension().empty())
				throw Py::RuntimeError("No file extension");

			if (file.hasExtension("stp") || file.hasExtension("step")) {
				// create new document and add Import feature
				App::Document *pcDoc = App::GetApplication().newDocument("Unnamed");
#if 1
				ImportStepParts(pcDoc, EncodedName.c_str());
#else
				Part::ImportStep *pcFeature = (Part::ImportStep *)pcDoc->addObject("Part::ImportStep", file.fileNamePure().c_str());
				pcFeature->FileName.setValue(Name);
#endif 
				pcDoc->recompute();
			}
#if 1
			else if (file.hasExtension("igs") || file.hasExtension("iges")) {
				App::Document *pcDoc = App::GetApplication().newDocument("Unnamed");
				ImportIgesParts(pcDoc, EncodedName.c_str());
				pcDoc->recompute();
			}
#endif
			else {
				TopoShape shape;
				shape.read(EncodedName.c_str());

				// create new document set loaded shape
				App::Document *pcDoc = App::GetApplication().newDocument(file.fileNamePure().c_str());
				Part::Feature *object = static_cast<Part::Feature *>(pcDoc->addObject
					("Part::Feature", file.fileNamePure().c_str()));
				object->Shape.setValue(shape);
				pcDoc->recompute();
			}

			return Py::None();
		}
		Py::Object insert(const Py::Tuple& args)
		{
			char* Name;
			const char* DocName;
			if (!PyArg_ParseTuple(args.ptr(), "ets", "utf-8", &Name, &DocName))
				throw Py::Exception();

			std::string EncodedName = std::string(Name);
			PyMem_Free(Name);

			//Base::Console().Log("Insert in Part with %s",Name);
			Base::FileInfo file(EncodedName.c_str());

			// extract ending
			if (file.extension().empty())
				throw Py::RuntimeError("No file extension");

			App::Document *pcDoc = App::GetApplication().getDocument(DocName);
			if (!pcDoc) {
				pcDoc = App::GetApplication().newDocument(DocName);
			}

			if (file.hasExtension("stp") || file.hasExtension("step")) {
#if 1
				ImportStepParts(pcDoc, EncodedName.c_str());
#else
				// add Import feature
				Part::ImportStep *pcFeature = (Part::ImportStep *)pcDoc->addObject("Part::ImportStep", file.fileNamePure().c_str());
				pcFeature->FileName.setValue(Name);
#endif 
				pcDoc->recompute();
			}
#if 1
			else if (file.hasExtension("igs") || file.hasExtension("iges")) {
				ImportIgesParts(pcDoc, EncodedName.c_str());
				pcDoc->recompute();
			}
#endif
			else {
				TopoShape shape;
				shape.read(EncodedName.c_str());

				Part::Feature *object = static_cast<Part::Feature *>(pcDoc->addObject
					("Part::Feature", file.fileNamePure().c_str()));
				object->Shape.setValue(shape);
				pcDoc->recompute();
			}

			return Py::None();
		}
		//////自定义Boolean
		//Py::Object customBoolean(const Py::Tuple& args)
		//{
		//	PyObject *pcObjsPy;
		//	PyObject *toolShapePy;
		//	PyObject *resultObjPy;
		//	if (!PyArg_ParseTuple(args.ptr(), "OOO", &pcObjsPy, &toolShapePy, &resultObjPy))
		//		throw Py::Exception();
		//	const TopoDS_Shape& toolShape = static_cast<Part::TopoShapePy*>(toolShapePy)->getTopoShapePtr()->getShape();

		//	App::DocumentObject* resultObj = static_cast<App::DocumentObjectPy*>(resultObjPy)->getDocumentObjectPtr();
		//	try{
		//		Py::Sequence list(pcObjsPy);
		//		std::vector<Base::Vector3d> Points;
		//		std::vector<Data::ComplexGeoData::Facet> Facets;
		//		TopoDS_Shape itShape;
		//		std::vector<TopoDS_Shape> finalShapes;
		//		std::vector<App::DocumentObject*> finalObjs;
		//		for (Py::Sequence::iterator it = list.begin(); it != list.end(); ++it) {
		//			PyObject* item = (*it).ptr();
		//			if (PyObject_TypeCheck(item, &(App::DocumentObjectPy::Type))) {
		//				App::DocumentObject* obj = static_cast<App::DocumentObjectPy*>(item)->getDocumentObjectPtr();
		//				{
		//					itShape = static_cast<Part::Feature*>(obj)->Shape.getValue();

		//					TopoDS_Shape finalShape;
		//					//测试
		//					clock_t t1, t2;
		//					if (!toolShape.IsNull())
		//					{
		//						t1 = clock();
		//						std::cout << "t1:" << t1 << std::endl;
		//						finalShape = Part::TopoShape(itShape).cut(toolShape);
		//						t2 = clock();
		//						std::cout << "t2:" << t1 << std::endl;
		//						std::cout << "this cut: " << (t2 - t1) << std::endl;
		//					}
		//					else{
		//						finalShape = itShape;
		//					}

		//					finalShapes.push_back(finalShape);
		//					finalObjs.push_back(obj);
		//					//加入颜色
		//					Part::Feature* objBase = dynamic_cast<Part::Feature*>(obj);
		//					Gui::ViewProvider* vpBase = Gui::Application::Instance->getViewProvider(objBase);
		//					std::vector<App::Color> baseCol = static_cast<PartGui::ViewProviderPart*>(vpBase)->DiffuseColor.getValues();
		//					//因为每一个所有的形状只能是一种颜色
		//					if (baseCol.size() != 0)
		//						ColorOfCon.push_back(baseCol[0]);
		//					else
		//						//默认
		//						ColorOfCon.push_back(App::Color(0.80, 0.80, 0.80, 0.5));
		//				}


		//			}
		//		}
		//	}
		//	catch (...)
		//	{
		//	}
		//}
		Py::Object exporter(const Py::Tuple& args)
		{
			PyObject* object;
			char* Name;
			if (!PyArg_ParseTuple(args.ptr(), "Oet", &object, "utf-8", &Name))
				throw Py::Exception();

			std::string EncodedName = std::string(Name);
			PyMem_Free(Name);

			BRep_Builder builder;
			TopoDS_Compound comp;
			builder.MakeCompound(comp);

			Py::Sequence list(object);
			for (Py::Sequence::iterator it = list.begin(); it != list.end(); ++it) {
				PyObject* item = (*it).ptr();
				if (PyObject_TypeCheck(item, &(App::DocumentObjectPy::Type))) {
					App::DocumentObject* obj = static_cast<App::DocumentObjectPy*>(item)->getDocumentObjectPtr();
					if (obj->getTypeId().isDerivedFrom(Part::Feature::getClassTypeId())) {
						Part::Feature* part = static_cast<Part::Feature*>(obj);
						const TopoDS_Shape& shape = part->Shape.getValue();
						if (!shape.IsNull())
							builder.Add(comp, shape);
					}
					else {
						Base::Console().Message("'%s' is not a shape, export will be ignored.\n", obj->Label.getValue());
					}
				}
			}

			TopoShape shape(comp);
			shape.write(EncodedName.c_str());

			return Py::None();
		}
		Py::Object read(const Py::Tuple& args)
		{
			char* Name;
			if (!PyArg_ParseTuple(args.ptr(), "et", "utf-8", &Name))
				throw Py::Exception();

			std::string EncodedName = std::string(Name);
			PyMem_Free(Name);

			TopoShape* shape = new TopoShape();
			shape->read(EncodedName.c_str());
			return Py::asObject(new TopoShapePy(shape));
		}
		Py::Object show(const Py::Tuple& args)
		{
			PyObject *pcObj = 0;
			char *name = "Shape";
			if (!PyArg_ParseTuple(args.ptr(), "O!|s", &(TopoShapePy::Type), &pcObj, &name))
				throw Py::Exception();

			App::Document *pcDoc = App::GetApplication().getActiveDocument();
			if (!pcDoc)
				pcDoc = App::GetApplication().newDocument();
			TopoShapePy* pShape = static_cast<TopoShapePy*>(pcObj);
			Part::Feature *pcFeature = static_cast<Part::Feature*>(pcDoc->addObject("Part::Feature", name));
			// copy the data
			pcFeature->Shape.setValue(pShape->getTopoShapePtr()->getShape());
			pcDoc->recompute();

			return Py::None();
		}
		Py::Object makeCompound(const Py::Tuple& args)
		{
			PyObject *pcObj;
			if (!PyArg_ParseTuple(args.ptr(), "O", &pcObj))
				throw Py::Exception();

			BRep_Builder builder;
			TopoDS_Compound Comp;
			builder.MakeCompound(Comp);

			try {
				Py::Sequence list(pcObj);
				for (Py::Sequence::iterator it = list.begin(); it != list.end(); ++it) {
					if (PyObject_TypeCheck((*it).ptr(), &(Part::TopoShapePy::Type))) {
						const TopoDS_Shape& sh = static_cast<TopoShapePy*>((*it).ptr())->
							getTopoShapePtr()->getShape();
						if (!sh.IsNull())
							builder.Add(Comp, sh);
					}
				}
			}
			catch (Standard_Failure& e) {
				throw Py::Exception(PartExceptionOCCError, e.GetMessageString());
			}

			return Py::asObject(new TopoShapeCompoundPy(new TopoShape(Comp)));
		}
		Py::Object makeShell(const Py::Tuple& args)
		{
			PyObject *obj;
			if (!PyArg_ParseTuple(args.ptr(), "O", &obj))
				throw Py::Exception();

			BRep_Builder builder;
			TopoDS_Shape shape;
			TopoDS_Shell shell;
			//BRepOffsetAPI_Sewing mkShell;
			builder.MakeShell(shell);

			try {
				Py::Sequence list(obj);
				for (Py::Sequence::iterator it = list.begin(); it != list.end(); ++it) {
					if (PyObject_TypeCheck((*it).ptr(), &(Part::TopoShapeFacePy::Type))) {
						const TopoDS_Shape& sh = static_cast<TopoShapeFacePy*>((*it).ptr())->
							getTopoShapePtr()->getShape();
						if (!sh.IsNull())
							builder.Add(shell, sh);
					}
				}

				shape = shell;
				BRepCheck_Analyzer check(shell);
				if (!check.IsValid()) {
					ShapeUpgrade_ShellSewing sewShell;
					shape = sewShell.ApplySewing(shell);
				}
			}
			catch (Standard_Failure& e) {
				throw Py::Exception(PartExceptionOCCError, e.GetMessageString());
			}

			return Py::asObject(new TopoShapeShellPy(new TopoShape(shape)));
		}
		Py::Object makeFace(const Py::Tuple& args)
		{
			try {
				char* className = 0;
				PyObject* pcPyShapeOrList = nullptr;
				PyErr_Clear();
				if (PyArg_ParseTuple(args.ptr(), "Os", &pcPyShapeOrList, &className)) {
					std::unique_ptr<FaceMaker> fm = Part::FaceMaker::ConstructFromType(className);

					//dump all supplied shapes to facemaker, no matter what type (let facemaker decide).
					if (PySequence_Check(pcPyShapeOrList)){
						Py::Sequence list(pcPyShapeOrList);
						for (Py::Sequence::iterator it = list.begin(); it != list.end(); ++it) {
							PyObject* item = (*it).ptr();
							if (PyObject_TypeCheck(item, &(Part::TopoShapePy::Type))) {
								const TopoDS_Shape& sh = static_cast<Part::TopoShapePy*>(item)->getTopoShapePtr()->getShape();
								fm->addShape(sh);
							}
							else {
								throw Py::TypeError("Object is not a shape.");
							}
						}
					}
					else if (PyObject_TypeCheck(pcPyShapeOrList, &(Part::TopoShapePy::Type))) {
						const TopoDS_Shape& sh = static_cast<Part::TopoShapePy*>(pcPyShapeOrList)->getTopoShapePtr()->getShape();
						if (sh.IsNull())
							throw Base::Exception("Shape is null!");
						if (sh.ShapeType() == TopAbs_COMPOUND)
							fm->useCompound(TopoDS::Compound(sh));
						else
							fm->addShape(sh);
					}
					else {
						throw Py::Exception(PyExc_TypeError, "First argument is neither a shape nor list of shapes.");
					}

					fm->Build();

					if (fm->Shape().IsNull())
						return Py::asObject(new TopoShapePy(new TopoShape(fm->Shape())));

					switch (fm->Shape().ShapeType()){
					case TopAbs_FACE:
						return Py::asObject(new TopoShapeFacePy(new TopoShape(fm->Shape())));
					case TopAbs_COMPOUND:
						return Py::asObject(new TopoShapeCompoundPy(new TopoShape(fm->Shape())));
					default:
						return Py::asObject(new TopoShapePy(new TopoShape(fm->Shape())));
					}
				}

				throw Py::Exception(Base::BaseExceptionFreeCADError, std::string("Argument type signature not recognized. Should be either (list, string), or (shape, string)"));

			}
			catch (Standard_Failure& e) {
				throw Py::Exception(PartExceptionOCCError, e.GetMessageString());
			}
			catch (Base::Exception &e){
				throw Py::Exception(Base::BaseExceptionFreeCADError, e.what());
			}
		}
		Py::Object makeFilledFace(const Py::Tuple& args)
		{
			// TODO: BRepFeat_SplitShape
			PyObject *obj;
			PyObject *surf = 0;
			if (!PyArg_ParseTuple(args.ptr(), "O|O!", &obj, &TopoShapeFacePy::Type, &surf))
				throw Py::Exception();

			// See also BRepOffsetAPI_MakeFilling
			BRepFill_Filling builder;
			try {
				if (surf) {
					const TopoDS_Shape& face = static_cast<TopoShapeFacePy*>(surf)->
						getTopoShapePtr()->getShape();
					if (!face.IsNull() && face.ShapeType() == TopAbs_FACE) {
						builder.LoadInitSurface(TopoDS::Face(face));
					}
				}
				Py::Sequence list(obj);
				int numConstraints = 0;
				for (Py::Sequence::iterator it = list.begin(); it != list.end(); ++it) {
					if (PyObject_TypeCheck((*it).ptr(), &(Part::TopoShapePy::Type))) {
						const TopoDS_Shape& sh = static_cast<TopoShapePy*>((*it).ptr())->
							getTopoShapePtr()->getShape();
						if (!sh.IsNull()) {
							if (sh.ShapeType() == TopAbs_EDGE) {
								builder.Add(TopoDS::Edge(sh), GeomAbs_C0);
								numConstraints++;
							}
							else if (sh.ShapeType() == TopAbs_FACE) {
								builder.Add(TopoDS::Face(sh), GeomAbs_C0);
								numConstraints++;
							}
							else if (sh.ShapeType() == TopAbs_VERTEX) {
								const TopoDS_Vertex& v = TopoDS::Vertex(sh);
								gp_Pnt pnt = BRep_Tool::Pnt(v);
								builder.Add(pnt);
								numConstraints++;
							}
						}
					}
				}

				if (numConstraints == 0) {
					throw Py::Exception(PartExceptionOCCError, "Failed to created face with no constraints");
				}

				builder.Build();
				if (builder.IsDone()) {
					return Py::asObject(new TopoShapeFacePy(new TopoShape(builder.Face())));
				}
				else {
					throw Py::Exception(PartExceptionOCCError, "Failed to created face by filling edges");
				}
			}
			catch (Standard_Failure& e) {
				throw Py::Exception(PartExceptionOCCError, e.GetMessageString());
			}
		}
		Py::Object makeSolid(const Py::Tuple& args)
		{
			PyObject *obj;
			if (!PyArg_ParseTuple(args.ptr(), "O!", &(TopoShapePy::Type), &obj))
				throw Py::Exception();

			try {
				const TopoDS_Shape& shape = static_cast<TopoShapePy*>(obj)
					->getTopoShapePtr()->getShape();
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
					return Py::asObject(new TopoShapeSolidPy(new TopoShape(solid)));
				}
				else if (count == 1) {
					BRepBuilderAPI_MakeSolid mkSolid(compsolid);
					TopoDS_Solid solid = mkSolid.Solid();
					return Py::asObject(new TopoShapeSolidPy(new TopoShape(solid)));
				}
				else { // if (count > 1)
					Standard_Failure::Raise("Only one compsolid can be accepted. Provided shape has more than one compsolid.");
					return Py::None(); //prevents compiler warning
				}
			}
			catch (Standard_Failure err) {
				std::stringstream errmsg;
				errmsg << "Creation of solid failed: " << err.GetMessageString();
				throw Py::Exception(PartExceptionOCCError, errmsg.str().c_str());
			}
		}
		Py::Object makePlane(const Py::Tuple& args)
		{
			double length, width;
			PyObject *pPnt = 0, *pDirZ = 0, *pDirX = 0;
			if (!PyArg_ParseTuple(args.ptr(), "dd|O!O!O!", &length, &width,
				&(Base::VectorPy::Type), &pPnt,
				&(Base::VectorPy::Type), &pDirZ,
				&(Base::VectorPy::Type), &pDirX))
				throw Py::Exception();

			if (length < Precision::Confusion()) {
				throw Py::ValueError("length of plane too small");
			}
			if (width < Precision::Confusion()) {
				throw Py::ValueError("width of plane too small");
			}

			try {
				gp_Pnt p(0, 0, 0);
				gp_Dir d(0, 0, 1);
				if (pPnt) {
					Base::Vector3d pnt = static_cast<Base::VectorPy*>(pPnt)->value();
					p.SetCoord(pnt.x, pnt.y, pnt.z);
				}
				if (pDirZ) {
					Base::Vector3d vec = static_cast<Base::VectorPy*>(pDirZ)->value();
					d.SetCoord(vec.x, vec.y, vec.z);
				}
				Handle(Geom_Plane) aPlane;
				if (pDirX) {
					Base::Vector3d vec = static_cast<Base::VectorPy*>(pDirX)->value();
					gp_Dir dx;
					dx.SetCoord(vec.x, vec.y, vec.z);
					aPlane = new Geom_Plane(gp_Ax3(p, d, dx));
				}
				else {
					aPlane = new Geom_Plane(p, d);
				}

				BRepBuilderAPI_MakeFace Face(aPlane, 0.0, length, 0.0, width
#if OCC_VERSION_HEX >= 0x060502
					, Precision::Confusion()
#endif
					);
				return Py::asObject(new TopoShapeFacePy(new TopoShape((Face.Face()))));
			}
			catch (Standard_DomainError) {
				throw Py::Exception(PartExceptionOCCDomainError, "creation of plane failed");
			}
			catch (Standard_Failure) {
				throw Py::Exception(PartExceptionOCCError, "creation of plane failed");
			}
		}
		Py::Object makeBox(const Py::Tuple& args)
		{
			double length, width, height;
			PyObject *pPnt = 0, *pDir = 0;
			if (!PyArg_ParseTuple(args.ptr(), "ddd|O!O!",
				&length, &width, &height,
				&(Base::VectorPy::Type), &pPnt,
				&(Base::VectorPy::Type), &pDir))
				throw Py::Exception();

			if (length < Precision::Confusion()) {
				throw Py::ValueError("length of box too small");
			}
			if (width < Precision::Confusion()) {
				throw Py::ValueError("width of box too small");
			}
			if (height < Precision::Confusion()) {
				throw Py::ValueError("height of box too small");
			}

			try {
				gp_Pnt p(0, 0, 0);
				gp_Dir d(0, 0, 1);
				if (pPnt) {
					Base::Vector3d pnt = static_cast<Base::VectorPy*>(pPnt)->value();
					p.SetCoord(pnt.x, pnt.y, pnt.z);
				}
				if (pDir) {
					Base::Vector3d vec = static_cast<Base::VectorPy*>(pDir)->value();
					d.SetCoord(vec.x, vec.y, vec.z);
				}
				BRepPrimAPI_MakeBox mkBox(gp_Ax2(p, d), length, width, height);
				TopoDS_Shape ResultShape = mkBox.Shape();
				return Py::asObject(new TopoShapeSolidPy(new TopoShape(ResultShape)));
			}
			catch (Standard_DomainError) {
				throw Py::Exception(PartExceptionOCCDomainError, "creation of box failed");
			}
		}
		///Start 草图建模的拉伸
		Py::Object makeExtrude(const Py::Tuple& args){
			const char* baseObjName = 0;
			double length;
			PyObject *pDir = 0;
			if (!PyArg_ParseTuple(args.ptr(), "sd|O!",
				& baseObjName,
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
				ExtrusionParameters params = computeFinalParameters(link,length);
				TopoShape result = extrudeShape(base->Shape.getShape(),params);

				return Py::asObject(new TopoShapeSolidPy(new TopoShape(result)));


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
			bool isReverse=false,
			bool isSymmetric=false,
			bool isSolid=true,
			double TaperAngle=0.0,
			double TaperAngleRev=0.0)
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



		TopoShape extrudeShape(const TopoShape source, ExtrusionParameters params)
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
					std::unique_ptr<FaceMaker> mkFace = FaceMaker::ConstructFromType(params.faceMakerClass.c_str());

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
			return TopoShape(result);
		}

		Base::Vector3d calculateShapeNormal(const App::DocumentObject* shapeLink){
			if (!shapeLink){
				std::cerr << "no resource obj" << std::endl;
			}
			const TopoShape &tsh = static_cast<const Part::Feature*>(shapeLink)->Shape.getShape();
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
				throw Py::Exception(PartExceptionOCCDomainError, "revolutionShape error");
				//return NULL;
			}
			if (!link->getTypeId().isDerivedFrom(Part::Feature::getClassTypeId()))
			{
				std::cerr << "base Area is not a part shape" << std::endl;
				throw Py::Exception(PartExceptionOCCDomainError, "revolutionShape error");
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
				TopoShape sourceShape = baseObj->Shape.getShape();
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
					std::unique_ptr<FaceMaker> mkFace = FaceMaker::ConstructFromType(faceMakerClass.c_str());

					TopoDS_Shape myShape = sourceShape.getShape();
					if (myShape.ShapeType() == TopAbs_COMPOUND)
						mkFace->useCompound(TopoDS::Compound(myShape));
					else
						mkFace->addShape(myShape);
					mkFace->Build();
					myShape = mkFace->Shape();
					sourceShape = TopoShape(myShape);

					makeSolid = Standard_False;//don't ask TopoShape::revolve to make solid, as we've made faces...
				}

				// actual revolution!
				TopoDS_Shape revolve = sourceShape.revolve(revAx, thisAngle, makeSolid);

				return revolve;
			}catch (Standard_Failure& e) {
				std::cerr << "make revolution error" << std::endl;
				throw Py::Exception(PartExceptionOCCDomainError, "revolutionShape error");
				//return new App::DocumentObjectExecReturn(e.GetMessageString());
			}
		}
		Py::Object makePicRevolution(const Py::Tuple& args)
		{
			const char* baseAreaName = 0;
			PyObject *pBase = 0;
			PyObject *pAxis = 0;
			double angle=360;

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
					throw Py::Exception(PartExceptionOCCDomainError, "revolution shape is null");
				}
				//if (resultShape->IsNull()){
				//	throw Py::Exception(PartExceptionOCCDomainError, "revolution shape is null");
				//}
				return Py::asObject(new TopoShapeSolidPy(new TopoShape(resultShape)));

			}
			catch (Standard_DomainError) {
				throw Py::Exception(PartExceptionOCCDomainError, "creation of revolution failed");
			}

		}
		/// end  旋转体
		Py::Object makeWedge(const Py::Tuple& args)
		{
			double xmin, ymin, zmin, z2min, x2min, xmax, ymax, zmax, z2max, x2max;
			PyObject *pPnt = 0, *pDir = 0;
			if (!PyArg_ParseTuple(args.ptr(), "dddddddddd|O!O!",
				&xmin, &ymin, &zmin, &z2min, &x2min, &xmax, &ymax, &zmax, &z2max, &x2max,
				&(Base::VectorPy::Type), &pPnt, &(Base::VectorPy::Type), &pDir))
				throw Py::Exception();

			double dx = xmax - xmin;
			double dy = ymax - ymin;
			double dz = zmax - zmin;
			double dz2 = z2max - z2min;
			double dx2 = x2max - x2min;
			if (dx < Precision::Confusion()) {
				throw Py::ValueError("delta x of wedge too small");
			}
			if (dy < Precision::Confusion()) {
				throw Py::ValueError("delta y of wedge too small");
			}
			if (dz < Precision::Confusion()) {
				throw Py::ValueError("delta z of wedge too small");
			}
			if (dz2 < 0) {
				throw Py::ValueError("delta z2 of wedge is negative");
			}
			if (dx2 < 0) {
				throw Py::ValueError("delta x2 of wedge is negative");
			}

			try {
				gp_Pnt p(0, 0, 0);
				gp_Dir d(0, 0, 1);
				if (pPnt) {
					Base::Vector3d pnt = static_cast<Base::VectorPy*>(pPnt)->value();
					p.SetCoord(pnt.x, pnt.y, pnt.z);
				}
				if (pDir) {
					Base::Vector3d vec = static_cast<Base::VectorPy*>(pDir)->value();
					d.SetCoord(vec.x, vec.y, vec.z);
				}
				BRepPrim_Wedge mkWedge(gp_Ax2(p, d), xmin, ymin, zmin, z2min, x2min, xmax, ymax, zmax, z2max, x2max);
				BRepBuilderAPI_MakeSolid mkSolid;
				mkSolid.Add(mkWedge.Shell());
				return Py::asObject(new TopoShapeSolidPy(new TopoShape(mkSolid.Solid())));
			}
			catch (Standard_DomainError) {
				throw Py::Exception(PartExceptionOCCDomainError, "creation of wedge failed");
			}
		}
		Py::Object makeLine(const Py::Tuple& args)
		{
			PyObject *obj1, *obj2;
			if (!PyArg_ParseTuple(args.ptr(), "OO", &obj1, &obj2))
				throw Py::Exception();

			Base::Vector3d pnt1, pnt2;
			if (PyObject_TypeCheck(obj1, &(Base::VectorPy::Type))) {
				pnt1 = static_cast<Base::VectorPy*>(obj1)->value();
			}
			else if (PyObject_TypeCheck(obj1, &PyTuple_Type)) {
				pnt1 = Base::getVectorFromTuple<double>(obj1);
			}
			else {
				throw Py::TypeError("first argument must either be vector or tuple");
			}
			if (PyObject_TypeCheck(obj2, &(Base::VectorPy::Type))) {
				pnt2 = static_cast<Base::VectorPy*>(obj2)->value();
			}
			else if (PyObject_TypeCheck(obj2, &PyTuple_Type)) {
				pnt2 = Base::getVectorFromTuple<double>(obj2);
			}
			else {
				throw Py::TypeError("second argument must either be vector or tuple");
			}

			// Create directly the underlying line geometry
			BRepBuilderAPI_MakeEdge makeEdge(gp_Pnt(pnt1.x, pnt1.y, pnt1.z),
				gp_Pnt(pnt2.x, pnt2.y, pnt2.z));

			const char *error = 0;
			switch (makeEdge.Error())
			{
			case BRepBuilderAPI_EdgeDone:
				break; // ok
			case BRepBuilderAPI_PointProjectionFailed:
				error = "Point projection failed";
				break;
			case BRepBuilderAPI_ParameterOutOfRange:
				error = "Parameter out of range";
				break;
			case BRepBuilderAPI_DifferentPointsOnClosedCurve:
				error = "Different points on closed curve";
				break;
			case BRepBuilderAPI_PointWithInfiniteParameter:
				error = "Point with infinite parameter";
				break;
			case BRepBuilderAPI_DifferentsPointAndParameter:
				error = "Different point and parameter";
				break;
			case BRepBuilderAPI_LineThroughIdenticPoints:
				error = "Line through identic points";
				break;
			}
			// Error 
			if (error) {
				throw Py::Exception(PartExceptionOCCError, error);
			}

			TopoDS_Edge edge = makeEdge.Edge();
			return Py::asObject(new TopoShapeEdgePy(new TopoShape(edge)));
		}
		Py::Object makePolygon(const Py::Tuple& args)
		{
			PyObject *pcObj;
			PyObject *pclosed = Py_False;
			if (!PyArg_ParseTuple(args.ptr(), "O|O!", &pcObj, &(PyBool_Type), &pclosed))
				throw Py::Exception();

			BRepBuilderAPI_MakePolygon mkPoly;
			try {
				Py::Sequence list(pcObj);
				for (Py::Sequence::iterator it = list.begin(); it != list.end(); ++it) {
					if (PyObject_TypeCheck((*it).ptr(), &(Base::VectorPy::Type))) {
						Base::Vector3d v = static_cast<Base::VectorPy*>((*it).ptr())->value();
						mkPoly.Add(gp_Pnt(v.x, v.y, v.z));
					}
					else if (PyObject_TypeCheck((*it).ptr(), &PyTuple_Type)) {
						Base::Vector3d v = Base::getVectorFromTuple<double>((*it).ptr());
						mkPoly.Add(gp_Pnt(v.x, v.y, v.z));
					}
				}

				if (!mkPoly.IsDone())
					Standard_Failure::Raise("Cannot create polygon because less than two vertices are given");

				// if the polygon should be closed
				if (PyObject_IsTrue(pclosed)) {
					if (!mkPoly.FirstVertex().IsSame(mkPoly.LastVertex())) {
						mkPoly.Add(mkPoly.FirstVertex());
					}
				}

				return Py::asObject(new TopoShapeWirePy(new TopoShape(mkPoly.Wire())));
			}
			catch (Standard_Failure& e) {
				throw Py::Exception(PartExceptionOCCError, e.GetMessageString());
			}
		}
		Py::Object makeCircle(const Py::Tuple& args)
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
				return Py::asObject(new TopoShapeEdgePy(new TopoShape(edge)));
			}
			catch (Standard_Failure) {
				throw Py::Exception(PartExceptionOCCError, "creation of circle failed");
			}
		}
		Py::Object makeSphere(const Py::Tuple& args)
		{
			double radius, angle1 = -90, angle2 = 90, angle3 = 360;
			PyObject *pPnt = 0, *pDir = 0;
			if (!PyArg_ParseTuple(args.ptr(), "d|O!O!ddd",
				&radius,
				&(Base::VectorPy::Type), &pPnt,
				&(Base::VectorPy::Type), &pDir,
				&angle1, &angle2, &angle3))
				throw Py::Exception();

			try {
				gp_Pnt p(0, 0, 0);
				gp_Dir d(0, 0, 1);
				if (pPnt) {
					Base::Vector3d pnt = static_cast<Base::VectorPy*>(pPnt)->value();
					p.SetCoord(pnt.x, pnt.y, pnt.z);
				}
				if (pDir) {
					Base::Vector3d vec = static_cast<Base::VectorPy*>(pDir)->value();
					d.SetCoord(vec.x, vec.y, vec.z);
				}
				BRepPrimAPI_MakeSphere mkSphere(gp_Ax2(p, d), radius, angle1*(M_PI / 180), angle2*(M_PI / 180), angle3*(M_PI / 180));
				TopoDS_Shape shape = mkSphere.Shape();
				return Py::asObject(new TopoShapeSolidPy(new TopoShape(shape)));
			}
			catch (Standard_DomainError) {
				throw Py::Exception(PartExceptionOCCDomainError, "creation of sphere failed");
			}
		}
		Py::Object makeCylinder(const Py::Tuple& args)
		{
			double radius, height, angle = 360;
			PyObject *pPnt = 0, *pDir = 0;
			if (!PyArg_ParseTuple(args.ptr(), "dd|O!O!d",
				&radius, &height,
				&(Base::VectorPy::Type), &pPnt,
				&(Base::VectorPy::Type), &pDir,
				&angle))
				throw Py::Exception();

			try {
				gp_Pnt p(0, 0, 0);
				gp_Dir d(0, 0, 1);
				if (pPnt) {
					Base::Vector3d pnt = static_cast<Base::VectorPy*>(pPnt)->value();
					p.SetCoord(pnt.x, pnt.y, pnt.z);
				}
				if (pDir) {
					Base::Vector3d vec = static_cast<Base::VectorPy*>(pDir)->value();
					d.SetCoord(vec.x, vec.y, vec.z);
				}
				BRepPrimAPI_MakeCylinder mkCyl(gp_Ax2(p, d), radius, height, angle*(M_PI / 180));
				TopoDS_Shape shape = mkCyl.Shape();
				return Py::asObject(new TopoShapeSolidPy(new TopoShape(shape)));
			}
			catch (Standard_DomainError) {
				throw Py::Exception(PartExceptionOCCDomainError, "creation of cylinder failed");
			}
		}
		Py::Object makeCone(const Py::Tuple& args)
		{
			double radius1, radius2, height, angle = 360;
			PyObject *pPnt = 0, *pDir = 0;
			if (!PyArg_ParseTuple(args.ptr(), "ddd|O!O!d",
				&radius1, &radius2, &height,
				&(Base::VectorPy::Type), &pPnt,
				&(Base::VectorPy::Type), &pDir,
				&angle))
				throw Py::Exception();

			try {
				gp_Pnt p(0, 0, 0);
				gp_Dir d(0, 0, 1);
				if (pPnt) {
					Base::Vector3d pnt = static_cast<Base::VectorPy*>(pPnt)->value();
					p.SetCoord(pnt.x, pnt.y, pnt.z);
				}
				if (pDir) {
					Base::Vector3d vec = static_cast<Base::VectorPy*>(pDir)->value();
					d.SetCoord(vec.x, vec.y, vec.z);
				}
				BRepPrimAPI_MakeCone mkCone(gp_Ax2(p, d), radius1, radius2, height, angle*(M_PI / 180));
				TopoDS_Shape shape = mkCone.Shape();
				return Py::asObject(new TopoShapeSolidPy(new TopoShape(shape)));
			}
			catch (Standard_DomainError) {
				throw Py::Exception(PartExceptionOCCDomainError, "creation of cone failed");
			}
		}

		void testTime(std::string mark,clock_t &t0, clock_t t1){
			t1 = clock();
			std::cerr << mark<<" " << double(t1 - t0) << std::endl;
		}
		Py::Object makeFuncMesh(const Py::Tuple& args)
		{
			//clock_t t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10;
			//由面形成实体的精确度 如果函数体的范围是1-10  将精确度设置为0.001（否则会很慢），一般情况下设置为0.01，
			Standard_Real facePrecision = 0.01;
			//type=0表示面，1表示体
			int type = 0;
			double radius1, radius2, height, angle = 360;
			char* func;
			double xmax, xmin, ymax, ymin, zmax, zmin = 0;
			char* path;
			//精度
			char* precision;
			PyObject *pPnt = 0, *pDir = 0;
			if (!PyArg_ParseTuple(args.ptr(), "isddddddss",
				&type,&func, &xmin, &xmax, &ymin, &ymax, &zmin, &zmax, &path,&precision
				))
				throw Py::Exception();

			try {

				//t0 = clock();
				/*输出文件*/
				std::string filePath(path);
				//生成文件，如果存在删除重来
				std::ofstream file(path, std::ios::trunc);
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
					if (1.0 < absmax < 10.0)
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
					//再稍微扩大一点
					double res = absmax / 10;
					//absmax = absmax + res;
					//
					xmin = -absmax-res;
					ymin = -absmax - res;
					zmin = -absmax - res;
					xmax = absmax +res;
					ymax = absmax + res;
					zmax = absmax + res;


					//这里确定面的精确度
					if (1.0 < absmax < 10.0)
						facePrecision = 0.001;
					//facePrecision = 2.1;

				}
				boost::format fmt(jsonTemp);
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
				stStartUpInfo.wShowWindow = SW_HIDE;
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

						for (size_t i = 0; i < 100; i++)
						{

							Base::FileInfo fi(objPath);
							if (fi.exists() && fi.isFile())
							{
								noexist = false;
								break;
							}
							Sleep(100);
						}
						//testTime("t3 ", t0, t1);
						/*
						//从共享内存中读取数据
						std::string strMapName("ShareMemory");                // 内存映射对象名称
						//float *strcomdata = { 0,1 };
						LPVOID pBuffer;                                    // 共享内存指针

						// 首先试图打开一个命名的内存映射文件对象  
						HANDLE hMap = ::OpenFileMapping(FILE_MAP_ALL_ACCESS, 0, strMapName.c_str());
						if (hMap){
							// 打开成功，映射对象的一个视图，得到指向共享内存的指针，显示出里面的数据
							pBuffer = ::MapViewOfFile(hMap, FILE_MAP_ALL_ACCESS, 0, 0, 0);
							std::cout << "read Points data:" << (char *)pBuffer << std::endl;
						}
						else{
							std::cout << "none points data\n";
						}
						// 解除文件映射，关闭内存映射文件对象句柄
						::UnmapViewOfFile(pBuffer);
						::CloseHandle(hMap);
						*/

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
							throw Py::Exception(PartExceptionOCCError, " Cant make Function Mesh");
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









				TopoDS_Shell mkPoly;

				try {
					Base::FileInfo fi(objPath);
					if (!fi.exists() || !fi.isFile())
						throw Base::FileException("File does not exist", objPath);
					if (!fi.isReadable())
						throw Base::FileException("No permission on the file", objPath);

					Base::ifstream str(fi, std::ios::in | std::ios::binary);


					//TopoDS_Shell mkPoly;

					//LoadOBJ(str, mkPoly);
					//TopoDS_Shell resultShape;
					TopoShape resultShape;
					//std::shared_ptr<TopoShape> resultShapePtr(new TopoShape());
					//testTime("t4 ", t0, t1);
					LoadOBJ2(str, resultShape, facePrecision);
					//testTime("t5 ", t0, t1);
					//	if (!mkPoly.IsDone())
					//		Standard_Failure::Raise("Cannot create polygon because less than two vertices are given");

					Py::Object result = Py::asObject(new TopoShapePy(new TopoShape(resultShape)));
					//testTime("t6 ", t0, t1);
					return result;
				}
				catch (Standard_Failure& e) {
					throw Py::Exception(PartExceptionOCCError, e.GetMessageString());
				}
			}
			catch (Standard_DomainError) {
				throw Py::Exception(PartExceptionOCCDomainError, "creation of funcmesh failed");
			}
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

					return Py::asObject(new TopoShapePy(new TopoShape(mkPoly)));
				}
				catch (Standard_Failure& e) {
					throw Py::Exception(PartExceptionOCCError, e.GetMessageString());
				}
			}
			catch (Standard_DomainError) {
				throw Py::Exception(PartExceptionOCCDomainError, "creation of objFileMesh failed");
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
				return Py::asObject(new TopoShapeEdgePy(new TopoShape(edge)));
			}
			catch (Standard_Failure) {
				throw Py::Exception(PartExceptionOCCError, "creation of circle failed");
			}
		}
		Py::Object makeTorus(const Py::Tuple& args)
		{
			double radius1, radius2, angle1 = 0.0, angle2 = 360, angle = 360;
			PyObject *pPnt = 0, *pDir = 0;
			if (!PyArg_ParseTuple(args.ptr(), "dd|O!O!ddd",
				&radius1, &radius2,
				&(Base::VectorPy::Type), &pPnt,
				&(Base::VectorPy::Type), &pDir,
				&angle1, &angle2, &angle))
				throw Py::Exception();

			try {
				gp_Pnt p(0, 0, 0);
				gp_Dir d(0, 0, 1);
				if (pPnt) {
					Base::Vector3d pnt = static_cast<Base::VectorPy*>(pPnt)->value();
					p.SetCoord(pnt.x, pnt.y, pnt.z);
				}
				if (pDir) {
					Base::Vector3d vec = static_cast<Base::VectorPy*>(pDir)->value();
					d.SetCoord(vec.x, vec.y, vec.z);
				}
				BRepPrimAPI_MakeTorus mkTorus(gp_Ax2(p, d), radius1, radius2, angle1*(M_PI / 180), angle2*(M_PI / 180), angle*(M_PI / 180));
				const TopoDS_Shape& shape = mkTorus.Shape();
				return Py::asObject(new TopoShapeSolidPy(new TopoShape(shape)));
			}
			catch (Standard_DomainError) {
				throw Py::Exception(PartExceptionOCCDomainError, "creation of torus failed");
			}
		}
		Py::Object makeHelix(const Py::Tuple& args)
		{
			double pitch, height, radius, angle = -1.0;
			PyObject *pleft = Py_False;
			PyObject *pvertHeight = Py_False;
			if (!PyArg_ParseTuple(args.ptr(), "ddd|dO!O!",
				&pitch, &height, &radius, &angle,
				&(PyBool_Type), &pleft,
				&(PyBool_Type), &pvertHeight))
				throw Py::Exception();

			try {
				TopoShape helix;
				Standard_Boolean anIsLeft = PyObject_IsTrue(pleft) ? Standard_True : Standard_False;
				Standard_Boolean anIsVertHeight = PyObject_IsTrue(pvertHeight) ? Standard_True : Standard_False;
				TopoDS_Shape wire = helix.makeHelix(pitch, height, radius, angle,
					anIsLeft, anIsVertHeight);
				return Py::asObject(new TopoShapeWirePy(new TopoShape(wire)));
			}
			catch (Standard_Failure& e) {
				throw Py::Exception(PartExceptionOCCError, e.GetMessageString());
			}
		}
		Py::Object makeLongHelix(const Py::Tuple& args)
		{
			double pitch, height, radius, angle = -1.0;
			PyObject *pleft = Py_False;
			if (!PyArg_ParseTuple(args.ptr(), "ddd|dO!", &pitch, &height, &radius, &angle,
				&(PyBool_Type), &pleft)) {
				throw Py::Exception("Part.makeLongHelix fails on parms");
			}

			try {
				TopoShape helix;
				Standard_Boolean anIsLeft = PyObject_IsTrue(pleft) ? Standard_True : Standard_False;
				TopoDS_Shape wire = helix.makeLongHelix(pitch, height, radius, angle, anIsLeft);
				return Py::asObject(new TopoShapeWirePy(new TopoShape(wire)));
			}
			catch (Standard_Failure& e) {
				throw Py::Exception(PartExceptionOCCError, e.GetMessageString());
			}
		}
		Py::Object makeThread(const Py::Tuple& args)
		{
			double pitch, depth, height, radius;
			if (!PyArg_ParseTuple(args.ptr(), "dddd", &pitch, &depth, &height, &radius))
				throw Py::Exception();

			try {
				TopoShape helix;
				TopoDS_Shape wire = helix.makeThread(pitch, depth, height, radius);
				return Py::asObject(new TopoShapeWirePy(new TopoShape(wire)));
			}
			catch (Standard_Failure& e) {
				throw Py::Exception(PartExceptionOCCError, e.GetMessageString());
			}
		}
		Py::Object makeRevolution(const Py::Tuple& args)
		{
			double vmin = DBL_MAX, vmax = -DBL_MAX;
			double angle = 360;
			PyObject *pPnt = 0, *pDir = 0, *pCrv;
			Handle(Geom_Curve) curve;
			union PyType_Object defaultType = { &Part::TopoShapeSolidPy::Type };
			PyObject* type = defaultType.o;
			if (PyArg_ParseTuple(args.ptr(), "O!|dddO!O!O!", &(GeometryPy::Type), &pCrv,
				&vmin, &vmax, &angle,
				&(Base::VectorPy::Type), &pPnt,
				&(Base::VectorPy::Type), &pDir,
				&(PyType_Type), &type)) {
				GeometryPy* pcGeo = static_cast<GeometryPy*>(pCrv);
				curve = Handle(Geom_Curve)::DownCast
					(pcGeo->getGeometryPtr()->handle());
				if (curve.IsNull()) {
					throw Py::Exception(PyExc_TypeError, "geometry is not a curve");
				}
				if (vmin == DBL_MAX)
					vmin = curve->FirstParameter();

				if (vmax == -DBL_MAX)
					vmax = curve->LastParameter();
			}
			else {
				PyErr_Clear();
				if (!PyArg_ParseTuple(args.ptr(), "O!|dddO!O!", &(TopoShapePy::Type), &pCrv,
					&vmin, &vmax, &angle, &(Base::VectorPy::Type), &pPnt,
					&(Base::VectorPy::Type), &pDir)) {
					throw Py::Exception();
				}
				const TopoDS_Shape& shape = static_cast<TopoShapePy*>(pCrv)->getTopoShapePtr()->getShape();
				if (shape.IsNull()) {
					throw Py::Exception(PartExceptionOCCError, "shape is empty");
				}

				if (shape.ShapeType() != TopAbs_EDGE) {
					throw Py::Exception(PartExceptionOCCError, "shape is not an edge");
				}

				const TopoDS_Edge& edge = TopoDS::Edge(shape);
				BRepAdaptor_Curve adapt(edge);

				const Handle(Geom_Curve)& hCurve = adapt.Curve().Curve();
				// Apply placement of the shape to the curve
				TopLoc_Location loc = edge.Location();
				curve = Handle(Geom_Curve)::DownCast(hCurve->Transformed(loc.Transformation()));
				if (curve.IsNull()) {
					throw Py::Exception(PartExceptionOCCError, "invalid curve in edge");
				}

				if (vmin == DBL_MAX)
					vmin = adapt.FirstParameter();
				if (vmax == -DBL_MAX)
					vmax = adapt.LastParameter();
			}

			try {
				gp_Pnt p(0, 0, 0);
				gp_Dir d(0, 0, 1);
				if (pPnt) {
					Base::Vector3d pnt = static_cast<Base::VectorPy*>(pPnt)->value();
					p.SetCoord(pnt.x, pnt.y, pnt.z);
				}
				if (pDir) {
					Base::Vector3d vec = static_cast<Base::VectorPy*>(pDir)->value();
					d.SetCoord(vec.x, vec.y, vec.z);
				}

				union PyType_Object shellType = { &Part::TopoShapeShellPy::Type };
				union PyType_Object faceType = { &Part::TopoShapeFacePy::Type };

				BRepPrimAPI_MakeRevolution mkRev(gp_Ax2(p, d), curve, vmin, vmax, angle*(M_PI / 180));
				if (type == defaultType.o) {
					TopoDS_Shape shape = mkRev.Solid();
					return Py::asObject(new TopoShapeSolidPy(new TopoShape(shape)));
				}
				else if (type == shellType.o) {
					TopoDS_Shape shape = mkRev.Shell();
					return Py::asObject(new TopoShapeShellPy(new TopoShape(shape)));
				}
				else if (type == faceType.o) {
					TopoDS_Shape shape = mkRev.Face();
					return Py::asObject(new TopoShapeFacePy(new TopoShape(shape)));
				}
				else {
					TopoDS_Shape shape = mkRev.Shape();
					return Py::asObject(new TopoShapePy(new TopoShape(shape)));
				}
			}
			catch (Standard_DomainError) {
				throw Py::Exception(PartExceptionOCCDomainError, "creation of revolved shape failed");
			}
		}
		Py::Object makeRuledSurface(const Py::Tuple& args)
		{
			// http://opencascade.blogspot.com/2009/10/surface-modeling-part1.html
			PyObject *sh1, *sh2;
			if (!PyArg_ParseTuple(args.ptr(), "O!O!", &(TopoShapePy::Type), &sh1,
				&(TopoShapePy::Type), &sh2))
				throw Py::Exception();

			const TopoDS_Shape& shape1 = static_cast<TopoShapePy*>(sh1)->getTopoShapePtr()->getShape();
			const TopoDS_Shape& shape2 = static_cast<TopoShapePy*>(sh2)->getTopoShapePtr()->getShape();

			try {
				if (shape1.ShapeType() == TopAbs_EDGE && shape2.ShapeType() == TopAbs_EDGE) {
					TopoDS_Face face = BRepFill::Face(TopoDS::Edge(shape1), TopoDS::Edge(shape2));
					return Py::asObject(new TopoShapeFacePy(new TopoShape(face)));
				}
				else if (shape1.ShapeType() == TopAbs_WIRE && shape2.ShapeType() == TopAbs_WIRE) {
					TopoDS_Shell shell = BRepFill::Shell(TopoDS::Wire(shape1), TopoDS::Wire(shape2));
					return Py::asObject(new TopoShapeShellPy(new TopoShape(shell)));
				}
				else {
					throw Py::Exception(PartExceptionOCCError, "curves must either be edges or wires");
				}
			}
			catch (Standard_Failure) {
				throw Py::Exception(PartExceptionOCCError, "creation of ruled surface failed");
			}
		}
		Py::Object makeTube(const Py::Tuple& args)
		{
			PyObject *pshape;
			double radius;
			double tolerance = 0.001;
			char* scont = "C0";
			int maxdegree = 3;
			int maxsegment = 30;

			// Path + radius
			if (!PyArg_ParseTuple(args.ptr(), "O!d|sii", &(TopoShapePy::Type), &pshape, &radius, &scont, &maxdegree, &maxsegment))
				throw Py::Exception();

			std::string str_cont = scont;
			int cont;
			if (str_cont == "C0")
				cont = (int)GeomAbs_C0;
			else if (str_cont == "C1")
				cont = (int)GeomAbs_C1;
			else if (str_cont == "C2")
				cont = (int)GeomAbs_C2;
			else if (str_cont == "C3")
				cont = (int)GeomAbs_C3;
			else if (str_cont == "CN")
				cont = (int)GeomAbs_CN;
			else if (str_cont == "G1")
				cont = (int)GeomAbs_G1;
			else if (str_cont == "G2")
				cont = (int)GeomAbs_G2;
			else
				cont = (int)GeomAbs_C0;

			try {
				const TopoDS_Shape& path_shape = static_cast<TopoShapePy*>(pshape)->getTopoShapePtr()->getShape();
				TopoShape myShape(path_shape);
				TopoDS_Shape face = myShape.makeTube(radius, tolerance, cont, maxdegree, maxsegment);
				return Py::asObject(new TopoShapeFacePy(new TopoShape(face)));
			}
			catch (Standard_Failure& e) {
				throw Py::Exception(PartExceptionOCCError, e.GetMessageString());
			}
		}
		Py::Object makeSweepSurface(const Py::Tuple& args)
		{
			PyObject *path, *profile;
			double tolerance = 0.001;
			int fillMode = 0;

			// Path + profile
			if (!PyArg_ParseTuple(args.ptr(), "O!O!|di", &(TopoShapePy::Type), &path,
				&(TopoShapePy::Type), &profile,
				&tolerance, &fillMode))
				throw Py::Exception();

			try {
				const TopoDS_Shape& path_shape = static_cast<TopoShapePy*>(path)->getTopoShapePtr()->getShape();
				const TopoDS_Shape& prof_shape = static_cast<TopoShapePy*>(profile)->getTopoShapePtr()->getShape();

				TopoShape myShape(path_shape);
				TopoDS_Shape face = myShape.makeSweep(prof_shape, tolerance, fillMode);
				return Py::asObject(new TopoShapeFacePy(new TopoShape(face)));
			}
			catch (Standard_Failure& e) {
				throw Py::Exception(PartExceptionOCCError, e.GetMessageString());
			}
		}
		Py::Object makeLoft(const Py::Tuple& args)
		{
#if 0
			PyObject *pcObj;
			if (!PyArg_ParseTuple(args.ptr(), "O", &pcObj))
				throw Py::Exception;

			NCollection_List<Handle(Geom_Curve)> theSections;
			Py::Sequence list(pcObj);
			for (Py::Sequence::iterator it = list.begin(); it != list.end(); ++it) {
				if (PyObject_TypeCheck((*it).ptr(), &(Part::GeometryCurvePy::Type))) {
					Handle(Geom_Curve) hCurve = Handle(Geom_Curve)::DownCast(
						static_cast<GeometryCurvePy*>((*it).ptr())->getGeomCurvePtr()->handle());
					theSections.Append(hCurve);
				}
			}

			//populate section generator
			GeomFill_SectionGenerator aSecGenerator;
			for (NCollection_List<Handle(Geom_Curve)>::Iterator anIt(theSections); anIt.More(); anIt.Next()) {
				const Handle(Geom_Curve)& aCurve = anIt.Value();
				aSecGenerator.AddCurve(aCurve);
			}
			aSecGenerator.Perform(Precision::PConfusion());

			Handle(GeomFill_Line) aLine = new GeomFill_Line(theSections.Size());

			//parameters
			const Standard_Integer aMinDeg = 1, aMaxDeg = BSplCLib::MaxDegree(), aNbIt = 0;
			Standard_Real aTol3d = 1e-4, aTol2d = Precision::Parametric(aTol3d);

			//algorithm
			GeomFill_AppSurf anAlgo(aMinDeg, aMaxDeg, aTol3d, aTol2d, aNbIt);
			anAlgo.Perform(aLine, aSecGenerator);

			if (!anAlgo.IsDone()) {
				PyErr_SetString(PartExceptionOCCError, "Failed to create loft surface");
				return 0;
			}

			Handle(Geom_BSplineSurface) aRes;
			aRes = new Geom_BSplineSurface(anAlgo.SurfPoles(), anAlgo.SurfWeights(),
				anAlgo.SurfUKnots(), anAlgo.SurfVKnots(), anAlgo.SurfUMults(), anAlgo.SurfVMults(),
				anAlgo.UDegree(), anAlgo.VDegree());
			return new BSplineSurfacePy(new GeomBSplineSurface(aRes));
#else
			PyObject *pcObj;
			PyObject *psolid = Py_False;
			PyObject *pruled = Py_False;
			PyObject *pclosed = Py_False;
			int degMax = 5;
			if (!PyArg_ParseTuple(args.ptr(), "O|O!O!O!i", &pcObj,
				&(PyBool_Type), &psolid,
				&(PyBool_Type), &pruled,
				&(PyBool_Type), &pclosed,
				&degMax)) {
				throw Py::Exception();
			}

			TopTools_ListOfShape profiles;
			Py::Sequence list(pcObj);

			for (Py::Sequence::iterator it = list.begin(); it != list.end(); ++it) {
				if (PyObject_TypeCheck((*it).ptr(), &(Part::TopoShapePy::Type))) {
					const TopoDS_Shape& sh = static_cast<TopoShapePy*>((*it).ptr())->
						getTopoShapePtr()->getShape();
					profiles.Append(sh);
				}
			}

			TopoShape myShape;
			Standard_Boolean anIsSolid = PyObject_IsTrue(psolid) ? Standard_True : Standard_False;
			Standard_Boolean anIsRuled = PyObject_IsTrue(pruled) ? Standard_True : Standard_False;
			Standard_Boolean anIsClosed = PyObject_IsTrue(pclosed) ? Standard_True : Standard_False;
			TopoDS_Shape aResult = myShape.makeLoft(profiles, anIsSolid, anIsRuled, anIsClosed, degMax);
			return Py::asObject(new TopoShapePy(new TopoShape(aResult)));
#endif
		}
		Py::Object makeSplitShape(const Py::Tuple& args)
		{
			PyObject* shape;
			PyObject* list;
			PyObject* checkInterior = Py_True;
			if (!PyArg_ParseTuple(args.ptr(), "O!O|O!", &(TopoShapePy::Type), &shape, &list,
				&PyBool_Type, &checkInterior))
				throw Py::Exception();

			try {
				TopoDS_Shape initShape = static_cast<TopoShapePy*>
					(shape)->getTopoShapePtr()->getShape();
				BRepFeat_SplitShape splitShape(initShape);
				splitShape.SetCheckInterior(PyObject_IsTrue(checkInterior) ? Standard_True : Standard_False);

				Py::Sequence seq(list);
				for (Py::Sequence::iterator it = seq.begin(); it != seq.end(); ++it) {
					Py::Tuple tuple(*it);
					Py::TopoShape sh1(tuple[0]);
					Py::TopoShape sh2(tuple[1]);
					const TopoDS_Shape& shape1 = sh1.extensionObject()->getTopoShapePtr()->getShape();
					const TopoDS_Shape& shape2 = sh2.extensionObject()->getTopoShapePtr()->getShape();
					if (shape1.IsNull() || shape2.IsNull())
						throw Py::RuntimeError("Cannot add null shape");
					if (shape2.ShapeType() == TopAbs_FACE) {
						if (shape1.ShapeType() == TopAbs_EDGE) {
							splitShape.Add(TopoDS::Edge(shape1), TopoDS::Face(shape2));
						}
						else if (shape1.ShapeType() == TopAbs_WIRE) {
							splitShape.Add(TopoDS::Wire(shape1), TopoDS::Face(shape2));
						}
						else if (shape1.ShapeType() == TopAbs_COMPOUND) {
							splitShape.Add(TopoDS::Compound(shape1), TopoDS::Face(shape2));
						}
						else {
							throw Py::TypeError("First item in tuple must be Edge, Wire or Compound");
						}
					}
					else if (shape2.ShapeType() == TopAbs_EDGE) {
						if (shape1.ShapeType() == TopAbs_EDGE) {
							splitShape.Add(TopoDS::Edge(shape1), TopoDS::Edge(shape2));
						}
						else {
							throw Py::TypeError("First item in tuple must be Edge");
						}
					}
					else {
						throw Py::TypeError("Second item in tuple must be Face or Edge");
					}
				}

				splitShape.Build();
				const TopTools_ListOfShape& d = splitShape.DirectLeft();
				const TopTools_ListOfShape& l = splitShape.Left();

				Py::List list1;
				for (TopTools_ListIteratorOfListOfShape it(d); it.More(); it.Next()) {
					list1.append(shape2pyshape(it.Value()));
				}

				Py::List list2;
				for (TopTools_ListIteratorOfListOfShape it(l); it.More(); it.Next()) {
					list2.append(shape2pyshape(it.Value()));
				}

				Py::Tuple tuple(2);
				tuple.setItem(0, list1);
				tuple.setItem(1, list2);
				return tuple;
			}
			catch (Standard_Failure& e) {
				throw Py::Exception(PartExceptionOCCError, e.GetMessageString());
			}
		}
		Py::Object makeWireString(const Py::Tuple& args)
		{
#ifdef FCUseFreeType
			PyObject *intext;
			const char* dir;
			const char* fontfile;
			const char* fontspec;
			bool useFontSpec = false;
			double height;
			double track = 0;

			Py_UNICODE *unichars;
			Py_ssize_t pysize;

			PyObject *CharList;

			if (PyArg_ParseTuple(args.ptr(), "Ossd|d", &intext,                               // compatibility with old version
				&dir,
				&fontfile,
				&height,
				&track)) {
				useFontSpec = false;
			}
			else {
				PyErr_Clear();
				if (PyArg_ParseTuple(args.ptr(), "Osd|d", &intext,
					&fontspec,
					&height,
					&track)) {
					useFontSpec = true;
				}
				else {
					throw Py::TypeError("** makeWireString bad args.");
				}
			}

#if PY_MAJOR_VERSION >= 3
			//FIXME: Test this!
			if (PyBytes_Check(intext)) {
				PyObject *p = Base::PyAsUnicodeObject(PyBytes_AsString(intext));
#else
			if (PyString_Check(intext)) {
				PyObject *p = Base::PyAsUnicodeObject(PyString_AsString(intext));
#endif
				if (!p) {
					throw Py::TypeError("** makeWireString can't convert PyString.");
				}
				pysize = PyUnicode_GetSize(p);
				unichars = PyUnicode_AS_UNICODE(p);
			}
			else if (PyUnicode_Check(intext)) {
				pysize = PyUnicode_GetSize(intext);
				unichars = PyUnicode_AS_UNICODE(intext);
			}
			else {
				throw Py::TypeError("** makeWireString bad text parameter");
			}

			try {
				if (useFontSpec) {
					CharList = FT2FC(unichars, pysize, fontspec, height, track);
				}
				else {
					CharList = FT2FC(unichars, pysize, dir, fontfile, height, track);
				}
			}
			catch (Standard_DomainError) {                                      // Standard_DomainError is OCC error.
				throw Py::Exception(PartExceptionOCCDomainError, "makeWireString failed - Standard_DomainError");
			}
			catch (std::runtime_error& e) {                                     // FT2 or FT2FC errors
				throw Py::Exception(PartExceptionOCCError, e.what());
			}

			return Py::asObject(CharList);
#else
			throw Py::RuntimeError("FreeCAD compiled without FreeType support! This method is disabled...");
#endif
			}
		Py::Object exportUnits(const Py::Tuple& args)
		{
			char* unit = 0;
			if (!PyArg_ParseTuple(args.ptr(), "|s", &unit))
				throw Py::Exception();

			if (unit) {
				if (strcmp(unit, "M") == 0 || strcmp(unit, "MM") == 0 || strcmp(unit, "IN") == 0) {
					if (!Interface_Static::SetCVal("write.iges.unit", unit)) {
						throw Py::RuntimeError("Failed to set 'write.iges.unit'");
					}
					if (!Interface_Static::SetCVal("write.step.unit", unit)) {
						throw Py::RuntimeError("Failed to set 'write.step.unit'");
					}
				}
				else {
					throw Py::ValueError("Wrong unit");
				}
			}

			Py::Dict dict;
			dict.setItem("write.iges.unit", Py::String(Interface_Static::CVal("write.iges.unit")));
			dict.setItem("write.step.unit", Py::String(Interface_Static::CVal("write.step.unit")));
			return dict;
		}
		Py::Object setStaticValue(const Py::Tuple& args)
		{
			char *name, *cval;
			if (PyArg_ParseTuple(args.ptr(), "ss", &name, &cval)) {
				if (!Interface_Static::SetCVal(name, cval)) {
					std::stringstream str;
					str << "Failed to set '" << name << "'";
					throw Py::RuntimeError(str.str());
				}
				return Py::None();
			}

			PyErr_Clear();
			PyObject* index_or_value;
			if (PyArg_ParseTuple(args.ptr(), "sO", &name, &index_or_value)) {
#if PY_MAJOR_VERSION >= 3
				if (PyLong_Check(index_or_value)) {
					int ival = (int)PyLong_AsLong(index_or_value);
#else
				if (PyInt_Check(index_or_value)) {
					int ival = (int)PyInt_AsLong(index_or_value);
#endif
					if (!Interface_Static::SetIVal(name, ival)) {
						std::stringstream str;
						str << "Failed to set '" << name << "'";
						throw Py::RuntimeError(str.str());
					}
					return Py::None();
				}
				else if (PyFloat_Check(index_or_value)) {
					double rval = PyFloat_AsDouble(index_or_value);
					if (!Interface_Static::SetRVal(name, rval)) {
						std::stringstream str;
						str << "Failed to set '" << name << "'";
						throw Py::RuntimeError(str.str());
					}
					return Py::None();
				}
				}

			throw Py::TypeError("First argument must be string and must be either string, int or float");
			}
		Py::Object cast_to_shape(const Py::Tuple& args)
		{
			PyObject *object;
			if (PyArg_ParseTuple(args.ptr(), "O!", &(Part::TopoShapePy::Type), &object)) {
				TopoShape* ptr = static_cast<TopoShapePy*>(object)->getTopoShapePtr();
				TopoDS_Shape shape = ptr->getShape();
				if (!shape.IsNull()) {
					TopAbs_ShapeEnum type = shape.ShapeType();
					switch (type)
					{
					case TopAbs_COMPOUND:
						return Py::asObject(new TopoShapeCompoundPy(new TopoShape(shape)));
					case TopAbs_COMPSOLID:
						return Py::asObject(new TopoShapeCompSolidPy(new TopoShape(shape)));
					case TopAbs_SOLID:
						return Py::asObject(new TopoShapeSolidPy(new TopoShape(shape)));
					case TopAbs_SHELL:
						return Py::asObject(new TopoShapeShellPy(new TopoShape(shape)));
					case TopAbs_FACE:
						return Py::asObject(new TopoShapeFacePy(new TopoShape(shape)));
					case TopAbs_WIRE:
						return Py::asObject(new TopoShapeWirePy(new TopoShape(shape)));
					case TopAbs_EDGE:
						return Py::asObject(new TopoShapeEdgePy(new TopoShape(shape)));
					case TopAbs_VERTEX:
						return Py::asObject(new TopoShapeVertexPy(new TopoShape(shape)));
					case TopAbs_SHAPE:
						return Py::asObject(new TopoShapePy(new TopoShape(shape)));
					default:
						break;
					}
				}
				else {
					throw Py::Exception(PartExceptionOCCError, "empty shape");
				}
			}

			throw Py::Exception();
		}
		Py::Object getSortedClusters(const Py::Tuple& args)
		{
			PyObject *obj;
			if (!PyArg_ParseTuple(args.ptr(), "O", &obj)) {
				throw Py::Exception(PartExceptionOCCError, "list of edges expected");
			}

			Py::Sequence list(obj);
			std::vector<TopoDS_Edge> edges;
			for (Py::Sequence::iterator it = list.begin(); it != list.end(); ++it) {
				PyObject* item = (*it).ptr();
				if (PyObject_TypeCheck(item, &(Part::TopoShapePy::Type))) {
					const TopoDS_Shape& sh = static_cast<Part::TopoShapePy*>(item)->getTopoShapePtr()->getShape();
					if (sh.ShapeType() == TopAbs_EDGE)
						edges.push_back(TopoDS::Edge(sh));
					else {
						throw Py::TypeError("shape is not an edge");
					}
				}
				else {
					throw Py::TypeError("item is not a shape");
				}
			}

			Edgecluster acluster(edges);
			tEdgeClusterVector aclusteroutput = acluster.GetClusters();

			Py::List root_list;
			for (tEdgeClusterVector::iterator it = aclusteroutput.begin(); it != aclusteroutput.end(); ++it) {
				Py::List add_list;
				for (tEdgeVector::iterator it1 = (*it).begin(); it1 != (*it).end(); ++it1) {
					add_list.append(Py::Object(new TopoShapeEdgePy(new TopoShape(*it1)), true));
				}
				root_list.append(add_list);
			}

			return root_list;
		}
		Py::Object sortEdges(const Py::Tuple& args)
		{
			PyObject *obj;
			if (!PyArg_ParseTuple(args.ptr(), "O", &obj)) {
				throw Py::TypeError("list of edges expected");
			}

			Py::Sequence list(obj);
			std::list<TopoDS_Edge> edges;
			for (Py::Sequence::iterator it = list.begin(); it != list.end(); ++it) {
				PyObject* item = (*it).ptr();
				if (PyObject_TypeCheck(item, &(Part::TopoShapePy::Type))) {
					const TopoDS_Shape& sh = static_cast<Part::TopoShapePy*>(item)->getTopoShapePtr()->getShape();
					if (sh.ShapeType() == TopAbs_EDGE)
						edges.push_back(TopoDS::Edge(sh));
					else {
						throw Py::TypeError("shape is not an edge");
					}
				}
				else {
					throw Py::TypeError("item is not a shape");
				}
			}

			std::list<TopoDS_Edge> sorted = sort_Edges(Precision::Confusion(), edges);
			Py::List sorted_list;
			for (std::list<TopoDS_Edge>::iterator it = sorted.begin(); it != sorted.end(); ++it) {
				sorted_list.append(Py::Object(new TopoShapeEdgePy(new TopoShape(*it)), true));
			}

			return sorted_list;
		}
		Py::Object sortEdges2(const Py::Tuple& args)
		{
			PyObject *obj;
			if (!PyArg_ParseTuple(args.ptr(), "O", &obj)) {
				throw Py::Exception(PartExceptionOCCError, "list of edges expected");
			}

			Py::Sequence list(obj);
			std::list<TopoDS_Edge> edges;
			for (Py::Sequence::iterator it = list.begin(); it != list.end(); ++it) {
				PyObject* item = (*it).ptr();
				if (PyObject_TypeCheck(item, &(Part::TopoShapePy::Type))) {
					const TopoDS_Shape& sh = static_cast<Part::TopoShapePy*>(item)->getTopoShapePtr()->getShape();
					if (sh.ShapeType() == TopAbs_EDGE)
						edges.push_back(TopoDS::Edge(sh));
					else {
						throw Py::TypeError("shape is not an edge");
					}
				}
				else {
					throw Py::TypeError("item is not a shape");
				}
			}

			Py::List root_list;
			while (edges.size()) {
				std::list<TopoDS_Edge> sorted = sort_Edges(Precision::Confusion(), edges);
				Py::List sorted_list;
				for (std::list<TopoDS_Edge>::iterator it = sorted.begin(); it != sorted.end(); ++it) {
					sorted_list.append(Py::Object(new TopoShapeEdgePy(new TopoShape(*it)), true));
				}
				root_list.append(sorted_list);
			}
			return root_list;
		}
		Py::Object toPythonOCC(const Py::Tuple& args)
		{
			PyObject *pcObj;
			if (!PyArg_ParseTuple(args.ptr(), "O!", &(TopoShapePy::Type), &pcObj))
				throw Py::Exception();

			try {
				TopoDS_Shape* shape = new TopoDS_Shape();
				(*shape) = static_cast<TopoShapePy*>(pcObj)->getTopoShapePtr()->getShape();
				PyObject* proxy = 0;
				proxy = Base::Interpreter().createSWIGPointerObj("OCC.TopoDS", "TopoDS_Shape *", (void*)shape, 1);
				return Py::asObject(proxy);
			}
			catch (const Base::Exception& e) {
				throw Py::Exception(PartExceptionOCCError, e.what());
			}
		}
		Py::Object fromPythonOCC(const Py::Tuple& args)
		{
			PyObject *proxy;
			if (!PyArg_ParseTuple(args.ptr(), "O", &proxy))
				throw Py::Exception();

			void* ptr;
			try {
				TopoShape* shape = new TopoShape();
				Base::Interpreter().convertSWIGPointerObj("OCC.TopoDS", "TopoDS_Shape *", proxy, &ptr, 0);
				TopoDS_Shape* s = reinterpret_cast<TopoDS_Shape*>(ptr);
				shape->setShape(*s);
				return Py::asObject(new TopoShapePy(shape));
			}
			catch (const Base::Exception& e) {
				throw Py::Exception(PartExceptionOCCError, e.what());
			}
		}

		/*loads an obj File get topo_shape*/
		bool LoadOBJ2(std::istream &rstrIn, TopoShape &resultShape, const Standard_Real facePrecision){
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
				std::shared_ptr<TopoShape> shapePtr(new TopoShape());
				
				shapePtr->setFaces(validPoints, validFacets, facePrecision);
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

				resultShape= getTopoShapeByPointsAndFaces(validPoints, validFacets);
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
				throw Py::Exception(PartExceptionOCCError, e.GetMessageString());
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

					std::unique_ptr<FaceMaker> fm
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



		};

	PyObject* initModule()
	{
		return (new Module)->module().ptr();
	}


		} // namespace Part
