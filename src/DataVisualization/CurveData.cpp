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

void DV::CurveData::setPoints(Data::ValuesPtr points)
{
	this->points = points;
}

