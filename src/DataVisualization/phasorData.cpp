#include"phasorData.h"
phasorData::phasorData(Hdf5Data& heData, const RunMod& mod) :DirData(heData,mod)
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
	//需要先清空数据
	mPiflist_rect.clear();
	p1.clear();
	p2.clear();
	len_coef.clear();
	/*************************************/
	Data::ListValuesPtr ListValues;
	//获取原始数据
	bool ok = autoModGetSourceData(ListValues);
	if (!ok && !ListValues &&ListValues->size() == 0)
		return false;
	auto it = (ListValues->begin());
	auto xtag = getXTag();
	auto ytag = getYTag();
	//获取横坐标的个数
	if (isTruedir())
	{
		posySize = (*it)->size(); it++;
		posxSize = (*it)->size();
	}
	else
	{
		posxSize = (*it)->size(); it++;
		posySize = (*it)->size();
	}
	
	//初始化范围
	initXYRang();
	//初始化图形数据
	initData();
	//初始化向量数据
	//initVectorData();
	initVectorData2();
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
	if (isTruedir())
	{
		//x
		xr.min = 0;
		xr.max = *(datasetEmB->end() - 1);
		setXRang(xr);
		//y
		yr.min = 0;
		yr.max = *(datasetEmA->end() - 1);
		setYRang(yr);
	}
	else
	{
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
	}
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
	if (isTruedir())
	{
		iter++;
	}
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
	auto iter = ListValues->begin();
	if (!isTruedir())
	{
		iter++;
	}
	Data::ValuesPtr datasetEmB = *iter;
	axis_ylist.push_back(0);
	for (auto iterb = datasetEmB->begin(); iterb != datasetEmB->end();iterb++)
	{
		//printf("y=%f\n", *iterb);
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
		qreal curlen = sqrt(dataC[i] * dataC[i] + dataC[i + mPiflist_rect.size()] * dataC[i + mPiflist_rect.size()]);
		if (SVector<curlen)
		{
			SVector = curlen;
			index_vector = i;
		}
	}
	//此处获取到缩放的比例
	m_xScale =abs(dataC[index_vector]);
	m_yScale =abs(dataC[index_vector+mPiflist_rect.size()]);
	for (auto i = 0; i < mPiflist_rect.size(); i++)
	{
		qreal x_scal = dataC[i];
		qreal y_scal = dataC[i+mPiflist_rect.size()];
#define _PROJECT_CHANGE_
#ifndef _PROJECT_CHANGE_
		p2.push_back(QPointF(x_scal, y_scal));
#else
		qreal x = p1[i].x() + abs(mPiflist_rect[i].width())*x_scal;
		qreal y = p1[i].y() + abs(mPiflist_rect[i].height())*y_scal;
		p2.push_back(QPointF(x,y));
	//	printf("%d___p0(%f,%f)->p1(%f,%f)\n",i,p1[i].x(),p1[i].y(),p2[i].x(),p2[i].y());	
#endif
	}
	//这里删除长度为0的线段
	for (auto i = p1.size() - 1; i >= 0;i--)
	{
#ifndef _PROJECT_CHANGE_
		if (p2[i].x()<0.0000001&&p2[i].x()>-0.0000001&&
			p2[i].y()<0.0000001&&p2[i].y()>-0.0000001)
#else
		if (p1[i]==p2[i])
#endif
		{
			p1.erase(p1.begin() + i);
			p2.erase(p2.begin() + i);
		}
	}
