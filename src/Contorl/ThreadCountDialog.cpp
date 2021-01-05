#include "ThreadCountDialog.h"
#include "ui_ThreadCountDialog.h"
ThreadCountDialog::ThreadCountDialog(QWidget *parent /*= 0*/)
	:QDialog(parent), ui(new Ui::ThreadCountDialog)
{
	ui->setupUi(this);
}

ThreadCountDialog::~ThreadCountDialog()
{

}

void ThreadCountDialog::on_pushButtonOk_clicked()
{
	okBuutonClicked = true;
	threadCount = ui->spinBoxThreadCount->value();
	this->close();
}

#include "moc_ThreadCountDialog.cpp"