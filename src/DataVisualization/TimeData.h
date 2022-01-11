#pragma once
#include "Data.h"
#include <vector>
#include <mutex>
#include "fftw3.h"
#include <QDir>

namespace DV {
	//后续的所有算法都通过这里枚举
	enum Alogrithm {
		InitData = 0,
		TimeDataForFFT = 1
	};

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
		void updateData(int alogrithm, std::string xTag = "", std::string yTag = "");

	private:
		//所有的点数据
		void fft(std::vector<float>& initdata, float fs);
		Data::ValuesPtr points;//显示的指针

	public:
		//对数据points进行FFT变换生成新的数据
		void dataToFFT(Data::Rang xr);
		Data::ValuesPtr getPointsPtr();
		void updatePoint(Data::ValuesPtr point);
		void saveAs(std::string path, SaveMod mod = PUSHBACK);

	public:
		int FunOfAlogrithm;//用来记录是否做过变换，为一个枚举值，后续可以增加枚举
	};
};
