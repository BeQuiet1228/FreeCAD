#include "Renderer.h"
#include <iostream>
#include <QPen>
#include <QPainter>
Renderer::Renderer(std::shared_ptr<Data> data)
{
	this->data = data;
}

Renderer::~Renderer()
{

}

/**
* @brief Renderer::setImage
* @param const QImage & map
* @return void
*/
void Renderer::setImage(const QImage& map)
{
	AutoMutex am(imageMutex);
	this->image = map;
}

/**
* @brief Renderer::getImage
* @return QT_NAMESPACE::QImage
*/
QImage Renderer::getImage()
{
	AutoMutex am(imageMutex);
	return this->image;
}

/**
* @brief Renderer::setSize 设置渲染图片的大小
* @param const QSize & size
* @return void
*/
void Renderer::setSize(const QSize& size)
{
	AutoMutex am(imageSizeMutex);
	imageSize = size;
}

/**
* @brief Renderer::setSize
* @param const int & width
* @param const int & hegiht
* @return void
*/
void Renderer::setSize(const int& width, const int& hegiht)
{
	AutoMutex am(imageSizeMutex);
	imageSize.setWidth(width);
	imageSize.setHeight(hegiht);
}

/**
* @brief Renderer::getSize
* @return QT_NAMESPACE::QSize
*/
QSize Renderer::getSize()
{
	AutoMutex am(imageSizeMutex);
	return imageSize;
}


/**
* @brief Renderer::setFindPosition 设置查找点的位置
* @param const QPointF & pos
* @return void
*/
void Renderer::setFindPosition(const QPointF& pos)
{
	AutoMutex am(findPositionMutex);
	findPosition = pos;
}

QPointF Renderer::getFindPosition()
{
	AutoMutex am(findPositionMutex);
	return findPosition;
}

bool Renderer::addListRang(std::list<Data::Rang> listRang)
{
	std::cerr << "Renderer::addListRang it can't be called here!" << std::endl;
	return false;
}

/**
* @brief Renderer::dataInit 初始化数据
* @return void
*/
void Renderer::dataInit()
{
	data->loadSourceData();
}

/**
* @brief Renderer::setXRang 设置x轴的渲染范围
* @param const Data::Rang & rang
* @return void
*/
void Renderer::setXRang(const Data::Rang& rang)
{
	Renderer::AutoMutex am(xRangMutex);
	xRang = rang;
}

/**
* @brief Renderer::getXRang 获取x轴的渲染范围
* @return Data::Rang
*/
Data::Rang Renderer::getXRang()
{
	Renderer::AutoMutex am(xRangMutex);
	return xRang;
}

/**
* @brief Renderer::setYRang 设置y轴的渲染范围
* @param const Data::Rang & rang
* @return void
*/
void Renderer::setYRang(const Data::Rang& rang)
{
	Renderer::AutoMutex am(yRangMutex);
	yRang = rang;
}

/**
* @brief Renderer::getYRang 获取y轴的渲染范围
* @return Data::Rang
*/
Data::Rang Renderer::getYRang()
{
	Renderer::AutoMutex am(yRangMutex);
	return yRang;
}

/**
* @brief Renderer::getTransitionScale 初始化数据与图片坐标的缩放比例
* @param float & xScale
* @param float & yScale
* @return bool
*/
bool Renderer::getTransitionScale(float& xScale, float& yScale)
{
	auto size = getSize();
	auto xr = getXRang();
	auto yr = getYRang();

	float xLength = xr.max - xr.min;
	float yLength = yr.max - yr.min;

	if (xLength < 0 || yLength < 0)
	{
#if MY_DEBUG
		std::cerr << "TimeRenderer::getTransitionScale length < 0" << std::endl;
#endif
		return false;
	}

	if (size.width() <= 0 || size.height() <= 0)
	{
#if MY_DEBUG
		std::cerr << "TimeRenderer::getTransitionScale size <= 0" << std::endl;
#endif
		return false;
	}
	xScale = yScale = 0.0;
	if(xLength != 0.0)
		xScale = size.width() / xLength;
	if(yLength != 0.0)
		yScale = size.height() / yLength;

	return true;
}

/**
* @brief Renderer::transitionDataToScreen 将数据按照缩放比例转换为屏幕数据
* @param const float & d 数据
* @param const float scale 缩放比例
* @param Data::Rang rang 渲染范围
* @return float 
*/
float Renderer::transitionDataToScreen(const float& d, const float scale, Data::Rang rang)
{
	return (d - rang.min)*scale;
}

/**
* @brief Renderer::displayPointInformation 绘制点位信息
* @param QPainter* painter
* @param QPointF* point
* @param std::map<QString, float> list 绘制列表
* @return void
*/
void Renderer::displayPointInformation(QPainter* painter, QPointF* point , std::map<QString, float> list)
{
	//设置画笔的颜色
	QPen pen;
	pen.setColor(QColor(102, 205, 170));
	pen.setWidth(2);
	painter->setPen(pen);
	painter->setBrush(QBrush(QColor(255, 250, 240)));
	//显示信息
	std::vector<QString> varstrlist;
	for(auto iter = list.begin(); iter != list.end();iter++)
	{
		QString varstr = QString("%1:%2").arg(iter->first).arg(iter->second, 0, 'E', 2);
		varstrlist.push_back(varstr);
	}
	QFont f;
	f.setPixelSize(17);
	QFontMetrics fm(f);
	int maxWidth = 0;
	int perHeight = 0;
	for each (QString var in varstrlist)
	{
		QRect rect = fm.boundingRect(var);
		if (rect.width() > maxWidth)
		{
			maxWidth = rect.width();
			perHeight = rect.height();
		}
	}
	//获取到最大长度,总高度
	QRect displayRect;
	displayRect.setX(point->x());
	displayRect.setY(point->y());
	auto size = getSize();
	//获取对话框的宽高
	int displayRectWidth = maxWidth + 20;
	int displayRectHeight = (perHeight + 3)*varstrlist.size() + 3;
	if (displayRect.y() > size.height() - displayRectHeight)
	{
		displayRect.setY(displayRect.y() - displayRectHeight);
	}
	if (displayRect.x() > size.width() - displayRectWidth)
	{
		displayRect.setX(displayRect.x() - displayRectWidth);
	}
	displayRect.setWidth(displayRectWidth);
	displayRect.setHeight(displayRectHeight);
	painter->drawRect(displayRect);
	//绘制信息
	painter->setFont(f);
	//for each (QString var in varstrlist)
	for (auto i = 0; i < varstrlist.size(); i++)
		painter->drawText(displayRect.x() + 10, displayRect.y() + (perHeight + 3)*(i + 1), varstrlist[i]);
}