#ifdef _PROJECT_CHANGE_
#undef _PROJECT_CHANGE_
#endif // _PROJECT_CHANGE_
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
/**
* @brief phasorData::initVectorData2 初始化向量数据（方式2）
* @return bool
*/
bool phasorData::initVectorData2(){
	Data::ListValuesPtr DataValueslist;
	bool ok = autoModGetSourceData(DataValueslist);
	if (!ok&& !DataValueslist&& DataValueslist->size() == 0)
		return false;
	auto iter = DataValueslist->begin();
	Data::ValuesPtr datasetEmA;
	Data::ValuesPtr datasetEmB;
	Data::ValuesPtr datasetEmC;
	if (isTruedir())
	{
		datasetEmB = *iter; iter++;
		datasetEmA = *iter; iter++;
		datasetEmC = *iter;
	}
	else
	{
		datasetEmA = *iter; iter++;
		datasetEmB = *iter; iter++;
		datasetEmC = *iter;
	}

	if (mPiflist_rect.empty())
		return false;
	//获取起点p1
	QVector<qreal> dataC;
	for (auto iterC = datasetEmC->begin(); iterC != datasetEmC->end(); iterC++)
		dataC.push_back(*iterC);
	for (auto i = 0; i < mPiflist_rect.size(); i++)
	{
		p1.push_back(QPointF(mPiflist_rect[i].left(), mPiflist_rect[i].bottom()));
	}	
	Data::Rang xr = getXRang();
	Data::Rang yr = getYRang();
	float Width = (xr.max - xr.min)/datasetEmA->size();
	float Height = (yr.max - yr.min) / datasetEmB->size();
	//获取最大的x,y系数
	float Svector = 0;//最大系数
	unsigned int index_vector=0;
	for (auto i = 0; i < mPiflist_rect.size();i++)
	{
		float curlen = sqrt(dataC[i]*dataC[i]+dataC[i+mPiflist_rect.size()]*dataC[i+mPiflist_rect.size()]);
		if (Svector<curlen)
		{
			Svector = curlen;
			index_vector = i;
		}
	}
	//获取到x,y的最大系数
	float MaxRectLen = sqrt(Width*Width+Height*Height);
	//获取p2的数据
	for (auto i = 0; i < mPiflist_rect.size();i++)
	{
		float x_coef = dataC[i];
		float y_coef = dataC[i + mPiflist_rect.size()];
		//printf("x_coef=%f,y_coef=%f\n", x_coef, y_coef);
		if (x_coef<0.0000001&&x_coef>-0.0000001&&
			y_coef<0.0000001&&y_coef>-0.0000001)
		{
			p2.push_back(p1[i]);
			len_coef.push_back(QPointF(0.0,0.0));
		}
		else
		{
			len_coef.push_back(QPointF(x_coef,y_coef));
			float _p2Len = sqrt(x_coef*x_coef + y_coef*y_coef);
			float rotation = _p2Len / Svector;
			QPointF _p2;
			//之前得计算方法--暂时保留
			//_p2.setX(p1[i].x() + MaxRectLen*rotation*(x_coef / _p2Len));
			//_p2.setY(p1[i].y() + MaxRectLen*rotation*(y_coef / _p2Len));
			_p2.setX(p1[i].x() + Width*rotation*(x_coef / _p2Len)*0.95);
			_p2.setY(p1[i].y() + Height*rotation*(y_coef / _p2Len)*0.95);
			p2.push_back(_p2);
		}
		
	}
	//去除不必要的向量
	for (auto i = p1.size()-1; i>=0;i--)
	{
		if (p1[i].x() - p2[i].x()>-0.000001&&p1[i].x() - p2[i].x() < 0.000001&&
			p1[i].y() - p2[i].y()>-0.000001&&p1[i].y() - p2[i].y() < 0.000001)
		{
			p1.erase(p1.begin() + i);
			len_coef.erase(len_coef.begin()+i);
			p2.erase(p2.begin() + i);
		}
	}
	return true;
}
/**
* @brief phasorData::findindexlen_coef 索引向量的长度系数
* @param int index
* @return QPointF
*/
QPointF phasorData::findindexlen_coef(int index)
{
	auto iter = len_coef.begin() + index;
	if (iter!=len_coef.end())
	{
		return *iter;
	}
	return QPointF(0.0, 0.0);
}
/**
* @brief phasorData::findindexP1 索引向量的起点
* @param int index
* @return QPointF
*/
QPointF phasorData::findindexP1(int index)
{
	auto iter = p1.begin() + index;
	if (iter!=p1.end())
	{
		return *iter;
	}
	return QPointF(0.0,0.0);
}