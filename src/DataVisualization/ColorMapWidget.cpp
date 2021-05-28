#include "ColorMapWidget.h"
#include <QDebug>
#include "realTimewidget.h"
/**
* @brief  ColorMapWidget::ColorMapWidget
* @param  QWidget * parent  
* @return   
*/
ColorMapWidget::ColorMapWidget(QWidget* parent) :QwtScaleWidget(parent)
{
}
/**
* @brief  ColorMapWidget::ColorMapWidget
* @param  QwtScaleDraw::Alignment align  
* @param  QWidget * parent  
* @return   
*/
ColorMapWidget::ColorMapWidget(QwtScaleDraw::Alignment align, QWidget* parent):
QwtScaleWidget(align,parent)
{
}
/**
* @brief  ColorMapWidget::~ColorMapWidget
* @return   
*/
ColorMapWidget::~ColorMapWidget()
{
}
/**
* @brief  ColorMapWidget::mouseDoubleClickEvent Êó±êË«»÷ÊÂ¼þ
* @param  QMouseEvent * event  
* @return void  
*/
void ColorMapWidget::mouseDoubleClickEvent(QMouseEvent *event)
{
	qDebug("QwtScaleWidget:mouseDoubleClicked");
	realTimewidget* newwidget = new realTimewidget();
	newwidget->show();
}
#include "moc_ColorMapWidget.cpp"