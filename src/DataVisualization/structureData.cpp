#include "structureData.h"
structureData::structureData(Hdf5Data& h5Data, const RunMod &mod)
	:Data(h5Data, mod)
{

}
void structureData::restorDeriveData()
{

}

structureData::~structureData()
{
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
	pointi1mx = *it; 
	pointXSize = (*it)->size();//获取I1MX的数据总数
	it++;
	pointi2mx = *it;
	pointYsize = (*it)->size();//获取I2MX的数据总数
	it++;
	pointi3mx = *it;//获取I3MX的数据总数
	it++;
	pointdatasetkmt = *it;
	//初始化范围
	initXYRang();
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
	return true;
}
/**
* @brief structureData::GetAllCutspace 获取切割的所有空间容器
* @return QVector<QRectF>
*/
QVector<QRectF> structureData::GetAllCutspace()
{
	//获取全部需要切割的空间
	QVector<QRectF> list;
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
	//获取dataSetKmt里的全部数据
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
		if (1 == var.point3&&var.point1 < pointXSize)
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