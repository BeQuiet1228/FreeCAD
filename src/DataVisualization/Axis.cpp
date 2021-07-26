#include "axis.h"
#include<QGridLayout>
#include"qwt/qwt_scale_engine.h"
#include"ScaleWidget.h"
#include<QMouseEvent>
#include"AxisLable.h"
#include "CustomConfig.h"
#include"C_encoding.h"
#include "TLabel.h"
#include<QFontMetrics>
Axis::Axis(QWidget* parent):
	/*QWidget(parent)*/
	ScaleWidget(parent)
{	//设置默认参数
	AxisNum = 5;
	mAxisunit = "X(x)";
	mAxisstyle = AxisBottom;
	axisvalrange.min = 0.0f;
	axisvalrange.max = 100.0f;
	/*mQwtScaleWidget = new ScaleWidget(this);*/
	//mQwtScaleWidget->resize(this->size());
	mAxisLable = new AxisLable();
	mAxisLable->setModal(true);
	mAxisLable->resize(300, 200);
	connect(mAxisLable, SIGNAL(signalCloseEvent()), this, SLOT(axiscloseEvent()));
	mTDialog = new TDialog();
	mTDialog->setModal(true);
	connect(mTDialog,SIGNAL(signalCloseEvent(bool)),this,SLOT(slotCloseEvent(bool)));
	islabel=true;
	isAxisdialog=true;
}
Axis::~Axis()
{
	delete mAxisLable;
	delete mTDialog;
}
void Axis::setAxisRange(double min, double max)
{
	if (min < max)
	{
		axisvalrange.min = min;
		axisvalrange.max = max;
		QwtLinearScaleEngine* mQwtLinearScaleEngine = new QwtLinearScaleEngine;
		setScaleDiv(mQwtLinearScaleEngine->divideScale(min, max, AxisNum, 5));
		setRange(min,max);
	}
}
void Axis::setAxisText(QString name)
{
	mAxisunit = name;
}
void Axis::setAxixStyle(Axisstyle style)
{
	mAxisstyle = style;
	switch (mAxisstyle)
	{
	case Axisleft:
	{
		setAlignment(QwtScaleDraw::LeftScale);
	}
		break;
	case AxisRight:
	{
		setAlignment(QwtScaleDraw::RightScale);
	}
		break;
	case AxisTop:
	{
		setAlignment(QwtScaleDraw::TopScale);
	}
		break;
	case AxisBottom: {
		setAlignment(QwtScaleDraw::BottomScale);
	}
		break;
	default:
		break;
	}
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
		unitFont = QString::fromStdString(axisGroup.getGroup("font").getValue("value"));
		
		
		//QFont unitFont;
		//QFont axisFont;
	}
	_update();
}
void Axis::_update()
{
	QFont mfont= font();
	mfont.setFamily(unitFont);
	setFont(mfont);
	//设置单位
	/*if (islabel)
	{
		QwtText mtext = title();
		QFont mfont = mtext.font();
		mfont.setFamily(unitFont);
		mfont.setPixelSize(mAxisunitSize);
		mtext.setColor(axisvalColor);
		mtext.setFont(mfont);
		mtext.setText(mAxisunit);
		setTitle(mtext);
	}*/
	//设置刻度
	{
		scaleDraw()->setAxisValColor(axisvalColor);
		scaleDraw()->setAxisColor(axisColor);
		scaleDraw()->setAxisValSize(axisvalSize);
	}
	{
		//调整大小
		QFont mfont;
		mfont.setPixelSize(axisvalSize);
		int ticklength = scaleDraw()->maxTickLength();
		int axislabelhight = scaleDraw()->maxLabelHeight(mfont);
		int axislabelwidth = scaleDraw()->maxLabelWidth(mfont);
		mfont.setPixelSize(mAxisunitSize);
		QFontMetrics fm(mfont);
		QRect rect = fm.boundingRect(mAxisunit);
		switch (mAxisstyle)
		{
		case Axisleft:
		case AxisRight:
		{
			int width = ticklength + axislabelwidth + rect.height() + 10;
			if (isColorBarEnabled())
				width += colorBarWidth();
			setMinimumWidth(width);
		}
		break;
		case AxisBottom:
		case AxisTop:
		{
			int height = ticklength + axislabelhight + rect.height() + 10;
			if (isColorBarEnabled())
				height += colorBarWidth();
			setMinimumHeight(height);
			
			
		}
		break;
		}
	}
	automatic();
}
void  Axis::resizeEvent(QResizeEvent* sizeEvent)
{
	//mQwtScaleWidget->resize(this->size());
	_update();
	//automatic();
}
void Axis::mouseDoubleClickEvent(QMouseEvent* e)
{
	if (e->button() != Qt::LeftButton)
		return;
#if 0
	if (!islabel && !isAxisdialog)
		return;
	QPointF pos=e->posF();
	QRectF left = QRectF(0.0, 0.0, this->width() / 2, this->height());
	QRectF right = QRectF(this->width() / 2, 0.0, this->width() / 2, this->height());
	QRectF top = QRectF(0.0,0.0,this->width(),this->height()/2);
	QRectF bottom = QRectF(0.0,this->height()/2,this->width(),this->height()/2);
	if (islabel && !isAxisdialog)
	{
		mTDialog->SetMsgtext(mAxisunit);
		mTDialog->show();
		return;
	}
	else if(!islabel&& isAxisdialog)
	{
		mAxisLable->setMinval(QString("%1").arg(axisvalrange.min));
		mAxisLable->setMaxval(QString("%1").arg(axisvalrange.max));
		mAxisLable->show();
		return;
	}
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
#endif
	//
	mAxisLable->setMinval(QString("%1").arg(axisvalrange.min));
	mAxisLable->setMaxval(QString("%1").arg(axisvalrange.max));
	mAxisLable->show();
}
void Axis::axiscloseEvent()
{
	valrange temp;
	temp.min = mAxisLable->getMinval();
	temp.max = mAxisLable->getMaxval();
	if (temp != axisvalrange && temp.min <= temp.max)
	{
		setAxisRange(temp.min, temp.max);
		emit sendAxisRang(temp.min, temp.max);
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
void Axis::setLabel(bool b) {
	islabel = b;
}
void Axis::setAxisdialog(bool b)
{
	isAxisdialog = b;
}
#include "moc_Axis.cpp"
