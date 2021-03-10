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
* @brief Renderer::setPixmap
* @param const QPixmap & map
* @return void
*/
void Renderer::setPixmap(const QPixmap& map)
{
	AutoMutex am(pixmapMutex);
	this->pixmap = map;
}

/**
* @brief Renderer::getPixmap
* @return QT_NAMESPACE::QPixmap
*/
QPixmap Renderer::getPixmap()
{
	AutoMutex am(pixmapMutex);
	return this->pixmap;
}

/**
* @brief Renderer::setSize 设置渲染图片的大小
* @param const QSize & size
* @return void
*/
void Renderer::setSize(const QSize& size)
{
	AutoMutex am(pixmapSizeMutex);
	pixmapSize = size;
}

/**
* @brief Renderer::setSize
* @param const int & width
* @param const int & hegiht
* @return void
*/
void Renderer::setSize(const int& width, const int& hegiht)
{
	AutoMutex am(pixmapSizeMutex);
	pixmapSize.setWidth(width);
	pixmapSize.setHeight(hegiht);
}

/**
* @brief Renderer::getSize
* @return QT_NAMESPACE::QSize
*/
QSize Renderer::getSize()
{
	AutoMutex am(pixmapSizeMutex);
	return pixmapSize;
}


bool Renderer::addListRang(std::list<Data::Rang> listRang)
{
	std::cerr << "Renderer::addListRang it can't be called here!" << std::endl;
	return false;
}
