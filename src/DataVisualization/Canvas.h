#pragma once
#include <QWidget>
#include <QImage>
#include <list>
#include <memory>
#include <QPaintEvent>
#include <QPen>
#include <QPainter>
#include <map>
#include <QMouseEvent>
#include <QRect>
#include "exportConfig.hpp"
class Canvas;
class DATA_VISUALIZATION_EXPORT CanvasItem{
	friend class Canvas;
public:
	CanvasItem();
	~CanvasItem() = default;
private:
	std::shared_ptr<QImage> image;
	QPoint pos;
	QPen pen;
public:
	void setImage(const QImage& image, const QPoint& point = QPoint(0, 0));
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
class DATA_VISUALIZATION_EXPORT Canvas : public QWidget{
	Q_OBJECT
public:
	enum MouseLeftMode{
		FIND_POINT = 0,
		SELECT_RECT
	};
public:
	Canvas(QWidget* parent = 0);
	~Canvas();
private:
	//绘制对象
	std::map<unsigned int,CanvasItem> items;
	//鼠标左键按下
	bool mouseLeftPress;
	//鼠标拖拽时的矩形框
	QRect selectRect;
	//鼠标左键功能绑定
	MouseLeftMode mouseLeftMode;
public:
	//添加显示项
	void addIteam(const CanvasItem& iteam);
	//移除显示项
	void removeItem(const unsigned int& rank);
	void clearIteam(){
		items.clear();
	};
protected:
	void paintEvent(QPaintEvent *event) override;
	void mouseMoveEvent(QMouseEvent *event) override;
	void mousePressEvent(QMouseEvent *event) override;
	void mouseReleaseEvent(QMouseEvent *event) override;
	void resizeEvent(QResizeEvent* event) override;
private:
	void initData();

Q_SIGNALS:
	void emitSelectRect(QRect);
	void emitSelectPoint(QPoint);
	void emitResize(QSize);

public:
	//从渲染器起始层级
	static const unsigned int SUB_RENDER_START_RANK = 10;
	static const unsigned int FIND_POINT_RENDER_RANK = SUB_RENDER_START_RANK + 20;
};