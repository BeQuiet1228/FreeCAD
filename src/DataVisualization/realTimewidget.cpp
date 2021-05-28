#include "realTimewidget.h"
#include "ui_realTimewidget.h"
/**
* @brief  realTimewidget::realTimewidget
* @param  QWidget * parent  
* @return   
*/
realTimewidget::realTimewidget(QWidget* parent) :QWidget(parent), ui(new Ui::realTimewidget)
{
	ui->setupUi(this);
}
/**
* @brief  realTimewidget::~realTimewidget
* @return   
*/
realTimewidget::~realTimewidget()
{

}

#include "moc_realTimewidget.cpp"