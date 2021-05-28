#pragma once
#ifndef COLOR_MAP_WIDGET_H_
#define COLOR_MAP_WIDGET_H_
#include "qwt/qwt_scale_widget.h"
class ColorMapWidget :public QwtScaleWidget
{
	Q_OBJECT
public:
	explicit ColorMapWidget(QWidget* parent = nullptr);
	explicit ColorMapWidget(QwtScaleDraw::Alignment, QWidget* parent = nullptr);
	~ColorMapWidget();
public:
	virtual void mouseDoubleClickEvent(QMouseEvent *event) override;
};

#endif