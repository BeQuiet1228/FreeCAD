#include "ScaleWidget.h"
#include <QMouseEvent>
#include "TLabel.h"
ScaleWidget::ScaleWidget(QWidget* parent):QwtScaleWidget(parent)
{

}
ScaleWidget::ScaleWidget(QwtScaleDraw::Alignment a, QWidget* parent):QwtScaleWidget(a,parent)
{

}
void ScaleWidget::setAlignment(QwtScaleDraw::Alignment alignment)
{
	QwtScaleWidget::setAlignment(alignment);
	mAlignment = alignment;
}
void ScaleWidget::resizeEvent(QResizeEvent* e)
{
	QWidget* wid=this->parentWidget();
	//QwtScaleWidget::resizeEvent(e);
}
void ScaleWidget::setRange(double min, double max)
{
	if(min<max)
	this->scaleDraw()->setRange(min, max);
}
void ScaleWidget::setAxisValColor(QColor color)
{
	this->scaleDraw()->setAxisValColor(color);
}
void ScaleWidget::automatic()
{
	switch (mAlignment)
	{
	case QwtScaleDraw::BottomScale:
	{
		setAlignment(QwtScaleDraw::BottomScale);
		scaleDraw()->move(0, 0);
		scaleDraw()->setLength(this->width() - 1);
		scaleDraw()->setPenWidth(1);
	}
		break;
	case QwtScaleDraw::TopScale:
	{
		setAlignment(QwtScaleDraw::TopScale);
		scaleDraw()->move(0,this->height()-1);
		scaleDraw()->setLength(this->width() - 1);
		scaleDraw()->setPenWidth(1);
	}
		break;
	case QwtScaleDraw::LeftScale:
	{
		setAlignment(QwtScaleDraw::LeftScale);
		scaleDraw()->move(this->width() - 1, 0);
		scaleDraw()->setLength(this->height() - 1);
		scaleDraw()->setPenWidth(1);
	}
		break;
	case QwtScaleDraw::RightScale:
	{
		setAlignment(QwtScaleDraw::RightScale);
		scaleDraw()->move(0, 0);
		scaleDraw()->setLength(this->height() - 1);
		scaleDraw()->setPenWidth(1);
	}
		break;
	}
}
void ScaleWidget::mouseDoubleClickEvent(QMouseEvent* e)
{
	/*if (e->button() != Qt::LeftButton)
		return;
	TDialog* mTDialog = new TDialog();
	mTDialog->setModal(true);
	mTDialog->show();*/
}
#include "moc_ScaleWidget.cpp"