#include "structureData.h"
structureData::structureData(Hdf5Data& h5Data, const RunMod &mod)
	:XYData(h5Data, mod)
{

}
void structureData::restorDeriveData()
{

}
structureData::~structureData()
{
	vacuo_vector.clear();
	conduit_vector.clear();
	datakmtinfo.clear();
	R_val.clear();
	rand_val.clear();
}
/**
* @brief structureData::loadPoint 载入点数据
* @return bool
*/
bool structureData::loadPoint()
{
	Data::ListValuesPtr listValues;
	bool ok = autoModGetSourceData(listValues);//获取原始数据
	if (!ok && !listValues && listValues->size() == 0)
		return false;
	auto it = (listValues->begin());
	pointXSize = (*it)->size();//获取I1MX的数据总数
	it++;
	pointYsize = (*it)->size();//获取I2MX的数据总数
	it++;
	//初始化范围
	initXYRang();
	loadrectpoint();
	return true;
}
/**
* @brief structureData::initXYRang 初始化横纵坐标的取值范围
* @return bool
*/
bool structureData::initXYRang(){
	if (pointXSize < 2||pointYsize<2)
		return false;
	//获取x轴的范围
	Rang xr, yr;
	
	/***********************************************************/
	//获取H5文件中取到的数据
	Data::ListValuesPtr listValues;
	bool ok = autoModGetSourceData(listValues);//获取原始数据
	if (!ok && !listValues && listValues->size() == 0)
		return false;
	auto it = (listValues->begin());
	Data::ValuesPtr pointi1mx = *it;
	it++;
	Data::ValuesPtr pointi2mx = *it;
	/*********************************************************/

	auto iterx = pointi1mx->begin();
	xr.min = *iterx;
	iterx = pointi1mx->end();
	iterx -= 1;
	xr.max = (*iterx);
	//获取y轴的范围
	
	auto itery=pointi2mx->begin();
	yr.min = *itery;
	itery = pointi2mx->end();
	itery -= 1;
	yr.max = *itery;
	setXRang(xr);
	setYRang(yr);
	return true;
}
/**
* @brief structureData::loadrectpoint 加载内部切割的矩形空间
* @return bool
*/
bool structureData::loadrectpoint(){
	if (pointXSize<2||pointYsize<2)
	{
		return false;
	}
	//获取真空坐标，和导管坐标
	vacuo_vector.clear();
	conduit_vector.clear();
	//获取全部切割的空间
	QVector<QRectF> list;
	list=GetAllCutspace();
	//获取datakmtinfo的信息
	GetdatasetKmt();
	//datakmtnifo获取成功，填充真空和导管队列
	fileproperty(list);
	//真空和导管队列装入完成
	//填充给圆柱坐标系需要的信息
	fileCylindrical_info();
	return true;
}
/**
* @brief structureData::GetAllCutspace 获取切割的所有空间容器
* @return QVector<QRectF>
*/
QVector<QRectF> structureData::GetAllCutspace()
{
	QVector<QRectF> list;
	//获取全部需要切割的空间

	/********************************************/
	//获取从H5F文件中获取到的数据
	Data::ListValuesPtr listValues;
	bool ok = autoModGetSourceData(listValues);//获取原始数据
	if (!ok && !listValues && listValues->size() == 0)
		return list;
	auto it = (listValues->begin());
	Data::ValuesPtr pointi1mx = *it; it++;
	Data::ValuesPtr pointi2mx = *it; it++;
	/*Data::ValuesPtr pointi3mx = *it; it++;
	Data::ValuesPtr pointdatasetkmt = *it;*/
	/********************************************/
	
	//开始获取
	auto iterleft = pointi1mx->begin();
	auto iterRight = pointi1mx->begin() + 1;
	auto iterTop = pointi2mx->begin();
	auto iterbottom = pointi2mx->begin() + 1;
	for (auto x = 0; x < pointXSize - 1; x++)
	{
		iterTop = pointi2mx->begin();
		iterbottom = pointi2mx->begin() + 1;
		for (auto y = 0; y < pointYsize - 1; y++)
		{
			QRectF temp;//介值
			temp.setLeft(*iterleft);
			temp.setRight(*iterRight);
			temp.setTop(*iterTop);
			temp.setBottom(*iterbottom);
			list.push_back(temp);
			iterTop++;
			iterbottom++;
		}
		iterleft++;
		iterRight++;
	}
	return list;
}
/**
* @brief structureData::GetdatasetKmt 获取datasetKmt中需要的数据 
* @return QVector<DaTaKmt> 相关数据的队列
*/
QVector<DaTaKmt> structureData::GetdatasetKmt()
{
	//获取全部需要切割的空间
	/*******************************************************/
	//获取从H5F文件中的到的数据
	Data::ListValuesPtr listValues;
	bool ok = autoModGetSourceData(listValues);//获取原始数据
	if (!ok && !listValues && listValues->size() == 0)
		return datakmtinfo;
	//获取dataSetKmt里的全部数据
	auto it = listValues->begin();
	
	Data::ValuesPtr pointi1mx = *it; it++;
	Data::ValuesPtr pointi2mx = *it; it++;
	Data::ValuesPtr pointi3mx = *it; it++;
	Data::ValuesPtr pointdatasetkmt = *it;
	/*******************************************************/

	auto iterkmt = pointdatasetkmt->begin();
	for (; iterkmt != pointdatasetkmt->end();)
	{
		DaTaKmt temp;
		//坐标1
		temp.point1 = *iterkmt;
		iterkmt++;
		//坐标2
		temp.point2 = *iterkmt;
		iterkmt++;
		//坐标3
		temp.point3 = *iterkmt;
		iterkmt++;
		//属性
		temp.pointproperty = *iterkmt;
		iterkmt++;
		datakmtinfo.push_back(temp);
	}
	return datakmtinfo;
}
/**
* @brief structureData::fileproperty  填充不同属性的切割空间
* @param QVector<QRectF> list 传入整个坐标系切割的空间
* @return void
*/
void structureData::fileproperty(QVector<QRectF> list)
{
	for each (DaTaKmt var in datakmtinfo)
	{
		if (1 == var.point3&&var.point1 < pointXSize-1)
		{
			switch (var.pointproperty)
			{
			case 3:
			{
				//导管
				conduit_vector.push_back(list[(var.point1 - 1)*(pointYsize - 1) + var.point2 - 1]);
			}
				break;
			case 1024:
			{
				//真空
				vacuo_vector.push_back(list[(var.point1 - 1)*(pointYsize - 1) + var.point2 - 1]);

			}
				break;
			}
		}
	}
}
/**
* @brief structureData::GetConduitPoint 获取导管所有的坐标
* @return QVector<QRectF> 
*/
QVector<QRectF> structureData::GetConduitPoint()
{
	return conduit_vector;
}
/**
* @brief structureData::Get_R_val 获取刻度队列
* @return QVector<qreal>
*/
QVector<qreal> structureData::Get_R_val()
{
	return R_val;
}
/**
* @brief structureData::Get_rand_val 获取需要切割的角度
* @return QVector<qreal>
*/
QVector<qreal> structureData::Get_rand_val()
{
	return rand_val;
}
/**
* @brief structureData::fileCylindrical_info 填充圆柱图需要的信息
* @return void
*/
void structureData::fileCylindrical_info()
{

	R_val.clear();
	rand_val.clear();
	
	Data::ListValuesPtr listValues;
	bool ok = autoModGetSourceData(listValues);//获取原始数据
	if (!ok && !listValues && listValues->size() == 0)
		return ;
	//获取dataSetKmt里的全部数据
	auto it = listValues->begin();

	Data::ValuesPtr pointi1mx = *it; it++;
	Data::ValuesPtr pointi2mx = *it; it++;
	Data::ValuesPtr pointi3mx = *it; it++;
	Data::ValuesPtr pointdatasetkmt = *it;

	QVector<qreal> _r_val;

	auto iter2mx = pointi2mx->begin();
	for (;iter2mx!=pointi2mx->end();iter2mx++)
	{
		_r_val.push_back(*iter2mx);
	}
//#define _DEBUG_
#ifdef _DEBUG_
	for (auto i = 0; i < _r_val.size();i++)
	{
		printf("%d---%f\n", i, _r_val[i]);
	}
#undef _DEBUG_
#endif
	//填充需要切割的角度
	for (auto iter3mx = pointi3mx->begin(); iter3mx != pointi3mx->end(); iter3mx++)
	{
		rand_val.push_back(*iter3mx);
	}
	
	for (auto i = 0; i < _r_val.size();i++)
	{
		R_val.push_back(0);
	}
	//根据导管和真空两种参数填入R_val
	for each (DaTaKmt var in datakmtinfo)
	{
		if (var.point1==pointXSize/2)
		{
			switch (var.pointproperty)
			{
			case 3:
			{
				//导管
				R_val[var.point2] = _r_val[var.point2];
			}
				break;
			case 1024:
			{
				//真空
			}
				break;
			}
		}
	}
//#define _DEBUG_
#ifdef _DEBUG_
	for each (qreal var in R_val)
	{
		printf("%f\n", var);
	}
#undef _DEBUG_
#endif
}
