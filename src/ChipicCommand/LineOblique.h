#pragma  once
#include "Model.h"
#include "Point.h"
class LineOblique :public Model
{

public:
	LineOblique();
	~LineOblique();

public:
	std::string toCommand() override;
	bool fromCommand(const std::string& command);

public:
	Point point1, point2;
};