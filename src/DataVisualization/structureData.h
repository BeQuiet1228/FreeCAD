#pragma once 
#ifndef _STRUCTUREDATA_H_
#define _STRUCTUREDATA_H_
#include "Data.h"
#include <vector>
#include <mutex>
#include <QVector>
#include <QRectF>
class structureData :public Data{
public:
	structureData(Hdf5Data& heData, const RunMod& mod = SINGLE_THREAD);
	~structureData();
protected:
	virtual void restorDeriveData() override;
public:
	//载入数据
	bool loadPoint();
	bool loadrectpoint();
	//获取数量
	int getPointSize()
	{
		return pointSize;
	}
	//获取一个点
	QPointF getPoint(const int& index);
	QPointF getPointHard(const int &index);
	//根据值寻找一个索引
	int findIndexFromXValueL(const float& x);
	int findIndexFromXValueR(const float& x);
	int findIndexFromYValueT(const float& y);
	int findIndexFromYValueB(const float& y);
	//获取真空坐标
	QVector<QRectF> GetVacuoPoint();
	//获取导管坐标
	QVector<QRectF> GetConduitPoint();
	//获取特定属性坐标
	QVector<QRectF> GetSpecificPoint(int property);
	//获取取值范围
	Rang getXRang()
	{
		std::lock_guard<std::mutex> am(xRangMutex);
		return xRang;
	}
	Rang getYRang()
	{
		std::lock_guard<std::mutex> am(yRangMutex);
		return yRang;
	}
	void setXRang(const Rang& rg)
	{
		std::lock_guard<std::mutex> am(xRangMutex);
		xRang = rg;
	}
	void setYRang(const Rang& rg)
	{
		std::lock_guard<std::mutex> am(yRangMutex);
		yRang = rg;
	}
private:
	//初始化xy的取值范围
	bool initXYRang();
private:
	//所有的点数据
	Data::ValuesPtr points;//后续会弃用
	//所有x的数据
	Data::ValuesPtr pointi1mx;
	//所有y的数据
	Data::ValuesPtr pointi2mx;
	Data::ValuesPtr pointi3mx;
	//方格的相关参数
	Data::ValuesPtr pointdatasetkmt;
	int pointSize;
	//横向点的个数
	int pointXSize;
	//纵向点的个数
	int pointYsize;
	//真空坐标
	QVector<QRectF> vacuo_vector;
	//导管坐标
	QVector<QRectF> conduit_vector;
	//特殊属性坐标
	QVector<QRectF> specificproperty_vector;
	//xy的范围
	Rang xRang, yRang;
	std::mutex xRangMutex, yRangMutex;
};


#endif