#include "Plot.h"
#include <QPainter>
Plot::Plot(QWidget* parent /*= 0*/)
	:QWidget(parent)
{

}

Plot::~Plot()
{

}

void Plot::paintEvent(QPaintEvent *event)
{
	QWidget::paintEvent(event);

	QPainter painter(this);
	painter.drawPixmap(0,0,pixmap.width(),pixmap.height(),pixmap);
}

