#pragma once
#include "ContourData.h"
#include "qwt/qwt_raster_data.h"
class CountourDataPolar :public ContourData{
public:
	CountourDataPolar(Hdf5Data& h5Data, const RunMod& mod = SINGLE_THREAD);
	~CountourDataPolar();

public:
	virtual QwtMatrixRasterData* getQwtMatrixRasterData() override;
};

class PolarMatrixRasterData :public QwtMatrixRasterData{
public:
	PolarMatrixRasterData() = default;
	~PolarMatrixRasterData() = default;

	double value(double x, double y) const;

};