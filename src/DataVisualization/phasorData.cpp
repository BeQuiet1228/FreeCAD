#include"phasorData.h"
phasorData::phasorData(Hdf5Data& heData, const RunMod& mod) :XYData(heData,mod)
{

}
phasorData::~phasorData(){
}
void phasorData::restorDeriveData()
{

}
/**
* @brief phasorData::loadPoint 加载数据
* @return bool
*/
bool phasorData::loadPoint()
{
	Data::ListValuesPtr ListValues;
	//获取原始数据
	bool ok = autoModGetSourceData(ListValues);
	if (!ok && !ListValues &&ListValues->size() == 0)
		return false;
	auto it = (ListValues->begin());
	//获取横坐标的个数
	posxSize = (*it)->size(); it++;
	posySize = (*it)->size();
	//初始化范围
	initXYRang();
	//计算出图形数据
	initData();
	//计算出向量数据
	initVectorData();
	return true;
}
/**
* @brief phasorData::initXYRang 初始化X-Y的范围
* @return bool
*/
bool phasorData::initXYRang(){
	if (posxSize < 2 || posySize < 2)
		return false;
	//获取x,y轴的取值范围
	Rang xr, yr;
	Data::ListValuesPtr ListValues;
	bool ok = autoModGetSourceData(ListValues);
	if (!ok && !ListValues && ListValues->size() == 0)
		return false;
	//获取成功
	auto it = ListValues->begin();
	Data::ValuesPtr datasetEmA = *it; it++;
	Data::ValuesPtr datasetEmB = *it;
	//因为datasetEmA和datasetEmB的数据都是连续的，所以直接取首尾端即可
	//x
	auto itx = datasetEmA->begin();
	xr.min = 0;
	itx = datasetEmA->end() - 1;
	xr.max = *itx;
	setXRang(xr);
	//y
	auto ity = datasetEmB->begin();
	yr.min = 0;
	ity = datasetEmB->end() - 1;
	yr.max = *ity;
	setYRang(yr);
	return true;
}
/**
* @brief phasorData::findIndexFromXValueL 查找该横坐标的左边的索引
*/
unsigned int phasorData::findIndexFromXValueL(const float& x)
{
	return 0;
}
/**
* @brief phasorData::initData 初始化相关数据
* @return bool
*/
bool phasorData::initData()
{
	//先获取H5F中的全部数据
	mPiflist_rect.clear();
	//std::vector<QPointF> pointlist;
	//获取x轴上的全部点
	std::vector<qreal> valuesA_list = getaxis_x();
	//获取y轴上的全部点
	std::vector<qreal> valueB_list=getaxis_y();
	//获取全部的切割空间
#pragma region 
	for (auto valueB = 0; valueB < valueB_list.size()-1;valueB++)
	{
		for (auto valueA = 0; valueA < valuesA_list.size() - 1;valueA++)
		{
			//获取切割矩形
			QRectF _rectf;
			_rectf.setLeft(valuesA_list[valueA]);
			_rectf.setRight(valuesA_list[valueA+1]);
			_rectf.setTop(valueB_list[valueB+1]);
			_rectf.setBottom(valueB_list[valueB]);
			mPiflist_rect.push_back(_rectf);
//#define _DEBUG_
#ifdef _DEBUG_
			printf("left=%f,right=%f,top=%f.bottom=%f\n",_rectf.left(),_rectf.right(),_rectf.top(),_rectf.bottom());
#endif
		}
	}
#pragma endregion
	return true;
}
/**
* @brief phasorData::getaxis_x 获取x轴上的刻度
* @return std::vector<qreal>
*/
std::vector<qreal> phasorData::getaxis_x()
{
	std::vector<qreal> axis_xlist;
	Data::ListValuesPtr ListValues;
	bool ok = autoModGetSourceData(ListValues);
	if (!ok &&!ListValues && 0 == ListValues->size())
		return axis_xlist;
	//获取EMA的全部数据
	auto iter = ListValues->begin();
	Data::ValuesPtr datasetEmA = *iter;
	axis_xlist.push_back(0);
	for (auto iter_A = datasetEmA->begin(); iter_A != datasetEmA->end();iter_A++)
	{
		axis_xlist.push_back(*iter_A);
	}
	return axis_xlist;
}
/**
* @brief phasorData::getaxis_y 获取y轴上的全部刻度
* @return std::vector<qreal>
*/
std::vector<qreal> phasorData::getaxis_y()
{
	std::vector<qreal> axis_ylist;
	Data::ListValuesPtr ListValues;
	bool ok = autoModGetSourceData(ListValues);
	if (!ok&& !ListValues&& ListValues->size() == 0)
		return axis_ylist;
	auto iter = ListValues->begin(); iter++;
	Data::ValuesPtr datasetEmB = *iter;
	axis_ylist.push_back(0);
	for (auto iterb = datasetEmB->begin(); iterb != datasetEmB->end();iterb++)
	{
		axis_ylist.push_back(*iterb);
	}
	return axis_ylist;
}
/**
* @brief phasorData::getAllCutRoom 获取全部切割空间
* @return QVector<QRectF>
*/
QVector<QRectF> phasorData::getAllCutRoom(){
	return mPiflist_rect;
}
/**
* @brief phasorData::initVectorData 初始化向量相关数据
* @return bool
*/
bool phasorData::initVectorData()
{
	Data::ListValuesPtr DataValueslist;
	bool ok = autoModGetSourceData(DataValueslist);
	if (!ok && !DataValueslist && DataValueslist->size()==0)
		return false;
	auto iter = DataValueslist->begin();
	Data::ValuesPtr datasetEmA = *iter; iter++;
	Data::ValuesPtr datasetEmB = *iter; iter++;
	Data::ValuesPtr datasetEmC = *iter;
	if (mPiflist_rect.empty())
		return false;
	//获取起点p1
	QVector<qreal> dataC;
	for (auto iterC = datasetEmC->begin(); iterC != datasetEmC->end();iterC++)
		dataC.push_back(*iterC);
	for (auto i = 0; i < mPiflist_rect.size();i++)
		p1.push_back(QPointF(mPiflist_rect[i].left(), mPiflist_rect[i].bottom()));
	//获取终点p2(真实的点位)
	//获取缩放比例
	qreal Srect = mPiflist_rect[0].width()*mPiflist_rect[0].height();
	int index_rectmin = 0;
	qreal SVector=0;
	qreal Widmin=mPiflist_rect[0].width(), HeightMin=mPiflist_rect[0].height(), Xmax=0, yMax=0;
	int index_vector = 0;
	//获取x和y的缩放
	for (auto i = 0; i < mPiflist_rect.size();i++)
	{
		if (Srect>mPiflist_rect[i].width()*mPiflist_rect[i].height())
		{
			Srect = mPiflist_rect[i].width()*mPiflist_rect[i].height();
			index_rectmin = i;
		}
		if (SVector<dataC[2*i]*dataC[2*i+1])
		{
			SVector = dataC[2 * i] * dataC[2 * i + 1];
			index_vector = i;
		}
	}
	//此处获取到缩放的比例
	m_xScale = abs(mPiflist_rect[index_rectmin].width()/dataC[2*index_vector]);
	m_yScale = abs(mPiflist_rect[index_rectmin].height()/dataC[2*index_vector+1]);
	for (auto i = 0; i < mPiflist_rect.size(); i++)
	{
		qreal x_scal = dataC[2 * i];
		qreal y_scal = dataC[2 * i + 1];
		qreal p2x = p1[i].x() + (mPiflist_rect[i].width()*x_scal);
		qreal p2y = p1[i].y() + (mPiflist_rect[i].height()*y_scal);
		//qreal p2x = p1[i].x() + x_scal*m_xScale;
		//qreal p2y = p1[i].y() + y_scal*m_yScale;
//#define _DEBUG_
#ifdef _DEBUG_
		printf("x_scal=%f,y_scal=%f,\tindex=%d\n,",x_scal,y_scal,2*i);
#endif
		p2.push_back(QPointF(p2x, p2y));
	}
	//这里删除长度为0的线段
	for (auto i = p1.size() - 1; i >= 0;i--)
	{
		bool ok = (p1[i] == p2[i]);
		if (ok)
		{
			p1.erase(p1.begin() + i);
			p2.erase(p2.begin() + i);
		}
	}
	return true;
}
/**
* @brief phasorData::Getp1Point 获取向量的起始点位集合
* @return QVector<QPointF>
*/
QVector<QPointF> phasorData::Getp1Point(){
	return p1;
}
/**
* @brief phasorData::Getp2Point 获取向量的终点集合
* @return QVector<QPointF>
*/
QVector<QPointF> phasorData::Getp2Point(){
	return p2;
}
/**
* @brief phasorData::GetVecXScale 获取横向的缩放
* @return float
*/
float phasorData::GetVecXScale(){
	return m_xScale;
}
/**
* @brief phasorData::GetVecYScale 获取纵向的缩放
* @return float
*/
float phasorData::GetVecYScale(){
	return m_yScale;
}