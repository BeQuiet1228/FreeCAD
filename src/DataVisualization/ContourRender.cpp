
#include "ContourRender.h"
#include "qwt/qwt_scale_map.h"
#include <QRectF>
#include <QImage>
#include "Data.h"
#include <memory.h>
#include <QtConcurrentRun>
#include <qmath.h>
ContourRender::ContourRender(std::shared_ptr<ContourData> data)
	:Renderer(std::dynamic_pointer_cast<Data>(data))
{
	setRenderThreadCount(1);
	setColorMap(new ColorMap);
}

ContourRender::~ContourRender()
{

}

bool ContourRender::drawImage()
{
	QwtScaleMap xmap, ymap;
	xmap.setPaintInterval(0, this->getSize().height() / 2);
	xmap.setScaleInterval(0, getXRang().max);
	ymap.setPaintInterval(0, this->getSize().height()/2);
	ymap.setScaleInterval(0, getYRang().max);
	QRectF rect(0, 0, getSize().width(), getSize().height());
	
	size = getSize();

	QImage img = renderImage(xmap, ymap, rect, getSize());

	setImage(img.mirrored(false, true));
	//setImage(img);
	return true;
}

bool ContourRender::addListRang(std::list<Data::Rang> listRang)
{
	return false;
}

bool ContourRender::drawPointImage()
{
	std::shared_ptr<ContourData> d = std::dynamic_pointer_cast<ContourData>(Renderer::data);

	auto pos = getFindPosition();
	//获取屏幕与数据的比例
	float xScale, yScale;
	getTransitionScale(xScale, yScale);
	Data::Rang xr = getXRang(), yr = getYRang();

	ContourData::Grid grid = d->findGrid(pos.x()/xScale+xr.min, pos.y()/yScale+yr.min);
	

	float x = grid.x, y = grid.y;
	x = transitionDataToScreen(x, xScale, getXRang());
	y = transitionDataToScreen(y, yScale, getYRang());
	//坐标翻转（因为坐标系原点不一致的关系）
	y = getSize().height() - y;

	//新建画布 画笔
	QImage img(getSize(), QImage::Format_ARGB32);
	img.fill(qRgba(0, 0, 0, 0));
	QPen pen(Qt::red);
	pen.setBrush(Qt::blue);
	pen.setWidth(5);
	QPainter painter(&img);
	painter.setPen(pen);

	QPointF point(x, y);
	painter.drawPoint(point);

	drawDisplayPoint(painter, point, grid);
	setImage(img);
	return true;
}

bool ContourRender::setDefaultRang()
{
	Data::Rang xr, yr;
	
	auto cd = std::dynamic_pointer_cast<ContourData>(Renderer::data);
	xr = cd->getXRang();
	yr = cd->getYRang();

	setXRang(xr);
	setYRang(yr);

	Data::Rang vr = cd->getVlaueRange();

	QList<double> contourLevels;
	for (double level = (vr.length()/10 + vr.min); level < vr.max; level += vr.length()/10)
		contourLevels += level;
	setContourLevels(contourLevels);
	return true;
}

void ContourRender::dataInit()
{
	auto cd = std::dynamic_pointer_cast<ContourData>(Renderer::data);
	cd->loadPoint();
	setData(cd->getQwtMatrixRasterData());
}

Data::Rang ContourRender::getValueRange()
{
	auto d = std::dynamic_pointer_cast<ContourData>(Renderer::data);
	if (!d)
		return Data::Rang();
	return d->getVlaueRange();
}

/**
* @brief ContourRender::drawDisplayPoint 显示点提示框
* @param QPainter & painter 画笔
* @param const QPointF & position 位置
* @param const ContourData::Grid & grid 网格信息
* @return void
*/
void ContourRender::drawDisplayPoint(QPainter& painter, const QPointF& position, const ContourData::Grid& grid)
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
		displayRect.setY(displayRect.y() - 90);
	}
	if (displayRect.x() > (size.width() - 170))
	{
		displayRect.setX(displayRect.x() - 190);
	}

	displayRect.setWidth(150);
	displayRect.setHeight(80);
	painter.drawRect(displayRect);
	//绘制显示信息
	QFont f;
	f.setPixelSize(17);
	painter.setFont(f);
	painter.drawText(displayRect.x() + 10,
		displayRect.y() + 20,
		QString("X:%1").arg(grid.x, 0, 'E', 2)
		);
	painter.drawText(displayRect.x() + 10,
		displayRect.y() + 40,
		QString("Y:%1").arg(grid.y, 0, 'E', 2)
		);
	painter.drawText(displayRect.x() + 10,
		displayRect.y() + 60,
		QString("Value:%1").arg(grid.value, 0, 'E', 2)
		);
}

