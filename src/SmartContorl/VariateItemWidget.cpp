#include "VariateItemWidget.h"
#include "ui_VariateItemWidget.h"
#include "SmartContorlUI.h"
VariateItemWidget::VariateItemWidget(QWidget *parent /*= 0*/)
	:QWidget(parent), ui(new Ui::VariateIteamWidget_UI)
{
	ui->setupUi(this);
	//不显示值个数
	//ui->label_3->hide();
	//ui->labelCount->hide();
}

VariateItemWidget::~VariateItemWidget()
{

}

void VariateItemWidget::setData(std::shared_ptr<VariateData> data)
{
	this->ui->labelName->setText(data->name);
	this->ui->labelCount->setText(QString::number(data->stepLength));
	this->ui->labelMax->setText(QString::number(data->max));
	this->ui->labelMini->setText(QString::number(data->mini));
	switch (data->Mode)
	{
	case 1:
		//this->ui->labelMode->setText("步长计算");
		this->ui->labelMode->setText("Mode1");
		break;
	case 2:
		//this->ui->labelMode->setText("动态输入");
		this->ui->labelMode->setText("Mode2");
		break;
	}
}

