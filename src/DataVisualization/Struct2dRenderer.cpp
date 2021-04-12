#include "Struct2dRenderer.h"
#include <qpen.h>
Struct2DRenderer::Struct2DRenderer(std::shared_ptr<Struct2dData> data):
Renderer(std::dynamic_pointer_cast<Data> (data)){
}
Struct2DRenderer::~Struct2DRenderer(){  }
bool Struct2DRenderer::drawImage() {
	float xScale, yScale;
	if (!getTransitionScale(xScale, yScale))
		return false;
	std::shared_ptr<Struct2dData> d = std::dynamic_pointer_cast<Struct2dData>(data);
	//获取x,y的取值范围
	auto xr = getXRang();
	auto yr = getYRang();
	//开始绘制
	QImage img(getSize(), QImage::Format_ARGB32);
	img.fill(qRgba(0, 0, 0, 0));
	QPen pen(Qt::black);
	pen.setWidth(1);
	std::map<int, std::map<int, std::vector<QPointF>>> map;
	return true;
}
bool Struct2DRenderer::addListRang(std::list<Data::Rang> listRang){
	return true;
}
bool Struct2DRenderer::drawPointImage(){
	return true;
}
bool Struct2DRenderer::setDefaultRang(){
	auto _Struct2DData = std::dynamic_pointer_cast<Struct2dData>(data);
	if (!_Struct2DData)
		return false;
	setXRang(_Struct2DData->getXRang());
	setYRang(_Struct2DData->getYRang());
	return true;
}
void Struct2DRenderer::dataInit(){
	Renderer::dataInit();
	auto _Struct2DData = std::dynamic_pointer_cast<Struct2dData>(data);
	if (_Struct2DData)
	{
		_Struct2DData->loadPoint();
	}
}