#include "Renderer.h"
#include <iostream>
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