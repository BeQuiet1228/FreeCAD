#include "TimeData.h"
#include "DataInformationGetter.h"
#include <fstream>

#define REAL 0
#define IMAG 1

namespace DV {
	TimeData::TimeData(Hdf5Data& h5Data, const RunMod& mod /*= SINGLE_THREAD*/)
		:XYData(h5Data, mod)
	{

	}

	TimeData::~TimeData()
	{

	}

	void TimeData::restorDeriveData()
	{

	}

	/**
	* @brief TimeData::loadPoint 载入点数据
	* @return bool
	*/
	bool TimeData::loadPoint()
	{
		Data::ListValuesPtr listValues;
		bool ok = autoModGetSourceData(listValues);//获取原始数据到listValues地址空间中

		if (!ok || !listValues || listValues->size() == 0)
			return false;
		points = *(listValues->begin());//交付数据给points
		setPointSize(points->size() / 2);
		//初始化范围
		initXYRang();

		//由于在initInformation中做过错误判断，所以这里不需要再做判断
		QString str = QString::fromStdString(headList.at(0));
		QStringList sl = str.split("$");
		if (sl.at(3).toStdString().find("Frequency") != std::string::npos) {
			this->FunOfAlogrithm = TimeDataForFFT;
		}
		else {
			this->FunOfAlogrithm = InitData;
		}

		return true; 
	}

	std::string TimeData::getInformationTitle()
	{
		std::string title;
		const std::string end = "  ";
		title += "观察分量:";
		title += DataInformationGetter::getObserveParam(headList.at(13)) + end;
		title += "观测面:";
		title += DataInformationGetter::getObserveFace(headList.at(15)) + end;

		return title;
	}

	/**
	* @brief TimeData::getPoint 根据索引给出一个点
	* @param const int & index
	* @return QPointF
	*/
	QPointF TimeData::getPoint(const unsigned int& index)
	{
		if (index >= getPointSize())
		{
			QPointF p;
			return p;
		}
		return getPointHard(index);
	}

	/**
	* @brief TimeData::getPointHard 根据索引给出一个点，这个函数不会判断容器边界，谨慎使用。
	* @param const unsigned int & index
	* @return QPointF
	*/
	QPointF TimeData::getPointHard(const unsigned int& index)
	{
		QPointF point;
		point.setX(points->at(index * 2));
		point.setY(points->at(index * 2 + 1));
		return point;
	}

	/**
	* @brief TimeData::findIndexFromXValueL 通过x轴的值查找最近的索引，靠近左边
	* @param const float & x
	* @return unsigned int
	*/
	unsigned int TimeData::findIndexFromXValueL(const float& x)
	{
		auto xr = getXRang();
		//如果范围小于最小值，那么直接返回第一个数值的索引
		if (x < xr.min)
			return 0;

		double step = xr.length() / getPointSize();
		unsigned int index = (x - xr.min) / step;
		//如果索引超出范围则返回0
		if (index > getPointSize())
			return getPointSize();
		return index;
	}

	/**
	* @brief TimeData::initXYRang 初始化xy的范围
	* @return bool
	*/
	bool TimeData::initXYRang()
	{
		if (getPointSize() < 2)
			return false;

		//获取x轴的范围
		//由于数据是均匀分布的，直接取头尾即可
		Rang xr, yr;
		auto iter = points->begin();
		xr.min = *iter;
		iter = points->end();
		iter -= 2;
		xr.max = *iter;

		//y轴范围只会一个一个比 QAQ
		int index = 1;
		yr.max = yr.min = points->at(index);
		float temp = 0;
		for (; index <= points->size(); index += 2)
		{
			temp = points->at(index);
			if (yr.max < temp)
				yr.max = temp;
			else if (yr.min > temp)
				yr.min = temp;
		}
		//如果y轴范围太小，则将数据置于中心
		if (abs(yr.min - yr.max) < 1e-36)
		{
			yr.min -= yr.min*0.0001 + 100;
			yr.max += yr.max*0.0001 + 100;
		}

		setXRang(xr);
		setYRang(yr);
		return true;

	}

	/**
	* @brief TimeData::dataToFFT FFT算法
	* @return 
	*/
	void TimeData::dataToFFT(Data::Rang xr) {
		Data::ValuesPtr nowPoints(new std::vector<float>);

		//确定现在的左右边界的index
		int n = (*points).size() / 2;
		int indexL = findIndexFromXValueR(xr.min);
		int indexR = findIndexFromXValueL(xr.max);
		indexL = indexL == 1 ? 0 : indexL;//由于函数会自动加一，但是在索引为0时，找不到左值，所以会在findIndexFromXValueL中韩慧0，在通过findIndexFromXValueR进行加1
		indexR = indexR == n ? n - 1 : indexR;//由于函数findIndexFromXValueL在index大于n时会返回n，但时points中最大索引为n-1
		Data::Rang XScope(points->at(indexL * 2), points->at(indexR * 2));
		float fs = 1 / ((points->at(indexR * 2) - points->at(indexL * 2)) * pow(10, -9));//采样频率间隔为时间采样的倒数

		//将X和Y轴的数据分别做处理
		std::vector<float> Xdata;
		std::vector<float> Ydata;
		
		for (int index = indexL; index <= indexR; ++index) {
			Xdata.emplace_back(points->at(index * 2));
			Ydata.emplace_back(points->at(index * 2 + 1));
		}

		fft(Ydata, fs);//主要的FFT程序，对Y数据进行FFT变换

		int num = (indexR - indexL) / 16;
		for (int index = 0; index <= num; ++index) {
			(*nowPoints).emplace_back(index * fs);
			(*nowPoints).emplace_back(Ydata[index]);
		}
		points = nowPoints;
		addHeadlistStr(13, XScope, "FFT");
		updateData(TimeDataForFFT, "Frequency(Hz)", getYTag());
	}

