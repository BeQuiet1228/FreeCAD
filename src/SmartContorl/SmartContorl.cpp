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
#include "OptimizeCurse.h"
#include <QFile>
#include <QTextIStream>
#include "SmartContorlData.h"
#include <QMessageBox>
#include <QTextCodec>
#include <QFileInfo>

QString SmartContorl::gbkStdstringToQstring(const std::string& str)
{
	QTextCodec* pCodec = QTextCodec::codecForName("gb2312");
	if (!pCodec) return "";

	QString qstr = pCodec->toUnicode(str.c_str(), str.length());
	return qstr;
}

SmartContorl::SmartContorl()
	:makeRunDataType(CONBINATION),optimizeCurse(nullptr)
{
	//获取chipicmanager管理对象
	chipicManager = ContorlInterface::GetInstance()->getChipicManager();
	//链接计算完成槽
	connect(chipicManager, SIGNAL(finishChipicM3dPath(unsigned long)), this, SLOT(chipicWorkFinished(unsigned long)));
	connect(chipicManager, SIGNAL(chipicStartFinished(unsigned long)), this, SLOT(chipicStartFinished(unsigned long)));
	connect(chipicManager, SIGNAL(chipicAnalysisFinished(unsigned long)), this, SLOT(chipicAnalysisFinished(unsigned long)));
	connect(chipicManager, SIGNAL(chipicErrorClose(unsigned long)), this, SLOT(chipicErrorClose(unsigned long)));

}

SmartContorl::~SmartContorl()
{
	delete optimizeCurse;
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
	{
		return;
	}

	//已有足够多的chipic在运行则不操作
	if (chipicDataRuning.size() >= chipicCount)
		return;

	//如果还有未解析完的内核 则返回
	if (!finishedIsVasible)
		return;

	auto iter = this->chipicDataWait.begin();
	//启动chipic
	chipicManager->sendStartChipicMessage((*iter)->m3dPath.toStdString(), 1);
	chipicDataRuning.insert(ChipicRunDataMap::value_type((*iter)->m3dPath, *iter));
	chipicDataWait.erase(iter);
	//设置为未解析完成状态
	finishedIsVasible = false;
	
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
	bool ok = resultDataFilter();
	//清理h5对象 这个暂时放在这里，后续应当写到lua脚本中
	SmartContorlData::GetInstance()->clearH5Object();
	//如果结果数据筛选失败，那么给出提示
	if (!ok)
	{
// 		QMessageBox* msgBox = new QMessageBox;
// 		msgBox->setAttribute(Qt::WA_DeleteOnClose);
// 		msgBox->setWindowTitle(QString::fromLocal8Bit("提示"));
// 		msgBox->setText(QString::fromLocal8Bit("优化结果数据筛选失败，请检查输出H5文件格式是否正确！"));
// 		msgBox->show();
		optimizeCurse->init(this);
		//运行优化之后的参数
		this->makeRunData();
		this->runChipic();
		return;
	}

	//清空完成运算数据
	//this->clearFinishData();
	//判断数据是否符合预期，符合则结束运行
	//或者是达到最大优化次数
	if (historyDatas.size() > maxCount || optimizeCurse->resultExpcet(this))
	{
		runing = false;
		return;
	}
		
	//调用优化算法对参数进行优化
	optimizeCurse->optimize(this);
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
	//saveResultFormIndex(0, "123");
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
	//保存log到文件
	auto p = this->fileMaker.m3dPath;
	p = p.left(p.length() - 4) + "_log.text";
	QFile file(p);
	if (file.open(QIODevice::ReadWrite))
	{
		QTextStream stream(&file);
		stream << QString::fromStdString(log);
	}
	file.close();

	emit smartContorlLog(log);
}
void SmartContorl::run()
{
	//如果已有其他chipic在运行则返回
	if (controlModIsRuning())
		return;
	//设置管理器运行模式
	chipicManager->setRunType(ChipicManager::AUTO);

	runing = true;
	finishedIsVasible = true;
	this->optimizeCurse->init(this);
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
	p = p.left(p.length() - 4) + "_log.text";
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
#if 0
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
		stream << (*i)->variate;
		stream << "F=" <<(*i)->resultData->getValue(0) << "\n\n";
	}
	stream << "-------------------------------------\n";
	file.close();
