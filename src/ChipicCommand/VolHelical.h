#pragma  once
#include "Model.h"
#include "Point.h"
class VolHelical :public Model
{

public:
	VolHelical();
	~VolHelical();

public:
	std::string toCommand() override;
	bool fromCommand(const std::string& command);

public:
	Point point1, point2, point3;
	//设置内外半径,螺距和宽度
	std::string value4,value5,value6,value7;
	void setRadius(const std::string& value4, const std::string& value5,const std::string& value6,const std::string& value7);
};