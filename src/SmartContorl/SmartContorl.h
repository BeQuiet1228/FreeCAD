#pragma once
#include <string>
#include "VariateAnalysis.h"
#include "ChipicRunData.h"
#include "FileMaker.h"
struct lua_State;
class SmartContorl{

public:
	SmartContorl();
	~SmartContorl();

public:
	//调用lua中的初始化函数
	void luaInit();
	//调用lua中的结果筛选函数
	void luaResultDataFilter();
	//调用lua中的结果比对函数
	bool luaResultExpcet();
	//调用lua中参数优化函数
	void luaOptimize();
	//载入lua脚本
	void luaLoadFromString(const std::string& lua);
	void luaLoadFromFile(const std::string& filePath);
	//根据参数组生成新的运行信息
	void makeRunData();
	
	//添加一个参数组
	void addVariate(const Variate& v){
		this->variates.push_back(v);
	};
	//获取虚拟机指针
	lua_State* getLuaState(){
		return lua_state;
	}
	//设置优化的m3d路径
	void setM3dPath(const QString& s){
		this->m3dPath = s;
	}
	void setM3dPath(const std::string s){
		this->m3dPath = QString::fromStdString(s);
	}
private:
	//lua虚拟机
	lua_State *lua_state;
	//参数组
	std::vector<Variate> variates;
	//待运行的m3d数据
	ChipicRunDatas chipicDataWait;
	//正在运行的m3d数据
	ChipicRunDataMap chipicDataRuning;
	//已经运行完的m3d数据
	ChipicRunDatas chipicDataFinish;
	//m3d文件路径
	QString m3dPath;
	//参数文件生成器
	FileMaker fileMaker;
};