#pragma  once
#include "Model.h"
#include "Point.h"
class VolSpherical :public Model
{

public:
	VolSpherical();
	~VolSpherical();

public:
	std::string toCommand() override;
	bool fromCommand(const std::string& command);

public:
	Point point1;
	//…Ë÷√∞Îæ∂//
	std::string value4;
	void setRadius(const std::string& value4);
};