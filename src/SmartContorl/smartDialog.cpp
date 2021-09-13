#include"smartDialog.h"
#include"ui_VariateInputDialog.h"
smartDialog::smartDialog(QWidget* parent):VariateInputDialog(parent)
{
	ui->label_5->show();
	ui->stepsize->show();
}
smartDialog::~smartDialog()
{

}

#include"moc_smartDialog.cpp"