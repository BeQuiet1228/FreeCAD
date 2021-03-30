#include "StructRenderer.h"

#include <QPainter>
#include <iostream>
#include <qpen.h>
#include <QPointF>
#include <QImage>
#include <QRgb>


StructureRenderer::StructureRenderer(std::shared_ptr<structureData> data)
	:Renderer(std::dynamic_pointer_cast<Data>(data)), m_Coordinate_Dir(Z_R_coordinater)
{

}

StructureRenderer::~StructureRenderer()
{

}
#include <QDebug>
bool StructureRenderer::drawImage()
{
	//获取坐标缩放比例
	switch(m_Coordinate_Dir)
	{
	case cylindrical_coordinate:
		return drawImage_Cylindrical_Coordinate();
	case polar_coordinate:
		return drawImage_Polar_coordinate();
	case Z_R_coordinater:
		return drawImage_Z_R();
	}
	return  false;
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
	auto _structureData = std::dynamic_pointer_cast<structureData>(data);
	if (!_structureData)
		return false;
	setXRang(_structureData->getXRang());
	setYRang(_structureData->getYRang());

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

void StructureRenderer::SetCoordinateDir(Coordinate_Dir _coordinadir)
{
	m_Coordinate_Dir = _coordinadir;
	switch (_coordinadir)
	{
	case cylindrical_coordinate:
	{
		auto _structureData = std::dynamic_pointer_cast<structureData>(data);
		if (!_structureData)
			return ;

		Data::Rang xr;
		QVector<qreal> R_range = _structureData->Get_R_val();
		auto maxiter = R_range.end() - 1;
//#define _DEBUG_
#ifdef _DEBUG_
		for each (qreal var in R_range)
		{
			printf("%f\n", var);
		}
#undef _DEBUG_
#endif
		xr.max = *maxiter;
		xr.min = -xr.max;
		setXRang(xr);
		setYRang(xr);
	}
		break;
	case polar_coordinate:
	{
	
	}
		break;
	case Z_R_coordinater:
	{
		setDefaultRang();
	}
		break;
	}
}
Coordinate_Dir StructureRenderer::getCurCoordinateDir()
{
	return m_Coordinate_Dir;
}
bool StructureRenderer::drawImage_Z_R()
{
	float yScale(0.0), xScale(0.0);
	if (!getTransitionScale(xScale, yScale))
		return false;
	std::shared_ptr<structureData> d = std::dynamic_pointer_cast<structureData>(data);
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
	for (; iter != _conduit_list.end(); iter++)
	{
		//获取缩放
		transitionRectF(*iter, xScale, xr, yScale, yr);
	}
	painter.drawRects(_conduit_list);
	auto nImg = img.mirrored(false, true);
	//#define _Debug
#ifdef _Debug
	static int index = 0;
	QString _path = QString("C:/Users/Administrator/Desktop/save/savepmg_%1.png").arg(index++);
	qDebug() << _path;
	bool res = nImg.save(_path);
#undef _Debug
#endif
	setImage(nImg);
	return true;
}

bool StructureRenderer::drawImage_Polar_coordinate(){
	return false;
}
bool StructureRenderer::drawImage_Cylindrical_Coordinate(){
	float yScale(0.0), xScale(0.0);
	if (!getTransitionScale(xScale, yScale))
		return false;
	std::shared_ptr<structureData> d = std::dynamic_pointer_cast<structureData>(data);
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
	//开始绘制圆柱
	QVector<qreal> _R_list = d->Get_R_val();
	QVector<qreal> _rand_list = d->Get_rand_val();
	//获取矩形
	QVector<QRectF> _rl = GetCylindricalRect(_R_list);
	auto iter = _rl.begin();
	for (; iter != _rl.end(); iter++)
	{
		//获取缩放
		transitionRectF(*iter, xScale, xr, yScale, yr);
	}
	//获取绘制角度
	//获取圆心
	QPointF  p1 = _rl[0].center();
	qreal pi = 3.1415926;//指定π
	//获取弧度与角度的比值
	qreal w1 = 180 / pi;
	qreal w2 = pi / 180;
	
	auto iterRange = _rand_list.begin();
	qreal startdeg = (*iterRange)*w1;
	iterRange = _rand_list.end() - 1;
	qreal enddeg = (*iterRange)*w1;
	for (auto i = 0; i < _rl.size();i++)
	{
		painter.drawArc(_rl[i], startdeg * 16, enddeg * 16);
	}
	//绘制切割线
	//起始设置为原点
	QVector<QLineF> _lines=Getlines(p1,_rl,_rand_list);
	painter.drawLines(_lines);
	/*for (auto cut = 0; cut < _rl.size();cut++)
	{
		qreal _width = _rl[cut].width();
		qreal _height = _rl[cut].height();
		for (auto i = 0; i < _rand_list.size(); i++)
		{
			qreal x = (_width / 2)*cos(_rand_list[i]) + p1.x();
			qreal y = p1.y() - (_height / 2)*sin(_rand_list[i]);
			QPointF p2 = QPointF(x, y);
			painter.drawLine(p1, p2);
		}
	}*/
	
	auto nImg = img.mirrored(false, true);
	//#define _Debug
#ifdef _Debug
	static int index = 0;
	QString _path = QString("C:/Users/Administrator/Desktop/save/savepmg_%1.png").arg(index++);
	qDebug() << _path;
	bool res = nImg.save(_path);
#undef _Debug
#endif
	setImage(nImg);
	return true;
}
QVector<QRectF> StructureRenderer::GetCylindricalRect(QVector<qreal> _r_rang)
{
	QVector<QRectF> CylindricalRectF;
	CylindricalRectF.clear();
	auto itera = _r_rang.begin();
	for (;itera!=_r_rang.end();itera++)
	{
		qreal r_distanse = *itera;
		QRectF temp;
		temp.setLeft(-r_distanse);
		temp.setRight(r_distanse);
		temp.setBottom(r_distanse);
		temp.setTop(-r_distanse);
		CylindricalRectF.push_back(temp);

	}
	return CylindricalRectF;
}
QVector<QLineF> StructureRenderer::Getlines(QPointF p0,QVector<QRectF> RAxis,QVector<qreal> rands)
{
	QVector<QLineF> lines;
	lines.clear();
	//起始为原点
	for (auto i = 0; i < RAxis.size()-1;i++)
	{
		QPointF lastpoint;
		QPointF nextpoint;
		if (RAxis[i].width()>0 && RAxis[i].height()>0&&RAxis[i+1].width()>0&&RAxis[i+1].height()>0)
		{
			for (auto j = 0; j < rands.size();j++)
			{
				lastpoint.setX(RAxis[i].width()/2*cos(rands[j])+p0.x());
				lastpoint.setY(p0.y() - RAxis[i].height() / 2 * sin(rands[j]));
				nextpoint.setX((RAxis[i + 1].width() / 2) * cos(rands[j]) + p0.x());
				nextpoint.setY(p0.y() - (RAxis[i + 1].height() / 2) * sin(rands[j]));
				lines.push_back(QLineF(lastpoint.x(),lastpoint.y(),nextpoint.x(),nextpoint.y()));
			}
		}
	}	
	return lines;
}