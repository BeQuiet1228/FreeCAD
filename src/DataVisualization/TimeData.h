#pragma once
#include "Data.h"
#include <vector>
#include <mutex>
class TimeData :public Data{
public:
	TimeData(Hdf5Data& h5Data, const RunMod& mod = SINGLE_THREAD);
	~TimeData();

protected:
	virtual void restorDeriveData() override;

public:
	//载入点数据
	bool loadPoint();
	//获取point数量
	unsigned int getPointSize(){
		return pointSize;
	};
	//获取一个点
	QPointF getPoint(const unsigned int& index);
	QPointF getPointHard(const unsigned int& index);
	//根据值寻找一个索引
	unsigned int findIndexFromXValueL(const float& x);
	unsigned int findIndexFromXValueR(const float& x);
	//获取范围
	Rang getXRang(){
		std::lock_guard<std::mutex> am(xRangMutex);
		return xRang;
	};
	void setXRang(const Rang& rg){
		std::lock_guard<std::mutex> am(xRangMutex);
		xRang = rg;
	}
	Rang getYRang(){
		std::lock_guard<std::mutex> am(yRangMutex);
		return yRang;
	};
	void setYRang(const Rang& rg){
		std::lock_guard<std::mutex> am(yRangMutex);
		yRang = rg;
	}
private:
	//初始化xy的范围
	bool initXYRang();
private:
	//所有的点数据
	Data::ValuesPtr points;
	//点的个数
	int pointSize;
	//xy的范围
	Rang xRang, yRang;
	std::mutex xRangMutex, yRangMutex;
};