#pragma once
#include "CommandObject.h"
#include "MarkGrid.h"
#include "ModelTexture.h"
class Model:public CommandObject{
public:
	Model();
	~Model();

public:
	//网格划分
	MarkGrid markGrid;
	//排序
	int older;
	//材质
	ModelTexture texture;
	//名称 写入时推荐使用setName函数
	std::string name;
public:
	void setName(const std::string& name);

};