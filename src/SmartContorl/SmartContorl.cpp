#include "SmartContorl.h"
extern "C"{
#include <lua/lua.h>
#include <lua/lualib.h>
#include <lua/lauxlib.h>
}
#include <iostream>
#include "LuaCInterface.h"
SmartContorl::SmartContorl()
{
	lua_state = luaL_newstate();
	luaL_openlibs(lua_state);
	//注册lua函数
	registerLuaFunction(lua_state);
}

SmartContorl::~SmartContorl()
{
	lua_close(lua_state);
}

/**
* @brief SmartContorl::luaInit 调用lua脚本中的初始化函数
* @return void
*/
void SmartContorl::luaInit()
{
	lua_getglobal(lua_state, "init");
	lua_pcall(lua_state, 0, 0, 0);
}

/**
* @brief SmartContorl::luaResultDataFilter 调用lua脚本中的结果筛选函数
* @return void
*/
void SmartContorl::luaResultDataFilter()
{
	lua_getglobal(lua_state, "resultDataFilter");
	lua_pcall(lua_state, 0, 0, 0);
}

/**
* @brief SmartContorl::luaResultExpcet 调用lua脚本中的运算结果比对函数
* @return bool true 说明结果达到预期
*/
bool SmartContorl::luaResultExpcet()
{
	lua_getglobal(lua_state,"resultExpcet");
	lua_pcall(lua_state, 0, 1, 0);
	bool re = false;
	if (lua_gettop(lua_state) != 0)
	{
		re = lua_toboolean(lua_state,-1);
	}
#ifdef MY_DEBUG
	std::cerr << "SmartContorl::luaResultExpcet() re :" << re << std::endl;
#endif // MY_DEBUG

	return re;
}

/**
* @brief SmartContorl::luaOptimize 调用lua脚本中的参数优化函数
* @return void
*/
void SmartContorl::luaOptimize()
{
	lua_getglobal(lua_state, "optimize");
	lua_pcall(lua_state, 0, 0, 0);
}

/**
* @brief SmartContorl::luaLoadFromString 以字符串的形式载入lua脚本
* @param const std::string & lua lua脚本字符串
* @return void
*/
void SmartContorl::luaLoadFromString(const std::string& lua)
{
	luaL_dostring(lua_state,lua.c_str());
}

/**
* @brief SmartContorl::luaLoadFromFile 以文件路径的形式载入lua脚本
* @param const std::string & filePath lua脚本文件路径
* @return void
*/
void SmartContorl::luaLoadFromFile(const std::string& filePath)
{
	luaL_dofile(lua_state, filePath.c_str());
}

/**
* @brief SmartContorl::makeRunData 根据参数组、m3d路径、生成对应的运行信息
* @return void
*/
void SmartContorl::makeRunData()
{
	//将变量组生成多组m3d文本
	auto m3ds = Variate::makeStringForVariates(variates);

	fileMaker.setM3dPath(m3dPath);
	this->chipicDataWait = fileMaker.makeFile(m3ds);
}

