#include "InterSpaceData.h"

InterspaceData::InterspaceData(Hdf5Data& h5Data, const RunMod& mod /*= SINGLE_THREAD*/)
	:TimeData(h5Data,mod)
{

}

unsigned int InterspaceData::findIndexFromXValueL(const float& x)
{
	auto xr = getXRang();
	//如果范围小于最小值，那么直接返回第一个数值的索引
	if (x < xr.min)
		return 0;
	if (x > xr.max)
		return getPointSize() - 1;

	unsigned int fm, am;
	fm = 0;
	am = getPointSize() - 1;
	unsigned int index;

	while ((am - fm) > 1) {
		index = (am - fm) / 2;
		getPoint(index + fm).x() > x ? am = index + fm : fm += index;
	}
	return fm;
}

