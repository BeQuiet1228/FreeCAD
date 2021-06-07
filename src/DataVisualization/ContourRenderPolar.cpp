#include "ContourRenderPolar.h"
#include "ContourRender.h"
#include "qwt/qwt_scale_map.h"
#include <qmath.h>
#include <memory.h>
#include <QtConcurrentRun>
#include <QRectF>
#include <QImage>
#include "CustomConfig.h"
#include "C_encoding.h"
#include <math.h>
#include "ConfigWidget.h"
ContourRenderPolar::ContourRenderPolar(std::shared_ptr<ContourData> data)
	:ContourRender(data)
{

}

ContourRenderPolar::~ContourRenderPolar()
{
	
}

bool ContourRenderPolar::drawImage()
{
	//setColorMap(ConfigWidget::getQwtLinearColorMap());
	if (colormapsite!=lastcolormapsite)
	{
		lastcolormapsite = colormapsite;
		QwtLinearColorMap* map = reinterpret_cast<QwtLinearColorMap*>(colormapsite);
		setColorMap(map);
	}
	QwtScaleMap xmap, ymap;
	xmap.setPaintInterval(0, this->getSize().width());
	xmap.setScaleInterval(getXRang().min, getXRang().max);
	ymap.setPaintInterval(0, this->getSize().height());
	ymap.setScaleInterval(getYRang().min, getYRang().max);
	QRectF rect(0, 0, getSize().width(), getSize().height());




	//新建画布 画笔
	QImage img(getSize(), QImage::Format_ARGB32);
	img.fill(qRgba(0, 0, 0, 0));

	if (testDisplayMode(DisplayMode::ImageMode))
	{
		img = renderImage(xmap, ymap, rect, getSize());
	}
	if (testDisplayMode(DisplayMode::ContourMode))
	{
		QPainter painter(&img);
		painter.setRenderHint(QPainter::Antialiasing, cfgInfo.isAA);



		QRectF area = QwtScaleMap::invTransform(xmap, ymap, rect);
		QwtRasterData::ContourLines lines = renderContourLines(area, rect.toRect().size());
		drawContourLines(&painter, xmap, ymap, lines);
	}

	setImage(img.mirrored(false, true));

	return true;
}

bool ContourRenderPolar::addListRang(std::list<Data::Rang> listRang)
{
	return true;
}

bool ContourRenderPolar::drawPointImage()
{
	std::shared_ptr<ContourData> d = std::dynamic_pointer_cast<ContourData>(Renderer::data);

	auto pos = getFindPosition();
	//获取屏幕与数据的比例
	float xScale, yScale;
	getTransitionScale(xScale, yScale);
	Data::Rang xr = getXRang(), yr = getYRang();

	ContourData::Grid grid = findPoint();
	float r = grid.x, theta = grid.y;
	float x, y;
	x = r * std::cos(theta);
	y = R * std::sin(theta);

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

	std::map<QString, float> list;
	list["R"] = r;
	list["THETA"] = theta;
	list["Value"] = grid.value;
	displayPointInformation(&painter, &point, list);
	setImage(img);
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
	setContourLevels(contourLevels);
	return true;
}

void ContourRenderPolar::dataInit()
{
	auto cd = std::dynamic_pointer_cast<ContourData>(Renderer::data);
	cd->loadPoint();
	setData(cd->getQwtMatrixRasterData());
}

ContourData::Grid ContourRenderPolar::findPoint()
{
	QPointF pos = getFindPosition();
	
	float xscale, yscale;
	if (!getTransitionScale(xscale, yscale))
	{
		std::cerr << "ContourRenderPolar::findPoint() get scale failed!" << std::endl;
	}

	float x, y;
	x = pos.x()/xscale + getXRang().min;
	y = pos.y()/yscale + getYRang().min;

	float r, theta;
	r = std::sqrt(std::pow(x, 2) + std::pow(y, 2));
	//这里使用y判断象限 然后调整theta的值
	if (y < 0)
	{
		theta = std::acos(x / r);
	}else {
		theta = 2*M_PI - std::acos(x / r);
	}
	
	std::cerr << "R:" << r << ",THETA:" << theta << std::endl;

	auto d = std::dynamic_pointer_cast<ContourData>(Renderer::data);

	return d->findGrid(r, theta);
}

/**
* @brief  ContourRenderPolar::setDefaultRang 设置坐标系默认取值范围
* @param  QSize &  
* @return bool  
*/
bool ContourRenderPolar::setDefaultRang(QSize& size){
	Data::Rang xr, yr;
	auto cd = std::dynamic_pointer_cast<ContourData>(Renderer::data);
	xr = cd->getXRang();
	yr = cd->getXRang();
	yr.min = -yr.max;
	setYRang(yr);
	float width = size.width();
	float height = size.height();
	float scale_w = width / height;
	xr.min = -xr.max;
	float xWidth=(xr.max - xr.min) * scale_w;
	xr.min = -xWidth / 2;
	xr.max = xWidth / 2;
	setXRang(xr);
	Data::Rang vr = cd->getVlaueRange();
	QList<double> contourLevels;
	for (double level = (vr.length() / 10 + vr.min); level < vr.max; level += vr.length() / 10)
		contourLevels += level;
	setContourLevels(contourLevels);
	return true;
}

