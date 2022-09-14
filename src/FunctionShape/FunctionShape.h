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

	class FunctionShapeD;
	class DATA_VISUALIZATION_EXPORT FunctionShape {
	public:
		FunctionShape();
		~FunctionShape();
		enum Type
		{
			XYZ= 0,
			RTZ =1
		};
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
		void setFunction(const std::string& function,const Type& type = XYZ);
	private:
		//生成vtk多边形数据
		vtkPolyData* generatePolyData();
		//缝补多边形数据
		TopoDS_Shape sewingPolydata(vtkPolyData* polydata);
		//shape数据转换为solid
		TopoDS_Solid shapeToSolid(TopoDS_Shape shape);
		TopoDS_Shape disposBounds(TopoDS_Solid sd);
		//计算边界扩大范围
		void autoBoundsUpRange();
	private:
		FunctionShapeD *d;
	};
}