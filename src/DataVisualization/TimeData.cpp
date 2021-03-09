#include "TimeData.h"

TimeData::TimeData(Hdf5Data& h5Data, const RunMod& mod /*= SINGLE_THREAD*/)
	:Data(h5Data, mod), pointSize(0)
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

	if (!ok && !listValues && listValues->size() == 0)
		return false;
	points = *(listValues->begin());
	pointSize = points->size()/2;
	//初始化范围
	initXYRang();

	return true;
}/**
* @brief TimeData::getPoint 根据索引给出一个点
* @param const int & index
* @return Point
*/
TimeData::Point TimeData::getPoint(const int& index)
{
	if (index >= pointSize)
	{
		Point p;
		return p;
	}
	return getPointHard(index);
}

/**
* @brief TimeData::getPointHard 根据索引给出一个点，这个函数不会判断容器边界，谨慎使用。
* @param const int & index
* @return Point
*/
TimeData::Point TimeData::getPointHard(const int& index)
{
	Point point;
	point.x = points->at(index * 2);
	point.y = points->at(index * 2 + 1);
	return point;
}

/**
* @brief TimeData::findIndexFromXValueL 通过x轴的值查找最近的索引，靠近左边
* @param const float & x
* @return int
*/
int TimeData::findIndexFromXValueL(const float& x)
{
	float step = (xRang.max - yRang.min) / pointSize;
	int index = x / step;
	return index;
}

/**
* @brief TimeData::findIndexFromXValueR 通过x轴的值查找最近的索引，靠近右边
* @param const float & x
* @return int
*/
int TimeData::findIndexFromXValueR(const float& x)
{
	return findIndexFromXValueR(x) + 1;
}

/**
* @brief TimeData::initXYRang 初始化xy的范围
* @return bool
*/
bool TimeData::initXYRang()
{
	if (pointSize <= 0)
		return false;

	//获取x轴的范围
	//由于数据是均匀分布的，直接取头尾即可
	auto iter = points->begin();
	xRang.min = *iter;
	iter = points->end();
	iter-=2;
	xRang.max = *iter;

	//y轴范围只会一个一个比 QAQ
	int index = 1;
	yRang.max = yRang.min = points->at(index);
	float temp = 0;
	for (; index <= points->size(); index += 2)
	{
		temp = points->at(index);
		if (yRang.max < temp)
			yRang.max = temp;
		if (yRang.min > temp)
			yRang.min = temp;
	}

	return true;

}
