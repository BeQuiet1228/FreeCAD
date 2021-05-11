#pragma once
#ifndef _DIR_DATA_H_
#define _DIR_DATA_H_
#include "Data.h"
class DirData:public XYData
{
public:
	DirData(Hdf5Data& hedata, const RunMod& mod = SINGLE_THREAD);
	~DirData() = default;
protected:
	bool isTruedir();
private:
};

#endif