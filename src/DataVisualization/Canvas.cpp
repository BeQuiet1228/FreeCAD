#include "Canvas.h"
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

