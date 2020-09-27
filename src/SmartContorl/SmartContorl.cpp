#include "SmartContorl.h"
extern "C"{
#include <lua/lua.h>
#include <lua/lualib.h>
#include <lua/lauxlib.h>
}
#include <iostream>
#include "LuaCInterface.h"
#include "Contorl/ContorlInterface.h"
#include "Contorl/Chipic.h"
SmartContorl::SmartContorl()
{
	lua_state = luaL_newstate();
	luaL_openlibs(lua_state);
	//注册lua函数
	registerLuaFunction(lua_state);
	//获取chipicmanager管理对象
	auto contorl = ContorlInterface::GetInstance();
	chipicManager = contorl->getChipicManager();
	chipicManager->setRunType(ChipicManager::AUTO);
	//链接计算完成槽
	connect(chipicManager, SIGNAL(finishChipicM3dPath(unsigned long)), this, SLOT(chipicWorkFinished(unsigned long)));
	connect(chipicManager, SIGNAL(chipicStartFinished(unsigned long)), this, SLOT(chipicStartFinished(unsigned long)));

	//测试使用代码
	ChipicRunDataPtr data;
	data.reset(new ChipicRunData);
	data->h5FilePath = "E:\\lingshiwenjianjia\\MILO_C\\MILO_C.h5";
	chipicDataFinish.push_back(data);
}

SmartContorl::~SmartContorl()
{
	lua_close(lua_state);
}

/**
* @brief SmartContorl::luaInit 调用lua脚本中的初始化函数
* @return void
*/
void SmartContorl::luaInit()
{
	lua_getglobal(lua_state, "init");
	lua_pcall(lua_state, 0, 0, 0);
}

/**
* @brief SmartContorl::luaResultDataFilter 调用lua脚本中的结果筛选函数
* @return void
*/
void SmartContorl::luaResultDataFilter()
{
	lua_getglobal(lua_state, "resultDataFilter");
	lua_pcall(lua_state, 0, 0, 0);
}

/**
* @brief SmartContorl::luaResultExpcet 调用lua脚本中的运算结果比对函数
* @return bool true 说明结果达到预期
*/
bool SmartContorl::luaResultExpcet()
{
	lua_getglobal(lua_state,"resultExpcet");
	lua_pcall(lua_state, 0, 1, 0);
	bool re = false;
	if (lua_gettop(lua_state) != 0)
	{
		re = lua_toboolean(lua_state,-1);
	}
#ifdef MY_DEBUG
	std::cerr << "SmartContorl::luaResultExpcet() re :" << re << std::endl;
#endif // MY_DEBUG

	return re;
}

/**
* @brief SmartContorl::luaOptimize 调用lua脚本中的参数优化函数
* @return void
*/
void SmartContorl::luaOptimize()
{
	lua_getglobal(lua_state, "optimize");
	lua_pcall(lua_state, 0, 0, 0);
}

/**
* @brief SmartContorl::luaLoadFromString 以字符串的形式载入lua脚本
* @param const std::string & lua lua脚本字符串
* @return void
*/
void SmartContorl::luaLoadFromString(const std::string& lua)
{
	luaL_dostring(lua_state,lua.c_str());
}

/**
* @brief SmartContorl::luaLoadFromFile 以文件路径的形式载入lua脚本
* @param const std::string & filePath lua脚本文件路径
* @return void
*/
void SmartContorl::luaLoadFromFile(const std::string& filePath)
{
	luaL_dofile(lua_state, filePath.c_str());
}

/**
* @brief SmartContorl::makeRunData 根据参数组、m3d路径、生成对应的运行信息
* @return void
*/
void SmartContorl::makeRunData()
{
	//将变量组生成多组m3d文本
	auto m3ds = Variate::makeStringForVariates(variates);

	fileMaker.setM3dPath(m3dPath);
	this->chipicDataWait = fileMaker.makeFile(m3ds);

	//清空变量组
	this->variates.clear();
}

/**
* @brief SmartContorl::runChipic 判断已运行的chipic数量，根据设置的最大运行数量，运行等待区中的m3d
* @return void
*/
void SmartContorl::runChipic()
{
	auto iter = this->chipicDataWait.begin();
	while (iter != this->chipicDataWait.end())
	{
		//已有足够多的chipic在运行则不操作
		if (chipicDataRuning.size() >= chipicCount)
			return;

		//启动chipic
		chipicManager->sendStartChipicMessage((*iter)->m3dPath.toStdString(), 1);
		chipicDataRuning.insert(ChipicRunDataMap::value_type((*iter)->m3dPath, *iter));
		chipicDataWait.erase(iter);

		iter = chipicDataWait.begin();
	}
}

/**
* @brief SmartContorl::dataOptimize 调用lua对参数进行优化
* @return void
*/
void SmartContorl::dataOptimize()
{
	//运算结果数据筛选
	this->luaResultDataFilter();
	//判断数据是否符合预期，符合则结束运行
	if (this->luaResultExpcet())
		return;
	//调用优化算法对参数进行优化
	this->luaOptimize();
}

/**
* @brief SmartContorl::chipicWorkFinished chipic计算完成槽
* @param unsigned long threadID
* @return void
*/
void SmartContorl::chipicWorkFinished(unsigned long threadID)
{
	//找到chipicdata对象
	auto dataIter = chipicDataRuning.begin();
	for (; dataIter != chipicDataRuning.end(); dataIter++)
	{
		if (dataIter->second->threadID == threadID)
			break;
	}

	auto chipicData = dataIter->second;
	chipicData->deleteItemAndBarPtr();

	chipicDataFinish.push_back(chipicData);
	chipicDataRuning.erase(dataIter);

	this->runChipic();

	//如果等待区和运行区没有任务了 则直接调用lua脚本优化参数
	if (this->chipicDataWait.size() == 0
		&& this->chipicDataRuning.size() == 0)
	{
		this->dataOptimize();
	}
}

/**
* @brief SmartContorl::chipicStartFinished chipic启动完成槽
* @param unsigned long threadID
* @return void
*/
void SmartContorl::chipicStartFinished(unsigned long threadID)
{
	//获取chipic对象
	auto chipicIter = chipicManager->chipicMap.find(threadID);
	if (chipicIter == chipicManager->chipicMap.end())
		return;
	auto chipic = chipicIter->second;

	//判断这个chipic对象是否是由this启动的
	QString path = QString::fromStdString(chipic->m3dPath);
	auto dataIter = chipicDataRuning.find(path);
	if (dataIter == chipicDataRuning.end())
		return;
	auto chipicData = dataIter->second;

	//生成ui 
	chipicData->setCreatDataBar(chipic);
	chipicData->threadID = threadID;
	chipicDataFinish.push_back(chipicData);

	emit addDataBar(chipicData->widgetItem, chipicData->dataBar);
}

#include "moc_SmartContorl.cpp"

/**
* @brief ChipicResultGetter::next 获取一个结果
* @param ChipicRunDataPtr & runData 
* @return bool false代表获取失败
*/
bool ChipicResultGetter::next(ChipicRunDataPtr& runData)
{
	if (this->iter == result.end())
		return false;
	runData = *iter;
	iter++;
	return true;
}
