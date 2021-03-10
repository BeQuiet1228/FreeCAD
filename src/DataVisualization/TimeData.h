#pragma once
#include "Data.h"
#include <vector>
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
	int getPointSize(){
		return pointSize;
	};
	//获取一个点
	QPointF getPoint(const int& index);
	QPointF getPointHard(const int& index);
	//根据值寻找一个索引
	int findIndexFromXValueL(const float& x);
	int findIndexFromXValueR(const float& x);
	//获取范围
	Rang getXRang(){
		return xRang;
	};
	Rang getYRang(){
		return yRang;
	};
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
};