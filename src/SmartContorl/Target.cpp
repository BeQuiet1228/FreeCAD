#include "target.h"
#include "HDF5Reader/hdf5io.h"
Target::Target()
	:targetComprison(new TargetComprisonGreaterThan()),value(0)
{

}

Target::~Target()
{
	delete targetComprison;
}

/**
* 对比两个参数哪一个更优
* @brief Target::comparison
* @param const double & par1
* @param const double & par2
* @return bool 如果par1 更优返回 true
*/
bool Target::comparison(const double& par1, const double& par2)
{
	return targetComprison->comparison(par1, par2);
}


void Target::setTargetComprison(TargetComprison* com)
{
	this->targetComprison = com;
}

TargetComprison* Target::getTargetComprison()
{
	return targetComprison;
}

/**
* 获取数据集 根据设定的数据别名
* @brief Targer::getH5Data 
* @param const std::string & filePath
* @return std::vector<float>
*/
Hdf5Data Target::getH5Data(const std::string& filePath)
{
	Hdf5IO H5IO(filePath);
	H5IO.initHdf5Data();

	Hdf5Data data;
	for each (Hdf5Data d in H5IO.hdf5DataList) {
		if (d.petName == Name)
			data = d;
	}

	if (data.petName != Name)
	{
		std::cerr << "Targer::getH5Data not find pet name!" << std::endl;
	}
	return data;
}

TargetTime::TargetTime()
{

}

TargetTime::~TargetTime()
{

}

std::vector<float> TargetTime::getH5DataValue(const std::string& filePath)
{
	Hdf5Data data = getH5Data(filePath);
	if (data.listDataSet.size() != 1)
	{
		std::cerr << "TargetTime::getH5DataValue data is not Observe!" << std::endl;
		return std::vector<float>();
	}

	DataSet dataSet = data.listDataSet[0];
	std::vector<float> values;
	if (Hdf5IO::getValue(dataSet, values)) {
		return values;
	}
	else {
		std::cerr << "TargetTime::getH5DataValue Hdf5IO::getValue failde!" << std::endl;
		return std::vector<float>();
	}

}

void TargetTime::setTimesRange(const double& min, const double& max)
{
	this->timesMax = max;
	this->timesMin = min;
}

double TargetTime::getMaxTime()
{
	return timesMax;
}

double TargetTime::getMinTime()
{
	return timesMin;
}

double TargetTimeMax::getTagetValue(const std::string& filePath)
{
	std::vector<float> value = getH5DataValue(filePath);

	if (value.size() < 2)
		return 0.0;
	float max = value[1];
	for (int i = 1; i < value.size(); i = i+2) {
		if(value.at(i-1)<timesMin)
			continue;
		if(value.at(i-1)>timesMax)
			break;
		max = max < value.at(i) ? value.at(i) : max;
	}

	return max;
}

double TargetTimeMin::getTagetValue(const std::string& filePath)
{
	std::vector<float> value = getH5DataValue(filePath);

	if (value.size() < 2)
		return 0.0;
	float min = value[1];
	for (int i = 1; i < value.size(); i = i + 2) {
		if (value.at(i - 1) < timesMin)
			continue;
		if (value.at(i - 1) > timesMax)
			break;
		min = min > value.at(i) ? value.at(i) : min;
	}

	return min;
}

double TargetTimeMean::getTagetValue(const std::string& filePath)
{
	std::vector<float> value = getH5DataValue(filePath);

	if (value.size() < 2)
		return 0.0;
	double addValue = 0.0;
	int valueCount = 0;
	for (int i = 1; i < value.size(); i= i + 2) {
		if (value.at(i - 1) < timesMin)
			continue;
		if (value.at(i - 1) > timesMax)
			break;
		addValue += value.at(i);
		valueCount++;
	}

	return addValue/valueCount;
}

bool TargetComprisonGreaterThan::comparison(const double& par1, const double& par2)
{
	if (par1 > par2)
		return true;
	return false;
}

TargetComprisonApproach::TargetComprisonApproach()
	:expect(0)
{

}

bool TargetComprisonApproach::comparison(const double& par1, const double& par2)
{
	if (abs(par1 - expect) < abs(par2 - expect))
		return true;
	return false;
}

