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
	CanvasItem();
	~CanvasItem() = default;
private:
	std::shared_ptr<QPixmap> pixmap;
	QPoint pos;
	QPen pen;
public:
	void setPixmap(const QPixmap& pixmap,const QPoint& point = QPoint(0,0)){
		this->pixmap.reset(new QPixmap(pixmap));
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
	//²ã¼¶
	unsigned int rank;
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