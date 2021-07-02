#include "axis.h"
#include<QGridLayout>
#include"qwt/qwt_scale_engine.h"
#include"ScaleWidget.h"
Axis::Axis(QWidget* parent):QWidget(parent)
{
	//设置默认参数
	AxisNum = 5;
	mAxisunit = "X(x)";
	mAxisstyle = AxisBottom;
	axisvalrange.min = 0.0f;
	axisvalrange.max = 100.0f;
	//mqgridlayout = new QGridLayout;
	//mqgridlayout->setSpacing(0);
	//this->setLayout(mqgridlayout);
	mQwtScaleWidget = new ScaleWidget(this);
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
	//int widgetCount = mqgridlayout->count();
	//ScaleWidget* mQwtScaleWidget = nullptr;
	//for (int index=widgetCount-1;index>=0;index--)
	//{
	//	mQwtScaleWidget = dynamic_cast<ScaleWidget*>(mqgridlayout->itemAt(index)->widget());
	//	if (mQwtScaleWidget)
	//		break;
	//}
	//if (!mQwtScaleWidget)
	//{
	//	mQwtScaleWidget = new ScaleWidget(this);
	//}
	mQwtScaleWidget->hide();
	switch (mAxisstyle)
	{
	case Axisleft:
	{
		mQwtScaleWidget->setAlignment(QwtScaleDraw::LeftScale);
	}break;
	case AxisRight:
	{
		mQwtScaleWidget->setAlignment(QwtScaleDraw::RightScale);
	}break;
	case AxisTop:
	{
		mQwtScaleWidget->setAlignment(QwtScaleDraw::TopScale);
	}break;
	case AxisBottom:
	{
		mQwtScaleWidget->setAlignment(QwtScaleDraw::BottomScale);
	
	}break;
	}
	QSize size = this->size();
	mQwtScaleWidget->setColorBarEnabled(true);
	QwtLinearScaleEngine * mQwtLinearScaleEngine = new QwtLinearScaleEngine;
	mQwtScaleWidget->setScaleDiv(mQwtLinearScaleEngine->divideScale(axisvalrange.min, axisvalrange.max, AxisNum, 5));
	mQwtScaleWidget->setTitle(mAxisunit);
	//mqgridlayout->addWidget(mQwtScaleWidget, 0, 0);
	int start, end;
	mQwtScaleWidget->setMargin(1);
	mQwtScaleWidget->setSpacing(0);
	mQwtScaleWidget->getBorderDistHint(start,end);
	mQwtScaleWidget->setBorderDist(0, 0);
	mQwtScaleWidget->show();
}

void  Axis::resizeEvent(QResizeEvent* sizeEvent)
{
	mQwtScaleWidget->resize(this->size());
}
#include "moc_Axis.cpp"
