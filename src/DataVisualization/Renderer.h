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
	virtual ~Renderer();

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
	QPointF getFindPosition();
	//操作范围
	void setXRang(const Data::Rang& rang);
	Data::Rang getXRang();
	void setYRang(const Data::Rang& rang);
	Data::Rang getYRang();

	
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
	//渲染范围
	Data::Rang xRang, yRang;
	std::mutex xRangMutex, yRangMutex;
protected:
	//数据类
	std::shared_ptr<Data> data;
public:
	virtual bool drawImage() = 0;
	virtual bool addListRang(std::list<Data::Rang> listRang);
	virtual bool drawPointImage() = 0;
	//设置为默认渲染范围
	virtual bool setDefaultRang() = 0;
	//初始化数据
	virtual void dataInit();
};