#pragma once
#include "Data.h"
#include <vector>
#include <mutex>
#include "qwt/qwt_matrix_raster_data.h"
#include "DirData.h"
class ContourData :public DirData{
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
	//获取图表信息
	std::string getInformationTitle() override;
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
	void setXYRange();
	//根据坐标轴的名称 获取范围
	Data::Rang getAxisRangeFromName(const std::string& name);
protected:
	std::vector<Grid> grids;

	Rang valueRang;
	std::mutex ValueRangMutex;
	//网格大小
	unsigned int width, height;
	//网格标尺
	std::vector<float> xScale, yScale;
};

class DefineMatrixRasterData :public QwtMatrixRasterData {
public:
	DefineMatrixRasterData();
	~DefineMatrixRasterData();

public:
	virtual double value(double x, double y) const override;

	void setXScale(const std::vector<float>& xScale) {
		this->xScale = xScale;
	}
	void setYScale(const std::vector<float>& yscale) {
		this->yScale = yscale;
	}

private:
	std::vector<float> xScale, yScale;

private:
	int findIndex(const std::vector<float>& scale, const double& pos) const;

	bool isInScal(const std::vector<float>& scale, const double& pos) const;
};