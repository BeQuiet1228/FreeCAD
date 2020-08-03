#include "VolSpecialCone.h"

VolSpecialCone::VolSpecialCone()
{

}

VolSpecialCone::~VolSpecialCone()
{

}

std::string VolSpecialCone::toCommand()
{
	if (notOutputCommand || name == "")
		return "";
	/*
	[1] 判断点是否有名称，有名称则不生成点的命令
	[2] 没有名称则生成一个名称，并生成一个对应的名称
	[3] 根据点的名称生成环形体的命令
	*/

	std::string cmd = "";
	if (point1.name == "")
	{
		point1.name = name + ".P1";
		cmd += point1.toCommand();
	}
	if (point2.name == "")
	{
		point2.name = name + ".P2";
		cmd += point2.toCommand();
	}

	std::string lineCmd = "VOLUME " + name + " CONE " + point1.name + " " + point2.name + " " + value4 + " " + value5 + ";\n";
	cmd += lineCmd;
	cmd += markGrid.toCommand();

	return cmd;
}

bool VolSpecialCone::fromCommand(const std::string& command)
{
	return false;
}
/**
* @brief VolAnnular::setRadius 设置内外半径的值
* @param const std::string & value4
* @param const std::string & value5
* @return void
*/
void VolSpecialCone::setRadius(const std::string& value4, const std::string& value5)
{
	this->value4 = value4;
	this->value5 = value5;
}