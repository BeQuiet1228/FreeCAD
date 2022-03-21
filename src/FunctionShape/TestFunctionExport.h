#pragma  once

#ifdef _FUNCTION_SHAPE_
#define DATA_VISUALIZATION_EXPORT __declspec(dllexport)
#else
#define DATA_VISUALIZATION_EXPORT   __declspec(dllimport)
#endif 

#include <vector>
#include <TopoDS_Shape.hxx>

class DATA_VISUALIZATION_EXPORT Timer {

public:
	Timer(const std::string &name = "");
	void start();
	void end();
private:
	std::string name;
	clock_t startClock, endClock;
};

class  DATA_VISUALIZATION_EXPORT TestExport {
public:
	struct Face 
	{
		int p1, p2, p3;
	};
	struct Point{
		double x, y, z;
	};
	struct VtkData
	{
		std::vector<Face> faces;
		std::vector<Point> points;
	};

public:
	TestExport() = default;
	~TestExport() = default;

	VtkData creatVtkData();
	TopoDS_Shape creatTopDS_shaPe();
};