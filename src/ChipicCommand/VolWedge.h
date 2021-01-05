#pragma  once
#include "Model.h"
#include "Point.h"
class VolWedge :public Model
{

public:
	VolWedge();
	~VolWedge();

public:
	std::string toCommand() override;
	bool fromCommand(const std::string& command);

public:
	Point point1, point2, point3, point4, point5, point6;
};