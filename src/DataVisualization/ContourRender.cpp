
#include "ContourRender.h"
#include "qwt/qwt_scale_map.h"
#include <QRectF>
#include <QImage>
#include "Data.h"
#include <memory.h>
#include <qmath.h>
#include "CustomConfig.h"
#include "C_encoding.h"
#include "ConfigWidget.h"
ContourRender::ContourRender(std::shared_ptr<ContourData> data)
	:Renderer(std::dynamic_pointer_cast<Data>(data)),contourLevelsMod(EQUAL_DIFFERENCE)
	,contourLevel(10)
{
	setRenderThreadCount(0);

	setDisplayMode(DisplayMode::ImageMode, true);
	setDisplayMode(DisplayMode::ContourMode, true);
}

ContourRender::~ContourRender()
{

}

bool ContourRender::drawImage()
{
	setColorMap(ConfigWidget::getQwtLinearColorMap());

	QwtScaleMap xmap, ymap;
	xmap.setPaintInterval(0, this->getSize().width());
	xmap.setScaleInterval(getXRang().min, getXRang().max);
	ymap.setPaintInterval(0, this->getSize().height());
	ymap.setScaleInterval(getYRang().min, getYRang().max);
	QRectF rect(0, 0, getSize().width(), getSize().height());

	//新建画布 画笔
	QImage img(getSize(), QImage::Format_ARGB32);
	img.fill(qRgba(0, 0, 0, 0));
	QPainter painter(&img);
	painter.setRenderHint(QPainter::Antialiasing, cfgInfo.isAA);
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
	std::shared_ptr<ContourData> d = std::dynamic_pointer_cast<ContourData>(Renderer::data);

	auto pos = getFindPosition();
	//获取屏幕与数据的比例
	float xScale, yScale;
	getTransitionScale(xScale, yScale);
	Data::Rang xr = getXRang(), yr = getYRang();

	ContourData::Grid grid = d->findGrid(pos.x()/xScale+xr.min, pos.y()/yScale+yr.min);
	

	float x = grid.x, y = grid.y;
	x = transitionDataToScreen(x, xScale, getXRang());
	y = transitionDataToScreen(y, yScale, getYRang());
	//坐标翻转（因为坐标系原点不一致的关系）
	y = getSize().height() - y;

	//新建画布 画笔
	QImage img(getSize(), QImage::Format_ARGB32);
	img.fill(qRgba(0, 0, 0, 0));
	QPen pen(Qt::red);
	pen.setBrush(Qt::blue);
	pen.setWidth(5);
	QPainter painter(&img);
	painter.setPen(pen);

	QPointF point(x, y);
	painter.drawPoint(point);

	std::map<QString, float> list;
	list["X"] = grid.x;
	list["Y"] = grid.y;
	list["Value"] = grid.value;
	displayPointInformation(&painter,&point,list);
	setImage(img);
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

	initContourLevels();

	return true;
}

void ContourRender::dataInit()
{
	auto cd = std::dynamic_pointer_cast<ContourData>(Renderer::data);
	cd->loadPoint();
	setData(cd->getQwtMatrixRasterData());
}

Data::Rang ContourRender::getValueRange()
{
	auto d = std::dynamic_pointer_cast<ContourData>(Renderer::data);
	if (!d)
		return Data::Rang();
	return d->getVlaueRange();
}

/**
* @brief ContourRender::getStructFace
* @return std::vector<float>
*/
std::vector<float> ContourRender::getStructFace()
{
	auto d = std::dynamic_pointer_cast<ContourData>(Renderer::data);
	return d->getStructFace();
}

/**
* @brief ContourRender::drawDisplayPoint 显示点提示框
* @param QPainter & painter 画笔
* @param const QPointF & position 位置
* @param const ContourData::Grid & grid 网格信息
* @return void
*/
void ContourRender::drawDisplayPoint(QPainter& painter, const QPointF& position, const ContourData::Grid& grid)
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
		displayRect.setY(displayRect.y() - 90);
	}
	if (displayRect.x() > (size.width() - 170))
	{
		displayRect.setX(displayRect.x() - 190);
	}

	displayRect.setWidth(150);
	displayRect.setHeight(80);
	painter.drawRect(displayRect);
	//绘制显示信息
	QFont f;
	f.setPixelSize(17);
	painter.setFont(f);
	painter.drawText(displayRect.x() + 10,
		displayRect.y() + 20,
		QString("X:%1").arg(grid.x, 0, 'E', 2)
		);
	painter.drawText(displayRect.x() + 10,
		displayRect.y() + 40,
		QString("Y:%1").arg(grid.y, 0, 'E', 2)
		);
	painter.drawText(displayRect.x() + 10,
		displayRect.y() + 60,
		QString("Value:%1").arg(grid.value, 0, 'E', 2)
		);
}

void ContourRender::initContourLevels()
{
	auto cd = std::dynamic_pointer_cast<ContourData>(Renderer::data);

	Data::Rang vr = cd->getVlaueRange();

	if (contourLevelsMod == EQUAL_DIFFERENCE)
	{
		QList<double> contourLevels;
		for (double level = (vr.length() / contourLevel + vr.min); level < vr.max; level += vr.length() / contourLevel)
			contourLevels += level;
		setContourLevels(contourLevels);
	}else if (contourLevelsMod == PROPORTIONAL)
	{
		QList<double> contourLevels;
		double m = 1.0/contourLevel;
		m =  pow(vr.length(), m);
		for (int i = 1; i <= contourLevel; i++)
		{
			double vl =vr.min +  pow(m,i);
			contourLevels += vl;
		}
		setContourLevels(contourLevels);
	}

}
/**
* @brief  ContourRender::loadconfig 读取配置
* @return void  
*/
void ContourRender::loadconfig(){
	Config::GetInstance()->loadConfig();
	ConfigGroup mGroup = Config::GetInstance()->getRootGroup();
	ConfigGroup contourGroup = mGroup.getGroup("contour");
	//线段取值
	if (contourGroup.getGroup("lineMapColors").getValue("value").find("ScaleColors") != std::string::npos)
		cfgInfo.mode = QwtLinearColorMap::Mode::ScaledColors;
	else
		cfgInfo.mode = QwtLinearColorMap::Mode::FixedColors;
	//抗锯齿
	cfgInfo.isAA = atoi(contourGroup.getGroup("AlisAttitude").getValue("isAlis").c_str());
	//等级
	auto lineMapColorGroup = contourGroup.getGroup("lineMapColorval");
	int count = atoi(lineMapColorGroup.getValue("valueNumber").c_str());
	cfgInfo.colorlist.clear(); cfgInfo.colorlist.reserve(count);
	for (auto index = 0; index < count;index++)
	{
		CfgInfo::valColor valcolor;
		valcolor.value= atof(
			lineMapColorGroup.getGroup(QString("level_%1").arg(index).toStdString()).getValue("value").c_str());
		valcolor.color= QStringToQColor(QString::fromStdString(
			lineMapColorGroup.getGroup(QString("level_%1").arg(index).toStdString()).getValue("color")));
		cfgInfo.colorlist.push_back(valcolor);
	}
	//等级模式
	if (contourGroup.getGroup("valueStyle").getValue("value").find("equivalent") != std::string::npos)
		cfgInfo.contourLevelsMod = EQUAL_DIFFERENCE;
	else
		cfgInfo.contourLevelsMod = PROPORTIONAL;
}
