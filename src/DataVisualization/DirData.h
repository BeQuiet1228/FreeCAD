#pragma once
#ifndef _DIR_DATA_H_
#define _DIR_DATA_H_
#include "Data.h"
#include"exportConfig.hpp"
namespace DV {
	/*
		带结构图的图表、调整数据方向的正确性。
	*/
	class DATA_VISUALIZATION_EXPORT DirData :public XYData
	{
	public:
		DirData(Hdf5Data& hedata, const RunMod& mod = SINGLE_THREAD);
		~DirData() = default;
	public:
		bool isTruedir();
	private:
	};
};


#endif