#pragma once
#ifndef _STRUCT_2D_DATA_H_
#define _STRUCT_2D_DATA_H_
#include "Data.h"
#include<map>
#include <vector>
#include "StructData.h"
class Struct2dData:public XYData
{
public:
	Struct2dData(Hdf5Data& heData, const RunMod& mode = SINGLE_THREAD);
	~Struct2dData();
protected:
	virtual void restorDeriveData() override;
	virtual bool initXYRang();
	bool initdata();
public:
	virtual bool loadPoint();
	virtual unsigned int findIndexFromXValueL(const float&x) override;
	std::list<unsigned __int64> isAnAttribute(unsigned __int64 p, StructData::PROPERTYPE);
public:
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
	void setXRang(const Rang& xr)
	{
		std::lock_guard<std::mutex> am(xRangMutex);
		xRang = xr;
	}
	void setYRang(const Rang& yr)
	{
		std::lock_guard<std::mutex> am(yRangMutex);
		yRang = yr;
	}
	int getposxSize()
	{
		return posxSize;
	}
	int getposySize()
	{
		return posySize;
	}
	std::map<int, std::map<int, std::vector<QPointF>>> GetAllinfo() {
		return allinfo;
	}
	std::map<int, std::map<int, std::vector<QPointF>>> getLineF()
	{
		return lineinfo;
	}
	std::vector<QPointF> ALLPOINTF()
	{
		return ALLPointf;
	}
private:
	//xy的范围
	Rang xRang, yRang;
	std::mutex xRangMutex, yRangMutex;
	//坐标的个数
	int posxSize;
	int posySize;
	std::map<int, std::map<int, std::vector<QPointF>>> allinfo;
	std::map<int, std::map<int, std::vector<QPointF>>> lineinfo;
	//全部点位，(包括多边型内部的网格点)
	std::vector<QPointF> ALLPointf;
 };
#endif