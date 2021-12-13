#include "Struct2dData.h"
/**
* @brief  Struct2dData::Struct2dData
* @param  Hdf5Data & heData  
* @param  const RunMod & mode  
* @return   
*/
Struct2dData::Struct2dData(Hdf5Data& heData, const RunMod& mode):XYData(heData,mode),istrue(false){
}
/**
* @brief  Struct2dData::~Struct2dData
* @return   
*/
Struct2dData::~Struct2dData(){
}
/**
* @brief  Struct2dData::restorDeriveData
* @return void  
*/
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
	auto itx = IM1X->begin(); itx++;//取第二个
	xr.min =*itx;
	itx = IM1X->end() - 1;
	xr.max = *itx;
	setXRang(xr);
	//y
	auto ity = IM2X->begin(); ity++;////取第二个
	yr.min = *ity;
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
	setXTag("Z(m)");
	setYTag("R(m)");
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
	for (auto iter= datasetkmt->begin();iter!=datasetkmt->end();)
	{
		unsigned __int64 x1 = *iter; iter++;
		unsigned __int64 x2 = *iter; iter++;
		unsigned __int64 x3 = *iter; iter++;
		unsigned __int64 x4 = *iter; iter++;

		std::list<unsigned __int64> rectPro = isAnAttribute(x3, StructData::RECTPROPER);
		std::list<unsigned __int64> linePro = isAnAttribute(x3,StructData::LINEPROPER);

		if (!rectPro.empty())
		{
			for each (auto var in rectPro)
				allinfo[x4][var].push_back(QPointF(*(IM1X->begin() + (x1 - 1)),*(IM2X->begin()+(x2-1))));
		}
		if (!linePro.empty())
		{
			for each (auto var in linePro)
				lineinfo[x4][var].push_back(QPointF(*(IM1X->begin()+(x1-1)),*(IM2X->begin()+(x2-1))));
		}
	}

	//存放全部点位
	ALLPointf.clear();
	ALLPointf.reserve(IM2X->size() * IM1X->size());
	for (auto y = 0; y < IM2X->size(); y++)
	{
		for (auto x = 0; x < IM1X->size(); x++)
		{

			ALLPointf.push_back(QPointF(*(IM1X->begin() + x), *(IM2X->begin() + y)));
		}
	}
	return true;
}
/**
* @brief  Struct2dData::findIndexFromXValueL
* @param  const float & x  
* @return unsigned int  
*/
unsigned int Struct2dData::findIndexFromXValueL(const float&x){
	return 0;
}
std::list<unsigned __int64> Struct2dData::isAnAttribute(unsigned __int64 p, StructData::PROPERTYPE sp)
{
	std::list<unsigned __int64> list;
#define CPM(a,b)\
	if((a)&(b)) list.push_back(b);

	switch (sp)
	{
	case StructData::RECTPROPER:
	{
		unsigned __int64 pro = p & 0xff;
		list.clear();

		CPM(pro,StructData::PERFECTCONDUCTOR);
		CPM(pro,StructData::CONDUCTORNEW);
		CPM(pro,StructData::DIOLECTRIC);
		CPM(pro,StructData::DIELECTIRANDCONDUCTANCE);
		CPM(pro,StructData::PERMEABILITY);
		CPM(pro,StructData::FREESPACE);
		CPM(pro,StructData::FOIL);
		//判断真空
		if (0 == pro)
		{
			list.push_back(0);
		}
		return list;
	}
	case StructData::LINEPROPER:
	{
		list.clear();
		unsigned __int64 linepro = p & 0xff00;
		
		CPM(linepro, 256);
		CPM(linepro, 512);
		CPM(linepro, 1024);
		CPM(linepro, 2048);
		CPM(linepro, 4096);
		CPM(linepro, 8192);
		CPM(linepro, 16384);
		CPM(linepro, 32768);
		CPM(linepro, 65536);

		return list;
	}
	}
}

Struct2dData::Struct2dData(Hdf5Data& heData, QPointF start, QPointF end, const RunMod& mode)
	:XYData(heData, mode),istrue(true)
{
	mstart = start;
	mend = end;
}