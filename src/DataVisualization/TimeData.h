#pragma once
#include "Data.h"
#include <vector>
#include <mutex>
class TimeData :public XYData{
public:
	TimeData(Hdf5Data& h5Data, const RunMod& mod = SINGLE_THREAD);
	~TimeData();

protected:
	virtual void restorDeriveData() override;

public:
	//获取一个点
	QPointF getPoint(const unsigned int& index);
	QPointF getPointHard(const unsigned int& index);
	//根据值寻找一个索引
	unsigned int findIndexFromXValueL(const float& x) override;
	//载入点数据
	bool loadPoint() override;
	//获取信息
	std::string getInformationTitle();
protected:
	//初始化xy的范围
	bool initXYRang() override;
private:
	//所有的点数据
	Data::ValuesPtr points;
};