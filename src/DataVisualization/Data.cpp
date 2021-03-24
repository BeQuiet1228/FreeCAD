#include "Data.h"

Data::Data(Hdf5Data& h5Data,const RunMod& mod)
	:h5Data(h5Data), sourceData(new ListValues)
	, sourceDataMutex(new std::mutex), runMod(mod), sourceDataIsLoad(false)
{

}

Data::~Data()
{

}

/**
* @brief Data::loadSourceData 获取h5文件中的数据
* @return bool 获取是否成功
*/
bool Data::loadSourceData()
{
	//防止二次载入 消耗资源
	if (isLoad())
		return true;
	return loadSourceDataHard();
}

/**
* @brief Data::loadSourceDataHard 获取h5文件中的数据 无论是否已经载入 都重新载入
* @return bool
*/
bool Data::loadSourceDataHard()
{
	auto h5IO = h5Data.hdf5Io;
	sourceDataIsLoad = h5IO->getValue(h5Data.listDataSet, *(sourceData.get()));
	return sourceDataIsLoad;
}

/**
* @brief Data::clearSourceData 清楚原始数据，目的是节约内存
* @return void
*/
void Data::clearSourceData()
{
	sourceData->clear();
	sourceDataIsLoad = false;
}

/**
* @brief Data::setRunMod 设置渲染模式
* @param const RunMod & mod
* @return void
*/
void Data::setRunMod(const RunMod& mod)
{
	if (this->runMod == mod)
		return;
	if (mod == MULTITHREAD)
		this->restorDeriveData();
	this->runMod = mod;
}

/**
* @brief Data::getSourceDataCopy 获取原始数据，这里获取的是复制对象，这里是为了保证多线程时的线程安全
* @param ListValuesPtr & listValuePtr 数据
* @return bool 是否获取成功
*/
bool Data::getSourceDataCopy(ListValuesPtr& listValuePtr)
{
	//如果数据还未载入则先载入数据
	if (!isLoad())
	{
		if (!loadSourceData())
			return false;
	}

	listValuePtr.reset(new ListValues());
	
	AutoMutx mutex(sourceDataMutex);
	for (auto iter = sourceData->begin(); iter != sourceData->end(); iter++)
	{
		Values *values = new Values;
		*values = *((*iter).get());
		ValuesPtr ptr(values);
		listValuePtr->push_back(ptr);
	}

	return true;
}

/**
* @brief Data::getSourceData 直接获取原始数据的reference
* @param ListValuesPtr & listValuePtr
* @return bool 成功返回true
*/
bool Data::getSourceData(ListValuesPtr& listValuePtr)
{
	//如果数据还未载入则先载入数据
	if (!isLoad())
	{
		if (!loadSourceData())
			return false;
	}

	//如果是多线程模式，不允许获取原始数据的引用
	if (runMod == MULTITHREAD)
		return false;
	listValuePtr = sourceData;

	return true;
}

/**
* @brief Data::autoModGetSourceData 根据线程模式自动选择获取原数据的方式
* @param ListValuesPtr & listValues
* @return bool
*/
bool Data::autoModGetSourceData(ListValuesPtr& listValues)
{
	bool ok(false);
	if (this->runMod == SINGLE_THREAD)
		ok = getSourceData(listValues);
	else if (this->runMod == MULTITHREAD)
		ok = getSourceDataCopy(listValues);
	return ok;
}

XYData::XYData(Hdf5Data& h5Data, const RunMod& mod /*= SINGLE_THREAD*/)
	:Data(h5Data, mod), pointSize(0)
{

}

/**
* @brief XYData::findIndexFromXValueR 通过x轴的值查找最近的索引，靠近右边
* @param const float & x
* @return unsigned int
*/
unsigned int XYData::findIndexFromXValueR(const float& x)
{
	unsigned int index = findIndexFromXValueL(x) + 1;
	if (index > getPointSize())
		return getPointSize() - 1;
	return index;
}
