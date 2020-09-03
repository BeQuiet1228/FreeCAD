#pragma once 
#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QCloseEvent>
#include <QSystemTrayIcon>
#include <qmenu.h>
#include <QAction>
namespace Ui {
	class MainWindow;
}

class ServiceUI : public QMainWindow
{
	Q_OBJECT

public:
	explicit ServiceUI(QWidget *parent = 0);
	~ServiceUI();

public Q_SLOTS:
	void on_pushButtonPath_clicked();

	void on_pushButtonStart_clicked();

	void on_pushButtonStop_clicked();

	void on_pushButtonCHIPICPath_clicked();

	void on_pushButtonClose_clicked();

	void inputText(QString str);


private:
	Ui::MainWindow *ui;
	void errorMessageBox(const std::string &error);
	bool closeB;

};

#endif // MAINWINDOW_H
