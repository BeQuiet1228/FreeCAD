#pragma once
#include <QWidget>
#include <QPaintEvent>
#include <QPixmap>
class Plot:public QWidget{
public:
	Plot(QWidget* parent = 0);
	~Plot();

protected:
	void paintEvent(QPaintEvent *event);

public:
	QPixmap pixmap;
};