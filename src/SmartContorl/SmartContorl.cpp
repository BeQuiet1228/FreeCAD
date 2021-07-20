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
#include <QFile>
#include <QTextIStream>
#include "SmartContorlData.h"
#include <QMessageBox>
#include "Contorl/MessageTransition.h"
SmartContorl::SmartContorl()
	:makeRunDataType(CONBINATION)
{
	lua_state = luaL_newstate();
	luaL_openlibs(lua_state);
	//注册lua函数
	registerLuaFunction(lua_state);
	//获取chipicmanager管理对象
	chipicManager = ContorlInterface::GetInstance()->getChipicManager();
	//链接计算完成槽
	connect(chipicManager, SIGNAL(finishChipicM3dPath(unsigned long)), this, SLOT(chipicWorkFinished(unsigned long)));
	connect(chipicManager, SIGNAL(chipicStartFinished(unsigned long)), this, SLOT(chipicStartFinished(unsigned long)));
	connect(chipicManager, SIGNAL(chipicAnalysisFinished(unsigned long)), this, SLOT(chipicAnalysisFinished(unsigned long)));
	connect(chipicManager, SIGNAL(chipicErrorClose(unsigned long)), this, SLOT(chipicErrorClose(unsigned long)));
	//测试使用代码
	/*ChipicRunDataPtr data;
	data.reset(new ChipicRunData);
	data->h5FilePath = "E:\\lingshiwenjianjia\\MILO_C\\MILO_C.h5";
	chipicDataFinish.push_back(data);*/
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
	int callBack = getLuaErrorCallBackFunction();
	callLuaFunction("init");
#if 0
	//获取方法
	lua_State* L = luaL_newstate();
	if (!L)
		return;
	luaL_openlibs(L);
	int ret = luaL_dofile(L,"C://Users//DELL//Desktop//test.lua");
	int res=lua_getglobal(L,"init");
	//压入参数
	std::string name = "RAA";
	double max = 0.5;
	double min = 0.1;
	int count = 3;
	std::string s1=lua_pushstring(L,name.c_str());
	lua_pushnumber(L,max);
	lua_pushnumber(L,min);
	lua_pushnumber(L,count);
	if ((res = lua_pcall(L, 4, 0,0))!=0)//参数数量,参数返回值，错误输出函数
	{
		printf("err %s\n",lua_tostring(lua_state,-1));
		lua_pop(lua_state, 1);//若有错误则弹出
		printf("top = %d \n", lua_gettop(lua_state));
	}
	lua_close(L);
#endif
#if 0
	int res = lua_getglobal(lua_state,"init2");
	//获取变量
	std::string name = "RCC";
	double max = 0.5;
	double min = 0.1;
	int count = 3;
	std::string s1 = lua_pushstring(lua_state, name.c_str());
	lua_pushnumber(lua_state, max);
	lua_pushnumber(lua_state, min);
	lua_pushnumber(lua_state, count);
	if ((res = lua_pcall(lua_state, 4, 0, 0)) != 0)//参数数量,参数返回值，错误输出函数
	{
		printf("err %s\n", lua_tostring(lua_state, -1));
		lua_pop(lua_state, 1);//若有错误则弹出
		printf("top = %d \n", lua_gettop(lua_state));
	}
#endif
}
//void SmartContorl::luaInit(std::string _name, double _max, double _min, int _count)
//{
//	int res = lua_getglobal(lua_state, "init2");
//	//获取变量
//	std::string name = _name;
//	double max = _max;
//	double min = _min;
//	int count = _count;
//	std::string s1 = lua_pushstring(lua_state, name.c_str());
//	lua_pushnumber(lua_state, max);
//	lua_pushnumber(lua_state, min);
//	lua_pushnumber(lua_state, count);
//	if ((res = lua_pcall(lua_state, 4, 0, 0)) != 0)//参数数量,参数返回值，错误输出函数
//	{
//		printf("err %s\n", lua_tostring(lua_state, -1));
//		lua_pop(lua_state, 1);//若有错误则弹出
//		printf("top = %d \n", lua_gettop(lua_state));
//	}
//}
/**
* @brief SmartContorl::luaResultDataFilter 调用lua脚本中的结果筛选函数
* @return bool
*/
bool SmartContorl::luaResultDataFilter()
{
	callLuaFunction("resultDataFilter",0,1);
	bool re = false;
	if (lua_gettop(lua_state) != 0)
	{
		re = lua_toboolean(lua_state, -1);
	}

	return re;
}