#endif
}

int SmartContorl::getHistorySize()
{
	return historyDatas.size();
}

void SmartContorl::addVariate(const Variate& v)
{
	this->variates.push_back(v);
}

void SmartContorl::setM3dPath(const QString& s)
{
	this->m3dPath = s;
	fileMaker.setM3dPath(s);
}

void SmartContorl::setM3dPath(const std::string s)
{
	this->m3dPath = QString::fromStdString(s);
	fileMaker.setM3dPath(m3dPath);
}

ChipicResultGetter SmartContorl::getResult()
{
	ChipicResultGetter result(chipicDataFinish);
	return result;
}

std::vector<SmartContorl::HistoryData> SmartContorl::getHistoryDatas()
{
	return historyDatas;
}

void SmartContorl::setRunDataMakeType(const MakeRunDataType& type)
{
	this->makeRunDataType = type;
}

QString SmartContorl::getM3dPath()
{
	return m3dPath;
}

void SmartContorl::stop()
{
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

	//设置管理器运行模式
	chipicManager->setRunType(ChipicManager::MANUAL);
}


/**
* @brief SmartContorl::controlModIsRuning 判断control模块是否已经在运行其他的东西
* @return bool
*/
bool SmartContorl::controlModIsRuning()
{
	auto control = ContorlInterface::GetInstance();
	bool ok = control->hasChipicRuning() || runing;
	if (ok)
	{
		QMessageBox* msgBox = new QMessageBox;
		msgBox->setAttribute(Qt::WA_DeleteOnClose);
		msgBox->setWindowTitle(gbkStdstringToQstring("提示"));
		msgBox->setText(gbkStdstringToQstring("有其他chipic正在运行中，请关闭后重新尝试！"));
		msgBox->show();
	}

	return ok;
}

bool SmartContorl::resultDataFilter()
{
	bool ok = optimizeCurse->resultDataFilter(this);
	if (!ok)
		return ok;
	std::vector<VectorF> valuesList;
	std::vector<std::string> headList;

	auto hisoty = getHistoryDatas();
	if (hisoty.size() == 0)
		return ok;

	//获取变量个数和目标函数个数
	int varCount = 0, functionCount = 0;
	varCount = hisoty[0].variates.size();
	functionCount = hisoty[0].datas[0]->resultData->size();

	//生成h5文件需要的头信息
	{
		headList.push_back("smartControl");
		headList.push_back(std::to_string(varCount));
		headList.push_back(std::to_string(functionCount));
		std::string varNames;
		for (auto var : hisoty[0].variates)
		{
			varNames += " " + var.name.toStdString();
		}
		headList.push_back(varNames);
	}
	//获取数据
	{
		//数据集的个数，对应种群个数
		int dataSetCount =  hisoty[0].datas.size();

		//初始化vector
		for (int i = 0; i < dataSetCount; i++)
			valuesList.push_back(VectorF());
		/*
		* 搜集数据信息
		* 信息的排列方式为 变量参数 、目标函数值
		*/
		for (auto his : hisoty)
		{
			auto vars = his.variates;
			ChipicRunDatas datas = his.datas;

			for (int i = 0; i < dataSetCount; i++)
			{
				for (auto var : vars)
				{
					valuesList[i].push_back(var.values[i]);
				}
				auto d = datas[i];
				auto result = d->resultData;
				for (int j = 0; j < result->size(); j++)
				{
					valuesList[i].push_back(result->getValue(j));
				}
			}
		}
	}
	//将数据保存到H5文件
	auto path = this->fileMaker.m3dPath;
	path = path.left(path.length() - 4) + "_opt.h5";
	
	Hdf5IO::creatNewH5File(path.toStdString());
	Hdf5IO hdf5(path.toStdString());
	hdf5.insertHdf5Group(headList, valuesList, varCount + functionCount);
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
	auto iter = chipicDataRuning.begin();
	for (; iter != chipicDataRuning.end(); iter++)
	{
		if(iter->second->threadID == threadID)
			break;
	}
	if (iter == chipicDataRuning.end())
	{
		std::cerr << "SmartContorl::chipicAnalysisFinished not find data with runing data." << std::endl;
		return;
	}
	iter->second->IsAnalysis = true;
	finishedIsVasible = true;
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
		msgBox->setWindowTitle(gbkStdstringToQstring("提示"));
		msgBox->setText(gbkStdstringToQstring("m3d文本出错，导致优化算法停止运行，文本路径:%1").arg(chipicData->m3dPath));
		msgBox->show();
		this->stop();
		return;
	}
	chipicData->errorExitCount++;
	std::cerr << chipicData->m3dPath.toStdString() << std::endl;

	//如果未被解析说明是上一次启动的内核，则直接调用run
	chipicDataWait.push_back(chipicData);
	chipicDataRuning.erase(dataIter);

	finishedIsVasible = !chipicData->IsAnalysis;
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
/**
* @brief SmartContorl::saveResultFormIndex 保存H5文件
* @param int index
* @param std::string str
* @return bool
*/

