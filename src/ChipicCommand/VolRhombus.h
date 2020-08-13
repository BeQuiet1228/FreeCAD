#pragma  once
#include "Model.h"
#include "Point.h"
class VolRhombus :public Model
{

public:
	VolRhombus();
	~VolRhombus();

public:
	std::string toCommand() override;
	bool fromCommand(const std::string& command);

public:
	Point point1, point2, point3, point4, point5, point6, point7, point8;
};