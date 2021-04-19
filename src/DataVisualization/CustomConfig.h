#pragma  once
#include <memory>
#include <mutex>
#include "xml/pugixml.hpp"

class ConfigGroup{
	friend class Config;
public:
	~ConfigGroup() = default;
private:
	ConfigGroup();
public:
	//添加数据
	void addSetting(const std::string& key, const std::string& value);
	//设置数据
	void setSetting(const std::string& key, const std::string& value);
	//获取数据
	std::string getValue(const std::string& key);
	//获取组
	ConfigGroup getGroup(const std::string& groupName);

	//是否为空
	bool empty(){
		return node.empty();
	};
private:
	pugi::xml_node node;
};

class Config{
public:
	~Config();
	static std::shared_ptr<Config> GetInstance(){
		static std::once_flag flag;
		std::call_once(flag, [&](){
			instance.reset(new Config);
		});

		return instance;
	}
private:
	Config();
	Config(const Config&) = delete;
	Config operator =(const Config&) = delete;

	static std::shared_ptr<Config> instance;

private:
	//xml文件对象
	pugi::xml_document* xmlDocument;
	//根组
	ConfigGroup rootGroup;
public:
	//获取根组
	ConfigGroup getRootGroup(){
		return rootGroup;
	}
	//载入配置文件
	bool loadConfig();
	//保存文件
	void saveFile(){
		xmlDocument->save_file("./DataVisualizationConfig.xml");
	}
};