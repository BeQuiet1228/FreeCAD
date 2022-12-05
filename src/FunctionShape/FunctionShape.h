#pragma once
#ifdef _FUNCTION_SHAPE_
#define DATA_VISUALIZATION_EXPORT __declspec(dllexport)
#else
#define DATA_VISUALIZATION_EXPORT   __declspec(dllimport)
#endif 


#include <TopoDS_Solid.hxx>
#include <TopoDS_Shape.hxx>

class vtkPolyData;
namespace FS {
	
	class DATA_VISUALIZATION_EXPORT Timer {

	public:
		Timer(const std::string& name = "");
		void start();
		void end();
	private:
		std::string name;
		clock_t startClock, endClock;
	};

	class DATA_VISUALIZATION_EXPORT Bounds {

	public:
		Bounds() :xmin(-2.0), xmax(2.0), ymin(-2.0), ymax(2.0), zmin(-2.0), zmax(2.0) {};
		double xmin, xmax, ymin, ymax, zmin, zmax;

	};
	enum CoordinateType
	{
		XYZ = 0,
		RTZ = 1
	};
	class FunctionShapeD;
	class DATA_VISUALIZATION_EXPORT FunctionShape {
	public:
		FunctionShape();
		virtual ~FunctionShape();

	public:
		//构建模型
		void buildShape();
		//获取模型
		TopoDS_Shape getShape();
		//设置边界
		void setBounds(const Bounds& b);
		//设置采样率
		void setSamplingRate(const unsigned int& x, const unsigned int& y, const unsigned int& z);
		//设置函数
		virtual void setFunction(const std::string& function);
	protected:
		//生成vtk多边形数据
		vtkPolyData* generatePolyData();
		//缝补多边形数据
		TopoDS_Shape sewingPolydata(vtkPolyData* polydata);
		//shape数据转换为solid
		TopoDS_Solid shapeToSolid(TopoDS_Shape shape);
		virtual TopoDS_Shape disposBounds(TopoDS_Solid sd);
		//计算边界扩大范围
		void autoBoundsUpRange();
	protected:
		FunctionShapeD *d;
	};

	class DATA_VISUALIZATION_EXPORT FunctionShapeCylinder : public FunctionShape {
	public:
		FunctionShapeCylinder();
	public:
		virtual void setFunction(const std::string& function) override;
		void setBoundsCylinder(const double& rmin, const double& rmax, const double& tmin, const double& tmax, const double& zmin, const double& zmax);
	protected:
		virtual TopoDS_Shape disposBounds(TopoDS_Solid sd) override;
	private:
		double rMin, rMax, tMin, tMax, zMax, zMin;

	};
}