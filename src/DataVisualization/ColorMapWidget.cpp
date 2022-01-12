#include "ColorMapWidget.h"
#include <QDebug>
#include "realTimewidget.h"
namespace DV {
	/**
	* @brief  ColorMapWidget::ColorMapWidget
	* @param  QWidget * parent
	* @return
	*/
	ColorMapWidget::ColorMapWidget(QWidget* parent) :QwtScaleWidget(parent), mrealTimewidget(nullptr)
	{
		isColse = true;
		min = 0;
		max = 1;
	}
	/**
	* @brief  ColorMapWidget::ColorMapWidget
	* @param  QwtScaleDraw::Alignment align
	* @param  QWidget * parent
	* @return
	*/
	ColorMapWidget::ColorMapWidget(QwtScaleDraw::Alignment align, QWidget* parent) :
		QwtScaleWidget(align, parent)
	{
		isColse = true;
		min = 0;
		max = 1;
	}
	/**
	* @brief  ColorMapWidget::~ColorMapWidget
	* @return
	*/
	ColorMapWidget::~ColorMapWidget()
	{
	}
	/**
	* @brief  ColorMapWidget::mouseDoubleClickEvent Êó±êË«»÷ÊÂ¼þ
	* @param  QMouseEvent * event
	* @return void
	*/
	void ColorMapWidget::mouseDoubleClickEvent(QMouseEvent* event)
	{
		//qDebug("QwtScaleWidget:mouseDoubleClicked");
		if (isColse)
		{
			//this->scaleDraw();
			//realTimewidget* newwidget = new realTimewidget();
			//newwidget->init(min, max);
			//connect(newwidget, SIGNAL(setcoloseEvent(bool)), this, SLOT(setclose(bool)));
			//connect(newwidget, SIGNAL(GetListDouble(std::vector<double>&)), this, SLOT(GetListDoubleslot(std::vector<double>&)));
			//newwidget->show();
			//isColse = false;
		}
	}
	/**
	* @brief  ColorMapWidget::setclose
	* @param  bool flag
	* @return void
	*/
	void ColorMapWidget::setclose(bool flag) {
		if (flag == true)
		{
			isColse = true;
		}
	}
	/**
	* @brief  ColorMapWidget::setValrange
	* @param  float rmin
	* @param  float rmax
	* @return void
	*/
	void ColorMapWidget::setValrange(float rmin, float rmax)
	{
		min = rmin;
		max = rmax;
	}
	void ColorMapWidget::GetListDoubleslot(std::vector<double>& listdouble)
	{
		emit GetListDouble(listdouble);
	}
};

#include "moc_ColorMapWidget.cpp"