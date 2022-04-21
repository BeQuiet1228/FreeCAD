#pragma once
#include "SmartContorl.h"

class OptimizeCurse {
public:
	OptimizeCurse() {};
	~OptimizeCurse() {};

public:
	virtual void init(SmartContorl* smartControl) = 0;
	virtual bool resultDataFilter(SmartContorl* smarControl) = 0;
	virtual bool resultExpcet(SmartContorl* smartControl) = 0;
	virtual void optimize(SmartContorl* smartCOntrol) = 0;
};

class OptimizeCurseLua :public OptimizeCurse{
public:
	OptimizeCurseLua();
	~OptimizeCurseLua();

public:
	virtual void init(SmartContorl* smartControl) override;
	virtual bool resultDataFilter(SmartContorl* smarControl) override;
	virtual bool resultExpcet(SmartContorl* smartControl)override;
	virtual void optimize(SmartContorl* smartCOntrol) override;

	//载入lua脚本
	void luaLoadFromString(const std::string& lua);
	void luaLoadFromFile(const std::string& filePath);

private:
	//获取错误处理函数再栈中的位置
	int getLuaErrorCallBackFunction();
	//打印lua脚本中的错误
	void printLuaError(const int& error);
	//调用一个lua函数
	void callLuaFunction(const std::string& functionName, const int& paramCount = 0, const int& returnCount = 0);

private:
	//lua虚拟机
	lua_State* lua_state;
};