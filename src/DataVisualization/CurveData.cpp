#include "CurveData.h"
#include <iostream>

DV::CurveData::CurveData()
	:TimeData(Hdf5Data(), SINGLE_THREAD)
{

}

DV::CurveData::~CurveData()
{

}

bool DV::CurveData::loadPoint()
{
	return true;
}

std::string DV::CurveData::getInformationTitle()
{
	return "";
}

void DV::CurveData::setPoints(Data::ValuesPtr points)
{
	this->points = points;
	setPointSize(points->size() / 2);
	initXYRang();
}

void DV::CurveData::setParValues(const ParValues& pars)
{
	//如果数据量不匹配,则不予设置
	//以免后面取点时出现越界
	for (auto iter = pars.begin(); iter != pars.end(); iter++)
	{
		if (iter->second.size() < getPointSize())
			return;
	}
	parValues = pars;
}

DV::CurveData::ParValues DV::CurveData::getParValues()
{
	return parValues;
}

std::list<std::shared_ptr<DV::CurveData>> DV::CurveData::Hdf5DataToListCurveData(Hdf5Data& h5d, const int& index)
{
	//获取参数个数
	std::string  temp = h5d.headList[1];
	temp = H5DataHead::getAttribute(temp);
	int varCount = std::stoi(temp);

	//获取目标函数值个数
	temp = h5d.headList[2];
	temp = H5DataHead::getAttribute(temp);
	int functionCount = std::stoi(temp);

	//获取一共有多少列
	int row = functionCount + varCount;

	//生成参数列表
	std::vector<std::string> valueNames;
	temp = H5DataHead::getAttribute(h5d.headList[3]);
	QStringList vars = QString::fromStdString(temp).simplified().split(' ');
	for (auto iter = vars.begin(); iter != vars.end(); iter++)
	{
		valueNames.push_back(iter->toStdString());
	}

	for (int i = 0; i < functionCount; i++)
	{
		valueNames.push_back("F" + std::to_string(i));
	}
	
	std::list<std::shared_ptr<CurveData>> datas;
	for (auto iter = h5d.listDataSet.begin(); iter != h5d.listDataSet.end(); iter++)
	{
		auto data = Hdf5DataSetToCurveData(*iter, valueNames, row, index);
		datas.push_back(data);
	}

	return datas;
}

std::shared_ptr<DV::CurveData> DV::CurveData::Hdf5DataSetToCurveData(DataSet& dataset, const std::vector<std::string> valueNames, const int& row,
	const int& index)
{
	VectorF values;
	Hdf5IO::getValue(dataset, values);

	std::vector<std::vector<float>> tempData;
	for (int i = 0; i < row; i++)
	{
		tempData.push_back(std::vector<float>());
		tempData[i].reserve(values.size() / 5 + 2);
	}
		
	for (int i = row -1; i < values.size(); i+=row)
	{
		for (int j = 0; j < row; j++)
		{
			tempData[j].push_back(values[i - (row - 1 - j)]);
		}
	}

	std::shared_ptr<CurveData> curveData(new CurveData());

	/*
	* 优化算法的数据中，横坐标是优化次数，写入数据的时候没有写入次数数据
	* 所以这里需要构造次数数据
	*/

	{
		auto points = Data::ValuesPtr(new Data::Values());
		std::vector<float>& pointYs = tempData[index];
		points->reserve(pointYs.size() * 2);
		int x = 1;
		for (auto iter = pointYs.begin(); iter != pointYs.end(); iter++)
		{
			points->push_back(x);
			points->push_back(*iter);
			x++;
		}
		curveData->setPoints(points);
	}


	ParValues parVlues;
	for (int i = 0; i < tempData.size(); i++)
	{
		parVlues[QString::fromStdString(valueNames[i])] = tempData[i];
	}
	curveData->setParValues(parVlues);

	return curveData;
}

