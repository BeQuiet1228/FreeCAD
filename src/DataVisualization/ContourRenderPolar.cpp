#include "ContourRenderPolar.h"
#include "ContourRender.h"
#include "qwt/qwt_scale_map.h"
#include <qmath.h>
#include <memory.h>
#include <QtConcurrentRun>
#include <QRectF>
#include <QImage>
ContourRenderPolar::ContourRenderPolar(std::shared_ptr<ContourData> data)
	:ContourRender(data)
{
	setRenderThreadCount(1);
	setColorMap(new ColorMap);

}

ContourRenderPolar::~ContourRenderPolar()
{
	
}

bool ContourRenderPolar::drawImage()
{
	initTransitionData();

	QwtScaleMap xmap, ymap;
	xmap.setPaintInterval(0, this->getSize().width());
	xmap.setScaleInterval(getXRang().min, getXRang().max);
	ymap.setPaintInterval(0, this->getSize().height());
	ymap.setScaleInterval(getYRang().min, getYRang().max);
	QRectF rect(0, 0, getSize().width(), getSize().height());

	size = getSize();

	QImage img = renderImage(xmap, ymap, rect, getSize());

	setImage(img.mirrored(false, true));
	//setImage(img);
	return true;
}

bool ContourRenderPolar::addListRang(std::list<Data::Rang> listRang)
{
	return true;
}

bool ContourRenderPolar::drawPointImage()
{
	return true;
}

bool ContourRenderPolar::setDefaultRang()
{
	Data::Rang xr, yr;

	auto cd = std::dynamic_pointer_cast<ContourData>(Renderer::data);
	xr = cd->getXRang();
	yr = cd->getYRang();

	xr.min = -xr.max;

	setXRang(xr);
	setYRang(xr);

	Data::Rang vr = cd->getVlaueRange();

	QList<double> contourLevels;
	for (double level = (vr.length() / 10 + vr.min); level < vr.max; level += vr.length() / 10)
		contourLevels += level;
	//setContourLevels(contourLevels);
	return true;
}

void ContourRenderPolar::dataInit()
{
	auto cd = std::dynamic_pointer_cast<ContourData>(Renderer::data);
	cd->loadPoint();
	setData(cd->getQwtMatrixRasterData());
}

void ContourRenderPolar::renderTile(const QwtScaleMap &xMap, const QwtScaleMap &yMap, const QRect &tile, QImage *image) const
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
					d_data->data->value(f.x(), f.y()));
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

QImage ContourRenderPolar::renderImage(const QwtScaleMap &xMap, const QwtScaleMap &yMap, const QRectF &area, const QSize &imageSize) const
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
				this, &ContourRenderPolar::renderTile,
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

QPointF ContourRenderPolar::transiton(const QwtScaleMap &xMap, const QwtScaleMap &yMap, const double& x, const double& y) const
{
	//QPointF origin(size.width() / 2, size.height() / 2);

	double MaxR = size.width() > size.height() ? size.height() / 2 : size.width() / 2;
	double xScale = size.width() / 2 / MaxR;
	double yScale = size.height() / 2 / MaxR;


	double nx, ny;
	nx = (x - origin.x())/xScale;
	ny = (y - origin.y());

	nx = xMap.invTransform(x);
	ny = yMap.invTransform(y);

	double r, theta;
	theta = qAtan2(nx, ny);
	r = sqrt(pow(nx, 2) + pow(ny, 2));
	//r = xMap.invTransform(r);

	if (theta < 0.0)
		theta += 2 * M_PI;
	if (theta < xMap.p1())
		theta += 2 * M_PI;


	return QPointF(r, theta);
}

void ContourRenderPolar::initTransitionData()
{
	Data::Rang xr, yr;
	xr = getXRang();
	yr = getYRang();

	auto d = std::dynamic_pointer_cast<ContourData>(Renderer::data);

	double rMax = d->getXRang().max;

	QSize size = getSize();
	double xScale = size.width() / xr.length();
	double yScale = size.height() / yr.length();
	
	origin.setX(-xr.min*xScale);
	origin.setY(yr.max*yScale);

	 this->xScale = (size.width() / xr.length()) / (size.height() / yr.length());
	//double yScale = size.height() / 2 / MaxR;
}

