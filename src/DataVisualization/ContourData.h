#pragma once
#include "Data.h"
#include <vector>
#include <mutex>
#include "qwt/qwt_matrix_raster_data.h"
class ContourData :public XYData{
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
	//获取一个rasterData对象
	virtual QwtMatrixRasterData* getQwtMatrixRasterData();
	//寻找一个网格
	Grid findGrid(const float& x, const float& y);
	//获取对应的结构体面
	std::vector<float> getStructFace();
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
	//获取顶点
	std::vector<Grid> getVertex(const double& x,const double& y) const;
protected:
	std::vector<Grid> grids;

	Rang valueRang;
	std::mutex ValueRangMutex;
	//网格大小
	unsigned int width, height;
};