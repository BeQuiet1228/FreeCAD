#pragma once
#include <QWidget>
#include <QPaintEvent>
#include <QPixmap>
#include <QGridLayout>
#include "Canvas.h"
class Axis;
class Plot:public QWidget{
public:
	Plot(QWidget* parent = 0);
	~Plot();
public:
	void addCanvasItem(const CanvasItem& item){
		canvas->addIteam(item);
	};
private:
	QGridLayout * gridLayout;
	Canvas *canvas;
	Axis *AxisL, *AxisB;
};