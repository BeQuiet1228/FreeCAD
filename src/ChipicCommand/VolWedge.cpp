#include "VolWedge.h"

VolWedge::VolWedge()
{

}
VolWedge::~VolWedge()
{

}
std::string VolWedge::toCommand()
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
		point1.name = name + ".P1";
		cmd += point1.toCommand();
	}
	if (point2.name == "")
	{
		point2.name = name + ".P2";
		cmd += point2.toCommand();
	}
	if (point3.name == "")
	{
		point3.name = name + ".P3";
		cmd += point3.toCommand();
	}
	if (point4.name == "")
	{
		point4.name = name + ".P4";
		cmd += point4.toCommand();
	}
	if (point5.name == "")
	{
		point5.name = name + ".P5";
		cmd += point5.toCommand();
	}
	if (point6.name == "")
	{
		point6.name = name + ".P6";
		cmd += point6.toCommand();
	}

	std::string AreaCmd = "VOLUME " + name + " WEDGE " + point1.name + " " + point2.name + " " + point3.name + " " + point4.name + " " + point5.name+" "+point6.name+";\n";
	cmd += AreaCmd;
	cmd += markGrid.toCommand();

	return cmd;
}

bool VolWedge::fromCommand(const std::string& command)
{
	return false;
}