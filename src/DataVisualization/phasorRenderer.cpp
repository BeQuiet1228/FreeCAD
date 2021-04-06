#include "phasorRenderer.h"
#include <qpen.h>
#include <QPainter>
#define  M_PI_ 3.141592653589793
phasorRenderer::phasorRenderer(std::shared_ptr<phasorData> data):Renderer(std::dynamic_pointer_cast<Data>(data))
{

}
phasorRenderer::~phasorRenderer(){

}
/**
* @brief phasorRenderer::drawImage 绘制图片
* @return bool
*/
bool phasorRenderer::drawImage(){
	//获取画布缩放
	float xScale(0.0), yScale(0.0);
	if (!getTransitionScale(xScale, yScale))
		return false;
	std::shared_ptr<phasorData> d = std::dynamic_pointer_cast<phasorData>(data);
	//获取x,y的取值范围
	auto xr = getXRang();
	auto yr = getYRang();
	//开始绘制
	QImage img(getSize(), QImage::Format_ARGB32);
	img.fill(qRgba(0, 0, 0, 0));
	QPen pen(Qt::black);
	pen.setWidth(1);
	QPainter painter(&img);
	painter.setRenderHint(QPainter::Antialiasing, true);
	painter.setPen(pen);
	//开始绘制图表
	/*QVector<QRectF> CutRoomlist = d->getAllCutRoom();
	for (auto iter = CutRoomlist.begin(); iter != CutRoomlist.end(); iter++)
		transitionRectF(*iter, xScale, yScale, xr, yr);
	painter.drawRects(CutRoomlist);*/
	QPen pen2(Qt::red);
	pen2.setWidth(2);
	painter.setPen(pen2);
	//绘制向量
	QVector<QPointF> p1 = d->Getp1Point();
	QVector<QPointF> p2 = d->Getp2Point();
	for (auto i = 0; i < p1.size();i++)
	{
		qreal _distance = sqrt((p2[i].x() - p1[i].x())*(p2[i].x()-p1[i].x())+(p2[i].y()-p1[i].y())*(p2[i].y()-p2[i].y()));
		if (_distance>0)
		{
			transitionpointF(p1[i], xScale, yScale, xr, yr);
			transitionpointF(p2[i], xScale, yScale, xr, yr);
			painter.drawLine(p1[i], p2[i]);
			painter.drawLine(p2[i], GetarrowTop(p2[i], p1[i]));
			painter.drawLine(p2[i], GetarrowBottom(p2[i], p1[i]));
		}
		
	}
	auto nImg = img.mirrored(false, true);
	setImage(nImg);
	return true;

	
}
/**
* @brief phasorRenderer::addListRang 
* @param std::list<Data::Rang> listRang
* @return bool
*/
bool phasorRenderer::addListRang(std::list<Data::Rang> listRang){
	return true;
}
/**
* @brief phasorRenderer::drawPointImage 绘制取点画面
* @return bool
*/
bool phasorRenderer::drawPointImage(){

	return true;
}
/**
* @brief phasorRenderer::setDefaultRang 设置默认坐标系数值范围
* @return bool
*/
bool phasorRenderer::setDefaultRang(){
	auto _phasorData = std::dynamic_pointer_cast<phasorData>(data);
	if (!_phasorData)
		return false;
	setXRang(_phasorData->getXRang());
	setYRang(_phasorData->getYRang());
	return true;
}
/**
* @brief phasorRenderer::dataInit 数据初始化
* @return void
*/
void phasorRenderer::dataInit(){
	Renderer::dataInit();
	auto _phasordata = std::dynamic_pointer_cast<phasorData>(data);
	if (_phasordata)
	{
		_phasordata->loadPoint();
	}
}
/**
* @brief phasorRenderer::transitionpointF 直角坐标系点位转换为屏幕点位
* @param QPointF & p
* @param const float& xScale
* @param const float& yScale
* @param const Data::Rang xr
* @param const Data::Rang yr
* @return void
*/
void phasorRenderer::transitionpointF(QPointF & p, const float& xScale, const float& yScale, const Data::Rang xr, const Data::Rang yr)
{
	p.setX(transitionX(p.x(), xScale, xr));
	p.setY(transitionY(p.y(), yScale, yr));
}
/**
* @brief phasorRenderer::GetarrowTop 获取箭头上半段
* @param QPointF endpoint 
* @param QPointF startpoint
* @return QPointF 
*/
QPointF phasorRenderer::GetarrowTop(QPointF endpoint, QPointF startpoint){
	//先获取线段长度
	qreal _distance = sqrt((endpoint.x() - startpoint.x())*(endpoint.x() - startpoint.x())+
		(endpoint.y() - startpoint.y())*(endpoint.y() - startpoint.y()));
	QLineF line(startpoint,endpoint);
	double angle = std::atan2(-line.dy(), line.dx());
	qreal arrowSize;
	if (_distance>30)
		arrowSize = 10;
	else
		arrowSize = _distance / 3;
	QPointF arrowP1 = line.p2() - QPointF(sin(angle + M_PI_ / 3)*arrowSize,
		cos(angle + M_PI_ / 3)*arrowSize);
	return arrowP1;
}
/**
* @brief phasorRenderer::GetarrowBottom 获取箭头下半段
* @param QPointF endpoint
* @param QPointF startpoint
* @return QPointF
*/
QPointF phasorRenderer::GetarrowBottom(QPointF endpoint, QPointF startpoint){
	qreal _distance = sqrt((endpoint.x()-startpoint.x())*(endpoint.x()-startpoint.x())+
		(endpoint.y()-startpoint.y())*(endpoint.y()-startpoint.y()));
	QLineF line(startpoint, endpoint);
	double angle = std::atan2(-line.dy(),line.dx());
	qreal arrowSize;
	if (_distance > 30)
		arrowSize = 10;
	else
		arrowSize = _distance / 3;
	QPointF arrowP2 = line.p2() - QPointF(sin(angle+M_PI_-M_PI_/3)*arrowSize,
		cos(angle+M_PI_-M_PI_/3)*arrowSize);
	return arrowP2;
}