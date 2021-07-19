#include "TimeData.h"
#include "DataInformationGetter.h"
TimeData::TimeData(Hdf5Data& h5Data, const RunMod& mod /*= SINGLE_THREAD*/)
	:XYData(h5Data, mod)
{

}

TimeData::~TimeData()
{

}

void TimeData::restorDeriveData()
{

}

/**
* @brief TimeData::loadPoint 载入点数据
* @return bool
*/
bool TimeData::loadPoint()
{
	Data::ListValuesPtr listValues;
	bool ok = autoModGetSourceData(listValues);

	if (!ok || !listValues || listValues->size() == 0)
		return false;
	points = *(listValues->begin());
	setPointSize(points->size()/2);
	//初始化范围
	initXYRang();

	return true;
}

std::string TimeData::getInformationTitle()
{
	std::string title;
	const std::string end = "  ";
	title += "观察分量:";
	title += DataInformationGetter::getObserveObejct(headList.at(2)) + end;
	title += "观测面:";
	title += DataInformationGetter::getObserveFace(headList.at(15)) + end;

	return title;
}

/**
* @brief TimeData::getPoint 根据索引给出一个点
* @param const int & index
* @return QPointF
*/
QPointF TimeData::getPoint(const unsigned int& index)
{
	if (index >= getPointSize())
	{
		QPointF p;
		return p;
	}
	return getPointHard(index);
}

/**
* @brief TimeData::getPointHard 根据索引给出一个点，这个函数不会判断容器边界，谨慎使用。
* @param const unsigned int & index
* @return QPointF
*/
QPointF TimeData::getPointHard(const unsigned int& index)
{
	QPointF point;
	point.setX(points->at(index * 2));
	point.setY(points->at(index * 2 + 1));
	return point;
}

/**
* @brief TimeData::findIndexFromXValueL 通过x轴的值查找最近的索引，靠近左边
* @param const float & x
* @return unsigned int
*/
unsigned int TimeData::findIndexFromXValueL(const float& x)
{
	auto xr = getXRang();
	//如果范围小于最小值，那么直接返回第一个数值的索引
	if (x < xr.min)
		return 0;

	double step = xr.length() / getPointSize();
	unsigned int index = (x - xr.min )/ step;
	//如果索引超出范围则返回0
	if (index > getPointSize())
		return getPointSize();
	return index;
}

/**
* @brief TimeData::initXYRang 初始化xy的范围
* @return bool
*/
bool TimeData::initXYRang()
{
	if (getPointSize() < 2)
		return false;

	//获取x轴的范围
	//由于数据是均匀分布的，直接取头尾即可
	Rang xr, yr;
	auto iter = points->begin();
	xr.min = *iter;
	iter = points->end();
	iter-=2;
	xr.max = *iter;

	//y轴范围只会一个一个比 QAQ
	int index = 1;
	yr.max = yr.min = points->at(index);
	float temp = 0;
	for (; index <= points->size(); index += 2)
	{
		temp = points->at(index);
		if (yr.max < temp)
			yr.max = temp;
		else if (yr.min > temp)
			yr.min = temp;
	}
	setXRang(xr);
	setYRang(yr);
	return true;

}
