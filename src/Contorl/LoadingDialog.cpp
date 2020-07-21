#include "LoadingDialog.h"
#include "ui_LoadingDialog.h"
#include "QMovie"
LoadingDialog::LoadingDialog(QWidget *parent /*= 0*/)
	:QDialog(parent), ui(new Ui::LoadingDialog)
{
	ui->setupUi(this);
	QMovie *movie = new QMovie(":/image/loading.gif");
	movie->start();
	ui->label_2->setMovie(movie);

	this->setModal(true);
}

LoadingDialog::~LoadingDialog()
{

}

#include "moc_LoadingDialog.cpp"