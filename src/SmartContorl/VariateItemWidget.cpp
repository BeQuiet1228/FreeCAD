#include "VariateItemWidget.h"
#include "ui_VariateItemWidget.h"
#include "SmartContorlUI.h"
VariateItemWidget::VariateItemWidget(QWidget *parent /*= 0*/)
	:QWidget(parent), ui(new Ui::VariateIteamWidget_UI)
{
	ui->setupUi(this);
	//不显示值个数
	ui->label_3->hide();
	ui->labelCount->hide();
	ui->labelMode->hide();
	ui->label_8->hide();
}
void VariateItemWidget::initUi()
{
	int MaxHeight = 0;
	//MaxHeight += ui->labelMode->size().height();
	MaxHeight += ui->labelName->size().height();
	//MaxHeight += ui->labelCount->size().height();
	MaxHeight += ui->labelMax->size().height();
	MaxHeight += ui->labelMini->size().height();
	MaxHeight += 10;
	this->setMaximumHeight(MaxHeight);
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

