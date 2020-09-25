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

/**
* @brief registerLuaFunction 向虚拟机中注册lua函数
* @param lua_State * L
* @return void
*/
void registerLuaFunction(lua_State *L)
{
	lua_register(L, "addVariate", addVariate);
}


