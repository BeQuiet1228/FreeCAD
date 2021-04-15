#pragma once
#include "ContourData.h"
#include "qwt/qwt_raster_data.h"
class ContourDataPolar :public ContourData{
public:
	ContourDataPolar(Hdf5Data& h5Data, const RunMod& mod = SINGLE_THREAD);
	~ContourDataPolar();

public:
	virtual QwtMatrixRasterData* getQwtMatrixRasterData() override;

	bool loadPoint() override;
};

class PolarMatrixRasterData :public QwtMatrixRasterData{
public:
	PolarMatrixRasterData() = default;
	~PolarMatrixRasterData() = default;

	double value(double x, double y) const;

};