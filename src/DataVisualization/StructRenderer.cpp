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
	
	switch (m_Coordinate_Dir)
	{
	case cylindrical_coordinate:
		return drawPointImage_Cylindrical();
	case polar_coordinate:
		return drawPointImage_polar();
	case Z_R_coordinater:
		return drawPointImage_Z_R();
	}

	
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
		//_structuredate->loadrectpoint();
		//释放中间参数
		//_structuredate->Dropout_value();
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
/**
* @brief StructureRenderer::SetCoordinateDir 设置结构图视图种类
* @param Coordinate_Dir _coordinadir
* @return void
*/
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
/**
* @brief StructureRenderer::getCurCoordinateDir 获取当前结构图视图种类
* @return Coordinate
*/
Coordinate_Dir StructureRenderer::getCurCoordinateDir()
{
	return m_Coordinate_Dir;
}
/**
* @brief StructureRenderer::drawImage_Z_R 绘制Z_R方位的结构图
* @return bool
*/
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
/**
* @brief StructureRenderer::drawImage_Polar_coordinate 绘制极坐标系
* @return bool
*/
bool StructureRenderer::drawImage_Polar_coordinate(){
	return false;
}
/**
* @brief StructureRenderer::drawImage_Cylindrical_Coordinate 绘制圆柱坐标系结构图
* @return bool
*/
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
	//auto iter = _rl.begin();
	for (auto iter=_rl.begin(); iter != _rl.end(); iter++)
	{
		//获取缩放
		transitionRectF(*iter, xScale, xr, yScale, yr);
	}
	//获取绘制角度
	//获取圆心
	QPointF  p1 = _rl[0].center();
	qreal pi = 3.1415926;//指定π
	//获取弧度与角度的转换系数
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
/**
* @brief StructureRenderer::GetCylindricalRect 获取需要绘制的圆柱的相切矩形队列
* @param QVector<qreal> _r_rang R刻度
* @return QVector<QRectF>
*/
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
/**
* @brief StructureRenderer::Getlines 获取需要绘制的圆柱图的线段
* @param QPointF p0 圆心坐标
* @param QVector<QRectF> RAxis 所有需要绘制的弧的相切矩形队列
* @param QVector<qreal> rands 切割的角度
* @return QVector<QLineF>
*/
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
/**
* @brief StructureRenderer::drawPointImage_Cylindrical 获取渲染的点（圆柱坐标系）
* @return bool
*/
bool StructureRenderer::drawPointImage_Cylindrical(){
	//新建画布 画笔
	QImage img(getSize(), QImage::Format_ARGB32);
	//填充透明画布
	img.fill(qRgba(0, 0, 0, 0));
	QPen pen(Qt::red);
	pen.setBrush(Qt::blue);
	pen.setWidth(5);
	QPainter painter(&img);
	painter.setPen(pen);
	//获取当前点位

	structureData::structpoint _point = findApoint_Cylindrical(this->getFindPosition());
#define _DEBUG_
#ifdef _DEBUG_
	printf("获取的当前点位:(x=%f,y=%f)\n", _point.x, _point.y);
#undef _DEBUG_
#endif
	//坐标翻转
	_point.y = getSize().height() - _point.y;
	painter.drawPoint(QPointF(_point.x,_point.y));
	drawDisplayPoint(painter, QPointF(_point.x, _point.y), QPointF(_point.d1, _point.d2));
	//auto nImg = img.mirrored(false, true);
	setImage(img);
	return true;
}
/**
* @brief StructureRenderer::drawPointImage_polar 获取渲染的点（极坐标）
* @return bool
*/
bool StructureRenderer::drawPointImage_polar(){
	return true;
}
/**
* @brief StructureRenderer::drawPointImage_Z_R 获取渲染的点（Z_R坐标）
* @return bool
*/
bool StructureRenderer::drawPointImage_Z_R(){

	//新建画布 画笔

	QImage img(getSize(), QImage::Format_ARGB32);
	img.fill(qRgba(0, 0, 0, 0));
	QPen pen(Qt::red);
	pen.setBrush(Qt::blue);
	pen.setWidth(5);
	QPainter painter(&img);
	painter.setPen(pen);
	QPointF A_pos;//原始坐标
	//获取当前点位
	structureData::structpoint _point = findApoint_Z_R(this->getFindPosition());
	//painter.drawPoint(this->getFindPosition());
//#define _DEBUG_
#ifdef _DEBUG_
	printf("获取绘制的点的结果:x=%f,y=%f\n",_point.x(),_point.y());
#undef _DEBUG_
#endif
	//坐标翻转
	_point.y = getSize().height() - _point.y;
	painter.drawPoint(QPointF(_point.x,_point.y));
	drawDisplayPoint(painter,QPointF(_point.x,_point.y),QPointF(_point.d1,_point.d2));
	//auto nImg = img.mirrored(false, true);
	setImage(img);
	return true;
}
/**
* @brief StructureRenderer::findApoint_Z_R 查找Z_R坐标系中最接近的点
* @param QPointF _curpostion 鼠标的点击坐标系参数
* @return structureData::structpoint 返回相关参数（包括真实参数和，直角坐标系下的参数）
*/
structureData::structpoint StructureRenderer::findApoint_Z_R(QPointF _curpostion){
	structureData::structpoint mpoint;
	//获取屏幕与数据的比例
	float xScale, yScale;
	getTransitionScale(xScale, yScale);
	auto xr = getXRang();
	auto yr = getYRang();
	//区域中的点
	std::list<structureData::structpoint> _point;
	//获取所有的点
	/******************************/
	std::shared_ptr<structureData> d = std::dynamic_pointer_cast<structureData>(data);
	//开始绘制图表
	//获取真实的数据
	QVector<QRectF> _conduit_list = d->GetConduitPoint();
	//获取矩形中心点
	QVector<QPointF> Scale_coord;
	for (auto iter = _conduit_list.begin(); iter != _conduit_list.end(); iter++)
	{
		//获取缩放
		//transitionRectF(*iter, xScale, xr, yScale, yr);
		QPointF _centerpoint = iter->center();
		_centerpoint.setX(transitionX(_centerpoint.x(), xScale, xr));
		_centerpoint.setY(transitionY(_centerpoint.y(), yScale, yr));
		Scale_coord.push_back(_centerpoint);
//#define _DEBUG_
#ifdef _DEBUG_
		printf("中心点point=(x=%f,y=%f)\n", _centerpoint.x(), _centerpoint.y());
#undef _DEBUG_
#endif
	}
	//获取最接近的中心点（待优化）
	unsigned int index = 0;
	float distance = 10000.0f;
	for (unsigned int i = 0; i < Scale_coord.size();i++)
	{
		float _distance = GetDistance(_curpostion, Scale_coord[i]);

		if (distance>_distance)
		{
//#define _DEBUG_
#ifdef _DEBUG_
			printf("距离范围为：distance=%f-----%d\n", distance, i);
#undef _DEBUG_
#endif
			distance = _distance;
			index = i;
		}
	}
	//获取到最近的中心点
	QRectF _rectf = _conduit_list[index];
	QRectF _recfCoord = _rectf;
	transitionRectF(_recfCoord,xScale,xr,yScale,yr);
	//获取接近的x坐标
	if (abs(_curpostion.x() - _recfCoord.left()) >= abs(_curpostion.x() - _recfCoord.right()))
	{
		mpoint.x = _recfCoord.right();
		mpoint.d1 = _conduit_list[index].right();
	}
	else
	{
		mpoint.x = _recfCoord.left();
		mpoint.d1
			= _conduit_list[index].left();
	}
	//qreal xpoint = ((abs(_curpostion.x() - _recfCoord.left())) >= (abs(_curpostion.x() - _recfCoord.right()))) ? (_recfCoord.right()) : (_recfCoord.left());
	//获取最接近的y坐标
	if ((abs(_curpostion.y() - _recfCoord.top())) >= (abs(_curpostion.y() - _recfCoord.bottom())))
	{
		mpoint.y = _recfCoord.bottom();
		mpoint.d2 = _conduit_list[index].bottom();
	}
	else
	{
		mpoint.y = _recfCoord.top();
		mpoint.d2 = _conduit_list[index].top();
	}
	//qreal ypoint = ((abs(_curpostion.y() - _recfCoord.top())) >= (abs(_curpostion.y() - _recfCoord.bottom()))) ? (_recfCoord.bottom()) : (_recfCoord.top());
#define _DEBUG_
#ifdef _DEBUG_
	printf("鼠标点坐标-(x=%f,y=%f)\n", _curpostion.x(), _curpostion.y());
	//printf("接近的点----(x=%f,y=%f)\n",xpoint,ypoint);
#undef _DEBUG_
#endif
	return mpoint;
}
/**
* @brief StructureRenderer::GetDistance 返回两点之间的距离
* @param QPointF p1 
* @param QPointF p2
* @return float
*/
float StructureRenderer::GetDistance(QPointF p1, QPointF p2)
{
	float distance;
	distance = ((p1.x() - p2.x())*(p1.x() - p2.x())) +
		((p1.y() - p2.y())*(p1.y() - p2.y()));
	return sqrt(distance);

}
/**
* @brief StructureRenderer::findApoint_Cylindrical 查找直直角坐标系中的最近点
* @param QPointF _curpoint当前鼠标点击的点位
* @return structureData::structpoint
*/
structureData::structpoint StructureRenderer::findApoint_Cylindrical(QPointF _curpoint)
{
	structureData::structpoint mpoint;
	//获取屏幕的缩放比例
	float xScale, yScale;
	getTransitionScale(xScale, yScale);
	auto xr = getXRang();
	auto yr = getYRang();
	/*********************************/
	//获取所有的点，只能一个一个对比
	std::shared_ptr<structureData> d = std::dynamic_pointer_cast<structureData>(data);
	//获取起始点,因为图表的刻度不一定是从零开始的。
	QVector<qreal> _R_list = d->Get_R_val();
	QVector<qreal> _rand_list = d->Get_rand_val();
	//获取矩形
	QVector<QRectF> _rl = GetCylindricalRect(_R_list);
	//获取原始的切割数据
	QVector<QLineF> a_lines = Getlines(QPointF(0.0, 0.0), _rl, _rand_list);
	for (auto iter = _rl.begin(); iter != _rl.end(); iter++)
	{
		//获取缩放
		transitionRectF(*iter, xScale, xr, yScale, yr);
	}
	//获取绘制角度
	//获取圆心
	QPointF  p1 = _rl[0].center();
	QVector<QLineF> _lines = Getlines(p1, _rl, _rand_list);
//#define _DEBUG_
#ifdef _DEBUG_
	for each (QLineF var in _lines)
	{
		printf("(x1=%f,y1=%f,x2=%f,y2=%f)\n", var.p1().x(), var.p1().y(), var.p2().x(), var.p2().y());
	}
#endif
	//开始比较
	float distance = 100000.0;//MAX_DISTANCE
	QPointF minPoint;
	unsigned int index = 0;
	unsigned int type = 0;
	for (auto  i = 0; i <_lines.size(); i++)
	{
		float _distance1 = GetDistance(_curpoint,_lines[i].p1());
		float _distance2 = GetDistance(_curpoint, _lines[i].p2());
		if (distance>_distance1 ||distance>_distance2)
		{
			index = i;
			distance = (_distance1 > _distance2) ? (_distance2) : (_distance1);
			type = (_distance1 > _distance2) ? (2) : (1);
			minPoint = (_distance1 > _distance2) ?(_lines[i].p2()) :(_lines[i].p1()) ;
		}
	}
	//获取到最小点
//#define _DEBUG_
#ifdef _DEBUG_
	printf("鼠标的点位(x=%f,y=%f)\n",_curpoint.x(),_curpoint.y());
	printf("计算得出最小点为（x=%f,y=%f）\n", minPoint.x(), minPoint.y());
#endif
	mpoint.x = minPoint.x();
	mpoint.y = minPoint.y();
	switch (type)
	{
	case 1:
	{
		mpoint.d1 = a_lines[index].p1().x();
		mpoint.d2 = a_lines[index].p1().y();
	}
		break;
	case 2:
	{
		mpoint.d1 = a_lines[index].p2().x();
		mpoint.d2 = a_lines[index].p2().y();
	}
		break;
	}
	return mpoint;
}
/**
* @brief StructureRenderer::drawDisplayPoint 绘制点位展示信息
* @param QPainter& painter
* @param const QPointF& position
* @param const QPointF& d
* @return void
*/
void StructureRenderer::drawDisplayPoint(QPainter& painter, const QPointF& position, const QPointF& d)
{
	//设置画笔的颜色
	QPen pen;
	pen.setColor(QColor(102, 205, 170));
	pen.setWidth(2);
	painter.setPen(pen);
	painter.setBrush(QBrush(QColor(255, 250, 240)));
	//建立话画框
	QRectF displayRect;
	displayRect.setX(position.x() + 10);
	displayRect.setY(position.y() - 5);
	//如果这个点在边界上  那么调整话框的位置
	auto size = getSize();
	if (displayRect.y() > (size.height() - 60))
	{
		displayRect.setY(displayRect.y() - 70);
	}
	if (displayRect.x() > (size.width() - 130))
	{
		displayRect.setX(displayRect.x() - 150);
	}

	displayRect.setWidth(110);
	displayRect.setHeight(50);
	painter.drawRect(displayRect);
	//绘制显示信息
	QFont f;
	f.setPixelSize(17);
	painter.setFont(f);
	painter.drawText(displayRect.x() + 10,
		displayRect.y() + 20,
		QString("X:%1").arg(d.x(), 0, 'E', 2)
		);
	painter.drawText(displayRect.x() + 10,
		displayRect.y() + 40,
		QString("Y:%1").arg(d.y(), 0, 'E', 2)
		);
}