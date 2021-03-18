#pragma once
#include <QWidget>
#include <QImage>
#include <list>
#include <memory>
#include <QPaintEvent>
#include <QPen>
#include <QPainter>
#include <map>
class Canvas;
class CanvasItem{
	friend class Canvas;
public:
	CanvasItem();
	~CanvasItem() = default;
private:
	std::shared_ptr<QImage> image;
	QPoint pos;
	QPen pen;
public:
	void setImage(const QImage& image,const QPoint& point = QPoint(0,0)){
		this->image.reset(new QImage(image));
		this->pos = point;
	}
	void setPen(const QPen& pen){
		this->pen = pen;
	}
	void setPos(const QPoint& pos){
		this->pos = pos;
	}
	QPoint getPos(){
		return this->pos;
	}
public:
	static void registerMetaTye();
	bool operator < (const CanvasItem& item);
	bool operator > (const CanvasItem& item);
	bool operator == (const CanvasItem& item);
public:
	//层级 同一个canvas中层级不能重复 不然会被覆盖掉
	unsigned int rank;
};
class Canvas :public QWidget{
public:
	Canvas(QWidget* parent = 0);
	~Canvas();
private:
	std::map<unsigned int,CanvasItem> items;
public:
	void addIteam(const CanvasItem& iteam);
	void clearIteam(){
		items.clear();
	};
protected:
	void paintEvent(QPaintEvent *event);
};