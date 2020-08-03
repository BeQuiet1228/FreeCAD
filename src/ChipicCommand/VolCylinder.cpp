#include "VolCylinder.h"

VolCylinder::VolCylinder()
{

}

VolCylinder::~VolCylinder()
{

}

std::string VolCylinder::toCommand()
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

	std::string lineCmd = "VOLUME " + name + " CYLINDER " + point1.name + " " + point2.name + " " + value4 + ";\n";
	cmd += lineCmd;
	cmd += markGrid.toCommand();

	return cmd;
}

bool VolCylinder::fromCommand(const std::string& command)
{
	return false;
}
/**
* @brief VolAnnular::setRadius 设置半径的值
* @param const std::string & value4
* @return void
*/
void VolCylinder::setRadius(const std::string& value4)
{
	this->value4 = value4;
}