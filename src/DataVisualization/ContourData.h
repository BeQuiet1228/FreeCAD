#pragma once
#include "Data.h"
#include <vector>
#include <mutex>
#include "qwt/qwt_raster_data.h"
class ContourData :public XYData, public QwtRasterData{
public:
	struct Grid
	{
		Grid() :x(0.0), y(0.0), value(0.0){};
		float x, y, value;
	};
public:
	ContourData(Hdf5Data& h5Data, const RunMod& mod = SINGLE_THREAD);
	~ContourData();

protected:
	virtual void restorDeriveData() override;
	bool initXYRang() override;
public:
	bool loadPoint() override;

	//获取值的范围
	virtual QwtDoubleInterval range() const override{
		return QwtDoubleInterval(valueRang.min, valueRang.max);
	}
	//获取网格中的值
	virtual double value(double x, double y) const override;
public:
	void setValueRang(const Rang& r){
		std::lock_guard<std::mutex> am(ValueRangMutex);
		valueRang = r;
	}
	Rang getVlaueRange() {
		std::lock_guard<std::mutex> am(ValueRangMutex);
		return valueRang;
	}
private:
	std::vector<Grid> grids;

	Rang valueRang;
	std::mutex ValueRangMutex;
};