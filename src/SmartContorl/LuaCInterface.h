#pragma  once
#include <string>

extern "C"{
#include <lua/lua.h>
#include <lua/lualib.h>
#include <lua/lauxlib.h>
}

//添加变量组
int addVariate(lua_State *L);
//获取所有的运算结果
int getAllResult(lua_State *L);
//获取下一结果
int nextResult(lua_State *luaState);
//打开结果文件
int openH5File(lua_State *luaState);
//查找结果图
int findResultData(lua_State *luaState);
//打开一个数据库
int openDataSet(lua_State *luaState);
//获取数据库数据的大
int getDataSetVlaueSize(lua_State *luaState);
//获取一个数据
int getValue(lua_State *luaState);
//获取历史运算次数大小
int getHistorySize(lua_State *luaState);
//获取一次优化中的组大小
int getGroupSize(lua_State *luaState);
//获取优化算法参数个数大小
int getParamSize(lua_State *luaState);
//添加优化算法参数
int addParam(lua_State *luaState);
//获取优化算法参数
int getParam(lua_State *luaState);
//注册lua函数
void registerLuaFunction(lua_State *L);