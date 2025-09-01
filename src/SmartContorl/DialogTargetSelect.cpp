#include "DialogTargetSelect.h"
#include "ui_DialogTargetSelect.h"
DialogTargetSelect::DialogTargetSelect(QWidget* parent /*= 0*/)
	:ui(new Ui::DialogTargetSelect),index(-1)
{
	ui->setupUi(this);
}

DialogTargetSelect::~DialogTargetSelect()
{
	delete ui;
}

void DialogTargetSelect::on_pushButtonOk_clicked()
{
	if (ui->radioButton->isChecked())
		index = 0;
	else if (ui->radioButton_2->isChecked())
		index = 1;
	else
		index = 2;
	this->close();
}

#include "moc_DialogTargetSelect.cpp"