	/**
	* @brief TimeData::fft 对数据进行FFT处理
	*/
	void TimeData::fft(std::vector<float>& initdata, float fs) {
		/*
		*fftw_complex 是FFTW自定义的复数类，不调用<complex>
		*/
		int n = initdata.size();
		fftw_complex* in = (fftw_complex*)fftw_malloc(sizeof(fftw_complex) * n);
		fftw_complex* out = (fftw_complex*)fftw_malloc(sizeof(fftw_complex) * n);

		//初始化类型 in
		for (int i = 0; i < n; i++) {
			in[i][REAL] = initdata[i];
			in[i][IMAG] = 0;
		}

		//定义plan，包含序列长度、输入序列、输出序列、变换方向、变换模式
		fftw_plan plan = fftw_plan_dft_1d(n, in, out, FFTW_FORWARD, FFTW_ESTIMATE);

		//对于每个plan，应当"一次定义 多次使用"，同一plan的运算速度极快
		fftw_execute(plan);

		//销毁plan
		fftw_destroy_plan(plan);

		float divide = n / 2;
		for (int i = 0; i < n; i++) {
			initdata[i] = sqrt(out[i][REAL] * out[i][REAL] + out[i][IMAG] * out[i][IMAG]);
			initdata[i] /= divide;
			initdata[i] /= fs;
		}
		initdata[0] /= 2.0;

		//释放out
		fftw_free(out);
	}

	Data::ValuesPtr TimeData::getPointsPtr() {
		return this->points;
	}

	void TimeData::updateData(int alogrithm, std::string xTag, std::string yTag) {
		setPointSize(points->size() / 2);
		initXYRang();//更改数据范围
		FunOfAlogrithm = alogrithm;//更新FFT标识符

		//更新坐标Tag
		std::string initxTag = getXTag();
		std::string inityTag = getYTag();
		if (!xTag.empty()) {
			setXTag(xTag);
		}
		if (!yTag.empty()) {
			setYTag(yTag);
		}

		for (auto& sh : headList) {
			auto index = sh.find(initxTag);
			if (index != std::string::npos) 
				sh.replace(index, initxTag.size(), getXTag());

			index = sh.find(inityTag);
			if (index != std::string::npos)
				sh.replace(index, inityTag.size(), getYTag());
		}
	}

	void TimeData::updatePoint(Data::ValuesPtr point) {
		this->points = point;
	}

	//将当前的数据添加到h5文件中
	bool TimeData::addNewGroup() {
		if (headList == h5Data.headList) {
			return false;
		}

		Group tmpgroup;
		try {
			tmpgroup = h5Data.hdf5File->openGroup("Group_grid").openGroup("2D_observe");
		}
		catch (...) {
			std::cerr << "open group fail" << std::endl;
		}

		Hdf5IO::addSubGroup(h5Data, tmpgroup, *points, headList);

		return true;
	}

	void TimeData::saveAs(std::string path, SaveMod mod)
	{
		QDir dir(QString::fromStdString(path));

		bool isGood = dir.exists();
		int res = -1;
		if (!isGood || mod == NEWFLODER)
		{
			res = Hdf5IO::creatNewH5File(path);
		}

		Hdf5IO* temp = new Hdf5IO(path);
		Hdf5Data* newh5Data = new Hdf5Data(h5Data);
		int groupSize = newh5Data->group.getNumObjs();
		std::string groupName = "DataGroup" + QString::number(groupSize).toStdString();
		Hdf5IO::addNewGroup(*temp, *newh5Data, *points, headList);
		
		if (-1 != res)
			res = Hdf5IO::closeH5File(res);
		delete temp;
		delete newh5Data;
	}

	//生成新的headList
	void TimeData::addHeadlistStr(int index, Data::Rang XScope, std::string str) {
		if (headList.size() < index + 1) {
			std::cerr << "Not have this index of attribute" << std::endl;
			return;
		}

		std::string& headstr = headList.at(index); 
		
		std::string addStr = " " + str + " " + std::to_string(XScope.min) + " ~ " + std::to_string(XScope.max);

		int i = headstr.size() - 1;
		while (headstr[i] == ' ') {
			--i;
		}
		headstr.insert(i + 1, addStr);
	}
};
