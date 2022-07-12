#include "CurveData.h"
#include <iostream>

DV::CurveData::CurveData()
	:TimeData(Hdf5Data(), SINGLE_THREAD)
{

}

DV::CurveData::~CurveData()
{

}

bool DV::CurveData::loadPoint()
{
	return true;
}

std::string DV::CurveData::getInformationTitle()
{
	return "";
}

void DV::CurveData::setPoints(Data::ValuesPtr points)
{
	this->points = points;
	setPointSize(points->size() / 2);
	initXYRang();
}

void DV::CurveData::setParValues(const ParValues& pars)
{
	//如果数据量不匹配,则不予设置
	//以免后面取点时出现越界
	for (auto iter = pars.begin(); iter != pars.end(); iter++)
	{
		if (iter->second.size() < getPointSize())
			return;
	}
	parValues = pars;
}

DV::CurveData::ParValues DV::CurveData::getParValues()
{
	return parValues;
}

