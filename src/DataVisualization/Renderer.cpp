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
* @brief Renderer::setRatioDisplay 据横纵比例设置刻度范围
* @param double & horizontal
* @param double & vertical
* @return void
* @Time 2021/6/28
*/
void Renderer::setRatioDisplay(double& horizontal, double& vertical)
{
	QSize size = getSize();
	float sizeWidth = size.width();
	float sizeHeight = size.height();
	Data::Rang xr = getXRang();
	Data::Rang yr = getYRang();
	float xlenth = xr.max - xr.min;
	float ylenth = yr.max - yr.min;
	if (horizontal==0.0f ||vertical==0.0f)
		return;
	float scale_coef = horizontal / vertical;
	{
		float newxlength = sizeWidth / sizeHeight*(ylenth*vertical) / horizontal;
		float newylength = sizeHeight / sizeWidth*(xlenth*horizontal) / vertical;
		if (newxlength >= xlenth)		xlenth = newxlength;
		else if (newylength >= ylenth)	ylenth = newylength;
		else
			std::cerr << "xlength And yLength err from void Plot::setRatioDisplay(double& horizonal, double& vertical)" << std::endl;
		xr.max = xr.min + xlenth;
		yr.max = yr.min + ylenth;
		setXRang(xr);
		setYRang(yr);
	}
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

std::string Renderer::getInformationTitile()
{
	return data->getInformationTitle();
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
	painter->setRenderHint(QPainter::Antialiasing, true);
	QPen pen;
	pen.setColor(QColor(0, 0, 0));
	pen.setWidth(4);
	painter->setPen(pen);
	painter->setBrush(QBrush(QColor(255, 250, 250)));
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
	//获取到最大长度,总高度，设置矩形框偏离点位5个像素点
	QRect displayRect;
	displayRect.setX(point->x()+10);
	displayRect.setY(point->y()+10);
	auto size = getSize();
	//获取对话框的宽高
	int displayRectWidth = maxWidth + 20;
	int displayRectHeight = (perHeight + 3)*varstrlist.size() + 10;
	if (displayRect.y()+10 > size.height() - displayRectHeight)
	{
		displayRect.setY(displayRect.y() - displayRectHeight-20);
	}
	if (displayRect.x()+10 > size.width() - displayRectWidth)
	{
		displayRect.setX(displayRect.x() - displayRectWidth-20);
	}
	displayRect.setWidth(displayRectWidth);
	displayRect.setHeight(displayRectHeight);
	painter->drawRoundRect(displayRect, 10,10);
	//绘制信息
	painter->setFont(f);
	QPen pen1; pen1.setColor(QColor(0, 0, 0)); pen1.setWidth(3);
	QPen pen2; pen2.setColor(QColor(125, 125, 125)); pen2.setWidth(3);
	unsigned int i = 0;
	for (auto index =list.begin(); index!=list.end();index++,i++)
	{
		auto x = displayRect.x() + 10;
		auto y = displayRect.y() + (perHeight + 3)*(i + 1);
		painter->setPen(pen1);
		QRect rect = fm.boundingRect(QString("%1:").arg(index->first));
		painter->drawText(x,y,QString("%1:").arg(index->first));
		painter->setPen(pen2);
		x = x + rect.width();
		painter->drawText(x, y, QString("%1").arg(index->second,0,'E',2));
	}
}

/**
* @brief  Renderer::setDefaultRang 设置坐标系默认取值范围
* @param  QSize & size  
* @return bool  
*/
bool Renderer::setDefaultRang(QSize& size){
	return setDefaultRang(); 
}

std::shared_ptr<Data> Renderer::getData()
{
	return data;
}

#include "moc_PlotAdapter.cpp"