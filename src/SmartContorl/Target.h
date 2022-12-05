#pragma once
#include <string>
#include <vector>
#include "HDF5Reader/hdf5io.h"
class TargetComprison {
public:
	TargetComprison() {};
	~TargetComprison() {};
public:
	virtual bool comparison(const double& par1, const double& par2) = 0;
};

class TargetComprisonGreaterThan :public TargetComprison {

public:
	virtual bool comparison(const double& par1, const double& par2) override;

};

class TargetComprisonApproach :public TargetComprison{
public:
	TargetComprisonApproach();
public:
	//目标函数值
	double expect;
	//接近误差，需要errorRange/100 得到精度范围
	int errorRange;
	virtual bool comparison(const double& par1, const double& par2) override;
};


class Target {
public:
	Target();
	virtual ~Target();
	//目标值
	double value;
public:
	virtual double getTagetValue(const std::string& filePath) = 0;
	virtual bool comparison(const double& par1, const double& par2);
	void setTargetComprison(TargetComprison* com);
	TargetComprison* getTargetComprison();
protected:
	virtual std::vector<float> getH5DataValue(const std::string& filePath)=0;
	virtual Hdf5Data getH5Data(const std::string& filePath);
public:
	std::string Name;
private:
	TargetComprison *targetComprison;
};
//关于时间图数据的目标类型
class TargetTime :public Target{
public:
	TargetTime();
	~TargetTime();

public:
	virtual std::vector<float> getH5DataValue(const std::string& filePath);
	void setTimesRange(const double& min, const double& max);
	double getMaxTime();
	double getMinTime();
protected:
	double timesMin, timesMax;
};

class TargetTimeMax :public TargetTime{
public:
	virtual double getTagetValue(const std::string& filePath);
};

class TargetTimeMin :public TargetTime {
public:
	virtual double getTagetValue(const std::string& filePath);
};

class TargetTimeMean :public TargetTime {
public:
	virtual double getTagetValue(const std::string& filePath);
};

class TargetFrequency :public Target {
public:
	virtual double getTagetValue(const std::string& filePath) override;
	void setFrequencyRange(const double& max, const double& min);
	double getMaxFrequency();
	double getMinFrequency();
	std::vector<float> getH5DataValue(const std::string& filePath);

protected:
	virtual Hdf5Data getH5Data(const std::string& filePath) override;
private:
	double maxFrequency, minFrequency;
};
