#pragma  once
#include "Model.h"
#include "Point.h"
class AreaRectangular :public Model
{

public:
	AreaRectangular();
	~AreaRectangular();

public:
	std::string toCommand() override;
	bool fromCommand(const std::string& command);

public:
	Point point1, point2;
};