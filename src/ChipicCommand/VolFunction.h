#pragma  once
#include "Model.h"
#include "Point.h"
class VolFunction :public Model
{

public:
	VolFunction();
	~VolFunction();

public:
	std::string toCommand() override;
	bool fromCommand(const std::string& command);
	//输入表达式，生成函数
	std::string expression;
	std::string setFunction(const std::string& expression);
public:
	Point point1, point2;
};