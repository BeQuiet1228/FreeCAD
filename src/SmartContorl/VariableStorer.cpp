#include "VariableStorer.h"
#include <iostream>
VariableStorer::VariableStorer()
	:xmlDocument(nullptr),filePath("")
{

}

VariableStorer::~VariableStorer()
{
	deleteXmlDocument();
}

bool VariableStorer::loadFile(const std::string& path)
{
	pugi::xml_document* doc = new pugi::xml_document;
	auto result = doc->load(path.c_str());
	if (result)
	{
		xmlDocument = doc;
		filePath = path;
		return true;
	}
#if MY_DEBUG
	std::cerr << "VariableStorer::loadFile load file failed,path : " << path << std::endl;
#endif
	delete doc;
	return false;
}

void VariableStorer::closeFile()
{
	deleteXmlDocument();
}

bool VariableStorer::fileIsLoad()
{
	if (xmlDocument != nullptr)
		return true;
	return false;
}

bool VariableStorer::saveFile(const std::string path /*= ""*/)
{
	return xmlDocument->save_file(path.c_str());
}

bool VariableStorer::saveFile()
{
	return saveFile(filePath);
}

bool VariableStorer::variableIsExsit(const std::string& name)
{
	auto node = xmlDocument->child("$$Variable$$");
	auto attr = node.attribute(name.c_str());
	if (attr)
		return true;
	return false;
}


std::string VariableStorer::getVariableToString(const std::string& name)
{
	return getVariableAtrribute(name).as_string();
}

int VariableStorer::getVariableToInt(const std::string& name)
{
	return getVariableAtrribute(name).as_int();
}

double VariableStorer::getVariableToDouble(const std::string& name)
{
	return getVariableAtrribute(name).as_double();
}


long long VariableStorer::getVariableToLLong(const std::string& name)
{
	return getVariableAtrribute(name).as_llong();
}

float VariableStorer::getVariableToFloat(const std::string& name)
{
	return getVariableAtrribute(name).as_float();
}

void VariableStorer::addVariable(const std::string& name, const std::string& var)
{
	auto node = xmlDocument->child("$$Variable$$");
	node.append_attribute(name.c_str()) = var.c_str();
}

/**
* @brief VariableStorer::deleteXmlDocument 释放掉xml对象 
* @return void
*/
void VariableStorer::deleteXmlDocument()
{
	delete xmlDocument;
	xmlDocument = nullptr;
}

/**
* @brief VariableStorer::getVariableAtrribute 获取变量对应的atrribute对象
* @param const std::string & name
* @return pugi::xml_attribute
*/
pugi::xml_attribute VariableStorer::getVariableAtrribute(const std::string& name)
{
	auto node = xmlDocument->child("$$Variable$$");
	return node.attribute(name.c_str());
}

