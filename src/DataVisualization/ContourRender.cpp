
#include "ContourRender.h"
#include "qwt/qwt_scale_map.h"
#include <QRectF>
#include <QImage>
#include "Data.h"
#include <memory.h>
ContourRender::ContourRender(std::shared_ptr<ContourData> data)
	:Renderer(std::dynamic_pointer_cast<Data>(data))
{
	setRenderThreadCount(4);
	setColorMap(new ColorMap);
}

ContourRender::~ContourRender()
{

}

bool ContourRender::drawImage()
{
	QwtScaleMap xmap, ymap;
	xmap.setPaintInterval(0, this->getSize().width());
	xmap.setScaleInterval(getXRang().min, getXRang().max);
	ymap.setPaintInterval(0, this->getSize().height());
	ymap.setScaleInterval(getYRang().min, getYRang().max);
	QRectF rect(0, 0, getSize().width(), getSize().height());

	//ÐÂ½¨»­²¼ »­±Ê
	QImage img(getSize(), QImage::Format_ARGB32);
	img.fill(qRgba(0, 0, 0, 0));
	QPainter painter(&img);
	painter.setRenderHint(QPainter::Antialiasing, true);
	draw(&painter, xmap, ymap, rect);

	//renderImage(xmap, ymap, rect, getSize());

	setImage(img.mirrored(false, true));

	return true;
}

bool ContourRender::addListRang(std::list<Data::Rang> listRang)
{
	return false;
}

bool ContourRender::drawPointImage()
{
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
