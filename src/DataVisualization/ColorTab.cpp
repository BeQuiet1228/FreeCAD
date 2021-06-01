#include "ColorTab.h"
#include "qwt/qwt_scale_widget.h"
#include "qwt/qwt_scale_engine.h"
#include "qwt/qwt_color_map.h"
/**
* @brief  ColorTab::ColorTab 构造函数
* @param  QWidget * parent  
* @return   
*/
ColorTab::ColorTab(QWidget* parent) :QWidget(parent), scaleWidget(nullptr), scaleEngine(nullptr), style(0)
{
	setMinimumSize(QSize(0, 0));
	setMaximumSize(QSize(16777715,1677715));
	initUI();
}
/**
* @brief  ColorTab::~ColorTab 析构函数
* @return   
*/
ColorTab::~ColorTab()
{

}
/**
* @brief  ColorTab::initUI 初始化UI
* @return void  
*/
void ColorTab::initUI()
{
	//默认构造
	scaleWidget = new QwtScaleWidget(QwtScaleDraw::BottomScale, this);
	scaleWidget->setColorBarEnabled(true);
	scaleWidget->setColorBarWidth(20);
	scaleEngine = new QwtLinearScaleEngine;
	QwtInterval interval(0, 1);
	//添加颜色
	QwtLinearColorMap* colormap = new QwtLinearColorMap(Qt::darkBlue, Qt::darkRed);
	colormap->setMode(QwtLinearColorMap::Mode::FixedColors);
	{
		colormap->addColorStop(0.2, Qt::blue);
		colormap->addColorStop(0.4, Qt::cyan);
		colormap->addColorStop(0.6, Qt::yellow);
		colormap->addColorStop(0.8, Qt::red);
		scaleWidget->setColorMap(interval, colormap);
	}
	scaleWidget->setScaleDiv(scaleEngine->divideScale(0,1,5,6,0));
	scaleWidget->resize(this->size());
}
/**
* @brief  ColorTab::resizeEvent 大小转换
* @param  QResizeEvent * event  
* @return void  
*/
void ColorTab::resizeEvent(QResizeEvent * event)
{
	scaleWidget->resize(this->size());
}
/**
* @brief  ColorTab::changmoveColor 改变颜色
* @param  std::vector<float> & val  
* @param  std::vector<QColor> & colors  
* @return void  
*/
void ColorTab::changmoveColor(std::vector<float>& val, std::vector<QColor>& colors,const QColor& firstColor,const QColor& endColor)
{
	QwtInterval interval(0.0, 1.0);
	QwtLinearColorMap* colormap = new QwtLinearColorMap(firstColor, endColor);
	//colormap->setMode(QwtLinearColorMap::Mode::FixedColors);
	switch (style)
	{
	case 0:
		colormap->setMode(QwtLinearColorMap::Mode::FixedColors); break;
	case 1:
		colormap->setMode(QwtLinearColorMap::Mode::ScaledColors); break;
	}
	{
		/*colormap->addColorStop(0,firstColor);
		colormap->addColorStop(0.9, endColor);*/
		for (auto index = 0; index < val.size(); index++)
			colormap->addColorStop(val[index],colors[index]);
	}
	scaleWidget->setColorMap(interval, colormap);
}
/**
* @brief  ColorTab::GetColors
* @param  std::vector<float> vals  
* @return std::vector<QT_NAMESPACE::QColor>  
*/
std::vector<QColor> ColorTab::GetColors(std::vector<float> vals)
{
	std::vector<QColor> colors;
	colors.clear();
	QwtInterval interval(0.0,1.0);
	for (auto index = 0; index < vals.size();index++)
	{
		colors.push_back(scaleWidget->colorMap()->color(interval, vals[index]));
	}
	return colors;
}
/**
* @brief  ColorTab::setColors 设置颜色
* @param  std::vector<float> & vals  
* @param  std::vector<QColor> & colors  
* @return void  
*/
void ColorTab::setColors(std::vector<float>& vals, std::vector<QColor>& colors)
{
	QwtInterval interval(0.0f,1.0f);
	QwtLinearColorMap* colormap = new QwtLinearColorMap(*colors.begin(),*(colors.end()-1));
	switch (style)
	{
	case 0:
		colormap->setMode(QwtLinearColorMap::Mode::FixedColors); break;
	case 1:
		colormap->setMode(QwtLinearColorMap::Mode::ScaledColors); break;
	}
	for (auto index = 1; index < colors.size()-1;index++)
	{
		colormap->addColorStop(vals[index], colors[index]);
	}
	scaleWidget->setColorMap(interval, colormap);
}

/**
* @brief  ColorTab::setStyle
* @param  int s  
* @return void  
*/
void ColorTab::setColorStyle(int s)
{
	style = s;
}
#include "moc_ColorTab.cpp"