double TargetFrequency::getTagetValue(const std::string& filePath)
{
	std::vector<float> value = getH5DataValue(filePath);

	if (value.size() < 2)
		return 0.0;
	double f1 = value[0];
	double e1 = value[1];
	for (int i = 1; i < value.size(); i = i + 2) {
		if (e1 < value[i])
		{
			e1 = value[i];
			f1 = value[i - 1];
		}
	}

	double f2 = 0;
	double e2 = 0;
	{
		int i = 1;
		for (; i < value.size(); i = i + 2) {
			if (value.at(i - 1) < minFrequency)
				continue;
			break;
		}
		if (i >= value.size())
			return 0.0;
		e2 = value[i];
		f2 = value[i - 1];
		for (; i < value.size(); i = i + 2) {
			if (value.at(i - 1) > maxFrequency)
				break;
			if (e2 < value[i])
			{
				e2 = value[i];
				f2 = value[i - 1];
			}
		}
	}
	/*
	* 2022 .7.7
		f1 f2 将单位转换为GHz 否则差值过大时，temp容易出现零值
	*/
	f1 = f1 * 1e-9;
	f2 = f2 * 1e-9;
	double temp = exp(-abs(f1 - f2));
	double add = 0;

	for (int i = 1; i < value.size() - 2; i = i + 2) {
		add = add + ((1- value[i]/e1) * (value[i + 1] - value[i - 1]));
	}
#if 0
	return add * temp;
#else

	return add * temp / value[value.size() - 2];
#endif
}

void TargetFrequency::setFrequencyRange(const double& max, const double& min)
{
	maxFrequency = max;
	minFrequency = min;
}

double TargetFrequency::getMaxFrequency()
{
	return maxFrequency;
}

double TargetFrequency::getMinFrequency()
{
	return minFrequency;
}

std::vector<float> TargetFrequency::getH5DataValue(const std::string& filePath)
{
	Hdf5Data data = getH5Data(filePath);
	if (data.listDataSet.size() != 1)
	{
		std::cerr << "TargetFrequency::getH5DataValue data is not Observe!" << std::endl;
		return std::vector<float>();
	}

	DataSet dataSet = data.listDataSet[0];
	std::vector<float> values;
	if (Hdf5IO::getValue(dataSet, values)) {
		return values;
	}
	else {
		std::cerr << "TargetFrequency::getH5DataValue Hdf5IO::getValue failde!" << std::endl;
		return std::vector<float>();
	}
}

Hdf5Data TargetFrequency::getH5Data(const std::string& filePath)
{
	Hdf5IO H5IO(filePath);
	H5IO.initHdf5Data();

	Hdf5Data data;
	for each (Hdf5Data d in H5IO.hdf5DataList) {
		if (d.petName != Name)
			continue;
		if (d.headList.size() < 14)
			continue;
		//判断头信息中有fft
		if (d.headList[13].find("FFT") == std::string::npos)
			continue;	
		data = d;		
	}

	if (data.petName != Name)
	{
		std::cerr << "Targer::getH5Data not find pet name!" << std::endl;
	}
	return data;
}

double TargetTimeDouble::getTagetValue(const std::string& filePath)
{
	this->Name = name1;
	double t1 = getTarget(filePath);
	this->Name = name2;
	double t2 = getTarget(filePath);

	return t1 / t2;
}

void TargetTimeDouble::setType(const TargetType& t)
{
	this->targetType = t;
}

double TargetTimeDouble::getMaxTarget(const std::string& filePath)
{
	std::vector<float> value = getH5DataValue(filePath);

	if (value.size() < 2)
		return 0.0;
	float max = value[1];
	for (int i = 1; i < value.size(); i = i + 2) {
		if (value.at(i - 1) < timesMin)
			continue;
		if (value.at(i - 1) > timesMax)
			break;
		max = max < value.at(i) ? value.at(i) : max;
	}

	return max;
}

double TargetTimeDouble::getMiniTarget(const std::string& filePath)
{
	std::vector<float> value = getH5DataValue(filePath);

	if (value.size() < 2)
		return 0.0;
	float min = value[1];
	for (int i = 1; i < value.size(); i = i + 2) {
		if (value.at(i - 1) < timesMin)
			continue;
		if (value.at(i - 1) > timesMax)
			break;
		min = min > value.at(i) ? value.at(i) : min;
	}

	return min;
}

double TargetTimeDouble::getMeanTarget(const std::string& filePath)
{
	std::vector<float> value = getH5DataValue(filePath);

	if (value.size() < 2)
		return 0.0;
	double addValue = 0.0;
	int valueCount = 0;
	for (int i = 1; i < value.size(); i = i + 2) {
		if (value.at(i - 1) < timesMin)
			continue;
		if (value.at(i - 1) > timesMax)
			break;
		addValue += value.at(i);
		valueCount++;
	}

	return addValue / valueCount;
}

double TargetTimeDouble::getTarget(const std::string& filePath)
{
	switch (targetType)
	{
	case TargetTimeDouble::MAX:
		return getMaxTarget(filePath);
		break;
	case TargetTimeDouble::Mini:
		return getMiniTarget(filePath);
		break;
	case TargetTimeDouble::Mean:
		return getMeanTarget(filePath);
		break;
	default:
		return 0.0;
		break;
	}
}
