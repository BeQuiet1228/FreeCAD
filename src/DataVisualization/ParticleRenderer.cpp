#include "ParticleRenderer.h"
#include "ParticleData.h"
#include <QPen>
#include <QPainter>
#include "C_encoding.h"
#include "CustomConfig.h"
ParticleRenderer::ParticleRenderer(std::shared_ptr<ParticleData> data)
	:Renderer(std::dynamic_pointer_cast<Data>(data))
{
	particleColor=Qt::red;
	particleSize = 1;
}

ParticleRenderer::~ParticleRenderer()
{

}

bool ParticleRenderer::drawImage()
{
	//获取坐标缩放比例
	float yScale(0.0), xScale(0.0);
	if (!getTransitionScale(xScale, yScale))
		return false;
	std::shared_ptr<ParticleData> d = std::dynamic_pointer_cast<ParticleData>(data);
	if (!d)
	{
#if LOG
		std::cerr << "ParticleRenderer::drawImage() data dynamic cast failed!" << std::endl;
#endif
		return false;
	}

	//获取起始点,因为图表的刻度不一定是从零开始的。
	auto xr = getXRang();
	auto yr = getYRang();

	//获取数据索引的范围
	int startIndex(0), endIndex(0);
	startIndex = d->findIndexFromXValueL(xr.min);
	endIndex = d->findIndexFromXValueL(xr.max);

	//新建画布 画笔
	QImage img(getSize(), QImage::Format_ARGB32);
	img.fill(qRgba(0, 0, 0, 0));
	QPen pen(particleColor);
	pen.setWidth(particleSize);
	QPainter painter(&img);
	painter.setPen(pen);

	ParticleData::Particle p;
	for (int index = startIndex + 1; index < endIndex; index++)
	{
		p = d->particles.at(index);
		p.x = transitionDataToScreen(p.x, xScale, xr);
		p.y = transitionDataToScreen(p.y, yScale, yr);
		painter.drawPoint(p.x,p.y);
	}
	//因为qpainter的屏幕坐标系原点在左上角，所以需要翻转图片才能得到我们想要的结果
	auto nImg = img.mirrored(false, true);
//#define _Debug
#ifdef _Debug
	static int index = 0;
	QString _path = QString("C:/Users/ASUS/Desktop/save/savepmg_%1.png").arg(index++);
	bool res = nImg.save(_path);
#undef _Debug
#endif
	setImage(nImg);

}

/**
* @brief ParticleRenderer::setDefaultRang 设置默认的渲染范围
* @return bool
*/
bool ParticleRenderer::setDefaultRang()
{
	auto particleData = std::dynamic_pointer_cast<ParticleData>(data);
	setXRang(particleData->getXRang());
	setYRang(particleData->getYRang());
	return true;
}

void ParticleRenderer::dataInit()
{
	Renderer::dataInit();
	auto pData = std::dynamic_pointer_cast<ParticleData>(data);
	if (!pData)
		return;
	pData->loadPoint();
}

/**
* @brief ParticleRenderer::drawPointImage
* @return bool
*/
bool ParticleRenderer::drawPointImage()
{
	//获取接近点
	ParticleData::Particle partical = findParticle(getFindPosition());
	//屏幕坐标
	QPointF tPoint(partical.x, partical.y);
	//新建画布 画笔
	QImage img(getSize(), QImage::Format_ARGB32);
	img.fill(qRgba(0, 0, 0, 0));
	QPen pen(Qt::red);
	pen.setBrush(Qt::blue);
	pen.setWidth(5);
	QPainter painter(&img);
	painter.setPen(pen);

	//将数据坐标转换为屏幕坐标
	tPoint = transitionPoint(tPoint);
	//坐标翻转（因为坐标系原点不一致的关系）
	tPoint.setY(getSize().height() - tPoint.y());
	//绘制点
	painter.drawPoint(tPoint);

	//绘制信息显示
	drawDisplayPoint(painter, tPoint, QPointF(partical.d1,partical.d2));

	setImage(img);
	return true;
}

