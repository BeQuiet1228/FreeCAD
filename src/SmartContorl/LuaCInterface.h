#pragma  once
#include <string>

extern "C"{
#include <lua/lua.h>
#include <lua/lualib.h>
#include <lua/lauxlib.h>
}

//添加变量组
int addVariate(lua_State *L);
//获取下一结果
int nextResult(lua_State *luaState);
//打开结果文件
int openH5File(lua_State *luaState);
//查找结果图
int findResultData(lua_State *luaState);
//打开一个数据库
int openDataSet(lua_State *luaState);
//获取一个数据
int getValue(lua_State *luaState);
//注册lua函数
void registerLuaFunction(lua_State *L);