#pragma once
#ifndef _STRUCT_2D_DATA_H_
#define _STRUCT_2D_DATA_H_
#include "Data.h"
#include<map>
#include <vector>
#include "exportConfig.hpp"
#include "StructData.h"
namespace DV {
	class DATA_VISUALIZATION_EXPORT Struct2dData :public XYData
	{
	public:
		Struct2dData(Hdf5Data& heData, const RunMod& mode = SINGLE_THREAD);
		Struct2dData(Hdf5Data& heData, QPointF start, QPointF end, const RunMod& mode = SINGLE_THREAD);
		~Struct2dData();
	protected:
		virtual void restorDeriveData() override;
		virtual bool initXYRang();
		bool initdata();
	public:
		virtual bool loadPoint();
		virtual unsigned int findIndexFromXValueL(const float& x) override;
		std::list<unsigned __int64> isAnAttribute(unsigned __int64 p, StructData::PROPERTYPE);
	public:
		Rang getXRang();
		Rang getYRang();
		void setXRang(const Rang& xr);
		void setYRang(const Rang& yr);
		int getposxSize();
		int getposySize();
		std::map<int, std::map<int, std::vector<QPointF>>> GetAllinfo();
		std::map<int, std::map<int, std::vector<QPointF>>> getLineF();
		std::vector<QPointF> ALLPOINTF();
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
		//去点选择范围
	public:
		QPointF mstart;
		QPointF mend;
		bool istrue;
	};
};

#endif