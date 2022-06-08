#include "CurveRenderer.h"

DV::CurveRenderer::CurveRenderer(const std::shared_ptr<CurveData> data)
	:TimeRenderer(data),pointColor(Qt::blue)
{

}

DV::CurveRenderer::~CurveRenderer()
{

}

void DV::CurveRenderer::dataInit()
{
	return;
}

bool DV::CurveRenderer::drawImage()
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
	endIndex = d->findIndexFromXValueR(xr.max);


	//新建画布 画笔
	QImage img(getSize(), QImage::Format_ARGB32);
	img.fill(qRgba(0, 0, 0, 0));
	QPen pen(penColor);
	pen.setWidth(pensize);
	QPainter painter(&img);
	painter.setRenderHint(QPainter::Antialiasing, isAA);
	painter.setPen(pen);
	QPen pointPen(pointColor);
	pointPen.setWidth(pensize + 2);

	//获取边界索引
	QPointF starPoint, endPoint;
	starPoint = d->getPoint(startIndex);
	transitionPoint(starPoint, xScale, xr, yScale, yr);
	//获取点 并绘制线
	for (int index = startIndex + 1; index < endIndex; index++)
	{
		endPoint = d->getPointHard(index);
		transitionPoint(endPoint, xScale, xr, yScale, yr);

		//画曲线
		painter.setPen(pen);
		painter.drawLine(starPoint, endPoint);

		//画点
		painter.setPen(pointPen);
		painter.drawPoint(endPoint);

		starPoint = endPoint;
	}
	//因为qpainter的屏幕坐标系原点在左上角，所以需要翻转图片才能得到我们想要的结果
	auto nImg = img.mirrored(false, true);
	setImage(nImg);
	return true;
}

bool DV::CurveRenderer::drawPointImage()
{
	//获取接近点
	int pointIndex = 0;
	QPointF point = findPoint(getFindPosition(),pointIndex);
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
	std::map<QString, float> list;
	list["X"] = point.x();
	list["Y"] = point.y();
	//绘制附加信息
	std::shared_ptr<CurveData> d = std::dynamic_pointer_cast<CurveData>(getData());
	if (d)
	{
		auto parValues = d->getParValues();
		for (auto iter = parValues.begin(); iter != parValues.end(); iter++)
		{
			list[iter->first] = iter->second[pointIndex];
		}
	}
	displayPointInformation(&painter, &tPoint, list);
	setImage(img);
	return true;
}

void DV::CurveRenderer::setPointColor(const QColor& color)
{
	pointColor = color;
}

QColor DV::CurveRenderer::getPointColor()
{
	return pointColor;
}

QPointF DV::CurveRenderer::findPoint(const QPointF& point, int& index)
{
	auto timeData = std::dynamic_pointer_cast<TimeData>(getData());
	if (!timeData)
	{
#ifdef MY_DEBUG
		std::cerr << "TimeRenderer::findPoint td is nullptr" << std::endl;
#endif
		return QPointF(0, 0);
	}
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

	//使用一个结构体来存储临时数据，
	struct PointIndex
	{
		QPointF point;
		int index;
	};

	std::list<PointIndex> points;	//区域中的点
	for (unsigned int rank = 1; points.size() == 0; rank++)
	{
		//正常行边长
		unsigned long riseLength = 10 * pow(2, rank);
		//正方形边界
		float xMin, xMax, yMin, yMax;
		xMax = point.x() + riseLength;
		xMin = point.x() - riseLength;
		yMax = point.y() + riseLength;
		yMin = point.y() - riseLength;

		/*
			当rank过大时，又可能会出现范围超过边界，那么mini会为负值，
			按照当前的算法，会导致获取数据索引不正确，所以这里加判断避免这种情况
		*/
		if (xMin < 0)
			xMin = 0;
		if (yMin < 0)
			yMin = 0;

		//获取数据索引的边界点
		int startIndex = timeData->findIndexFromXValueL(xMin / xScale + xr.min);
		int endIndex = timeData->findIndexFromXValueR(xMax / xScale + xr.min);

		//寻找区域中的点
		QPointF p;
		for (int index = startIndex; index < endIndex; index++)
		{
			p = timeData->getPoint(index);
			float y = (p.y() - yr.min) * yScale;
			if (y > yMin && y < yMax)
			{
				PointIndex pi;
				pi.point = p;
				pi, index = index;
				points.push_back(pi);
			}
				

		}

	}

	//距离
	float minDistance;
	QPointF temp;
	for (auto i = points.begin(); i != points.end(); i++)
	{
		float x = (i->point.x() - xr.min) * xScale;
		float y = (i->point.y() - yr.min) * yScale;
		float xDistance = abs(point.x() - x);
		float yDistance = abs(point.y() - y);
		float d = sqrt(pow(xDistance, 2) + pow(yDistance, 2));
		if (i == points.begin())
		{
			minDistance = d;
			temp = i->point;
			index = i->index;
		}

		if (d < minDistance)
		{
			temp = i->point;
			minDistance = d;
			index = i->index;
		}
	}
	return temp;
}

