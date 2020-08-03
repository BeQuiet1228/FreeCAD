#include "VolSpherical.h"

VolSpherical::VolSpherical()
{

}
VolSpherical::~VolSpherical()
{

}
std::string VolSpherical::toCommand()
{
	if (notOutputCommand || name == "")
		return "";
	/*
	[1] 判断点是否有名称，有名称则不生成点的命令
	[2] 没有名称则生成一个名称，并生成一个对应的名称
	[3] 根据点的名称生成体的命令
	*/

	std::string cmd = "";
	if (point1.name == "")
	{
		point1.name = name + ".P";
		cmd += point1.toCommand();
	}

	std::string AreaCmd = "VOLUME " + name + " SPHERICAL " + point1.name + " " + value4+ ";\n";
	cmd += AreaCmd;
	cmd += markGrid.toCommand();

	return cmd;
}

bool VolSpherical::fromCommand(const std::string& command)
{
	return false;
}
void VolSpherical::setRadius(const std::string& value4)
{
	this->value4 = value4;
}