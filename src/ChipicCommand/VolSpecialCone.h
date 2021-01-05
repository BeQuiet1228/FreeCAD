#pragma  once
#include "Model.h"
#include "Point.h"
class VolSpecialCone :public Model
{

public:
	VolSpecialCone();
	~VolSpecialCone();

public:
	std::string toCommand() override;
	bool fromCommand(const std::string& command);

public:
	Point point1, point2;
	//内半径，外半径
	std::string  value4, value5;
	//设置内外半径
	void setRadius(const std::string& value4, const std::string& value5);
};