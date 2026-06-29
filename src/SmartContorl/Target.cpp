#include "target.h"
#include "HDF5Reader/hdf5io.h"
// ... (之前的代码保持不变)
#include <fstream>
#include <sstream>
#include <cstdlib>
#include <Windows.h>
#include <QDir>
#include <QImage>
#include <QPainter>
#include <QPen>
#include <QColor>
#include <QPointF>
#include <QString>
#include <QDateTime>
#include <QDebug>
#include <QFile>
#include <QByteArray>
#include <QCoreApplication>
#include "DataVisualization\StructData.h"
#include "DataVisualization\StructRender.h"
#include "DataVisualization\ParticleData.h"
#include "DataVisualization\ParticleRenderer.h"
#include <memory>
#include <cmath>
using namespace DV;
namespace DV {
	// 使用完全限定名来定义嵌套结构体的构造函数
	Data::Rang::Rang()
	{
		this->max = 0.0f;
		this->min = 0.0f;
	}

	Data::Rang::Rang(const float& _min, const float& _max)
	{
		this->max = _max;
		this->min = _min;
	}
}
// TargetPiMode 实现
TargetPiMode::TargetPiMode()
{
	this->Name = "PiModeTarget"; // 默认名称
	m_targetWheelCount = 0;
}

TargetPiMode::~TargetPiMode()
{
}
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

