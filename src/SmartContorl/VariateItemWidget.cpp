#include "VariateItemWidget.h"
#include "ui_VariateItemWidget.h"
#include "SmartContorlUI.h"
VariateItemWidget::VariateItemWidget(QWidget *parent /*= 0*/)
	:QWidget(parent), ui(new Ui::VariateIteamWidget_UI)
{
	ui->setupUi(this);
}

VariateItemWidget::~VariateItemWidget()
{

}

void VariateItemWidget::setData(std::shared_ptr<VariateData> data)
{
	this->ui->labelName->setText(data->name);
	this->ui->labelCount->setText(QString::number(data->count));
	this->ui->labelMax->setText(QString::number(data->max));
	this->ui->labelMini->setText(QString::number(data->mini));
}

