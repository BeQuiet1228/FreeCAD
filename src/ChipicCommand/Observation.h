#pragma once
#include "CommandObject.h"
#include "Model.h"
#include <vector>
class Observation:public CommandObject
{
public:
	Observation();
	~Observation();

public:
	//名称
	std::string name;

private:
	//指定观测对象 该指针由本对象释放
	Model* model;

private:
	std::string modelsToCommand();
};