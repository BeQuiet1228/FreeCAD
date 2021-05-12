#include "ContourRenderPolar.h"
#include "ContourRender.h"
#include "qwt/qwt_scale_map.h"
#include <qmath.h>
#include <memory.h>
#include <QtConcurrentRun>
#include <QRectF>
#include <QImage>
#include "CustomConfig.h"

ContourRenderPolar::ContourRenderPolar(std::shared_ptr<ContourData> data)
	:ContourRender(data)
{

}

ContourRenderPolar::~ContourRenderPolar()
{
	
}

bool ContourRenderPolar::drawImage()
{

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
		painter.setRenderHint(QPainter::Antialiasing, contourPolarparam.isAA);



		QRectF area = QwtScaleMap::invTransform(xmap, ymap, rect);
		QwtRasterData::ContourLines lines = renderContourLines(area, rect.toRect().size());
		drawContourLines(&painter, xmap, ymap, lines);
	}

	setImage(img.mirrored(false, true));

	return true;

/*
	QImage img = renderImage(xmap, ymap, rect, getSize());
	QPainter painter(&img);
	painter.setRenderHint(QPainter::Antialiasing, true);


	
	QRectF area = QwtScaleMap::invTransform(xmap, ymap, rect);
	QwtRasterData::ContourLines lines =renderContourLines(area, rect.toRect().size());
	drawContourLines(&painter, xmap, ymap, lines);

	setImage(img.mirrored(false, true));

	return true; */
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
	setContourLevels(contourLevels);
	return true;
}

void ContourRenderPolar::dataInit()
{
	auto cd = std::dynamic_pointer_cast<ContourData>(Renderer::data);
	cd->loadPoint();
	setData(cd->getQwtMatrixRasterData());
}
void ContourRenderPolar::loadconfig()
{
	Config::GetInstance()->loadConfig();
	ConfigGroup mGroup = Config::GetInstance()->getRootGroup();
	ConfigGroup contourGroup = mGroup.getGroup("Contour");
	//获取抗锯齿属性
	contourPolarparam.isAA = atoi(contourGroup.getValue("isAlis").c_str());
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

