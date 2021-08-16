#include "SmartContorlData.h"
#include "smartcontorl.h"
#include "CInterfaceStack.h"
#include <QDir>
#include "VariableStorer.h"
std::shared_ptr<SmartContorlData> SmartContorlData::_instance;

SmartContorlData::SmartContorlData()
{
	smartContorl = new SmartContorl;
	resultGetter = new ChipicResultGetter();
	cStack = new CInterfaceStack;
	variableStorer = new VariableStorer;
	//测试代码
	//getChipicRunResult();
}

SmartContorlData::~SmartContorlData()
{
	delete smartContorl;
	delete resultGetter;
	delete cStack;
	delete variableStorer;
}

/**
* @brief SmartContorlData::openActiveH5File 打开当前h5文件
* @return bool
*/
bool SmartContorlData::openActiveH5File()
{
	auto qPath = cStack->activeRunData->h5FilePath;
	QDir dir;
	if (!(dir.exists(qPath)))
	{
#ifdef MY_LOG
		std::cerr << "SmartContorlData::openActiveH5File() file is not exists! path: "
			<< qPath.toStdString();
		return false;
#endif // MY_LOG
	}
	std::string h5filePath = qPath.toStdString();
	
	//设置文件路径
	this->hdf5IO.setFilePath(h5filePath);
	//初始化对象
	this->hdf5IO.initHdf5Data();

	return true;
}

/**
* @brief SmartContorlData::findResultData 通过名称寻找一个结果图
* @param const std::string & name
* @return bool false 查找失败
*/
bool SmartContorlData::findResultData(const std::string& name)
{
	std::vector<Hdf5Data> &dataList = hdf5IO.hdf5DataList;
	auto iter = dataList.begin();
	for (; iter != dataList.end(); iter++)
	{
		//名称中会有许多多余的空格，暂时先这样去掉
		if (iter->petName == name)
			break;
	}
	if (iter == dataList.end())
		return false;
	cStack->activeH5Data = *iter;
	return true;
}

/**
* @brief SmartContorlData::openDataSet 打开一个数据库
* @param const int & index
* @return bool false 打开失败
*/
bool SmartContorlData::openDataSet(const int& index /*= 0*/)
{
	if (cStack->activeH5Data.listDataSet.size() <= index)
		return false;
	auto dataSet = cStack->activeH5Data.listDataSet.at(index);

	VectorF values;
	if (!hdf5IO.getValue(dataSet,values))
		return false;
	cStack->activeValues = values;
	return true;
}

int SmartContorlData::getDataSetValueSize()
{
	return cStack->activeValues.size();
}

/**
* @brief SmartContorlData::getDataSetValue 根据索引 获取一个数据
* @param const int & index
* @return float
*/
float SmartContorlData::getDataSetValue(const int& index)
{
	if (cStack->activeValues.size() <= index)
		return 0;
	float value = cStack->activeValues.at(index);
	return value;
}

/**
* @brief SmartContorlData::nextResult 获取一下个结果
* @return bool false 没有下一个
*/
bool SmartContorlData::nextResult()
{
	ChipicRunDataPtr data;
	if (resultGetter->next(data))
	{
		cStack->activeRunData = data;
		return true;
	}else{
		return false;
	}
}

/**
* @brief SmartContorlData::getChipicRunResult 获取下一个结果
* @return void
*/
void SmartContorlData::getChipicRunResult()
{
	*resultGetter = smartContorl->getResult();
	resultGetter->reset();

}

/**
* @brief SmartContorlData::addParam 向当前的cstack中的resultData中添加优化参数
* @param const float & value
* @return void
*/
void SmartContorlData::addParam(const float& value)
{
	cStack->activeRunData->resultData->addValue(value);
}

void SmartContorlData::clear()
{
	this->cStack->clear();
}

void SmartContorlData::clearH5Object()
{
	this->cStack->clear();
	hdf5IO.deleteH5File();
}
