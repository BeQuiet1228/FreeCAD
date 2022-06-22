#include "DialogTargetSelect.h"
#include "ui_DialogTargetSelect.h"
DialogTargetSelect::DialogTargetSelect(QWidget* parent /*= 0*/)
	:ui(new Ui::DialogTargetSelect),index(0)
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
	else
		index = 1;
	this->close();
}

#include "moc_DialogTargetSelect.cpp"