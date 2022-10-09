#include "TimeAlgData.h"
#include "DataInformationGetter.h"
#include <fstream>

#define REAL 0
#define IMAG 1

namespace DV {
	TimeAlgData::TimeAlgData(Hdf5Data& h5Data, const RunMod& mod /*= SINGLE_THREAD*/)
		:TimeData(h5Data, mod)
	{

	}

	TimeAlgData::~TimeAlgData()
	{

	}

	/**
	* @brief TimeData::loadPoint 载入点数据
	* @return bool
	*/
	bool TimeAlgData::loadPoint()
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

	/**
	* @brief TimeData::dataToFFT FFT算法
	* @return 
	*/
	void TimeAlgData::dataToFFT(Data::Rang xr) {
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
	void TimeAlgData::fft(std::vector<float>& initdata, float fs) {
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

	void TimeAlgData::dataToGather(Data::Rang xr) {
		Data::ValuesPtr nowPoints(new std::vector<float>);

		//确定现在的左右边界的index
		int n = (*points).size() / 2;
		int indexL = findIndexFromXValueR(xr.min);
		int indexR = findIndexFromXValueL(xr.max);
		indexL = indexL == 1 ? 0 : indexL;//由于函数会自动加一，但是在索引为0时，找不到左值，所以会在findIndexFromXValueL中韩慧0，在通过findIndexFromXValueR进行加1
		indexR = indexR == n ? n - 1 : indexR;//由于函数findIndexFromXValueL在index大于n时会返回n，但时points中最大索引为n-1
		Data::Rang XScope(points->at(indexL * 2), points->at(indexR * 2));

		float maxY = 0;
		for (int index = indexL; index <= indexR; ++index) {
			float tmp = abs(points->at(index * 2 + 1));
			maxY = std::max(maxY, tmp);
		}

		float maxYOrder = maxY / 50.0;
		int indexOrder = 0;
		for (int index = indexR; index >= indexL; --index) {
			if (abs(points->at(index * 2 + 1)) > maxYOrder) {
				indexOrder = index;
				break;
			}
		}

		indexOrder = std::min(indexOrder + (indexOrder - indexL) / 10, indexR);
		for (int index = indexL; index <= indexOrder; ++index) {
			(*nowPoints).emplace_back(points->at(index * 2));
			(*nowPoints).emplace_back(points->at(index * 2 + 1));
		}

		points = nowPoints;
		addHeadlistStr(13, XScope, "gather");
		updateData(gatherData, getXTag(), getYTag());
	}

	Data::ValuesPtr TimeAlgData::getPointsPtr() {
		return this->points;
	}

	void TimeAlgData::updateData(int alogrithm, std::string xTag, std::string yTag) {
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

	void TimeAlgData::updatePoint(Data::ValuesPtr point) {
		this->points = point;
	}

	//将当前的数据添加到h5文件中
	bool TimeAlgData::addNewGroup() {
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

	void TimeAlgData::saveAs(std::string path, SaveMod mod)
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
	void TimeAlgData::addHeadlistStr(int index, Data::Rang XScope, std::string str) {
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
