#pragma  once
#include "Model.h"
#include "Point.h"
class AreaConformal :public Model
{

public:
	AreaConformal();
	~AreaConformal();

public:
	std::string toCommand() override;
	bool fromCommand(const std::string& command);

public:
	Point point1, point2;
};