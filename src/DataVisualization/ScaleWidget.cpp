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
#include "moc_ScaleWidget.cpp"