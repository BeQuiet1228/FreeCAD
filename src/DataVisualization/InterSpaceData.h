#pragma once
#include "TimeData.h"

class InterspaceData:public TimeData{
public:
	InterspaceData(Hdf5Data& h5Data, const RunMod& mod = SINGLE_THREAD);
	~InterspaceData() = default;
};