#pragma once 
#ifndef _STRUCTUREDATA_H_
#define _STRUCTUREDATA_H_
#include "Data.h"
#include <vector>
#include <mutex>
#include <QVector>
#include <QRectF>
typedef struct DaTaKmt
{ 
	//坐标1
	int point1;
	//坐标2
	int point2;
	//坐标3
	int point3;
	//属性
	int pointproperty;
}DATAKMT;
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
	//获取切割的空间
	QVector<QRectF> GetAllCutspace();
	//获取dataSetkmt的全部数据
	QVector<DaTaKmt> GetdatasetKmt();
	//填充相关属性的队列
	void fileproperty(QVector<QRectF> list);
private:
	//所有1mx的数据
	Data::ValuesPtr pointi1mx;
	//所有2mx的数据
	Data::ValuesPtr pointi2mx;
	//所有3mx的数据
	Data::ValuesPtr pointi3mx;
	//方格的相关参数
	Data::ValuesPtr pointdatasetkmt;
	//横向点的个数
	int pointXSize;
	//纵向点的个数
	int pointYsize;
	//真空坐标
	QVector<QRectF> vacuo_vector;
	//导管坐标
	QVector<QRectF> conduit_vector;
	//datasetkmt的数据采集
	QVector<DaTaKmt> datakmtinfo;
	//xy的范围
	Rang xRang, yRang;
	std::mutex xRangMutex, yRangMutex;
};


#endif