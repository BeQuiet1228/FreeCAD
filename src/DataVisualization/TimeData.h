#pragma once
#include "Data.h"
#include <vector>
#include <mutex>
#include "fftw3.h"

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
	protected:
		//初始化xy的范围
		bool initXYRang() override;
	private:
		//所有的点数据
		Data::ValuesPtr points;
		Data::Values initpoints;//原始数据
		void fft(std::vector<float>& initdata, float fs);
		std::vector<Values> pointsContain;

	public:
		//对数据points进行FFT变换生成新的数据
		void dataToFFT(Data::Rang xr);
		std::vector<float> TimeData::getXYRange();
		void recoverData();
	};
};
