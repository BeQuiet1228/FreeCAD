#include "MarkGrid.h"

MarkGrid::MarkGrid()
{
	name = "";
	value1 = value2 = value3 = "";
	check1 = check2 = check3 = false;
	miniMum1 = miniMum2 = miniMum3 = false;
	midMum1 = midMum2 = midMum3 = false;
	maxMum1 = maxMum2 = maxMum3 = false;
}

MarkGrid::~MarkGrid()
{

}

std::string MarkGrid::toCommand()
{
	if (name == "" || notOutputCommand)
		return "";
	std::string cmd = "";
	if (check1)
		cmd += makeMark("X1", value1, miniMum1, midMum1, maxMum1);
	if (check2)
		cmd += makeMark("X2", value2, miniMum2, midMum2, maxMum2);
	if (check3)
		cmd += makeMark("X3", value3, miniMum3, midMum3, maxMum3);

	return cmd;
}

bool MarkGrid::fromCommand(const std::string& command)
{
	return false;
}

/**
* @brief MarkGrid::setValue 设置网格划分的值，调用此函数自动将chcek设置true
* @param const std::string & value1
* @param const std::string & value2
* @param const std::string & value3
* @return void
*/
void MarkGrid::setValue(const std::string& value1, const std::string& value2, const std::string& value3)
{
	this->value1 = value1;
	this->value2 = value2;
	this->value3 = value3;

	this->check1 = this->check2 = this->check3 = true;
}

/**
* @brief MarkGrid::makeMidCommand 生的 min mid max  对应的命令
* @param const bool & mini
* @param const bool & mid
* @param const bool & max
* @return std::string
*/
std::string MarkGrid::makeMidCommand(const bool& mini, const bool& mid, const bool& max)
{
	std::string cmd = "";
	if (mini)
		cmd += "MINIMUM ";
	if (mid)
		cmd += "MIDPOINT ";
	if (max)
		cmd += "MAXMUM ";

	return cmd;
}

/**
* @brief MarkGrid::makeMark 生成一条mark
* @param const std::string & direction 方向
* @param const std::string & value 网格值
* @param const bool & mini 
* @param const bool & mid
* @param const bool & max
* @return std::string
*/
std::string MarkGrid::makeMark(const std::string& direction, const std::string& value, const bool& mini, const bool& mid, const bool& max)
{
	std::string cmd = "";
	cmd = "MARK " + this->name + " " + direction + " " + makeMidCommand(mini, mid, max)
		+ "SIZE " + value + ";\n";
	return cmd;
}

