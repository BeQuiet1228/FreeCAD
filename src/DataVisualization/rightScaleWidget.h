#pragma once
#ifndef RIGHTSCALEWIDGET_H_
#define RIGHTSCALEWIDGET_H_
#include "ScaleWidget.h"
class AxisLable;
class rightScaleWidget :public ScaleWidget
{
	Q_OBJECT
public:
	explicit rightScaleWidget(QWidget* parent=nullptr);
	explicit rightScaleWidget(QwtScaleDraw::Alignment, QWidget* parent = nullptr);
	~rightScaleWidget();
	void initUI();
	void automatic();
public:
	virtual void mouseDoubleClickEvent(QMouseEvent* e)override;
public Q_SLOTS:
	void slotCloseEvent();
private:
	int GetdecimalBit(double& value);
protected:
	AxisLable* mAxisLable;

};
#endif