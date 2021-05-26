#include "Struct2dData.h"

Struct2dData::Struct2dData(Hdf5Data& heData, const RunMod& mode):XYData(heData,mode){
}
Struct2dData::~Struct2dData(){
}
void Struct2dData::restorDeriveData(){
}
/**
* @brief Struct2dData::initXYRang 初始化数值区间
* @return bool
*/
bool Struct2dData::initXYRang(){
	if (posxSize < 2 || posySize < 2)
		return false;
	Data;; ListValuesPtr ListValues;
	bool ok = autoModGetSourceData(ListValues);
	if (!ok&&!ListValues&&ListValues->size())
		return false;
	auto it = ListValues->begin();
	Data::ValuesPtr IM1X = *it; it++;
	Data::ValuesPtr IM2X = *it;
	Rang xr, yr;
	//x
	auto itx = IM1X->begin();
	xr.min =0;
	itx = IM1X->end() - 1;
	xr.max = *itx;
	setXRang(xr);
	//y
	auto ity = IM2X->begin();
	yr.min = 0;
	ity = IM2X->end() - 1;
	yr.max = *ity;
	setYRang(yr);
	return true;
}
/**
* @brief Struct2dData::loadPoint
* @return bool
*/
bool Struct2dData::loadPoint(){
	Data::ListValuesPtr ListValues;
	//获取原始数据
	bool ok = autoModGetSourceData(ListValues);
	if (!ok&&!ListValues&&ListValues->size() == 0)
		return false;
	auto it = ListValues->begin();
	//获取横纵坐标的个数
	posxSize = (*it)->size(); it++;
	posySize = (*it)->size();
	//初始化范围
	initXYRang();
	initdata();
	return true;
}
/**
* @brief Struct2dData::initdata 初始化数据
* @return bool
*/
bool Struct2dData::initdata(){
	Data::ListValuesPtr ListValues;
	//获取原始数据
	bool ok = autoModGetSourceData(ListValues);
	if (!ok&&!ListValues&&ListValues->size() == 0)
		return false;
	allinfo.clear();
	auto it = ListValues->begin();
	Data::ValuesPtr IM1X = *it; it++;
	Data::ValuesPtr IM2X = *it; it++;
	Data::ValuesPtr datasetkmt = *it;
	std::vector<datasetkmtinfo> datasetkmtlist;
	//装入
	for (auto iterdataset = datasetkmt->begin(); iterdataset != datasetkmt->end();)
	{
		datasetkmtinfo _datasetkmtinfo;
		_datasetkmtinfo.data1 = *iterdataset; iterdataset++;
		_datasetkmtinfo.data2 = *iterdataset; iterdataset++;
		_datasetkmtinfo.data3 = *iterdataset; iterdataset++;
		_datasetkmtinfo.data4 = *iterdataset; iterdataset++;
		datasetkmtlist.push_back(_datasetkmtinfo);
	}
	//装入成功
	//获取所有点位
	ALLPointf.clear();
	ALLPointf.reserve(IM2X->size()*IM1X->size());
	for (auto y = 0; y < IM2X->size(); y++)
	{
		for (auto x = 0; x < IM1X->size();x++)
		{
		
			ALLPointf.push_back(QPointF(*(IM1X->begin() + x), *(IM2X->begin() + y)));
		}
	}
	allinfo.clear();
	for each(datasetkmtinfo i in datasetkmtlist)
	{
		allinfo[i.data3][i.data4].push_back(QPointF(*(IM1X->begin() + i.data1-1), *(IM2X->begin() + i.data2-1)));
	}
	return true;
}
unsigned int Struct2dData::findIndexFromXValueL(const float&x){
	return 0;
}