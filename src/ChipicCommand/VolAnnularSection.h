#pragma  once
#include "Model.h"
#include "Point.h"
class VolAnnularSection :public Model
{

public:
	VolAnnularSection();
	~VolAnnularSection();

public:
	std::string toCommand() override;
	bool fromCommand(const std::string& command);

public:
	Point point1, point2, point3, point4;
	//…Ë÷√ƒ⁄Õ‚∞Îæ∂
	std::string value4, value5;
	void setRadius(const std::string& value4, const std::string& value5);
};