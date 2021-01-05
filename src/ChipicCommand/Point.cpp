#include "Point.h"

Point::Point(){

}

Point::~Point()
{

}

std::string Point::toCommand()
{
	if (notOutputCommand || name == "")
		return "";
	//生成点对应的命令
	std::string cmd = "";
	cmd = "POINT " + name + " " + value1 + "," + value2 + "," + value3 + ";\n";
	//生成mark
	cmd += markGrid.toCommand();
	return cmd;
}

bool Point::fromCommand(const std::string& command)
{
	return false;
}

/**
* @brief Point::setValue 设置坐标的三个值
* @param const std::string & value1
* @param const std::string & value2
* @param const std::string & value3
* @return void
*/
void Point::setValue(const std::string& value1, const std::string& value2, const std::string& value3)
{
	this->value1 = value1;
	this->value2 = value2;
	this->value3 = value3;
}
