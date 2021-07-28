#include "VariateInputDialog.h"
#include "ui_VariateInputDialog.h"
#include "SmartContorlUI.h"
#include <iostream>
VariateInputDialog::VariateInputDialog(QWidget *parent /*= 0*/)
	:QDialog(parent), ui(new Ui::VariateInputDialog_UI)
{
	ui->setupUi(this);
	ui->label_5->hide();
	ui->stepsize->hide();
	this->setModal(true);
}

VariateInputDialog::~VariateInputDialog()
{

}

std::shared_ptr<VariateData> VariateInputDialog::getData()
{
	if (!data)
		data.reset(new VariateData);
	data->name = this->ui->lineEditName->text();
	data->max = this->ui->lineEditMax->text().toDouble();
	data->mini = this->ui->lineEditMini->text().toDouble();
	data->stepLength = this->ui->stepsize->text().toInt();
	return data;
}


void VariateInputDialog::on_pushButtonOk_clicked()
{
	std::cout << "ok" << std::endl;
	this->close();
	okClicked = true;
}

#include "moc_VariateInputDialog.cpp"
