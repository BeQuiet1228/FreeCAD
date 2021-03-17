#pragma once
#include <QPixmap>
#include <mutex>
#include <QSize>
#include "Data.h"
#include <memory>
#include <list>
class Renderer{
public:
	using AutoMutex = std::lock_guard<std::mutex>;
public: 
	Renderer(std::shared_ptr<Data> data);
	~Renderer();

public:
	//操作渲染图
	void setPixmap(const QPixmap& map);
	QPixmap getPixmap();
	//设置渲染大小
	void setSize(const QSize& size);
	void setSize(const int& width, const int& hegiht);
	QSize getSize();
	//设置取点的位置
	void setFindPosition(const QPointF& pos);

private:
	//渲染图
	QPixmap pixmap;
	std::mutex pixmapMutex;
	//渲染大小
	QSize pixmapSize;
	std::mutex pixmapSizeMutex;
	//点的位置
	QPointF findPosition;
	std::mutex findPositionMutex;
protected:
	//数据类
	std::shared_ptr<Data> data;
public:
	virtual bool drawPixmap() = 0;
	virtual bool addListRang(std::list<Data::Rang> listRang);
	virtual bool drawPointPixmap() = 0;
};