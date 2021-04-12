#include "ContourRenderPolar.h"
#include "ContourRender.h"
#include "qwt/qwt_scale_map.h"
#include <qmath.h>
ContourRenderPolar::ContourRenderPolar(std::shared_ptr<ContourData> data)
	:Renderer(data)
{
	setRenderThreadCount(0);
	setColorMap(new ColorMap);

}

ContourRenderPolar::~ContourRenderPolar()
{
	
}

bool ContourRenderPolar::drawImage()
{
	QwtScaleMap xmap, ymap;
	xmap.setPaintInterval(0, this->getSize().height()/2);
	xmap.setScaleInterval(0, getXRang().max);
	ymap.setPaintInterval(0, 2*M_PI);
	ymap.setScaleInterval(getYRang().min, getYRang().max);
	QRectF rect(0, 0, getSize().width(), getSize().height());

	//ÐÂ½¨»­²¼ »­±Ê
	QImage img(getSize(), QImage::Format_ARGB32);
	img.fill(qRgba(0, 0, 0, 0));
	QPainter painter(&img);
	painter.setRenderHint(QPainter::Antialiasing, true);
	draw(&painter, ymap, xmap, QPointF(rect.width()/2,rect.height()/2),rect.height()/10,rect);

	//renderImage(xmap, ymap, rect, getSize());

	setImage(img.mirrored(false, true));

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

	setXRang(xr);
	setYRang(yr);

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

