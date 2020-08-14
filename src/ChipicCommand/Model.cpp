#include "Model.h"

Model::Model()
	:name("")
{

}

Model::~Model()
{
}

/**
* @brief Model::setName 设置名称 并设置材料、网格划分的名称
* @param const std::string & name
* @return void
*/
void Model::setName(const std::string& name)
{
	this->name = name;
	texture.name = name;
	markGrid.name = name;
}

