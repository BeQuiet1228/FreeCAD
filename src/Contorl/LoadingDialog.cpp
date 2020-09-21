#include "LoadingDialog.h"
#include "ui_LoadingDialog.h"
#include "QMovie"
#include "MessageTransition.h"
LoadingDialog::LoadingDialog(QWidget *parent /*= 0*/)
	:QDialog(parent), ui(new Ui::LoadingDialog)
{
	ui->setupUi(this);
	QMovie *movie = new QMovie(":/image/loading.gif");
	movie->start();
	ui->label_2->setMovie(movie);

	this->setModal(true);

	//背景透明
	//this->setAttribute(Qt::WA_TranslucentBackground);
	//无边框
	this->setWindowFlags(Qt::FramelessWindowHint);
}

LoadingDialog::~LoadingDialog()
{

}

/**
* @brief LoadingDialog::setText 设置提示信息
* @param const std::string & text
* @return void
*/
void LoadingDialog::setText(const std::string& text)
{
	QString t = MessageTransition::gbkStdstringToQstring(text);
	t = t.remove("@#$");
	ui->label->setText(t);
}

void LoadingDialog::show()
{
	isShow = true;
	QDialog::show();
}

void LoadingDialog::close()
{
	isShow = false;
	QDialog::close();
}

void LoadingDialog::closeEvent(QCloseEvent *event)
{
	QDialog::closeEvent(event);
	//emit dialogClose();
}

#include "moc_LoadingDialog.cpp"