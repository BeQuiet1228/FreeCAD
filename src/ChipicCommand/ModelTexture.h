#pragma once
#include "CommandObject.h"
class ModelTexture:public CommandObject{
public:
	enum TextureType{
		UNDEFINED = 0, //未定义
		CONDUCTOR,	//导体
		DEFINED,	//自定义
		VACUO		//真空
	};
public:
	ModelTexture();
	~ModelTexture();

public:
	std::string toCommand() override;
	bool fromCommand(const std::string& command) override;
public:
	//材料类型
	TextureType type;
	//对应的模型名称
	std::string name;
};