/**
* @brief SmartContorl::luaResultExpcet 调用lua脚本中的运算结果比对函数
* @return bool true 说明结果达到预期
*/
bool SmartContorl::luaResultExpcet()
{
	callLuaFunction("resultExpcet", 0, 1);
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
	callLuaFunction("optimize");
}

/**
* @brief SmartContorl::luaLoadFromString 以字符串的形式载入lua脚本
* @param const std::string & lua lua脚本字符串
* @return void
*/
void SmartContorl::luaLoadFromString(const std::string& lua)
{
	std::cout << lua << std::endl;
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
	//auto m3ds = Variate::makeStringForVariates(variates);
	std::vector<QString> m3ds;
	switch (makeRunDataType)
	{
	case SmartContorl::CONBINATION:
		m3ds = Variate::combinationStringForVariates(variates);
		break;
	case SmartContorl::EXHAUSTIVITY:
		m3ds = Variate::makeStringForVariates(variates);
		break;
	}
	
	fileMaker.setM3dPath(m3dPath);
	this->chipicDataWait = fileMaker.makeFile(m3ds);
	
	//保存变量信息
	runData.variates = this->variates;
	//清空变量组
	this->variates.clear();
}

/**
* @brief SmartContorl::runChipic 判断已运行的chipic数量，根据设置的最大运行数量，运行等待区中的m3d
* @return void
*/
void SmartContorl::runChipic()
{
	/*
		日期：2021-2-4
		对启动顺序做修改，之前是在最大限制个数中，一次尽可能多的启动。
		现在修改为每次只启动一个。然后再解析完成槽中不停的触发这个函数，这样可以解决解析时消息过多，
		超过windows消息栈大小的问题。
	*/
#if 1
	//如果等待区为空则退出
	if (chipicDataWait.size() <= 0)
		return;
	auto iter = this->chipicDataWait.begin();
	//已有足够多的chipic在运行则不操作
	if (chipicDataRuning.size() >= chipicCount)
		return;
	//启动chipic
	chipicManager->sendStartChipicMessage((*iter)->m3dPath.toStdString(), 1);
	chipicDataRuning.insert(ChipicRunDataMap::value_type((*iter)->m3dPath, *iter));
	chipicDataWait.erase(iter);
	
#else
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
#endif
	
}

/**
* @brief SmartContorl::dataOptimize 调用lua对参数进行优化
* @return void
*/
void SmartContorl::dataOptimize()
{
	//运算结果数据筛选
	bool ok = this->luaResultDataFilter();
	//清理h5对象 这个暂时放在这里，后续应当写到lua脚本中
	SmartContorlData::GetInstance()->clearH5Object();
	//如果结果数据筛选失败，那么给出提示
	if (!ok)
	{
		QMessageBox* msgBox = new QMessageBox;
		msgBox->setAttribute(Qt::WA_DeleteOnClose);
		msgBox->setWindowTitle(QString::fromLocal8Bit("提示"));
		msgBox->setText(QString::fromLocal8Bit("优化结果数据筛选失败，请检查输出H5文件格式是否正确！"));
		msgBox->show();
		return;
	}

	//清空完成运算数据
	//this->clearFinishData();
	//判断数据是否符合预期，符合则结束运行
	if (this->luaResultExpcet())
		return;
	//调用优化算法对参数进行优化
	this->luaOptimize();
	//运行优化之后的参数
	this->makeRunData();
	this->runChipic();
}

/**
* @brief SmartContorl::getHistoryGroupSize 获取历史记录中的一组数据的大小
* @param const int & groupIndex 组的索引
* @return int
*/
int SmartContorl::getHistoryGroupSize(const int& groupIndex)
{
	int size = 0;
	if (historyDatas.size() > groupIndex)
	{
		size = historyDatas.at(groupIndex).datas.size();
	}

	return size;
}

/**
* @brief SmartContorl::getHistoryGroupParamSize 获取历史记录中某一次运算的参数个数
* @param const int & groupIndex 组的索引
* @param const int & index 某一次运算的索引
* @return int
*/
int SmartContorl::getHistoryGroupParamSize(const int& groupIndex, const int& index)
{
	int size = 0;
	if (getHistoryGroupSize(groupIndex) > index)
	{
		auto chipicData = historyDatas.at(groupIndex).datas.at(index);
		size = chipicData->resultData->size();
	}

	return size;
}

