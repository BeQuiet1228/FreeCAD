#pragma  once
#include <string>
class DataInformationGetter {
public:
	DataInformationGetter() = default;
	~DataInformationGetter() = default;

public:
	//获取观测分量
	static std::string getObserveObejct(const std::string& head);
	//获取观测面
	static std::string getObserveFace(const std::string& head);
	//获取观测时间
	static std::string getObserveTime(const std::string& head);
	//获取矢量图的观测参数
	static std::string getVectorParam(const std::string& head);
	//获取时间观测图的观测分量
	static std::string getObserveParam(const std::string& head);
};