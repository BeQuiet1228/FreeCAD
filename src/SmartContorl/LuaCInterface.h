#pragma  once
#include <string>

extern "C"{
#include <lua/lua.h>
#include <lua/lualib.h>
#include <lua/lauxlib.h>
}

//添加变量组
int addVariate(lua_State *L);
//注册lua函数
void registerLuaFunction(lua_State *L);