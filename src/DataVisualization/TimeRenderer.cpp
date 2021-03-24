#include "TimeRenderer.h"
#include <QPainter>
#include <iostream>
#include <qpen.h>
#include <QPointF>
#include <QImage>
#include <QRgb>
#include <list>
#include <math.h>
#include <QRectF>
#include <QBrush>
TimeRenderer::TimeRenderer(std::shared_ptr<TimeData> data)
	:Renderer(std::dynamic_pointer_cast<Data>(data))
{

}

TimeRenderer::~TimeRenderer()
{

}

bool TimeRenderer::drawImage()
{
	//获取坐标缩放比例
	float yScale(0.0), xScale(0.0);
	if (!getTransitionScale(xScale, yScale))
		return false;

	std::shared_ptr<TimeData> d = std::dynamic_pointer_cast<TimeData>(data);
	if (!d)
	{
#if LOG
		std::cerr << "TimeRenderer::drawImage() data dynamic cast failed!" << std::endl;
#endif
		return false;
	}


	//获取起始点,因为图表的刻度不一定是从零开始的。
	auto xr = getXRang();
	auto yr = getYRang();

	//获取数据索引的范围
	int startIndex(0), endIndex(0);
	startIndex = d->findIndexFromXValueL(xr.min);
	endIndex = d->findIndexFromXValueL(xr.max);

	//新建画布 画笔
	QImage img(getSize(), QImage::Format_ARGB32);
	img.fill(qRgba(0, 0, 0, 0));
	QPen pen(Qt::red);
	pen.setWidth(1);
	QPainter painter(&img);
	painter.setRenderHint(QPainter::Antialiasing, true);;
	painter.setPen(pen);
	
	//获取边界索引
	QPointF starPoint, endPoint;
	starPoint = d->getPoint(startIndex);
	transitionPoint(starPoint, xScale, xr, yScale, yr);
	startIndex++;
	//获取点 并绘制线
	for (int index = startIndex + 1 ; index < endIndex; index++)
	{
		endPoint = d->getPointHard(index);
		transitionPoint(endPoint, xScale, xr, yScale, yr);
		painter.drawLine(starPoint,endPoint);
		starPoint = endPoint;
	}
	//因为qpainter的屏幕坐标系原点在左上角，所以需要翻转图片才能得到我们想要的结果
	auto nImg = img.mirrored(false, true);
	setImage(nImg);
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
* @brief TimeRenderer::drawPointImage 渲染取点的页面
* @return bool
*/
bool TimeRenderer::drawPointImage()
{
	//获取接近点
	QPointF point = findPoint(getFindPosition());
	//屏幕坐标
	QPointF tPoint = point;
	//新建画布 画笔
	QImage img(getSize(), QImage::Format_ARGB32);
	img.fill(qRgba(0, 0, 0, 0));
	QPen pen(Qt::red);
	pen.setBrush(Qt::blue);
	pen.setWidth(5);
	QPainter painter(&img);
	painter.setPen(pen);

	//将数据坐标转换为屏幕坐标
	transitionPoint(tPoint);
	//坐标翻转（因为坐标系原点不一致的关系）
	tPoint.setY(getSize().height() - tPoint.y());
	//绘制点
	painter.drawPoint(tPoint);

	//绘制信息显示
	drawDisplayPoint(painter, tPoint, point);

	setImage(img);
	return true;
}

/**
* @brief TimeRenderer::setDefaultRang 设置默认的渲染范围
* @return bool
*/
bool TimeRenderer::setDefaultRang()
{
	auto timeData = std::dynamic_pointer_cast<TimeData>(data);
	if (!timeData)
		return false;
	/*
		默认情况，图表上方需要留出空白。
		如果有负值，默认情况下也需要将0作为一个刻度，所以下方也需要留白。
	*/
	auto yr = timeData->getYRang();
	if (yr.min < 0)
	{
		float j = (yr.max - yr.min) / 5;    //总长度除以8,得到平均值（上方多留一格所以除以8）
		int m = yr.max / j;       //获得正值需要多少格
		if ((m * j) > yr.max)    //解决浮点数精度问题（8.9999/3.0=3的问题）
			m--;
		int n = -(5 - m - 1); //获得负值需要的格数
		yr.max = j * (m + 1);   //获得最大值
		yr.min = j * (n - 1);  //获得最小值

	}else{                  //没有负值，留出上方空间即可
		yr.max *= 1.3;
	}
	setXRang(timeData->getXRang());
	setYRang(yr);

	return true;
}

/**
* @brief TimeRenderer::dataInit 初始化数据
* @return void
*/
void TimeRenderer::dataInit()
{
	Renderer::dataInit();
	auto timeDta = std::dynamic_pointer_cast<TimeData>(data);
	if (timeDta)
		timeDta->loadPoint();
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
* @brief TimeRenderer::transitionPoint 将一个数据点转换为屏幕上点
* @param QPointF & point
* @return void
*/
void TimeRenderer::transitionPoint(QPointF& point)
{
	//获取屏幕与数据的比例
	float xScale, yScale;
	getTransitionScale(xScale, yScale);
	transitionPoint(point, xScale, getXRang(), yScale, getYRang());
	
}

/**
* @brief TimeRenderer::findPoint 根据屏幕坐标寻找数据中最近的点
* @param const QPointF & point 屏幕坐标
* @return QT_NAMESPACE::QPointF 数据中最近的点
*/
QPointF TimeRenderer::findPoint(const QPointF& point)
{
	//获取屏幕与数据的比例
	float xScale, yScale;
	getTransitionScale(xScale, yScale);
	auto xr = getXRang();
	auto yr = getYRang();
	
	/*
		1. 在屏幕中寻找近似点时，在以点击点为中心的正方形区域中寻找。
		2. 给定一个正方形边长的初始长度。
		3. 如果在第一个区域中为找到一个点，那么增加正方形边长，继续寻找。
		4. 当在某个区域中找到一些点之后，将这些点与点击点的距离算出来比较，得出最近点。
	*/

	std::list<QPointF> points;	//区域中的点
	for (unsigned int rank = 1;points.size() == 0; rank++)
	{
		//正常行边长
		unsigned long riseLength = 10 * pow(2, rank);
		//正方形边界
		float xMin, xMax, yMin, yMax;
		xMax = point.x() + riseLength;
		xMin = point.x() - riseLength;
		yMax = point.y() + riseLength;
		yMin = point.y() - riseLength;

		//获取数据对象
		auto td = std::dynamic_pointer_cast<TimeData>(data);
		if (!td)
		{
#ifdef MY_DEBUG
			std::cerr << "TimeRenderer::findPoint td is nullptr" << std::endl;
#endif
			break;
		}
		//获取数据索引的边界点
		int startIndex = td->findIndexFromXValueL(xMin / xScale + xr.min);
		int endIndex = td->findIndexFromXValueR(xMax / xScale + xr.min);
		
		//寻找区域中的点
		QPointF p;
		for (int index = startIndex; index < endIndex; index++)
		{
			p = td->getPoint(index);
			float y = (p.y() - yr.min) * yScale;
			if (y > yMin && y < yMax)
				points.push_back(p);

		}

	}
	
	//距离
	float minDistance;
	QPointF temp;
	for (auto i = points.begin(); i != points.end(); i++)
	{
		float x = (i->x() - xr.min)*xScale;
		float y = (i->y() - yr.min)*yScale;
		float xDistance = abs(point.x() - x);
		float yDistance = abs(point.y() - y);
		float d = sqrt(pow(xDistance, 2) + pow(yDistance, 2));
		if (i == points.begin())
			minDistance = d;
		if (d < minDistance)
		{
			temp = *i;
			minDistance = d;
		}
	}
	return temp;

}

/**
* @brief TimeRenderer::drawDisplayPoint 在画布中显示点的信息
* @param QPainter & painter 绘制器
* @param const QPointF & position 点在屏幕上的位置
* @param const QPointF & d 点的数据
* @return void
*/
void TimeRenderer::drawDisplayPoint(QPainter& painter, const QPointF& position, const QPointF& d)
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

