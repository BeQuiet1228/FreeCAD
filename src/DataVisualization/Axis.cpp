#include "axis.h"
#include<QGridLayout>
#include"qwt/qwt_scale_engine.h"
#include"ScaleWidget.h"
#include<QMouseEvent>
#include"AxisLable.h"
#include "CustomConfig.h"
#include"C_encoding.h"
#include "TLabel.h"
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
	//mGridLayout = new QGridLayout();
	connect(mAxisLable, SIGNAL(signalCloseEvent()), this, SLOT(axiscloseEvent()));
	//mGridLayout->setSpacing(0);
	mTDialog = new TDialog(this);
	mTDialog->setModal(true);
	connect(mTDialog,SIGNAL(signalCloseEvent(bool)),this,SLOT(slotCloseEvent(bool)));
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
	if (Config::GetInstance()->loadConfig())
	{
		auto Group = Config::GetInstance()->getRootGroup();
		auto axisGroup = Group.getGroup("axis");
		mAxisunitSize = atoi(axisGroup.getGroup("axisSize").getValue("value").c_str());
		axisColor = QStringToQColor(QString::fromStdString(axisGroup.getGroup("axisColor").getValue("value")));
		axisvalColor=QStringToQColor(QString::fromStdString( axisGroup.getGroup("axisvalColor").getValue("value")));
		axisvalSize = atoi( axisGroup.getGroup("axisvalSize").getValue("value").c_str());
	}
	_update();
}
void Axis::_update()
{
	QSize size = this->size();
	mQwtScaleWidget->setColorBarEnabled(false);
	QwtLinearScaleEngine* mQwtLinearScaleEngine = new QwtLinearScaleEngine;
	mQwtScaleWidget->setScaleDiv(mQwtLinearScaleEngine->divideScale(axisvalrange.min, axisvalrange.max, AxisNum, 5));
	mQwtScaleWidget->setRange(axisvalrange.min, axisvalrange.max);
	mQwtScaleWidget->setMargin(1);
	mQwtScaleWidget->setSpacing(1);
	mQwtScaleWidget->setBorderDist(0, 0);
	//设置单位
	{
		QwtText mtext = mQwtScaleWidget->title();
		QFont mfont = mtext.font();
		mfont.setPixelSize(mAxisunitSize);
		mtext.setColor(axisvalColor);
		mtext.setFont(mfont);
		mtext.setText(mAxisunit);
		mQwtScaleWidget->setTitle(mtext);
	}
	//设置刻度
	{
		mQwtScaleWidget->scaleDraw()->setAxisValColor(axisvalColor);
		mQwtScaleWidget->scaleDraw()->setAxisColor(axisColor);
		mQwtScaleWidget->scaleDraw()->setAxisValSize(axisvalSize);
	}
	switch (mAxisstyle)
	{
	case Axisleft:
	{
		mQwtScaleWidget->setAlignment(QwtScaleDraw::LeftScale);
		mQwtScaleWidget->scaleDraw()->move(this->width()-1,0);
		mQwtScaleWidget->scaleDraw()->setLength(size.height()-1);
		mQwtScaleWidget->scaleDraw()->setPenWidth(1);
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
		mQwtScaleWidget->scaleDraw()->move(0,0);
		mQwtScaleWidget->scaleDraw()->setLength(this->width()-1);
		mQwtScaleWidget->scaleDraw()->setPenWidth(1);
	}break;
	}

}
void  Axis::resizeEvent(QResizeEvent* sizeEvent)
{
	mQwtScaleWidget->resize(this->size());
	_update();
}
void Axis::mouseDoubleClickEvent(QMouseEvent* e)
{
	if (e->button() != Qt::LeftButton)
		return;
	
	QPointF pos=e->posF();
	QRectF left = QRectF(0.0, 0.0, this->width() / 2, this->height());
	QRectF right = QRectF(this->width() / 2, 0.0, this->width() / 2, this->height());
	QRectF top = QRectF(0.0,0.0,this->width(),this->height()/2);
	QRectF bottom = QRectF(0.0,this->height()/2,this->width(),this->height()/2);
	switch (mAxisstyle)
	{
	case Axisleft:
	{
		if (left.contains(pos))
		{
			mTDialog->SetMsgtext(mAxisunit);
			mTDialog->show();
		}
		else if (right.contains(pos))
		{
			mAxisLable->setMinval(QString("%1").arg(axisvalrange.min));
			mAxisLable->setMaxval(QString("%1").arg(axisvalrange.max));
			//mAxisLable->setAxisUnitval(QString("%1").arg(mAxisunit));
			mAxisLable->show();
		}
	}
		break;
	case AxisRight:
	{
		if (left.contains(pos))
		{
			mAxisLable->setMinval(QString("%1").arg(axisvalrange.min));
			mAxisLable->setMaxval(QString("%1").arg(axisvalrange.max));
			//mAxisLable->setAxisUnitval(QString("%1").arg(mAxisunit));
			mAxisLable->show();
		}
		else if(right.contains(pos))
		{
			mTDialog->SetMsgtext(mAxisunit);
			mTDialog->show();
		}
	}
		break;
	case AxisTop:
	{
		if (top.contains(pos))
		{
			mTDialog->SetMsgtext(mAxisunit);
			mTDialog->show();
		}
		else if (bottom.contains(pos))
		{
			mAxisLable->setMinval(QString("%1").arg(axisvalrange.min));
			mAxisLable->setMaxval(QString("%1").arg(axisvalrange.max));
			//mAxisLable->setAxisUnitval(QString("%1").arg(mAxisunit));
			mAxisLable->show();
		}
	}
		break;
	case AxisBottom:
	{
		if (top.contains(pos))
		{
			mAxisLable->setMinval(QString("%1").arg(axisvalrange.min));
			mAxisLable->setMaxval(QString("%1").arg(axisvalrange.max));
			//mAxisLable->setAxisUnitval(QString("%1").arg(mAxisunit));
			mAxisLable->show();
		}
		else if (bottom.contains(pos))
		{
			mTDialog->SetMsgtext(mAxisunit);
			mTDialog->show();
		}
	}
		break;
	}
}
void Axis::axiscloseEvent()
{
	valrange temp;
	temp.min = mAxisLable->getMinval();
	temp.max = mAxisLable->getMaxval();
	//mAxisunit = mAxisLable->getAxisUnitval();
	mAxisLable->hide();
	if (temp != axisvalrange && temp.min <= temp.max)
	{
		emit sendAxisRang(temp.min, temp.max);
		axisvalrange = temp;
	}
	_update();
}
void Axis::slotCloseEvent(bool isclose)
{
	mAxisunit = mTDialog->GetMsgText();
	if (isclose)
	{
		mTDialog->hide();
	}
	_update();
}
#include "moc_Axis.cpp"
