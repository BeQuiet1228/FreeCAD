#pragma once
#include "ContourData.h"
class CountourDataPolar :public ContourData{
public:
	CountourDataPolar(Hdf5Data& h5Data, const RunMod& mod = SINGLE_THREAD);
	~CountourDataPolar();

public:
	virtual QwtMatrixRasterData* getQwtMatrixRasterData() override;
};