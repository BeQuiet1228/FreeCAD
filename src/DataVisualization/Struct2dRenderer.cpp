#include "Struct2dRenderer.h"
#include <qpen.h>
#include <QPainter>
#include "CustomConfig.h"
#include "C_encoding.h"
#include "StructRender.h"
#include <QDebug>
Struct2DRenderer::Struct2DRenderer(std::shared_ptr<Struct2dData> data):
Renderer(std::dynamic_pointer_cast<Data> (data)){

	color_tab[1]=QColor(125,125,125,255);
	color_tab[3]=QColor(255,0,255,0);
	color_tab[4]=QColor(255,125,125,255);
	color_tab[5]=QColor(125,125,255,255);
	color_tab[9]=QColor(255,255,0,255);
	QPen pen(Qt::red);
	//虚线
	pen.setStyle(Qt::DashLine);
	pen.setWidth(5);
	pen_tab[1] = pen;
	pen_tab[3] = pen;
	pen_tab[4] = pen;
	pen_tab[5] = pen;
	pen_tab[9] = pen;

}
Struct2DRenderer::~Struct2DRenderer(){  }
/**
* @brief Struct2DRenderer::drawImage()
* @return bool 
*/
bool Struct2DRenderer::drawImage() {
	//return drawPloy();
	return getPloy_grid();
}
/**
* @brief Struct2DRenderer::addListRang 
* @param std::list<Data::Rang> listRang
* @return bool
*/
bool Struct2DRenderer::addListRang(std::list<Data::Rang> listRang){
	return true;
}
/**
* @brief Struct2DRenderer::drawPointImage 点位绘制
* @return bool
*/
bool Struct2DRenderer::drawPointImage(){
	//新建画布

	QImage img(getSize(),QImage::Format_ARGB32);
	img.fill(qRgba(0, 0, 0, 0));
	QPen pen(Qt::red);
	pen.setBrush(Qt::blue);
	pen.setWidth(5);
	QPainter painter(&img);
	painter.setPen(pen);
	//原始坐标
	QPointF A_pos=this->getFindPosition();
	QPointF d_pos=QPointF(0.0,0.0);
	//获取当前点位
	/**************************/
	d_pos=GetA_pos(A_pos);
	/***************************/
	A_pos.setY(getSize().height()-A_pos.y());
	painter.drawPoint(A_pos);
	drawDisplayPoint(painter,A_pos,d_pos);
	setImage(img);
	return true;
}
/**
* @brief Struct2DRenderer::setDefaultRang 设置默认数据区间
* @return bool
*/
bool Struct2DRenderer::setDefaultRang(){
	auto _Struct2DData = std::dynamic_pointer_cast<Struct2dData>(data);
	if (!_Struct2DData)
		return false;
	setXRang(_Struct2DData->getXRang());
	setYRang(_Struct2DData->getYRang());
	return true;
}
/**
* @brief Struct2DRenderer::dataInit 数值初始化
* return void
*/
void Struct2DRenderer::dataInit(){
	Renderer::dataInit();
	auto _Struct2DData = std::dynamic_pointer_cast<Struct2dData>(data);
	if (_Struct2DData)
	{
		_Struct2DData->loadPoint();
	}
}
/**
* @brief Struct2DRenderer::Getlines 获取线段
* @param std::vector<QPointF> points
* @return QVector<QLineF>
*/
QVector<QLineF> Struct2DRenderer::Getlines(std::vector<QPointF> points){
	QVector<QLineF> lines;
	/*int index = 0;
	while (index<points.size())
	{
		for (auto i = 0; i < points.size();i++)
		{
			if (index==i)
				continue;
			if (points[index].x()==points[i].x()||points[index].y()==points[i].y())
			{
				lines.push_back(QLineF(points[index], points[i]));
			}
		}
		index++;
	}*/
	for (auto i = 0; i < points.size()-1;i++)
	{
		lines.push_back(QLineF(points[i], points[i + 1]));
	}
	return lines;
}
/**
* @brief Struct2DRenderer::drawDisplayPoint 绘制显示信息
* @param QPainter& painter
* @param const QPointF& position
* @param const QPointF& d
* @return void
*/
void Struct2DRenderer::drawDisplayPoint(QPainter& painter, const QPointF& position, const QPointF& d)
{
	//设置画笔的颜色
	QPen pen;
	pen.setColor(QColor(102, 205, 170));
	pen.setWidth(2);
	painter.setPen(pen);
	painter.setBrush(QBrush(QColor(255, 250, 240)));
	//建立话画框
	QRectF displayRect;
	displayRect.setX(position.x() + 10);
	displayRect.setY(position.y() - 5);
	//如果这个点在边界上  那么调整话框的位置
	auto size = getSize();
	if (displayRect.y() > (size.height() - 60))
	{
		displayRect.setY(displayRect.y() - 70);
	}
	if (displayRect.x() > (size.width() - 130))
	{
		displayRect.setX(displayRect.x() - 150);
	}
	displayRect.setWidth(110);
	displayRect.setHeight(50);
	painter.drawRect(displayRect);
	//绘制显示信息
	QFont f;
	f.setPixelSize(17);
	painter.setFont(f);
	painter.drawText(displayRect.x() + 10,
		displayRect.y() + 20,
		QString("X:%1").arg(d.x(), 0, 'E', 2)
		);
	painter.drawText(displayRect.x() + 10,
		displayRect.y() + 40,
		QString("Y:%1").arg(d.y(), 0, 'E', 2)
		);
}
/**
* @brief Struct2DRenderer::GetA_pos 获取最接近的点
* @param QPointF& A_pos 屏幕上的点
* @return QPointF 真实坐标
*/
QPointF Struct2DRenderer::GetA_pos(QPointF& A_pos)
{
	float xScale, yScale;
	getTransitionScale(xScale, yScale);
	auto xr = getXRang();
	auto yr = getYRang();
	std::shared_ptr<Struct2dData> d = std::dynamic_pointer_cast<Struct2dData> (data);
	std::map<int, std::map<int, std::vector<QPointF>>> map = d->GetAllinfo();
	int data1=0, data2=0, data3=0;
	unsigned int minDistance = ~0;
	for (auto iter1 = map.begin(); iter1 != map.end();iter1++)
	{
		for (auto iter2 = iter1->second.begin(); iter2 != iter1->second.end();iter2++)
		{
			for (auto index3 = 0; index3 < iter2->second.size();index3++)
			{
				QPointF p1 = iter2->second[index3];
				transitionPoint(p1, xScale, xr, yScale, yr);
				unsigned int Cur_Distance = sqrt((p1.x() - A_pos.x())*(p1.x() - A_pos.x()) + (p1.y() - A_pos.y())*(p1.y() - A_pos.y()));
				if (minDistance>Cur_Distance)
				{
					data1 = iter1->first;
					data2 = iter2->first;
					data3 = index3;
					minDistance = Cur_Distance;
				}
			}
		}
	}
	//获取最小的点
	QPointF dpos = map[data1][data2][data3];
	QPointF apos = dpos;
	transitionPoint(apos, xScale, xr, yScale, yr);
	A_pos = apos;
	return dpos;
}
/**
* @brief Struct2DRenderer::SetColor 设置不同多边形的颜色
* @param int pro 多边形属性
* @param QColor _color 颜色
* @return void
*/
void Struct2DRenderer::SetColor(int pro, QColor _color)
{
	color_tab[pro] = _color;
}
/**
* @brief Struct2DRenderer::SetPen 设置直线情况下的画笔风格
* @param int pro 直线的属性
* @param QPen pen 画笔
* @return void
*/
void Struct2DRenderer::SetPen(int pro, QPen pen)
{
	pen_tab[pro] = pen;
}
/**
* @brief Struct2DRenderer::getPloy_grid 获取多边形的网格
* @return void
*/
bool Struct2DRenderer::getPloy_grid(){
	float xScale, yScale;
	if (!getTransitionScale(xScale, yScale))
		return false;
	std::shared_ptr<Struct2dData> d = std::dynamic_pointer_cast<Struct2dData>(data);
	//获取x,y的取值范围
	auto xr = getXRang();
	auto yr = getYRang();
	//开始绘制
	QImage img1(getSize(), QImage::Format_ARGB32);
	img1.fill(qRgba(255,255,255,255));
	QPen pen(Qt::black);
	pen.setWidth(1);
	QPainter painter1(&img1);
	painter1.setPen(pen);
	std::vector<QPointF> allpos = d->ALLPOINTF();
	int XSize = d->getposxSize();
	int YSize = d->getposySize();
	//绘制第二张图
	QImage img2(getSize(), QImage::Format_ARGB32);
	img2.fill(qRgba(255, 255, 255, 255));
	QPainter painter2(&img2);
	painter2.setCompositionMode(QPainter::CompositionMode_DestinationIn);
	std::map<int, std::map<int, std::vector<QPointF>>> map = d->GetAllinfo();
	QVector<QVector<QLineF>> lines_list;
	QVector<linepen> linepenlist;
	for (auto iter = map.begin(); iter != map.end(); iter++)
	{
		auto itercolor = color_tab.find(iter->first);
		if (itercolor != color_tab.end())
		{
			QBrush brush(itercolor.value());
			painter1.setBrush(brush);
			painter2.setBrush(brush);//设置画刷
			for (auto iterlines = iter->second.begin(); iterlines != iter->second.end(); iterlines++)
			{
				if (iterlines->second.size() == 2)
				{
					linepen _linepen;
					auto linestyle = pen_tab.find(iter->first);
					if (linestyle != pen_tab.end())
					{
						_linepen.pen= linestyle.value();
						auto iterpoint = (*iterlines).second.begin();
						transitionPoint(*iterpoint, xScale, xr, yScale, yr);
						transitionPoint(*(iterpoint + 1), xScale, xr, yScale, yr);
						_linepen.line = QLineF((*iterpoint), *(iterpoint + 1));
						linepenlist.push_back(_linepen);
					}
				}
				if (iterlines->second.size()>2)
				{
					QPainterPath _path;
					auto iterpoint = (*iterlines).second.begin();
					transitionPoint(*iterpoint, xScale, xr, yScale, yr);
					_path.moveTo(*iterpoint); iterpoint++;
					for (; iterpoint != (*iterlines).second.end(); iterpoint++)
					{
						transitionPoint(*iterpoint, xScale, xr, yScale, yr);
						_path.lineTo(*iterpoint);
					}
					QVector<QLineF> lines = Getlines((*iterlines).second);
					painter2.fillPath(_path, QBrush(QColor(0,0,0,0)));
					painter1.drawPath(_path);
					lines_list.push_back(lines);
				}
			}
		}
	}
#pragma region 测试用
	//绘制横向切割线
	QVector<QLineF> liney = GetCutLine_y();
	QVector<QLineF> linex = GetCurLine_x();
	painter1.drawLines(linex);
	painter1.drawLines(liney);
#pragma endregion
	painter1.setCompositionMode(QPainter::CompositionMode_SourceOver);
	painter1.drawImage(0, 0, img2);
	for each (QVector<QLineF> var in lines_list)
	{
		painter1.drawLines(var);
	}
	//绘制线段
	/**********************************************/
	for each (linepen var in linepenlist)
	{
		painter1.setPen(var.pen);
		painter1.drawLine(var.line);
	}
	/**********************************************/
	auto nImg = img1.mirrored(false, true);
	//替换白色为透明色
	QColor srColor(255, 255, 255, 255);
	QColor desAlpha(0, 0, 0, 0);
	for (int w = 0; w < nImg.width();++w)
	{
		for (int h = 0; h < nImg.height();++h)
		{
			if (nImg.pixel(w,h)==srColor.rgb())
			{
				nImg.setPixel(w, h, desAlpha.rgba());
			}
		}
	}
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
* @brief Struct2DRenderer::drawPloy 绘制多边形
* @return bool
*/
bool Struct2DRenderer::drawPloy()
{
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
	std::map<int, std::map<int, std::vector<QPointF>>> map = d->GetAllinfo();
	QVector<QVector<QLineF>> lines_list;
	for (auto iter = map.begin(); iter != map.end(); iter++)
	{
		auto itercolor = color_tab.find(iter->first);
		if (itercolor != color_tab.end())
		{
			QBrush brush(itercolor.value());
			painter.setBrush(brush);
			for (auto iterlines = iter->second.begin(); iterlines != iter->second.end(); iterlines++)
			{
				if (iterlines->second.size() == 2)
				{
					auto linestyle = pen_tab.find(iter->first);
					if (linestyle != pen_tab.end())
					{
						painter.setPen(*linestyle);
					}
					auto iterpoint = (*iterlines).second.begin();
					transitionPoint(*iterpoint, xScale, xr, yScale, yr);
					transitionPoint(*(iterpoint + 1), xScale, xr, yScale, yr);
					painter.drawLine((*iterpoint), *(iterpoint + 1));
					painter.setPen(pen);
				}
				else
				{
					QPainterPath _path;
					auto iterpoint = (*iterlines).second.begin();
					transitionPoint(*iterpoint, xScale, xr, yScale, yr);
					_path.moveTo(*iterpoint); iterpoint++;
					for (; iterpoint != (*iterlines).second.end(); iterpoint++)
					{
						transitionPoint(*iterpoint, xScale, xr, yScale, yr);
						_path.lineTo(*iterpoint);
					}
					QVector<QLineF> lines = Getlines((*iterlines).second);
					painter.drawPath(_path);
					lines_list.push_back(lines);
				}
			}
		}
	}
	for each (QVector<QLineF> var in lines_list)
	{
		painter.drawLines(var);
	}
	//QPen pen2(Qt::white);
	//pen2.setWidth(1);
	//painter.setPen(pen2);
	//std::vector<QPointF> allpos = d->ALLPOINTF();
	//int XSize = d->getposxSize();
	//int YSize = d->getposySize();
	////测试用
	//for (auto y = 0; y < YSize-1;y++)
	//{
	//	for (auto x = 0; x < XSize-1;x++)
	//	{
	//		QPointF _left = allpos[y*(XSize)+x];
	//		QPointF _right = allpos[y*(XSize) + (x + 1)];
	//		transitionPoint(_left, xScale, xr, yScale, yr);
	//		transitionPoint(_right, xScale, xr, yScale, yr);
	//		painter.drawLine(_left, _right);
	//	}
	//}

	//for (auto x = 0; x < XSize - 1; x++)
	//{
	//	for (auto y = 0; y < YSize - 1; y++)
	//	{
	//		QPointF _top = allpos[y*(XSize)+x];
	//		QPointF _bottom = allpos[(y+1)*(XSize)+(x)];
	//		transitionPoint(_top, xScale, xr, yScale, yr);
	//		transitionPoint(_bottom, xScale, xr, yScale, yr);
	//		painter.drawLine(_top, _bottom);
	//	}
	//}
	auto nImg = img.mirrored(false, true);
	setImage(nImg);
	return true;
}
QVector<QLineF> Struct2DRenderer::GetCurLine_x(){
	QVector<QLineF> lines;
	float xScale, yScale;
	getTransitionScale(xScale, yScale);
	auto xr = getXRang();
	auto yr = getYRang();
	std::shared_ptr<Struct2dData> d = std::dynamic_pointer_cast<Struct2dData>(data);
	std::vector<QPointF> Allpoint = d->ALLPOINTF();
	int posxSizeX = d->getposxSize();
	int posxSizeY = d->getposySize();
	for (auto y = 0; y < posxSizeY;y++)
	{
		QPointF _left = Allpoint[y*posxSizeX];
		QPointF _right = Allpoint[(y + 1)*posxSizeX - 1];
		transitionPoint(_left, xScale, xr, yScale, yr);
		transitionPoint(_right, xScale, xr, yScale, yr);
		lines.push_back(QLineF(_left, _right));
	}
	return lines;
}
QVector<QLineF> Struct2DRenderer::GetCutLine_y(){
	QVector<QLineF> lines;
	float xScale, yScale;
	getTransitionScale(xScale, yScale);
	auto xr = getXRang();
	auto yr = getYRang();
	std::shared_ptr<Struct2dData> d = std::dynamic_pointer_cast<Struct2dData>(data);
	std::vector<QPointF> Allpoint = d->ALLPOINTF();
	int posxsize = d->getposxSize();
	int posysize = d->getposySize();
	for (auto x = 0; x < posxsize;x++)
	{
		QPointF bottom = Allpoint[x];
		QPointF top = Allpoint[(posysize - 1)*posxsize + x];
		transitionPoint(top, xScale, xr, yScale, yr);
		transitionPoint(bottom, xScale, xr, yScale, yr);
		lines.push_back(QLineF(top,bottom));
	}
	return lines;
}

/**
* @brief  Struct2DRenderer::loadconfig 加载配置
* @return void  
*/
void Struct2DRenderer::loadconfig(){
//获取配置
	Config::GetInstance()->loadConfig();
	auto mGroup = Config::GetInstance()->getRootGroup();
	auto structGroup = mGroup.getGroup("struct");
	auto struct2DGroup = mGroup.getGroup("struct2D");
#define GETCONFIG(x)\
	color_tab[x]=QStringToQColor(QString::fromStdString(structGroup.getValue(#x)));\
	color_line[x]=QStringToQColor(QString::fromStdString(structGroup.getValue(#x "line")));\
			{QPen pen(QStringToQColor(QString::fromStdString(struct2DGroup.getValue(#x))));\
	pen.setStyle((struct2DGroup.getValue(#x "type").find("solid")!=std::string::npos)?(Qt::SolidLine):(Qt::DashLine));\
	pen.setWidth(atoi((struct2DGroup.getValue(#x "width")).c_str()));\
	pen_tab[x]=pen;\
	qDebug()<<x<<color_tab[x];\
	}
	GETCONFIG(Perfect_Conductor);
	GETCONFIG(Conductor_New);
	GETCONFIG(Diolectric);
	GETCONFIG(Permeability);
	GETCONFIG(Vacuo);
#undef GETCONFIG(x)
	isAA = atoi(structGroup.getValue("isAlis").c_str());
}