void ContourRender::renderTile(const QwtScaleMap &xMap, const QwtScaleMap &yMap, const QRect &tile, QImage *image) const
{
	const QwtInterval range = d_data->data->interval(Qt::ZAxis);
	if (!range.isValid())
		return;

	if (d_data->colorMap->format() == QwtColorMap::RGB)
	{
		for (int y = tile.top(); y <= tile.bottom(); y++)
		{
			//const double ty = yMap.invTransform(y);
			QPointF f;
			QRgb *line = reinterpret_cast<QRgb *>(image->scanLine(y));
			line += tile.left();

			for (int x = tile.left(); x <= tile.right(); x++)
			{
				//const double tx = xMap.invTransform(x);
				f = transiton(xMap, yMap, x, y);
				*line++ = d_data->colorMap->rgb(range,
					d_data->data->value(f.x(),f.y()));
			}
		}
	}
	else if (d_data->colorMap->format() == QwtColorMap::Indexed)
	{
		for (int y = tile.top(); y <= tile.bottom(); y++)
		{
			const double ty = yMap.invTransform(y);

			unsigned char *line = image->scanLine(y);
			line += tile.left();

			for (int x = tile.left(); x <= tile.right(); x++)
			{
				const double tx = xMap.invTransform(x);

				*line++ = d_data->colorMap->colorIndex(range,
					d_data->data->value(tx, ty));
			}
		}
	}
}

QImage ContourRender::renderImage(const QwtScaleMap &xMap, const QwtScaleMap &yMap, const QRectF &area, const QSize &imageSize) const
{
	if (imageSize.isEmpty() || d_data->data == NULL
		|| d_data->colorMap == NULL)
	{
		return QImage();
	}

	const QwtInterval intensityRange = d_data->data->interval(Qt::ZAxis);
	if (!intensityRange.isValid())
		return QImage();

	QImage::Format format = (d_data->colorMap->format() == QwtColorMap::RGB)
		? QImage::Format_ARGB32 : QImage::Format_Indexed8;

	QImage image(imageSize, format);

	if (d_data->colorMap->format() == QwtColorMap::Indexed)
		image.setColorTable(d_data->colorMap->colorTable(intensityRange));

	d_data->data->initRaster(area, image.size());

#if DEBUG_RENDER
	QElapsedTimer time;
	time.start();
#endif

#if QT_VERSION >= 0x040400 && !defined(QT_NO_QFUTURE)
	uint numThreads = renderThreadCount();

	if (numThreads <= 0)
		numThreads = QThread::idealThreadCount();

	if (numThreads <= 0)
		numThreads = 1;

	const int numRows = imageSize.height() / numThreads;

	QList< QFuture<void> > futures;
	for (uint i = 0; i < numThreads; i++)
	{
		QRect tile(0, i * numRows, image.width(), numRows);
		if (i == numThreads - 1)
		{
			tile.setHeight(image.height() - i * numRows);
			renderTile(xMap, yMap, tile, &image);
		}
		else
		{
			futures += QtConcurrent::run(
				this, &ContourRender::renderTile,
				xMap, yMap, tile, &image);
		}
	}
	for (int i = 0; i < futures.size(); i++)
		futures[i].waitForFinished();

#else // QT_VERSION < 0x040400
	const QRect tile(0, 0, image.width(), image.height());
	renderTile(xMap, yMap, tile, &image);
#endif

#if DEBUG_RENDER
	const qint64 elapsed = time.elapsed();
	qDebug() << "renderImage" << imageSize << elapsed;
#endif

	d_data->data->discardRaster();

	return image;
}

QPointF ContourRender::transiton(const QwtScaleMap &xMap, const QwtScaleMap &yMap, const double& x, const double& y) const
{
	QPointF origin(size.width()/2,size.height()/2);
	double nx, ny;
	nx = x - origin.x();
	ny = y - origin.y();

	double r, theta;
	theta = qAtan2(nx,ny);
	r = sqrt(pow(nx,2) + pow(ny,2));
	r = xMap.invTransform(r);

	if (theta < 0.0)
		theta += 2 * M_PI;
	if (theta < xMap.p1())
		theta += 2 * M_PI;


	return QPointF(r, theta);
}
