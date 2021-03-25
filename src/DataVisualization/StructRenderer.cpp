#include "StructRenderer.h"

#include <QPainter>
#include <iostream>
#include <qpen.h>
#include <QPointF>
#include <QImage>
#include <QRgb>
StructureRenderer::StructureRenderer(std::shared_ptr<structureData> data)
	:Renderer(std::dynamic_pointer_cast<Data>(data))
{

}

StructureRenderer::~StructureRenderer()
{

}
#include <QDebug>
bool StructureRenderer::drawImage()
{
	//获取坐标缩放比例
	float yScale(0.0), xScale(0.0);
	if (!getTransitionScale(xScale, yScale))
		return false;

	std::shared_ptr<structureData> d = std::dynamic_pointer_cast<structureData>(data);
	if (!d)
	{
#if LOG
		std::cerr << "StructureRenderer::drawImage() data dynamic cast failed!" << std::endl;
#endif
		return false;
	}
	//获取起始点,因为图表的刻度不一定是从零开始的。
	auto xr = getXRang();
	auto yr = getYRang();
	//开始绘制
	//新建画布 画笔
	QImage img(getSize(), QImage::Format_ARGB32);
	img.fill(qRgba(0, 0, 0, 0));
	QPen pen(Qt::black);
	pen.setWidth(1);
	QPainter painter(&img);
	painter.setRenderHint(QPainter::Antialiasing, true);;
	painter.setPen(pen);

	//开始绘制图表
	QVector<QRectF> _conduit_list = d->GetConduitPoint();
	auto iter = _conduit_list.begin();
	for (;iter!=_conduit_list.end();iter++)
	{
		//获取缩放
		transitionRectF(*iter, xScale, xr, yScale, yr);
	}
	painter.drawRects(_conduit_list);
	/*for (int index = 0; index < _conduit_list.size(); index++)
	{
			painter.drawLine(_conduit_list[index].left(), _conduit_list[index].top(), _conduit_list[index].right(), _conduit_list[index].top());
			painter.drawLine(_conduit_list[index].left(), _conduit_list[index].bottom(), _conduit_list[index].right(), _conduit_list[index].bottom());
			painter.drawLine(_conduit_list[index].left(), _conduit_list[index].top(), _conduit_list[index].left(), _conduit_list[index].bottom());
			painter.drawLine(_conduit_list[index].right(), _conduit_list[index].top(), _conduit_list[index].right(), _conduit_list[index].bottom());
	}*/
	auto nImg = img.mirrored(false, true);
//#define _Debug
#ifdef _Debug
	static int index = 0;
	QString _path = QString("C:/Users/Administrator/Desktop/save/savepmg_%1.png").arg(index++);
	qDebug() << _path;
	bool res=nImg.save(_path);
#undef _Debug
#endif
	setImage(nImg);
	return true;
}

/**
* @brief TimeRenderer::addListRang 设置范围 一共两个 1. x轴范围 2. y轴范围
* @param std::list<Data::Rang> listRang
* @return bool
*/
bool StructureRenderer::addListRang(std::list<Data::Rang> listRang)
{
	if (listRang.size() != 2)
		return false;
	auto iter = listRang.begin();
	setXRang(*iter);
	iter++;
	setYRang(*iter);
}
/**
* @brief TimeRenderer::drawPointImage 渲染取点
* @return bool
*/
bool StructureRenderer::drawPointImage()
{
	//新建画布 画笔
	/*QImage img(getSize(), QImage::Format_ARGB32);
	img.fill(qRgba(0, 0, 0, 0));
	QPen pen(Qt::red);
	pen.setBrush(Qt::blue);
	pen.setWidth(5);
	QPainter painter(&img);
	painter.setPen(pen);
	painter.drawPoint(this->getFindPosition());
	auto nImg = img.mirrored(false, true);
	setImage(nImg);*/
	//待实现
	return true;
}

/**
* @brief TimeRenderer::setDefaultRang 设置默认的渲染范围
* @return bool
*/
bool StructureRenderer::setDefaultRang()
{
	auto timeData = std::dynamic_pointer_cast<structureData>(data);
	if (!timeData)
		return false;
	setXRang(timeData->getXRang());
	setYRang(timeData->getYRang());

	return true;
}

/**
* @brief TimeRenderer::dataInit 初始化数据
* @return void
*/
void StructureRenderer::dataInit()
{
	Renderer::dataInit();
	auto _structuredate = std::dynamic_pointer_cast<structureData>(data);
	if (_structuredate)
	{
		_structuredate->loadPoint();
		_structuredate->loadrectpoint();
	}
		
}

/**
* @brief TimeRenderer::transitionX 坐标值转换
* @param const float & x
* @param const float & xScale  缩放比例
* @param const Data::Rang & xr 渲染范围
* @return float
*/
float StructureRenderer::transitionX(const float& x, const float& xScale, const Data::Rang& xr)
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
float StructureRenderer::transitionY(const float& y, const float& yScale, const Data::Rang& yr)
{
	return (y - yr.min)*yScale;
}
/**
* @brief StructureRenderer::transitionRectF 切割空间的坐标转换
* @param QRectF& _rect
* @param const float& xScale
* @param const Data::Rang& xr
* @param const float& yScale
* @param Data::Rang& yr
* @return void
*/
void StructureRenderer::transitionRectF(QRectF& _rectf, const float& xScale, const Data::Rang& xr, const float& yScale, Data::Rang& yr)
{
	_rectf.setLeft(transitionX(_rectf.left(), xScale,xr));
	_rectf.setRight(transitionX(_rectf.right(),xScale,xr));
	_rectf.setTop(transitionY(_rectf.top(), yScale, yr));
	_rectf.setBottom(transitionY(_rectf.bottom(), yScale, yr));
}
/**
* @brief TimeRenderer::getTransitionScale 初始化数据与图片坐标的缩放比例
* @param float & xScale
* @param float & yScale
* @return bool
*/
bool StructureRenderer::getTransitionScale(float& xScale, float& yScale)
{
	auto size = getSize();
   	auto xr = getXRang();
	auto yr = getYRang();

	float xLength = xr.max - xr.min;
	float yLength = yr.max - yr.min;

	if (xLength < 0 || yLength < 0)
	{
#if MY_DEBUG
		std::cerr << "StructRenderer::getTransitionScale length < 0" << std::endl;
#endif
		return false;
	}

	if (size.width() <= 0 || size.height() <= 0)
	{
#if MY_DEBUG
		std::cerr << "StructRenderer::getTransitionScale size <= 0" << std::endl;
#endif
		return false;
	}
	xScale = size.width() / xLength;
	yScale = size.height() / yLength;
	return true;
}

