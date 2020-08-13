#include "VolHelical.h"

VolHelical::VolHelical()
{

}
VolHelical::~VolHelical()
{

}
std::string VolHelical::toCommand()
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
	std::string VolumeCmd = "VOLUME " + name + " HELICAL " + point1.name + " " + point2.name + " " + value4 + " " + value5 + " " + point3.name + " " + value6+" "+value7+ ";\n";
	cmd += VolumeCmd;
	cmd += markGrid.toCommand();

	return cmd;
}

bool VolHelical::fromCommand(const std::string& command)
{
	return false;
}
void VolHelical::setRadius(const std::string& value4, const std::string& value5, const std::string& value6, const std::string& value7)
{
	this->value4 = value4;
	this->value5 = value5;
	this->value6 = value6;
	this->value7 = value7;
}