bool SmartContorl::saveResultFormIndex(int index, std::string str)
{
	if (historyDatas.empty())
		return false;
	auto datas = historyDatas.rbegin()->datas;

	if (index >= datas.size())
		return false;
	auto saveResult = datas[index];
	//读取m3d文件
	QString dstPath = this->m3dPath;
	int dstlastindex = dstPath.lastIndexOf("/");
	//获取工程路径
	dstPath = dstPath.mid(0,dstlastindex);
	std::string dstPathstr = dstPath.toStdString();
	//获取工程名
	QString proName = this->m3dPath;
	int profroIndex = dstlastindex;
	int prolastindex = proName.lastIndexOf(".");
	proName = proName.mid(profroIndex,prolastindex-profroIndex);
	std::string proNamestr = proName.toStdString();
	QString saveM3dPath = saveResult->m3dPath;
	if (saveM3dPath.toLower().endsWith(".m3d") || saveM3dPath.toLower().endsWith(".m2d"))
	{

		QString dstFileName = dstPath + proName + "_" + QString::fromStdString(str) + saveM3dPath.right(4);
		std::string dstFileNamestr = dstFileName.toStdString();
		//如果文件存在，先删除
		QFileInfo file(dstFileName);
		if (file.exists() == true)
		{
			QFile dstfile(dstFileName);
			dstfile.remove();
		}
		//保存文件'
		bool ok=QFile::copy(saveM3dPath, dstFileName);
	}
	QString saveH5Path = saveResult->h5FilePath;
	std::string saveH5Pathstr = saveH5Path.toStdString();
	if (saveH5Path.toLower().endsWith(".h5"))
	{
		QString dstFileName = dstPath + proName + "_" + QString::fromStdString(str) + saveH5Path.right(3);
		std::string dstfileNamestr = dstFileName.toStdString();
		//如果文件存在，先删除
		QFileInfo file(dstFileName);
		if (file.exists() == true)
		{
			QFile dstfile(dstFileName);
			dstfile.remove();
		}
		//保存文件
		bool ok=QFile::copy(saveH5Path, dstFileName);
	}
}

OptimizeCurse* SmartContorl::getOptimizeCurse()
{
	return optimizeCurse;
}


void SmartContorl::setOptimizeCurse(OptimizeCurse* op)
{
	delete optimizeCurse;
	this->optimizeCurse = op;
}

#include "moc_SmartContorl.cpp"
