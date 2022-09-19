#include "FunctionShape.h"
#include "MyFunction.h"

#include <vtkPolyData.h>
#include <vtkSampleFunction.h>
#include <vtkNew.h>
#include <vtkContourFilter.h>
#include <vtkImplicitFunction.h>

#include <TopoDS_Face.hxx>
#include <TopoDS_Wire.hxx>
#include <TopoDS_Vertex.hxx>
#include <TopoDS_Compound.hxx>
#include <BRep_Builder.hxx>
#include <BRepBuilderAPI_MakeVertex.hxx>
#include <BRepBuilderAPI_MakePolygon.hxx>
#include <BRepBuilderAPI_MakeFace.hxx>
#include <BRepBuilderAPI_Sewing.hxx>
#include <TopExp_Explorer.hxx>
#include <BRepBuilderAPI_MakeSolid.hxx>
#include <BRepLib.hxx>
#include <TopoDS.hxx>
#include <BRepPrimAPI_MakeBox.hxx>
#include <BRepAlgoAPI_Cut.hxx>
# include <BRepPrimAPI_MakeCylinder.hxx>
#include "Function.h"

namespace FS {

	class FunctionShapeD {
	public:
		FunctionShapeD():dx(20), dy(20), dz(20) {};
	public:
		TopoDS_Shape shape;
		//函数采样率
		unsigned int dx, dy, dz;
		//函数边界
		Bounds bounds;
		//边界误差  
		//处理非封闭函数时需要扩大的边界范围
		//扩大边界范围之后用标准边界进行布尔运算
		double rx, ry, rz;

		vtkNew<vtkContourFilter> contourFilter;
		
		//函数对象
		FunctionString* function = nullptr;

	};

}

void FS:: FunctionShapeCylinder::setFunction(const std::string& function)
{
	delete d->function;
	d->function = new FunctionStringClinder();
	d->function->setFunctionString(function);
}

FS::FunctionShapeCylinder::FunctionShapeCylinder()
	:rMax(0),rMin(0),tMin(0),tMax(0),zMin(0),zMax(0)
{

}

void FS::FunctionShapeCylinder::setBoundsCylinder(const double& rmin, const double& rmax, const double& tmin, const double& tmax, const double& zmin, const double& zmax)
{
	Bounds bounds;
	rMin = rmin;
	rMax = rmax;
	tMin = tmin;
	tMax = tmax;
	zMin = zmin;
	zMax = zmax;

	bounds.xmax = rMax;
	bounds.ymax = rMax;
	bounds.xmin = -rMax;
	bounds.ymin = -rMax;
	bounds.zmin = zMin;
	bounds.zmax = zMax;

	setBounds(bounds);

}

TopoDS_Shape FS::FunctionShapeCylinder::disposBounds(TopoDS_Solid sd)
{
	//边界厚度
//需要确保多余的部分全部被切掉
	double hx = 2 * d->rx;
	double hy = 2 * d->ry;
	double hz = 2 * d->rz;

	//生成边界盒子
	Bounds& bounds = d->bounds;
	gp_Pnt p1(bounds.xmin - hx, bounds.ymin - hy, bounds.zmin - hz);
	gp_Pnt p2(bounds.xmax + hx, bounds.ymax + hy, bounds.zmax + hz);
	BRepPrimAPI_MakeBox box(p1, p2);
	box.Build();

	gp_Pnt p(0, 0, 0);
	gp_Dir dir(0, 0, 1);
	BRepPrimAPI_MakeCylinder mkCyl(gp_Ax2(p, dir),d->bounds.xmax ,d->bounds.zmax, M_PI );
	mkCyl.Build();

	BRepAlgoAPI_Cut cut(box.Solid(), mkCyl.Solid());
	cut.Build();

	//使用边界盒子剪切函数
	BRepAlgoAPI_Cut cut2(sd, cut.Shape());
	cut2.Build();

	return cut2.Shape();
}

FS::FunctionShape::FunctionShape()
{
	d = new FunctionShapeD;

	autoBoundsUpRange();
}

FS::FunctionShape::~FunctionShape()
{

}

void FS::FunctionShape::buildShape()
{
	Timer pt("GeneratePolyData");
	pt.start();
	auto polydata = generatePolyData();
	pt.end();

	Timer ps("sewingPolydata");
	ps.start();
	d->shape = sewingPolydata(polydata);
	ps.end();

	Timer po("shapeToSolid");
	po.start();
	auto solid = shapeToSolid(d->shape);
	po.end();

	Timer pd("disposBounds");
	pd.start();
	d->shape = disposBounds(solid);
	pd.end();
}


TopoDS_Shape FS::FunctionShape::getShape()
{
	return d->shape;
}

