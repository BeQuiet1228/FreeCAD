#include "NetworkClientLoginDailog.h"
#include "ui_NetworkClientLoginDailog.h"
NetworkClientDialog::NetworkClientDialog(QWidget *parent /*= 0*/)
	:QDialog(parent), ui(new Ui::NetworkClientDialog)
{
	ui->setupUi(this);
	this->state = LOGIN;
	ui->lineEditPassword_2->hide();
	ui->labelPassword_2->hide();
}

NetworkClientDialog::~NetworkClientDialog()
{

}

void NetworkClientDialog::on_pushButton_clicked()
{
	if (state == LOGIN)
	{
		state = REGISTER;
		ui->pushButtonLogin->setText(QString::fromLocal8Bit("注册"));
		ui->lineEditPassword_2->show();
		ui->labelPassword_2->show();

	}else{
		state = LOGIN;
		ui->pushButtonLogin->setText(QString::fromLocal8Bit("登录"));
		ui->lineEditPassword_2->hide();
		ui->labelPassword_2->hide();
	}
}

void NetworkClientDialog::on_pushButtonLogin_clicked()
{
	emit pushButtonClicked();
}
/**
* @brief NetworkClientDialog::getIpAndPort 获取ip跟端口
* @param QString & ip
* @param QString & port
* @return void
*/
void NetworkClientDialog::getIpAndPort(QString& ip, QString& port)
{
	ip = ui->lineEditIP->text();
	port = ui->lineEditPort->text();
}

/**
* @brief NetworkClientDialog::setIpAndPort 设置IP跟端口
* @param const QString & ip
* @param const QString & port
* @return void
*/
void NetworkClientDialog::setIpAndPort(const QString& ip, const QString& port)
{
	ui->lineEditIP->setText(ip);
	ui->lineEditPort->setText(port);
}

/**
* @brief NetworkClientDialog::setUserNameAndPassword 设置用户名跟密码
* @param const QString & userName
* @param const QString & password
* @return void
*/
void NetworkClientDialog::setUserNameAndPassword(const QString& userName, const QString& password)
{
	ui->lineEditAcount->setText(userName);
	ui->lineEditPassword->setText(password);
}

/**
* @brief NetworkClientDialog::getUserNameAndPassword 获取用户名与密码
* @param QString & userName
* @param QString & password
* @return void
*/
void NetworkClientDialog::getUserNameAndPassword(QString& userName, QString& password)
{
	userName = ui->lineEditAcount->text();
	password = ui->lineEditPassword->text();
}

/**
* @brief NetworkClientDialog::getUserNameAndPassword 获取用户名与密码
* @param QString & userName
* @param QString & password_1
* @param QString &password_2 确认密码
* @return void
*/
void NetworkClientDialog::getUserNameAndPassword(QString& userName, QString& password_1, QString& password_2)
{
	userName = ui->lineEditAcount->text();
	password_1 = ui->lineEditPassword->text();
	password_2 = ui->lineEditPassword_2->text();
}

#include "moc_NetworkClientLoginDailog.cpp"