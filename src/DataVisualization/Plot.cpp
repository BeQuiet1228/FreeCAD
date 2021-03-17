#include "Plot.h"
#include <QPainter>
#include "Canvas.h"
#include "Axis.h"
Plot::Plot(QWidget* parent /*= 0*/)
	:QWidget(parent)
{
	gridLayout = new QGridLayout;
	this->setLayout(gridLayout);
	canvas = new Canvas();
	AxisL = new Axis();
	AxisB = new Axis();

	gridLayout->addWidget(canvas, 0, 1, 1, 1);
	gridLayout->addWidget(AxisL, 0, 0, 1, 1);
	gridLayout->addWidget(AxisB, 1, 1, 1, 1);

	gridLayout->setRowStretch(0, 9);
	gridLayout->setRowStretch(1, 1);
	gridLayout->setColumnStretch(0, 1);
	gridLayout->setColumnStretch(1, 9);
	
}

Plot::~Plot()
{
	delete canvas;
	delete AxisB;
	delete AxisL;
}


#include "moc_Plot.cpp"