void FS::FunctionShape::setBounds(const Bounds& b)
{
	d->bounds = b;
	autoBoundsUpRange();
}

void FS::FunctionShape::setSamplingRate(const unsigned int& x, const unsigned int& y, const unsigned int& z)
{
	d->dx = x;
	d->dy = y;
	d->dz = z;
	autoBoundsUpRange();
}

void FS::FunctionShape::setFunction(const std::string& function)
{
	delete d->function;
 	d->function = new FunctionStringClinder();
	d->function->setFunctionString(function);
}

vtkPolyData* FS::FunctionShape::generatePolyData()
{
	//创建一个隐函数
// 	if(!d->function)
// 		d->function = new MyFuntion4();

	//对函数进行采样
	vtkNew<vtkSampleFunction> sample;
	sample->SetSampleDimensions(d->dx,d->dy,d->dz);
	sample->SetImplicitFunction(d->function);
	//设置函数采样范围
	Bounds& bounds = d->bounds;
	sample->SetModelBounds(bounds.xmin - d->rx, bounds.xmax + d->rx,bounds.ymin - d->ry,bounds.ymax + d->ry,bounds.zmin - d->rz,bounds.zmax + d->rz);
	sample->CappingOn();
	sample->SetCapValue(0);

	//提取等值面
	d->contourFilter->SetInputConnection(sample->GetOutputPort());
	d->contourFilter->SetValue(0, 0);
	d->contourFilter->Update();

	return d->contourFilter->GetOutput();
}

TopoDS_Shape FS::FunctionShape::sewingPolydata(vtkPolyData* polydata)
{
	auto pointData = polydata->GetPoints();
	auto faceCount = polydata->GetNumberOfPolys();

	gp_XYZ p1, p2, p3;
	TopoDS_Vertex Vertex1, Vertex2, Vertex3;
	TopoDS_Face newFace;
	TopoDS_Wire newWire;


	TopoDS_Compound aComp;
	BRep_Builder BuildTool;
	BuildTool.MakeCompound(aComp);

	double p[3];

	for (int i = 0; i < faceCount; i++) {

		auto idlist = polydata->GetCell(i)->GetPointIds();

		pointData->GetPoint(idlist->GetId(0), p);
		p1.SetCoord(p[0], p[1], p[2]);
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

	return aSewingTool.SewedShape();
}

TopoDS_Solid FS::FunctionShape::shapeToSolid(TopoDS_Shape shape)
{
	TopExp_Explorer anExp(shape, TopAbs_SHELL);
	BRepBuilderAPI_MakeSolid mkSolid;

	int count = 0;
	for (; anExp.More(); anExp.Next()) {
		++count;
		mkSolid.Add(TopoDS::Shell(anExp.Current()));
	}

	TopoDS_Solid solid = mkSolid.Solid();
	BRepLib::OrientClosedSolid(solid);

	return solid;
}

TopoDS_Shape FS::FunctionShape::disposBounds(TopoDS_Solid sd)
{
	//边界厚度
	//需要确保多余的部分全部被切掉
	double hx = 2 * d->rx;
	double hy = 2 * d->ry;
	double hz = 2 * d->rz;
	
	//生成边界盒子
	Bounds& bounds = d->bounds;
	gp_Pnt p1(bounds.xmin - hx, bounds.ymin - hy, bounds.zmin - hz);
	gp_Pnt p2(bounds.xmax + hx, bounds.ymax + hy,bounds.zmax + hz);
	BRepPrimAPI_MakeBox box(p1, p2);
	box.Build();

	gp_Pnt p3(bounds.xmin , bounds.ymin , bounds.zmin );
	gp_Pnt p4(bounds.xmax, bounds.ymax , bounds.zmax);
	BRepPrimAPI_MakeBox box1(p3, p4);
	box1.Build();

	BRepAlgoAPI_Cut cut(box.Solid(), box1.Solid());
	cut.Build();

	//使用边界盒子剪切函数
	BRepAlgoAPI_Cut cut2(sd, cut.Shape());
	cut2.Build();

	return cut2.Shape();
}

void FS::FunctionShape::autoBoundsUpRange()
{
	double scaler = 2;//扩大比例

	Bounds& bounds = d->bounds;
	d->rx = (bounds.xmax - bounds.xmin) / d->dx * scaler;
	d->ry = (bounds.ymax - bounds.ymin) / d->dy * scaler;
	d->rz = (bounds.zmax - bounds.zmin) / d->dz * scaler;
}


FS::Timer::Timer(const std::string& name)
{
	this->name = name;

}

void FS::Timer::start()
{
	startClock = clock();
}

void FS::Timer::end()
{
	endClock = clock();
	std::cerr << "Timer " << name << ":" << double(endClock - startClock) / 1000 << "s" << std::endl;
}

