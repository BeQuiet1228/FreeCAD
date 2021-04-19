#include "StructRender.h"
#include <Qpen>
#include <QPainter>
StructRender::StructRender(std::shared_ptr<StructData> data) :Renderer(std::dynamic_pointer_cast<Data>(data)){		
	color_tab[StructTexture::Perfect_Conductor] = QColor(125, 125, 125, 255);
}
StructRender::~StructRender(){

}

/**
* @brief StructRender::transitionX 坐标值转换
* @param const float & x
* @param const float & xScale  缩放比例
* @param const Data::Rang & xr 渲染范围
* @return float
*/
float StructRender::transitionX(const float& x, const float& xScale, const Data::Rang& xr)
{
	return (x - xr.min)*xScale;
}

/**
* @brief StructRender::transitionY 坐标值转转
* @param const float & y
* @param const float & yScale 缩放比例
* @param const Data::Rang & yr 渲染范围
* @return float
*/
float StructRender::transitionY(const float& y, const float& yScale, const Data::Rang& yr)
{
	return (y - yr.min)*yScale;
}

/**
* @brief StructRender::transitionRectF 切割空间的坐标转换
* @param QRectF& _rect
* @param const float& xScale
* @param const Data::Rang& xr
* @param const float& yScale
* @param Data::Rang& yr
* @return void
*/
void StructRender::transitionRectF(QRectF& _rectf, const float& xScale, const Data::Rang& xr, const float& yScale, Data::Rang& yr)
{
	_rectf.setLeft(transitionX(_rectf.left(), xScale, xr));
	_rectf.setRight(transitionX(_rectf.right(), xScale, xr));
	_rectf.setTop(transitionY(_rectf.top(), yScale, yr));
	_rectf.setBottom(transitionY(_rectf.bottom(), yScale, yr));
}

/**
* @brief TimeRenderer::getTransitionScale 初始化数据与图片坐标的缩放比例
* @param float & xScale
* @param float & yScale
* @return bool
*/
bool StructRender::getTransitionScale(float& xScale, float& yScale)
{
	auto size = getSize();
	auto xr = getXRang();
	auto yr = getYRang();

	float xLength = xr.max - xr.min;
	float yLength = yr.max - yr.min;

	if (xLength < 0 || yLength < 0)
	{
#if MY_DEBUG
		std::cerr << "StructRenderer::getTransitionScale length < 0" << std::endl;
#endif
		return false;
	}

	if (size.width() <= 0 || size.height() <= 0)
	{
#if MY_DEBUG
		std::cerr << "StructRenderer::getTransitionScale size <= 0" << std::endl;
#endif
		return false;
	}
	xScale = size.width() / xLength;
	yScale = size.height() / yLength;
	return true;
}

/**
* @brief StructRender::transitionPoint 转换坐标
* @param QPointF& point
* @param const float& xScale
* @param const Data::Rang& xr
* @param const float& yScale
* @param const Data::Rang& yr
* @return void
*/
void StructRender::transitionPoint(QPointF& point, const float& xScale, const Data::Rang& xr, const float& yScale, const Data::Rang& yr)
{
	point.setX(transitionX(point.x(), xScale, xr));
	point.setY(transitionY(point.y(), yScale, yr));
}

bool StructRender::drawImage(){
	std::shared_ptr<StructData> d = std::dynamic_pointer_cast<StructData>(data);
	C_TYPE ctype = d->GetC_TYPE();
	switch (ctype)
	{
	case POLAR:
		return drawImage_polar();
	case CYLINDRICAL:
		return drawImage_cylindrical();
	case CARTESIAN:
		return drawImage_cartesian();
	}
}
bool StructRender::addListRang(std::list<Data::Rang> listRang){
	return true;
}
bool StructRender::drawPointImage(){
	return true;
}
bool StructRender::setDefaultRang(){
	auto d = std::dynamic_pointer_cast<StructData>(data);
	if (!d)
		return false;
	setXRang(d->getXRang());
	setYRang(d->getYRang());
	return true;
}
void StructRender::dataInit(){
	Renderer::dataInit();
	auto d = std::dynamic_pointer_cast<StructData>(data);
	if (d)
	{
		d->loadPoint();
		d->loadroom();
	}
}

bool StructRender::drawImage_polar()
{
	std::shared_ptr<StructData> d = std::dynamic_pointer_cast<StructData>(data);
	DirectionType _type = d->GetDirectionType();
	switch (_type)
	{
	case R_Z:
		return drawImage_polar_r_z();
	case R_THETA:
		return drawImage_polar_r_theta();
	}
}
bool StructRender::drawImage_cylindrical()
{
	return true;
}
bool StructRender::drawImage_cartesian()
{
	return true;
}

bool StructRender::drawImage_polar_r_z(){
	float yScale(0.0), xScale(0.0);
	if (!getTransitionScale(xScale, yScale))
		return false;
	std::shared_ptr<StructData> d = std::dynamic_pointer_cast<StructData>(data);
	//获取起始点,因为图表的刻度不一定是从零开始的。
	auto xr = getXRang();
	auto yr = getYRang();
	//开始绘制
	//新建画布 画笔
	QImage img(getSize(), QImage::Format_ARGB32);
	img.fill(qRgba(0, 0, 0, 0));
	QPen pen(Qt::black);
	pen.setWidth(1);
	QPainter painter(&img);
	painter.setRenderHint(QPainter::Antialiasing, true);;
	painter.setPen(pen);
	QMap<int, QVector<QRectF>> _map = d->GetAllKMTInfo();
	for (auto iter = _map.begin(); iter != _map.end(); iter++)
	{
		auto itercolor = color_tab.find(iter.key());
		if (itercolor != color_tab.end())
		{
			//进行缩放
			for (auto iterrecct = iter.value().begin(); iterrecct != iter.value().end(); iterrecct++)
				transitionRectF(*iterrecct, xScale, xr, yScale, yr);
			QBrush m_brush(itercolor.value());
			painter.setBrush(m_brush);
			painter.drawRects(iter.value());
		}
	}
	auto nImg = img.mirrored(false, true);
#define _Debug
#ifdef _Debug
	static int index = 0;
	QString _path = QString("C:/Users/Administrator/Desktop/save/savepmg_%1.png").arg(index++);
	bool res = nImg.save(_path);
#undef _Debug
#endif
	setImage(nImg);
	return true;
}
bool StructRender::drawImage_polar_r_theta(){
	return true;
}