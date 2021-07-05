#include "ScaleWidget.h"
ScaleWidget::ScaleWidget(QWidget* parent):QwtScaleWidget(parent)
{

}
ScaleWidget::ScaleWidget(QwtScaleDraw::Alignment a, QWidget* parent):QwtScaleWidget(a,parent)
{

}
void ScaleWidget::setAlignment(QwtScaleDraw::Alignment alignment)
{
	QwtScaleWidget::setAlignment(alignment);
}
void ScaleWidget::resizeEvent(QResizeEvent* e)
{
	QWidget* wid=this->parentWidget();
	//QwtScaleWidget::resizeEvent(e);
}

void ScaleWidget::setRange(double min, double max)
{
	if(min<max)
	this->scaleDraw()->setRange(min, max);
}
void ScaleWidget::setAxisValColor(QColor color)
{
	this->scaleDraw()->setAxisValColor(color);
}
#include "moc_ScaleWidget.cpp"