/**
* @brief SmartContorl::getHistoryGroupParam 获取运行历史记录中一个参数的值
* @param const int & goupIdex 组的索引
* @param const int & index 某次运行的索引
* @param const int & paramIndex 参数索引
* @return float
*/
float SmartContorl::getHistoryGroupParam(const int& goupIdex, const int& index, const int& paramIndex)
{
	float param = 0.0;
	if (getHistoryGroupParamSize(goupIdex, index) <= paramIndex)
		return param;

	auto chipicData = historyDatas.at(goupIdex).datas.at(index);
	param = chipicData->resultData->getValue(paramIndex);

	return param;
}

/**
* @brief SmartContorl::clearFinishData清空已完成的数据，并将数据存到历史数据中
* @return void
*/
void SmartContorl::clearFinishData()
{
	/*
		这里需要将结果数据按变量生成的顺序排序，否则无法与脚本中的参数一一对应。
	*/
	unsigned int count = this->chipicDataFinish.size();
	ChipicRunDatas tempDatas;
	for (int i = 0; i < count; i++)
	{
		tempDatas.push_back(ChipicRunDataPtr());
	}
	for (auto iter = chipicDataFinish.begin(); iter != chipicDataFinish.end(); iter++)
	{
		tempDatas[(*iter)->rank] = *iter;
	}

	runData.datas = tempDatas;
	historyDatas.push_back(runData);
	saveCurrentData();
	chipicDataFinish.clear();
}

/**
* @brief SmartContorl::printLog 在这里集中处理lua中打印出来的信息
* @param const std::string
* @return void
*/
void SmartContorl::printLog(const std::string& log)
{
	emit smartContorlLog(log);
}
void SmartContorl::run(const QString& lua)
{
	//设置管理器运行模式
	chipicManager->setRunType(ChipicManager::AUTO);

	runing = true;
	this->luaLoadFromString(lua.toStdString());
	this->luaInit();
	this->makeRunData();
	this->initDataFile();
	this->runChipic();
}

/**
* @brief SmartContorl::initDataFile 初始化用于存运行数据的文件
* @return void
*/
void SmartContorl::initDataFile()
{
	auto p = this->fileMaker.m3dPath;
	p = p.left(p.length() - 4) + ".data";
	QFile file(p);
	if (!file.open(QIODevice::ReadWrite))
	{
		return;
	}
	file.remove();
	if (!file.open(QIODevice::ReadWrite))
	{
		return;
	}
	file.close();
}

void SmartContorl::saveCurrentData()
{
	auto p = this->fileMaker.m3dPath;
	p = p.left(p.length() - 4) + ".data";
	QFile file(p);
	if (!file.open(QIODevice::Append))
	{
		return;
	}
	QTextStream stream(&file);

	stream << "-------------------------------------\n";
	auto tempDatas = runData.datas;
	for (auto i = tempDatas.begin(); i != tempDatas.end(); i++)
	{
		stream << (*i)->variate << "\n";
		stream << "F=" <<(*i)->resultData->getValue(0) << "\n";
	}
	stream << "-------------------------------------\n";

}

void SmartContorl::stop()
{
	//设置管理器运行模式
	chipicManager->setRunType(ChipicManager::MANUAL);

	runing = false;

	variates.clear();

	chipicDataWait.clear();
	
	//关闭已经启动完成的chipic，并清理掉 正在启动中的待启动完成之后在行处理
	std::vector<QString> paths;
	for (auto i = chipicDataRuning.begin(); i != chipicDataRuning.end(); i++)
	{
		if (i->second->threadID != 0)
		{
			paths.push_back(i->first);
			chipicManager->closeChipic(i->second->threadID);
			i->second->deleteItemAndBarPtr();
		}
	}
	for (auto i = paths.begin(); i != paths.end(); i++)
	{
		auto iter = chipicDataRuning.find(*i);
		if (iter != chipicDataRuning.end())
			chipicDataRuning.erase(iter);
	}

	chipicDataFinish.clear();

	historyDatas.clear();
}
/**
* @brief SmartContorl::getLuaErrorCallBackFunction 将错误处理函数放入栈中，并返回再栈中位置
* @return int
*/
int SmartContorl::getLuaErrorCallBackFunction()
{
	lua_pushcfunction(lua_state, pcallErrorCallBack);
	int callBack = lua_gettop(lua_state);

	return callBack;
}

