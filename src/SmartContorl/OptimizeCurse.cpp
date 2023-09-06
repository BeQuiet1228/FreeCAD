#include "OptimizeCurse.h"
extern "C" {
#include <lua/lua.h>
#include <lua/lualib.h>
#include <lua/lauxlib.h>
}
#include <iostream>
#include "LuaCInterface.h"

OptimizeCurseLua::OptimizeCurseLua()
{
	lua_state = luaL_newstate();
	luaL_openlibs(lua_state);
	//注册lua函数
	registerLuaFunction(lua_state);
}

OptimizeCurseLua::~OptimizeCurseLua()
{
	lua_close(lua_state);
}

void OptimizeCurseLua::init(SmartContorl* smartControl)
{
	callLuaFunction("init");
}

bool OptimizeCurseLua::resultDataFilter(SmartContorl* smarControl)
{
	callLuaFunction("resultDataFilter", 0, 1);
	bool re = false;
	if (lua_gettop(lua_state) != 0)
	{
		re = lua_toboolean(lua_state, -1);
	}

	return re;
}

bool OptimizeCurseLua::resultExpcet(SmartContorl* smartControl)
{
	callLuaFunction("resultExpcet", 0, 1);
	bool re = false;
	if (lua_gettop(lua_state) != 0)
	{
		re = lua_toboolean(lua_state, -1);
	}
#ifdef MY_DEBUG
	std::cerr << "SmartContorl::luaResultExpcet() re :" << re << std::endl;
#endif // MY_DEBUG

	return re;
}

void OptimizeCurseLua::optimize(SmartContorl* smartCOntrol)
{
	callLuaFunction("printInformation");
	callLuaFunction("optimize");
}

void OptimizeCurseLua::luaLoadFromString(const std::string& lua)
{
	luaL_dostring(lua_state, lua.c_str());
}

void OptimizeCurseLua::luaLoadFromFile(const std::string& filePath)
{
	luaL_dofile(lua_state, filePath.c_str());
}

/**
* 将错误处理函数放入栈中 并返回它在栈中的位置
* @brief OptimizeCurseLua::getLuaErrorCallBackFunction 
* @return int
*/
int OptimizeCurseLua::getLuaErrorCallBackFunction()
{
	lua_pushcfunction(lua_state, pcallErrorCallBack);
	int callBack = lua_gettop(lua_state);

	return callBack;
}

/**
* @brief OptimizeCurseLua::printLuaError 打印lua在运行过程中的错误
* @param const int & error
* @return void
*/
void OptimizeCurseLua::printLuaError(const int& error)
{
	if (error != 0)
	{
		int t = lua_type(lua_state, -1);
		if (t != 4)
			return;
		std::string str = lua_tostring(lua_state, -1);
		std::cerr << str << std::endl;
		lua_pop(lua_state, -1);
	}
}

void OptimizeCurseLua::callLuaFunction(const std::string& functionName, const int& paramCount /*= 0*/, const int& returnCount /*= 0*/)
{
	int callBack = getLuaErrorCallBackFunction();
	//获取方法init
	lua_getglobal(lua_state, functionName.c_str());
	//传人参数

	int erro = lua_pcall(lua_state, paramCount, returnCount, callBack);
	printLuaError(erro);
}

