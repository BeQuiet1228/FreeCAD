#pragma once
#ifndef  SCALE_WIDGET_H_
#define  SCALE_WIDGET_H_
#include "qwt/qwt_scale_widget.h"
class ScaleWidget :public QwtScaleWidget
{
	Q_OBJECT
public:
	explicit ScaleWidget(QWidget* parent=nullptr);
	explicit ScaleWidget(QwtScaleDraw::Alignment,QWidget* parent=nullptr);

public:
	void setAlignment(QwtScaleDraw::Alignment);
	void setRange(double min,double max);
	void setAxisValColor(QColor);
	virtual void resizeEvent(QResizeEvent*) override;
};
#endif