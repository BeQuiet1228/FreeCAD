#pragma once
#include <QDialog>

namespace Ui {
	class NetworkClientDialog;
}

class NetworkClientDialog:public QDialog
{
	Q_OBJECT
public:
	NetworkClientDialog(QWidget *parent = 0);
	~NetworkClientDialog();

	enum State{
		REGISTER = 0,
		LOGIN
	};
private:
	Ui::NetworkClientDialog *ui;
public Q_SLOTS:
	//注册登录切换按钮
	void on_pushButton_clicked();
	//登录或者注册按钮被点击
	void on_pushButtonLogin_clicked();
Q_SIGNALS:
	void pushButtonClicked();
public:
	//设置获取链接地址和端口
	void getIpAndPort(QString& ip, QString& port);
	void setIpAndPort(const QString& ip, const QString& port);
	//设置获取账号密码
	void setUserNameAndPassword(const QString& userName,const QString& password);
	void getUserNameAndPassword(QString& userName, QString& password);
	void getUserNameAndPassword(QString& userName, QString& password_1,QString& password_2);
public:
	//状态
	State state;

};