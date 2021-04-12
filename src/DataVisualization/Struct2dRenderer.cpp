#include "Struct2dRenderer.h"
#include <qpen.h>
#include <QPainter>
Struct2DRenderer::Struct2DRenderer(std::shared_ptr<Struct2dData> data):
Renderer(std::dynamic_pointer_cast<Data> (data)){

	color_tab[1]=QColor(125,125,125);
	color_tab[3]=QColor(255,255,125);
	color_tab[4]=QColor(255,125,125);
	color_tab[5]=QColor(125,125,255);
	color_tab[6]=QColor(255,255,0);
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
	QPainter painter(&img);
	painter.setPen(pen);
	std::map<int, std::map<int, std::vector<QPointF>>> map=d->GetAllinfo();
	for (auto iter = map.begin(); iter != map.end();iter++)
	{
		auto itercolor = color_tab.find(iter->first);
		if (itercolor!=color_tab.end())
		{
			QBrush brush(itercolor.value());
			painter.setBrush(brush);
			for (auto iterlines = iter->second.begin(); iterlines != iter->second.end();iterlines++)
			{
				if (iterlines->second.size() == 2)
				{
					auto iterpoint = (*iterlines).second.begin();
					transitionPoint(*iterpoint, xScale, xr, yScale, yr);
					transitionPoint(*(iterpoint + 1),xScale,xr,yScale,yr);
					painter.drawLine((*iterpoint),*(iterpoint+1));
				}
				else
				{
					QPainterPath _path;
					auto iterpoint = (*iterlines).second.begin();
					transitionPoint(*iterpoint,xScale,xr,yScale,yr);
					_path.moveTo(*iterpoint); iterpoint++;
					for (;iterpoint!=(*iterlines).second.end();iterpoint++)
					{
						transitionPoint(*iterpoint, xScale, xr, yScale, yr);
						_path.lineTo(*iterpoint);
					}
					painter.drawPath(_path);
				}
				

			}
		}
	}
	auto nImg = img.mirrored(false, true);
	setImage(nImg);
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