TargetComparisonProminence::TargetComparisonProminence()
: expect(0.0)
{
}
bool TargetComparisonProminence::comparison(const double& par1, const double& par2)
{
	int spokes1 = (int)par1;
	double concavity1 = par1 - spokes1;
	int spokes2 = (int)par2;
	double concavity2 = par2 - spokes2;
	int targetSpokes = (int)this->expect;
	int dist1 = std::abs(spokes1 - targetSpokes);
	int dist2 = std::abs(spokes2 - targetSpokes);
	if (dist1 != dist2) {
		return dist1 < dist2;
	}
	// === 第二层比较：凹陷度 (加时赛) ===
	if (std::abs(concavity1 - concavity2) > 0.0001) {
		return concavity1 > concavity2;
	}
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

void TargetPiMode::setTargetWheelCount(int count)
{
	m_targetWheelCount = count;
}

int TargetPiMode::getTargetWheelCount() const
{
	return m_targetWheelCount;
}

// 核心逻辑：调用 Python 并返回识别到的轮辐数量
double TargetPiMode::getTagetValue(const std::string& filePath)
{
	// 0. 准备画布和日志
	QString runPath = QDir::currentPath();
	QString historyDirName = "APhotoHistory";
	QString historyFullPath = runPath + "/" + historyDirName;
	QDir dir(historyFullPath);
	if (!dir.exists()) {
		dir.mkpath(".");
	}
	QFileInfo fileInfo(QString::fromStdString(filePath));
	QString baseName = fileInfo.completeBaseName(); // 获取不带后缀的文件名
	QString timeTag = QDateTime::currentDateTime().toString("MMdd_HHmmss_zzz");
	std::string imagePath = QString("%1/%2_%3.png").arg(historyFullPath).arg(baseName).arg(timeTag).toStdString();
	const int IMG_WIDTH = 1200;
	const int IMG_HEIGHT = 800;
	QImage finalImage(IMG_WIDTH, IMG_HEIGHT, QImage::Format_ARGB32);
	finalImage.fill(Qt::white); // 白底
	QPainter painter(&finalImage); 
	QString stepLogPath = QCoreApplication::applicationDirPath() + "/Debug_Step_Log.txt";
	std::ofstream stepLog(stepLogPath.toStdString(), std::ios::out | std::ios::unitbuf);
	try {
		stepLog << ">>> [Step 1] 开始处理: " << filePath << std::endl;
		Hdf5IO h5IO(filePath);
		h5IO.initHdf5Data();
		stepLog << ">>> [Step 2] Hdf5IO 初始化完成，共发现 " << h5IO.hdf5DataList.size() << " 个数据集" << std::endl;
		// =========================================================
		// [Part A] 绘制结构图 (背景层)
		// =========================================================
		QImage structImg;  // 结构图（层级高，在上）
		QImage partImg;    // 粒子图（层级低，在下）
		Data::Rang structXRange;
		Data::Rang structYRange;
		Hdf5Data h5DataStruct;
		bool foundStruct = false;
		for (const auto& data : h5IO.hdf5DataList) {
			if (data.name == "struct") {
				h5DataStruct = data;
				foundStruct = true;
				break;
			}
		}
		if (foundStruct) {
			auto structData = std::make_shared<StructData>(
				h5DataStruct, DirectionType::R_THETA,
				false, 0.0f, StructData::RunMod::SINGLE_THREAD
				);
			structData->loadPoint();
			structData->loadroom();
			// 实例化画家
			StructRender structRender(structData);
			structRender.setSize(QSize(IMG_WIDTH, IMG_HEIGHT));
			structRender.setDefaultRang();
			// 画图
			structRender.drawImage();
			structXRange = structRender.getXRang();
			structYRange = structRender.getYRang();
			structImg = structRender.getImage();
		}
		// =========================================================
		// [Part B] 绘制粒子图 (前景层) 
		// =========================================================
		Hdf5Data h5DataPart;
		bool foundParticle = false;
		// 1. 查找 PHASESPACE 数据
		for (const auto& data : h5IO.hdf5DataList) {
			if (data.name == "PHASESPACE") {
				h5DataPart = data;
				foundParticle = true;
				break;
			}
		}
		if (!foundParticle) {
			return 0.0;
		}
		// 2. 加载粒子点位
		auto particleData = std::make_shared<ParticleData>(h5DataPart);
		particleData->loadPoint();
		int pCount = particleData->particles.size();
		// 3. 只有粒子数大于0才画图
		if (pCount > 0) {
			ParticleRenderer particleRender(particleData);
			// 【重要】设置和结构图一样的大小，保证对齐
			particleRender.setSize(QSize(IMG_WIDTH, IMG_HEIGHT));
			// 自动设置范围 (理想情况下，它计算出的范围应该和结构图一致)
			// 设置样式
			particleRender.setXRang(structXRange);
			particleRender.setYRang(structYRange);
			particleRender.setParticleSize(3);
			particleRender.setAA(false);
			particleRender.setParticleColor(Qt::red);
			// 绘制
			particleRender.drawImage();
			// 4. 叠加到最终画布 (画在结构图上面)
			partImg = particleRender.getImage();
		}
		// =========================================================
		// 保存最终结果
		// =========================================================
		painter.drawImage(0, 0, partImg);
		painter.drawImage(0, 0, structImg);
		painter.end();
		bool saved = finalImage.save(QString::fromStdString(imagePath));
	}
	catch (const std::exception& e) {
		stepLog << ">>> [Fatal Error] " << e.what() << std::endl;
		return 0.0;
	}
	stepLog.close();
	// Python 调用部分
	const std::string pythonPath = "C:\\Users\\11231\\.conda\\envs\\yolov11\\python.exe";
	std::string command = "cmd /c \"\"" + pythonPath + "\" model_runner.py \"" + imagePath + "\"\"";
	int ret = system(command.c_str());
	double identifiedResult = readPythonResult("default_model_output.json");
	// 写主日志
	QString logPath = QCoreApplication::applicationDirPath() + "/Spoke_Log.txt";
	std::ofstream log(logPath.toStdString(), std::ios::app);
	if (log.is_open()) {
		log << QDateTime::currentDateTime().toString("yyyy-MM-dd HH:mm:ss").toStdString()
			<< " | File: " << filePath
			<< " | Result: " << identifiedResult << std::endl;
	}
	return identifiedResult;
}

// 简单的结果读取器
double TargetPiMode::readPythonResult(const std::string& resultPath)
{
	std::ifstream inputFile(resultPath);
	if (!inputFile.is_open()) {
		return 0.0;
	}
	std::stringstream buffer;
	buffer << inputFile.rdbuf();
	std::string content = buffer.str();
	inputFile.close();
	if (content.empty()) return 0.0;
	int spokes = 0;
	double concavity = 0.0;
	try {
		// 1. 手动查找 "spokes"
		size_t posSpokes = content.find("\"spokes\"");
		if (posSpokes != std::string::npos) {
			// 找到冒号
			size_t posColon = content.find(":", posSpokes);
			// 找到逗号或大括号结束
			size_t posEnd = content.find_first_of(",}", posColon);

			if (posColon != std::string::npos && posEnd != std::string::npos) {
				std::string numStr = content.substr(posColon + 1, posEnd - posColon - 1);
				spokes = std::stoi(numStr);
			}
		}

		// 2. 手动查找 "concavity"
		size_t posConcavity = content.find("\"concavity\"");
		if (posConcavity != std::string::npos) {
			size_t posColon = content.find(":", posConcavity);
			size_t posEnd = content.find_first_of(",}", posColon);

			if (posColon != std::string::npos && posEnd != std::string::npos) {
				std::string numStr = content.substr(posColon + 1, posEnd - posColon - 1);
				concavity = std::stod(numStr);
			}
		}
	}
	catch (...) {
		// 解析出错保底返回
		return 0.0;
	}
	return (double)spokes + concavity;
}