#pragma once
#include "TimeData.h"
#include "fftw3.h"
#include <QDir>

namespace DV {
	//后续的所有算法都通过这里枚举
	enum Alogrithm {
		InitData = 0,
		TimeDataForFFT = 1,
		InterspaceDataFFT = 2,
		gatherData = 3

	};

	class TimeAlgData :public TimeData {
	public:
		TimeAlgData(Hdf5Data& h5Data, const RunMod& mod = SINGLE_THREAD);
		~TimeAlgData();

	protected:
		//所有的点数据
		void fft(std::vector<float>& initdata, float fs);
		void addHeadlistStr(int index, Data::Rang XScope, std::string str);

	public:
		//对数据points进行算法变换生成新的数据
		bool loadPoint() override;
		virtual void dataToFFT(Data::Rang xr);
		virtual void dataToGather(Data::Rang xr);
		virtual bool addNewGroup();

		Data::ValuesPtr getPointsPtr();
		void updateData(int alogrithm, std::string xTag = "", std::string yTag = "");
		void updatePoint(Data::ValuesPtr point);
		void saveAs(std::string path, SaveMod mod = PUSHBACK);//重构Data的save专为TimeData使用

	public:
		int FunOfAlogrithm;//用来记录是否做过变换，为一个枚举值，后续可以增加枚举
	};
};
