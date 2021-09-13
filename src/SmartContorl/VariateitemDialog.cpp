#include "VariateitemDialog.h"
#include "SmartContorlUI.h"
#include "ui_VariateItemWidget.h"
/**
* @brief VariateitemDialog::VariateitemDialog 构造
* @param QWidget * parent
* @return 
* @Time 2021/7/15
*/
VariateitemDialog::VariateitemDialog(QWidget* parent)
	:VariateItemWidget(parent)
{
	ui->label_3->		show();
	ui->labelCount->	show();
	ui->labelMode->		show();
	ui->label_8->		show();
	//
	
}
void VariateitemDialog::initUi()
{
	int MaxHeight = 0;
	MaxHeight += ui->labelMode->size().height();
	MaxHeight += ui->labelName->size().height();
	MaxHeight += ui->labelCount->size().height();
	MaxHeight += ui->labelMax->size().height();
	MaxHeight += ui->labelMini->size().height();
	MaxHeight += 2;
	this->setMaximumHeight(MaxHeight);
}
/**
* @brief VariateitemDialog::~VariateitemDialog 析构
* @return 
* @Time 2021/7/15
*/
VariateitemDialog::~VariateitemDialog()
{

}
/**
* @brief VariateitemDialog::setData 设置数据
* @param std::shared_ptr<VariateData> data
* @return void
* @Time 2021/7/15
*/
void VariateitemDialog::setData(std::shared_ptr<VariateData> data)
{
	this->ui->labelName->setText(data->name);
	this->ui->labelCount->setText(QString::number(data->stepLength));
	this->ui->labelMax->setText(QString::number(data->max));
	this->ui->labelMini->setText(QString::number(data->mini));
	switch (data->Mode)
	{
	case 1:
		this->ui->labelMode->setText("Mode1");
		break;
	case 2:
		this->ui->labelMode->setText("Mode2");
		break;
	}
}
#include "moc_VariateitemDialog.cpp"

