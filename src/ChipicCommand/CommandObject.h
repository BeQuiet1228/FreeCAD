#pragma once
#include <string>
class CommandObject{

public:
	CommandObject() = default;
	virtual ~CommandObject(){};

public:
	//生成对应的命令
	virtual std::string toCommand() = 0;
	//从命令中获取对象参数
	virtual bool fromCommand(const std::string& command) = 0;

public:
	bool notOutputCommand = false;
};