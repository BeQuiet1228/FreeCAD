#include "Canvas.h"
#include <QMetaType>
#include <mutex>
Canvas::Canvas(QWidget* parent /*= 0*/)
	:QWidget(parent)
{
	
}

Canvas::~Canvas()
{

}

void Canvas::paintEvent(QPaintEvent *event)
{
	QPainter painter(this);
	for (auto item = items.begin(); item != items.end(); item++)
	{
		painter.setPen(item->pen);
		painter.drawPixmap(item->pos.x(), item->pos.y(), item->pixmap->width()
			, item->pixmap->height(), *(item->pixmap.get()));
	}
	painter.drawRect(0, 0, this->width()-2, this->height()-2);
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
	:pixmap(nullptr), rank(0), pos(0, 0)
{

}
