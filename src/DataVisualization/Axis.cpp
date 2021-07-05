#include "axis.h"
#include<QGridLayout>
#include"qwt/qwt_scale_engine.h"
#include"ScaleWidget.h"
#include<QMouseEvent>
#include"AxisLable.h"
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
	mQwtScaleWidget->resize(this->size());
	mAxisLable = new AxisLable(this);
	mAxisLable->setModal(true);
	mAxisLable->resize(300, 200);
	connect(mAxisLable, SIGNAL(signalCloseEvent()), this, SLOT(axiscloseEvent()));
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
	mQwtScaleWidget->hide();
	switch (mAxisstyle)
	{
	case Axisleft:
	{
		mQwtScaleWidget->setAlignment(QwtScaleDraw::LeftScale);
		mQwtScaleWidget->scaleDraw()->move(this->width()-1,0);
		mQwtScaleWidget->scaleDraw()->setLength(this->height()-1);
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
		mQwtScaleWidget->scaleDraw()->move(0,1);
		mQwtScaleWidget->scaleDraw()->setLength(this->width()-1);
	}break;
	}
	QSize size = this->size();
	mQwtScaleWidget->setColorBarEnabled(false);
	QwtLinearScaleEngine * mQwtLinearScaleEngine = new QwtLinearScaleEngine;
	mQwtScaleWidget->setScaleDiv(mQwtLinearScaleEngine->divideScale(axisvalrange.min, axisvalrange.max, AxisNum, 5));
	mQwtScaleWidget->setRange(axisvalrange.min,axisvalrange.max);
	mQwtScaleWidget->setTitle(mAxisunit);
	mQwtScaleWidget->setMargin(1);
	mQwtScaleWidget->setSpacing(0);
	mQwtScaleWidget->setBorderDist(0, 0);
	mQwtScaleWidget->show();
}

void  Axis::resizeEvent(QResizeEvent* sizeEvent)
{
	mQwtScaleWidget->resize(this->size());
}
void Axis::mouseDoubleClickEvent(QMouseEvent* e)
{
	if (e->button() != Qt::LeftButton)
		return;
	mAxisLable->setMinval(QString("%1").arg(axisvalrange.min));
	mAxisLable->setMaxval(QString("%1").arg(axisvalrange.max));
	mAxisLable->setAxisUnitval(QString("%1").arg(mAxisunit));
	mAxisLable->show();
}
void Axis::axiscloseEvent()
{
	valrange temp;
	temp.min = mAxisLable->getMinval();
	temp.max = mAxisLable->getMaxval();
	if (temp != axisvalrange && temp.min <= temp.max)
	{
		//emit sendAxisRang(temp.min, temp.max);
		axisvalrange = temp;
	}
	mAxisunit = mAxisLable->getAxisUnitval();
	mAxisLable->hide();
	_update();
}
#include "moc_Axis.cpp"
