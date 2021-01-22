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
#include "MessageTransition.h"
ServiceUI::ServiceUI(QWidget *parent) :
QMainWindow(parent),
ui(new Ui::MainWindow)
{

	ui->setupUi(this);
	ui->pushButtonStop->setEnabled(false);
	closeB = false;

	ui->textEdit->setFont(QFont("", 12));


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

	this->inputText(tr("\n<---开始运行服务端--->\n"));

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

void ServiceUI::errorMessageBox(const std::string &error)
{
	QMessageBox mes;
	mes.setText(MessageTransition::gbkStdstringToQstring(error));
	mes.exec();
}

void ServiceUI::on_pushButtonClose_clicked()
{
	this->close();
}





void ServiceUI::inputText(QString str)
{
	static QTextCursor cursor = ui->textEdit->textCursor();
	cursor.insertText(str);
	ui->textEdit->setTextCursor(cursor);
}
#include "moc_ServiceUI.cpp"