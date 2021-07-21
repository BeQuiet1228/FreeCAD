#include "StructRender.h"
#include <Qpen>
#include <QPainter>
#include "CustomConfig.h"
#include "C_encoding.h"
#include <QDebug>
#include <QPixmap>
void changColorPixmap(QPixmap& map,QColor& color);
QString lineicon[] = { ":/struct/C.png", ":/struct/a.png", ":/struct/s.png" };
/**
* @brief  StructRender::StructRender
* @param  std::shared_ptr<StructData> data  
* @return   
*/
StructRender::StructRender(std::shared_ptr<StructData> data) :Renderer(std::dynamic_pointer_cast<Data>(data)){		
	color_tab[StructData::PERFECTCONDUCTOR] = QColor(125, 125, 125, 255);
	isAA = true;
}
/**
* @brief  StructRender::~StructRender
* @return   
*/
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
* @brief  StructRender::transitionLineF 线段转换
* @param  QLineF & line  
* @param  const float & xScale  
* @param  const float & yScale  
* @param  const Data::Rang & xr  
* @param  const Data::Rang & yr  
* @return void  
*/
void StructRender::transitionLineF(QLineF& line, const float& xScale, const float& yScale, const Data::Rang &xr, const Data::Rang& yr)
{
	QPointF p1 = line.p1();;
	QPointF p2 = line.p2();
	p1.setX(transitionX(p1.x(), xScale, xr));
	p1.setY(transitionY(p1.y(), yScale, yr));
	p2.setX(transitionX(p2.x(), xScale, xr));
	p2.setY(transitionY(p2.y(), yScale, yr));
	line.setP1(p1);
	line.setP2(p2);
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
/**
* @brief StructRender::drawImage 绘制
* @return bool
*/
bool StructRender::drawImage(){
	std::shared_ptr<StructData> d = std::dynamic_pointer_cast<StructData>(data);
	DirectionType _type = d->GetDirectionType();
	switch (_type)
	{
	case X_Y:
	case X_Z:
	case Y_Z:
	case R_Z:
		return drawImageRectspace();
	case R_THETA:
		return drawImageRandspace();
	}
}
/**
* @brief  StructRender::addListRang
* @param  std::list<Data::Rang> listRang  
* @return bool  
*/
bool StructRender::addListRang(std::list<Data::Rang> listRang){
	return true;
}
/**
* @brief StructRender::drawPointImage 取点
* @return bool 
*/
bool StructRender::drawPointImage(){
	std::shared_ptr<StructData> d = std::dynamic_pointer_cast<StructData>(data);
	DirectionType _type = d->GetDirectionType();
	switch (_type)
	{
	case X_Y:
	case X_Z:
	case Y_Z:
	case R_Z:
		return drawPointRect();
	case R_THETA:
		return drawPointCir();
	}
}
/**
* @brief StructRender::setDefaultRang 设置默认刻度区间
* @return bool
*/
bool StructRender::setDefaultRang(){
	auto d = std::dynamic_pointer_cast<StructData>(data);
	if (!d)
		return false;
	if (d->getIsface())
	{
		_3DPointf startPoint = d->getStartPoint();
		_3DPointf endPoint = d->getEndPoint();
		DirectionType _type = d->GetDirectionType();
		Data::Rang xr, yr;
		switch (_type)
		{
		case X_Y:
		{
			xr.min = startPoint._1st;
			xr.max = endPoint._1st;
			yr.min = startPoint._2rd;
			yr.max = endPoint._2rd;
		}
			break;
		case X_Z:
		{
			//Data::Rang xr, yr;
			xr.min = startPoint._1st;
			xr.max = endPoint._1st;
			yr.min = startPoint._3th;
			yr.max = endPoint._3th;
		}
			break;
		case Y_Z:
		{
			xr.min = startPoint._2rd;
			xr.max = endPoint._2rd;
			yr.min = startPoint._3th;
			yr.max = endPoint._3th;
		}
			break;
		case R_Z:
		{
			switch (d->GetC_TYPE())
			{
			case C_TYPE::POLAR:
			{
				xr.min = startPoint._3th;
				xr.max = endPoint._3th;
				yr.min = startPoint._1st;
				yr.max = endPoint._1st;
			}
				break;
			case C_TYPE::CYLINDRICAL:
			{
				xr.min = startPoint._1st;
				xr.max = endPoint._1st;
				yr.min = startPoint._2rd;
				yr.max = endPoint._2rd;
			}
				break;
			}
		}
			break;
		}
		d->setXRang(xr);
		d->setYRang(yr);
	}
	setXRang(d->getXRang());
	setYRang(d->getYRang());
	return true;
}
/**
* @brief StructRender::dataInit 初始化数据
* @return void
*/
void StructRender::dataInit(){
	Renderer::dataInit();
	auto d = std::dynamic_pointer_cast<StructData>(data);
	if (d)
	{
		d->loadPoint();
		d->loadroom();
	}
}
/**
* @brief StructRender::GetPath 获取绘制路径
* @param std::vector<StructData::CutCir>& _vector 圆柱坐标系数据
* @param const Data::Rang& xr 
* @param const Data::Rang& yr
* @param const float& xScale
* @param const float& yScale
* @return QVector<QPainterPath>
*/
QVector<QPainterPath> StructRender::GetPath(std::vector<StructData::CutCir>& _vector, const Data::Rang& xr, const Data::Rang& yr, const float& xScale, const float& yScale)
{
	//qreal pi = 3.141592653589793;
	qreal w1 = 180 / M_PI;
	QPointF p0(0.0, 0.0);
	transitionPoint(p0, xScale, xr, yScale, yr);
	QVector<QPainterPath> pathlist;
	for (auto iterrect = _vector.begin(); iterrect != _vector.end(); iterrect++)
	{
		QPainterPath path;
		transitionPoint(iterrect->inner1, xScale, xr, yScale, yr);
		transitionPoint(iterrect->inner2, xScale, xr, yScale, yr);
		transitionPoint(iterrect->excir1, xScale, xr, yScale, yr);
		transitionPoint(iterrect->excir2, xScale, xr, yScale, yr);
#pragma region 绘制路径
		path.moveTo(iterrect->inner1);
		path.lineTo(iterrect->excir1);
		//外圈矩形
		QRectF excirrect;
		float HR = iterrect->R_excir*xScale;
		float VR = iterrect->R_excir*yScale;
		excirrect.setLeft(p0.x() - HR);
		excirrect.setTop(p0.y() - VR);
		excirrect.setBottom(p0.y() + VR);
		excirrect.setRight(p0.x()+ HR);

		path.arcTo(excirrect, -iterrect->startAngle*w1, -((iterrect->endAngle*w1) - (iterrect->startAngle*w1)));
		path.lineTo(iterrect->inner2);
		HR = iterrect->R_inner*xScale;
		VR = iterrect->R_inner*yScale;
		excirrect.setLeft(p0.x() - HR);
		excirrect.setTop(p0.y() - VR);
		excirrect.setBottom(p0.y() + VR);
		excirrect.setRight(p0.x() + HR);
		path.arcTo(excirrect, -iterrect->endAngle*w1, -((iterrect->startAngle*w1) - (iterrect->endAngle*w1)));
		pathlist.push_back(path);
#pragma  endregion
	}
	return pathlist;
}
/**
* @brief StructRender::drawImageRectspace 绘制-矩形空间
* @return bool
*/
bool StructRender::drawImageRectspace(){
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
	painter.setRenderHint(QPainter::Antialiasing, isAA);
	painter.setPen(pen);
	std::map<int, std::vector<QRectF>> mapInfo = d->GetAllcutInfo();

	for (auto iter = mapInfo.begin(); iter != mapInfo.end(); iter++)
	{
		auto itercolor = color_tab.find(iter->first);
		auto itercolorpen = color_pen.find(iter->first);
		if (itercolor != color_tab.end() && itercolor.value() != Qt::white);
		{
			//进行缩放
			for (auto iterrecct = iter->second.begin(); iterrecct != iter->second.end(); iterrecct++)
				transitionRectF(*iterrecct, xScale, xr, yScale, yr);
			if (itercolorpen!=color_pen.end())
			{
				QPen pen(itercolorpen.value());
				pen.setWidth(1);
				painter.setPen(pen);
			}
			else
			{
				QPen pen(Qt::black);
				pen.setWidth(1);
				painter.setPen(pen);
			}
			QBrush m_brush(itercolor.value());
			painter.setBrush(m_brush);
			painter.drawRects(QVector<QRectF>::fromStdVector(iter->second));
		}
	}
	//绘制线段
	std::map<unsigned __int64, std::vector<QLineF>> mlines = d->GetProperLines();
	for (auto iter=mlines.begin();iter!=mlines.end();iter++)
	{
		//查找当前属性是否有对应颜色
		auto itercolor=pixmap.find(iter->first);
		if (itercolor!=pixmap.end())
		{
			for (auto iterline = iter->second.begin(); iterline != iter->second.end();iterline++)
			{
				transitionLineF(*iterline, xScale, yScale, xr, yr);
				QLine line = QLine(QPoint(iterline->p1().x(), iterline->p1().y()), QPoint(iterline->p2().x(), iterline->p2().y()));
				QLineF linef = *iterline;
			}
			QVector<QLineF> lines = QVector<QLineF>::fromStdVector(iter->second);
			DrawLine(painter, lines, iter->first);
		}
	}
	auto nImg = img.mirrored(false, true);
#ifdef MY_DEBUG
	//测试打印出全部属性
	QStringList msg;
	for (auto iter = mapInfo.begin(); iter != mapInfo.end(); iter++)
	{
		msg << QString::number(iter->first,10);
	}
	for (auto iter = mlines.begin(); iter != mlines.end();iter++)
	{
		msg << QString::number(iter->first,10);
	}
	qDebug() << "getAllProperty:" << msg;
#endif // MY_DEBUG
	setImage(nImg);
	return true;
}
/**
* @brief StructRender::drawImageRandspace 绘制-扇形空间
* @return bool
*/
bool StructRender::drawImageRandspace(){
	float yScale(0.0), xScale(0.0);
	if (!getTransitionScale(xScale, yScale))
		return false;
	std::shared_ptr<StructData> d = std::dynamic_pointer_cast<StructData>(data);
	//获取起始点,因为图表的刻度不一定是从零开始的。
	auto xr = getXRang();
	auto yr = getYRang();
	QImage img(getSize(), QImage::Format_ARGB32);
	img.fill(qRgba(0, 0, 0, 0));
	QPen pen(Qt::black);
	pen.setWidth(1);
	QPainter painter(&img);
	painter.setRenderHint(QPainter::Antialiasing, isAA);;
	painter.setPen(pen);
	//绘制圆柱
	std::map<int, std::vector<StructData::CutCir>> _map = d->GetAllcurInfo_cir();
	for (auto iter = _map.begin(); iter != _map.end(); iter++)
	{
		auto itercolor = color_tab.find(iter->first);
		auto itercolorpen = color_pen.find(iter->first);
		if (itercolor != color_tab.end()&&itercolor.value()!=Qt::white)
		{
			if (itercolorpen!=color_pen.end())
			{
				QPen pen(itercolorpen.value());
				pen.setWidth(1);
				painter.setPen(pen);
			}
			else
			{
				QPen pen(Qt::black);
				pen.setWidth(1);
				painter.setPen(pen);
			}
			QBrush m_brush(itercolor.value());
			painter.setBrush(m_brush);
			QVector<QPainterPath> _path = GetPath(iter->second, xr, yr, xScale, yScale);
			for (auto iterpath = _path.begin(); iterpath != _path.end(); iterpath++)
				painter.drawPath(*iterpath);
		}
	}
	auto nImg = img.mirrored(false, true);
	//auto nImg = img;
//#define _Debug
#ifdef _Debug
	static int index = 0;
	QString _path = QString("C:/Users/ASUS/Desktop/save/savepmg_%1.png").arg(index++);
	bool res = nImg.save(_path);
#undef _Debug
#endif
	setImage(nImg);
	return true;
}
/**
* @brief StructRender::findApointZr 查找最近的点-ZR方向
* @return StructData::structpoint
*/
StructData::structpoint StructRender::findApointZr(QPointF _curpostion){
	StructData::structpoint mpoint;
	//获取屏幕与数据的比例
	float xScale, yScale;
	getTransitionScale(xScale, yScale);
	auto xr = getXRang();
	auto yr = getYRang();
	//区域中的点
	std::list<StructData::structpoint> _point;
	//获取所有的点
	/******************************/
	std::shared_ptr<StructData> d = std::dynamic_pointer_cast<StructData>(data);
	//开始绘制图表
	//获取真实的数据
	std::vector<QRectF> conduitList = d->GetAllcutInfo()[3];
	//添加所有属性
	auto func = [&](StructData::structType structtexture){
		std::vector<QRectF> tempList = d->GetAllcutInfo()[structtexture];
		if (!tempList.empty())
		{
			conduitList.insert(conduitList.end(),tempList.begin(),tempList.end());
		}
	};
	func(StructData::PERFECTCONDUCTOR);
	func(StructData::CONDUCTORNEW);
	func(StructData::DIOLECTRIC);
	func(StructData::DIELECTIRANDCONDUCTANCE);
	func(StructData::PERMEABILITY);
	func(StructData::FREESPACE);
	func(StructData::FOIL);
	//获取矩形中心点
	std::vector<QPointF> scaleCoord;
	for (auto iter = conduitList.begin(); iter != conduitList.end(); iter++)
	{
		//获取缩放
		QPointF _centerpoint = iter->center();
		_centerpoint.setX(transitionX(_centerpoint.x(), xScale, xr));
		_centerpoint.setY(transitionY(_centerpoint.y(), yScale, yr));
		scaleCoord.push_back(_centerpoint);
	}
	unsigned int index = 0;
	float distance = 10000.0f;
	for (unsigned int i = 0; i < scaleCoord.size(); i++)
	{
		float _distance = GetDistance(_curpostion, scaleCoord[i]);

		if (distance > _distance)
		{
			distance = _distance;
			index = i;
		}
	}
	//获取到最近的中心点
	QRectF rectf = conduitList[index];
	QRectF recfCoord = rectf;
	transitionRectF(recfCoord, xScale, xr, yScale, yr);
	//获取接近的x坐标
	if (abs(_curpostion.x() - recfCoord.left()) >= abs(_curpostion.x() - recfCoord.right()))
	{
		mpoint.x = recfCoord.right();
		mpoint.d1 = conduitList[index].right();
	}
	else
	{
		mpoint.x = recfCoord.left();
		mpoint.d1
			= conduitList[index].left();
	}
	if ((abs(_curpostion.y() - recfCoord.top())) >= (abs(_curpostion.y() - recfCoord.bottom())))
	{
		mpoint.y = recfCoord.bottom();
		mpoint.d2 = conduitList[index].bottom();
	}
	else
	{
		mpoint.y = recfCoord.top();
		mpoint.d2 = conduitList[index].top();
	}
	//获取线段的点位
	auto  lines = d->GetProperLines();
	std::vector<QPointF> linePointf;
	for (auto itermap = lines.begin(); itermap != lines.end();itermap++)
	{
		for (auto iterline = itermap->second.begin(); iterline != itermap->second.end();iterline++)
		{
			linePointf.push_back(iterline->p1());
			linePointf.push_back(iterline->p2());
		}
	}
	std::vector<QPointF> linescalePointf;
	linescalePointf.insert(linescalePointf.end(), linePointf.begin(), linePointf.end());
	float ldistance=10000.0f;
	float lindex = 0;
	for (int index = 0; index < linescalePointf.size();index++)
	{
		transitionPoint(linescalePointf[index],xScale,xr,yScale,yr);
		float lcurdistance = GetDistance(_curpostion, linescalePointf[index]);
		if (ldistance>lcurdistance)
		{
			ldistance = lcurdistance;
			lindex = index;
		}
	}
	QPointF rectPointf(mpoint.x,mpoint.y);
	distance = GetDistance(rectPointf, _curpostion);
	if (distance>ldistance)
	{
		mpoint.x = linescalePointf[lindex].x();
		mpoint.y = linescalePointf[lindex].y();
		mpoint.d1 = linePointf[lindex].x();
		mpoint.d2 = linePointf[lindex].y();
	}
	return mpoint;
}
/**
* @brief StructRender::GetDistance 获取距离
* @param QPointF p1
* @param QPointF p2
* @return float
*/
float StructRender::GetDistance(QPointF p1, QPointF p2)
{
	float distance;
	distance = ((p1.x() - p2.x())*(p1.x() - p2.x())) +
		((p1.y() - p2.y())*(p1.y() - p2.y()));
	return sqrt(distance);

}
/**
* @brief StructRender::drawPointRect 绘制点位-矩形
* @return bool
*/
bool StructRender::drawPointRect(){
	QImage img(getSize(), QImage::Format_ARGB32);
	img.fill(qRgba(0, 0, 0, 0));
	QPen pen(Qt::red);
	pen.setBrush(Qt::blue);
	pen.setWidth(5);
	QPainter painter(&img);
	painter.setPen(pen);
	QPointF A_pos;//原始坐标
	//获取当前点位
	StructData::structpoint _point = findApointZr(this->getFindPosition());
	//坐标翻转
	_point.y = getSize().height() - _point.y;
	painter.drawPoint(QPointF(_point.x, _point.y));
	std::map<QString, float> list;
	list["X"] = _point.d1;
	list["Y"] = _point.d2;
	displayPointInformation(&painter, &QPointF(_point.x, _point.y), list);
	setImage(img);
	return true;
}
/**
* @brief StructRender::drawPointCir 绘制点位-圆
*/
bool StructRender::drawPointCir(){
	//新建画布 画笔
	QImage img(getSize(), QImage::Format_ARGB32);
	//填充透明画布
	img.fill(qRgba(0, 0, 0, 0));
	QPen pen(Qt::red);
	pen.setBrush(Qt::blue);
	pen.setWidth(5);
	QPainter painter(&img);
	painter.setPen(pen);
	//获取当前点位
	QPointF A_Point = this->getFindPosition();
	//A_Point.setY(getSize().height()-A_Point.y());
	StructData::structpoint _point = findApointCylindrical(A_Point);
	//坐标翻转
	_point.y = getSize().height() - _point.y;
	painter.drawPoint(QPointF(_point.x, _point.y));
	std::map<QString, float> list;
	list["R"] = _point.d1;
	list["THETA"] = _point.d2;
	displayPointInformation(&painter, &QPointF(_point.x, _point.y), list);
	setImage(img);
	return true;
}
/**
* @brief StructRender::findApointCylindrical 查找最近的点-cylindrical坐标系
* @return StructData::structpoint
*/
StructData::structpoint StructRender::findApointCylindrical(QPointF _curpoint)
{
	StructData::structpoint mpoint;
	//获取屏幕的缩放比例
	float xScale, yScale;
	getTransitionScale(xScale, yScale);
	auto xr = getXRang();
	auto yr = getYRang();
	/*********************************/
	//获取所有的点，只能一个一个对比
	std::shared_ptr<StructData> d = std::dynamic_pointer_cast<StructData>(data);
	//获取起始点,因为图表的刻度不一定是从零开始的。
	std::map<int, std::vector<StructData::CutCir>> map = d->GetAllcurInfo_cir();
	QVector<QPointF> pointlist;
	//查找方式还待优化
	int key, index, pointype;
	unsigned int _mindistance = ~0;
	for (auto iter = color_tab.begin(); iter != color_tab.end(); iter++)
	{
		auto iterp = map.find(iter.key());
		if (iterp != map.end())
		{
			for (auto _index = 0; _index < map[iter.key()].size(); _index++)
			{
				transitionPoint(map[iter.key()][_index].inner1, xScale, xr, yScale, yr);
				QPointF inner1 = map[iter.key()][_index].inner1;
				transitionPoint(map[iter.key()][_index].inner2, xScale, xr, yScale, yr);
				QPointF inner2 = map[iter.key()][_index].inner2;
				transitionPoint(map[iter.key()][_index].excir1, xScale, xr, yScale, yr);
				QPointF excir1 = map[iter.key()][_index].excir1;
				transitionPoint(map[iter.key()][_index].excir2, xScale, xr, yScale, yr);
				QPointF excir2 = map[iter.key()][_index].excir2;
				unsigned int distance_inner1 = sqrt((inner1.x() - _curpoint.x())*(inner1.x() - _curpoint.x()) + (inner1.y() - _curpoint.y())*(inner1.y() - _curpoint.y()));
				unsigned int distance_inner2 = sqrt((inner2.x() - _curpoint.x())*(inner2.x() - _curpoint.x()) + (inner2.y() - _curpoint.y())*(inner2.y() - _curpoint.y()));
				unsigned int distance_excir1 = sqrt((excir1.x() - _curpoint.x())*(excir1.x() - _curpoint.x()) + (excir1.y() - _curpoint.y())*(excir1.y() - _curpoint.y()));
				unsigned int distance_excir2 = sqrt((excir2.x() - _curpoint.x())*(excir2.x() - _curpoint.x()) + (excir2.y() - _curpoint.y())*(excir2.y() - _curpoint.y()));
				//比较距离
				if (_mindistance > distance_inner1)
				{
					_mindistance = distance_inner1;
					key = iter.key();
					index = _index;
					pointype = 0;
				}
				if (_mindistance > distance_inner2)
				{
					_mindistance = distance_inner2;
					key = iter.key();
					index = _index;
					pointype = 1;
				}
				if (_mindistance > distance_excir1)
				{
					_mindistance = distance_excir1;
					key = iter.key();
					index = _index;
					pointype = 2;
				}
				if (_mindistance > distance_excir2)
				{
					_mindistance = distance_excir2;
					key = iter.key();
					index = _index;
					pointype = 3;
				}
			}
		}
	}
	//找到最近的点
	std::map<int, std::vector<StructData::CutCir>> __map = d->GetAllcurInfo_cir();
	QPointF dp;
	switch (pointype)
	{
	case 0:
	{
		mpoint.x = map[key][index].inner1.x();
		mpoint.y = map[key][index].inner1.y();
		//mpoint.d1 = __map[key][index].inner1.x();
		//mpoint.d2 = __map[key][index].inner1.y();
		mpoint.d1 = __map[key][index].R_inner;
		mpoint.d1 = __map[key][index].startAngle;
	}
		break;
	case 1:
	{
		mpoint.x = map[key][index].inner2.x();
		mpoint.y = map[key][index].inner2.y();
		//mpoint.d1 = __map[key][index].inner2.x();
		//mpoint.d2 = __map[key][index].inner2.y();
		mpoint.d1 = __map[key][index].R_inner;
		mpoint.d2 = __map[key][index].endAngle;
	}
		break;
	case 2:
	{
		mpoint.x = map[key][index].excir1.x();
		mpoint.y = map[key][index].excir1.y();
		//mpoint.d1 = __map[key][index].excir1.x();
		//mpoint.d2 = __map[key][index].excir1.y();
		mpoint.d1 = __map[key][index].R_excir;
		mpoint.d2 = __map[key][index].startAngle;
	}
		break;
	case 3:
	{
		mpoint.x = map[key][index].excir2.x();
		mpoint.y = map[key][index].excir2.y();
		//mpoint.d1 = __map[key][index].excir2.x();
		//mpoint.d2 = __map[key][index].excir2.y();
		mpoint.d1 = __map[key][index].R_excir;
		mpoint.d2 = __map[key][index].endAngle;
	}
		break;
	}
	return mpoint;
}
/**
* @brief  StructRender::loadconfig 读取配置
* @return void  
*/
void StructRender::loadconfig()
{
	Config::GetInstance()->loadConfig();
	ConfigGroup mGroup = Config::GetInstance()->getRootGroup();
	ConfigGroup structConfig = mGroup.getGroup("struct");
#define LoadColor(a)\
	color_tab[(a)] = QStringToQColor(QString::fromStdString(structConfig.getGroup(#a+12).getValue("value")));\
	color_pen[(a)] = QStringToQColor(QString::fromStdString(structConfig.getGroup(#a "LINE"+12).getValue("value")));
	LoadColor(StructData::PERFECTCONDUCTOR);
	LoadColor(StructData::CONDUCTORNEW);
	LoadColor(StructData::DIOLECTRIC);
	LoadColor(StructData::PERMEABILITY);
	LoadColor(StructData::DIELECTIRANDCONDUCTANCE);
	LoadColor(StructData::FREESPACE);
	LoadColor(StructData::FOIL);
	//线段
	//PORT 2**8/256，2**9/512，2**10/1024
	//DRIVER--2^11/2048,2^12/4096,2^13/8192
	//INDUCTOR--2^14/16384,2^15/32768,2^16/65536
	QPixmap mapc(lineicon[0]);
	QPixmap mapa(lineicon[1]);
	QPixmap maps(lineicon[2]);
	QSize pngsize(16, 16);
	changColorPixmap(maps, QStringToQColor(QString::fromStdString(structConfig.getGroup("PORT").getValue("value"))));
	changColorPixmap(mapa, QStringToQColor(QString::fromStdString(structConfig.getGroup("DRIVER").getValue("value"))));
	changColorPixmap(mapc, QStringToQColor(QString::fromStdString(structConfig.getGroup("INDUCTOR").getValue("value"))));
	mapc = mapc.scaled(pngsize, Qt::KeepAspectRatio, Qt::SmoothTransformation);
	mapa = mapa.scaled(pngsize, Qt::KeepAspectRatio, Qt::SmoothTransformation);
	maps = maps.scaled(pngsize, Qt::KeepAspectRatio, Qt::SmoothTransformation);
	QMatrix rm;
	rm.rotate(180);
	mapc = mapc.transformed(QPixmap::trueMatrix(rm,pngsize.width(),pngsize.height()));
	mapa = mapa.transformed(QPixmap::trueMatrix(rm, pngsize.width(), pngsize.height()));
	maps = maps.transformed(QPixmap::trueMatrix(rm, pngsize.width(), pngsize.height()));
	pixmap[256] = pixmap[512]=pixmap[1024]=maps;
	pixmap[2048] = pixmap[4096] = pixmap[8192] = mapa;
	pixmap[16384] = pixmap[32768] = pixmap[65536] = mapc;
#undef LoadColor(a)
	isAA = atoi(structConfig.getValue("isAlis").c_str());
}
/**
* @brief  StructRender::setDefaultRang 设置默认坐标取值范围
* @param  QSize & size  
* @return bool  
*/
bool StructRender::setDefaultRang(QSize& size){
	std::shared_ptr<StructData> d = std::dynamic_pointer_cast<StructData>(data);
	DirectionType _type = d->GetDirectionType();
	switch (_type)
	{
	case R_THETA:
	{
		auto xr=d->getXRang();
		auto yr=d->getYRang();
		float scale_x = (float)size.width() / (float)size.height();
		float xwidth = (xr.max - xr.min)*scale_x;
		xr.min = -xwidth / 2;
		xr.max = xwidth / 2;
		setXRang(xr);
		setYRang(yr);
		return true;
	}
		break;
	default:
	{
		return setDefaultRang();
	}
		break;
	}
	
}
/**
* @brief  StructRender::DrawLine 绘制线段
* @param  QPainter & painter  
* @param  QVector<QLineF> & lines  
* @param  int mPorper  
* @return void  
*/
void StructRender::DrawLine(QPainter& painter, QVector<QLineF>& lines, int mPorper)
{
	QSize pngSize = pixmap[mPorper].size();
	for (auto iter = lines.begin(); iter != lines.end();iter++)
	{
		QPointF p1 = iter->p1();
		QPointF p2 = iter->p2();
		//纵向
		if (p1.x()==p2.x())
		{
			auto intervalnumber = abs(p1.y() - p2.y()) / pixmap[mPorper].size().height();
			auto startpos = (p1.y() > p2.y()) ? (p2.y()) : (p1.y());
			auto endpos = (p1.y() > p2.y()) ? (p1.y()) : (p2.y());
			for (auto index = 0; index < intervalnumber;index++)
			{
				QRect rect;
				rect.setLeft(p1.x() - pngSize.width() / 2);
				rect.setRight(rect.left() + pngSize.width());
				rect.setTop(startpos+index*pngSize.height());
				if (rect.top() + pngSize.height() >= endpos)
				{
					rect.setBottom(endpos);
					QPixmap map = pixmap[mPorper].copy(0,0,pngSize.width(),endpos-rect.top());
					painter.drawPixmap(rect,map);
				}
				else
				{
					rect.setBottom(rect.top() + pngSize.height());
					painter.drawPixmap(rect, pixmap[mPorper]);
				}
				
			}
		}
		//横向
		else if (p1.y()==p2.y())
		{
			auto intervalnumber = abs(p1.x() - p2.x()) / pixmap[mPorper].size().width();
			auto startpos = (p1.x() > p2.x()) ? (p2.x()) : (p1.x());
			auto endpos = (p1.x() > p2.x()) ? (p1.x()) : (p2.x());
			//图像翻转
			QMatrix rm;
			rm.rotate(90);
			QPixmap mapy = pixmap[mPorper].transformed(QPixmap::trueMatrix(rm, pngSize.width(), pngSize.height()));
			for (auto index = 0; index < intervalnumber; index++)
			{
				QRect rect;
				rect.setTop(p1.y()-pngSize.height()/2);
				rect.setBottom(rect.top() + pngSize.height());
				rect.setLeft(startpos+index*pngSize.width());
				if (rect.left() + pngSize.width() >= endpos)
				{
					rect.setRight(endpos);
					QPixmap map = mapy.copy(0, 0, endpos - rect.left(), rect.height());
					painter.drawPixmap(rect,map);
				}
				else
				{
					rect.setRight(rect.left() + pngSize.width());
					painter.drawPixmap(rect, mapy);
				}
				
			}
		}
	}
}
/**
* @brief  changColorPixmap
* @param  QPixmap & map  
* @return void  
*/
void changColorPixmap(QPixmap& map, QColor& color)
{
	//默认为红色
	QImage img = map.toImage();
	QColor colorred = QStringToQColor("ffdc3023");
	for (auto w = 0; w < img.width();w++)
	{
		for (auto h = 0; h < img.height();h++)
		{
			//qDebug() << QString::number(img.pixel(w, h), 16);
			if (img.pixel(w,h)==colorred.rgb())
			{
				img.setPixel(w, h, color.rgba());
			}
		}
	}
	map = QPixmap::fromImage(img);
}


