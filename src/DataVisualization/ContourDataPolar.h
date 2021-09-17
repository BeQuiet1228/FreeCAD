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

class ContourDataPloarHalfGridFullCircle :public ContourDataPolar {
public:
	ContourDataPloarHalfGridFullCircle(Hdf5Data& h5Data, const RunMod& mod = SINGLE_THREAD);
	~ContourDataPloarHalfGridFullCircle() = default;
public:
	virtual QwtMatrixRasterData* getQwtMatrixRasterData() override;
};

class PolarMatrixRasterData :public DefineMatrixRasterData{
public:
	PolarMatrixRasterData() = default;
	~PolarMatrixRasterData() = default;

	double value(double x, double y) const;


	static double FastAtan2(double y, double x);
	static double FastAtan( double x);
};

//根据h5文件信息创建数据对象
ContourDataPolar* CreateContourDataPolar(Hdf5Data& h5);