#include "VolRhombus.h"

VolRhombus::VolRhombus()
{

}
VolRhombus::~VolRhombus()
{

}
std::string VolRhombus::toCommand()
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
	if (point7.name == "")
	{
		point7.name = name + ".P7";
		cmd += point7.toCommand();
	}
	if (point8.name == "")
	{
		point8.name = name + ".P8";
		cmd += point8.toCommand();
	}

	std::string VolumeCmd = "VOLUME " + name + " RHOMBUS " + point1.name + " " + point2.name + " " + point3.name + " " + point4.name + " " + point5.name + " "+point6.name+" "+point7.name+" "+point8.name+";\n";
	cmd += VolumeCmd;
	cmd += markGrid.toCommand();

	return cmd;
}

bool VolRhombus::fromCommand(const std::string& command)
{
	return false;
}