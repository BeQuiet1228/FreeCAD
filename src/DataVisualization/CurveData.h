#pragma  once
#include "TimeData.h"
#include <map>
#include <vector>
namespace DV {
	class  CurveData :public TimeData{
	public:
		CurveData();
		~CurveData();
	public:
		using ParValues = std::map<QString, std::vector<double>>;
	public:
		bool loadPoint() override;
		//获取信息
		std::string getInformationTitle() override;
		//设置点数据
		void setPoints(Data::ValuesPtr points);
		//设置额外的参数
		void setParValues(const ParValues& pars);
		ParValues getParValues();
	private:
		//附加数据，用于取点时显示
		ParValues parValues;
	};
}