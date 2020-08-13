#include "VolToroidalSection.h"

VolToroidalSection::VolToroidalSection()
{

}
VolToroidalSection::~VolToroidalSection()
{

}
std::string VolToroidalSection::toCommand()
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

	std::string VolumeCmd = "VOLUME " + name + " TOROIDAL_SECTION " + point1.name + " " + point2.name + " " + value4 +" "+ value5 +" " + point3.name + " " + point4.name + ";\n";
	cmd += VolumeCmd;
	cmd += markGrid.toCommand();

	return cmd;
}

bool VolToroidalSection::fromCommand(const std::string& command)
{
	return false;
}
void VolToroidalSection::setRadius(const std::string& value4, const std::string& value5)
{
	this->value4 = value4;
	this->value5 = value5;
}