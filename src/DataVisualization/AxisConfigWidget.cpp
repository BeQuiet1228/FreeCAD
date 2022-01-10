#include "AxisConfigWidget.h"
#include "ui_AxisConfigWidget.h"
DV::AxisConfigWidget::AxisConfigWidget(QWidget* parent/*=nullptr*/)
	:QWidget(parent),ui(new Ui::AxisConfigWidget)
{
	ui->setupUi(this);
	initUi();
}

DV::AxisConfigWidget::~AxisConfigWidget()
{

}

void DV::AxisConfigWidget::initUi()
{

}
#include "moc_AxisConfigWidget.cpp"