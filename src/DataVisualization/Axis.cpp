#include "axis.h"
#include<QGridLayout>
#include "qwt/qwt_scale_draw.h"
Axis::Axis(QWidget* parent):QWidget(parent)
{
	//设置默认参数
	AxisNum = 5;
	mAxisunit = "X(x)";
	mAxisstyle = AxisBottom;
	axisvalrange.min = 0.0f;
	axisvalrange.max = 100.0f;
	mqgridlayout = new QGridLayout;
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
	for (int index=widgetCount;index>=0;index--)
	{
		
	}
	switch (mAxisstyle)
	{
	case Axisleft:
	{
	}break;
	case AxisRight:
	{
	}break;
	case AxisTop:
	{
	}break;
	case AxisBottom:
	{
		QwtScaleDraw* newScale = new QwtScaleDraw();
		
	}break;
	}
}
#include "moc_Axis.cpp"
