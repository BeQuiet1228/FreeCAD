#pragma once
#include "target.h"
#include "xml/pugixml.hpp"
class TargetItem {
public:
	TargetItem();
	~TargetItem();
public:
	virtual void loadTarget(Target* target) = 0;
	virtual Target* GenerateTarget() = 0;

	//载入和保存
	virtual void saveXml(pugi::xml_node node) = 0;
	virtual void loadXml(pugi::xml_node node) = 0;

	//设置类型，用于xml载入
	void setType(const std::string& t);
	std::string getType();
private:
	std::string type;

};