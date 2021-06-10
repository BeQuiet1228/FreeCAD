#include "Canvas.h"
#include <QMetaType>
#include <mutex>
#include <QPoint>
#include <iostream>
Canvas::Canvas(QWidget* parent /*= 0*/)
	:QWidget(parent)
{
	initData();
}

Canvas::~Canvas()
{

}

/**
* @brief Canvas::addIteam 添加一个item 如果rank已经存在 那么会覆盖掉之前的 
* @param const CanvasItem & iteam
* @return void
*/
void Canvas::addIteam(const CanvasItem& iteam)
{
	auto iter = this->items.find(iteam.rank);
	if (iter != this->items.end())
		items.erase(iter);
	items.insert(std::map<unsigned int, CanvasItem>::value_type(iteam.rank, iteam));
	update();
}

/**
* @brief Canvas::removeItem 移除显示项  如果没有该项则不做操作
* @param const unsigned int & rank 层级
* @return void
*/
void Canvas::removeItem(const unsigned int& rank)
{
	auto iter = items.find(rank);
	if (iter == items.end())
		return;
	items.erase(iter);
	update();
}

void Canvas::paintEvent(QPaintEvent *event)
{
	QPainter painter(this);
	//绘制外边框线
	painter.drawRect(0, 0, this->width() - 1, this->height() - 1);

	for (auto item = items.begin(); item != items.end(); item++)
	{
#if 0
		std::cerr << "canvas width:" << this->size().width()
			<< ",canvas height:" << this->size().height() << ",image width:" << this->size().width()
			<< ",image height:" << this->size().height() 
			<< ",draw pos:(" << item->second.pos.x() << "," << item->second.pos.y() << ")" << std::endl;
#endif
		painter.setPen(item->second.pen);
		painter.drawImage(item->second.pos, *(item->second.image.get()));
	}
	if (mouseLeftPress)
	{
		painter.drawRect(selectRect);
	}

}

/**
* @brief Canvas::mouseMoveEvent
* @param QMouseEvent * event
* @return void
*/
void Canvas::mouseMoveEvent(QMouseEvent *event)
{
	QWidget::mouseMoveEvent(event);
	if (!mouseLeftPress)
		return;
	selectRect.setWidth(event->pos().x() - selectRect.x());
	selectRect.setHeight(event->pos().y() - selectRect.y());
	update();
}

/**
* @brief Canvas::mousePressEvent
* @param QMouseEvent * event
* @return void
*/
void Canvas::mousePressEvent(QMouseEvent *event)
{
	QWidget::mousePressEvent(event);
	if (event->button() != Qt::RightButton)
		return;
	mouseLeftPress = true;
	selectRect.setX(event->pos().x());
	selectRect.setY(event->pos().y());
	selectRect.setWidth(0);
	selectRect.setHeight(0);
}

void Canvas::mouseReleaseEvent(QMouseEvent *event)
{
	QWidget::mouseReleaseEvent(event);
	//右键取点
	if (event->button() == Qt::LeftButton)
	{
		emitSelectPoint(event->pos());
		return;
	}
	//左键拖拽放大	
	if (event->button() != Qt::RightButton)
		return;
	mouseLeftPress = false;
	update();
	emitSelectRect(selectRect);
	selectRect.setWidth(0);
	selectRect.setHeight(0);
}

void Canvas::resizeEvent(QResizeEvent* event)
{
	QWidget::resizeEvent(event);
	emitResize(event->size());
}

void Canvas::initData()
{
	mouseLeftMode = SELECT_RECT;
	mouseLeftPress = false;
	selectRect.setWidth(0);
	selectRect.setHeight(0);
}

/**
* @brief CanvasItem::registerMetaTye 注册自定义信号参数
* @return void
*/
void CanvasItem::registerMetaTye()
{
	static std::once_flag flag;
	std::call_once(flag, [&](){
		qRegisterMetaType<CanvasItem>("CanvasItem");
	});
}


bool CanvasItem::operator==(const CanvasItem& item)
{
	return this->rank == item.rank;
}

bool CanvasItem::operator>(const CanvasItem& item)
{
	return this->rank > item.rank;
}

bool CanvasItem::operator<(const CanvasItem& item)
{
	return this->rank < item.rank;
}

CanvasItem::CanvasItem()
	:image(nullptr), rank(0), pos(0, 0)
{

}

#include "moc_Canvas.cpp"