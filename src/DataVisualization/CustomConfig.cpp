#include "CustomConfig.h"
#include <iostream>

std::shared_ptr<Config> Config::instance;


bool Config::loadConfig()
{
	xmlDocument->load_file("./DataVisualizationConfig.xml");
	rootGroup.node = xmlDocument->child("root");
	if (rootGroup.empty())
		rootGroup.node = xmlDocument->append_child("root");
	return true;
}

Config::Config()
{
	xmlDocument = new pugi::xml_document;
	loadConfig();
}
Config::~Config()
{
	delete xmlDocument;
}

ConfigGroup::ConfigGroup()
	:node(nullptr)
{

}

/**
* @brief ConfigGroup::addSetting 在组内添加键值对
* @param const std::string & key  键
* @param const std::string & value 值
* @return void
*/
void ConfigGroup::addSetting(const std::string& key, const std::string& value)
{
	if (empty())
		return;
	node.append_attribute(key.c_str()) = value.c_str();
	Config::GetInstance()->saveFile();
}

void ConfigGroup::setSetting(const std::string& key, const std::string& value)
{
	if (empty())
		return;
	node.attribute(key.c_str()) = value.c_str();
	Config::GetInstance()->saveFile(); 
}

/**
* @brief ConfigGroup::getValue 获取值
* @param const std::string & key 键
* @return std::string
*/
std::string ConfigGroup::getValue(const std::string& key)
{
	if (empty())
		return "";
	return node.attribute(key.c_str()).as_string();
}

/**
* @brief ConfigGroup::getGroup 获取组对象
* @param const std::string & groupName 组名称
* @return ConfigGroup
*/
ConfigGroup ConfigGroup::getGroup(const std::string& groupName)
{
	ConfigGroup group;
	group.node = node.child(groupName.c_str());
	if (group.node.empty())
		group.node = node.append_child(groupName.c_str());
	return group;
}
