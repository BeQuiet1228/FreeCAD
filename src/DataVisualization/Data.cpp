#include "Data.h"

Data::Data(Hdf5Data& h5Data,const RunMod& mod)
	:h5Data(h5Data), sourceData(new ListValues)
	, sourceDataMutex(new std::mutex), runMod(mod), sourceDataIsLoad(false), headList(h5Data.headList)
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
	AutoMutx am(sourceDataMutex);
	sourceDataIsLoad = Hdf5IO::getValue(h5Data.listDataSet, *(sourceData.get()));
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

void Data::initInformation()
{
	std::cerr << "Can't call Data::initInformation()" << std::endl;
}

/**
* @brief Data::stringToDirection 将坐标tile转换为方向
* @param const std::string & str
* @return DirectionType
*/
DirectionType Data::stringToDirection(const std::string& str)
{

	DirectionType direction;

	if (str == "X ")
		direction = X;
	else if (str == "Y ")
		direction = Y;
	else if (str == "Z ")
		direction = Z;
	else if (str == "R ")
		direction = R;
	else if (str == "R*cos")
		direction = R;
	else if (str == "R*sin")
		direction = THETA;
	else
		direction = NONE;

	return direction;
}

XYData::XYData(Hdf5Data& h5Data, const RunMod& mod /*= SINGLE_THREAD*/)
	:Data(h5Data, mod), pointSize(0), directionTyp(NONE), mapType(NEEDLESS_STRUCT)
{
	
}

unsigned int XYData::findIndexFromXValueL(const float& x)
{
	std::cerr << "Can't call XYData::findIndexFromXValueL" << std::endl;
	return 0;
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

void XYData::initInformation()
{
	if (headList.size() == 0)
		return;
	QString str = QString::fromStdString(headList.at(0));
	QStringList sl = str.split("$");
	
	if (sl.size() < 6)
		return;
	setXTag(sl.at(3).toStdString());
	setYTag(sl.at(4).toStdString());
}

/**
* @brief XYData::initDiretion 初始化数据方向信息
* @return void
*/
void XYData::initDiretion()
{
	initInformation();
	QString xt = QString::fromStdString(getXTag());
	QString yt = QString::fromStdString(getYTag());

	if (xt.indexOf('(') < 0 || yt.indexOf('(') < 0)
		return;
	QString xd = xt.split('(').at(0);
	QString yd = yt.split('(').at(0);
	directionTyp = DirectionType(stringToDirection(xd.toStdString()) | stringToDirection(yd.toStdString()));
	if (directionTyp == NONE)
		mapType = NEEDLESS_STRUCT;
	else
		mapType = NEED_STRUCT;
}
