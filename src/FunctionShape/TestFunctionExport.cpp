#include "TestFunctionExport.h"

#include "InitVtk.hpp"
#include <vtkRenderer.h>
#include <vtkActor.h>
#include <vtkRenderWindow.h>
#include <vtkRenderWindowInteractor.h>
#include <vtkPolyDataMapper.h>
#include <vtkSphere.h>
#include <vtkSampleFunction.h>
#include <vtkContourFilter.h>
#include <vtkProperty.h>
#include <vtkNew.h>
#include <vtkPointData.h>
#include <vtkCellData.h>
#include <vtkTriangleFilter.h>
#include <vtkCell.h>
#include <vtkSTLWriter.h>
# include <TopTools_MapOfShape.hxx>
# include <TopoDS.hxx>
# include <TopoDS_Compound.hxx>
# include <TopoDS_Iterator.hxx>
# include <TopoDS_Solid.hxx>
# include <TopoDS_Vertex.hxx>
# include <TopExp.hxx>
# include <TopExp_Explorer.hxx>
# include <TopTools_ListIteratorOfListOfShape.hxx>
# include <BRepLib.hxx>
# include <BSplCLib.hxx>
# include <Bnd_Box.hxx>
# include <BRep_Builder.hxx>
# include <BRep_Tool.hxx>
# include <BRepAdaptor_Curve.hxx>
# include <BRepAdaptor_CompCurve.hxx>
# include <BRepAdaptor_HCurve.hxx>
# include <BRepAdaptor_HCompCurve.hxx>
# include <BRepAdaptor_Surface.hxx>
# include <BRepAlgoAPI_Common.hxx>
# include <BRepAlgoAPI_Cut.hxx>
# include <BRepAlgoAPI_Fuse.hxx>
# include <BRepAlgo_Fuse.hxx>
# include <BRepAlgoAPI_Section.hxx>
# include <BRepBndLib.hxx>
# include <BRepBuilderAPI_FindPlane.hxx>
# include <BRepLib_FindSurface.hxx>
# include <BRepBuilderAPI_GTransform.hxx>
# include <BRepBuilderAPI_MakeEdge.hxx>
# include <BRepBuilderAPI_MakeFace.hxx>
# include <BRepBuilderAPI_MakePolygon.hxx>
# include <BRepBuilderAPI_MakeSolid.hxx>
# include <BRepBuilderAPI_MakeVertex.hxx>
# include <BRepBuilderAPI_MakeWire.hxx>
# include <BRepBuilderAPI_MakeShell.hxx>
# include <BRepBuilderAPI_NurbsConvert.hxx>
# include <BRepBuilderAPI_FaceError.hxx>
# include <BRepBuilderAPI_Copy.hxx>
# include <BRepBuilderAPI_Transform.hxx>
# include <BRepCheck_Analyzer.hxx>
# include <BRepCheck_ListIteratorOfListOfStatus.hxx>
# include <BRepCheck_Result.hxx>
# include <BRepClass_FaceClassifier.hxx>
# include <BRepFilletAPI_MakeFillet.hxx>
# include <BRepGProp.hxx>
# include <BRepMesh_IncrementalMesh.hxx>
# include <BRepMesh_Triangle.hxx>
# include <BRepMesh_Edge.hxx>
# include <BRepOffsetAPI_MakeThickSolid.hxx>
# include <BRepOffsetAPI_MakeOffsetShape.hxx>
# include <BRepOffsetAPI_MakeOffset.hxx>
# include <BRepOffsetAPI_MakePipe.hxx>
# include <BRepOffsetAPI_MakePipeShell.hxx>
# include <BRepOffsetAPI_Sewing.hxx>
# include <BRepOffsetAPI_ThruSections.hxx>
# include <BRepPrimAPI_MakePrism.hxx>
# include <BRepPrimAPI_MakeRevol.hxx>
# include <BRepTools.hxx>
# include <BRepTools_ReShape.hxx>
# include <BRepTools_ShapeSet.hxx>
# include <BRepTools_WireExplorer.hxx>
# include <BRepFill_CompatibleWires.hxx>
#include <BRepPrimAPI_MakeBox.hxx>
#include "MyFunction.h"

TestExport::VtkData TestExport::creatVtkData()
{
	//创建一个隐函数
	MyFuntion* function;
	function = new MyFuntion1();

	//对函数进行采样
	vtkNew<vtkSampleFunction> sample;
	sample->SetSampleDimensions(20, 20, 20);
	sample->SetImplicitFunction(function);
	//设置函数采样范围
	double value = 2.0;
	double xmin = -value, xmax = value, ymin = -value, ymax = value,
		zmin = -value, zmax = value;
	sample->SetModelBounds(xmin, xmax, ymin, ymax, zmin, zmax);
	sample->CappingOn();
	sample->SetCapValue(0);

	//提取等值面
	vtkNew<vtkContourFilter> filter;
	filter->SetInputConnection(sample->GetOutputPort());
	filter->SetValue(0, 0);
	filter->Update();

	vtkSmartPointer<vtkSTLWriter> stlWriter =
		vtkSmartPointer<vtkSTLWriter>::New();
	stlWriter->SetFileName("contour");
	stlWriter->SetInputConnection(filter->GetOutputPort());
	stlWriter->Write();


	vtkNew<vtkTriangleFilter> triangleFilter;
	triangleFilter->SetInputData(filter->GetOutput());
	triangleFilter->Update();

	stlWriter->SetFileName("triangle");
	stlWriter->SetInputConnection(triangleFilter->GetOutputPort());
	stlWriter->Write();

	auto data = triangleFilter->GetOutput();

	auto pointData = data->GetPoints();
	std::vector<Point> points;
	points.reserve(pointData->GetNumberOfPoints());

	Point Temp;
	double p[3];
	for (int i = 0; i < pointData->GetNumberOfPoints(); i++)
	{
		pointData->GetPoint(i, p);
		Temp.x = p[0];
		Temp.y = p[1];
		Temp.z = p[2];
		points.push_back(Temp);
	}

	auto faceCount = data->GetNumberOfPolys();

	std::vector<Face> faces;
/*	auto faceCount = cellArray->GetNumberOfCells();*/
	faces.reserve(faceCount);
	Face temp;
	for (int i = 0;i < faceCount;i++)
	{
		auto idlist = data->GetCell(i)->GetPointIds();
		temp.p1 = idlist->GetId(0);
		temp.p2 = idlist->GetId(1);
		temp.p3 = idlist->GetId(2);
		faces.push_back(temp);
	}

	VtkData vd;
	vd.faces = faces;
	vd.points = points;
	
	return vd;
}

