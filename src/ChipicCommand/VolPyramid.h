#pragma  once
#include "Model.h"
#include "Point.h"
class VolPyramid :public Model
{

public:
	VolPyramid();
	~VolPyramid();

public:
	std::string toCommand() override;
	bool fromCommand(const std::string& command);

public:
	Point point1, point2, point3, point4, point5;
};