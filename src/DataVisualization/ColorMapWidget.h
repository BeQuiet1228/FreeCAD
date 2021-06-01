#pragma once
#ifndef COLOR_MAP_WIDGET_H_
#define COLOR_MAP_WIDGET_H_
#include "qwt/qwt_scale_widget.h"
class realTimewidget;
class ColorMapWidget :public QwtScaleWidget
{
	Q_OBJECT
public:
	explicit ColorMapWidget(QWidget* parent = nullptr);
	explicit ColorMapWidget(QwtScaleDraw::Alignment, QWidget* parent = nullptr);
	~ColorMapWidget();
Q_SIGNALS:
	void GetListDouble(std::vector<double>&);
	public Q_SLOTS:
	void setclose(bool);
	void setValrange(float rmin,float rmax);
	void GetListDoubleslot(std::vector<double>&);
public:
	virtual void mouseDoubleClickEvent(QMouseEvent *event) override;
	realTimewidget* mrealTimewidget;
	bool isColse;
	float min;
	float max;
};

#endif