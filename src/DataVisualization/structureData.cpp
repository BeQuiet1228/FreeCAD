#include "structureData.h"
structureData::structureData(Hdf5Data& h5Data, const RunMod &mod)
	:Data(h5Data, mod), pointSize(0)
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
	pointXSize = (*it)->size();//获取横坐标的数量
	it++;
	pointi2mx = *it;
	pointYsize = (*it)->size();
	it++;

	//初始化范围
	initXYRang();
	return true;
}
QPointF structureData::getPoint(const int& index){
	if (index >= pointSize)
	{
		QPointF p;
		return p;
	}
	return getPointHard(index);
}
QPointF structureData::getPointHard(const int &index){
	QPointF point;
	point.setX(points->at(index * 2));
	point.setY(points->at(index * 2 + 1));
	return point;
}


int structureData::findIndexFromXValueL(const float& x){
	//float step = (xRang.max - yRang.min) / pointSize;
	//int index = x / step;
	//待实现
	return 0;
}
int structureData::findIndexFromXValueR(const float& x){
	//return findIndexFromXValueL(x) + 1;
	//待实现
	return 0;
}

int structureData::findIndexFromYValueT(const float& y)
{
	//待实现
	return 0;
}
int structureData::findIndexFromYValueB(const float& y)
{
	//待实现
	return 0;
}
bool structureData::initXYRang(){
	if (pointXSize < 2||pointYsize<2)
		return false;

	//获取x轴的范围
	//由于数据是均匀分布的，直接取头尾即可
	Rang xr, yr;
	auto iterx = pointi1mx->begin();
	xr.min = *iterx;
	iterx = pointi1mx->end();
	iterx -= 1;
	xr.max = (*iterx);

	auto itery=pointi2mx->begin();
	yr.min = *itery;
	itery = pointi2mx->end();
	itery -= 1;
	yr.max = *itery;

	setXRang(xr);
	setYRang(yr);
	return true;
}

bool structureData::loadrectpoint(){
	if (pointXSize<2||pointYsize<2)
	{
		return false;
	}
	//获取真空坐标，和导管坐标
	vacuo_vector.clear();
	conduit_vector.clear();
	QVector<QRectF> list;//全部坐标
	QVector<int> _property;//属性
	//开始获取
	auto iterleft = pointi1mx->begin();
	auto iterRight = pointi1mx->begin() + 1;
	auto iterTop = pointi2mx->begin();
	auto iterbottom = pointi2mx->begin() + 1;

	for (auto y = 0; y < pointYsize - 1;y++)
	{
		for (auto x = 0; x < pointXSize - 1;x++)
		{
			QRectF temp;//介值
			temp.setLeft(*iterleft);
			temp.setRight(*iterRight);
			temp.setTop(*iterTop);
			temp.setBottom(*iterbottom);
			list.push_back(temp);
			iterleft++;
			iterRight++;
		}
		iterTop++;
		iterbottom++;
	}
	//获取成功，开始分类
	for (auto i = 0; i < pointdatasetkmt->size() / 4; i++)
	{

	}
}