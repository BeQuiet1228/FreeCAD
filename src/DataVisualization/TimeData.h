#pragma once
#include "Data.h"
#include <vector>
#include <mutex>

namespace DV {
	class TimeData :public XYData {
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
		virtual unsigned int findIndexFromXValueL(const float& x) override;
		//载入点数据
		bool loadPoint() override;
		//获取信息
		std::string getInformationTitle();
	public:
		//初始化xy的范围
		bool initXYRang() override;

	protected:
		Data::ValuesPtr points;//显示的指针
	};
};