TopoDS_Shape TestExport::creatTopDS_shaPe()
{

	Timer ti;
	ti.start();
	//创建一个隐函数
	MyFuntion* function;
	function = new MyFuntion1();

	//对函数进行采样
	vtkNew<vtkSampleFunction> sample;
	sample->SetSampleDimensions(20, 20, 20);
	sample->SetImplicitFunction(function);
	//设置函数采样范围
	double value = 2.0;
	double xmin = -value, xmax = value, ymin = -value, ymax = value,
		zmin = -value, zmax = value;
	sample->SetModelBounds(xmin, xmax, ymin, ymax, zmin, zmax);
	sample->CappingOn();
	sample->SetCapValue(0);

	//提取等值面
	vtkNew<vtkContourFilter> filter;
	filter->SetInputConnection(sample->GetOutputPort());
	filter->SetValue(0, 0);
	filter->Update();

	vtkSmartPointer<vtkSTLWriter> stlWriter =
		vtkSmartPointer<vtkSTLWriter>::New();
	stlWriter->SetFileName("contour");
	stlWriter->SetInputConnection(filter->GetOutputPort());
	stlWriter->Write();


	vtkNew<vtkTriangleFilter> triangleFilter;
	triangleFilter->SetInputData(filter->GetOutput());
	triangleFilter->Update();

	stlWriter->SetFileName("triangle");
	stlWriter->SetInputConnection(triangleFilter->GetOutputPort());
	stlWriter->Write();

	auto data = triangleFilter->GetOutput();

	auto pointData = data->GetPoints();


	auto faceCount = data->GetNumberOfPolys();


	gp_XYZ p1, p2, p3;
	TopoDS_Vertex Vertex1, Vertex2, Vertex3;
	TopoDS_Face newFace;
	TopoDS_Wire newWire;


	TopoDS_Compound aComp;
	BRep_Builder BuildTool;
	BuildTool.MakeCompound(aComp);

	double p[3];

	for (int i = 0; i < faceCount; i++) {

		auto idlist = data->GetCell(i)->GetPointIds();

		pointData->GetPoint(idlist->GetId(0), p);
		p1.SetCoord(p[0], p[1],p[2]);
		pointData->GetPoint(idlist->GetId(1), p);
		p2.SetCoord(p[0], p[1], p[2]);
		pointData->GetPoint(idlist->GetId(2), p);
		p3.SetCoord(p[0], p[1], p[2]);

		if ((!(p1.IsEqual(p2, 0.0))) && (!(p1.IsEqual(p3, 0.0)))) {
			Vertex1 = BRepBuilderAPI_MakeVertex(p1);
			Vertex2 = BRepBuilderAPI_MakeVertex(p2);
			Vertex3 = BRepBuilderAPI_MakeVertex(p3);

			newWire = BRepBuilderAPI_MakePolygon(Vertex1, Vertex2, Vertex3, Standard_True);
			if (!newWire.IsNull()) {
				newFace = BRepBuilderAPI_MakeFace(newWire);
				if (!newFace.IsNull())
					BuildTool.Add(aComp, newFace);
			}
		}
	}

	BRepBuilderAPI_Sewing aSewingTool;
	aSewingTool.Init(1.0e-06, Standard_True);

	aSewingTool.Load(aComp);
	aSewingTool.Perform();


	TopExp_Explorer anExp(aSewingTool.SewedShape(), TopAbs_SHELL);
	BRepBuilderAPI_MakeSolid mkSolid;

	int count = 0;
	for (; anExp.More(); anExp.Next()) {
		++count;
		mkSolid.Add(TopoDS::Shell(anExp.Current()));
	}

	TopoDS_Solid solid = mkSolid.Solid();
	BRepLib::OrientClosedSolid(solid);


	//test
	gp_Pnt pn1(2,2,2), pn2(-2,-2,-2);
	BRepPrimAPI_MakeBox box(pn1,pn2);
	box.Build();

	gp_Pnt pn3(1, 1, 1), pn4(-1, -1, -1);
	BRepPrimAPI_MakeBox box1(pn3, pn4);
	box1.Build();

	BRepAlgoAPI_Cut cut(box.Solid(), box1.Solid());
	cut.Build();


	BRepAlgoAPI_Cut cut2(solid, cut.Shape());
	cut2.Build();
	ti.end();

	return solid;

}

Timer::Timer(const std::string& name)
{
	this->name = name;

}

void Timer::start()
{
	startClock	= clock();
}

void Timer::end()
{
	endClock = clock();
	std::cerr << "Timer " << name<< ":" << double(endClock - startClock)/1000 << "s" << std::endl;
}
