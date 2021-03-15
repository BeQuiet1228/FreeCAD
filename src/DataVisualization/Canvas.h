#pragma once
#include <QWidget>
#include <QPixmap>
#include <list>
#include <memory>
#include <QPaintEvent>
#include <QPen>
#include <QPainter>
class Canvas;
class CanvasItem{
	friend class Canvas;
public:
	CanvasItem():pixmap(nullptr){}
	~CanvasItem(){}
private:
	std::shared_ptr<QPixmap> pixmap;
	QPoint pos;
	QPen pen;
public:
	void setPixmap(const QPixmap& pixmap,const QPoint& point){
		this->pixmap.reset(new QPixmap(pixmap));
		this->pos = point;
	}
	void setPen(const QPen& pen){
		this->pen = pen;
	}
};
class Canvas :public QWidget{
public:
	Canvas(QWidget* parent = 0);
	~Canvas();
private:
	std::list<CanvasItem> items;
public:
	void addIteam(const CanvasItem& iteam){
		this->items.push_back(iteam);
	}
	void clearIteam(){
		items.clear();
	};
protected:
	void paintEvent(QPaintEvent *event);
};