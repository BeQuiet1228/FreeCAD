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
		using ParValues = std::map<QString, std::vector<float>>;
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

	public:
		//通过hdf5文件生成多个曲线数据，仅限于优化算法生成的h5数据
		static std::list<std::shared_ptr<CurveData>> Hdf5DataToListCurveData(Hdf5Data& h5d, const int& index);
		static std::shared_ptr<CurveData> Hdf5DataSetToCurveData(DataSet& dataset,const std::vector<std::string> valueNames,const int & row,
			const int& index);
	};
}