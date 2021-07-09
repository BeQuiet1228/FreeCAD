#pragma once
#include "xml/pugixml.hpp"
class VariableStorer {
public:
	VariableStorer();
	~VariableStorer();

public:
	bool loadFile(const std::string& path);
	void creatXmlDocument();
	void closeFile();
	bool fileIsLoad();
	bool saveFile(const std::string path);
	bool saveFile();
	bool variableIsExsit(const std::string& name);
	void addVariable(const std::string& name, const std::string& var);
	void clearVar();
	//获取数据
public:
	std::string getVariableToString(const std::string& name);
	int getVariableToInt(const std::string& name);
	double getVariableToDouble(const std::string& name);
	long long getVariableToLLong(const std::string& name);
	float getVariableToFloat(const std::string& name);
private:
	//xml 对象
	pugi::xml_document* xmlDocument;
	//文件路径
	std::string filePath;
private:
	void deleteXmlDocument();
	pugi::xml_attribute getVariableAtrribute(const std::string& name);
};