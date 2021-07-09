#include "LuaCInterface.h"
#include "SmartContorlData.h"
#include "SmartContorl.h"
#include <iostream>
#include <sstream>
#include "VariableStorer.h"
#include <QFileInfo>

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
		std::cerr << "value: " << *i << std::endl;
	}
#endif // MY_DEBUG
	return 0;
}

int getAllResult(lua_State *L)
{
	auto contorlData = SmartContorlData::GetInstance();
	contorlData->getChipicRunResult();
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

int closeH5File(lua_State *luaState)
{
	/*auto contorlData = SmartContorlData::GetInstance();
	bool b = contorlData->openActiveH5File();*/
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

int getDataSetVlaueSize(lua_State *luaState)
{
	auto contorlData = SmartContorlData::GetInstance();
	int size = contorlData->getDataSetValueSize();
	lua_pushinteger(luaState,size);
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

int getHistorySize(lua_State *luaState)
{
	auto contorlData = SmartContorlData::GetInstance();
	int size = contorlData->smartContorl->getHistorySize();
	lua_pushinteger(luaState, size);

	return 1;
}

int getGroupSize(lua_State *luaState)
{
	auto contorlData = SmartContorlData::GetInstance();
	int index = lua_tointeger(luaState, 1);

	int size = contorlData->smartContorl->getHistoryGroupSize(index);
	lua_pushinteger(luaState, size);

	return 1;
}

int getParamSize(lua_State *luaState)
{
	auto contorlData = SmartContorlData::GetInstance();
	int groupIndex = lua_tointeger(luaState, 1);
	int index = lua_tointeger(luaState, 2);

	int size = contorlData->smartContorl->getHistoryGroupParamSize(groupIndex,index);
	lua_pushinteger(luaState, size);
	return 1;
}

int addParam(lua_State *luaState)
{
	auto contorlData = SmartContorlData::GetInstance();
	float value = lua_tonumber(luaState, 1);
	contorlData->addParam(value);
	return 0;

}

int getParam(lua_State *luaState)
{
	auto contorlData = SmartContorlData::GetInstance();
	int groupIndex = lua_tointeger(luaState, 1);
	int index = lua_tointeger(luaState, 2);
	int paramIndex = lua_tointeger(luaState, 3);

	float value = contorlData->smartContorl->getHistoryGroupParam(groupIndex, index, paramIndex);
	lua_pushnumber(luaState, value);

	return 1;
}

int saveParamsInHistory(lua_State *luaState)
{
	auto contorlData = SmartContorlData::GetInstance();
	contorlData->smartContorl->clearFinishData();
	return 0;
}

int cppPrint(lua_State *luaState)
{
	auto contorlData = SmartContorlData::GetInstance();
	std::string s = lua_tostring(luaState, 1);
	contorlData->smartContorl->printLog(s + "\n");
	return 0;
}

int pcallErrorCallBack(lua_State *luaState)
{
	lua_Debug debug = {};
	int live = 0;
	while (lua_getstack(luaState, live, &debug))
	{
		live++;
	}
	lua_getinfo(luaState, "Sln", &debug);
	if (lua_gettop(luaState) < 1)
		return 0;
	int type = lua_type(luaState, -1);
	std::string err = lua_tostring(luaState, -1);
	lua_pop(luaState, 1);
	std::string msg;
	//msg += debug.short_src + ":line " + debug.currentline;
	/*if (debug.name != 0) {
		msg << "(" << debug.namewhat << " " << debug.name << ")";
	}*/

	msg += " [" + err + "]\n";
	lua_pushstring(luaState, msg.c_str());
	return 1;

}

/**
* @brief setRunDataMakeType 设置运行数据的生成格式 目前仅有组合 与 穷举两种
* @param lua_State * luaState
* @return int
*/
int setRunDataMakeType(lua_State* luaState)
{
	auto contorlData = SmartContorlData::GetInstance();
	auto contorl = contorlData->smartContorl;
	
	std::string type = lua_tostring(luaState, 1);
	if (type == "conbination")
		contorl->setRunDataMakeType(SmartContorl::CONBINATION);
	else if(type == "exhaustivity")
		contorl->setRunDataMakeType(SmartContorl::EXHAUSTIVITY);
	return 1;
}

/**
* @brief variableIsExsit	查看本地变量是否存在
* @param lua_State * luaState
* @return int
*/
int variableIsExsit(lua_State* luaState)
{
	std::string name = lua_tostring(luaState, 1);
	
	auto contorlData = SmartContorlData::GetInstance();
	auto variableStorer = contorlData->variableStorer;

	bool b = variableStorer->variableIsExsit(name);
	lua_pushboolean(luaState,b);

	return 1;
}

/**
* @brief getFileVariable 获取文件变量  变量类型 s - string, i - int,n - double
* @param lua_State * luaState
* @return int
*/
int getFileVariable(lua_State* luaState)
{
	std::string name = lua_tostring(luaState, 1);
	std::string type = lua_tostring(luaState, 2);

	auto contorlData = SmartContorlData::GetInstance();
	auto variableStorer = contorlData->variableStorer;

	if (type == "s"){
		std::string variable = variableStorer->getVariableToString(name);
		lua_pushstring(luaState, variable.c_str());
	}
	else if (type == "i") {
		int variable = variableStorer->getVariableToInt(name);
		lua_pushinteger(luaState,variable);
	}
	else if (type == "n") {
		double variable = variableStorer->getVariableToDouble(name);
		lua_pushnumber(luaState,variable);
	}
	return 1;
}


int addFileVariable(lua_State* luaState)
{
	std::string name = lua_tostring(luaState, 1);
	std::string type = lua_tostring(luaState, 3);

	std::string value;

	if (type == "s") {
		value = lua_tostring(luaState, 2);
	}
	else if (type == "i") {
		int va = lua_tointeger(luaState, 2);
		value = QString::number(va).toStdString();
	}
	else if (type == "n") {
		double va = lua_tonumber(luaState,2);
		value = QString::number(va).toStdString();
	}

	auto contorlData = SmartContorlData::GetInstance();
	auto variableStorer = contorlData->variableStorer;

	variableStorer->addVariable(name, value);
	return 1;
}

int openVariableFile(lua_State* luaState)
{
	std::string fileName = lua_tostring(luaState, 1);
	auto contorlData = SmartContorlData::GetInstance();
	auto control = contorlData->smartContorl;
	QString m3dPath = control->getM3dPath();

	QFileInfo fileInfo(m3dPath);
	m3dPath = m3dPath.remove(fileInfo.fileName());

	m3dPath += QString::fromStdString(fileName) + ".var";

	auto variableStorer = contorlData->variableStorer;
	bool b = variableStorer->loadFile(m3dPath.toStdString());
	lua_pushboolean(luaState, b);

	return 1;
}

int closeVariableFile(lua_State* luaState)
{
	auto contorlData = SmartContorlData::GetInstance();
	auto variableStorer = contorlData->variableStorer;
	variableStorer->closeFile();

	return 1;
}

int saveVariableFile(lua_State* luaState)
{
	std::string fileName = lua_tostring(luaState, 1);
	auto contorlData = SmartContorlData::GetInstance();
	auto control = contorlData->smartContorl;
	QString m3dPath = control->getM3dPath();

	QFileInfo fileInfo(m3dPath);
	m3dPath = m3dPath.remove(fileInfo.fileName());

	m3dPath += QString::fromStdString(fileName) + ".var";

	auto variableStorer = contorlData->variableStorer;
	bool b = variableStorer->saveFile(m3dPath.toStdString());
	lua_pushboolean(luaState, b);

	return 1;
}

int clearVarableFileVar(lua_State* luaSate)
{
	auto contorlData = SmartContorlData::GetInstance();
	auto variableStorer = contorlData->variableStorer;
	variableStorer->clearVar();

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
	lua_register(L, "getHistorySize", getHistorySize);
	lua_register(L, "getGroupSize", getGroupSize);
	lua_register(L, "getParamSize", getParamSize);
	lua_register(L, "getParam", getParam);
	lua_register(L, "addParam", addParam);
	lua_register(L, "getAllResult", getAllResult);
	lua_register(L, "getDataSetVlaueSize", getDataSetVlaueSize);
	lua_register(L, "saveParamsInHistory", saveParamsInHistory);
	lua_register(L, "cppPrint", cppPrint);
	lua_register(L, "setRunDataMakeType", setRunDataMakeType);
}


