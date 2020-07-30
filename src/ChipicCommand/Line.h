#pragma  once
#include "Model.h"
#include "Point.h"
class Line :public Model
{

public:
	Line();
	~Line();

public:
	std::string toCommand() override;
	bool fromCommand(const std::string& command);

public:
	Point point1, point2;
};

