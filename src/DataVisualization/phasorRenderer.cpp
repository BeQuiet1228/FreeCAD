#include "phasorRenderer.h"
#include <qpen.h>
#include <QPainter>
#define  M_PI_ (3.141592653589793)
#define  HORI_GRID (10.0f)
#define  VERT_GRID (10.0f)
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
	//return drawImage_Coord();
	return drawImage_Scence();
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
/**
* @brief phasorRenderer::transionVector 向量坐标转换
* @param QPointF endpoint
* @param QPointF startpoint
* @param const float& xScale
* @param const float& yScale
* @retrun void
*/
void phasorRenderer::transionVector(QPointF& endpoint, QPointF startpoint, const float& xScale, const float& yScale)
{
	qreal x_distance = (endpoint.x() - startpoint.x())*xScale;
	qreal y_distance = (endpoint.y() - startpoint.y())*yScale;
	endpoint.setX( x_distance+ startpoint.x());
	endpoint.setY( y_distance+ startpoint.y());
}

bool phasorRenderer::drawImage_Scence(){
	//获取画布缩放
	float xScale(0.0), yScale(0.0);
	if (!getTransitionScale(xScale, yScale))
		return false;
	//获取data数据
	std::shared_ptr<phasorData> d = std::dynamic_pointer_cast<phasorData>(data);
	//获取x,y的范围
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
	//获取屏幕网格10*10
	QVector<QRectF> CutRect = GetRectF_Scene(xr, yr);
	for (auto iter = CutRect.begin(); iter != CutRect.end(); iter++)
		transitionRectF(*iter, xScale, yScale, xr, yr);
	painter.drawRects(CutRect);
	//寻找向量
	QPen pen2(Qt::red);
	pen2.setWidth(2);
	painter.setPen(pen2);
	//

	//先画出传统的向量
	//绘制向量
	QVector<QPointF> p1 = d->Getp1Point();
	QVector<QPointF> p2 = d->Getp2Point();
	//向量可能太小，需要缩放
	for (auto i = 0; i < p1.size(); i++)
	{
			//transitionpointF(p1[i],d->GetVecXScale(),d->GetVecYScale(),xr,yr);
			//transitionpointF(p2[i], d->GetVecXScale(), d->GetVecYScale(), xr, yr);
			transionVector(p2[i], p1[i], d->GetVecXScale(), d->GetVecYScale());
			transitionpointF(p1[i], xScale, yScale, xr, yr);
			transitionpointF(p2[i], xScale, yScale, xr, yr);
			/*painter.drawLine(p1[i], p2[i]);
			painter.drawLine(p2[i], GetarrowTop(p2[i], p1[i]));
			painter.drawLine(p2[i], GetarrowBottom(p2[i], p1[i]));*/
	}
	QVector<QLineF> linelist = findVecLines(CutRect, p1, p2);
	painter.drawLines(linelist);
	auto nImg = img.mirrored(false, true);
	setImage(nImg);
	return true;
}
QVector<QRectF> phasorRenderer::GetRectF_Scene(const Data::Rang xr, const Data::Rang yr){
	QVector<QRectF> scene_Rect;
	qreal x_distance = (xr.max - xr.min) / HORI_GRID;
	qreal y_distance = (yr.max - yr.min) / VERT_GRID;
	for (auto y = 0; y < VERT_GRID;y++)
	{
		for (auto x = 0; x < HORI_GRID;x++)
		{
			QRectF _cutRect;
			_cutRect.setLeft(xr.min+x*x_distance);
			_cutRect.setRight(_cutRect.left()+x_distance);
			_cutRect.setTop(yr.min+y*y_distance);
			_cutRect.setBottom(_cutRect.top()+y_distance);
			scene_Rect.push_back(_cutRect);
		}
	}
	return scene_Rect;
}

bool phasorRenderer::drawImage_Coord(){
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
	//向量可能太小，需要缩放
	for (auto i = 0; i < p1.size(); i++)
	{
		transionVector(p2[i], p1[i], d->GetVecXScale(), d->GetVecYScale());
		transitionpointF(p1[i], xScale, yScale, xr, yr);
		transitionpointF(p2[i], xScale, yScale, xr, yr);
		painter.drawLine(p1[i], p2[i]);
		painter.drawLine(p2[i], GetarrowTop(p2[i], p1[i]));
		painter.drawLine(p2[i], GetarrowBottom(p2[i], p1[i]));
	}
	auto nImg = img.mirrored(false, true);
	setImage(nImg);
	return true;
}
/**
* @brief phasorRenderer::findVecLines 索引出需要绘制的向量
* @param QVector<QRectF> scene_rect 屏幕网格（10*10）
* @param QVector<QPointF> p1 向量起点
* @param QVector<QPointF> p2 向量终点
* @return QVector<QLineF>
*/
QVector<QLineF> phasorRenderer::findVecLines(QVector<QRectF> scene_rect, QVector<QPointF> p1, QVector<QPointF> p2){
	QVector<QLineF> lines;
	for (auto iter = scene_rect.begin(); iter != scene_rect.end();iter++)
	{
		int index = -1;
		qreal Distance_min = sqrt((iter->width())*(iter->width()) + (iter->height())*(iter->height()));
		for (auto indexp1 = 0; indexp1 < p1.size();indexp1++)
		{
			qreal _distance = sqrt((p1[indexp1].x() - iter->left())*(p1[indexp1].x() - iter->left()) + 
				(p1[indexp1].y() - iter->bottom())*(p1[indexp1].y() - iter->bottom()));
			if (Distance_min>_distance && p1[indexp1].x()>=iter->left()&& p1[indexp1].y()>=iter->bottom())
			{
				Distance_min = _distance;
				index = indexp1;
			}
		}
		if (-1!=index)
		{
			//判断是否需要缩放
			lines.push_back(QLineF(p1[index], p2[index]));
			lines.push_back(QLineF(p2[index], GetarrowTop(p2[index], p1[index])));
			lines.push_back(QLineF(p2[index], GetarrowBottom(p2[index], p1[index])));
		}
	}
	return lines;
}