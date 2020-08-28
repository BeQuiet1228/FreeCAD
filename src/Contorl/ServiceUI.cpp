#include "ServiceUI.h"
#include "ui_ServiceUI.h"
#include <QFileDialog>
#include <qfile.h>
#include <qmessagebox.h>
#include <QTextStream>
#include <qprocess.h>
#include <QDebug>
#include <QSystemTrayIcon>
#include <qtextcursor.h>
#include <qfont.h>
#include <QApplication>
#include "NetworkServer.h"
#include <iostream>
ServiceUI::ServiceUI(QWidget *parent) :
QMainWindow(parent),
ui(new Ui::MainWindow)
{

	ui->setupUi(this);
	ui->pushButtonStop->setEnabled(false);
	closeB = false;

	ui->textEdit->setFont(QFont("", 12));

	//新建QSystemTrayIcon对象
	mSysTrayIcon = new QSystemTrayIcon(this);
	//新建托盘要显示的icon
	QIcon icon = QIcon(":/icon.ico");
	//将icon设到QSystemTrayIcon对象中
	mSysTrayIcon->setIcon(icon);
	//当鼠标移动到托盘上的图标时，会显示此处设置的内容
	mSysTrayIcon->setToolTip(QObject::trUtf8("CHIPIC 服务端程序"));
	//给QSystemTrayIcon添加槽函数
	connect(mSysTrayIcon, SIGNAL(activated(QSystemTrayIcon::ActivationReason)), this, SLOT(activatedSysTrayIcon(QSystemTrayIcon::ActivationReason)));

	//建立托盘操作的菜单
	createActions();
	createMenu();
	//在系统托盘显示此对象
	mSysTrayIcon->show();

	auto service = NetworkServer::GetInstance();

	QString ip = service->getListeneAddress();

	QString port = QString::number(service->getListenePort());

	QString workPath = service->getWorkPath();

	ui->lineEditIP->setText(ip);
	ui->lineEditPort->setText(port);
	ui->lineEditPath->setText(workPath);
}

ServiceUI::~ServiceUI()
{
	if (mSysTrayIcon)
		delete mSysTrayIcon;
	delete ui;
}

void ServiceUI::on_pushButtonPath_clicked()
{
	QString Path = QFileDialog::getExistingDirectory(
		this, "配置工作路径",
		"/");
	ui->lineEditPath->setText(Path + "/");
}

void ServiceUI::on_pushButtonStart_clicked()
{

	if (ui->lineEditIP->text().isEmpty()){
		errorMessageBox("IP地址不能为空！");
		return;
	}
	if (ui->lineEditPort->text().isEmpty())
	{
		errorMessageBox("端口地址不能为空！");
		return;
	}
	if (ui->lineEditPath->text().isEmpty())
	{
		errorMessageBox("工作路径不能为空！");
		return;
	}
	
	auto service = NetworkServer::GetInstance();
	service->setAddressAndPort(ui->lineEditIP->text(), ui->lineEditPort->text().toInt());
	service->setWorkPath(ui->lineEditPath->text());
	service->startListene();

	this->inputText("\n<---开始运行服务端--->\n");

	ui->lineEditCHIPICPath->setEnabled(false);
	ui->lineEditIP->setEnabled(false);
	ui->lineEditPath->setEnabled(false);
	ui->lineEditPort->setEnabled(false);
	ui->pushButtonCHIPICPath->setEnabled(false);
	ui->pushButtonPath->setEnabled(false);
	ui->pushButtonStart->setEnabled(false);
	ui->pushButtonStop->setEnabled(true);

}

void ServiceUI::on_pushButtonStop_clicked()
{
	ui->lineEditCHIPICPath->setEnabled(true);
	ui->lineEditIP->setEnabled(true);
	ui->lineEditPath->setEnabled(true);
	ui->lineEditPort->setEnabled(true);
	ui->pushButtonCHIPICPath->setEnabled(true);
	ui->pushButtonPath->setEnabled(true);
	ui->pushButtonStart->setEnabled(true);
	ui->pushButtonStop->setEnabled(false);

	this->inputText("\n<---服务端已停止运行--->\n");
	auto service = NetworkServer::GetInstance();
	service->killService();
}

void ServiceUI::on_pushButtonCHIPICPath_clicked()
{
	QString fileName = QFileDialog::getOpenFileName(this, tr("配置CHIPIC路径"),
		"/home",
		tr("Images (*.exe)"));
	ui->lineEditCHIPICPath->setText(fileName);
}

void ServiceUI::errorMessageBox(const QString &error)
{
	QMessageBox mes;
	mes.setText(error);
	mes.exec();
}

void ServiceUI::on_pushButtonClose_clicked()
{
	exit(0);
}

void ServiceUI::closeEvent(QCloseEvent *event)
{

	//event->ignore();
	//隐藏主窗口
	//this->hide();

}


void ServiceUI::activatedSysTrayIcon(QSystemTrayIcon::ActivationReason reason)
{
	switch (reason){
	case QSystemTrayIcon::Trigger:
		//        mSysTrayIcon->showMessage(QObject::trUtf8("Message Title"),
		//                                  QObject::trUtf8("欢迎使用此程序"),
		//                                  QSystemTrayIcon::Information,
		//                                  1000);
		this->show();
	default:
		break;
	}
}

void ServiceUI::createActions()
{
	mShowMainAction = new QAction(QObject::trUtf8("显示主界面"), this);
	connect(mShowMainAction, SIGNAL(triggered()), this, SLOT(showMainAction()));

	mExitAppAction = new QAction(QObject::trUtf8("退出"), this);
	connect(mExitAppAction, SIGNAL(triggered()), this, SLOT(exitAppAction()));

}

void ServiceUI::createMenu()
{
	mMenu = new QMenu(this);
	mMenu->addAction(mShowMainAction);

	mMenu->addSeparator();

	mMenu->addAction(mExitAppAction);

	mSysTrayIcon->setContextMenu(mMenu);
}

void ServiceUI::showMainAction()
{
	this->show();
}

void ServiceUI::exitAppAction()
{
	exit(0);
}

void ServiceUI::inputText(QString str)
{
	static QTextCursor cursor = ui->textEdit->textCursor();
	cursor.insertText(str);
	ui->textEdit->setTextCursor(cursor);
}
#include "moc_ServiceUI.cpp"