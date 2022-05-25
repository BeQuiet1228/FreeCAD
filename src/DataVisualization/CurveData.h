#pragma  once
#include "TimeData.h"
namespace DV {
	class  CurveData :public TimeData{
	public:
		CurveData();
		~CurveData();
	public:
		bool loadPoint() override;
		//获取信息
		std::string getInformationTitle() override;
		//设置点数据
		void setPoints(Data::ValuesPtr points);

	};
}