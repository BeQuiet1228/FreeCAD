#include "axis.h"
#include<QGridLayout>
#include "qwt/qwt_scale_draw.h"
#include "qwt/qwt_scale_widget.h"
#include"qwt/qwt_scale_engine.h"
Axis::Axis(QWidget* parent):QWidget(parent)
{
	//设置默认参数
	AxisNum = 5;
	mAxisunit = "X(x)";
	mAxisstyle = AxisBottom;
	axisvalrange.min = 0.0f;
	axisvalrange.max = 100.0f;
	mqgridlayout = new QGridLayout;
	mqgridlayout->setSpacing(0);
	this->setLayout(mqgridlayout);
}
Axis::~Axis()
{

}
void Axis::setAxisRange(double min, double max)
{
	if (min < max)
	{
		axisvalrange.min = min;
		axisvalrange.max = max;
	}
}
void Axis::setAxisText(QString name)
{
	mAxisunit = name;
}
void Axis::setAxixStyle(Axisstyle style)
{
	mAxisstyle = style;
}
void Axis::SetAxisNumber(int number)
{
	if (number > 1)
		AxisNum = number;
}
void Axis::loadconfig()
{

}
void Axis::_update()
{
	int widgetCount = mqgridlayout->count();
	QwtScaleWidget* mQwtScaleWidget = nullptr;
	for (int index=widgetCount-1;index>=0;index--)
	{
		mQwtScaleWidget = dynamic_cast<QwtScaleWidget*>(mqgridlayout->itemAt(index)->widget());
		if (mQwtScaleWidget)
			break;
	}
	if (!mQwtScaleWidget)
	{
		mQwtScaleWidget = new QwtScaleWidget();
	}
	mQwtScaleWidget->hide();
	switch (mAxisstyle)
	{
	case Axisleft:
	{
		//mQwtScaleWidget = new QwtScaleWidget(QwtScaleDraw::LeftScale);
		mQwtScaleWidget->setAlignment(QwtScaleDraw::LeftScale);
	}break;
	case AxisRight:
	{
		mQwtScaleWidget->setAlignment(QwtScaleDraw::RightScale);
		//mQwtScaleWidget = new QwtScaleWidget(QwtScaleDraw::RightScale);
	}break;
	case AxisTop:
	{
		mQwtScaleWidget->setAlignment(QwtScaleDraw::TopScale);
		//mQwtScaleWidget = new QwtScaleWidget(QwtScaleDraw::TopScale);
	}break;
	case AxisBottom:
	{
		mQwtScaleWidget->setAlignment(QwtScaleDraw::BottomScale);
		//mQwtScaleWidget = new QwtScaleWidget(QwtScaleDraw::BottomScale);
	
	}break;
	}
	mQwtScaleWidget->setColorBarEnabled(true);
	QwtLinearScaleEngine * mQwtLinearScaleEngine = new QwtLinearScaleEngine;
	mQwtScaleWidget->setScaleDiv(mQwtLinearScaleEngine->divideScale(axisvalrange.min, axisvalrange.max, AxisNum, 5));
	mqgridlayout->addWidget(mQwtScaleWidget, 0, 0);
	//mQwtScaleWidget->setShown(false);
	mQwtScaleWidget->show();
}
#include "moc_Axis.cpp"
