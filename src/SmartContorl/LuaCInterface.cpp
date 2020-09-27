#include "LuaCInterface.h"
#include "SmartContorlData.h"
#include "SmartContorl.h"
#include <iostream>



/**
* @brief addVariate 添加变量组
* @param lua_State * L
* @return int
*/
int addVariate(lua_State *L)
{
	auto contorlData = SmartContorlData::GetInstance();
	auto contorl = contorlData->smartContorl;
	Variate variate;
	//获取名称参数
	variate.name = lua_tostring(L, 1);
	int iiii = lua_gettop(L);
	//获取值
	lua_pushnil(L);

	if (lua_istable(L,-2))
		int ii = lua_gettop(L);
	while (lua_next(L,-2))
	{
		std::string temp = lua_tostring(L, -1);
		variate.addValue(temp);
		lua_pop(L, 1);
	}
	contorl->addVariate(variate);
#ifdef MY_DEBUG
	std::cerr << "variate name : " << variate.name.toStdString() << std::endl;
	auto v = variate.values;
	for (auto i = v.begin(); i != v.end(); i++)
	{
		std::cerr << "value: " << i->toStdString() << std::endl;
	}
#endif // MY_DEBUG
	return 0;
}

int nextResult(lua_State *luaState)
{
	auto contorlData = SmartContorlData::GetInstance();
	bool b = contorlData->nextResult();
	lua_pushboolean(luaState,b);
	return 1;
}

int openH5File(lua_State *luaState)
{
	auto contorlData = SmartContorlData::GetInstance();
	bool b = contorlData->openActiveH5File();
	lua_pushboolean(luaState, b);
	return 1;
}

int findResultData(lua_State *luaState)
{
	auto contorlData = SmartContorlData::GetInstance();
	std::string name = lua_tostring(luaState, 1);
	bool b = contorlData->findResultData(name);
	lua_pushboolean(luaState, b);
	return 1;
}

int openDataSet(lua_State *luaState)
{
	auto contorlData = SmartContorlData::GetInstance();
	int index = lua_tointeger(luaState, 1);
	bool b = contorlData->openDataSet(index);
	lua_pushboolean(luaState, b);
	return 1;
}

int getValue(lua_State *luaState)
{
	auto contorlData = SmartContorlData::GetInstance();
	int index = lua_tointeger(luaState, 1);
	float value = contorlData->getDataSetValue(index);
	lua_pushnumber(luaState, value);
	return 1;
}

/**
* @brief registerLuaFunction 向虚拟机中注册lua函数
* @param lua_State * L
* @return void
*/
void registerLuaFunction(lua_State *L)
{
	lua_register(L, "addVariate", addVariate);
	lua_register(L, "nextResult", nextResult);
	lua_register(L, "findResultData", findResultData);
	lua_register(L, "openDataSet", openDataSet);
	lua_register(L, "getValue", getValue);
	lua_register(L, "openH5File", openH5File);
}


