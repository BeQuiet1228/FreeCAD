#include "ContourData.h"

ContourData::ContourData(Hdf5Data& h5Data, const RunMod& mod /*= SINGLE_THREAD*/)
	:XYData(h5Data,mod)
{

}

ContourData::~ContourData()
{

}

void ContourData::restorDeriveData()
{

}

bool ContourData::initXYRang()
{
	return true;
}

/**
* @brief ContourData::loadPoint 载入点数据
* @return bool
*/
bool ContourData::loadPoint()
{
	Data::ListValuesPtr listValues;
	bool ok = autoModGetSourceData(listValues);

	if (!ok || !listValues || listValues->size() != 3)
		return false;

	//获取网格数据
	ValuesPtr xg, yg, vg;
	auto listValuesIter = listValues->begin();
	xg = *listValuesIter;
	listValuesIter++;
	yg = *listValuesIter;
	listValuesIter++;
	vg = *listValuesIter;

	if (xg->size() == 0 || yg->size() == 0 || vg->size() == 0)
		return false;

	//预分配空间
	grids.clear();
	grids.reserve(xg->size()*yg->size());

	auto xIter = xg->begin();
	auto yIter = yg->begin();
	auto vIter = vg->begin();

	//获取网格数据 并初始化网格范围
	Rang vr;
	vr.min = vr.max = *vIter;
	Grid tempGrid;
	for (; xIter != xg->end() && vIter != vg->end(); xIter++)
	{
		for (; xIter != yg->end() && vIter != vg->end(); yIter++)
		{
			//生成网格信息
			tempGrid.x = *xIter;
			tempGrid.y = *yIter;
			tempGrid.value = *vIter;
			grids.push_back(tempGrid);

			//生成value范围信息
			if (*vIter > vr.max)
				vr.max = *vIter;
			else if (*vIter < vr.min)
				vr.min = *vIter;

			vIter++;
		}
	
	}

	//初始化数据范围
	setValueRang(vr);
	Rang xr, yr;
	
	xr.min = *(xg->begin());
	xIter = xg->end();
	xIter--;
	xr.max = *xIter;

	yr.min = *(yg->begin());
	yIter = yg->end();
	yIter--;
	yr.max = *yIter;

	initXYRang();
}

double ContourData::value(double x, double y) const
{
	return 0.0;
}

