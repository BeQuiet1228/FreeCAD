#pragma  once
#include "Model.h"
#include "Point.h"
class VolCylinder :public Model
{

public:
	VolCylinder();
	~VolCylinder();

public:
	std::string toCommand() override;
	bool fromCommand(const std::string& command);

public:
	Point point1, point2;
	//∞Îæ∂
	std::string  value4;
	//…Ë÷√∞Îæ∂
	void setRadius(const std::string& value4);
};