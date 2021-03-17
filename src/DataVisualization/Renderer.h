#pragma once
#include <QImage>
#include <mutex>
#include <QSize>
#include "Data.h"
#include <memory>
#include <list>
#include <QImage>
class Renderer{
public:
	using AutoMutex = std::lock_guard<std::mutex>;
public: 
	Renderer(std::shared_ptr<Data> data);
	~Renderer();

public:
	//操作渲染图
	void setImage(const QImage& map);
	QImage getImage();
	//设置渲染大小
	void setSize(const QSize& size);
	void setSize(const int& width, const int& hegiht);
	QSize getSize();
	//设置取点的位置
	void setFindPosition(const QPointF& pos);

private:
	//渲染图
	QImage image;
	std::mutex imageMutex;
	//渲染大小
	QSize imageSize;
	std::mutex imageSizeMutex;
	//点的位置
	QPointF findPosition;
	std::mutex findPositionMutex;
protected:
	//数据类
	std::shared_ptr<Data> data;
public:
	virtual bool drawImage() = 0;
	virtual bool addListRang(std::list<Data::Rang> listRang);
	virtual bool drawPointImage() = 0;
};