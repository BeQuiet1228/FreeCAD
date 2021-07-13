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
//关闭h5文件
int closeH5File(lua_State *luaState);
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
//存储当前参数到历史记录
int saveParamsInHistory(lua_State *luaState);
//运行时需要看见的信息
int cppPrint(lua_State *luaState);
//lua脚本运行出错时的错误处理函数
int pcallErrorCallBack(lua_State *luaState);
//设置数据生成模式
int setRunDataMakeType(lua_State* luaState);
//查看变量是否存在
int variableIsExsit(lua_State* luaState);
//获取变量值
int getFileVariable(lua_State* luaState);
//添加文件变量
int addFileVariable(lua_State* luaState);
//打开变量文件
int openVariableFile(lua_State* luaState);
//关闭变量文件
int closeVariableFile(lua_State* luaState);
//保存变量文件
int saveVariableFile(lua_State* luaState);
//清理变量文件对象
int clearVarableFileVar(lua_State* luaSate);
//创建一个变量文件对象
int creatVarableFileObject(lua_State* luaState);

//注册lua函数
void registerLuaFunction(lua_State *L);