#include "AreaRectangular.h"

AreaRectangular::AreaRectangular()
{

}
AreaRectangular::~AreaRectangular()
{

}
std::string AreaRectangular::toCommand()
{
	if (notOutputCommand || name == "")
		return "";
	/*
	[1] 判断点是否有名称，有名称则不生成点的命令
	[2] 没有名称则生成一个名称，并生成一个对应的名称
	[3] 根据点的名称生成面的命令
	*/

	std::string cmd = "";
	if (point1.name == "")
	{
		point1.name = name + ".LO";
		cmd += point1.toCommand();
	}
	if (point2.name == "")
	{
		point2.name = name + ".HI";
		cmd += point2.toCommand();
	}

	std::string AreaCmd = "Area " + name + " RECTANGULAR " + point1.name + " " + point2.name + ";\n";
	cmd += AreaCmd;
	cmd += markGrid.toCommand();

	return cmd;
}

bool AreaRectangular::fromCommand(const std::string& command)
{
	return false;
}