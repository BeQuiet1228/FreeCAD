#include "CurveData.h"

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

