#include "TimeRenderer.h"
#include <QPainter>
#include <iostream>
#include <qpen.h>
#include <QPointF>
#include <QImage>
TimeRenderer::TimeRenderer(std::shared_ptr<TimeData> data)
	:Renderer(std::dynamic_pointer_cast<Data>(data))
{

}

TimeRenderer::~TimeRenderer()
{

}

bool TimeRenderer::drawPixmap()
{
	//获取坐标缩放比例
	float yScale(0.0), xScale(0.0);
	if (!getTransitionScale(xScale, yScale))
		return false;

	std::shared_ptr<TimeData> d = std::dynamic_pointer_cast<TimeData>(data);
	if (!d)
	{
#if LOG
		std::cerr << "TimeRenderer::drawPixmap() data dynamic cast failed!" << std::endl;
#endif
		return false;
	}

	//获取起始点,因为图表的刻度不一定是从零开始的。
	auto xr = getXRang();
	auto yr = getYRang();

	//获取数据索引的范围
	int startIndex(0), endIndex(0);
	startIndex = d->findIndexFromXValueL(xr.min);
	endIndex = d->findIndexFromXValueR(xr.max);

	//新建画布 画笔
	QPixmap *pixmap = new QPixmap(getSize());
	QImage imag;
 	pixmap->fill(Qt::transparent);
	QPen pen(Qt::black);
	QPainter painter(&imag);
	painter.setPen(pen);
	
	QPointF starPoint, endPoint;
	starPoint = d->getPoint(startIndex);
	transitionPoint(starPoint, xScale, xr, yScale, yr);
	startIndex++;
	for (int index = startIndex + 1 ; index < endIndex; index++)
	{
		endPoint = d->getPoint(index);
		transitionPoint(endPoint, xScale, xr, yScale, yr);
		painter.drawLine(starPoint,endPoint);
		starPoint = endPoint;
	}

	setPixmap(*pixmap);
	return true;
}

/**
* @brief TimeRenderer::addListRang 设置范围 一共两个 1. x轴范围 2. y轴范围
* @param std::list<Data::Rang> listRang
* @return bool
*/
bool TimeRenderer::addListRang(std::list<Data::Rang> listRang)
{
	if (listRang.size() != 2)
		return false;
	auto iter = listRang.begin();
	setXRang(*iter);
	iter++;
	setYRang(*iter);
}

/**
* @brief TimeRenderer::setXRang 设置x轴的渲染范围
* @param const Data::Rang & rang
* @return void
*/
void TimeRenderer::setXRang(const Data::Rang& rang)
{
	Renderer::AutoMutex am(xRangMutex);
	xRang = rang;
}

/**
* @brief TimeRenderer::getXRang 获取x轴的渲染范围
* @return Data::Rang
*/
Data::Rang TimeRenderer::getXRang()
{
	Renderer::AutoMutex am(xRangMutex);
	return xRang;
}

/**
* @brief TimeRenderer::setYRang 设置y轴的渲染范围
* @param const Data::Rang & rang
* @return void
*/
void TimeRenderer::setYRang(const Data::Rang& rang)
{
	Renderer::AutoMutex am(yRangMutex);
	yRang = rang;
}

/**
* @brief TimeRenderer::getYRang 获取y轴的渲染范围
* @return Data::Rang
*/
Data::Rang TimeRenderer::getYRang()
{
	Renderer::AutoMutex am(yRangMutex);
	return yRang;
}

/**
* @brief TimeRenderer::transitionX 坐标值转换
* @param const float & x
* @param const float & xScale  缩放比例
* @param const Data::Rang & xr 渲染范围
* @return float
*/
float TimeRenderer::transitionX(const float& x, const float& xScale, const Data::Rang& xr)
{
	return (x - xr.min)*xScale;
}

/**
* @brief TimeRenderer::transitionY 坐标值转转
* @param const float & y 
* @param const float & yScale 缩放比例
* @param const Data::Rang & yr 渲染范围
* @return float
*/
float TimeRenderer::transitionY(const float& y, const float& yScale, const Data::Rang& yr)
{
	return (y - yr.min)*yScale;
}



/**
* @brief TimeRenderer::transitionPoint 坐标值转换
* @param QPointF & point
* @param const float & xScale
* @param const Data::Rang & xr
* @param const float & yScale
* @param Data::Rang & yr
* @return void
*/
void TimeRenderer::transitionPoint(QPointF& point, const float& xScale, const Data::Rang& xr, const float& yScale, Data::Rang& yr)
{
	point.setX(transitionX(point.x(), xScale, xr));
	point.setY(transitionY(point.y(), yScale,yr));
}

/**
* @brief TimeRenderer::getTransitionScale 初始化数据与图片坐标的缩放比例
* @param float & xScale
* @param float & yScale
* @return bool
*/
bool TimeRenderer::getTransitionScale(float& xScale, float& yScale)
{
	auto size = getSize();
	auto xr = getXRang();
	auto yr = getYRang();

	float xLength = xr.max - xr.min;
	float yLength = yr.max - yr.min;

	if (xLength < 0 || yLength < 0)
	{
#if LOG
		std::cerr << "TimeRenderer::getTransitionScale length < 0" << std::endl;
#endif
		return false;
	}

	if (size.width() <= 0 || size.height() <= 0)
	{
#if LOG
		std::cerr << "TimeRenderer::getTransitionScale size <= 0" << std::endl;
#endif
		return false;
	}
	xScale = size.width() / xLength;
	yScale = size.height() / yLength;
}


