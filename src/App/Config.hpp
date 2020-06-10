#pragma once
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/ini_parser.hpp>
#include <string>
#include "Singleton.hpp"

namespace PicNet
{
	//配置读取类
	class Config{
	public:
		Config(std::string path)
		{
				boost::property_tree::ini_parser::read_ini(path, _properities);
				_items = _properities.get_child("setting");
		}
		//通过Key值获取内容
		template<typename T>
		T Get(const char* name)
		{
			return _items.get<T>(name);
		}

		//获取当前应用程序路径
		std::string static GetProgramDir()

		{
			char exeFullPath[MAX_PATH]; // Full path

			std::string strPath = "";

			GetModuleFileName(NULL, exeFullPath, MAX_PATH);

			strPath = (std::string)exeFullPath;    // Get full path of the file

			int pos = strPath.find_last_of('\\', strPath.length());

			return strPath.substr(0, pos);  // Return the directory without the file name
		}

	private:
		boost::property_tree::ptree _properities;
		boost::property_tree::basic_ptree<std::string, std::string> _items;
	};

	typedef Singleton<Config> ConfigSingleton;
}