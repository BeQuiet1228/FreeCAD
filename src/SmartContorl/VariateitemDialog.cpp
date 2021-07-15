#include "VariateitemDialog.h"
#include "SmartContorlUI.h"
#include "ui_VariateItemWidget.h"
VariateitemDialog::VariateitemDialog(QWidget* parent)
	:VariateItemWidget(parent)
{
	ui->label_3->		show();
	ui->labelCount->	show();
	ui->labelMode->		show();
	ui->label_8->		show();
}
VariateitemDialog::~VariateitemDialog()
{

}
void VariateitemDialog::setData(std::shared_ptr<VariateData> data)
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
#include "moc_VariateitemDialog.cpp"