/**
* @brief ParticleRenderer::findParticle 根据屏幕上点击的坐标 寻找近似点
* @param const QPointF & point
* @return ParticleData::Particle
*/
ParticleData::Particle ParticleRenderer::findParticle(const QPointF& point)
{
	//获取屏幕与数据的比例
	float xScale, yScale;
	getTransitionScale(xScale, yScale);
	auto xr = getXRang();
	auto yr = getYRang();

	/*
	1. 在屏幕中寻找近似点时，在以点击点为中心的正方形区域中寻找。
	2. 给定一个正方形边长的初始长度。
	3. 如果在第一个区域中为找到一个点，那么增加正方形边长，继续寻找。
	4. 当在某个区域中找到一些点之后，将这些点与点击点的距离算出来比较，得出最近点。
	*/

	std::list<ParticleData::Particle> particles;	//区域中的点
	for (unsigned int rank = 1; particles.size() == 0; rank++)
	{
		//正常行边长
		unsigned long riseLength = 10 * pow(2, rank);
		//正方形边界
		float xMin, xMax, yMin, yMax;
		xMax = point.x() + riseLength;
		xMin = point.x() - riseLength;
		yMax = point.y() + riseLength;
		yMin = point.y() - riseLength;

		//获取数据对象
		auto pd = std::dynamic_pointer_cast<ParticleData>(data);
		if (!pd)
		{
#ifdef MY_DEBUG
			std::cerr << "ParticleRenderer::findParticle pd is nullptr" << std::endl;
#endif
			break;
		}
		//获取数据索引的边界点
		int startIndex = pd->findIndexFromXValueL(xMin / xScale + xr.min);
		int endIndex = pd->findIndexFromXValueR(xMax / xScale + xr.min);

		//寻找区域中的点
		ParticleData::Particle p;
		for (int index = startIndex; index < endIndex; index++)
		{
			p = pd->getParticleHard(index);
			float y = (p.y - yr.min) * yScale;
			if (y > yMin && y < yMax)
				particles.push_back(p);

		}

	}

	//距离
	float minDistance;
	ParticleData::Particle temp;
	for (auto i = particles.begin(); i != particles.end(); i++)
	{
		float x = (i->x - xr.min)*xScale;
		float y = (i->y - yr.min)*yScale;
		float xDistance = abs(point.x() - x);
		float yDistance = abs(point.y() - y);
		float d = sqrt(pow(xDistance, 2) + pow(yDistance, 2));
		if (i == particles.begin())
		{
			minDistance = d;
			temp = *i;
		}
			
		if (d < minDistance)
		{
			temp = *i;
			minDistance = d;
		}
	}
	return temp;
}

/**
* @brief ParticleRenderer::drawDisplayPoint
* @param QPainter & painter
* @param const QPointF & position
* @param const QPointF & d
* @return void
*/
void ParticleRenderer::drawDisplayPoint(QPainter& painter, const QPointF& position, const QPointF& d)
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
* @brief ParticleRenderer::transitionPoint
* @param const QPointF & point
* @return QT_NAMESPACE::QPointF
*/
QPointF ParticleRenderer::transitionPoint(const QPointF& point)
{
	//获取屏幕与数据的比例
	float xScale, yScale;
	getTransitionScale(xScale, yScale);
	float x = point.x(), y = point.y();
	x = transitionDataToScreen(x, xScale, getXRang());
	y = transitionDataToScreen(y, yScale, getYRang());
	
	QPointF po(x, y);
	return po;
}
void ParticleRenderer::loadconfig()
{
	Config::GetInstance()->loadConfig();
	auto Group = Config::GetInstance()->getRootGroup();
	auto particleGroup = Group.getGroup("particle");
	particleColor = QStringToQColor(QString::fromStdString(particleGroup.getValue("color")));
	particleSize = atoi(particleGroup.getValue("size").c_str());
}
