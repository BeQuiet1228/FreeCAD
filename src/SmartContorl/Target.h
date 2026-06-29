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
//2026.1.16新增
class TargetComparisonProminence : public TargetComprison {
public:
	TargetComparisonProminence();
	virtual ~TargetComparisonProminence() {}

public:
	double expect; // 目标轮辐数 (例如 10.0)
	// 重写比较逻辑
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
public:
	double getG() {
		return g;
	};
	void setG(const double& g) {
		this->g = g;
	};
private:
	double g;
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

class TargetTimeDouble :public TargetTime {
public:
	std::string name1,name2;
	enum TargetType{
		MAX = 0,
		Mini,
		Mean
	};
public:
	virtual double getTagetValue(const std::string& filePath);
	void setType(const TargetType & t);
private:
	TargetType targetType;
	double getMaxTarget(const std::string& filePath);
	double getMiniTarget(const std::string& filePath);
	double getMeanTarget(const std::string& filePath);
	double getTarget(const std::string& filePath);
};
// 新增：YOLO π模识别目标类
class TargetPiMode : public Target {
public:
	TargetPiMode();
	virtual ~TargetPiMode();
public:
	// 重写获取目标值的函数，这里将调用 Python
	virtual double getTagetValue(const std::string& filePath) override;
	virtual std::vector<float> getH5DataValue(const std::string& filePath) override { return std::vector<float>(); }

	void setTargetWheelCount(int count);
	int getTargetWheelCount() const;
protected:
	// 读取 Python 生成的结果文件
	double readPythonResult(const std::string& resultPath);

private:
	int m_targetWheelCount; // 期望识别到的轮辐数量
};