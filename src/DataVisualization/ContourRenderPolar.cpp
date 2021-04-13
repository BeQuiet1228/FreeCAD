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


	QImage img = renderImage(xmap, ymap, rect, getSize());

	
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



