#include "InterSpaceData.h"
namespace DV {
	InterspaceData::InterspaceData(Hdf5Data& h5Data, const RunMod& mod /*= SINGLE_THREAD*/)
		:TimeData(h5Data, mod)
	{

	}

	unsigned int InterspaceData::findIndexFromXValueL(const float& x)
	{
		auto xr = getXRang();
		//如果范围小于最小值，那么直接返回第一个数值的索引
		if (x < xr.min)
			return 0;
		if (x > xr.max)
			return getPointSize() - 1;

		unsigned int fm, am;
		fm = 0;
		am = getPointSize() - 1;
		unsigned int index;

		while ((am - fm) > 1) {
			index = (am - fm) / 2;
			getPoint(index + fm).x() > x ? am = index + fm : fm += index;
		}
		return fm;
	}

	/**
	* @brief TimeData::getPoints 获取Points指针
	* @return Data::ValuesPtr
	*/
	void InterspaceData::dataToFFT(Data::Rang xr) {
		Data::ValuesPtr nowPoints(new std::vector<float>);
		int tmp = nowPoints.use_count();
		//确定现在的左右边界的index
		int n = (*points).size() / 2;
		int indexL = findIndexFromXValueR(xr.min);
		int indexR = findIndexFromXValueL(xr.max);
		indexL = indexL == 1 ? 0 : indexL;//由于函数会自动加一，但是在索引为0时，找不到左值，所以会在findIndexFromXValueL中韩慧0，在通过findIndexFromXValueR进行加1
		indexR = indexR == n ? n - 1 : indexR;//由于函数findIndexFromXValueL在index大于n时会返回n，但时points中最大索引为n-1
		float rangStep = 1 / ((points->at(indexR * 2) - points->at(indexL * 2)));//采样频率间隔为时间采样的倒数

		//将X和Y轴的数据分别做处理
		std::vector<float> Xdata;
		std::vector<float> Ydata;

		for (int index = indexL; index <= indexR; ++index) {
			Xdata.emplace_back(points->at(index * 2));
			Ydata.emplace_back(points->at(index * 2 + 1));
		}

		fft(Ydata, rangStep);//主要的FFT程序，对Y数据进行FFT变换

		int num = (indexR - indexL) / 3;//空间图在原数据点上缩小3倍
		for (int index = 0; index <= num; ++index) {
			(*nowPoints).emplace_back(index * rangStep);
			(*nowPoints).emplace_back(Ydata[index]);
		}
		points = nowPoints;
		updateData(InterspaceDataFFT, getNewXTag(), getYTag());
		addHeadlistStr(11, "FFT");
	}

	std::string InterspaceData::getNewXTag() {
		QString str = QString::fromStdString(headList.at(0));
		QStringList sl = str.split("=");

		str = sl.at(1);
		sl = str.split("$");
		QString temp = sl.at(1);
		
		std::string newXTag = " (cyc/m)";
		if (temp == "CYLINDRICAL")
			newXTag = "Z" + newXTag;
		else if (temp == "POLAR")
			newXTag = "R" + newXTag;
		else if (temp == "CARTESIAN")
			newXTag = "R" + newXTag;

		return newXTag;
	}

	//将当前的数据添加到h5文件中
	bool InterspaceData::addNewGroup() {
		if (headList == h5Data.headList) {
			return false;
		}

		Hdf5Data* newh5Data = new Hdf5Data(h5Data);
		newh5Data->addSubGroup("Group_grid", "2D_rangers", this->points, headList);
		delete newh5Data;
		return true;
	}
	
};
