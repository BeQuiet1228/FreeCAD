#pragma  once
#include "Model.h"
#include "Point.h"
class VolConformal :public Model
{

public:
	VolConformal();
	~VolConformal();

public:
	std::string toCommand() override;
	bool fromCommand(const std::string& command);

public:
	Point point1, point2;
};