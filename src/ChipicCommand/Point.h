#pragma once
#include "Model.h"
#include "MarkGrid.h"
class Point:public Model
{
public:
	Point();
	~Point();
public:
	//坐标值、点名称
	std::string value1, value2, value3;
	//网格划分
	MarkGrid markGrid;
public:
	std::string toCommand() override;
	bool fromCommand(const std::string& command) override;

	//设置点坐标
	void setValue(const std::string& value1, const std::string& value2, const std::string& value3);
};