void SmartContorl::printLuaError(const int& error)
{
	if (error != 0)
	{
		int t = lua_type(lua_state, -1);
		if (t != 4)
			return;
		std::string str = lua_tostring(lua_state, -1);
		std::cerr << str << std::endl;
		lua_pop(lua_state, -1);
	}
}

/**
* @brief SmartContorl::callLuaFunction 调用一个lua函数
* @param const std::string & functionName 函数名
* @param const int & paramCount 参数个数
* @param const int & returnCount 返回值个数
* @return void
*/
void SmartContorl::callLuaFunction(const std::string& functionName, const int& paramCount, const int& returnCount)
{
	int callBack = getLuaErrorCallBackFunction();
	//获取方法init
	lua_getglobal(lua_state, functionName.c_str());
	//传人参数

	int erro = lua_pcall(lua_state, paramCount, returnCount, callBack);
	printLuaError(erro);
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
	if (dataIter == chipicDataRuning.end())
		return;
	auto chipicData = dataIter->second;
	chipicData->deleteItemAndBarPtr();

	chipicDataFinish.push_back(chipicData);
	chipicDataRuning.erase(dataIter);

	//暂时这样保证chipic是一个个启动的
	if (finishedIsVasible)
	{
		this->runChipic();
		finishedIsVasible = false;
	}
		

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
	{
#if MY_LOG
		std::cerr << "SmartContorl::chipicStartFinished find chipic object faild" << std::endl;
#endif
		return;
	}
	auto chipic = chipicIter->second;

	//判断这个chipic对象是否是由this启动的
	QString path = QString::fromStdString(chipic->m3dPath);
	auto dataIter = chipicDataRuning.find(path);
	if (dataIter == chipicDataRuning.end())
		return;
	//判断整个模块的运行状态  如果已经是停止状态则清理掉数据  并清理掉正在运行的程序
	if (!runing)
	{
		chipicDataRuning.erase(dataIter);
		chipicManager->closeChipic(threadID);
		return;
	}

	auto chipicData = dataIter->second;

	//生成ui 
	chipicData->setCreatDataBar(chipic);
	chipicData->threadID = threadID;
	//chipicDataFinish.push_back(chipicData);

	emit addDataBar(chipicData->widgetItem, chipicData->dataBar);
}

void SmartContorl::chipicAnalysisFinished(unsigned long threadID)
{
	if (chipicDataRuning.size() == chipicCount)
		finishedIsVasible = true;
	else
		finishedIsVasible = false;
	this->runChipic();
}

void SmartContorl::chipicErrorClose(unsigned long threadID)
{
	std::cerr << "Error exit!" << std::endl;
	//找到chipicdata对象
	auto dataIter = chipicDataRuning.begin();
	for (; dataIter != chipicDataRuning.end(); dataIter++)
	{
		if (dataIter->second->threadID == threadID)
			break;
	}
	if (dataIter == chipicDataRuning.end())
		return;
	auto chipicData = dataIter->second;
	chipicData->deleteItemAndBarPtr();

	/*
		判断错误重启的次数，如果超过三次，则判定这个文本有问题。给出提示并停止优化
	*/
	if (chipicData->errorExitCount == 3)
	{
		QMessageBox *msgBox = new QMessageBox;
		msgBox->setAttribute(Qt::WA_DeleteOnClose);
		msgBox->setWindowTitle(QString::fromLocal8Bit("提示"));
		msgBox->setText(QString::fromLocal8Bit("m3d文本出错，导致优化算法停止运行，文本路径:%1").arg(m3dPath));
		msgBox->show();
		this->stop();
		return;
	}
	chipicData->errorExitCount++;
	
	std::cerr << chipicData->m3dPath.toStdString() << std::endl;
	/*
		判断等待区是否还有未运行的，如果还有则说明还有未解析完成的内核。
		则不调用启动函数。
	*/

	bool hasWait = false;
	if (chipicDataWait.size() > 0)
		hasWait = true;
	chipicDataWait.push_back(chipicData);
	chipicDataRuning.erase(dataIter);

	if (!hasWait)
		runChipic();

}

/**
* @brief ChipicResultGetter::next 获取一个结果
* @param ChipicRunDataPtr & runData
* @return bool false代表获取失败
*/
bool ChipicResultGetter::next(ChipicRunDataPtr& runData)
{
	if (this->iter == result.end())
	{
		return false;
	}
	runData = *iter;
	iter++;
	return true;
}

#include "moc_SmartContorl.cpp"
